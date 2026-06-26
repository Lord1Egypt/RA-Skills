from __future__ import annotations

import csv
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import AppConfig
from .filters import evaluate_title
from .http_client import HttpClient
from .models import AnnouncementRecord, DownloadPlan
from .repository import StateRepository


@dataclass(slots=True)
class RunSummary:
    pages_fetched: int = 0
    announcements_seen: int = 0
    announcements_eligible: int = 0
    download_candidates: int = 0
    downloaded: int = 0
    skipped_existing: int = 0
    failed_downloads: int = 0


class AnnualReportService:
    def __init__(
        self,
        config: AppConfig,
        repository: StateRepository,
        client: HttpClient,
        logger: logging.Logger,
    ) -> None:
        self.config = config
        self.repository = repository
        self.client = client
        self.logger = logger
        self._processed_announcement_ids: set[str] = set()
        self._eligible_announcement_ids: set[str] = set()

    def run(self) -> RunSummary:
        summary = RunSummary()
        self.repository.backfill_report_kinds(self.config.year)
        stock_codes = self._load_stock_codes()
        self.logger.info("Loaded %s unique A-share stock codes from %s", len(stock_codes), self.config.stock_csv_path)
        for stock_code in stock_codes:
            self._scan_stock_code(stock_code, summary)

        summary.announcements_eligible = len(self._eligible_announcement_ids)
        summary.download_candidates = len(self._eligible_announcement_ids)
        self.repository.export_manifest(
            self.config.manifest_path,
            self.repository.build_download_plans(self.config.year, self.config.output_dir),
        )
        self.logger.info("Run summary: %s", asdict(summary))
        return summary

    def _scan_stock_code(self, stock_code: str, summary: RunSummary) -> None:
        query = stock_code
        search_start_date = f"{self.config.year}-01-01"
        start_page = self.repository.begin_keyword_scan(stock_code)
        self.logger.info(
            "Scanning stock '%s' with query '%s' and sdate '%s' from page %s",
            stock_code,
            query,
            search_start_date,
            start_page,
        )

        page_num = start_page
        while True:
            if self.config.max_pages_per_keyword is not None and page_num > self.config.max_pages_per_keyword:
                self.logger.info(
                    "Reached max page limit %s for stock '%s'",
                    self.config.max_pages_per_keyword,
                    stock_code,
                )
                self.repository.advance_keyword_scan(stock_code, page_num - 1, has_more=False)
                break

            payload = self.client.search(
                keyword=query,
                page_num=page_num,
                sdate=search_start_date,
            )
            announcements = payload.get("announcements") or []
            total_pages = int(payload.get("totalpages") or 0)
            summary.pages_fetched += 1
            summary.announcements_seen += len(announcements)

            eligible_in_page = 0
            for item in announcements:
                record = self._to_record(item, query)
                self.repository.save_announcement(record)
                if record.is_eligible:
                    eligible_in_page += 1
                    self._eligible_announcement_ids.add(record.announcement_id)
                    if record.announcement_id in self._processed_announcement_ids:
                        continue
                    self._processed_announcement_ids.add(record.announcement_id)
                    outcome = self._download_record_immediately(record)
                    if outcome == "downloaded":
                        summary.downloaded += 1
                    elif outcome == "skipped":
                        summary.skipped_existing += 1
                    else:
                        summary.failed_downloads += 1
            self.logger.info(
                "Stock '%s' page %s/%s: %s records, %s eligible",
                stock_code,
                page_num,
                total_pages or "?",
                len(announcements),
                eligible_in_page,
            )

            has_more_flag = payload.get("hasMore")
            if isinstance(has_more_flag, bool):
                has_more = bool(announcements) and has_more_flag
            else:
                has_more = bool(announcements) and page_num < total_pages
            self.repository.advance_keyword_scan(stock_code, page_num, has_more=has_more)
            if not has_more:
                break
            page_num += 1

    def _download_record_immediately(self, record: AnnouncementRecord) -> str:
        plan = self.repository.build_download_plan_for_announcement(
            record.announcement_id,
            self.config.year,
            self.config.output_dir,
        )
        if plan is None:
            return "failed"
        return self._download_if_needed(plan)

    def _download_if_needed(self, plan: DownloadPlan) -> str:
        if self.config.dry_run:
            self.logger.info("Dry-run: would download %s -> %s", plan.pdf_url, plan.target_path)
            return "skipped"

        same_file_recorded = plan.downloaded and plan.download_path == str(plan.target_path)
        if not self.config.force_redownload and same_file_recorded and plan.target_path.exists():
            self.logger.info("Skipping existing download for %s", plan.sec_code)
            return "skipped"

        try:
            self.logger.info(
                "Downloading %s %s -> %s",
                plan.sec_code,
                plan.announcement_date,
                plan.target_path,
            )
            self.client.download_file(plan.pdf_url, plan.target_path)
            self.repository.mark_download_success(plan.announcement_id, plan.target_path)
            return "downloaded"
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Failed to download %s: %s", plan.sec_code, exc)
            self.repository.mark_download_failure(plan.announcement_id, str(exc))
            return "failed"

    def _to_record(self, item: dict[str, object], keyword: str) -> AnnouncementRecord:
        raw_title = str(item.get("announcementTitle") or "")
        filter_result = evaluate_title(raw_title, self.config.year)
        sec_code = str(item.get("secCode") or "").zfill(6)
        return AnnouncementRecord(
            announcement_id=str(item.get("announcementId") or ""),
            sec_code=sec_code,
            sec_name=str(item.get("secName") or ""),
            title_raw=raw_title,
            title_clean=filter_result.title_clean,
            title_body=filter_result.title_body,
            announcement_time_ms=int(item.get("announcementTime") or 0),
            adjunct_url=str(item.get("adjunctUrl") or ""),
            adjunct_type=str(item.get("adjunctType") or ""),
            org_id=(str(item["orgId"]) if item.get("orgId") is not None else None),
            query_keyword=keyword,
            report_kind=filter_result.report_kind,
            is_eligible=filter_result.is_eligible,
            reject_reason=filter_result.reason,
        )

    def _load_stock_codes(self) -> list[str]:
        csv_path = self._resolve_stock_csv_path()
        encodings = ("utf-8-sig", "utf-8", "gb18030", "gbk")
        last_error: Exception | None = None
        for encoding in encodings:
            try:
                with csv_path.open("r", encoding=encoding, newline="") as handle:
                    reader = csv.reader(handle)
                    next(reader, None)
                    codes = {
                        row[0].strip().zfill(6)
                        for row in reader
                        if row and self._is_a_share_code(row[0].strip())
                    }
                return sorted(codes)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        raise RuntimeError(f"Unable to read stock CSV: {csv_path}") from last_error

    def _resolve_stock_csv_path(self) -> Path:
        candidate = self.config.stock_csv_path
        if candidate.exists():
            return candidate
        for path in Path.cwd().rglob("上市公司基础信息.csv"):
            return path
        raise FileNotFoundError(f"Stock CSV not found: {candidate}")

    @staticmethod
    def _is_a_share_code(code: str) -> bool:
        code = code.strip().zfill(6)
        a_share_prefixes = (
            "000",
            "001",
            "002",
            "003",
            "300",
            "301",
            "600",
            "601",
            "603",
            "605",
            "688",
            "689",
        )
        return len(code) == 6 and code.isdigit() and code.startswith(a_share_prefixes)

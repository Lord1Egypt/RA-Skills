from __future__ import annotations

import csv
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .filters import evaluate_title
from .models import AnnouncementRecord, DownloadPlan, format_cninfo_date


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class StateRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._initialize()

    def close(self) -> None:
        self.connection.close()

    def begin_keyword_scan(self, keyword: str) -> int:
        now = utc_now_iso()
        row = self.connection.execute(
            "SELECT next_page, in_progress FROM search_progress WHERE keyword = ?",
            (keyword,),
        ).fetchone()
        if row is None:
            self.connection.execute(
                """
                INSERT INTO search_progress (
                    keyword, next_page, in_progress, last_started_at, updated_at
                ) VALUES (?, 1, 1, ?, ?)
                """,
                (keyword, now, now),
            )
            self.connection.commit()
            return 1

        if row["in_progress"]:
            self.connection.execute(
                """
                UPDATE search_progress
                SET last_started_at = ?, updated_at = ?
                WHERE keyword = ?
                """,
                (now, now, keyword),
            )
            self.connection.commit()
            return int(row["next_page"])

        self.connection.execute(
            """
            UPDATE search_progress
            SET next_page = 1, in_progress = 1, last_started_at = ?, updated_at = ?
            WHERE keyword = ?
            """,
            (now, now, keyword),
        )
        self.connection.commit()
        return 1

    def advance_keyword_scan(self, keyword: str, current_page: int, has_more: bool) -> None:
        now = utc_now_iso()
        if has_more:
            self.connection.execute(
                """
                UPDATE search_progress
                SET next_page = ?, in_progress = 1, updated_at = ?
                WHERE keyword = ?
                """,
                (current_page + 1, now, keyword),
            )
        else:
            self.connection.execute(
                """
                UPDATE search_progress
                SET next_page = 1, in_progress = 0, last_completed_at = ?, updated_at = ?
                WHERE keyword = ?
                """,
                (now, now, keyword),
            )
        self.connection.commit()

    def save_announcement(self, record: AnnouncementRecord) -> None:
        now = utc_now_iso()
        self.connection.execute(
            """
            INSERT INTO announcements (
                announcement_id,
                sec_code,
                sec_name,
                title_raw,
                title_clean,
                title_body,
                announcement_time_ms,
                adjunct_url,
                adjunct_type,
                org_id,
                query_keyword,
                report_kind,
                is_eligible,
                reject_reason,
                downloaded,
                download_path,
                download_error,
                last_downloaded_at,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL, NULL, ?, ?)
            ON CONFLICT(announcement_id) DO UPDATE SET
                sec_code = excluded.sec_code,
                sec_name = excluded.sec_name,
                title_raw = excluded.title_raw,
                title_clean = excluded.title_clean,
                title_body = excluded.title_body,
                announcement_time_ms = excluded.announcement_time_ms,
                adjunct_url = excluded.adjunct_url,
                adjunct_type = excluded.adjunct_type,
                org_id = excluded.org_id,
                query_keyword = excluded.query_keyword,
                report_kind = excluded.report_kind,
                is_eligible = excluded.is_eligible,
                reject_reason = excluded.reject_reason,
                updated_at = excluded.updated_at
            """,
            (
                record.announcement_id,
                record.sec_code,
                record.sec_name,
                record.title_raw,
                record.title_clean,
                record.title_body,
                record.announcement_time_ms,
                record.adjunct_url,
                record.adjunct_type,
                record.org_id,
                record.query_keyword,
                record.report_kind,
                int(record.is_eligible),
                record.reject_reason,
                now,
                now,
            ),
        )
        self.connection.commit()

    def build_download_plans(self, year: int, output_dir: Path) -> list[DownloadPlan]:
        rows = self.connection.execute(
            """
            SELECT
                announcement_id,
                sec_code,
                sec_name,
                title_clean,
                announcement_time_ms,
                report_kind,
                adjunct_url,
                downloaded,
                download_path,
                download_error
            FROM announcements
            WHERE is_eligible = 1
            ORDER BY sec_code ASC, report_kind ASC, announcement_time_ms DESC, announcement_id DESC
            """
        ).fetchall()

        plans: list[DownloadPlan] = []
        seen_code_kind_counts: dict[tuple[str, str], int] = {}
        for row in rows:
            sec_code = str(row["sec_code"]).zfill(6)
            announcement_date = format_cninfo_date(int(row["announcement_time_ms"]))
            report_kind = str(row["report_kind"] or "unknown")
            key = (sec_code, report_kind)
            seen_count = seen_code_kind_counts.get(key, 0)
            seen_code_kind_counts[key] = seen_count + 1
            if seen_count == 0:
                filename = f"{sec_code}_{year}_{report_kind}.pdf"
            else:
                filename = f"{sec_code}_{year}_{report_kind}_{row['announcement_id']}.pdf"
            plans.append(
                DownloadPlan(
                    announcement_id=str(row["announcement_id"]),
                    sec_code=sec_code,
                    sec_name=str(row["sec_name"]),
                    title_clean=str(row["title_clean"]),
                    announcement_date=announcement_date,
                    report_kind=report_kind,
                    pdf_url=f"https://static.cninfo.com.cn/{str(row['adjunct_url']).lstrip('/')}",
                    target_path=output_dir / filename,
                    downloaded=bool(row["downloaded"]),
                    download_path=row["download_path"],
                    download_error=row["download_error"],
                )
        )
        return plans

    def build_download_plan_for_announcement(
        self,
        announcement_id: str,
        year: int,
        output_dir: Path,
    ) -> DownloadPlan | None:
        row = self.connection.execute(
            """
            SELECT
                announcement_id,
                sec_code,
                sec_name,
                title_clean,
                announcement_time_ms,
                report_kind,
                adjunct_url,
                downloaded,
                download_path,
                download_error
            FROM announcements
            WHERE announcement_id = ? AND is_eligible = 1
            """,
            (announcement_id,),
        ).fetchone()
        if row is None:
            return None

        sec_code = str(row["sec_code"]).zfill(6)
        announcement_date = format_cninfo_date(int(row["announcement_time_ms"]))
        report_kind = str(row["report_kind"] or "unknown")
        rank = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM announcements
            WHERE is_eligible = 1
              AND sec_code = ?
              AND report_kind = ?
              AND (
                    announcement_time_ms > ?
                    OR (
                        announcement_time_ms = ?
                        AND announcement_id > ?
                    )
              )
            """,
            (
                sec_code,
                report_kind,
                int(row["announcement_time_ms"]),
                int(row["announcement_time_ms"]),
                str(row["announcement_id"]),
            ),
        ).fetchone()[0]

        if int(rank) == 0:
            filename = f"{sec_code}_{year}_{report_kind}.pdf"
        else:
            filename = f"{sec_code}_{year}_{report_kind}_{row['announcement_id']}.pdf"

        return DownloadPlan(
            announcement_id=str(row["announcement_id"]),
            sec_code=sec_code,
            sec_name=str(row["sec_name"]),
            title_clean=str(row["title_clean"]),
            announcement_date=announcement_date,
            report_kind=report_kind,
            pdf_url=f"https://static.cninfo.com.cn/{str(row['adjunct_url']).lstrip('/')}",
            target_path=output_dir / filename,
            downloaded=bool(row["downloaded"]),
            download_path=row["download_path"],
            download_error=row["download_error"],
        )

    def mark_download_success(self, announcement_id: str, target_path: Path) -> None:
        now = utc_now_iso()
        self.connection.execute(
            """
            UPDATE announcements
            SET downloaded = 1,
                download_path = ?,
                download_error = NULL,
                last_downloaded_at = ?,
                updated_at = ?
            WHERE announcement_id = ?
            """,
            (str(target_path), now, now, announcement_id),
        )
        self.connection.commit()

    def mark_download_failure(self, announcement_id: str, error: str) -> None:
        self.connection.execute(
            """
            UPDATE announcements
            SET downloaded = 0,
                download_error = ?,
                updated_at = ?
            WHERE announcement_id = ?
            """,
            (error, utc_now_iso(), announcement_id),
        )
        self.connection.commit()

    def export_manifest(self, manifest_path: Path, plans: Iterable[DownloadPlan]) -> None:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "sec_code",
                    "sec_name",
                    "announcement_id",
                    "announcement_date",
                    "report_kind",
                    "title_clean",
                    "pdf_url",
                    "target_path",
                    "downloaded",
                    "download_path",
                    "download_error",
                ],
            )
            writer.writeheader()
            for plan in plans:
                writer.writerow(
                    {
                        "sec_code": plan.sec_code,
                        "sec_name": plan.sec_name,
                        "announcement_id": plan.announcement_id,
                        "announcement_date": plan.announcement_date,
                        "report_kind": plan.report_kind,
                        "title_clean": plan.title_clean,
                        "pdf_url": plan.pdf_url,
                        "target_path": str(plan.target_path),
                        "downloaded": int(plan.downloaded),
                        "download_path": plan.download_path or "",
                        "download_error": plan.download_error or "",
                    }
                )

    def get_counts(self) -> dict[str, int]:
        total = self.connection.execute("SELECT COUNT(*) FROM announcements").fetchone()[0]
        eligible = self.connection.execute(
            "SELECT COUNT(*) FROM announcements WHERE is_eligible = 1"
        ).fetchone()[0]
        downloaded = self.connection.execute(
            "SELECT COUNT(*) FROM announcements WHERE downloaded = 1"
        ).fetchone()[0]
        return {"total": int(total), "eligible": int(eligible), "downloaded": int(downloaded)}

    def backfill_report_kinds(self, year: int) -> None:
        rows = self.connection.execute(
            """
            SELECT announcement_id, title_raw, title_clean
            FROM announcements
            WHERE is_eligible = 1
              AND (report_kind IS NULL OR report_kind = '' OR report_kind = 'unknown')
            """
        ).fetchall()
        for row in rows:
            title = str(row["title_raw"] or row["title_clean"] or "")
            report_kind = evaluate_title(title, year).report_kind or "unknown"
            self.connection.execute(
                "UPDATE announcements SET report_kind = ?, updated_at = ? WHERE announcement_id = ?",
                (report_kind, utc_now_iso(), str(row["announcement_id"])),
            )
        self.connection.commit()

    def _initialize(self) -> None:
        self.connection.executescript(
            """
            PRAGMA journal_mode = WAL;

            CREATE TABLE IF NOT EXISTS search_progress (
                keyword TEXT PRIMARY KEY,
                next_page INTEGER NOT NULL DEFAULT 1,
                in_progress INTEGER NOT NULL DEFAULT 0,
                last_started_at TEXT,
                last_completed_at TEXT,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS announcements (
                announcement_id TEXT PRIMARY KEY,
                sec_code TEXT NOT NULL,
                sec_name TEXT NOT NULL,
                title_raw TEXT NOT NULL,
                title_clean TEXT NOT NULL,
                title_body TEXT NOT NULL,
                announcement_time_ms INTEGER NOT NULL,
                adjunct_url TEXT NOT NULL,
                adjunct_type TEXT,
                org_id TEXT,
                query_keyword TEXT NOT NULL,
                report_kind TEXT,
                is_eligible INTEGER NOT NULL,
                reject_reason TEXT,
                downloaded INTEGER NOT NULL DEFAULT 0,
                download_path TEXT,
                download_error TEXT,
                last_downloaded_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_announcements_code_time
                ON announcements (sec_code, announcement_time_ms DESC, announcement_id DESC);

            CREATE INDEX IF NOT EXISTS idx_announcements_eligible
                ON announcements (is_eligible, sec_code, report_kind);
            """
        )
        columns = {
            row["name"] for row in self.connection.execute("PRAGMA table_info(announcements)").fetchall()
        }
        if "report_kind" not in columns:
            self.connection.execute("ALTER TABLE announcements ADD COLUMN report_kind TEXT")
        self.connection.commit()

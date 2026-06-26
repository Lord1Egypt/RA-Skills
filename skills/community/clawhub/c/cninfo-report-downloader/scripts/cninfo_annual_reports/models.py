from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


CNINFO_TIMEZONE = timezone(timedelta(hours=8))


@dataclass(slots=True, frozen=True)
class AnnouncementRecord:
    announcement_id: str
    sec_code: str
    sec_name: str
    title_raw: str
    title_clean: str
    title_body: str
    announcement_time_ms: int
    adjunct_url: str
    adjunct_type: str
    org_id: str | None
    query_keyword: str
    report_kind: str | None
    is_eligible: bool
    reject_reason: str | None


@dataclass(slots=True)
class DownloadPlan:
    announcement_id: str
    sec_code: str
    sec_name: str
    title_clean: str
    announcement_date: str
    report_kind: str
    pdf_url: str
    target_path: Path
    downloaded: bool
    download_path: str | None
    download_error: str | None


def format_cninfo_date(timestamp_ms: int) -> str:
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=CNINFO_TIMEZONE).strftime("%Y-%m-%d")

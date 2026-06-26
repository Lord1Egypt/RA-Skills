from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/134.0.0.0 Safari/537.36"
)


@dataclass(slots=True)
class AppConfig:
    year: int = 2025
    stock_csv_path: Path = Path("上市公司基础信息.csv")
    board_types: list[str] = field(default_factory=lambda: ["szb", "cyb", "hzb", "kcb"])
    page_size: int = 20
    sleep_seconds: float = 1.2
    timeout_seconds: float = 30.0
    max_retries: int = 5
    retry_backoff_seconds: float = 1.5
    output_dir: Path = Path("downloads") / "2025"
    runtime_dir: Path = Path("runtime")
    database_path: Path = Path("runtime") / "state.db"
    manifest_path: Path = Path("runtime") / "manifest_2025.csv"
    log_path: Path = Path("runtime") / "logs" / "cninfo_2025.log"
    dry_run: bool = False
    force_redownload: bool = False
    max_pages_per_keyword: int | None = None
    user_agent: str = DEFAULT_USER_AGENT
    referer: str = "https://www.cninfo.com.cn/new/fulltextSearch"

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

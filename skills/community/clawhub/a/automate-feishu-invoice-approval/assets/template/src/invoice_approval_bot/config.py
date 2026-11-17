from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, Optional

from .errors import ConfigurationError


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"{name} 必须是 true 或 false")


def load_dotenv(path: Path) -> None:
    """Load a small, shell-free subset of .env without overriding real env vars."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    project_dir: Path
    data_dir: Path
    database_path: Path
    mapping_path: Path
    invoice_schema_path: Path
    approval_code: Optional[str]
    auto_submit: bool
    dry_run: bool
    reply_enabled: bool
    min_confidence: float
    allowed_senders: FrozenSet[str]
    required_buyer_name: str
    required_buyer_tax_id: str
    codex_bin: str
    codex_model: Optional[str]
    codex_timeout_seconds: int
    lark_cli_bin: str
    lark_ready_timeout_seconds: int

    @classmethod
    def from_env(cls, project_dir: Optional[Path] = None) -> "Settings":
        root = (project_dir or Path(__file__).resolve().parents[2]).resolve()
        load_dotenv(root / ".env")

        def rooted(env_name: str, default: str) -> Path:
            value = Path(os.getenv(env_name, default))
            return value if value.is_absolute() else root / value

        min_confidence = float(os.getenv("INVOICE_MIN_CONFIDENCE", "0.90"))
        if not 0 <= min_confidence <= 1:
            raise ConfigurationError("INVOICE_MIN_CONFIDENCE 必须在 0 和 1 之间")

        allowed = frozenset(
            value.strip()
            for value in os.getenv("ALLOWED_SENDER_OPEN_IDS", "").split(",")
            if value.strip()
        )
        approval_code = os.getenv("LARK_APPROVAL_CODE", "").strip() or None
        codex_model = os.getenv("CODEX_MODEL", "").strip() or None
        required_buyer_name = os.getenv("REQUIRED_BUYER_NAME", "").strip()
        required_buyer_tax_id = os.getenv("REQUIRED_BUYER_TAX_ID", "").strip()
        if not required_buyer_name:
            raise ConfigurationError("请配置 REQUIRED_BUYER_NAME")
        if not required_buyer_tax_id:
            raise ConfigurationError("请配置 REQUIRED_BUYER_TAX_ID")

        return cls(
            project_dir=root,
            data_dir=rooted("DATA_DIR", "data"),
            database_path=rooted("DATABASE_PATH", "data/submissions.sqlite3"),
            mapping_path=rooted("APPROVAL_MAPPING_FILE", "config/approval_mapping.json"),
            invoice_schema_path=root / "config" / "invoice-output.schema.json",
            approval_code=approval_code,
            auto_submit=_parse_bool(os.getenv("BOT_AUTO_SUBMIT", "false"), "BOT_AUTO_SUBMIT"),
            dry_run=_parse_bool(os.getenv("BOT_DRY_RUN", "true"), "BOT_DRY_RUN"),
            reply_enabled=_parse_bool(
                os.getenv("BOT_REPLY_ENABLED", "true"), "BOT_REPLY_ENABLED"
            ),
            min_confidence=min_confidence,
            allowed_senders=allowed,
            required_buyer_name=required_buyer_name,
            required_buyer_tax_id=required_buyer_tax_id,
            codex_bin=os.getenv("CODEX_BIN", "codex"),
            codex_model=codex_model,
            codex_timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "180")),
            lark_cli_bin=os.getenv("LARK_CLI_BIN", "lark-cli"),
            lark_ready_timeout_seconds=int(
                os.getenv("LARK_READY_TIMEOUT_SECONDS", "30")
            ),
        )

    @property
    def images_dir(self) -> Path:
        return self.data_dir / "invoices"

    @property
    def codex_output_dir(self) -> Path:
        return self.data_dir / "codex-output"

    def ensure_directories(self) -> None:
        for path in (self.data_dir, self.images_dir, self.codex_output_dir):
            path.mkdir(mode=0o700, parents=True, exist_ok=True)

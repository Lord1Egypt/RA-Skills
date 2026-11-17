from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from pathlib import Path

from .config import Settings
from .errors import BotError
from .mapping import load_mapping
from .service import InvoiceApprovalService
from .storage import SubmissionStore


def _settings() -> Settings:
    return Settings.from_env()


def command_validate(settings: Settings) -> int:
    failures = []
    for binary in (settings.lark_cli_bin, settings.codex_bin):
        if not shutil.which(binary):
            failures.append(f"找不到命令：{binary}")
    try:
        mapping = load_mapping(settings.mapping_path)
    except BotError as exc:
        failures.append(str(exc))
        mapping = {}
    approval_code = settings.approval_code or str(mapping.get("approval_code", ""))
    if not approval_code or approval_code.startswith("请替换"):
        failures.append("尚未配置真实 approval_code")
    if not settings.invoice_schema_path.exists():
        failures.append(f"缺少 Codex 输出 schema：{settings.invoice_schema_path}")

    summary = {
        "project_dir": str(settings.project_dir),
        "mapping_path": str(settings.mapping_path),
        "database_path": str(settings.database_path),
        "auto_submit": settings.auto_submit,
        "dry_run": settings.dry_run,
        "reply_enabled": settings.reply_enabled,
        "min_confidence": settings.min_confidence,
        "sender_allowlist_count": len(settings.allowed_senders),
        "required_buyer_name_configured": bool(settings.required_buyer_name),
        "required_buyer_tax_id_configured": bool(settings.required_buyer_tax_id),
        "ok": not failures,
        "failures": failures,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


def command_records(settings: Settings, limit: int) -> int:
    settings.ensure_directories()
    store = SubmissionStore(settings.database_path)
    try:
        print(json.dumps(store.recent(limit), ensure_ascii=False, indent=2))
    finally:
        store.close()
    return 0


def command_process_event(settings: Settings, path: Path) -> int:
    event = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(event, dict):
        raise BotError("事件文件必须包含一个 JSON 对象")
    service = InvoiceApprovalService(settings)
    service.process_event(event)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="飞书发票识别自动提交审批助手")
    parser.add_argument(
        "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"]
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run", help="持续监听飞书图片消息")
    subparsers.add_parser("validate", help="检查本地配置（不会提交审批）")
    records = subparsers.add_parser("records", help="查看最近的处理记录")
    records.add_argument("--limit", type=int, default=20)
    process_event = subparsers.add_parser(
        "process-event", help="处理一个本地事件 JSON，便于联调"
    )
    process_event.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    try:
        settings = _settings()
        if args.command == "validate":
            return command_validate(settings)
        if args.command == "records":
            return command_records(settings, args.limit)
        if args.command == "process-event":
            return command_process_event(settings, args.path)
        service = InvoiceApprovalService(settings)
        service.run_forever()
        return 0
    except KeyboardInterrupt:
        return 130
    except (BotError, OSError, ValueError, json.JSONDecodeError) as exc:
        logging.getLogger(__name__).error("%s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())

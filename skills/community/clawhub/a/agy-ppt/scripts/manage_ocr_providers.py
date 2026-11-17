#!/usr/bin/env python3
"""Inspect and manage the Phase 15 OCR provider configuration."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ocr_providers import (  # noqa: E402
    OCRConfigurationStore, OCRError, OCRProviderManager, TesseractProvider,
    tesseract_validation_probe,
)


def _default_user_root() -> Path:
    configured = os.environ.get("XDG_CONFIG_HOME")
    return Path(configured) if configured else Path.home() / ".config"


def _manager(args: argparse.Namespace) -> OCRProviderManager:
    provider = TesseractProvider()
    return OCRProviderManager(
        {provider.provider_id: provider},
        OCRConfigurationStore(args.project_root, args.user_config_root),
        validation_probes={"tesseract": tesseract_validation_probe},
    )


def _emit(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--user-config-root", type=Path, default=_default_user_root())
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    show = sub.add_parser("show")
    show.add_argument("--provider", dest="explicit")
    validate = sub.add_parser("validate")
    validate.add_argument("--provider")
    validate.add_argument("--language", action="append", default=[])
    set_parser = sub.add_parser("set")
    set_parser.add_argument("--scope", choices=("project", "user"), required=True)
    set_parser.add_argument("--provider", required=True)
    fallback = set_parser.add_mutually_exclusive_group()
    fallback.add_argument("--allow-fallback", action="store_true", dest="allow_fallback")
    fallback.add_argument("--no-allow-fallback", action="store_false", dest="allow_fallback")
    set_parser.set_defaults(allow_fallback=None)
    unset = sub.add_parser("unset")
    unset.add_argument("--scope", choices=("project", "user"), required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = _manager(args)
    try:
        if args.command == "list":
            _emit({"providers": manager.list_providers()})
        elif args.command == "show":
            _emit(manager.effective(explicit=args.explicit).to_dict())
        elif args.command == "validate":
            _emit(manager.validate(provider_id=args.provider, languages=tuple(args.language)))
        elif args.command == "set":
            _emit({"configuration": manager.set(args.scope, args.provider, allow_fallback=args.allow_fallback).to_dict(), "scope": args.scope})
        else:
            _emit({"removed": manager.unset(args.scope), "scope": args.scope})
        return 0
    except OCRError as exc:
        _emit({"error_code": exc.error_code, "message": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

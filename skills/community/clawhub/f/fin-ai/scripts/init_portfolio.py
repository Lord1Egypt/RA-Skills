#!/usr/bin/env python3
"""Initialize a user portfolio data directory for portfolio-workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import (
    DEFAULT_PROFILE,
    USER_DATA_ROOT,
    bootstrap_portfolio_dir,
    resolve_portfolio_dir,
    write_user_settings,
)


def init_portfolio(
    *,
    portfolio_dir: Path | None = None,
    profile: str | None = None,
    set_default: bool = True,
) -> dict[str, str]:
    resolved_profile = profile or DEFAULT_PROFILE
    resolved_portfolio_dir = resolve_portfolio_dir(
        portfolio_dir=portfolio_dir,
        profile=resolved_profile,
        prefer_repo=False,
    )
    bootstrap_portfolio_dir(resolved_portfolio_dir)
    settings_path = None
    default_updated = False
    settings_warning = ""
    if set_default:
        try:
            settings_path = write_user_settings(
                {
                    "default_profile": resolved_profile,
                    "default_portfolio_dir": str(resolved_portfolio_dir),
                }
            )
            default_updated = True
        except Exception as exc:
            settings_warning = f"写入默认用户配置失败（{exc.__class__.__name__}）"
    return {
        "profile": resolved_profile,
        "portfolio_dir": str(resolved_portfolio_dir),
        "config_path": str(resolved_portfolio_dir / "config.json"),
        "holdings_dir": str(resolved_portfolio_dir / "holdings"),
        "snapshots_dir": str(resolved_portfolio_dir / "snapshots"),
        "user_data_root": str(USER_DATA_ROOT),
        "settings_path": str(settings_path) if settings_path else "",
        "default_updated": "true" if default_updated else "false",
        "settings_warning": settings_warning,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="初始化 portfolio-workflows 的用户数据目录。")
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="用户数据 profile 名，默认 default")
    parser.add_argument("--portfolio-dir", help="显式指定 portfolio 数据目录")
    parser.add_argument("--no-set-default", action="store_true", help="只初始化目录，不写入默认用户配置")
    args = parser.parse_args()

    result = init_portfolio(
        portfolio_dir=Path(args.portfolio_dir).expanduser() if args.portfolio_dir else None,
        profile=args.profile,
        set_default=not args.no_set_default,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

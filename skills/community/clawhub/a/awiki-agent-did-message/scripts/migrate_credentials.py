"""Migrate legacy flat-file credentials into the indexed directory layout.

Usage:
    uv run python scripts/migrate_credentials.py
    uv run python scripts/migrate_credentials.py --credential default

[INPUT]: credential_migration
[OUTPUT]: JSON migration summary
[POS]: Standalone migration CLI for upgrading local credential storage

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import argparse
import json
import logging

from credential_migration import migrate_legacy_credentials
from utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """CLI entry point."""
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(
        description="Migrate legacy flat-file credentials into the new layout",
    )
    parser.add_argument(
        "--credential",
        type=str,
        default=None,
        help="Only migrate a specific credential name",
    )
    args = parser.parse_args()

    logger.info("migrate_credentials CLI started credential=%s", args.credential)
    result = migrate_legacy_credentials(args.credential)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

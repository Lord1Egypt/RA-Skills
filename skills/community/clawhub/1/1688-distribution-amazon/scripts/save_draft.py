"""Compatibility entrypoint for saving a Dianxiaobao localSave draft.

The canonical script is release_product.py. This alias exists because some
agents infer a save_draft.py name from the Chinese step label.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts import release_product


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args:
        print("Usage: python scripts/save_draft.py <session_dir>", file=sys.stderr)
        return 1
    return release_product.main_with_args([args[0], "--release-type", "localSave", *args[1:]])


if __name__ == "__main__":
    sys.exit(main())

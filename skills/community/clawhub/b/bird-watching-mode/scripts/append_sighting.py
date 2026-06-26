#!/usr/bin/env python3
"""Append one observation to workspace/bird.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from bird_json_util import load_doc, save_doc, utc_now_iso, workspace_bird_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a bird sighting to workspace/bird.json",
        epilog="When called by an agent: absolute path for this script, --workspace, and --image if set.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Absolute path to project root (contains workspace/)",
    )
    parser.add_argument("--species", required=True, help="Species label (any language)")
    parser.add_argument("--notes", default="", help="Free text notes")
    parser.add_argument(
        "--source",
        choices=("text", "photo"),
        default="text",
        help="How the record was obtained",
    )
    parser.add_argument("--image", default="", help="Absolute path to image file if source=photo")
    parser.add_argument(
        "--time",
        dest="time_utc",
        default="",
        help="ISO 8601 timestamp (default: now UTC)",
    )
    parser.add_argument(
        "--birdid-stdout",
        default="",
        help="Optional raw BirdID CLI output to store on the row",
    )
    args = parser.parse_args()
    ws: Path = args.workspace

    doc = load_doc(ws)
    obs: Dict[str, Any] = {
        "time_utc": args.time_utc.strip() or utc_now_iso(),
        "species": args.species.strip(),
        "notes": args.notes.strip(),
        "source": args.source,
        "image_path": args.image.strip() or None,
        "birdid_stdout": args.birdid_stdout.strip() or None,
    }
    doc.setdefault("observations", []).append(obs)
    save_doc(ws, doc)
    print(workspace_bird_path(ws))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

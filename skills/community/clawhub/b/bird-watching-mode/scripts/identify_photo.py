#!/usr/bin/env python3
"""Run BirdID identify using region from workspace/bird.json; print stdout for the agent."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from bird_json_util import infer_country_code, load_doc, save_doc, utc_now_iso, workspace_bird_path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def superpicky_skill_root() -> Path:
    env = os.environ.get("SUPERPICKY_CLI_SKILL", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return (skill_root().parent / "superpicky-cli").resolve()


def birdid_cmd_for_region(
    image: Path,
    region: Optional[Dict[str, Any]],
    *,
    top: int,
    extra_args: List[str],
) -> List[str]:
    root = superpicky_skill_root()
    run_sh = root / "scripts" / "run.sh"
    cmd: List[str] = [str(run_sh), "--birdid", "identify", f"-t{top}", str(image)]
    if region:
        kind = (region.get("kind") or "").strip()
        code = (region.get("code") or "").strip()
        parent = (region.get("parent") or "").strip()
        cc = infer_country_code(region)
        if kind == "country" and code:
            cmd.extend(["-c", code])
        elif code:
            cmd.extend(["-c", cc])
            if kind == "region" or ("-" in code and parent):
                cmd.extend(["-r", code])
    cmd.extend(extra_args)
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="BirdID identify using bird.json region",
        epilog="When called by an agent: absolute path for this script, --workspace, and the image file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Absolute path to project root (contains workspace/)",
    )
    parser.add_argument("image", type=Path, help="Absolute path to image file")
    parser.add_argument("-t", "--top", type=int, default=5, help="BirdID -t")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append a sighting with birdid_stdout; species empty unless --append-species",
    )
    parser.add_argument(
        "--append-species",
        default="",
        help="With --append, set species field",
    )
    parser.add_argument(
        "extra",
        nargs="*",
        help="Extra args passed to birdid identify (e.g. --no-yolo)",
    )
    args = parser.parse_args()
    ws: Path = args.workspace
    img: Path = args.image.expanduser().resolve()
    if not img.is_file():
        print(f"not a file: {img}", file=sys.stderr)
        return 2

    doc = load_doc(ws)
    region = doc.get("region")
    r: Optional[Dict[str, Any]] = region if isinstance(region, dict) else None
    if r is None:
        print("warning: bird.json has no region; running without -c/-r", file=sys.stderr)

    cmd = birdid_cmd_for_region(img, r, top=args.top, extra_args=list(args.extra))
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        return proc.returncode

    if args.append:
        out = ((proc.stdout or "") + (proc.stderr or "")).strip()
        obs = {
            "time_utc": utc_now_iso(),
            "species": args.append_species.strip(),
            "notes": "",
            "source": "photo",
            "image_path": str(img),
            "birdid_stdout": out or None,
        }
        doc.setdefault("observations", []).append(obs)
        save_doc(ws, doc)
        print(f"appended -> {workspace_bird_path(ws)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

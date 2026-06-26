# pyright: reportMissingImports=false
import argparse
import os
import sys
from datetime import datetime

import bpy  # type: ignore

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import compat  # type: ignore  # noqa: E402


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _log(fp, msg: str) -> None:
    fp.write(msg.rstrip() + "\n")
    fp.flush()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--out_glb", required=True)
    parser.add_argument("--out_fbx", default="")
    parser.add_argument("--out_usdc", default="")
    parser.add_argument("--log", default="run-log.txt")
    argv = sys.argv
    if "--" in argv:
        idx = argv.index("--")
        argv = argv[idx + 1:]  # type: ignore[index]
    else:
        argv = []
    args = parser.parse_args(argv)

    _ensure_dir(os.path.dirname(args.out_glb) or ".")
    if args.out_fbx:
        _ensure_dir(os.path.dirname(args.out_fbx) or ".")
    if args.out_usdc:
        _ensure_dir(os.path.dirname(args.out_usdc) or ".")
    _ensure_dir(os.path.dirname(args.log) or ".")

    with open(args.log, "a", encoding="utf-8") as lf:
        _log(lf, f"[export] {datetime.utcnow().isoformat()}Z")
        _log(lf, f"[export] blender={compat.blender_version_string()}")
        _log(lf, f"[export] blend={args.blend}")
        _log(lf, f"[export] out_glb={args.out_glb}")
        if args.out_fbx:
            _log(lf, f"[export] out_fbx={args.out_fbx}")
        if args.out_usdc:
            _log(lf, f"[export] out_usdc={args.out_usdc}")

        bpy.ops.wm.open_mainfile(filepath=args.blend)

        # GLB (required)
        compat.export_glb(args.out_glb)
        _log(lf, f"[export] wrote={args.out_glb}")

        # FBX (optional)
        if args.out_fbx:
            compat.export_fbx(args.out_fbx)
            _log(lf, f"[export] wrote={args.out_fbx}")

        # USDC (optional)
        # Note: USD format is generally inferred from file extension.
        if args.out_usdc:
            compat.export_usd_best_effort(args.out_usdc)
            _log(lf, f"[export] wrote={args.out_usdc}")

        _log(lf, "[export] ok")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

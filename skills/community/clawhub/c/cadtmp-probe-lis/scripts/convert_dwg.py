#!/usr/bin/env python3
"""Convert DWG/DWT files to DXF using the vendored ezdwg converter."""
from __future__ import annotations

import argparse
import json
import os
import resource
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VENDOR_DIR = SCRIPT_DIR.parent / "vendor"
if VENDOR_DIR.is_dir():
    sys.path.insert(0, str(VENDOR_DIR))

SUPPORTED_SUFFIXES = {".dwg", ".dwt"}

from cad_common import peak_rss_mb
from cad_preflight import preflight_file
def start_watchdog(cap_mb: int) -> str:
    try:
        sys.path.insert(0, str(SCRIPT_DIR))
        import mem_guard

        mem_guard.start(cap_mb, name="dwg转换内存闸")
        return f"watchdog:{cap_mb}MB"
    except Exception as exc:
        return f"watchdog-failed:{exc}"

def collect_files(paths: list[str], recursive: bool) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            files.extend(
                p for p in path.glob(pattern) if p.suffix.lower() in SUPPORTED_SUFFIXES
            )
        elif path.exists():
            files.append(path)
    return sorted(dict.fromkeys(files))

def resolve_output(src: Path, out_arg: str | None, multiple: bool) -> Path:
    if out_arg is None:
        return Path.cwd() / (src.stem + ".dxf")
    out = Path(out_arg)
    if not multiple and out.suffix.lower() == ".dxf":
        return out
    return out / (src.stem + ".dxf")

def convert_one(src: Path, out: Path, args: argparse.Namespace) -> dict:
    if out.exists() and not args.overwrite:
        return {
            "ok": True,
            "status": "exists",
            "input": str(src),
            "output": str(out),
            "note": "已存在，未变更；如需覆盖请加 --overwrite",
        }

    from ezdwg.convert import to_dxf

    result = to_dxf(
        str(src),
        str(out),
        types=args.types,
        dxf_version=args.dxf_version,
        strict=args.strict,
        include_unsupported=args.include_unsupported,
        preserve_colors=not args.no_colors,
        modelspace_only=args.modelspace_only,
        explode_dimensions=not args.native_dimensions,
        flatten_inserts=args.flatten_inserts,
        dim_block_policy=args.dim_block_policy,
    )
    return {
        "ok": True,
        "status": "converted",
        "input": str(src),
        "output": str(out),
        "total_entities": result.total_entities,
        "written_entities": result.written_entities,
        "skipped_entities": result.skipped_entities,
        "skipped_by_type": result.skipped_by_type,
    }

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(
        description="Convert DWG/DWT to DXF with vendored ezdwg (no CAD software required)."
    )
    parser.add_argument("paths", nargs="+", help="DWG/DWT file(s) or folder(s)")
    parser.add_argument("--out", help="Output DXF file, or directory for batches")
    parser.add_argument("--recursive", action="store_true", help="Search folders recursively")
    parser.add_argument(
        "--dxf-version",
        default="R2010",
        help="DXF version for ezdxf.new(), e.g. R2000/R2004/R2010/R2018 (default: R2010)",
    )
    parser.add_argument("--types", help='Entity filter passed to query(), e.g. "LINE ARC LWPOLYLINE"')
    parser.add_argument("--strict", action="store_true", help="Fail if any entity cannot be converted")
    parser.add_argument(
        "--include-unsupported",
        action="store_true",
        help="Also query unsupported entity types (keeps skip reporting)",
    )
    parser.add_argument("--no-colors", action="store_true", help="Skip DWG color resolution for speed")
    parser.add_argument("--modelspace-only", action="store_true", help="Export model space entities only")
    parser.add_argument(
        "--native-dimensions",
        action="store_true",
        help="Keep DIMENSION entities instead of exploding them to primitives (default: explode)",
    )
    parser.add_argument(
        "--flatten-inserts",
        action="store_true",
        help="Explode INSERT/MINSERT references into primitives in model space",
    )
    parser.add_argument(
        "--dim-block-policy",
        choices=("smart", "legacy"),
        default="smart",
        help="Anonymous dimension block INSERT handling policy",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output DXF files")
    parser.add_argument(
        "--max-file-mb",
        type=int,
        default=200,
        help="Entry gate: refuse files larger than this unless --allow-big (default: 200)",
    )
    parser.add_argument("--allow-big", action="store_true", help="Convert files larger than --max-file-mb")
    parser.add_argument("--cap-mb", type=int, default=int(os.environ.get("CAD_MEM_LIMIT_MB", "4096")),
                        help="Watchdog memory cap in MB (default: 4096)")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    cap_state = start_watchdog(args.cap_mb)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    files = collect_files(args.paths, args.recursive)
    if not files:
        print("No .dwg or .dwt files found.")
        return 1

    results: list[dict] = []
    for src in files:
        pf = preflight_file(src)
        if not pf.get("ok"):
            results.append({
                "ok": False,
                "status": "skipped",
                "input": str(src),
                "output": str(resolve_output(src, args.out, len(files) > 1)),
                "error": pf.get("reason", "快速失败：输入不是可识别的 DWG/DXF"),
            })
            continue
        mb = src.stat().st_size / 1048576.0
        out = resolve_output(src, args.out, len(files) > 1)
        if mb > args.max_file_mb and not args.allow_big:
            results.append({
                "ok": False,
                "status": "too-big",
                "input": str(src),
                "output": str(out),
                "error": f"文件 {mb:.0f}MB 超过入口上限 {args.max_file_mb}MB，需加 --allow-big",
            })
            continue
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            results.append(convert_one(src, out, args))
        except Exception as exc:
            results.append({
                "ok": False,
                "status": "error",
                "input": str(src),
                "output": str(out),
                "error": f"{type(exc).__name__}: {exc}",
            })

    print(f"[dwg转换内存闸] cap={cap_state} 已用峰值 RSS={peak_rss_mb()}MB", file=sys.stderr)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            if item.get("status") == "exists":
                print(f"已存在，未变更: {item['output']}")
            elif not item.get("ok"):
                print(f"失败: {item['input']} -> {item['output']}: {item.get('error')}")
            else:
                print(f"input: {item['input']}")
                print(f"output: {item['output']}")
                print(
                    "total_entities: {total}  written_entities: {written}  skipped_entities: {skipped}".format(
                        total=item.get("total_entities"),
                        written=item.get("written_entities"),
                        skipped=item.get("skipped_entities"),
                    )
                )
                if item.get("skipped_by_type"):
                    print(f"skipped_by_type: {item['skipped_by_type']}")
    return 0 if all(item.get("ok", False) for item in results) else 2

if __name__ == "__main__":
    raise SystemExit(main())

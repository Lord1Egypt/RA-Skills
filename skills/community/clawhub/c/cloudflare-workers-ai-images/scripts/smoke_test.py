#!/usr/bin/env python3
import json
import os
import struct
import subprocess
import sys
import zlib
from pathlib import Path


def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    )


def make_png(width: int, height: int, rgba_rows: list[bytes]) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    raw = b"".join(b"\x00" + row for row in rgba_rows)
    idat = png_chunk(b"IDAT", zlib.compress(raw, level=9))
    iend = png_chunk(b"IEND", b"")
    return signature + ihdr + idat + iend


def write_png(path: Path, png_bytes: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes)


def build_source_png() -> bytes:
    width, height = 64, 64
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            if x < 32:
                row.extend((255, 255, 255, 255))
            else:
                row.extend((220, 220, 220, 255))
        rows.append(bytes(row))
    return make_png(width, height, rows)


def run_case(label: str, cmd: list[str]) -> dict:
    print(f"\n=== {label} ===")
    print("$", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stdout = proc.stdout.strip()
    result = {
        "label": label,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": proc.stderr.strip(),
        "ok": proc.returncode == 0,
        "stdout_len": len(stdout),
    }
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    print(f"result: {'OK' if result['ok'] else 'FAIL'}")
    return result


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    script = root / "scripts" / "cf_workers_ai_image.py"
    tmp = root / ".smoke-test"
    out_dir = tmp / "output"
    input_dir = tmp / "input"
    out_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    missing = [name for name in ["CF_ACCOUNT_ID", "CF_API_TOKEN"] if not os.environ.get(name)]
    if missing:
        print(json.dumps({"ok": False, "error": f"Missing env vars: {', '.join(missing)}"}, ensure_ascii=False))
        return 2

    source = input_dir / "source.png"
    write_png(source, build_source_png())

    tests = [
        (
            "text2img",
            [
                sys.executable,
                str(script),
                "text2img",
                "smoke test: a simple blue circle on white background",
                "--width",
                "512",
                "--height",
                "512",
                "--output",
                str(out_dir),
            ],
        ),
        (
            "img2img",
            [
                sys.executable,
                str(script),
                "img2img",
                "smoke test: slightly restyle the source image",
                "--image",
                str(source),
                "--strength",
                "0.5",
                "--output",
                str(out_dir),
            ],
        ),
    ]

    results = [run_case(label, cmd) for label, cmd in tests]

    for item in results:
        output_path = Path(item["stdout"]) if item["stdout"] else None
        item["has_output"] = bool(item["stdout"])
        item["output_exists"] = bool(output_path and output_path.exists() and output_path.is_file())
        item["ok"] = item["ok"] and item["has_output"] and item["output_exists"] and item["stdout_len"] > 0

    summary = {
        "ok": all(item["ok"] for item in results),
        "results": results,
        "output_dir": str(out_dir),
        "note": "Smoke test now validates temporary-file output for chat handoff.",
    }
    print("\n=== summary ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

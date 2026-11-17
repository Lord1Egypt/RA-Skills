#!/usr/bin/env python3
"""FK-Bench Skill — 保护打包脚本。

把明文数据集 data/v2.0/*.json 压缩混淆成单个 data.bin, 并可删除明文
JSON, 防止他人直接翻阅 722 道题目与 gold 答案。

用法:
    python protect.py                     # 生成 data.bin(保留明文源)
    python protect.py --remove-plaintext  # 生成 data.bin 并删除明文 JSON

生成后的 data.bin 由 scripts/sample.py 与 scripts/score.py 自动读取;
两个脚本在 data.bin 缺失时回退到明文 data/v2.0(便于作者本地开发)。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_ROOT / "assets" / "benchmark" / "data" / "v2.0"
PACK_PATH = SKILL_ROOT / "assets" / "benchmark" / "data.bin"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _datapack import pack_dir  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forklift-protect")
    parser.add_argument("--remove-plaintext", action="store_true",
                        help="打包后删除 data/v2.0 下的明文 JSON")
    args = parser.parse_args(argv)

    if not DATA_DIR.exists():
        print(f"error: dataset dir not found: {DATA_DIR}", file=sys.stderr)
        return 2

    n = pack_dir(DATA_DIR, PACK_PATH)
    print(f"Packed {n} JSON files -> {PACK_PATH} ({PACK_PATH.stat().st_size} bytes)")

    if args.remove_plaintext:
        removed = 0
        for p in DATA_DIR.glob("*.json"):
            p.unlink()
            removed += 1
        print(f"Removed {removed} plaintext JSON files from {DATA_DIR}")
    else:
        print("Plaintext sources kept. Run with --remove-plaintext to hide them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""FK-Bench Skill — 题库扩充打包脚本。

把原 500 道基础题(data.bin)与扩充题(``generator/papers.py`` + ``generator/safety_assist.py``)
合并, 重新加密打包进 data.bin。扩充题 item_id 前缀为 FK-EXT(FK-EXT-*)与 FK-EXT2(FK-EXT2-*)。

用法:
    python extend.py                     # 合并 500+N, 生成 data.bin(保留明文)
    python extend.py --remove-plaintext  # 合并后删除明文 JSON

生成器 seed 固定 42, 保证扩充题可复现。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
BENCH = SKILL_ROOT / "assets" / "benchmark"
DATA_DIR = BENCH / "data" / "v2.0"
PACK_PATH = BENCH / "data.bin"

sys.path.insert(0, str(BENCH))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _datapack import load_pack, pack_dir  # noqa: E402
from generator.papers import generate_papers  # noqa: E402
from generator.safety_assist import generate_ext2  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forklift-extend")
    parser.add_argument("--remove-plaintext", action="store_true",
                        help="合并打包后删除明文 JSON")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    # 1) 加载原题(从 data.bin)
    if not PACK_PATH.exists():
        print(f"error: data.bin not found: {PACK_PATH}", file=sys.stderr)
        return 2
    original = load_pack(PACK_PATH)

    # 2) 生成扩充题(两批)
    extras = generate_papers(args.seed)
    extras += generate_ext2(args.seed)

    # 3) 写回明文目录(用于重新打包)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for fname, text in original.items():
        (DATA_DIR / fname).write_text(text, encoding="utf-8")
    for it in extras:
        fname = f"{it.item_id.lower()}.json"
        (DATA_DIR / fname).write_text(it.to_json(), encoding="utf-8")

    # 4) 重新打包
    total = pack_dir(DATA_DIR, PACK_PATH)

    # 5) 可选删除明文
    if args.remove_plaintext:
        removed = 0
        for p in DATA_DIR.glob("fk-*.json"):
            p.unlink()
            removed += 1
        print(f"Removed {removed} plaintext JSON files from {DATA_DIR}")

    print(f"Merged {len(original)} original + {len(extras)} extended "
          f"= {total} items -> {PACK_PATH} ({PACK_PATH.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

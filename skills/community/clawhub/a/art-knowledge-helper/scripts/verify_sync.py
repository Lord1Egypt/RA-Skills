#!/usr/bin/env python3
"""
艺术知识库助手 · 同步验证脚本
verify_sync.py - 验证本地知识库与百度网盘是否完全同步

用法：python verify_sync.py

作者：小艺艺术知识库助手 v1.0 | 2026-04-22
"""

import io
import sys
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ─── 路径配置（从 config.json 读取）────────────────────────────────────────
def load_config():
    cfg = Path(__file__).parent.parent / 'config.json'
    if cfg.exists():
        with open(cfg, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

config = load_config()
KB = Path(config.get('knowledge_base_path', ''))
BD = Path(config.get('baidu_path', ''))

if not KB or not KB.exists():
    print("❌ 知识库路径未配置或路径无效！")
    print("请编辑本目录下的 config.json，填写 knowledge_base_path")
    sys.exit(1)

BOOK_EXTENSIONS = {'.pdf', '.epub', '.mobi', '.azw3', '.djvu', '.cbz', '.cbr'}
SKIP = {'node_modules', '.git', 'Thumbs.db'}

def is_book(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in BOOK_EXTENSIONS

def is_skipped(path: Path) -> bool:
    return any(s in str(path) for s in SKIP)

def collect_books(root: Path) -> dict:
    books = {}
    if not root.exists():
        return books
    for f in root.rglob('*'):
        if is_book(f) and not is_skipped(f):
            rel = str(f.relative_to(root))
            books[rel] = f.stat().st_size
    return books

def main():
    print("🔍 艺术知识库 · 同步验证")
    print("=" * 50)
    print(f"📍 本地：{KB}")
    print(f"☁️  百度：{BD}")
    print()

    kb_books = collect_books(KB)
    bd_books = collect_books(BD) if BD.exists() else {}

    kb_set = set(kb_books.keys())
    bd_set = set(bd_books.keys())

    only_kb = kb_set - bd_set
    only_bd = bd_set - kb_set
    common = kb_set & bd_set

    size_diff = 0
    for rel in common:
        if kb_books[rel] != bd_books[rel]:
            size_diff += 1

    print(f"📚 本地书籍：{len(kb_set)} 本")
    print(f"☁️  百度书籍：{len(bd_set)} 本")
    print(f"✅ 共同书籍：{len(common)} 本")
    if size_diff:
        print(f"⚠️  大小不同的文件：{size_diff} 个")
    print()

    if not only_kb and not only_bd and not size_diff:
        print("🎉 完全同步！本地与百度盘完全一致。")
    else:
        if only_kb:
            print(f"📤 本地有但百度没有（{len(only_kb)} 本）：")
            for rel in sorted(only_kb)[:10]:
                print(f"  + {rel}")
            if len(only_kb) > 10:
                print(f"  ... 还有 {len(only_kb) - 10} 本")
        if only_bd:
            print(f"📥 百度有但本地没有（{len(only_bd)} 本）：")
            for rel in sorted(only_bd)[:10]:
                print(f"  - {rel}")
            if len(only_bd) > 10:
                print(f"  ... 还有 {len(only_bd) - 10} 本")
        if size_diff:
            print(f"⚠️  {size_diff} 个文件大小不一致，需要重新同步")

if __name__ == '__main__':
    main()

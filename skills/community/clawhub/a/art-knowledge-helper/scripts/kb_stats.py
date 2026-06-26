#!/usr/bin/env python3
"""
艺术知识库助手 · 统计脚本
kb_stats.py - 统计知识库藏书量，按分类展示

用法：python kb_stats.py

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
    config_path = Path(__file__).parent.parent / 'config.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

config = load_config()
KB = Path(config.get('knowledge_base_path', ''))

if not KB or not KB.exists():
    print("❌ 知识库路径未配置或路径无效！")
    print("请编辑本目录下的 config.json，填写 knowledge_base_path")
    sys.exit(1)

# ─── 分类顺序与中文名 ────────────────────────────────────────────────────────
CAT_INFO = [
    ('01_摄影艺术',    '📷  摄影艺术',       '摄影、构图、灯光'),
    ('02_绘画技法',    '🎨  绘画技法',       '素描、水彩、油画'),
    ('03_插画设计',    '✏️  插画设计',       '插画、绘本、漫画分镜'),
    ('04_动画艺术',    '🎬  动画艺术',       '动画原理、运动规律'),
    ('04_艺术史论',    '📜  艺术史论',       '艺术史、理论、美学'),
    ('05_数字艺术',    '💻  数字艺术',       '数字绘画、3D、概念设计'),
    ('06_各国艺术',    '🌍  各国艺术',       '中国、日本、非洲、拉美'),
    ('07_艺术解剖',    '🦴  艺术解剖',       '人体解剖、艺用解剖'),
    ('08_视觉设计',    '🖋  视觉设计',       '平面设计、字体、版式'),
    ('09_幻想艺术',    '🧙  幻想艺术',       '幻想艺术、科幻设定'),
    ('10_参考资料',    '📖  参考资料',       '工具书、图鉴'),
    ('11_音乐教程',    '🎵  音乐教程',       '乐理、作曲'),
]

BOOK_EXTENSIONS = {'.pdf', '.epub', '.mobi', '.azw3', '.djvu', '.cbz', '.cbr'}

def scan_category(cat_dir: Path):
    """扫描一个分类目录，返回书籍信息"""
    books = []
    other_files = []
    for f in cat_dir.rglob('*'):
        if not f.is_file():
            continue
        if 'node_modules' in str(f) or '.git' in str(f):
            continue
        ext = f.suffix.lower()
        if ext in BOOK_EXTENSIONS:
            size_mb = round(f.stat().st_size / 1024 / 1024, 2)
            books.append({'name': f.name, 'size_mb': size_mb, 'path': str(f.relative_to(KB))})
        elif not f.name.startswith('~'):
            size_mb = round(f.stat().st_size / 1024 / 1024, 2)
            other_files.append({'name': f.name, 'size_mb': size_mb})

    books.sort(key=lambda x: x['name'])
    return books, other_files

def main():
    print("📚 艺术知识库 · 藏书统计")
    print("=" * 60)
    print(f"📍 知识库：{KB}")
    print()

    total_books = 0
    total_size_mb = 0
    stats = []

    for cat_id, cat_label, cat_desc in CAT_INFO:
        cat_dir = KB / cat_id
        if not cat_dir.exists():
            stats.append((cat_label, cat_desc, 0, 0, []))
            continue

        books, other = scan_category(cat_dir)
        cat_size = sum(b['size_mb'] for b in books)
        total_books += len(books)
        total_size_mb += cat_size
        stats.append((cat_label, cat_desc, len(books), cat_size, books))

    # 打印结果
    print(f"{'分类':<6}  {'书数':>4}  {'大小(MB)':>10}  说明")
    print("─" * 60)
    for cat_label, cat_desc, n, size, _ in stats:
        cat_name = cat_label.split(' ', 1)[1] if ' ' in cat_label else cat_label
        print(f"{cat_name:<16} {n:>4}  {size:>10.1f} MB  {cat_desc}")

    print("─" * 60)
    print(f"{'合计':<16} {total_books:>4}  {total_size_mb:>10.1f} MB")
    print()

    # 找出藏书最多的分类
    if stats:
        top_cat = max(stats, key=lambda x: x[2])
        top_name = top_cat[0].split(' ', 1)[1] if ' ' in top_cat[0] else top_cat[0]
        print(f"🏆 藏书最丰富的分类：{top_name}（{top_cat[2]} 本，{top_cat[3]:.1f} MB）")
        print(f"📊 平均每本书：{total_size_mb / total_books:.1f} MB" if total_books else "")

    print()
    print("💡 提示：运行 `scan_downloads.py` 可扫描下载目录中的新书")

if __name__ == '__main__':
    main()

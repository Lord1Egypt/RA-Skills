#!/usr/bin/env python3
"""
艺术知识库助手 · 核心脚本集
scan_downloads.py - 扫描下载目录，找出近30天内新增的艺术类书籍

用法：python scan_downloads.py [天数]
默认：扫描近30天

作者：小艺艺术知识库助手 v1.0 | 2026-04-22
"""

import io
import sys
import json
import re
import time
import argparse
from datetime import datetime
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
DOWNLOADS = Path(config.get('downloads_path', ''))

if not DOWNLOADS or not DOWNLOADS.exists():
    print("❌ 下载目录未配置或路径无效！")
    print("请编辑本目录下的 config.json，填写 downloads_path")
    sys.exit(1)

# ─── 艺术关键词（用于识别艺术类书籍） ─────────────────────────────────────
ART_KEYWORDS = [
    # 技法
    'drawing', 'painting', 'sketch', 'watercolor', 'watercolour', 'oil painting',
    'acrylic', 'charcoal', 'pencil', 'color', 'colour', 'light', 'shadow',
    'render', 'rendering', 'shading', 'composition', 'perspective', 'anatomy',
    'portrait', 'figure', 'still life', 'landscape', 'en plein air',
    # 素描/速写
    'sketchbook', 'sketching', 'draw', 'how to draw', 'anatom', 'gesture',
    # 插画/绘本
    'illustration', 'illustrator', 'illustrated', 'comic', 'manga', 'graphic novel',
    'sequential art', 'cartoon', 'character design', 'concept art',
    # 摄影
    'photography', 'photograph', 'camera', 'portrait', 'lighting', 'composition',
    # 数字艺术
    'digital painting', 'digital art', 'photoshop', 'procreate', 'clip studio',
    'concept design', 'environment art', 'matte painting',
    # 动画/运动
    'animation', 'animator', 'motion', 'timing', '12 principles', 'acting',
    # 艺术史/理论
    'art history', 'art theory', 'art movement', 'impressionism', 'renaissance',
    'modern art', 'contemporary art', 'baroque', 'romanticism', 'cubism',
    # 设计
    'graphic design', 'typography', 'font', 'logo', 'branding', 'layout',
    # 其他
    'art book', 'art of', 'master', 'tutorial', 'guide to', 'step by step',
    # 中文关键词
    '素描', '速写', '水彩', '油画', '丙烯', '插画', '绘本', '漫画', '分镜',
    '摄影', '光线', '构图', '人体', '解剖', '艺用', '动物', '静物', '风景',
    '光影', '渲染', '上色', '配色', '数字绘画', '概念设计', '场景', '角色设计',
    '动画', '运动规律', '原画', '艺术史', '艺术理论', '平面设计', '字体',
    '视觉设计', '幻想艺术', '艺术', '画集', '画册', '教程', '技法',
    '莫奈', '梵高', '伦勃朗', '达芬奇', '米开朗基罗', '德加', '马蒂斯',
    '透纳', '萨金特', '费欣', '佐恩', '丢勒', '门采尔', '安格尔',
]

ART_EXTENSIONS = {'.pdf', '.epub', '.mobi', '.azw3', '.djvu', '.cbz', '.cbr'}

def is_art_related(filename: str) -> bool:
    """检查文件名是否与艺术相关"""
    name_lower = filename.lower()
    for kw in ART_KEYWORDS:
        if kw in name_lower:
            return True
    return False

def get_file_age_days(path: Path) -> float:
    """获取文件年龄（天）"""
    try:
        return (time.time() - path.stat().st_mtime) / 86400
    except:
        return 999

def scan_downloads(days: int = 30) -> dict:
    """扫描下载目录，返回近N天内的艺术类书籍"""
    print(f"📂 扫描目录：{DOWNLOADS}")
    print(f"⏱  筛选：近 {days} 天内下载的书籍")
    print()

    if not DOWNLOADS.exists():
        print(f"❌ 目录不存在：{DOWNLOADS}")
        return {}

    # 收集书籍文件
    art_books = []
    for f in DOWNLOADS.iterdir():
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext not in ART_EXTENSIONS:
            continue
        age = get_file_age_days(f)
        if age > days:
            continue
        if not is_art_related(f.name):
            continue
        size_mb = round(f.stat().st_size / 1024 / 1024, 2)
        art_books.append({
            'name': f.name,
            'path': str(f),
            'size_mb': size_mb,
            'age_days': round(age, 1),
            'modified': datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
        })

    # 按时间排序
    art_books.sort(key=lambda x: x['modified'], reverse=True)

    print(f"✅ 找到 {len(art_books)} 本近 {days} 天内的艺术类书籍：")
    print()
    for i, book in enumerate(art_books, 1):
        print(f"  {i:2d}. [{book['modified']}] {book['size_mb']:6.2f} MB  {book['name'][:55]}")

    return {'books': art_books, 'total': len(art_books)}

def check_against_kb(books: list) -> dict:
    """对照知识库，检查哪些是新增的"""
    if not books:
        return {}

    kb_books = set()
    if KB.exists():
        for cat_dir in KB.iterdir():
            if not cat_dir.is_dir():
                continue
            for f in cat_dir.rglob('*'):
                if f.is_file() and f.suffix.lower() in ART_EXTENSIONS:
                    kb_books.add(f.name.lower())

    results = {'new': [], 'already_exists': []}
    for book in books:
        name_lower = book['name'].lower()
        is_new = True
        for kb_name in kb_books:
            if kb_name in name_lower or name_lower.replace(' ', '') in kb_name.replace(' ', ''):
                is_new = False
                break
            kb_words = set(re.findall(r'[a-zA-Z]{4,}', kb_name))
            book_words = set(re.findall(r'[a-zA-Z]{4,}', name_lower))
            overlap = kb_words & book_words
            if len(overlap) >= 3 and len(book_words) >= 3:
                ratio = len(overlap) / min(len(kb_words), len(book_words))
                if ratio > 0.6:
                    is_new = False
                    break

        if is_new:
            results['new'].append(book)
        else:
            results['already_exists'].append(book)

    return results

def main():
    parser = argparse.ArgumentParser(description='扫描下载目录中的艺术类书籍')
    parser.add_argument('days', nargs='?', type=int, default=30, help='扫描近N天内的文件（默认30）')
    args = parser.parse_args()

    result = scan_downloads(args.days)
    if not result.get('books'):
        print("没有找到符合条件的书籍。")
        return

    print()
    print("─── 正在对照知识库 ───")
    checked = check_against_kb(result['books'])

    if checked.get('new'):
        print(f"\n🌟 {len(checked['new'])} 本可能是新增书籍（对照已有库存）：")
        for i, book in enumerate(checked['new'], 1):
            print(f"  {i:2d}. {book['name'][:55]}")
    else:
        print("\n⚠️ 没有发现明显的新增书籍。")

    if checked.get('already_exists'):
        print(f"\n📚 {len(checked['already_exists'])} 本已在知识库中：")
        for book in checked['already_exists']:
            print(f"  ✓ {book['name'][:55]}")

    # 保存结果
    output = DOWNLOADS.parent / f'art_books_scan_{datetime.now().strftime("%Y%m%d")}.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 扫描结果已保存：{output.name}")

if __name__ == '__main__':
    main()

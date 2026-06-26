#!/usr/bin/env python3
"""
艺术知识库助手 · 归档脚本
archive_books.py - 将新书归档到知识库对应分类

用法：python archive_books.py
运行前请先运行 scan_downloads.py 确认新书

作者：小艺艺术知识库助手 v1.0 | 2026-04-22
"""

import io
import sys
import json
import shutil
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
DOWNLOADS = Path(config.get('downloads_path', ''))

if not KB or not KB.exists():
    print("❌ 知识库路径未配置或路径无效！")
    print("请编辑本目录下的 config.json，填写 knowledge_base_path")
    sys.exit(1)

# ─── 分类规则（关键词 → 分类目录）─────────────────────────────────────────
CLASSIFICATION_RULES = [
    # 摄影
    (['photo', 'photog', 'camera', 'lightroom', 'canon', 'nikon', 'sony',
      'portrait photo', 'wedding photo', 'landscape photo', 'drone',
      '摄影', '相机', '人像摄影', '风光摄影', '摄影教程', '婚纱摄影',
      'photoshop photography', 'light'], '01_摄影艺术'),

    # 艺术解剖
    (['anatom', 'anatomy', 'bridgman', 'hogarth', 'body', '肌肉', '骨骼',
      '艺用解剖', '人体结构', '肌肉训练', 'figure drawing reference',
      'art models', 'pose reference', '动态解剖'], '07_艺术解剖'),

    # 动画艺术
    (['animation', 'animator', 'animating', 'motion design', 'mograph',
      '12 principles', ' disney', 'pixar', '3d animation', 'stop motion',
      'timing', 'acting for animators', 'the animator', 'animation survival'],
     '04_动画艺术'),

    # 数字艺术 / 概念设计
    (['digital painting', 'digital art', 'concept art', 'concept design',
      'environment art', 'matte painting', 'digital sculpt', 'zbrush',
      'blender', '3d modeling', 'maya', 'houdini', 'digital sculpting',
      'digital illustration', 'procreate', 'clip studio paint',
      '数字绘画', '概念设计', '3D', '数字艺术', '游戏美术', '影视概念'],
     '05_数字艺术'),

    # 插画设计
    (['illustration', 'illustrator', 'illustrated', 'comic', 'manga',
      'graphic novel', 'sequential art', 'cartoon', 'character design',
      'storyboard', 'picture book', '繪本', '绘本', '分镜', 'storyboard',
      '插画', '漫画', '动漫', '卡通', '角色设计', '构图与创作',
      'understanding comics', 'reinventing comics', 'making comics'],
     '03_插画设计'),

    # 幻想艺术
    (['fantasy art', 'fantasy illustration', 'sci-fi', 'science fiction',
      'concept creature', 'fantasy creature', 'speculative art',
      'imaginative realism', '幻想艺术', '幻想', '科幻设定', '幻想生物'],
     '09_幻想艺术'),

    # 视觉设计（字体 / 平面）
    (['typography', 'type design', 'font', 'logo design', 'branding',
      'graphic design', 'visual design', 'poster design', 'packaging',
      '平面设计', '字体设计', '品牌设计', '版式设计', '海报设计',
      'logo', 'branding', 'indesign'],
     '08_视觉设计'),

    # 绘画技法（素描/水彩/油画）
    (['drawing', 'sketch', 'pencil', 'charcoal', 'sketchbook',
      'how to draw', 'figure drawing', 'portrait drawing',
      'watercolor', 'watercolour', 'oil painting', 'acrylic',
      'painting technique', 'painting tutorial', 'alla prima',
      'plein air', 'en plein air', 'color', 'colour', 'light and shadow',
      '素描', '速写', '水彩', '油画', '丙烯', '绘画技法', '绘画教程',
      '调色', '配色', '光影', '上色', '厚涂', '渲染', '静物', '风景',
      'portrait painting', 'watercolour tutorial', 'oil tutorial',
      'sketching', 'rendering', 'shading', 'perspective drawing',
      '动物素描', '动物绘画', 'wildlife', ' animal'],
     '02_绘画技法'),

    # 艺术史论
    (['art history', 'art theory', 'art movement', 'impressionism',
      'renaissance', 'modern art', 'contemporary art', 'baroque',
      'romanticism', 'cubism', 'surrealism', 'expressionism',
      'art criticism', 'aesthetics', 'art philosophy', 'sociology of art',
      '艺术史', '艺术理论', '美学', '艺术哲学', '艺术评论',
      '艺术的故事', '文明的故事', 'art of', 'master', 'collection',
      '艺术史论', '艺术概论', '当代艺术', '印象派', '文艺复兴',
      '莫奈', '梵高', '伦勃朗', '达芬奇', '马蒂斯', '高更', '塞尚',
      '戈雅', '安格尔', '德拉克洛瓦', '门采尔', '萨金特', '费欣', '佐恩',
      'manet', 'monet', 'rembrandt', 'davinci', 'michelangelo', 'goya',
      'ingres', 'gauguin', 'cezanne', ' PICASSO', 'vermeer', 'hopper',
      'Turner', 'waterhouse', 'lein', 'frida', 'Kahlo', 'okeeffe'],
     '04_艺术史论'),

    # 各国艺术（按国家/地区）
    (['chinese art', 'japanese art', 'korean art', 'indian art', 'african art',
      'latin american art', 'asian art', 'oriental art', 'arab art',
      'islamic art', 'persian art', 'byzantine art', 'ancient art',
      'world art', 'art of', 'architecture', 'art and architecture',
      '中国艺术', '日本艺术', '中国画', '国画', '浮世绘', '书法',
      '水墨', '工笔', '写意', '陶瓷', '青铜器', '石窟', '壁画',
      '非洲艺术', '拉美艺术', '印度艺术', '亚洲艺术', '伊斯兰艺术',
      '古代艺术', '艺术与建筑', '建筑史'],
     '06_各国艺术'),

    # 音乐教程
    (['music', 'musical', 'composition', 'harmony', 'counterpoint',
      'orchestration', 'theory of music', 'music theory', 'piano',
      'guitar', 'violin', 'jazz', 'blues', 'rock', 'electronic music',
      '乐理', '作曲', '和声', '对位法', '配器', '音乐理论',
      '钢琴', '吉他', '爵士', '古典音乐', '电子音乐'],
     '11_音乐教程'),

    # 参考资料
    (['dictionary', 'encyclopedia', 'encyclopaedia', 'reference',
      'handbook', 'guide', 'glossary', 'atlas',
      '词典', '百科', '图鉴', '手册', '参考资料'],
     '10_参考资料'),
]

def classify_book(filename: str) -> str:
    """根据文件名关键词，判断书籍应归档到哪个分类"""
    name_lower = filename.lower()
    for keywords, category in CLASSIFICATION_RULES:
        for kw in keywords:
            if kw.lower() in name_lower:
                return category
    return '10_参考资料'  # 默认归入参考资料

def get_archive_destinations(filename: str) -> tuple:
    """获取归档目标路径（本地 + 百度盘）"""
    category = classify_book(filename)
    return KB / category, (BD / category) if BD.exists() else None

def archive_file(src_path: Path, dry_run: bool = False) -> dict:
    """归档单个文件，返回结果信息"""
    local_dest, bd_dest = get_archive_destinations(src_path.name)
    local_dest.mkdir(parents=True, exist_ok=True)
    dest_path = local_dest / src_path.name

    if dest_path.exists():
        return {'status': 'exists', 'dest': str(dest_path), 'name': src_path.name}

    if dry_run:
        return {'status': 'would_copy', 'dest': str(dest_path), 'name': src_path.name}

    shutil.copy2(src_path, dest_path)

    # 同时复制到百度盘
    if bd_dest:
        bd_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, bd_dest / src_path.name)

    return {'status': 'archived', 'dest': str(dest_path), 'name': src_path.name}

def main():
    print("📦 艺术知识库 · 归档工具")
    print("=" * 50)
    print()

    if not DOWNLOADS.exists():
        print(f"❌ 下载目录不存在：{DOWNLOADS}")
        print("请编辑 config.json，填写 downloads_path")
        return

    print(f"📂 扫描：{DOWNLOADS}")
    print()

    EXTENSIONS = {'.pdf', '.epub', '.mobi', '.azw3', '.djvu', '.cbz', '.cbr'}
    candidates = [f for f in DOWNLOADS.iterdir() if f.is_file() and f.suffix.lower() in EXTENSIONS]

    if not candidates:
        print("下载目录中没有找到书籍文件。")
        return

    print(f"📋 找到 {len(candidates)} 个候选文件，开始归档……")
    print()

    results = {'archived': [], 'skipped': [], 'errors': []}
    for f in candidates:
        try:
            result = archive_file(f)
            if result['status'] == 'archived':
                size_mb = round(f.stat().st_size / 1024 / 1024, 2)
                cat = classify_book(f.name)
                print(f"  ✅ {size_mb:6.2f} MB  →  {cat}  {result['name'][:45]}")
                results['archived'].append(result)
            elif result['status'] == 'exists':
                results['skipped'].append(result)
        except Exception as e:
            print(f"  ❌ {f.name}: {e}")
            results['errors'].append({'name': f.name, 'error': str(e)})

    print()
    print("─── 归档完成 ───")
    print(f"  ✅ 新归档：{len(results['archived'])} 本")
    print(f"  ⏭  已存在：{len(results['skipped'])} 本")
    if results['errors']:
        print(f"  ❌ 错误：{len(results['errors'])} 本")

if __name__ == '__main__':
    main()

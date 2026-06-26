#!/usr/bin/env python3
"""
艺术知识库助手 · 百度网盘同步脚本
sync_to_baidu.py - 将本地知识库同步到百度网盘

用法：python sync_to_baidu.py

原理：使用 Python 直接复制文件到百度网盘同步目录
（百度网盘同步版客户端会自动上传到云端）

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

if not KB or not KB.exists():
    print("❌ 知识库路径未配置或路径无效！")
    print("请编辑本目录下的 config.json，填写 knowledge_base_path")
    sys.exit(1)

if not BD:
    print("❌ 百度网盘路径未配置！")
    print("请编辑 config.json，填写 baidu_path")
    sys.exit(1)

# ─── 要跳过的文件 ──────────────────────────────────────────────────────────
SKIP_PATTERNS = ['node_modules', '.git', '.DS_Store', 'Thumbs.db', '~$']

def should_skip(path: Path) -> bool:
    for pat in SKIP_PATTERNS:
        if pat in str(path):
            return True
    return path.name.startswith('~')

def sync_directory(src_dir: Path, dst_dir: Path, stats: dict) -> None:
    """递归同步目录"""
    if not src_dir.exists():
        print(f"  ⚠️  源目录不存在：{src_dir}")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)

    for src_file in src_dir.rglob('*'):
        if not src_file.is_file() or should_skip(src_file):
            continue

        rel_path = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel_path

        if dst_file.exists():
            if dst_file.stat().st_size == src_file.stat().st_size:
                continue  # 大小相同，跳过
        else:
            dst_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(src_file, dst_file)
            stats['copied'] += 1
            stats['copied_mb'] += src_file.stat().st_size / 1024 / 1024
        except Exception as e:
            stats['errors'].append(str(src_file))
            print(f"  ❌ 复制失败：{src_file.name}")

def main():
    print("🔄 艺术知识库 → 百度网盘 同步工具")
    print("=" * 50)
    print(f"📂 源：{KB}")
    print(f"☁️  目标：{BD}")
    print()

    if not BD.exists():
        print("⚠️  百度网盘同步目录不存在，将自动创建")
        BD.mkdir(parents=True, exist_ok=True)
        print("✅ 已创建目标目录")

    stats = {'copied': 0, 'copied_mb': 0, 'errors': []}

    print("─── 同步中 ───")
    sync_directory(KB, BD, stats)

    print()
    print("─── 同步完成 ───")
    print(f"  ✅ 复制/更新文件：{stats['copied']} 个（{stats['copied_mb']:.1f} MB）")
    if stats['errors']:
        print(f"  ❌ 错误：{len(stats['errors'])} 个")

    print()
    print("💡 提示：百度网盘客户端会自动将更改同步到云端")
    print("💡 如需验证同步状态，运行 verify_sync.py")

if __name__ == '__main__':
    main()

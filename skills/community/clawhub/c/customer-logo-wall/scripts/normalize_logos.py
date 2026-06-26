#!/usr/bin/env python3
"""
normalize_logos.py
将下载的 Logo 文件统一转换为真正的 PNG 格式

常见问题：
  - 搜索引擎返回的图片实际是 JPEG/WEBP/SVG，但扩展名为 .png
  - SVG 文件伪装为 PNG → Anthropic API / python-pptx 报错 "Could not process image"
  - WEBP 格式在部分系统和 PowerPoint 中不支持

本脚本自动检测并修复以上问题。

用法：
  python3 normalize_logos.py --logos-dir ./logos [--companies companies.json]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow 未安装，请运行: pip install Pillow")
    sys.exit(1)


def detect_format(filepath: str) -> str:
    """检测文件的真实格式，返回 'PNG', 'JPEG', 'WEBP', 'SVG', 或 'UNKNOWN'"""
    with open(filepath, 'rb') as f:
        header = f.read(16)

    if header[:4] == b'\x89PNG':
        return 'PNG'
    if header[:2] == b'\xff\xd8':
        return 'JPEG'
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return 'WEBP'
    if header.lstrip()[:5] in (b'<?xml', b'<svg ', b'<SVG '):
        return 'SVG'

    # Fallback: 用 Pillow 检测
    try:
        img = Image.open(filepath)
        return img.format or 'UNKNOWN'
    except Exception:
        return 'UNKNOWN'


def convert_svg_to_png(svg_path: str, output_path: str, size: int = 800) -> bool:
    """SVG → PNG 转换，按优先级尝试多种工具"""
    # 1. rsvg-convert (最佳质量)
    try:
        result = subprocess.run(
            ['rsvg-convert', '-w', str(size), '-h', str(size),
             '--keep-aspect-ratio', svg_path, '-o', output_path],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and os.path.exists(output_path):
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 2. cairosvg (Python)
    try:
        import cairosvg
        with open(svg_path, 'rb') as f:
            svg_data = f.read()
        cairosvg.svg2png(bytestring=svg_data, write_to=output_path, output_width=size)
        if os.path.exists(output_path):
            return True
    except (ImportError, Exception):
        pass

    # 3. qlmanage (macOS 自带)
    try:
        tmp_svg = svg_path + '.svg'
        shutil.copy2(svg_path, tmp_svg)
        result = subprocess.run(
            ['qlmanage', '-t', '-s', str(size), '-o', '/tmp/', tmp_svg],
            capture_output=True, text=True, timeout=15
        )
        os.remove(tmp_svg)
        tmp_png = f'/tmp/{os.path.basename(tmp_svg)}.png'
        if os.path.exists(tmp_png):
            shutil.move(tmp_png, output_path)
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return False


def normalize_logo(filepath: str) -> tuple[bool, str]:
    """
    将单个 logo 文件标准化为真正的 PNG。
    返回 (success, message)。
    """
    if not os.path.exists(filepath):
        return False, "文件不存在"

    fmt = detect_format(filepath)

    if fmt == 'PNG':
        # 验证 Pillow 也能正常读取
        try:
            img = Image.open(filepath)
            img.verify()
            return True, "已是 PNG"
        except Exception:
            return False, "PNG 文件损坏"

    if fmt == 'SVG':
        tmp_out = filepath + '.tmp.png'
        ok = convert_svg_to_png(filepath, tmp_out)
        if ok:
            shutil.move(tmp_out, filepath)
            return True, "SVG → PNG"
        return False, "SVG 转换失败（需安装 rsvg-convert / cairosvg / qlmanage）"

    if fmt in ('JPEG', 'WEBP'):
        try:
            img = Image.open(filepath)
            img_rgba = img.convert('RGBA')
            img_rgba.save(filepath, 'PNG')
            return True, f"{fmt} → PNG"
        except Exception as e:
            return False, f"{fmt} 转换失败: {e}"

    return False, f"无法识别的格式: {fmt}"


def main():
    parser = argparse.ArgumentParser(description='Logo 格式标准化工具')
    parser.add_argument('--logos-dir', required=True, help='Logo 目录')
    parser.add_argument('--companies', help='公司 JSON 文件（可选，用于过滤文件）')
    args = parser.parse_args()

    # 确定要处理的文件列表
    if args.companies:
        with open(args.companies) as f:
            companies = json.load(f)
        files = [c.get('file', '') for c in companies if c.get('file')]
    else:
        files = [f for f in os.listdir(args.logos_dir)
                 if f.endswith('.png') and not f.startswith('_')]

    print(f"\n🔧 标准化 {len(files)} 个 Logo 文件...\n")

    stats = {'ok': 0, 'converted': 0, 'failed': 0}
    failed_files = []

    for filename in sorted(files):
        filepath = os.path.join(args.logos_dir, filename)
        success, message = normalize_logo(filepath)

        if success:
            if message == "已是 PNG":
                print(f"  ✓ {filename}: {message}")
                stats['ok'] += 1
            else:
                print(f"  ✅ {filename}: {message}")
                stats['converted'] += 1
        else:
            print(f"  ❌ {filename}: {message}")
            stats['failed'] += 1
            failed_files.append(filename)

    print(f"\n{'═' * 50}")
    print(f"  原生 PNG: {stats['ok']}")
    print(f"  已转换:   {stats['converted']}")
    print(f"  失败:     {stats['failed']}")
    if failed_files:
        print(f"  失败文件: {', '.join(failed_files)}")
    print(f"{'═' * 50}")

    return 0 if stats['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

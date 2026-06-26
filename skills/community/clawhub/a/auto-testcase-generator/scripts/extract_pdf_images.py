#!/usr/bin/env python3
"""
PDF 图片优化提取脚本

从 PDF 文档中提取高质量唯一图片，自动去重和质量过滤。

用法:
    python extract_pdf_images.py <pdf文件路径> [输出目录]

示例:
    python extract_pdf_images.py input/需求文档.pdf
    python extract_pdf_images.py input/需求文档.pdf output/images

依赖:
    pip install PyMuPDF
"""

import sys
import os
import hashlib
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("错误: 需要安装 PyMuPDF 库")
    print("请执行: pip install PyMuPDF")
    sys.exit(1)

# Windows 环境编码处理
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def extract_unique_images(pdf_path, output_dir=None, min_width=100, min_height=100, min_size=5120):
    """
    从 PDF 中提取唯一的高质量图片。

    参数:
        pdf_path: PDF 文件路径
        output_dir: 输出目录（默认为 PDF 同目录下的 images 子目录）
        min_width: 最小宽度阈值（像素），默认 100
        min_height: 最小高度阈值（像素），默认 100
        min_size: 最小文件大小阈值（字节），默认 5KB

    返回:
        保存的图片信息列表
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        print(f"错误: PDF 文件不存在: {pdf_path}")
        return []

    # 确定输出目录
    if output_dir is None:
        output_dir = pdf_path.parent / "images"
    else:
        output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"开始提取 PDF 唯一图片: {pdf_path}")
    print(f"输出目录: {output_dir}")
    print(f"过滤条件: 最小尺寸 {min_width}x{min_height}px, 最小大小 {min_size} bytes")

    # 打开 PDF 文档
    doc = fitz.open(str(pdf_path))

    # 用于去重的集合
    seen_xrefs = set()
    seen_hashes = set()
    saved_images = []
    skipped_count = 0

    # 遍历每一页收集所有图片 xref
    all_xrefs = set()
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        for img in image_list:
            all_xrefs.add(img[0])

    print(f"发现 {len(all_xrefs)} 个图片对象")

    # 按 xref 提取唯一图片
    for i, xref in enumerate(sorted(all_xrefs)):
        try:
            pix = fitz.Pixmap(doc, xref)
            width = pix.width
            height = pix.height
            img_data = pix.tobytes()
            img_size = len(img_data)

            # 计算 MD5 哈希值用于去重
            img_hash = hashlib.md5(img_data).hexdigest()

            # 质量过滤
            if (width > min_width and height > min_height and
                    img_size > min_size and
                    img_hash not in seen_hashes):

                # CMYK 颜色空间转换为 RGB
                if pix.n - pix.alpha >= 4:
                    pix_rgb = fitz.Pixmap(fitz.csRGB, pix)
                    img_filename = f"image_{len(saved_images) + 1:02d}_{width}x{height}.png"
                    img_path = output_dir / img_filename
                    pix_rgb.save(str(img_path))
                    pix_rgb = None
                else:
                    img_filename = f"image_{len(saved_images) + 1:02d}_{width}x{height}.png"
                    img_path = output_dir / img_filename
                    pix.save(str(img_path))

                seen_hashes.add(img_hash)
                saved_images.append({
                    'filename': img_filename,
                    'path': str(img_path),
                    'xref': xref,
                    'width': width,
                    'height': height,
                    'size': img_size,
                    'hash': img_hash[:8]
                })

                print(f"  保存: {img_filename} ({width}x{height}, {img_size} bytes)")
            else:
                skipped_count += 1
                reason = []
                if width <= min_width or height <= min_height:
                    reason.append("尺寸过小")
                if img_size <= min_size:
                    reason.append("文件过小")
                if img_hash in seen_hashes:
                    reason.append("重复图片")
                print(f"  跳过: xref={xref} ({width}x{height}, {img_size} bytes) - {', '.join(reason)}")

            pix = None

        except Exception as e:
            print(f"  错误: xref={xref} - {e}")

    doc.close()

    # 输出统计信息
    print(f"\n{'='*40}")
    print(f"提取完成!")
    print(f"  图片对象总数: {len(all_xrefs)}")
    print(f"  保存有效图片: {len(saved_images)}")
    print(f"  跳过/过滤图片: {skipped_count}")
    if len(all_xrefs) > 0:
        print(f"  去重过滤率: {(1 - len(saved_images) / len(all_xrefs)) * 100:.1f}%")
    print(f"  输出目录: {output_dir}")

    if saved_images:
        print(f"\n保存的图片列表:")
        for img in saved_images:
            print(f"  {img['filename']}: {img['width']}x{img['height']}, "
                  f"{img['size']} bytes, hash={img['hash']}")

    return saved_images


def main():
    if len(sys.argv) < 2:
        print("用法: python extract_pdf_images.py <pdf文件路径> [输出目录]")
        print()
        print("示例:")
        print("  python extract_pdf_images.py input/需求文档.pdf")
        print("  python extract_pdf_images.py input/需求文档.pdf output/images")
        print()
        print("可选参数通过环境变量设置:")
        print("  MIN_WIDTH=100    最小宽度(px)")
        print("  MIN_HEIGHT=100   最小高度(px)")
        print("  MIN_SIZE=5120    最小文件大小(bytes)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # 从环境变量读取可选参数
    min_width = int(os.environ.get('MIN_WIDTH', 100))
    min_height = int(os.environ.get('MIN_HEIGHT', 100))
    min_size = int(os.environ.get('MIN_SIZE', 5120))

    result = extract_unique_images(pdf_path, output_dir, min_width, min_height, min_size)

    if result:
        sys.exit(0)
    else:
        print("\n未提取到有效图片")
        sys.exit(1)


if __name__ == "__main__":
    main()

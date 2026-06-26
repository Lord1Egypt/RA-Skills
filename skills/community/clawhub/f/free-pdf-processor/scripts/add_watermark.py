#!/usr/bin/env python3
"""
PDF 水印添加脚本
用法: python add_watermark.py <input.pdf> <output.pdf> <watermark_text> 
      [--opacity 0.3] [--rotation -45] [--font_size 48]
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def add_watermark(
    input_path: str,
    output_path: str,
    watermark_text: str,
    opacity: float = 0.3,
    rotation: int = -45,
    font_size: int = 48
) -> bool:
    """为 PDF 添加水印"""
    doc = fitz.open(input_path)
    
    for page_num, page in enumerate(doc, 1):
        # 获取页面尺寸
        rect = page.rect
        
        # 创建水印文本
        text = watermark_text
        
        # 计算文本宽度（近似）
        # 使用标准字体
        font_name = "helv"
        
        # 创建水印文本对象
        text_point = fitz.Point(rect.width / 2, rect.height / 2)
        
        # 添加水印（每页重复）
        page.insert_text(
            text_point,
            text,
            fontsize=font_size,
            fontname=font_name,
            color=(0.8, 0.8, 0.8),
            opacity=opacity,
            rotate=rotation,
            align=1  # 居中
        )
        
        print(f"已添加水印到第 {page_num} 页")
    
    # 保存
    doc.save(output_path)
    doc.close()
    
    print(f"\n水印添加完成: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='为 PDF 添加水印')
    parser.add_argument('input_path', help='输入 PDF 文件路径')
    parser.add_argument('output_path', help='输出 PDF 文件路径')
    parser.add_argument('watermark_text', help='水印文字')
    parser.add_argument('--opacity', '-o', type=float, default=0.3, help='透明度 (0-1)')
    parser.add_argument('--rotation', '-r', type=int, default=-45, help='旋转角度')
    parser.add_argument('--font_size', '-s', type=int, default=48, help='字体大小')
    
    args = parser.parse_args()
    
    try:
        add_watermark(
            args.input_path,
            args.output_path,
            args.watermark_text,
            args.opacity,
            args.rotation,
            args.font_size
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
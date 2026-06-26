#!/usr/bin/env python3
"""
PDF 压缩脚本
用法: python compress_pdf.py <input.pdf> <output.pdf> [--level 1-5]
"""
import sys
import argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def compress_pdf(input_path: str, output_path: str, level: int = 2) -> bool:
    """压缩 PDF 文件"""
    doc = fitz.open(input_path)
    original_size = Path(input_path).stat().st_size
    
    # 保存选项
    # garbage: 清理未使用对象 (0-4)
    # deflate: 压缩内容流
    # clean: 清理 graphics 状态
    
    save_options = {
        'garbage': min(level, 4),
        'deflate': True,
        'clean': True
    }
    
    if level >= 3:
        save_options['compress_images'] = True
    
    doc.save(output_path, **save_options)
    doc.close()
    
    compressed_size = Path(output_path).stat().st_size
    ratio = (1 - compressed_size / original_size) * 100
    
    print(f"压缩完成: {output_path}")
    print(f"原始大小: {original_size / 1024:.1f} KB")
    print(f"压缩后: {compressed_size / 1024:.1f} KB")
    print(f"压缩率: {ratio:.1f}%")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='压缩 PDF')
    parser.add_argument('input_path', help='输入 PDF 文件路径')
    parser.add_argument('output_path', help='输出 PDF 文件路径')
    parser.add_argument('--level', '-l', type=int, default=2, 
                       choices=[1, 2, 3, 4, 5], help='压缩级别 (1=低, 5=高)')
    
    args = parser.parse_args()
    
    try:
        compress_pdf(args.input_path, args.output_path, args.level)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

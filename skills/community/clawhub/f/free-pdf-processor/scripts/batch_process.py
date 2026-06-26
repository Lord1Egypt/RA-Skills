#!/usr/bin/env python3
"""
PDF 批量处理脚本
用法: python batch_process.py <input_dir> <output_dir> --operation <operation> [options]
支持的操作:
  - extract_text: 提取文本
  - extract_images: 提取图片  
  - add_watermark: 添加水印
  - compress: 压缩 PDF
示例: 
  python batch_process.py ./input ./output --operation extract_text
  python batch_process.py ./input ./output --operation add_watermark --text "机密"
"""
import sys
import os
import argparse
from pathlib import Path

# 导入各功能模块
from extract_text import extract_text
from extract_images import extract_images
from add_watermark import add_watermark


def batch_process(input_dir: str, output_dir: str, operation: str, **options) -> dict:
    """批量处理 PDF 文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找所有 PDF 文件
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"在 {input_dir} 中未找到 PDF 文件")
        return {'success': 0, 'failed': 0}
    
    results = {'success': 0, 'failed': 0, 'details': []}
    
    for pdf_file in pdf_files:
        try:
            print(f"\n处理: {pdf_file.name}")
            
            output_file = output_path / pdf_file.name
            
            if operation == 'extract_text':
                # 文本输出到同名 .txt 文件
                output_txt = output_path / f"{pdf_file.stem}.txt"
                extract_text(str(pdf_file), str(output_txt), options.get('metadata', False))
            
            elif operation == 'extract_images':
                # 图片输出到同名子目录
                img_dir = output_path / pdf_file.stem
                extract_images(str(pdf_file), str(img_dir))
            
            elif operation == 'add_watermark':
                watermark_text = options.get('text', 'WATERMARK')
                add_watermark(str(pdf_file), str(output_file), watermark_text,
                             options.get('opacity', 0.3),
                             options.get('rotation', -45),
                             options.get('font_size', 48))
            
            elif operation == 'compress':
                # 压缩 PDF
                import fitz
                doc = fitz.open(str(pdf_file))
                # 压缩图片
                for page in doc:
                    for img in page.get_images():
                        # 简单压缩
                        pass
                doc.save(str(output_file), garbage=4, deflate=True)
                doc.close()
            
            else:
                print(f"Unknown operation: {operation}")
                continue
            
            results['success'] += 1
            print(f"✓ 完成: {pdf_file.name}")
            
        except Exception as e:
            results['failed'] += 1
            results['details'].append({'file': pdf_file.name, 'error': str(e)})
            print(f"✗ 失败: {pdf_file.name} - {e}")
    
    print(f"\n=== 批量处理完成 ===")
    print(f"成功: {results['success']}")
    print(f"失败: {results['failed']}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='PDF 批量处理')
    parser.add_argument('input_dir', help='输入目录')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--operation', '-op', required=True, 
                       choices=['extract_text', 'extract_images', 'add_watermark', 'compress'],
                       help='要执行的操作')
    parser.add_argument('--text', '-t', help='水印文字 (用于 add_watermark)')
    parser.add_argument('--metadata', '-m', action='store_true', help='包含元数据')
    parser.add_argument('--opacity', '-o', type=float, default=0.3, help='水印透明度')
    parser.add_argument('--rotation', '-r', type=int, default=-45, help='水印旋转角度')
    parser.add_argument('--font_size', '-s', type=int, default=48, help='水印字体大小')
    
    args = parser.parse_args()
    
    options = {
        'text': args.text,
        'metadata': args.metadata,
        'opacity': args.opacity,
        'rotation': args.rotation,
        'font_size': args.font_size,
    }
    
    try:
        batch_process(args.input_dir, args.output_dir, args.operation, **options)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
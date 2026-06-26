#!/usr/bin/env python3
"""
PDF 图片提取脚本
用法: python extract_images.py <pdf_path> <output_dir>
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_images(pdf_path: str, output_dir: str) -> list:
    """提取 PDF 中的所有图片"""
    doc = fitz.open(pdf_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    extracted_images = []
    
    for page_num, page in enumerate(doc, 1):
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            
            image_ext = base_image["ext"]
            image_data = base_image["image"]
            
            # 生成文件名
            filename = f"page{page_num}_img{img_index + 1}.{image_ext}"
            filepath = output_path / filename
            
            # 保存图片
            with open(filepath, "wb") as f:
                f.write(image_data)
            
            extracted_images.append({
                'page': page_num,
                'index': img_index + 1,
                'filename': filename,
                'path': str(filepath),
                'size': len(image_data),
                'ext': image_ext
            })
            
            print(f"提取: 第{page_num}页 - 图片{img_index + 1} -> {filename}")
    
    doc.close()
    
    # 保存图片索引文件
    index_file = output_path / "images_index.json"
    import json
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_images, f, ensure_ascii=False, indent=2)
    
    print(f"\n共提取 {len(extracted_images)} 张图片")
    print(f"索引文件: {index_file}")
    
    return extracted_images


def main():
    parser = argparse.ArgumentParser(description='提取 PDF 图片')
    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('output_dir', help='输出目录')
    
    args = parser.parse_args()
    
    try:
        extract_images(args.pdf_path, args.output_dir)
    except FileNotFoundError:
        print(f"Error: 文件不存在 - {args.pdf_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

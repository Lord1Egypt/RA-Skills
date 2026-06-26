#!/usr/bin/env python3
"""
PDF OCR 识别脚本
用法: python ocr_pdf.py <pdf_path> <output.pdf> [--lang chi_sim+eng]
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing dependency. {e}")
    print("Run: pip install pytesseract pillow pymupdf")
    print("\n注意: 还需要安装 Tesseract OCR 引擎")
    print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    sys.exit(1)


def ocr_pdf(pdf_path: str, output_path: str, lang: str = 'chi_sim+eng') -> bool:
    """对 PDF 进行 OCR 识别"""
    # 检查 Tesseract 路径（Windows 常见位置）
    import os
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break
    
    # 打开 PDF
    input_doc = fitz.open(pdf_path)
    output_doc = fitz.open()
    
    for page_num, page in enumerate(input_doc, 1):
        print(f"处理第 {page_num} 页...")
        
        # 获取页面尺寸
        rect = page.rect
        
        # 将页面转换为图片
        mat = fitz.Matrix(2.0, 2.0)  # 2x 提高分辨率
        pix = page.get_pixmap(matrix=mat)
        
        # 转换为 PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # OCR 识别
        try:
            text = pytesseract.image_to_string(img, lang=lang)
        except Exception as e:
            print(f"  OCR 失败: {e}")
            text = f"[OCR 识别失败，请检查 Tesseract 安装]"
        
        # 创建新页面
        new_page = output_doc.new_page(width=rect.width, height=rect.height)
        
        # 插入原文图片
        new_page.insert_image(rect, pixmap=pix)
        
        # 在图片下方添加识别的文本
        text_height = 500  # 文本区域高度
        if rect.height > text_height:
            # 调整页面大小以容纳文本
            new_page = output_doc.new_page(width=rect.width, height=rect.height + text_height)
            new_page.insert_image(fitz.Rect(0, 0, rect.width, rect.height), pixmap=pix)
            
            # 添加文本
            text_rect = fitz.Rect(0, rect.height, rect.width, rect.height + text_height)
            new_page.insert_textbox(
                text_rect,
                text,
                fontsize=10,
                align=0
            )
        else:
            new_page.insert_image(rect, pixmap=pix)
    
    # 保存
    output_doc.save(output_path)
    output_doc.close()
    input_doc.close()
    
    print(f"OCR 完成: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='PDF OCR 识别')
    parser.add_argument('pdf_path', help='输入 PDF 文件路径')
    parser.add_argument('output_path', help='输出 PDF 文件路径')
    parser.add_argument('--lang', '-l', default='chi_sim+eng', 
                       help='识别语言 (默认: chi_sim+eng)')
    
    args = parser.parse_args()
    
    try:
        ocr_pdf(args.pdf_path, args.output_path, args.lang)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

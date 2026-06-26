#!/usr/bin/env python3
"""
PDF 加密脚本
用法: python encrypt_pdf.py <pdf_path> <output.pdf> <password>
"""
import sys
import argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def encrypt_pdf(input_path: str, output_path: str, password: str) -> bool:
    """加密 PDF 文件"""
    doc = fitz.open(input_path)
    
    # 加密
    doc.save(
        output_path,
        encryption=fitz.PDF_ENCRYPT_AES_256,
        user_pw=password,
        owner_pw=password
    )
    
    doc.close()
    
    print(f"加密完成: {output_path}")
    print(f"密码: {password}")
    return True


def main():
    parser = argparse.ArgumentParser(description='加密 PDF')
    parser.add_argument('input_path', help='输入 PDF 文件路径')
    parser.add_argument('output_path', help='输出 PDF 文件路径')
    parser.add_argument('password', help='加密密码')
    
    args = parser.parse_args()
    
    try:
        encrypt_pdf(args.input_path, args.output_path, args.password)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

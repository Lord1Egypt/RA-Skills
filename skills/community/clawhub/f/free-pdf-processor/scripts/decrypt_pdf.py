#!/usr/bin/env python3
"""
PDF 解密脚本
用法: python decrypt_pdf.py <encrypted.pdf> <output.pdf> <password>
"""
import sys
import argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def decrypt_pdf(input_path: str, output_path: str, password: str) -> bool:
    """解密 PDF 文件"""
    # 打开加密的 PDF（需要密码）
    doc = fitz.open(input_path)
    
    # 验证密码
    if doc.is_encrypted:
        if not doc.authenticate(password):
            doc.close()
            print("Error: 密码错误")
            return False
    
    # 移除加密并保存
    doc.save(output_path, encryption=0)
    doc.close()
    
    print(f"解密完成: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='解密 PDF')
    parser.add_argument('input_path', help='输入加密的 PDF 文件路径')
    parser.add_argument('output_path', help='输出 PDF 文件路径')
    parser.add_argument('password', help='解密密码')
    
    args = parser.parse_args()
    
    try:
        decrypt_pdf(args.input_path, args.output_path, args.password)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

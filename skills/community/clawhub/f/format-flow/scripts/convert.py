#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档格式转换工具 - 主入口
支持: Word ↔ PDF ↔ Markdown + Web/Text/Excel/Image

模块化版本 v3.0
"""

import sys
import argparse
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

# 检查并安装依赖
from utils import (
    check_and_install_dependencies, 
    get_file_list, 
    print_info, 
    print_error,
    print_feature_status
)

success, missing = check_and_install_dependencies()
if not success:
    print_error(f"Failed to install dependencies: {', '.join(missing)}")
    sys.exit(1)

# 导入转换器
from converters import (
    # 文档转换
    convert_word_to_pdf,
    batch_convert_word_to_pdf,
    convert_word_to_markdown,
    batch_convert_word_to_markdown,
    convert_pdf_to_markdown,
    batch_convert_pdf_to_markdown,
    convert_markdown_to_word,
    batch_convert_markdown_to_word,
    
    # 网页转换
    convert_url_to_markdown,
    convert_html_file_to_markdown,
    batch_convert_urls_to_markdown,
    
    # 文本格式化
    format_notes,
    batch_format_notes,
    
    # Excel 转换
    convert_excel_to_json,
    batch_convert_excel_to_json,
    get_sheet_names,
    
    # 图片处理
    compress_image,
    convert_image_format,
    resize_image,
    batch_compress_images,
    batch_convert_format
)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Format Flow - Seamless Multi-Format Document Converter v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Word → PDF
  python convert.py word2pdf document.docx
  python convert.py word2pdf --batch ./documents
  
  # Word → Markdown (extract images)
  python convert.py word2md document.docx
  python convert.py word2md --batch ./documents --recursive
  
  # PDF → Markdown
  python convert.py pdf2md document.pdf
  
  # Markdown → Word
  python convert.py md2word document.md
  
  # Web → Markdown
  python convert.py web2md https://example.com
  python convert.py web2md page.html
  
  # Text Formatter
  python convert.py textfmt notes.txt --operations normalize titles paragraphs
  
  # Excel → JSON
  python convert.py excel2json data.xlsx --format records
  
  # Image Compress
  python convert.py imgcompress photo.jpg --quality 85
  python convert.py imgcompress --batch ./images --quality 85
  
  # Image Convert
  python convert.py imgconvert photo.png --format jpeg

For more information, visit: https://github.com/your-repo/doc-converter
        """
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='Conversion type')
    
    # ============ 文档转换命令 ============
    
    # Word → PDF
    parser_word2pdf = subparsers.add_parser('word2pdf', help='Convert Word to PDF')
    parser_word2pdf.add_argument('input', help='Word file or directory')
    parser_word2pdf.add_argument('-o', '--output', help='Output file or directory')
    parser_word2pdf.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_word2pdf.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_word2pdf.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # Word → Markdown
    parser_word2md = subparsers.add_parser('word2md', help='Convert Word to Markdown')
    parser_word2md.add_argument('input', help='Word file or directory')
    parser_word2md.add_argument('-o', '--output', help='Output file or directory')
    parser_word2md.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_word2md.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_word2md.add_argument('--no-images', action='store_true', help='Skip image extraction')
    parser_word2md.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # PDF → Markdown
    parser_pdf2md = subparsers.add_parser('pdf2md', help='Convert PDF to Markdown')
    parser_pdf2md.add_argument('input', help='PDF file or directory')
    parser_pdf2md.add_argument('-o', '--output', help='Output file or directory')
    parser_pdf2md.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_pdf2md.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_pdf2md.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # Markdown → Word
    parser_md2word = subparsers.add_parser('md2word', help='Convert Markdown to Word')
    parser_md2word.add_argument('input', help='Markdown file or directory')
    parser_md2word.add_argument('-o', '--output', help='Output file or directory')
    parser_md2word.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_md2word.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_md2word.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # ============ 网页转换命令 ============
    
    # Web → Markdown
    parser_web2md = subparsers.add_parser('web2md', help='Convert web page/HTML to Markdown')
    parser_web2md.add_argument('input', help='URL or HTML file path')
    parser_web2md.add_argument('-o', '--output', help='Output Markdown file')
    parser_web2md.add_argument('--batch', action='store_true', help='Batch conversion (for URLs from file)')
    parser_web2md.add_argument('--no-metadata', action='store_true', help='Skip metadata')
    parser_web2md.add_argument('--no-clean', action='store_true', help='Skip content cleaning')
    parser_web2md.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # ============ 文本格式化命令 ============
    
    # Text Formatter
    parser_textfmt = subparsers.add_parser('textfmt', help='Format plain text notes')
    parser_textfmt.add_argument('input', help='Text file or directory')
    parser_textfmt.add_argument('-o', '--output', help='Output file or directory')
    parser_textfmt.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_textfmt.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_textfmt.add_argument('--operations', nargs='+', 
                                choices=['normalize', 'titles', 'paragraphs', 'lists', 
                                        'linenumbers', 'outline', 'toc', 'timestamp'],
                                default=['normalize', 'titles', 'paragraphs'],
                                help='Formatting operations to apply')
    parser_textfmt.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # ============ Excel 转换命令 ============
    
    # Excel → JSON
    parser_excel2json = subparsers.add_parser('excel2json', help='Convert Excel to JSON')
    parser_excel2json.add_argument('input', help='Excel file or directory')
    parser_excel2json.add_argument('-o', '--output', help='Output JSON file or directory')
    parser_excel2json.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_excel2json.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_excel2json.add_argument('--format', choices=['records', 'grouped', 'nested', 'array'],
                                   default='records', help='JSON format type')
    parser_excel2json.add_argument('--sheet', help='Sheet name (default: first sheet)')
    parser_excel2json.add_argument('--group-column', help='Group column name (for "grouped" format)')
    parser_excel2json.add_argument('--key-columns', nargs='+', help='Key column names (for "nested" format)')
    parser_excel2json.add_argument('--indent', type=int, default=2, help='JSON indent')
    parser_excel2json.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # ============ 图片处理命令 ============
    
    # Image Compress
    parser_imgcompress = subparsers.add_parser('imgcompress', help='Compress images')
    parser_imgcompress.add_argument('input', help='Image file or directory')
    parser_imgcompress.add_argument('-o', '--output', help='Output file or directory')
    parser_imgcompress.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_imgcompress.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_imgcompress.add_argument('--quality', type=int, default=85, help='Compression quality (1-100)')
    parser_imgcompress.add_argument('--max-size', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                                    help='Maximum dimensions')
    parser_imgcompress.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # Image Convert
    parser_imgconvert = subparsers.add_parser('imgconvert', help='Convert image format')
    parser_imgconvert.add_argument('input', help='Image file or directory')
    parser_imgconvert.add_argument('-o', '--output', help='Output file or directory')
    parser_imgconvert.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_imgconvert.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_imgconvert.add_argument('--format', required=True, 
                                   choices=['PNG', 'JPEG', 'WEBP', 'GIF', 'BMP'],
                                   help='Target format')
    parser_imgconvert.add_argument('--quality', type=int, default=95, help='Quality for JPEG/WEBP')
    parser_imgconvert.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # Image Resize
    parser_imgresize = subparsers.add_parser('imgresize', help='Resize images')
    parser_imgresize.add_argument('input', help='Image file or directory')
    parser_imgresize.add_argument('-o', '--output', help='Output file or directory')
    parser_imgresize.add_argument('--batch', action='store_true', help='Batch conversion')
    parser_imgresize.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser_imgresize.add_argument('--size', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                                  help='Target size')
    parser_imgresize.add_argument('--scale', type=float, help='Scale factor')
    parser_imgresize.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # 显示功能状态
    parser.add_argument('--status', action='store_true', help='Show feature availability status')
    
    args = parser.parse_args()
    
    # 显示功能状态
    if hasattr(args, 'status') and args.status:
        print_feature_status()
        return
    
    if not args.command:
        parser.print_help()
        print("\nUse --status to check feature availability")
        return
    
    input_path = Path(args.input)
    verbose = not args.quiet
    
    # ============ 执行转换 ============
    
    # 文档转换
    if args.command == 'word2pdf':
        if args.batch:
            files = get_file_list(input_path, ['.docx', '.doc'], args.recursive)
            if not files:
                print_error("No Word files found")
                return
            batch_convert_word_to_pdf(files, verbose=verbose)
        else:
            convert_word_to_pdf(input_path, 
                               output_path=Path(args.output) if args.output else None,
                               verbose=verbose)
    
    elif args.command == 'word2md':
        if args.batch:
            files = get_file_list(input_path, ['.docx', '.doc'], args.recursive)
            if not files:
                print_error("No Word files found")
                return
            batch_convert_word_to_markdown(
                files, 
                extract_images=not args.no_images,
                verbose=verbose
            )
        else:
            convert_word_to_markdown(
                input_path,
                output_path=Path(args.output) if args.output else None,
                extract_images=not args.no_images,
                verbose=verbose
            )
    
    elif args.command == 'pdf2md':
        if args.batch:
            files = get_file_list(input_path, ['.pdf'], args.recursive)
            if not files:
                print_error("No PDF files found")
                return
            batch_convert_pdf_to_markdown(files, verbose=verbose)
        else:
            convert_pdf_to_markdown(
                input_path,
                output_path=Path(args.output) if args.output else None,
                verbose=verbose
            )
    
    elif args.command == 'md2word':
        if args.batch:
            files = get_file_list(input_path, ['.md', '.markdown'], args.recursive)
            if not files:
                print_error("No Markdown files found")
                return
            batch_convert_markdown_to_word(files, verbose=verbose)
        else:
            convert_markdown_to_word(
                input_path,
                output_path=Path(args.output) if args.output else None,
                verbose=verbose
            )
    
    # 网页转换
    elif args.command == 'web2md':
        # 判断是 URL 还是本地文件
        if input_path.suffix.lower() in ['.html', '.htm']:
            # 本地 HTML 文件
            convert_html_file_to_markdown(
                input_path,
                output_path=Path(args.output) if args.output else None,
                verbose=verbose
            )
        else:
            # URL
            convert_url_to_markdown(
                args.input,  # 保持原样（可能是 URL 字符串）
                output_path=Path(args.output) if args.output else None,
                include_metadata=not args.no_metadata,
                clean_content=not args.no_clean,
                verbose=verbose
            )
    
    # 文本格式化
    elif args.command == 'textfmt':
        if args.batch:
            files = get_file_list(input_path, ['.txt', '.text', '.md'], args.recursive)
            if not files:
                print_error("No text files found")
                return
            batch_format_notes(files, operations=args.operations, verbose=verbose)
        else:
            format_notes(
                input_path,
                output_path=Path(args.output) if args.output else None,
                operations=args.operations,
                verbose=verbose
            )
    
    # Excel 转换
    elif args.command == 'excel2json':
        if args.batch:
            files = get_file_list(input_path, ['.xlsx', '.xls'], args.recursive)
            if not files:
                print_error("No Excel files found")
                return
            batch_convert_excel_to_json(files, format_type=args.format, verbose=verbose)
        else:
            convert_excel_to_json(
                input_path,
                output_path=Path(args.output) if args.output else None,
                format_type=args.format,
                sheet_name=args.sheet,
                group_column=args.group_column,
                key_columns=args.key_columns,
                indent=args.indent,
                verbose=verbose
            )
    
    # 图片处理
    elif args.command == 'imgcompress':
        if args.batch:
            files = get_file_list(input_path, ['.jpg', '.jpeg', '.png', '.webp', '.gif'], args.recursive)
            if not files:
                print_error("No image files found")
                return
            max_size = tuple(args.max_size) if args.max_size else None
            batch_compress_images(files, quality=args.quality, max_size=max_size, verbose=verbose)
        else:
            max_size = tuple(args.max_size) if args.max_size else None
            compress_image(
                input_path,
                output_path=Path(args.output) if args.output else None,
                quality=args.quality,
                max_size=max_size,
                verbose=verbose
            )
    
    elif args.command == 'imgconvert':
        if args.batch:
            files = get_file_list(input_path, ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'], args.recursive)
            if not files:
                print_error("No image files found")
                return
            batch_convert_format(files, target_format=args.format, quality=args.quality, verbose=verbose)
        else:
            convert_image_format(
                input_path,
                output_path=Path(args.output) if args.output else None,
                target_format=args.format,
                quality=args.quality,
                verbose=verbose
            )
    
    elif args.command == 'imgresize':
        size = tuple(args.size) if args.size else None
        resize_image(
            input_path,
            output_path=Path(args.output) if args.output else None,
            size=size,
            scale=args.scale,
            verbose=verbose
        )


if __name__ == '__main__':
    main()

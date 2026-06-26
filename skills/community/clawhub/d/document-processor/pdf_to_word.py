#!/usr/bin/env python3
"""
PDF转Word工具
将PDF文件转换为Word文档，尽量保留原始格式
"""

import sys
import os
import argparse
from pathlib import Path

try:
    from pdf2docx import Converter
    PDF2DOCX_AVAILABLE = True
except ImportError:
    PDF2DOCX_AVAILABLE = False
    print("警告: pdf2docx 库未安装，部分功能可能受限")

try:
    from PyPDF2 import PdfReader
    PYPYDF2_AVAILABLE = True
except ImportError:
    PYPYDF2_AVAILABLE = False

class PDFToWordConverter:
    def __init__(self):
        self.pdf_path = None
        self.word_path = None
        
    def check_dependencies(self):
        """检查依赖库"""
        if not PDF2DOCX_AVAILABLE:
            print("错误: 需要安装 pdf2docx 库")
            print("安装命令: pip install pdf2docx")
            return False
        return True
    
    def validate_pdf(self, pdf_path):
        """验证PDF文件"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"文件格式不支持: {pdf_path}，请提供PDF文件")
        
        # 检查文件大小
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            raise ValueError("PDF文件为空")
        
        if file_size > 100 * 1024 * 1024:  # 100MB
            print(f"警告: 文件较大 ({file_size/1024/1024:.1f} MB)，转换可能需要较长时间")
        
        return True
    
    def convert(self, pdf_path, word_path, pages=None):
        """转换PDF到Word"""
        if not self.check_dependencies():
            return False
        
        self.pdf_path = pdf_path
        self.word_path = word_path
        
        try:
            # 验证PDF文件
            self.validate_pdf(pdf_path)
            
            print(f"📄 输入PDF: {pdf_path}")
            print(f"📝 输出Word: {word_path}")
            
            # 获取PDF页数
            if PYPYDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    total_pages = len(reader.pages)
                    print(f"📊 PDF总页数: {total_pages}")
            
            print("🔄 开始转换PDF到Word...")
            
            # 创建转换器
            cv = Converter(pdf_path)
            
            # 设置转换参数
            cv.convert(
                word_path,
                start=0,  # 从第0页开始
                end=None,  # 到最后一页
                pages=pages  # 指定页面
            )
            
            # 关闭转换器
            cv.close()
            
            print("✅ 转换完成!")
            
            # 验证输出文件
            if os.path.exists(word_path):
                file_size = os.path.getsize(word_path)
                print(f"📦 输出文件大小: {file_size / 1024:.2f} KB")
                return True
            else:
                print("❌ 错误: 输出文件未生成")
                return False
                
        except Exception as e:
            print(f"❌ 转换失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert_with_options(self, pdf_path, word_path, **options):
        """使用选项转换PDF到Word"""
        if not self.check_dependencies():
            return False
        
        try:
            print(f"📄 输入PDF: {pdf_path}")
            print(f"📝 输出Word: {word_path}")
            
            # 创建转换器
            cv = Converter(pdf_path)
            
            # 提取转换选项
            start_page = options.get('start_page', 0)
            end_page = options.get('end_page', None)
            pages = options.get('pages', None)
            
            print("🔄 开始转换...")
            
            # 执行转换
            cv.convert(
                word_path,
                start=start_page,
                end=end_page,
                pages=pages
            )
            
            cv.close()
            
            print("✅ 转换完成!")
            return True
            
        except Exception as e:
            print(f"❌ 转换失败: {str(e)}")
            return False

def batch_convert(input_dir, output_dir, pattern="*.pdf"):
    """批量转换PDF文件"""
    if not PDF2DOCX_AVAILABLE:
        print("错误: 需要安装 pdf2docx 库")
        return False
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return False
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找PDF文件
    pdf_files = list(input_path.glob(pattern))
    
    if not pdf_files:
        print(f"在 {input_dir} 中未找到PDF文件")
        return False
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    converter = PDFToWordConverter()
    success_count = 0
    fail_count = 0
    
    for pdf_file in pdf_files:
        print(f"\n处理文件: {pdf_file.name}")
        
        # 生成输出文件名
        word_file = output_path / f"{pdf_file.stem}.docx"
        
        try:
            if converter.convert(str(pdf_file), str(word_file)):
                success_count += 1
                print(f"✅ 成功: {pdf_file.name} -> {word_file.name}")
            else:
                fail_count += 1
                print(f"❌ 失败: {pdf_file.name}")
                
        except Exception as e:
            fail_count += 1
            print(f"❌ 错误: {pdf_file.name} - {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"批量转换完成!")
    print(f"✅ 成功: {success_count} 个文件")
    print(f"❌ 失败: {fail_count} 个文件")
    print(f"📁 输出目录: {output_dir}")
    
    return success_count > 0

def main():
    parser = argparse.ArgumentParser(
        description='PDF转Word工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 单个文件转换
  %(prog)s input.pdf output.docx
  
  # 批量转换
  %(prog)s --batch ./pdfs ./docs
  
  # 转换指定页面
  %(prog)s input.pdf output.docx --pages "1,3,5-7"
  
  # 转换页面范围
  %(prog)s input.pdf output.docx --start 1 --end 10
        """
    )
    
    # 主要参数
    parser.add_argument('input', nargs='?', help='输入PDF文件路径')
    parser.add_argument('output', nargs='?', help='输出Word文件路径')
    
    # 批量处理选项
    parser.add_argument('--batch', action='store_true', help='批量转换模式')
    parser.add_argument('--input-dir', help='输入目录（批量模式）')
    parser.add_argument('--output-dir', help='输出目录（批量模式）')
    parser.add_argument('--pattern', default='*.pdf', help='文件匹配模式（默认: *.pdf）')
    
    # 转换选项
    parser.add_argument('--pages', type=str, help='指定页面，如 "1,3,5-7"')
    parser.add_argument('--start', type=int, help='开始页码（从1开始）')
    parser.add_argument('--end', type=int, help='结束页码')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not PDF2DOCX_AVAILABLE:
        print("错误: 需要安装 pdf2docx 库")
        print("安装命令: pip install pdf2docx")
        return 1
    
    converter = PDFToWordConverter()
    
    # 批量模式
    if args.batch:
        input_dir = args.input_dir or args.input
        output_dir = args.output_dir or args.output
        
        if not input_dir or not output_dir:
            parser.error("批量模式需要 --input-dir 和 --output-dir 参数")
        
        success = batch_convert(input_dir, output_dir, args.pattern)
        return 0 if success else 1
    
    # 单个文件模式
    if not args.input or not args.output:
        parser.error("单个文件模式需要 input 和 output 参数")
    
    print("=" * 50)
    print("PDF转Word转换工具")
    print("=" * 50)
    
    # 准备转换选项
    options = {}
    
    if args.pages:
        # 解析页面参数
        pages = []
        for part in args.pages.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start-1, end))  # pdf2docx使用0-based索引
            else:
                pages.append(int(part)-1)
        options['pages'] = pages
    
    if args.start:
        options['start_page'] = args.start - 1  # 转换为0-based
    
    if args.end:
        options['end_page'] = args.end - 1  # 转换为0-based
    
    # 执行转换
    if options:
        success = converter.convert_with_options(args.input, args.output, **options)
    else:
        success = converter.convert(args.input, args.output)
    
    print("=" * 50)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
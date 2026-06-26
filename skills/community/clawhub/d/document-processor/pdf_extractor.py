#!/usr/bin/env python3
"""
PDF页面提取工具 - 增强版
支持多种提取模式：页面范围、特定页面、奇数页、偶数页等
"""

import sys
import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

class PDFExtractor:
    def __init__(self):
        self.reader = None
        self.writer = None
    
    def open_pdf(self, pdf_path):
        """打开PDF文件"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"文件格式不支持: {pdf_path}，请提供PDF文件")
        
        try:
            self.reader = PdfReader(pdf_path)
            return len(self.reader.pages)
        except Exception as e:
            raise ValueError(f"无法读取PDF文件: {str(e)}")
    
    def extract_pages(self, start_page, end_page, output_path):
        """提取指定范围的页面"""
        if not self.reader:
            raise ValueError("请先打开PDF文件")
        
        total_pages = len(self.reader.pages)
        
        # 验证页码范围
        if start_page < 1 or start_page > total_pages:
            raise ValueError(f"开始页码 {start_page} 超出范围 (1-{total_pages})")
        if end_page < 1 or end_page > total_pages:
            raise ValueError(f"结束页码 {end_page} 超出范围 (1-{total_pages})")
        if start_page > end_page:
            raise ValueError(f"开始页码 {start_page} 不能大于结束页码 {end_page}")
        
        # 创建PDF写入器
        self.writer = PdfWriter()
        
        # 提取页面
        extracted_pages = 0
        print(f"正在提取第 {start_page} 页到第 {end_page} 页...")
        for page_num in range(start_page - 1, end_page):
            page = self.reader.pages[page_num]
            self.writer.add_page(page)
            extracted_pages += 1
            print(f"  ✓ 已添加第 {page_num + 1} 页")
        
        # 写入输出文件
        print(f"正在写入输出文件: {output_path}")
        with open(output_path, 'wb') as output_file:
            self.writer.write(output_file)
        
        return extracted_pages
    
    def extract_specific_pages(self, page_numbers, output_path):
        """提取指定的多个页面"""
        if not self.reader:
            raise ValueError("请先打开PDF文件")
        
        total_pages = len(self.reader.pages)
        
        # 创建PDF写入器
        self.writer = PdfWriter()
        
        # 提取页面
        extracted_pages = 0
        print(f"正在提取指定页面: {page_numbers}")
        for page_num in page_numbers:
            if page_num < 1 or page_num > total_pages:
                print(f"  ⚠ 警告: 页码 {page_num} 超出范围，已跳过")
                continue
            
            page = self.reader.pages[page_num - 1]
            self.writer.add_page(page)
            extracted_pages += 1
            print(f"  ✓ 已添加第 {page_num} 页")
        
        # 写入文件
        with open(output_path, 'wb') as output_file:
            self.writer.write(output_file)
        
        return extracted_pages
    
    def extract_even_pages(self, output_path):
        """提取所有偶数页"""
        if not self.reader:
            raise ValueError("请先打开PDF文件")
        
        self.writer = PdfWriter()
        extracted_pages = 0
        
        print("正在提取所有偶数页...")
        for i, page in enumerate(self.reader.pages):
            if (i + 1) % 2 == 0:  # 偶数页（第2、4、6...页）
                self.writer.add_page(page)
                extracted_pages += 1
                print(f"  ✓ 已添加第 {i + 1} 页（偶数页）")
        
        with open(output_path, 'wb') as output_file:
            self.writer.write(output_file)
        
        return extracted_pages
    
    def extract_odd_pages(self, output_path):
        """提取所有奇数页"""
        if not self.reader:
            raise ValueError("请先打开PDF文件")
        
        self.writer = PdfWriter()
        extracted_pages = 0
        
        print("正在提取所有奇数页...")
        for i, page in enumerate(self.reader.pages):
            if (i + 1) % 2 == 1:  # 奇数页（第1、3、5...页）
                self.writer.add_page(page)
                extracted_pages += 1
                print(f"  ✓ 已添加第 {i + 1} 页（奇数页）")
        
        with open(output_path, 'wb') as output_file:
            self.writer.write(output_file)
        
        return extracted_pages
    
    def extract_by_interval(self, interval, start=1, output_path=None):
        """按间隔提取页面（如每3页提取1页）"""
        if not self.reader:
            raise ValueError("请先打开PDF文件")
        
        if interval < 1:
            raise ValueError("间隔必须大于0")
        
        self.writer = PdfWriter()
        extracted_pages = 0
        
        print(f"正在按间隔 {interval} 提取页面（从第 {start} 页开始）...")
        for i in range(start - 1, len(self.reader.pages), interval):
            page = self.reader.pages[i]
            self.writer.add_page(page)
            extracted_pages += 1
            print(f"  ✓ 已添加第 {i + 1} 页")
        
        if output_path:
            with open(output_path, 'wb') as output_file:
                self.writer.write(output_file)
        
        return extracted_pages

def parse_page_spec(spec):
    """解析页面规格字符串"""
    page_numbers = []
    parts = spec.split(',')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if '-' in part:
            # 处理页码范围
            range_parts = part.split('-')
            if len(range_parts) != 2:
                raise ValueError(f"无效的页码范围: {part}")
            
            try:
                start = int(range_parts[0])
                end = int(range_parts[1])
                if start > end:
                    start, end = end, start  # 自动纠正顺序
                page_numbers.extend(range(start, end + 1))
            except ValueError:
                raise ValueError(f"无效的页码: {part}")
        else:
            # 处理单个页码
            try:
                page_numbers.append(int(part))
            except ValueError:
                raise ValueError(f"无效的页码: {part}")
    
    # 去重并排序
    return sorted(set(page_numbers))

def main():
    parser = argparse.ArgumentParser(
        description='PDF页面提取工具 - 支持多种提取模式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 提取页面范围
  %(prog)s input.pdf output.pdf --start 14 --end 29
  
  # 提取特定页面
  %(prog)s input.pdf output.pdf --pages "1,3,5-7,10"
  
  # 提取所有奇数页
  %(prog)s input.pdf output.pdf --odd
  
  # 提取所有偶数页
  %(prog)s input.pdf output.pdf --even
  
  # 按间隔提取（每3页提取1页）
  %(prog)s input.pdf output.pdf --interval 3
        """
    )
    
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('output', help='输出PDF文件路径')
    
    # 提取模式选项
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--start', type=int, help='开始页码（从1开始）')
    group.add_argument('-p', '--pages', type=str, help='指定多个页码，用逗号分隔，例如: 1,3,5-7,10')
    group.add_argument('--odd', action='store_true', help='提取所有奇数页')
    group.add_argument('--even', action='store_true', help='提取所有偶数页')
    group.add_argument('--interval', type=int, help='按间隔提取页面（如每3页提取1页）')
    
    # 其他选项
    parser.add_argument('-e', '--end', type=int, help='结束页码（包含），与--start一起使用')
    parser.add_argument('--start-page', type=int, default=1, help='间隔提取的起始页码（默认: 1）')
    
    args = parser.parse_args()
    
    # 参数验证
    if args.start and not args.end:
        parser.error("--start 参数需要与 --end 参数一起使用")
    if args.end and not args.start:
        parser.error("--end 参数需要与 --start 参数一起使用")
    if args.start and args.start < 1:
        parser.error("开始页码必须大于0")
    if args.end and args.end < 1:
        parser.error("结束页码必须大于0")
    if args.start and args.end and args.start > args.end:
        # 自动交换
        args.start, args.end = args.end, args.start
        print(f"注意: 已自动调整页码范围为 {args.start}-{args.end}")
    
    # 创建提取器
    extractor = PDFExtractor()
    
    try:
        # 打开PDF文件
        print("=" * 50)
        print("PDF页面提取工具")
        print("=" * 50)
        
        total_pages = extractor.open_pdf(args.input)
        print(f"📄 输入文件: {args.input}")
        print(f"📊 总页数: {total_pages}")
        print(f"💾 输出文件: {args.output}")
        print("-" * 50)
        
        extracted_count = 0
        
        # 根据模式提取页面
        if args.pages:
            page_numbers = parse_page_spec(args.pages)
            extracted_count = extractor.extract_specific_pages(page_numbers, args.output)
        
        elif args.start and args.end:
            extracted_count = extractor.extract_pages(args.start, args.end, args.output)
        
        elif args.odd:
            extracted_count = extractor.extract_odd_pages(args.output)
        
        elif args.even:
            extracted_count = extractor.extract_even_pages(args.output)
        
        elif args.interval:
            extracted_count = extractor.extract_by_interval(
                args.interval, args.start_page, args.output
            )
        
        # 输出结果
        print("-" * 50)
        print(f"✅ 提取完成!")
        print(f"📄 提取页数: {extracted_count}")
        print(f"💾 输出文件: {args.output}")
        
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"📦 文件大小: {file_size / 1024:.2f} KB")
            
            # 验证输出
            try:
                output_reader = PdfReader(args.output)
                print(f"🔍 验证: 输出文件包含 {len(output_reader.pages)} 页")
            except:
                print("⚠ 警告: 无法验证输出文件")
        
        print("=" * 50)
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {str(e)}")
        return 1
    except ValueError as e:
        print(f"❌ 错误: {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
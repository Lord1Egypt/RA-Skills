#!/usr/bin/env python3
"""
PDF OCR工具 - 识别扫描件PDF中的页码和文字
使用Tesseract OCR引擎识别图片中的文字
"""

import sys
import os
import re
import argparse
import tempfile
from pathlib import Path

try:
    import pdf2image
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class PDFOCRProcessor:
    def __init__(self):
        self.temp_dir = None
        self.ocr_results = []
        
    def check_dependencies(self):
        """检查OCR依赖"""
        missing = []
        
        if not PDF2IMAGE_AVAILABLE:
            missing.append("pdf2image")
            print("警告: 需要安装 pdf2image: pip install pdf2image")
        
        if not TESSERACT_AVAILABLE:
            missing.append("pytesseract 和 Pillow")
            print("警告: 需要安装:")
            print("  pip install pytesseract pillow")
            print("还需要安装 Tesseract OCR 引擎:")
            print("  macOS: brew install tesseract")
            print("  Ubuntu: sudo apt-get install tesseract-ocr")
            print("  Windows: 下载安装 Tesseract")
        
        if missing:
            print(f"❌ 缺少依赖: {', '.join(missing)}")
            return False
        
        # 检查Tesseract是否可用
        try:
            pytesseract.get_tesseract_version()
            print("✅ Tesseract OCR 可用")
            return True
        except Exception as e:
            print(f"❌ Tesseract 不可用: {str(e)}")
            return False
    
    def extract_page_images(self, pdf_path, pages=None, dpi=150):
        """从PDF提取页面为图片"""
        if not PDF2IMAGE_AVAILABLE:
            raise ImportError("需要安装 pdf2image")
        
        print(f"📄 从PDF提取图片 (DPI: {dpi})...")
        
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp(prefix="pdf_ocr_")
        print(f"📁 临时目录: {self.temp_dir}")
        
        try:
            # 转换PDF为图片
            images = pdf2image.convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=pages[0] if pages else None,
                last_page=pages[-1] if pages else None,
                output_folder=self.temp_dir,
                fmt='png',
                thread_count=4
            )
            
            print(f"✅ 提取了 {len(images)} 张图片")
            return images
            
        except Exception as e:
            print(f"❌ 提取图片失败: {str(e)}")
            # 清理临时目录
            self.cleanup()
            raise
    
    def ocr_image(self, image, page_num, language='chi_sim+eng'):
        """对单张图片进行OCR识别"""
        if not TESSERACT_AVAILABLE:
            raise ImportError("需要安装 pytesseract 和 Pillow")
        
        print(f"  🔍 OCR识别第 {page_num} 页...")
        
        try:
            # 使用Tesseract进行OCR
            text = pytesseract.image_to_string(
                image,
                lang=language,
                config='--psm 6'  # 假设为统一文本块
            )
            
            # 保存图片用于调试
            debug_path = os.path.join(self.temp_dir, f"page_{page_num:03d}.png")
            image.save(debug_path)
            
            return {
                'page_num': page_num,
                'text': text,
                'image_path': debug_path,
                'language': language
            }
            
        except Exception as e:
            print(f"  ❌ 第 {page_num} 页OCR失败: {str(e)}")
            return {
                'page_num': page_num,
                'text': '',
                'error': str(e)
            }
    
    def find_page_numbers(self, ocr_results, search_range=None):
        """从OCR结果中查找页码"""
        print("\n🔢 查找页码...")
        
        page_mapping = {}  # 标注页码 -> 文件页码
        all_numbers = []   # 所有找到的数字
        
        for result in ocr_results:
            file_page = result['page_num']
            text = result['text']
            
            if not text:
                continue
            
            # 查找所有数字
            numbers = re.findall(r'\b(\d{1,3})\b', text)
            
            if numbers:
                # 记录所有找到的数字
                for num in numbers:
                    all_numbers.append((int(num), file_page))
                
                # 特别关注可能出现在底部的数字（可能是页码）
                lines = text.split('\n')
                if lines:
                    # 检查最后几行（页码通常在底部）
                    for line in lines[-3:]:
                        line_nums = re.findall(r'\b(\d{1,3})\b', line.strip())
                        for num in line_nums:
                            page_num = int(num)
                            # 如果这个数字看起来像页码（在合理范围内）
                            if 1 <= page_num <= 500:
                                if page_num not in page_mapping:
                                    page_mapping[page_num] = file_page
                                    print(f"  📍 可能页码 {page_num} -> 文件第 {file_page} 页")
        
        # 如果没有找到明显的页码，显示所有找到的数字
        if not page_mapping and all_numbers:
            print("\n📊 所有找到的数字:")
            for num, file_page in sorted(all_numbers, key=lambda x: x[1]):
                print(f"  文件第 {file_page:3d} 页: 数字 {num}")
        
        return page_mapping
    
    def analyze_pdf_structure(self, pdf_path, start_page=1, end_page=50, language='chi_sim+eng'):
        """分析PDF结构，识别页码"""
        if not self.check_dependencies():
            return None
        
        print("="*60)
        print("PDF OCR页码识别工具")
        print("="*60)
        print(f"📄 分析文件: {pdf_path}")
        print(f"📖 分析页面: {start_page} - {end_page}")
        print(f"🗣️  OCR语言: {language}")
        print("="*60)
        
        try:
            # 提取指定范围的页面图片
            pages_to_analyze = list(range(start_page, end_page + 1))
            images = self.extract_page_images(pdf_path, pages_to_analyze)
            
            # 对每张图片进行OCR
            self.ocr_results = []
            for i, image in enumerate(images):
                file_page = start_page + i
                result = self.ocr_image(image, file_page, language)
                self.ocr_results.append(result)
            
            # 查找页码
            page_mapping = self.find_page_numbers(self.ocr_results)
            
            # 显示OCR结果摘要
            print("\n📋 OCR结果摘要:")
            pages_with_text = sum(1 for r in self.ocr_results if r['text'].strip())
            print(f"  📄 分析页面数: {len(self.ocr_results)}")
            print(f"  🔤 有文字的页面: {pages_with_text}")
            print(f"  🔢 找到的可能页码: {len(page_mapping)}")
            
            if page_mapping:
                print("\n📊 页码映射:")
                for page_num, file_page in sorted(page_mapping.items()):
                    print(f"  标注页码 {page_num:3d} -> 文件第 {file_page:3d} 页")
                
                # 分析偏移规律
                if len(page_mapping) >= 3:
                    offsets = []
                    for page_num, file_page in page_mapping.items():
                        offsets.append(file_page - page_num)
                    
                    avg_offset = sum(offsets) / len(offsets)
                    print(f"\n📐 平均页码偏移: {avg_offset:.1f} 页")
            
            # 保存详细结果
            self.save_results(pdf_path)
            
            return {
                'page_mapping': page_mapping,
                'ocr_results': self.ocr_results,
                'temp_dir': self.temp_dir
            }
            
        except Exception as e:
            print(f"❌ 分析失败: {str(e)}")
            import traceback
            traceback.print_exc()
            self.cleanup()
            return None
    
    def save_results(self, pdf_path):
        """保存OCR结果"""
        if not self.ocr_results:
            return
        
        results_file = os.path.join(self.temp_dir, "ocr_results.txt")
        
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("PDF OCR分析结果\n")
            f.write("="*60 + "\n\n")
            
            for result in self.ocr_results:
                f.write(f"页面 {result['page_num']}:\n")
                f.write("-"*40 + "\n")
                
                if 'error' in result:
                    f.write(f"错误: {result['error']}\n")
                else:
                    text = result['text'].strip()
                    if text:
                        f.write(text[:500])  # 只保存前500字符
                        if len(text) > 500:
                            f.write("\n... (截断)")
                    else:
                        f.write("[无文字内容]")
                
                f.write("\n\n")
        
        print(f"💾 详细结果保存到: {results_file}")
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
                print(f"🧹 已清理临时目录: {self.temp_dir}")
            except:
                pass
    
    def extract_by_labeled_pages(self, pdf_path, start_label, end_label, output_path, language='chi_sim+eng'):
        """根据标注的页码提取页面"""
        print(f"\n🎯 目标: 提取标注页码 {start_label}-{end_label}")
        
        # 首先分析PDF找到页码映射
        print("🔍 正在分析PDF结构...")
        result = self.analyze_pdf_structure(pdf_path, 1, 100, language)
        
        if not result or 'page_mapping' not in result:
            print("❌ 无法分析PDF页码结构")
            return False
        
        page_mapping = result['page_mapping']
        
        if not page_mapping:
            print("❌ 未找到任何页码")
            return False
        
        # 查找目标页码对应的文件页面
        file_pages = []
        for label in range(start_label, end_label + 1):
            if label in page_mapping:
                file_pages.append(page_mapping[label])
            else:
                print(f"⚠ 未找到标注页码 {label}")
        
        if not file_pages:
            print("❌ 未找到任何目标页码")
            return False
        
        file_start = min(file_pages)
        file_end = max(file_pages)
        
        print(f"\n📄 将提取文件页面: {file_start} - {file_end}")
        
        # 使用PyPDF2提取页面
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            print(f"\n🔄 正在提取...")
            for i in range(file_start - 1, file_end):
                page = reader.pages[i]
                writer.add_page(page)
                print(f"  ✓ 已添加第 {i+1} 页")
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            print(f"\n✅ 提取完成!")
            print(f"💾 输出文件: {output_path}")
            
            # 验证
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                pages = len(PdfReader(output_path).pages)
                print(f"📦 输出: {pages}页, {size/1024:.1f}KB")
            
            # 清理临时文件
            self.cleanup()
            
            return True
            
        except ImportError:
            print("❌ 需要安装 PyPDF2: pip install PyPDF2")
            return False
        except Exception as e:
            print(f"❌ 提取失败: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='PDF OCR工具 - 识别扫描件PDF中的页码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 分析PDF页码结构
  %(prog)s analyze input.pdf --start 1 --end 50
  
  # 根据标注页码提取
  %(prog)s extract input.pdf output.pdf --start-label 14 --end-label 29
  
  # 使用中文OCR
  %(prog)s analyze input.pdf --language chi_sim
  
  # 使用中英文混合OCR
  %(prog)s analyze input.pdf --language chi_sim+eng
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='分析PDF页码结构')
    analyze_parser.add_argument('input', help='输入PDF文件')
    analyze_parser.add_argument('--start', type=int, default=1, help='开始页面 (默认: 1)')
    analyze_parser.add_argument('--end', type=int, default=50, help='结束页面 (默认: 50)')
    analyze_parser.add_argument('--language', default='chi_sim+eng', help='OCR语言 (默认: chi_sim+eng)')
    
    # extract命令
    extract_parser = subparsers.add_parser('extract', help='根据标注页码提取')
    extract_parser.add_argument('input', help='输入PDF文件')
    extract_parser.add_argument('output', help='输出PDF文件')
    extract_parser.add_argument('--start-label', type=int, required=True, help='开始标注页码')
    extract_parser.add_argument('--end-label', type=int, required=True, help='结束标注页码')
    extract_parser.add_argument('--language', default='chi_sim+eng', help='OCR语言 (默认: chi_sim+eng)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    processor = PDFOCRProcessor()
    
    try:
        if args.command == 'analyze':
            result = processor.analyze_pdf_structure(
                args.input,
                args.start,
                args.end,
                args.language
            )
            return 0 if result else 1
            
        elif args.command == 'extract':
            success = processor.extract_by_labeled_pages(
                args.input,
                args.start_label,
                args.end_label,
                args.output,
                args.language
            )
            return 0 if success else 1
            
    except KeyboardInterrupt:
        print("\n⏹ 用户中断")
        processor.cleanup()
        return 1
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        processor.cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main())
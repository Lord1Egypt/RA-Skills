#!/usr/bin/env python3
"""
Word转PDF工具
将Word文档转换为PDF文件，保留格式和布局
"""

import sys
import os
import argparse
from pathlib import Path

try:
    from docx2pdf import convert
    DOCX2PDF_AVAILABLE = True
except ImportError:
    DOCX2PDF_AVAILABLE = False
    print("警告: docx2pdf 库未安装，尝试使用其他方法")

try:
    import comtypes.client
    COMTYPES_AVAILABLE = True
except ImportError:
    COMTYPES_AVAILABLE = False

try:
    from win32com import client as win32client
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False

class WordToPDFConverter:
    def __init__(self):
        self.word_path = None
        self.pdf_path = None
        
    def check_dependencies(self):
        """检查依赖库"""
        if not DOCX2PDF_AVAILABLE and not COMTYPES_AVAILABLE and not WIN32COM_AVAILABLE:
            print("错误: 需要安装转换库")
            print("推荐安装: pip install docx2pdf")
            print("或者安装: pip install comtypes (Windows)")
            print("或者安装: pip install pywin32 (Windows)")
            return False
        return True
    
    def validate_word_file(self, word_path):
        """验证Word文件"""
        if not os.path.exists(word_path):
            raise FileNotFoundError(f"Word文件不存在: {word_path}")
        
        valid_extensions = ['.docx', '.doc']
        file_ext = os.path.splitext(word_path)[1].lower()
        
        if file_ext not in valid_extensions:
            raise ValueError(f"文件格式不支持: {word_path}，请提供.docx或.doc文件")
        
        # 检查文件大小
        file_size = os.path.getsize(word_path)
        if file_size == 0:
            raise ValueError("Word文件为空")
        
        return True
    
    def convert_using_docx2pdf(self, word_path, pdf_path):
        """使用docx2pdf库转换"""
        try:
            print("使用 docx2pdf 库进行转换...")
            convert(word_path, pdf_path)
            return True
        except Exception as e:
            print(f"docx2pdf转换失败: {str(e)}")
            return False
    
    def convert_using_comtypes(self, word_path, pdf_path):
        """使用comtypes库转换（Windows）"""
        try:
            print("使用 comtypes 库进行转换...")
            
            # 创建Word应用
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            
            try:
                # 打开文档
                doc = word.Documents.Open(os.path.abspath(word_path))
                
                # 保存为PDF
                doc.SaveAs(
                    os.path.abspath(pdf_path),
                    FileFormat=17  # PDF格式
                )
                
                # 关闭文档
                doc.Close()
                return True
                
            finally:
                # 退出Word应用
                word.Quit()
                
        except Exception as e:
            print(f"comtypes转换失败: {str(e)}")
            return False
    
    def convert_using_win32com(self, word_path, pdf_path):
        """使用win32com库转换（Windows）"""
        try:
            print("使用 win32com 库进行转换...")
            
            # 创建Word应用
            word = win32client.Dispatch('Word.Application')
            word.Visible = False
            
            try:
                # 打开文档
                doc = word.Documents.Open(os.path.abspath(word_path))
                
                # 保存为PDF
                doc.SaveAs(
                    os.path.abspath(pdf_path),
                    FileFormat=17  # PDF格式
                )
                
                # 关闭文档
                doc.Close()
                return True
                
            finally:
                # 退出Word应用
                word.Quit()
                
        except Exception as e:
            print(f"win32com转换失败: {str(e)}")
            return False
    
    def convert(self, word_path, pdf_path):
        """转换Word到PDF"""
        if not self.check_dependencies():
            return False
        
        self.word_path = word_path
        self.pdf_path = pdf_path
        
        try:
            # 验证Word文件
            self.validate_word_file(word_path)
            
            print(f"📝 输入Word: {word_path}")
            print(f"📄 输出PDF: {pdf_path}")
            
            # 检查文件信息
            file_size = os.path.getsize(word_path)
            print(f"📦 输入文件大小: {file_size / 1024:.2f} KB")
            
            print("🔄 开始转换Word到PDF...")
            
            success = False
            
            # 尝试不同的转换方法
            if DOCX2PDF_AVAILABLE:
                success = self.convert_using_docx2pdf(word_path, pdf_path)
            
            if not success and COMTYPES_AVAILABLE:
                success = self.convert_using_comtypes(word_path, pdf_path)
            
            if not success and WIN32COM_AVAILABLE:
                success = self.convert_using_win32com(word_path, pdf_path)
            
            if not success:
                print("❌ 所有转换方法都失败了")
                return False
            
            print("✅ 转换完成!")
            
            # 验证输出文件
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
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

def batch_convert(input_dir, output_dir, pattern="*.docx"):
    """批量转换Word文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return False
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找Word文件
    word_files = list(input_path.glob(pattern))
    
    # 也查找.doc文件
    doc_files = list(input_path.glob("*.doc"))
    word_files.extend(doc_files)
    
    if not word_files:
        print(f"在 {input_dir} 中未找到Word文件")
        return False
    
    print(f"找到 {len(word_files)} 个Word文件")
    
    converter = WordToPDFConverter()
    success_count = 0
    fail_count = 0
    
    for word_file in word_files:
        print(f"\n处理文件: {word_file.name}")
        
        # 生成输出文件名
        pdf_file = output_path / f"{word_file.stem}.pdf"
        
        try:
            if converter.convert(str(word_file), str(pdf_file)):
                success_count += 1
                print(f"✅ 成功: {word_file.name} -> {pdf_file.name}")
            else:
                fail_count += 1
                print(f"❌ 失败: {word_file.name}")
                
        except Exception as e:
            fail_count += 1
            print(f"❌ 错误: {word_file.name} - {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"批量转换完成!")
    print(f"✅ 成功: {success_count} 个文件")
    print(f"❌ 失败: {fail_count} 个文件")
    print(f"📁 输出目录: {output_dir}")
    
    return success_count > 0

def main():
    parser = argparse.ArgumentParser(
        description='Word转PDF工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 单个文件转换
  %(prog)s input.docx output.pdf
  
  # 批量转换
  %(prog)s --batch ./docs ./pdfs
  
  # 转换所有.doc和.docx文件
  %(prog)s --batch ./docs ./pdfs --pattern "*.doc*"
        """
    )
    
    # 主要参数
    parser.add_argument('input', nargs='?', help='输入Word文件路径')
    parser.add_argument('output', nargs='?', help='输出PDF文件路径')
    
    # 批量处理选项
    parser.add_argument('--batch', action='store_true', help='批量转换模式')
    parser.add_argument('--input-dir', help='输入目录（批量模式）')
    parser.add_argument('--output-dir', help='输出目录（批量模式）')
    parser.add_argument('--pattern', default='*.docx', help='文件匹配模式（默认: *.docx）')
    
    args = parser.parse_args()
    
    # 检查依赖
    converter = WordToPDFConverter()
    if not converter.check_dependencies():
        return 1
    
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
    print("Word转PDF转换工具")
    print("=" * 50)
    
    # 执行转换
    success = converter.convert(args.input, args.output)
    
    print("=" * 50)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子书解析脚本
支持 EPUB 和 PDF 格式的电子书解析
输出结构化的 JSON 格式数据
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from ebooklib import epub
    from bs4 import BeautifulSoup
except ImportError:
    print("错误：缺少依赖库，请安装：pip install ebooklib beautifulsoup4", file=sys.stderr)
    sys.exit(1)

try:
    from pypdf import PdfReader
except ImportError:
    print("错误：缺少依赖库，请安装：pip install pypdf", file=sys.stderr)
    sys.exit(1)


class EbookParser:
    """电子书解析器基类"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
    
    def parse(self, chapter_numbers: Optional[List[int]] = None) -> Dict:
        """解析电子书，返回结构化数据"""
        raise NotImplementedError


class EpubParser(EbookParser):
    """EPUB格式解析器"""
    
    def parse(self, chapter_numbers: Optional[List[int]] = None) -> Dict:
        """解析EPUB文件"""
        try:
            book = epub.read_epub(str(self.file_path))
        except Exception as e:
            raise Exception(f"EPUB解析失败: {str(e)}")
        
        # 提取书籍元数据
        metadata = {
            "book_title": self._get_metadata(book, 'title') or self.file_path.stem,
            "author": self._get_metadata(book, 'creator') or "未知作者",
            "total_chapters": 0,
            "chapters": []
        }
        
        # 提取章节内容
        chapters = []
        chapter_idx = 1
        
        for item in book.get_items():
            if item.get_type() == 9:  # ITEM_DOCUMENT
                # 检查是否需要解析该章节
                if chapter_numbers and chapter_idx not in chapter_numbers:
                    chapter_idx += 1
                    continue
                
                # 解析HTML内容
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                
                # 提取章节标题
                title = self._extract_title(soup, chapter_idx)
                
                # 提取正文内容
                content = self._extract_content(soup)
                
                # 只保留有实际内容的章节
                if content.strip():
                    chapters.append({
                        "number": chapter_idx,
                        "title": title,
                        "content": content
                    })
                
                chapter_idx += 1
        
        metadata["total_chapters"] = len(chapters)
        metadata["chapters"] = chapters
        
        return metadata
    
    def _get_metadata(self, book, field: str) -> Optional[str]:
        """提取元数据"""
        try:
            metadata = book.get_metadata('DC', field)
            if metadata and len(metadata) > 0:
                return metadata[0][0]
        except:
            pass
        return None
    
    def _extract_title(self, soup, chapter_idx: int) -> str:
        """提取章节标题"""
        # 尝试从标题标签提取
        for tag in ['h1', 'h2', 'h3', 'h4']:
            title_tag = soup.find(tag)
            if title_tag:
                return title_tag.get_text().strip()
        
        # 如果没有标题标签，返回默认标题
        return f"第{chapter_idx}章"
    
    def _extract_content(self, soup) -> str:
        """提取正文内容"""
        # 移除脚本和样式标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 提取文本
        text = soup.get_text()
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text


class PdfParser(EbookParser):
    """PDF格式解析器"""
    
    def parse(self, chapter_numbers: Optional[List[int]] = None) -> Dict:
        """解析PDF文件"""
        try:
            reader = PdfReader(str(self.file_path))
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
        
        metadata = {
            "book_title": self._get_title(reader) or self.file_path.stem,
            "author": self._get_author(reader) or "未知作者",
            "total_chapters": 0,
            "chapters": []
        }
        
        # PDF按页处理，每页作为一个"章节"
        chapters = []
        total_pages = len(reader.pages)
        
        # 如果指定了章节编号，转换为页码范围
        if chapter_numbers:
            page_indices = [pn - 1 for pn in chapter_numbers if 0 < pn <= total_pages]
        else:
            page_indices = range(total_pages)
        
        for page_num in page_indices:
            page = reader.pages[page_num]
            content = page.extract_text()
            
            if content and content.strip():
                chapters.append({
                    "number": page_num + 1,
                    "title": f"第{page_num + 1}页",
                    "content": content.strip()
                })
        
        metadata["total_chapters"] = len(chapters)
        metadata["chapters"] = chapters
        
        return metadata
    
    def _get_title(self, reader) -> Optional[str]:
        """提取PDF标题"""
        try:
            if reader.metadata and reader.metadata.title:
                return reader.metadata.title
        except:
            pass
        return None
    
    def _get_author(self, reader) -> Optional[str]:
        """提取PDF作者"""
        try:
            if reader.metadata and reader.metadata.author:
                return reader.metadata.author
        except:
            pass
        return None


def detect_format(file_path: str) -> str:
    """检测电子书格式"""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.epub':
        return 'epub'
    elif ext == '.pdf':
        return 'pdf'
    else:
        raise ValueError(f"不支持的文件格式: {ext}，仅支持 .epub 和 .pdf 格式")


def parse_ebook(input_path: str, chapter_numbers: Optional[List[int]] = None) -> Dict:
    """解析电子书主函数"""
    # 检测格式
    format_type = detect_format(input_path)
    
    # 选择解析器
    if format_type == 'epub':
        parser = EpubParser(input_path)
    elif format_type == 'pdf':
        parser = PdfParser(input_path)
    else:
        raise ValueError(f"不支持的格式: {format_type}")
    
    # 执行解析
    return parser.parse(chapter_numbers)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='电子书解析工具 - 支持EPUB和PDF格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 解析整本书
  python ebook_parser.py --input book.epub
  
  # 解析指定章节
  python ebook_parser.py --input book.epub --chapter 1 2 3
  
  # 输出到文件
  python ebook_parser.py --input book.epub --output result.json
        '''
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='电子书文件路径（支持.epub和.pdf格式）'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='输出JSON文件路径（默认输出到标准输出）'
    )
    
    parser.add_argument(
        '--chapter', '-c',
        type=int,
        nargs='+',
        help='指定要解析的章节编号（可指定多个，如：--chapter 1 2 3）'
    )
    
    args = parser.parse_args()
    
    try:
        # 解析电子书
        result = parse_ebook(args.input, args.chapter)
        
        # 输出结果
        json_output = json.dumps(result, ensure_ascii=False, indent=2)
        
        if args.output:
            # 写入文件
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"解析完成，结果已保存到: {args.output}", file=sys.stderr)
        else:
            # 输出到标准输出
            print(json_output)
            
    except FileNotFoundError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"解析失败: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

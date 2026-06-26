#!/usr/bin/env python3
"""
PDF书籍解析脚本
功能：提取PDF书籍的章节结构和页面内容，输出JSON格式
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print(json.dumps({"status": "error", "message": "请安装 pdfplumber: pip install pdfplumber==0.10.3"}))
    sys.exit(1)


def extract_text_with_layout(pdf_path: str) -> list:
    """提取PDF文本，保持布局信息"""
    pages = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_data = {
                "page_number": i + 1,
                "text": page.extract_text() or "",
                "width": page.width,
                "height": page.height
            }
            
            # 提取表格（如果有）
            tables = page.extract_tables()
            if tables:
                page_data["tables"] = [
                    [cell for cell in row if cell] 
                    for table in tables 
                    for row in table
                ]
            
            pages.append(page_data)
    
    return pages


def detect_chapters(pages: list) -> list:
    """基于文本特征识别章节结构"""
    chapters = []
    current_chapter = None
    
    # 常见的中英文章节标题模式
    chapter_patterns = [
        r'^第[一二三四五六七八九十百千万\d]+[章节篇部]',
        r'^(Chapter|Section|Part)\s+\d+',
        r'^\d+\.\s+[A-Z]',  # 1. Title
        r'^\d+\.\d+\s+',    # 1.1 Title
    ]
    
    for page in pages:
        lines = page["text"].split('\n')
        for line in lines[:5]:  # 检查前5行（章节标题通常在顶部）
            line = line.strip()
            if not line:
                continue
                
            # 检测是否为章节标题
            is_chapter = False
            for pattern in chapter_patterns:
                import re
                if re.match(pattern, line):
                    is_chapter = True
                    break
            
            if is_chapter:
                if current_chapter:
                    current_chapter["end_page"] = page["page_number"]
                    chapters.append(current_chapter)
                
                current_chapter = {
                    "title": line,
                    "start_page": page["page_number"],
                    "end_page": page["page_number"],
                    "key_content": []
                }
                break
    
    # 添加最后一个章节
    if current_chapter:
        current_chapter["end_page"] = pages[-1]["page_number"]
        chapters.append(current_chapter)
    
    return chapters


def extract_key_content(text: str, max_length: int = 5000) -> str:
    """提取关键内容（前N个字符）"""
    if len(text) <= max_length:
        return text
    
    # 尽量在句子边界截断
    truncated = text[:max_length]
    last_period = truncated.rfind('。')
    last_newline = truncated.rfind('\n')
    
    cutoff = max(last_period, last_newline)
    if cutoff > max_length * 0.7:
        return truncated[:cutoff + 1]
    
    return truncated + "..."


def parse_pdf(pdf_path: str, output_path: str = None) -> dict:
    """主解析函数"""
    result = {
        "status": "success",
        "file": pdf_path,
        "pages": [],
        "chapters": [],
        "total_pages": 0
    }
    
    try:
        # 提取所有页面内容
        pages = extract_text_with_layout(pdf_path)
        result["pages"] = pages
        result["total_pages"] = len(pages)
        
        # 检测章节结构
        chapters = detect_chapters(pages)
        result["chapters"] = chapters
        
        # 生成章节摘要（包含关键内容）
        for i, chapter in enumerate(chapters):
            start_page = chapter["start_page"] - 1
            end_page = chapter["end_page"]
            
            chapter_text = ""
            for page in pages[start_page:end_page]:
                chapter_text += page["text"] + "\n"
            
            result["chapters"][i]["summary"] = extract_key_content(chapter_text)
            result["chapters"][i]["word_count"] = len(chapter_text)
        
        # 输出到文件或stdout
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result
        
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)
        return result


def main():
    parser = argparse.ArgumentParser(description='PDF书籍解析工具')
    parser.add_argument('--input', '-i', required=True, help='输入PDF文件路径')
    parser.add_argument('--output', '-o', help='输出JSON文件路径（可选）')
    
    args = parser.parse_args()
    
    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({
            "status": "error",
            "message": f"文件不存在: {args.input}"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 执行解析
    result = parse_pdf(str(input_path), args.output)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

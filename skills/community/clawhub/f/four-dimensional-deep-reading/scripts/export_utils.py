#!/usr/bin/env python3
"""
export_utils.py - Four-Dimensional Deep Reading Export Utilities
Version: 1.0.0

支持导出格式：
- Anki闪卡 (CSV格式)
- Obsidian Markdown (双链结构)
- Notion Blocks (JSON格式)

Usage:
    from export_utils import export_to_anki, export_to_obsidian, export_to_notion
    
    # Anki导出
    export_to_anki(analysis_report, "output.csv", deck_name="阅读笔记")
    
    # Obsidian导出
    export_to_obsidian(analysis_report, vault_path="~/Obsidian/Vault")
    
    # Notion导出
    export_to_notion(analysis_report, notion_api_key, database_id)
"""

import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class FlashCard:
    """Anki闪卡数据结构"""
    front: str  # 正面（问题/提示）
    back: str   # 背面（答案）
    tags: List[str] = field(default_factory=list)
    
    def to_anki_row(self) -> List[str]:
        """转换为Anki CSV格式"""
        return [self.front, self.back, " ".join(self.tags)]


@dataclass
class ObsidianNote:
    """Obsidian笔记数据结构"""
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)  # 双向链接


class AnalysisReportParser:
    """分析报告解析器 - 从4视角报告提取可导出内容"""
    
    def __init__(self, report_content: str, book_title: str, language: str = "zh"):
        self.content = report_content
        self.book_title = book_title
        self.language = language
        
    def extract_lms_content(self) -> Dict:
        """提取LMS架构师内容 - 核心方法论来源"""
        pattern = r'##\s*Method\s*\(.*?\)(.*?)(?=##\s*Summary|##\s*[^\s]+|$)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        method_content = match.group(1).strip() if match else ""
        
        pattern = r'##\s*Summary\s*\(.*?\)(.*?)(?=##|\Z)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        summary_content = match.group(1).strip() if match else ""
        
        pattern = r'##\s*Logic\s*\(.*?\)(.*?)(?=##\s*Method|##\s*[^\s]+|$)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        logic_content = match.group(1).strip() if match else ""
        
        return {
            "method": method_content,
            "summary": self._clean_markdown(summary_content),
            "logic": logic_content
        }
    
    def extract_axiom_content(self) -> Dict:
        """提取第一性原理师内容"""
        pattern = r'##\s*Core\s+Premises(.*?)(?=##\s*Underlying|##\s*[^\s]+|$)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        premises = match.group(1).strip() if match else ""
        
        pattern = r'##\s*One-Sentence\s+Summary(.*?)(?=##|\Z)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        one_sentence = match.group(1).strip() if match else ""
        
        return {
            "premises": premises,
            "one_sentence": self._clean_markdown(one_sentence)
        }
    
    def extract_swan_content(self) -> Dict:
        """提取黑天鹅猎手内容"""
        pattern = r'##\s*Boundary\s+Conditions(.*?)(?=##|\Z)'
        match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
        boundary = match.group(1).strip() if match else ""
        
        return {
            "boundary": boundary
        }
    
    def _clean_markdown(self, text: str) -> str:
        """清理Markdown格式"""
        # 移除标题标记
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        # 移除加粗标记
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # 移除链接
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # 清理多余空白
        text = re.sub(r'\n{3,}', '\n', text)
        return text.strip()
    
    def generate_flashcards(self) -> List[FlashCard]:
        """从报告生成Anki闪卡"""
        cards = []
        tags = [self._sanitize_filename(self.book_title), "4d-reading"]
        
        # 从LMS提取方法论卡
        lms = self.extract_lms_content()
        if lms["method"]:
            cards.append(FlashCard(
                front=f"【{self.book_title}】核心方法论是什么？",
                back=lms["method"][:500],  # 限制长度
                tags=tags + ["method"]
            ))
        
        if lms["summary"]:
            cards.append(FlashCard(
                front=f"【{self.book_title}】一句话总结",
                back=lms["summary"],
                tags=tags + ["summary"]
            ))
            
        # 从Axiom提取前提卡
        axiom = self.extract_axiom_content()
        if axiom["premises"]:
            # 提取每个前提作为独立闪卡
            lines = axiom["premises"].split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('-'):
                        line = line[1:].strip()
                    if line and len(line) > 5:
                        cards.append(FlashCard(
                            front=f"【{self.book_title}】核心前提",
                            back=line,
                            tags=tags + ["premise"]
                        ))
        
        if axiom["one_sentence"]:
            cards.append(FlashCard(
                front=f"【{self.book_title}】一句话概括",
                back=axiom["one_sentence"],
                tags=tags + ["core"]
            ))
        
        # 从Black Swan提取边界条件卡
        swan = self.extract_swan_content()
        if swan["boundary"]:
            lines = swan["boundary"].split('\n')
            for line in lines:
                line = line.strip()
                if '|' in line and '条件' in line:
                    continue  # 跳过表头
                if line and not line.startswith('#') and not line.startswith('|'):
                    cards.append(FlashCard(
                        front=f"【{self.book_title}】边界条件",
                        back=line[:300],
                        tags=tags + ["boundary"]
                    ))
        
        return cards
    
    def _sanitize_filename(self, name: str) -> str:
        """清理文件名特殊字符"""
        return re.sub(r'[^\w\u4e00-\u9fff]', '_', name)[:50]


# ==================== Anki Export ====================

def export_to_anki(cards: List[FlashCard], output_path: str, deck_name: str = "4D-Reading") -> Dict[str, Any]:
    """
    导出为Anki可导入的CSV文件
    
    Args:
        cards: 闪卡列表
        output_path: 输出文件路径
        deck_name: 卡组名称
        
    Returns:
        {"success": bool, "cards_count": int, "path": str}
    """
    output_path = os.path.expanduser(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Anki CSV格式: Front, Back, Tags
    with open(output_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['front', 'back', 'tags'])  # 表头
        for card in cards:
            writer.writerow(card.to_anki_row())
    
    return {
        "success": True,
        "cards_count": len(cards),
        "path": output_path,
        "deck_name": deck_name,
        "import_instructions": f"导入Anki: 文件 → 导入 → 选择 {output_path}"
    }


# ==================== Obsidian Export ====================

def export_to_obsidian(report_content: str, book_title: str, vault_path: str, 
                       language: str = "zh") -> Dict[str, Any]:
    """
    导出为Obsidian Markdown格式
    
    Args:
        report_content: 分析报告内容
        book_title: 书名
        vault_path: Obsidian库路径
        language: 语言
        
    Returns:
        {"success": bool, "files_created": list}
    """
    vault_path = os.path.expanduser(vault_path)
    
    parser = AnalysisReportParser(report_content, book_title, language)
    books_dir = os.path.join(vault_path, "4D-Reading", parser._sanitize_filename(book_title))
    os.makedirs(books_dir, exist_ok=True)
    files_created = []
    
    # 1. 主笔记文件
    main_note = f"""---
title: {book_title} - 四维深度阅读
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [4d-reading, book-notes, {parser._sanitize_filename(book_title)}]
---

# {book_title}

> 四维深度阅读分析报告
> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

{report_content}

---

*由 Four-Dimensional Deep Reading 技能生成*
"""
    
    main_path = os.path.join(books_dir, f"{parser._sanitize_filename(book_title)}.md")
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main_note)
    files_created.append(main_path)
    
    # 2. 闪卡文件 (用于Obsidian插件)
    cards = parser.generate_flashcards()
    if cards:
        cards_note = f"""---
title: {book_title} - 闪卡
tags: [anki, flashcards, {parser._sanitize_filename(book_title)}]
---

# {book_title} 闪卡

"""
        for i, card in enumerate(cards, 1):
            cards_note += f"""## 卡片 {i}

**Q:** {card.front}

**A:** {card.back}

---

"""
        cards_path = os.path.join(books_dir, "flashcards.md")
        with open(cards_path, 'w', encoding='utf-8') as f:
            f.write(cards_note)
        files_created.append(cards_path)
    
    # 3. 方法论提取文件
    lms = parser.extract_lms_content()
    if lms["method"]:
        method_note = f"""---
title: {book_title} - 核心方法论
tags: [methodology, {parser._sanitize_filename(book_title)}]
---

# {book_title} - 核心方法论

{lms['method']}

## 一句话总结
{lms['summary']}

"""
        method_path = os.path.join(books_dir, "methodology.md")
        with open(method_path, 'w', encoding='utf-8') as f:
            f.write(method_note)
        files_created.append(method_path)
    
    return {
        "success": True,
        "files_created": files_created,
        "vault_path": vault_path
    }


# ==================== Notion Export ====================

def export_to_notion(report_content: str, book_title: str, 
                     notion_api_key: str, database_id: str,
                     language: str = "zh") -> Dict[str, Any]:
    """
    导出到Notion数据库
    
    Args:
        report_content: 分析报告内容
        book_title: 书名
        notion_api_key: Notion API密钥
        database_id: Notion数据库ID
        language: 语言
        
    Returns:
        {"success": bool, "page_id": str, "blocks": list}
    """
    try:
        from notion_client import Client
    except ImportError:
        return {
            "success": False,
            "error": "请安装notion-client: pip install notion-client"
        }
    
    client = Client(auth=notion_api_key)
    parser = AnalysisReportParser(report_content, book_title, language)
    
    # 创建页面
    page_id = client.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": book_title}}]},
            "Tags": {"multi_select": [{"name": "4D-Reading"}, {"name": "book-notes"}]},
            "Date": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}},
        }
    ).get("id")
    
    # 添加内容块
    blocks = []
    
    # 标题块
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "📚 四维深度阅读分析报告"}}]
        }
    })
    
    # 分割报告为适当大小的块
    report_lines = report_content.split('\n')
    current_paragraph = []
    current_heading = ""
    
    for line in report_lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测标题
        if line.startswith('## '):
            # 保存之前的段落
            if current_paragraph:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": '\n'.join(current_paragraph)}}]}
                })
                current_paragraph = []
            
            heading_text = line[3:]
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": heading_text}}]}
            })
        elif line.startswith('# '):
            continue  # 跳过主标题
        else:
            current_paragraph.append(line)
    
    # 保存最后的段落
    if current_paragraph:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": '\n'.join(current_paragraph)}}]}
        })
    
    # 批量添加块 (每次最多100个)
    for i in range(0, len(blocks), 100):
        client.blocks.children.append(page_id, blocks[i:i+100])
    
    # 添加闪卡数据库块
    cards = parser.generate_flashcards()
    if cards:
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🎴 生成的闪卡"}}]}
        })
        
        for card in cards[:20]:  # 限制数量
            blocks.append({
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"type": "text", "text": {"content": card.front}}],
                    "children": [{
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"type": "text", "text": {"content": card.back}}]}
                    }]
                }
            })
        
        client.blocks.children.append(page_id, blocks[len(blocks)-len(cards[:20])-1:])
    
    return {
        "success": True,
        "page_id": page_id,
        "cards_count": len(cards),
        "blocks_count": len(blocks),
        "notion_url": f"https://notion.so/{page_id.replace('-', '')}"
    }


# ==================== 一键导出 ====================

def export_all(report_content: str, book_title: str, 
               output_dir: str = "~/Documents/4D-Reading",
               vault_path: Optional[str] = None,
               notion_key: Optional[str] = None,
               notion_db: Optional[str] = None,
               language: str = "zh") -> Dict[str, Any]:
    """
    一键导出到所有支持的格式
    
    Args:
        report_content: 分析报告内容
        book_title: 书名
        output_dir: 输出目录
        vault_path: Obsidian库路径 (可选)
        notion_key: Notion API密钥 (可选)
        notion_db: Notion数据库ID (可选)
        language: 语言
        
    Returns:
        {"anki": dict, "obsidian": dict, "notion": dict}
    """
    parser = AnalysisReportParser(report_content, book_title, language)
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "anki": None,
        "obsidian": None,
        "notion": None,
        "book_title": book_title,
        "timestamp": datetime.now().isoformat()
    }
    
    # 1. Anki导出
    anki_path = os.path.join(output_dir, f"{parser._sanitize_filename(book_title)}_anki.csv")
    cards = parser.generate_flashcards()
    if cards:
        results["anki"] = export_to_anki(cards, anki_path, deck_name=book_title)
    
    # 2. Obsidian导出
    if vault_path:
        results["obsidian"] = export_to_obsidian(report_content, book_title, vault_path, language)
    
    # 3. Notion导出
    if notion_key and notion_db:
        results["notion"] = export_to_notion(report_content, book_title, notion_key, notion_db, language)
    
    return results


# ==================== CLI Entry ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python export_utils.py anki <report_file> <output_csv>")
        print("  python export_utils.py obsidian <report_file> <vault_path>")
        print("  python export_utils.py all <report_file> <output_dir> [--vault <path>]")
        sys.exit(1)
    
    mode = sys.argv[1]
    report_file = sys.argv[2]
    
    # 读取报告
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 提取书名 (从第一行标题)
    book_title = "Unknown Book"
    if report_content:
        match = re.search(r'^#\s+(.+)$', report_content, re.MULTILINE)
        if match:
            book_title = match.group(1).strip()
    
    if mode == "anki":
        output_path = sys.argv[3] if len(sys.argv) > 3 else "output.csv"
        parser = AnalysisReportParser(report_content, book_title)
        cards = parser.generate_flashcards()
        result = export_to_anki(cards, output_path)
        print(f"✓ Anki导出成功: {result['cards_count']} 张闪卡 → {output_path}")
        
    elif mode == "obsidian":
        vault_path = sys.argv[3] if len(sys.argv) > 3 else "~/Obsidian/Vault"
        result = export_to_obsidian(report_content, book_title, vault_path)
        print(f"✓ Obsidian导出成功: {len(result['files_created'])} 个文件")
        
    elif mode == "all":
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "~/Documents/4D-Reading"
        result = export_all(report_content, book_title, output_dir)
        print(f"✓ 一键导出完成:")
        if result["anki"]:
            print(f"  - Anki: {result['anki']['cards_count']} 张闪卡")
        if result["obsidian"]:
            print(f"  - Obsidian: {len(result['obsidian']['files_created'])} 个文件")
        if result["notion"]:
            print(f"  - Notion: {result['notion']['notion_url']}")
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
#!/usr/bin/env python3
"""
文档解析器：提取文章主题、关键词、现有引用和搜索建议
支持格式：Markdown / LaTeX / Word (.docx)
"""

import re
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Set, Optional


class DocumentParser:
    """通用文档解析基类"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.file_type = ""
        
    def parse(self) -> Dict:
        """解析文档并返回结构化信息"""
        raise NotImplementedError
    
    def extract_keywords(self, text: str, top_k: int = 7) -> List[str]:
        """提取关键词（基于学术术语模式）"""
        # 学术术语模式：驼峰命名、连字符连接、特定后缀
        patterns = [
            # 驼峰命名（如 GraphNeuralNetwork）
            r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',
            # 连字符连接（如 graph-neural-network）
            r'\b[a-z]+(?:-[a-z]+){1,3}\b',
            # 常见学术术语
            r'\b(?:neural|network|learning|model|algorithm|optimization|prediction|forecasting|classification|regression|clustering|embedding|attention|transformer|bert|gpt|cnn|rnn|lstm|gru|gan|vae|gnn|gnn|graph|temporal|spatial|multivariate|univariate|series|time)\b',
            # 大写缩写（2-5个字母）
            r'\b[A-Z]{2,5}\b',
        ]
        
        keywords = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.extend([m.lower() if m.isupper() else m for m in matches])
        
        # 统计频率并去重
        from collections import Counter
        keyword_counts = Counter(keywords)
        
        # 过滤停用词
        stopwords = {'the', 'and', 'for', 'with', 'via', 'using', 'based', 'from', 
                     'this', 'that', 'such', 'also', 'more', 'than', 'only', 
                     'even', 'both', 'each', 'all', 'any', 'can', 'may', 'use',
                     'one', 'two', 'new', 'first', 'second', 'third', 'et', 'al'}
        
        filtered = [(k, v) for k, v in keyword_counts.items() 
                   if k.lower() not in stopwords and len(k) > 2]
        
        # 返回 top_k 个关键词
        return [k for k, _ in sorted(filtered, key=lambda x: x[1], reverse=True)[:top_k]]
    
    def generate_search_queries(self, keywords: List[str], context: str) -> List[str]:
        """基于关键词和上下文生成搜索 query"""
        queries = []
        
        if len(keywords) >= 2:
            # Query 1: 主要方法
            queries.append(f"{keywords[0]} {keywords[1]}")
            
            # Query 2: 方法 + 应用场景
            if len(keywords) >= 3:
                queries.append(f"{keywords[0]} {keywords[2]} prediction")
            
            # Query 3: 扩展同义词
            synonyms = self._expand_synonyms(keywords[:2])
            if synonyms:
                queries.append(f"{synonyms[0]} {synonyms[1] if len(synonyms) > 1 else keywords[1]}")
        
        # 确保至少有 2 个 query
        if len(queries) < 2:
            queries.append(" ".join(keywords[:3]) if len(keywords) >= 3 else " ".join(keywords))
        
        return queries[:4]
    
    def _expand_synonyms(self, terms: List[str]) -> List[str]:
        """扩展学术术语同义词"""
        synonym_map = {
            'gnn': ['graph neural network', 'graph convolutional network', 'gcn'],
            'graphneuralnetwork': ['gnn', 'graph convolutional network'],
            'graph-neural-network': ['gnn', 'gcn'],
            'transformer': ['attention mechanism', 'self-attention', 'bert', 'gpt'],
            'deep-learning': ['neural network', 'deep neural network', 'dnn'],
            'deeplearning': ['deep learning', 'neural network'],
            'time-series': ['temporal data', 'sequential data', 'time series forecasting'],
            'timeseries': ['time series', 'temporal prediction'],
            'multivariate': ['multi-variable', 'multi-variate'],
        }
        
        expanded = []
        for term in terms:
            term_lower = term.lower()
            if term_lower in synonym_map:
                expanded.extend(synonym_map[term_lower][:1])
            else:
                expanded.append(term)
        
        return expanded


class MarkdownParser(DocumentParser):
    """Markdown 文档解析器"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_type = "markdown"
    
    def parse(self) -> Dict:
        """解析 Markdown 文档"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        return {
            "file_type": self.file_type,
            "title": self._extract_title(),
            "abstract": self._extract_abstract(),
            "sections": self._extract_sections(),
            "keywords": self.extract_keywords(self.content),
            "existing_citations": self._extract_citations(),
            "content_preview": self._get_preview(),
            "suggested_queries": self.generate_search_queries(
                self.extract_keywords(self.content), 
                self.content
            )
        }
    
    def _extract_title(self) -> str:
        """提取标题（第一个 # 标题）"""
        match = re.search(r'^#\s+(.+)$', self.content, re.MULTILINE)
        return match.group(1).strip() if match else ""
    
    def _extract_abstract(self) -> str:
        """提取摘要"""
        # 寻找 Abstract 或 摘要 部分
        patterns = [
            r'##?\s*(?:Abstract|摘要)\s*\n\n?(.+?)(?=\n##|\Z)',
            r'(?:^|\n)([^#\n].{100,500}?)(?=\n##|\n\n##|\Z)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()[:500]
        return ""
    
    def _extract_sections(self) -> List[str]:
        """提取章节标题"""
        sections = re.findall(r'^##?\s+(.+)$', self.content, re.MULTILINE)
        return [s.strip() for s in sections[:10]]
    
    def _extract_citations(self) -> List[str]:
        """提取已有引用"""
        citations = []
        
        # arXiv ID 模式
        arxiv_matches = re.findall(r'arxiv[:/](\d{4}\.\d{4,5})', self.content, re.IGNORECASE)
        citations.extend([f"arxiv:{m}" for m in arxiv_matches])
        
        # DOI 模式
        doi_matches = re.findall(r'10\.\d{4,}/[^\s\]]+', self.content)
        citations.extend([f"doi:{m}" for m in doi_matches])
        
        # 引用标记模式 [1], [2], etc.
        ref_matches = re.findall(r'\[(\d+)\]', self.content)
        
        return list(set(citations))
    
    def _get_preview(self) -> str:
        """获取内容预览"""
        # 移除 markdown 标记，保留纯文本
        text = re.sub(r'!?\[([^\]]*)\]\([^\)]+\)', r'\1', self.content)  # 移除链接和图片
        text = re.sub(r'[#*_`]', '', text)  # 移除格式标记
        text = re.sub(r'\n+', ' ', text)  # 合并换行
        return text[:800]


class LaTeXParser(DocumentParser):
    """LaTeX 文档解析器"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_type = "latex"
    
    def parse(self) -> Dict:
        """解析 LaTeX 文档"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        return {
            "file_type": self.file_type,
            "title": self._extract_title(),
            "abstract": self._extract_abstract(),
            "sections": self._extract_sections(),
            "keywords": self._extract_keywords_latex() or self.extract_keywords(self.content),
            "existing_citations": self._extract_citations(),
            "bibliography_files": self._extract_bib_files(),
            "content_preview": self._get_preview(),
            "suggested_queries": self.generate_search_queries(
                self.extract_keywords(self.content),
                self.content
            )
        }
    
    def _extract_title(self) -> str:
        """提取标题"""
        match = re.search(r'\\title\{([^}]+)\}', self.content)
        return match.group(1).strip() if match else ""
    
    def _extract_abstract(self) -> str:
        """提取摘要"""
        match = re.search(r'\\begin\{abstract\}(.+?)\\end\{abstract\}', 
                         self.content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip()[:500] if match else ""
    
    def _extract_sections(self) -> List[str]:
        """提取章节"""
        sections = re.findall(r'\\section\{([^}]+)\}', self.content)
        return sections[:10]
    
    def _extract_keywords_latex(self) -> List[str]:
        """提取 LaTeX 关键词"""
        match = re.search(r'\\keywords\{([^}]+)\}', self.content, re.IGNORECASE)
        if match:
            return [k.strip() for k in match.group(1).split(',')]
        return []
    
    def _extract_citations(self) -> List[str]:
        """提取引用标记"""
        # \cite{key1,key2}
        cites = re.findall(r'\\cite[pt]?\{([^}]+)\}', self.content)
        all_cites = []
        for cite_group in cites:
            all_cites.extend([c.strip() for c in cite_group.split(',')])
        return list(set(all_cites))
    
    def _extract_bib_files(self) -> List[str]:
        """提取引用的 .bib 文件"""
        matches = re.findall(r'\\bibliography\{([^}]+)\}', self.content)
        return [m.strip() for m in matches]
    
    def _get_preview(self) -> str:
        """获取纯文本预览"""
        # 移除 LaTeX 命令
        text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?', ' ', self.content)
        text = re.sub(r'%.*?\n', ' ', text)  # 移除注释
        text = re.sub(r'\s+', ' ', text)  # 合并空白
        return text[:800]


class WordParser(DocumentParser):
    """Word 文档解析器（.docx）"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_type = "word"
    
    def parse(self) -> Dict:
        """解析 Word 文档"""
        try:
            from docx import Document
        except ImportError:
            return {
                "file_type": self.file_type,
                "error": "python-docx not installed. Run: pip install python-docx",
                "content_preview": ""
            }
        
        doc = Document(self.file_path)
        full_text = []
        sections = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                full_text.append(text)
                # 检测标题（简单启发式：短段落且以大写字母开头）
                if len(text) < 100 and text[0].isupper() and not text[-1] in '.!?':
                    sections.append(text)
        
        content = '\n'.join(full_text)
        
        return {
            "file_type": self.file_type,
            "title": full_text[0] if full_text else "",
            "abstract": self._extract_abstract_word(full_text),
            "sections": sections[:10],
            "keywords": self.extract_keywords(content),
            "existing_citations": [],  # Word 中难以自动提取
            "content_preview": content[:800],
            "suggested_queries": self.generate_search_queries(
                self.extract_keywords(content),
                content
            )
        }
    
    def _extract_abstract_word(self, paragraphs: List[str]) -> str:
        """从 Word 段落中提取摘要"""
        # 寻找 "Abstract" 或 "摘要" 后面的段落
        for i, para in enumerate(paragraphs):
            if re.match(r'^(Abstract|摘要)\s*$', para, re.IGNORECASE):
                if i + 1 < len(paragraphs):
                    return paragraphs[i + 1][:500]
        
        # 如果没有明确标记，返回前几个段落中较长的一个
        for para in paragraphs[1:5]:
            if 100 < len(para) < 500:
                return para
        return ""


def detect_file_type(file_path: str) -> str:
    """检测文件类型"""
    ext = Path(file_path).suffix.lower()
    if ext == '.md':
        return 'markdown'
    elif ext in ['.tex', '.latex']:
        return 'latex'
    elif ext == '.docx':
        return 'word'
    else:
        # 尝试根据内容检测
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)
            if content.startswith('%') or '\\documentclass' in content:
                return 'latex'
            elif '# ' in content or content.startswith('#'):
                return 'markdown'
        return 'unknown'


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python parse_document.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(json.dumps({"error": f"File not found: {file_path}"}))
        sys.exit(1)
    
    # 检测文件类型并选择解析器
    file_type = detect_file_type(file_path)
    
    parser_map = {
        'markdown': MarkdownParser,
        'latex': LaTeXParser,
        'word': WordParser,
    }
    
    parser_class = parser_map.get(file_type)
    if not parser_class:
        print(json.dumps({"error": f"Unsupported file type: {file_type}"}))
        sys.exit(1)
    
    # 解析文档
    parser = parser_class(file_path)
    result = parser.parse()
    
    # 添加文件路径
    result["file_path"] = file_path
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

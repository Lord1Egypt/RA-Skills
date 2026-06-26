#!/usr/bin/env python3
"""
Doc Genius - 智能文档处理助手（优化版 v1.2.0）
支持PDF/Word/Markdown智能摘要、格式转换、批量处理
优化：TextRank算法、降级策略、错误处理
"""
import sys
import os
import json
import argparse
import re
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
import concurrent.futures
from dataclasses import dataclass, asdict
import requests
from collections import defaultdict
import math

# 本地依赖
try:
    import PyPDF2
    from docx import Document
    import markdown
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请安装: pip install PyPDF2 python-docx markdown beautifulsoup4")
    sys.exit(1)

# 可选：OpenAI API
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ═══════════════════════════════════════════════════
# TextRank 算法实现
# ═══════════════════════════════════════════════════

class TextRankSummarizer:
    """TextRank 摘要算法"""
    
    def __init__(self, damping: float = 0.85, max_iter: int = 100, tol: float = 1e-4):
        """
        初始化TextRank
        
        Args:
            damping: 阻尼系数（通常0.85）
            max_iter: 最大迭代次数
            tol: 收敛阈值
        """
        self.damping = damping
        self.max_iter = max_iter
        self.tol = tol
    
    def split_sentences(self, text: str) -> List[str]:
        """
        智能分句（支持中英文）
        
        改进点：
        - 处理中文标点（。！？）
        - 处理英文标点（.!?）
        - 过滤太短的句子
        - 去除重复
        """
        # 中文分句
        sentences = re.split(r'[。！？\n]', text)
        
        # 英文分句
        english_sentences = []
        for s in sentences:
            english_sentences.extend(re.split(r'(?<=[.!?])\s+', s))
        
        # 清理和过滤
        cleaned = []
        for s in english_sentences:
            s = s.strip()
            # 过滤条件：长度>10，不为纯数字/符号
            if len(s) > 10 and not re.match(r'^[\d\s\W]+$', s):
                if s not in cleaned:  # 去重
                    cleaned.append(s)
        
        return cleaned
    
    def sentence_similarity(self, s1: str, s2: str) -> float:
        """
        计算两个句子的相似度（基于词重叠）
        
        改进点：
        - 使用词集合而非词频
        - 归一化处理
        """
        # 分词（简单空格分词，中文按字符）
        words1 = set(self._tokenize(s1))
        words2 = set(self._tokenize(s2))
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _tokenize(self, text: str) -> List[str]:
        """分词（简化版，支持中英文）"""
        # 英文：按空格分
        tokens = text.lower().split()
        
        # 中文：按字符分（简单处理）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        for chars in chinese_chars:
            tokens.extend(list(chars))
        
        # 过滤停用词和标点
        stop_words = {'的', '是', '在', '和', '了', 'the', 'a', 'an', 'is', 'are', 'was', 'were'}
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
        
        return tokens
    
    def build_similarity_matrix(self, sentences: List[str]) -> List[List[float]]:
        """构建句子相似度矩阵"""
        n = len(sentences)
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.sentence_similarity(sentences[i], sentences[j])
                matrix[i][j] = sim
                matrix[j][i] = sim
        
        return matrix
    
    def pagerank(self, matrix: List[List[float]]) -> List[float]:
        """PageRank算法"""
        n = len(matrix)
        if n == 0:
            return []
        
        # 初始化得分
        scores = [1.0 / n] * n
        
        # 计算每行的和（用于归一化）
        row_sums = [sum(row) for row in matrix]
        
        # 迭代计算
        for _ in range(self.max_iter):
            new_scores = []
            for i in range(n):
                rank_sum = 0.0
                for j in range(n):
                    if i != j and row_sums[j] > 0:
                        rank_sum += matrix[j][i] / row_sums[j] * scores[j]
                
                new_rank = (1 - self.damping) + self.damping * rank_sum
                new_scores.append(new_rank)
            
            # 检查收敛
            diff = sum(abs(new_scores[i] - scores[i]) for i in range(n))
            scores = new_scores
            
            if diff < self.tol:
                break
        
        return scores
    
    def summarize(self, text: str, num_sentences: int = 5) -> str:
        """
        生成摘要
        
        Args:
            text: 原文
            num_sentences: 摘要句子数
        """
        # 分句
        sentences = self.split_sentences(text)
        
        if len(sentences) <= num_sentences:
            return '。'.join(sentences)
        
        # 构建相似度矩阵
        matrix = self.build_similarity_matrix(sentences)
        
        # 计算TextRank得分
        scores = self.pagerank(matrix)
        
        # 选择得分最高的句子
        ranked_sentences = sorted(
            zip(sentences, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 取前N句
        top_sentences = [s[0] for s in ranked_sentences[:num_sentences]]
        
        # 按原文顺序排列
        ordered_summary = []
        for sentence in sentences:
            if sentence in top_sentences:
                ordered_summary.append(sentence)
        
        return '。'.join(ordered_summary[:num_sentences])


# ═══════════════════════════════════════════════════
# 关键词提取器（TF-IDF简化版）
# ═══════════════════════════════════════════════════

class KeywordExtractor:
    """关键词提取器"""
    
    def __init__(self):
        self.stop_words = {
            # 中文停用词
            '的', '是', '在', '和', '了', '有', '我', '他', '她', '它',
            '这', '那', '就', '也', '都', '而', '及', '与', '或', '但',
            # 英文停用词
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below'
        }
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        提取关键词（TF-IDF简化版）
        
        改进点：
        - 使用TF（词频）
        - 过滤停用词
        - 过滤数字和标点
        - 过滤太短的词
        """
        # 分词
        words = self._tokenize(text)
        
        # 统计词频
        word_freq = defaultdict(int)
        for word in words:
            if self._is_valid_keyword(word):
                word_freq[word] += 1
        
        # 按词频排序
        sorted_words = sorted(
            word_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 返回前N个关键词
        return [word for word, freq in sorted_words[:num_keywords]]
    
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        # 英文
        tokens = text.lower().split()
        
        # 中文（按字符）
        chinese = re.findall(r'[\u4e00-\u9fff]+', text)
        for chars in chinese:
            # 中文按2-4字切分（简单处理）
            tokens.extend([chars[i:i+2] for i in range(len(chars)-1)])
        
        return tokens
    
    def _is_valid_keyword(self, word: str) -> bool:
        """判断是否为有效关键词"""
        # 长度检查
        if len(word) < 2:
            return False
        
        # 停用词检查
        if word in self.stop_words:
            return False
        
        # 纯数字检查
        if word.isdigit():
            return False
        
        # 纯标点检查
        if re.match(r'^[\W_]+$', word):
            return False
        
        return True


# ═══════════════════════════════════════════════════
# 文档处理器（优化版）
# ═══════════════════════════════════════════════════

@dataclass
class DocumentInfo:
    """文档信息"""
    file: str
    type: str
    summary: str
    keywords: List[str]
    word_count: int
    pages: Optional[int] = None
    error: Optional[str] = None
    method: Optional[str] = None  # 新增：摘要方法（ai/textrank/fallback）


class DocumentProcessorV2:
    """文档处理器 v2.0（优化版）"""
    
    def __init__(self, method: str = "auto", model: str = "gpt-3.5-turbo"):
        """
        初始化
        
        Args:
            method: 摘要方法（auto/ai/textrank/fallback）
            model: AI模型
        """
        self.method = method
        self.model = model
        
        # 初始化组件
        self.textrank = TextRankSummarizer()
        self.keyword_extractor = KeywordExtractor()
        
        # 检查OpenAI
        self.openai_available = OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY")
        
        if method == "ai" and not self.openai_available:
            print("⚠️ OpenAI不可用，自动切换到TextRank模式")
            self.method = "textrank"
    
    # ═══════════════════════════════════════════════════
    # 文本提取（保持不变）
    # ═══════════════════════════════════════════════════
    
    def extract_text_pdf(self, file_path: Path) -> Tuple[str, int]:
        """从PDF提取文本"""
        text = []
        pages = 0
        
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = len(reader.pages)
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"PDF提取失败: {e}")
        
        return '\n'.join(text), pages
    
    def extract_text_docx(self, file_path: Path) -> str:
        """从Word提取文本"""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n'.join(paragraphs)
        except Exception as e:
            raise Exception(f"Word提取失败: {e}")
    
    def extract_text_markdown(self, file_path: Path) -> str:
        """从Markdown提取文本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        except Exception as e:
            raise Exception(f"Markdown提取失败: {e}")
    
    def extract_text(self, file_path: Path) -> Tuple[str, str, Optional[int]]:
        """自动识别格式并提取文本"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            text, pages = self.extract_text_pdf(file_path)
            return text, 'pdf', pages
        elif suffix in ['.docx', '.doc']:
            text = self.extract_text_docx(file_path)
            return text, 'word', None
        elif suffix in ['.md', '.markdown']:
            text = self.extract_text_markdown(file_path)
            return text, 'markdown', None
        elif suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, 'text', None
        else:
            raise ValueError(f"不支持的格式: {suffix}")
    
    # ═══════════════════════════════════════════════════
    # 摘要生成（优化版，带降级策略）
    # ═══════════════════════════════════════════════════
    
    def summarize_ai(self, text: str, max_words: int = 200) -> Tuple[str, str]:
        """
        AI摘要（OpenAI API）
        
        Returns:
            (摘要, 方法名)
        """
        if not self.openai_available:
            raise Exception("OpenAI不可用")
        
        try:
            client = openai.OpenAI()
            
            # 限制输入长度
            if len(text) > 10000:
                text = text[:10000] + "..."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的文档摘要助手。请用简洁、准确的语言总结文档的核心内容。"
                    },
                    {
                        "role": "user",
                        "content": f"请用{max_words}字以内总结以下文档：\n\n{text}"
                    }
                ],
                max_tokens=max_words * 2,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip(), "ai"
        except Exception as e:
            raise Exception(f"AI摘要失败: {e}")
    
    def summarize_textrank(self, text: str, num_sentences: int = 5) -> Tuple[str, str]:
        """
        TextRank摘要
        
        Returns:
            (摘要, 方法名)
        """
        try:
            summary = self.textrank.summarize(text, num_sentences)
            return summary, "textrank"
        except Exception as e:
            raise Exception(f"TextRank摘要失败: {e}")
    
    def summarize_fallback(self, text: str, num_sentences: int = 5) -> Tuple[str, str]:
        """
        降级摘要（抽取前N句）
        
        Returns:
            (摘要, 方法名)
        """
        try:
            sentences = self.textrank.split_sentences(text)
            selected = sentences[:num_sentences]
            return '。'.join(selected), "fallback"
        except Exception as e:
            # 最后的降级：返回原文前200字
            return text[:200] + "..." if len(text) > 200 else text, "emergency"
    
    def summarize_with_fallback(self, text: str, method: str = "auto") -> Tuple[str, str]:
        """
        智能摘要（带降级策略）
        
        降级链：AI → TextRank → Fallback → Emergency
        
        Returns:
            (摘要, 使用的方法)
        """
        # 如果指定了方法
        if method == "ai":
            return self.summarize_ai(text)
        elif method == "textrank":
            return self.summarize_textrank(text)
        elif method == "fallback":
            return self.summarize_fallback(text)
        
        # 自动模式：按降级链尝试
        # 1. 尝试AI
        if self.method in ["auto", "ai"] and self.openai_available:
            try:
                return self.summarize_ai(text)
            except Exception as e:
                print(f"⚠️ AI摘要失败，降级到TextRank: {e}")
        
        # 2. 尝试TextRank
        if self.method in ["auto", "textrank"]:
            try:
                return self.summarize_textrank(text)
            except Exception as e:
                print(f"⚠️ TextRank摘要失败，降级到Fallback: {e}")
        
        # 3. 降级到抽取式
        return self.summarize_fallback(text)
    
    # ═══════════════════════════════════════════════════
    # 主接口
    # ═══════════════════════════════════════════════════
    
    def summarize(self, file_path: Path, output_format: str = "json") -> Dict[str, Any]:
        """
        智能摘要（优化版）
        """
        # 提取文本
        text, doc_type, pages = self.extract_text(file_path)
        
        # 生成摘要（带降级）
        summary, method = self.summarize_with_fallback(text, self.method)
        
        # 提取关键词
        keywords = self.keyword_extractor.extract_keywords(text)
        
        # 统计字数
        word_count = len(text.split())
        
        # 构造结果
        result = DocumentInfo(
            file=str(file_path.name),
            type=doc_type,
            summary=summary,
            keywords=keywords,
            word_count=word_count,
            pages=pages,
            method=method
        )
        
        if output_format == "json":
            return asdict(result)
        else:
            return self._format_as_text(result)
    
    def _format_as_text(self, doc_info: DocumentInfo) -> str:
        """格式化为文本"""
        text = f"""文件: {doc_info.file}
类型: {doc_info.type}
字数: {doc_info.word_count}
摘要方法: {doc_info.method}
"""
        if doc_info.pages:
            text += f"页数: {doc_info.pages}\n"
        
        text += f"""
摘要:
{doc_info.summary}

关键词: {', '.join(doc_info.keywords)}
"""
        return text


# ═══════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='Doc Genius v1.2.0 - 智能文档处理助手（优化版）')
    
    parser.add_argument('command', choices=['summarize', 'test'], help='命令')
    parser.add_argument('file', type=Path, nargs='?', help='文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--method', choices=['auto', 'ai', 'textrank', 'fallback'], default='auto', help='摘要方法')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='AI模型')
    
    args = parser.parse_args()
    
    # 测试模式
    if args.command == 'test':
        print("🧪 测试TextRank算法...")
        test_text = """
        这是一个测试文档。TextRank是一种用于文本摘要的算法。
        它基于PageRank算法，通过计算句子之间的相似度来选择重要句子。
        TextRank不需要训练数据，是一种无监督学习方法。
        这个算法在多个任务上表现良好，包括文本摘要和关键词提取。
        """
        
        summarizer = TextRankSummarizer()
        summary = summarizer.summarize(test_text, 2)
        print(f"摘要: {summary}")
        
        extractor = KeywordExtractor()
        keywords = extractor.extract_keywords(test_text, 5)
        print(f"关键词: {keywords}")
        
        return
    
    # 摘要模式
    if args.command == 'summarize':
        if not args.file:
            print("❌ 错误: 请指定文件路径")
            sys.exit(1)
        
        if not args.file.exists():
            print(f"❌ 错误: 文件不存在 - {args.file}")
            sys.exit(1)
        
        print(f"📄 正在处理文档: {args.file.name}")
        
        try:
            processor = DocumentProcessorV2(method=args.method, model=args.model)
            result = processor.summarize(args.file, args.format)
            
            print("\n" + "="*60)
            
            if args.format == 'json':
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result)
            
            print("="*60)
            print("\n✅ 处理完成！")
        
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()

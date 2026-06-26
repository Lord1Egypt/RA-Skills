#!/usr/bin/env python3
"""
pdf_parser.py - 多策略PDF解析器（带质量评分）
自动选择最优解析策略
"""

import re
from pathlib import Path
from typing import Dict, Any, Tuple


class PDFParser:
    """多策略PDF解析器"""
    
    def __init__(self, text: str):
        self.raw_text = text
        self.quality_score = 0.0
    
    def parse(self) -> Dict[str, Any]:
        """
        执行多策略解析，返回清洗后文本 + 质量分
        
        Returns:
            {
                "text": 清洗后的文本,
                "quality_score": 0-1之间的质量分,
                "strategy": 使用的策略名称
            }
        """
        # 策略1: 规则清洗（快速）
        cleaned_text = self._rule_clean()
        score = self._evaluate_quality(cleaned_text)
        
        if score >= 0.7:
            return {
                "text": cleaned_text,
                "quality_score": score,
                "strategy": "rule_based"
            }
        
        # 策略2: 深度清洗（慢但更彻底）
        deep_cleaned = self._deep_clean(cleaned_text)
        deep_score = self._evaluate_quality(deep_cleaned)
        
        if deep_score >= 0.6:
            return {
                "text": deep_cleaned,
                "quality_score": deep_score,
                "strategy": "deep_clean"
            }
        
        # 回退: 返回原始文本 + 低分
        return {
            "text": self.raw_text,
            "quality_score": max(0.3, score),
            "strategy": "fallback"
        }
    
    def _rule_clean(self) -> str:
        """
        规则清洗：快速修复常见PDF问题
        """
        text = self.raw_text
        
        # 1. 修复常见粘连词
        replacements = [
            (r'ATTENTIONRESIDUALS', 'ATTENTION RESIDUALS'),
            (r'TECHNICALREPORT', 'TECHNICAL REPORT'),
            (r'ABSTRACT\s*\n([A-Z])', r'ABSTRACT\n\1'),  # ABSTRACT后换行
            (r'KimiTeam', 'Kimi Team'),
            (r'MoonshotAI', 'Moonshot AI'),
            (r'PreNorm', 'Pre-Norm'),
            (r'LLMs', 'LLMs'),  # 保留LLMs不拆分
            (r'BlockAttnRes', 'Block AttnRes'),
            (r'FullAttnRes', 'Full AttnRes'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        
        # 2. 修复引用标记粘连: [12]with → [12] with
        text = re.sub(r'(\[\d+\])([a-zA-Z])', r'\1 \2', text)
        
        # 3. 修复单词粘连（保留常见缩写）
        # 小写+大写边界加空格（排除常见缩写）
        text = re.sub(
            r'(?<![\bLL|\bAI|\bML|\bDL|\bRL|\bNLP|\bCV])([a-z])([A-Z])',
            r'\1 \2',
            text
        )
        
        # 4. 清理PDF特殊字符
        text = re.sub(r'\(cid:\d+\)', '', text)
        text = re.sub(r'\x00', '', text)
        
        # 5. 修复连字符断行
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        
        # 6. 合并过短行（非句子结尾）
        lines = text.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                cleaned_lines.append('')
                continue
            
            # 短行且非句子结尾，合并到上一行
            if (len(line) < 50 and 
                i > 0 and 
                cleaned_lines and
                not re.search(r'[.!?:;]$', cleaned_lines[-1]) and
                not line.startswith('Figure') and
                not line.startswith('Table')):
                cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _deep_clean(self, text: str) -> str:
        """深度清洗：更激进的修复"""
        # 1. 识别并保护数学表达式
        math_expressions = []
        def protect_math(match):
            math_expressions.append(match.group(0))
            return f"MATH_PLACEHOLDER_{len(math_expressions)-1}"
        
        # 保护 O(Ld), α_i 等数学符号
        text = re.sub(r'O\([^)]+\)', protect_math, text)
        text = re.sub(r'[αβγδεζηθ]_[a-z0-9]', protect_math, text)
        
        # 2. 更激进的空格修复
        text = re.sub(r'([a-z])([A-Z])(?![a-z])', r'\1 \2', text)
        
        # 3. 修复章节标题格式
        text = re.sub(r'^(\d+)\s+([A-Z])', r'\1. \2', text, flags=re.MULTILINE)
        
        # 4. 恢复数学表达式
        for i, expr in enumerate(math_expressions):
            text = text.replace(f"MATH_PLACEHOLDER_{i}", expr)
        
        return text
    
    def _evaluate_quality(self, text: str) -> float:
        """
        评估清洗后文本质量（0-1）
        
        评分维度:
        1. 粘连词比例（40%）
        2. 句子完整性（30%）
        3. 可读性（30%）
        """
        if not text or len(text) < 100:
            return 0.0
        
        score = 0.0
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # 1. 粘连词检测（40%）
        # 检测小写+大写模式（排除常见缩写）
        adhesion_patterns = [
            r'(?<!^)(?<![\s\[])\b[a-z]+[A-Z][a-z]+\b',  # 小写开头的大写词
            r'[a-z][A-Z](?![a-z])',  # 单字母边界
        ]
        adhesion_count = sum(len(re.findall(p, text)) for p in adhesion_patterns)
        adhesion_ratio = adhesion_count / total_words
        score += max(0, 1 - adhesion_ratio * 5) * 0.4  # 5%容忍度
        
        # 2. 句子完整性（30%）
        sentences = re.split(r'[.!?]+', text)
        valid_sentences = [s for s in sentences if len(s.strip()) > 10]
        if len(sentences) > 0:
            sentence_ratio = len(valid_sentences) / len(sentences)
            score += sentence_ratio * 0.3
        
        # 3. 可读性（30%）
        # 检测异常长词（可能是粘连）
        long_words = [w for w in words if len(w) > 25]
        long_word_ratio = len(long_words) / total_words
        score += max(0, 1 - long_word_ratio * 10) * 0.3
        
        return min(1.0, score)
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        提取论文主要章节
        
        Returns:
            {
                "abstract": 摘要文本,
                "introduction": 引言文本,
                ...
            }
        """
        sections = {}
        
        # 提取摘要
        abstract_match = re.search(
            r'ABSTRACT\s*\n(.*?)(?:\n\n|\n\d+\s+\w|\Z)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        if abstract_match:
            sections["abstract"] = abstract_match.group(1).strip()
        
        # 提取引言
        intro_match = re.search(
            r'1\.?\s+Introduction\s*\n(.*?)(?:\n\n\d+\.?\s+\w|\Z)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        if intro_match:
            sections["introduction"] = intro_match.group(1).strip()
        
        return sections


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="多策略PDF解析器")
    parser.add_argument("input", help="输入文本文件或PDF文件")
    parser.add_argument("--output", "-o", help="输出清洗后的文本文件")
    
    args = parser.parse_args()
    
    # 读取输入
    input_path = Path(args.input)
    if input_path.suffix == '.pdf':
        # 需要pdfplumber提取文本
        try:
            import pdfplumber
            with pdfplumber.open(input_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages[:20])
        except ImportError:
            print("❌ pdfplumber未安装，请运行: pip install pdfplumber")
            return 1
    else:
        text = input_path.read_text(encoding='utf-8')
    
    # 解析
    parser = PDFParser(text)
    result = parser.parse()
    
    # 输出
    print(f"📊 质量评分: {result['quality_score']:.2f}/1.0")
    print(f"🔧 使用策略: {result['strategy']}")
    
    if args.output:
        Path(args.output).write_text(result["text"], encoding='utf-8')
        print(f"✅ 已保存: {args.output}")
    
    return 0


if __name__ == "__main__":
    exit(main())

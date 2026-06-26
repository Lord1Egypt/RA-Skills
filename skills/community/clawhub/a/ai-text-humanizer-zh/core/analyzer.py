#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI text detection engine using rule-based analysis.

Optimized version with unified regex scanning to avoid O(N*M) complexity.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

from .utils import (
    get_sentences, word_count, clean_text,
    count_em_dashes, count_curly_quotes,
    count_exclamation, count_question
)
from .rules import RuleSet, load_rules_with_user


@dataclass
class SentenceReport:
    """单个句子的检测结果"""
    sentence: str
    score: int = 0
    reasons: List[str] = field(default_factory=list)
    ai_jargon_cnt: int = 0
    puffery_cnt: int = 0
    marketing_cnt: int = 0
    vague_cnt: int = 0
    hedging_cnt: int = 0
    chatbot_cnt: int = 0
    citation_cnt: int = 0
    cutoff_cnt: int = 0
    markdown_cnt: int = 0
    negative_parallel_cnt: int = 0
    superficial_verb_cnt: int = 0
    filler_cnt: int = 0
    rule_of_three_cnt: int = 0
    sentence_starter_cnt: int = 0
    rhetorical_cnt: int = 0
    list_marker_cnt: int = 0


@dataclass
class DetectionReport:
    """完整检测报告"""
    total_issues: int = 0
    word_count: int = 0
    char_count: int = 0
    ai_probability: float = 0.0
    ai_level: str = "low"
    sentence_reports: List[SentenceReport] = field(default_factory=list)
    ai_jargon_count: int = 0
    puffery_count: int = 0
    marketing_count: int = 0
    vague_count: int = 0
    hedging_count: int = 0
    chatbot_count: int = 0
    citation_count: int = 0
    cutoff_count: int = 0
    markdown_count: int = 0
    negative_parallel_count: int = 0
    superficial_verb_count: int = 0
    filler_count: int = 0
    rule_of_three_count: int = 0
    sentence_starter_count: int = 0
    rhetorical_count: int = 0
    list_marker_count: int = 0
    em_dash_count: int = 0
    curly_quote_count: int = 0
    exclamation_count: int = 0
    question_count: int = 0


class AIDetector:
    """AI文本检测器 - 优化版，使用统一正则一次扫描"""
    
    # 类别名称到属性名的映射
    CATEGORY_ATTR_MAP = {
        'ai_jargon': 'ai_jargon_cnt',
        'puffery': 'puffery_cnt',
        'marketing': 'marketing_cnt',
        'vague': 'vague_cnt',
        'hedging': 'hedging_cnt',
        'chatbot': 'chatbot_cnt',
        'citation': 'citation_cnt',
        'cutoff': 'cutoff_cnt',
        'markdown': 'markdown_cnt',
        'negative_parallel': 'negative_parallel_cnt',
        'superficial_verb': 'superficial_verb_cnt',
        'filler': 'filler_cnt',
        'rule_of_three': 'rule_of_three_cnt',
        'list_marker': 'list_marker_cnt',
    }
    
    # 类别权重
    CATEGORY_WEIGHTS = {
        'ai_jargon': 1,
        'puffery': 2,
        'marketing': 2,
        'vague': 1,
        'hedging': 1,
        'chatbot': 3,
        'citation': 5,
        'cutoff': 3,
        'markdown': 2,
        'negative_parallel': 1,
        'superficial_verb': 1,
        'filler': 1,
        'rule_of_three': 2,
        'list_marker': 1,
    }
    
    def __init__(self, rules: Optional[RuleSet] = None, user_rules_path: Optional[str] = None):
        if rules is None:
            rules = load_rules_with_user(user_rules_path)
        self.rules = rules
        self._compiled_sentence_patterns = self._compile_sentence_patterns()
        self._compiled_rhetorical_patterns = self._compile_patterns(self.rules.rhetorical_patterns)
        
        # 构建统一正则（会初始化 _word_to_category）
        self._word_to_category = {}
        self._unified_regex = self._build_unified_regex()
        self._sentence_starter_regex = self._build_sentence_starter_regex()
    
    def _compile_patterns(self, patterns: List[str]) -> List[re.Pattern]:
        """编译正则模式列表"""
        compiled = []
        for p in patterns:
            try:
                compiled.append(re.compile(p, re.IGNORECASE))
            except re.error:
                continue
        return compiled
    
    def _compile_sentence_patterns(self) -> List[re.Pattern]:
        """编译句子级模式"""
        compiled = []
        for item in self.rules.sentence_patterns:
            pattern_str = item.get("pattern", "")
            if pattern_str:
                try:
                    compiled.append(re.compile(pattern_str, re.IGNORECASE))
                except re.error:
                    continue
        return compiled
    
    def _build_unified_regex(self) -> Optional[re.Pattern]:
        """构建统一正则表达式，一次扫描所有类别
        
        使用非命名组 + 匹配后检查内容的方式，避免组名冲突问题
        """
        # 收集所有词汇及其类别
        self._word_to_category = {}  # word.lower() -> category
        all_words = []
        
        categories = [
            ('ai_jargon', self.rules.ai_jargon),
            ('puffery', self.rules.puffery_phrases),
            ('marketing', self.rules.marketing_speak),
            ('vague', self.rules.vague_attributions),
            ('hedging', self.rules.hedging_phrases),
            ('chatbot', self.rules.chatbot_artifacts),
            ('citation', self.rules.citation_bugs),
            ('cutoff', self.rules.knowledge_cutoff),
            ('markdown', self.rules.markdown_artifacts),
            ('negative_parallel', self.rules.negative_parallelisms),
            ('superficial_verb', self.rules.superficial_verbs),
            ('filler', self.rules.filler_phrases),
            ('rule_of_three', self.rules.rule_of_three_patterns),
            ('list_marker', self.rules.list_markers),
        ]
        
        for cat_name, words in categories:
            if not words:
                continue
            for w in words:
                if w:
                    w_lower = w.lower()
                    # 如果同一个词出现在多个类别，保留第一个
                    if w_lower not in self._word_to_category:
                        self._word_to_category[w_lower] = cat_name
                        all_words.append(w)
        
        if not all_words:
            return None
        
        # 按长度降序排序，确保长词优先匹配
        all_words.sort(key=len, reverse=True)
        
        # 构建非命名组正则
        parts = [re.escape(w) for w in all_words]
        return re.compile('|'.join(parts), re.IGNORECASE)
    
    def _safe_group_name(self, text: str) -> str:
        """将文本转换为安全的正则组名"""
        # 只保留字母数字和下划线
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()[:8]
    
    def _build_sentence_starter_regex(self) -> Optional[re.Pattern]:
        """构建句首连接词正则"""
        starters = self.rules.sentence_starters
        if not starters:
            return None
        
        # 按长度降序排序，优先匹配更长的
        starters_sorted = sorted(set(starters), key=len, reverse=True)
        pattern = '|'.join(re.escape(s) for s in starters_sorted)
        # 匹配句首（行首或句号后）
        return re.compile(rf'(?:^|[。！？\n])\s*({pattern})', re.IGNORECASE)
    
    def detect(self, text: str) -> DetectionReport:
        """检测文本中的AI特征，返回详细报告 - 优化版"""
        text = clean_text(text)
        sentences = get_sentences(text)
        word_cnt = word_count(text)
        
        report = DetectionReport(
            word_count=word_cnt,
            char_count=len(text.replace(' ', '').replace('\n', ''))
        )
        
        # 计算每个句子的起始位置
        sentence_positions = self._get_sentence_positions(text, sentences)
        
        # 一次扫描获取所有匹配
        all_matches = self._find_all_matches(text)
        
        # 将匹配分配到各句子
        sentence_matches = self._assign_matches_to_sentences(
            all_matches, sentence_positions, len(sentences)
        )
        
        # 分析每个句子
        for i, sent in enumerate(sentences):
            sent_report = self._analyze_sentence_fast(
                sent, sentence_matches.get(i, [])
            )
            report.sentence_reports.append(sent_report)
            report.total_issues += sent_report.score
            report.ai_jargon_count += sent_report.ai_jargon_cnt
            report.puffery_count += sent_report.puffery_cnt
            report.marketing_count += sent_report.marketing_cnt
            report.vague_count += sent_report.vague_cnt
            report.hedging_count += sent_report.hedging_cnt
            report.chatbot_count += sent_report.chatbot_cnt
            report.citation_count += sent_report.citation_cnt
            report.cutoff_count += sent_report.cutoff_cnt
            report.markdown_count += sent_report.markdown_cnt
            report.negative_parallel_count += sent_report.negative_parallel_cnt
            report.superficial_verb_count += sent_report.superficial_verb_cnt
            report.filler_count += sent_report.filler_cnt
            report.rule_of_three_count += sent_report.rule_of_three_cnt
            report.sentence_starter_count += sent_report.sentence_starter_cnt
            report.rhetorical_count += sent_report.rhetorical_cnt
            report.list_marker_count += sent_report.list_marker_cnt
        
        # 全局特征
        report.em_dash_count = count_em_dashes(text)
        report.curly_quote_count = count_curly_quotes(text)
        report.exclamation_count = count_exclamation(text)
        report.question_count = count_question(text)
        
        if report.em_dash_count > self.rules.punctuation.get("em_dash_threshold", 3):
            report.total_issues += report.em_dash_count
        report.total_issues += report.curly_quote_count * self.rules.punctuation.get("curly_quote_weight", 1)
        if report.exclamation_count > self.rules.punctuation.get("exclamation_threshold", 2):
            report.total_issues += report.exclamation_count
        if report.question_count > self.rules.punctuation.get("question_mark_threshold", 3):
            report.total_issues += report.question_count
        
        # 计算AI概率
        max_possible = max(1, word_cnt * 0.5)
        prob = min(100, (report.total_issues / max_possible) * 100)
        report.ai_probability = round(prob, 1)
        
        # 判定等级
        if report.citation_count > 0 or report.chatbot_count > 0:
            report.ai_level = "very high"
        elif report.total_issues > 30 or report.ai_probability > 70:
            report.ai_level = "high"
        elif report.total_issues > 15 or report.ai_probability > 40:
            report.ai_level = "medium"
        else:
            report.ai_level = "low"
        
        return report
    
    def _get_sentence_positions(self, text: str, sentences: List[str]) -> List[Tuple[int, int]]:
        """获取每个句子在原文中的位置范围"""
        positions = []
        search_start = 0
        
        for sent in sentences:
            # 在原文中找到句子的位置
            idx = text.find(sent, search_start)
            if idx >= 0:
                positions.append((idx, idx + len(sent)))
                search_start = idx + 1
            else:
                # 如果找不到，使用上一个位置或0
                if positions:
                    positions.append((positions[-1][1], positions[-1][1] + len(sent)))
                else:
                    positions.append((0, len(sent)))
        
        return positions
    
    def _find_all_matches(self, text: str) -> List[Tuple[int, int, str, str]]:
        """一次扫描文本，返回所有匹配
        
        Returns:
            List of (start, end, category, matched_text)
        """
        if not self._unified_regex:
            return []
        
        matches = []
        for m in self._unified_regex.finditer(text):
            matched_text = m.group(0)
            # 通过词汇查找类别
            cat = self._word_to_category.get(matched_text.lower(), 'unknown')
            matches.append((m.start(), m.end(), cat, matched_text))
        
        return matches
    
    def _assign_matches_to_sentences(
        self, 
        matches: List[Tuple[int, int, str, str]], 
        sentence_positions: List[Tuple[int, int]],
        num_sentences: int
    ) -> Dict[int, List[Tuple[str, str]]]:
        """将匹配结果分配到对应的句子
        
        Returns:
            Dict[sentence_index, List[(category, matched_text)]]
        """
        result = {}
        
        for start, end, cat, text in matches:
            # 二分查找找到匹配所在的句子
            sent_idx = self._find_sentence_index(start, sentence_positions)
            if sent_idx >= 0 and sent_idx < num_sentences:
                if sent_idx not in result:
                    result[sent_idx] = []
                result[sent_idx].append((cat, text))
        
        return result
    
    def _find_sentence_index(self, pos: int, positions: List[Tuple[int, int]]) -> int:
        """二分查找位置所在的句子索引"""
        left, right = 0, len(positions) - 1
        
        while left <= right:
            mid = (left + right) // 2
            start, end = positions[mid]
            
            if start <= pos < end:
                return mid
            elif pos < start:
                right = mid - 1
            else:
                left = mid + 1
        
        # 如果超出范围，返回最后一个句子
        if left >= len(positions):
            return len(positions) - 1
        return left
    
    def _analyze_sentence_fast(
        self, 
        sentence: str, 
        matches: List[Tuple[str, str]]
    ) -> SentenceReport:
        """快速分析单个句子（基于预计算的匹配结果）"""
        sr = SentenceReport(sentence=sentence)
        score = 0
        reasons = []
        
        # 统计各类别匹配
        cat_counts: Dict[str, int] = {}
        for cat, matched_text in matches:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
        # 应用权重并记录
        for cat, cnt in cat_counts.items():
            weight = self.CATEGORY_WEIGHTS.get(cat, 1)
            score += cnt * weight
            attr = self.CATEGORY_ATTR_MAP.get(cat)
            if attr:
                setattr(sr, attr, cnt)
            reasons.append(f"{cat}: {cnt}次")
        
        # 检查句首连接词
        if self._sentence_starter_regex:
            m = self._sentence_starter_regex.search(sentence)
            if m:
                score += 1
                sr.sentence_starter_cnt += 1
                reasons.append(f"sentence_starter: {m.group(1)}")
        
        # 检查反问句模式
        for pat in self._compiled_rhetorical_patterns:
            if pat.search(sentence):
                score += 1
                sr.rhetorical_cnt += 1
                reasons.append("rhetorical_pattern")
                break
        
        # 检查长句
        sent_len = len(sentence.replace(' ', ''))
        if sent_len > 40:
            score += 1
            reasons.append(f"long_sentence ({sent_len}字)")
        
        sr.score = score
        sr.reasons = reasons
        return sr

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI text rewriting engine.

Optimized version with unified replacement regex, sentence patterns,
and synonym replacement support.
"""

import re
import random
import json
from typing import List, Tuple, Dict, Optional
from pathlib import Path

from .rules import RuleSet, load_rules_with_user
from .utils import get_sentences, clean_text


class AIRewriter:
    """AI文本改写器 - 支持短语替换、句式改写、同义词替换"""
    
    def __init__(
        self, 
        rules: Optional[RuleSet] = None, 
        user_rules_path: Optional[str] = None,
        synonyms_path: Optional[str] = None
    ):
        """
        初始化改写器
        
        :param rules: 规则集，若为None则从默认路径加载
        :param user_rules_path: 用户自定义规则文件路径（JSON）
        :param synonyms_path: 同义词库文件路径（JSON）
        """
        if rules is None:
            rules = load_rules_with_user(user_rules_path)
        self.rules = rules
        
        # 构建统一替换正则
        self._repl_pattern, self._repl_map = self._build_unified_replacement()
        
        # 编译句子级改写模式（支持多模板）
        self._sentence_patterns = self._prepare_sentence_patterns()
        
        # 加载同义词库
        self.synonyms = self._load_synonyms(synonyms_path)
        self._synonym_pattern = self._build_synonym_pattern()
        
        # 术语白名单 - 不进行同义词替换
        self._term_whitelist = {
            '人工智能', '深度学习', '机器学习', '神经网络', '自然语言处理',
            '计算机视觉', '知识图谱', '大数据', '物联网', '云计算',
            '区块链', '边缘计算', '强化学习', '迁移学习', '联邦学习',
            '图像识别', '语音识别', '人脸识别', '指纹识别',
            '智能城市', '智慧城市', '智能交通', '智慧交通',
            '智能医疗', '智慧医疗', '智能教育', '智慧教育',
            '数据分析', '数据挖掘', '数据科学',
            '算法', '模型', '系统', '平台', '架构',
            'API', 'SDK', 'AI', 'ML', 'NLP', 'CV',
            '实时', '动态', '自动化', '智能化',
        }
        
        # 后处理配置
        self._post_cleanup = getattr(rules, 'data', {}).get('post_cleanup', {})
        
        # Chatbot结尾语
        self._chatbot_endings = [
            "希望这对您有帮助",
            "希望这对你有帮助",
            "希望对您有帮助",
            "希望对你有帮助",
            "希望以上信息对您有所启发",
            "希望以上信息对你有所启发",
            "希望以上分析对您有所启发",
            "希望以上分析对你有所启发",
            "欢迎随时交流",
            "请随时联系",
            "如果您有任何见解",
            "如果你有任何见解",
            "如果您有任何问题",
            "如果你有任何问题",
        ]
    
    def _build_unified_replacement(self) -> Tuple[Optional[re.Pattern], Dict[str, str]]:
        """构建统一替换正则，一次扫描所有替换"""
        replacements = self.rules.replacements
        if not replacements:
            return None, {}
        
        # 按长度降序排序，确保长模式优先匹配
        sorted_items = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        parts = []
        repl_map = {}
        
        for old, new in sorted_items:
            if old:
                parts.append(re.escape(old))
                repl_map[old.lower()] = new
        
        if not parts:
            return None, {}
        
        pattern = re.compile('|'.join(parts), re.IGNORECASE)
        return pattern, repl_map
    
    def _prepare_sentence_patterns(self) -> List[Tuple[re.Pattern, List[str]]]:
        """编译句子级改写模式，每个模式对应多个可能的改写模板"""
        patterns = []
        for item in self.rules.sentence_patterns:
            pattern_str = item.get("pattern", "")
            rewrites = item.get("rewrites", [])
            if pattern_str and rewrites:
                try:
                    pat = re.compile(pattern_str, re.IGNORECASE | re.DOTALL)
                    patterns.append((pat, rewrites))
                except re.error:
                    continue
        return patterns
    
    def _load_synonyms(self, synonyms_path: Optional[str] = None) -> Dict[str, List[str]]:
        """加载同义词库，支持用户自定义 JSON 文件"""
        if synonyms_path:
            with open(synonyms_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        default_path = Path(__file__).parent.parent / 'resources' / 'synonyms.json'
        if default_path.exists():
            with open(default_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _build_synonym_pattern(self) -> Optional[re.Pattern]:
        """构建同义词匹配正则"""
        if not self.synonyms:
            return None
        
        # 按长度降序排序，避免短词破坏长词
        keys = sorted(self.synonyms.keys(), key=len, reverse=True)
        if not keys:
            return None
        
        return re.compile('|'.join(re.escape(k) for k in keys))
    
    def rewrite(self, text: str, aggressive: bool = False) -> Tuple[str, List[str]]:
        """改写文本，返回 (改写后文本, 变更列表)"""
        changes = []
        text = clean_text(text)
        
        # 1. Markdown清理
        text, md_changes = self._clean_markdown(text)
        changes.extend(md_changes)
        
        # 2. Chatbot痕迹清理
        text, chat_changes = self._clean_chatbot_artifacts(text)
        changes.extend(chat_changes)
        
        # 3. 短语替换 - 使用统一正则
        if self._repl_pattern:
            text, count = self._apply_unified_replacement(text)
            if count > 0:
                changes.append(f"短语替换 ({count}处)")
        
        # 4. 句子级模式改写（随机选择模板）
        for pattern, rewrites in self._sentence_patterns:
            text, cnt = self._apply_sentence_pattern(text, pattern, rewrites)
            if cnt > 0:
                changes.append(f"句式改写 ({cnt}处)")
        
        # 5. 同义词替换（激进模式概率更高）
        if self._synonym_pattern and self.synonyms:
            prob = 0.4 if aggressive else 0.25
            text, count = self._replace_synonyms(text, prob)
            if count > 0:
                changes.append(f"同义词替换 ({count}处, 概率{prob:.0%})")
        
        # 6. 破折号处理
        old_dashes = text.count('——') + text.count('—')
        text = re.sub(r'——', '，', text)
        text = re.sub(r'—', '，', text)
        new_dashes = text.count('——') + text.count('—')
        if old_dashes > new_dashes:
            changes.append(f"替换破折号 ({old_dashes - new_dashes}处)")
        
        # 7. 长句拆分（激进模式）
        if aggressive:
            text, split_count = self._split_long_sentences(text)
            if split_count > 0:
                changes.append(f"拆分长句 ({split_count}处)")
        
        # 8. 后处理清理
        text = self._post_process(text)
        
        text = clean_text(text)
        return text, changes
    
    def _apply_unified_replacement(self, text: str) -> Tuple[str, int]:
        """应用统一替换正则"""
        total_count = 0
        
        def replacer(match):
            nonlocal total_count
            key = match.group(0).lower()
            replacement = self._repl_map.get(key, match.group(0))
            if replacement != match.group(0):
                total_count += 1
            return replacement
        
        text = self._repl_pattern.sub(replacer, text)
        return text, total_count
    
    def _apply_sentence_pattern(
        self, 
        text: str, 
        pattern: re.Pattern, 
        rewrites: List[str]
    ) -> Tuple[str, int]:
        """应用句子级正则改写，随机选择模板"""
        count = 0
        
        def replacer(match):
            nonlocal count
            template = random.choice(rewrites)
            result = match.expand(template)
            if result != match.group(0):
                count += 1
            return result
        
        text, cnt = pattern.subn(replacer, text)
        return text, cnt
    
    def _replace_synonyms(self, text: str, probability: float = 0.3) -> Tuple[str, int]:
        """随机替换文本中的高频词"""
        if not self._synonym_pattern or not self.synonyms:
            return text, 0
        
        count = 0
        
        def replacer(match):
            nonlocal count
            word = match.group(0)
            
            # 白名单术语不替换
            if word in self._term_whitelist:
                return word
            
            # 按概率决定是否替换
            if random.random() > probability:
                return word
            
            candidates = self.synonyms.get(word, [])
            
            # 过滤掉与原文相同的词和白名单术语
            candidates = [c for c in candidates if c != word and c not in self._term_whitelist]
            
            if not candidates:
                return word
            
            count += 1
            return random.choice(candidates)
        
        text = self._synonym_pattern.sub(replacer, text)
        return text, count
    
    def _clean_markdown(self, text: str) -> Tuple[str, List[str]]:
        """清理Markdown格式 - 使用非贪婪匹配避免回溯"""
        changes = []
        
        # 移除粗体标记
        count = 0
        while '**' in text:
            new_text = re.sub(r'\*\*([^*]+?)\*\*', r'\1', text)
            if new_text == text:
                break
            count += 1
            text = new_text
        if count > 0:
            changes.append(f"移除粗体标记 ({count}处)")
        
        # 移除标题标记
        headings = len(re.findall(r'^#{1,6}\s+', text, re.MULTILINE))
        if headings > 0:
            text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
            changes.append(f"移除标题标记 ({headings}处)")
        
        # 移除代码块
        code_blocks = len(re.findall(r'```.*?```', text, re.DOTALL))
        if code_blocks > 0:
            text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
            changes.append(f"移除代码块 ({code_blocks}处)")
        
        # 移除行内代码
        inline_code = len(re.findall(r'`[^`]+?`', text))
        if inline_code > 0:
            text = re.sub(r'`([^`]+?)`', r'\1', text)
            changes.append(f"移除行内代码 ({inline_code}处)")
        
        # 移除分隔线
        hr_count = len(re.findall(r'^[-*_]{3,}\s*$', text, re.MULTILINE))
        if hr_count > 0:
            text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
            changes.append(f"移除分隔线 ({hr_count}处)")
        
        return text, changes
    
    def _clean_chatbot_artifacts(self, text: str) -> Tuple[str, List[str]]:
        """清理聊天机器人痕迹"""
        changes = []
        
        for phrase in self._chatbot_endings:
            if phrase in text:
                text = text.replace(phrase, "")
                changes.append(f"移除chatbot痕迹: {phrase[:10]}...")
        
        if "如果您有任何问题" in text:
            text = re.sub(r'如果您有任何问题[^。！？]{0,30}[。！？]', '', text)
            changes.append("移除chatbot结尾语")
        
        if "如果您有任何疑问" in text:
            text = re.sub(r'如果您有任何疑问[^。！？]{0,30}[。！？]', '', text)
            changes.append("移除chatbot结尾语")
        
        if "作者：AI" in text or "作者：人工智能" in text:
            text = text.replace("作者：AI写作助手", "").replace("作者：人工智能", "")
            changes.append("移除AI署名")
        
        return text, changes
    
    def _split_long_sentences(self, text: str) -> Tuple[str, int]:
        """拆分长句（激进模式）"""
        sentences = get_sentences(text)
        new_sentences = []
        split_count = 0
        
        for sent in sentences:
            if len(sent) > 60:
                parts = re.split(r'[，,]', sent)
                if len(parts) > 1:
                    first = parts[0].strip()
                    rest = '，'.join(parts[1:]).strip()
                    if first and rest:
                        new_sentences.append(first + '。')
                        new_sentences.append(rest)
                        split_count += 1
                        continue
            new_sentences.append(sent)
        
        return ' '.join(new_sentences), split_count
    
    def _post_process(self, text: str) -> str:
        """后处理：清理残留问题"""
        # 修复标点问题：句号后不应有逗号
        text = re.sub(r'。\s*[,，]+\s*', '。', text)
        text = re.sub(r'。\s*、\s*', '。', text)
        
        # 修复逗号后多余逗号
        text = re.sub(r'[,，]\s*[,，]+', '，', text)
        
        # 清理句首多余标点
        text = re.sub(r'([。\n])[,，、\s]+', r'\1', text)
        text = re.sub(r'^[,，、\s]+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n[,，、\s]+', '\n', text)
        
        # 清理句尾多余标点
        text = re.sub(r'[,，、\s]+$', '', text, flags=re.MULTILINE)
        text = re.sub(r'[,，]+\s*([。！？])', r'\1', text)
        
        # 清理多余空格
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 修复标点后多余空格
        text = re.sub(r'([。！？，、；：])\s+', r'\1', text)
        
        # 清理残留问题
        text = re.sub(r'\n[。！？，、；：]+\n', '\n', text)
        text = re.sub(r'^[。！？，、；：]+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*{2,}', '', text)
        text = re.sub(r'[【\[\(][\]\)]', '', text)
        
        # 修复特定短语问题
        text = re.sub(r'变成(当前|现在)', r'成为\1', text)
        text = re.sub(r'潜在安全危险', '安全隐患', text)
        text = re.sub(r'可能安全风险', '潜在安全风险', text)
        
        # 修复句式改写后的残留问题
        text = re.sub(r'，此外还有', '，还有', text)
        text = re.sub(r'，此外并且', '，并且', text)
        text = re.sub(r'此外并且', '并且', text)
        text = re.sub(r'欠缺以', '不足以', text)
        text = re.sub(r'，同时也部分', '，部分', text)
        
        # 清理结尾残留
        text = re.sub(r'[。！？]\s*探讨\s*$', '。', text)
        text = re.sub(r'[。！？]\s*交流\s*$', '。', text)
        
        return text.strip()

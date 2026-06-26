#!/usr/bin/env python3
"""
上下文管理器 - 负责对话主题的连续性判断和上下文切换
"""

import json
import os
import re
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def _default_skill_config() -> Dict:
    """与 config.json 及代码默认值一致（单层嵌套合并用）"""
    return {
        "context_switch": {
            "similarity_threshold": 0.7,
            "continuity_threshold": 0.35,
            "compress_relevance_threshold": 0.3,
            "continuity_bonus_for_partial": 0.3,
            "drift_similarity_cap": 0.65,
            "time_decay_factor": 0.95,
            "max_topic_history": 10,
            "memory_relevance_threshold": 0.5,
        },
        "token_optimization": {
            "enabled": True,
            "token_limit": 80000,
            "compression_threshold": 56000,
            "context_cleanup_threshold": 0.8,
            "memory_load_limit": 2000,
            "optimization_interval": 300,
            "max_history_size": 100,
        },
        "memory_search": {
            "max_search_results": 5,
            "keyword_limit": 5,
            "search_depth": 2,
            "file_types": ["*.md"],
        },
        "optimization_settings": {
            "auto_optimization": True,
            "health_score_threshold": 70,
            "suggestions_check_interval": 600,
        },
    }


def _merge_user_config(base: Dict, user: Dict) -> Dict:
    """按顶层键合并嵌套 dict，避免用户 JSON 只写部分键时丢失默认子键"""
    for key, val in user.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(val, dict)
        ):
            merged = {**base[key], **val}
            base[key] = merged
        else:
            base[key] = val
    return base


def apply_environment_overrides(config: Dict) -> None:
    """
    环境变量覆盖配置（名称与 SKILL.md 一致）：
    - CONTEXT_HISTORY_SIZE -> context_switch.max_topic_history (1–100)
    - MEMORY_SEARCH_DEPTH -> memory_search.search_depth (1–3)
    - TOKEN_OPTIMIZER_ENABLED -> token_optimization.enabled (true/false/1/0)
    - CONTEXT_SWITCH_LOG_LEVEL -> context_switch.log_level (DEBUG/INFO/WARNING/ERROR)
    """
    cs = config.setdefault("context_switch", {})
    ms = config.setdefault("memory_search", {})
    to = config.setdefault("token_optimization", {})

    ch = os.environ.get("CONTEXT_HISTORY_SIZE", "").strip()
    if ch.isdigit():
        cs["max_topic_history"] = max(1, min(100, int(ch)))

    d = os.environ.get("MEMORY_SEARCH_DEPTH", "").strip()
    if d.isdigit():
        ms["search_depth"] = max(1, min(3, int(d)))

    te = os.environ.get("TOKEN_OPTIMIZER_ENABLED", "").strip().lower()
    if te in ("0", "false", "no", "off"):
        to["enabled"] = False
    elif te in ("1", "true", "yes", "on"):
        to["enabled"] = True

    ll = os.environ.get("CONTEXT_SWITCH_LOG_LEVEL", "").strip().upper()
    if ll in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        cs["log_level"] = ll


def load_skill_config(config_file: Optional[str] = None) -> Dict:
    """加载配置文件并应用环境变量覆盖。"""
    cfg = _default_skill_config()
    if config_file and Path(config_file).exists():
        with open(config_file, "r", encoding="utf-8") as f:
            _merge_user_config(cfg, json.load(f))
    apply_environment_overrides(cfg)
    lvl = cfg.get("context_switch", {}).get("log_level")
    if lvl:
        logging.getLogger().setLevel(getattr(logging, lvl, logging.INFO))
        if not logging.getLogger().handlers:
            logging.basicConfig(level=getattr(logging, lvl, logging.INFO))
    return cfg

@dataclass
class TopicSummary:
    """对话主题摘要"""
    topic: str
    keywords: List[str]
    timestamp: datetime
    tokens_used: int
    content_snippet: str
    is_compressed: bool = False  # 是否已压缩（渐变漂移时保留摘要、减少 token）
    
@dataclass
class ContextState:
    """上下文状态"""
    current_topic: Optional[str]
    topic_history: List[TopicSummary]
    memory_context: Optional[Dict]
    last_switch_time: Optional[datetime]
    switch_count: int
    total_tokens: int

class ContextManager:
    """上下文管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.context_file = Path("memory/context_switch_state.json")
        self.state = self._load_context_state()
        
    def _load_config(self, config_file: Optional[str]) -> Dict:
        return load_skill_config(config_file)
    
    def _load_context_state(self) -> ContextState:
        """加载上下文状态"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return self._dict_to_context_state(data)
            except Exception as e:
                print(f"加载上下文状态失败: {e}")
        
        # 创建新的上下文状态
        return ContextState(
            current_topic=None,
            topic_history=[],
            memory_context=None,
            last_switch_time=None,
            switch_count=0,
            total_tokens=0
        )
    
    def _dict_to_context_state(self, data: Dict) -> ContextState:
        """将字典转换为上下文状态"""
        topic_history = []
        for topic_data in data.get('topic_history', []):
            topic_history.append(TopicSummary(
                topic=topic_data['topic'],
                keywords=topic_data['keywords'],
                timestamp=datetime.fromisoformat(topic_data['timestamp']),
                tokens_used=topic_data['tokens_used'],
                content_snippet=topic_data['content_snippet'],
                is_compressed=topic_data.get('is_compressed', False)
            ))
        
        return ContextState(
            current_topic=data.get('current_topic'),
            topic_history=topic_history,
            memory_context=data.get('memory_context'),
            last_switch_time=datetime.fromisoformat(data['last_switch_time']) if data.get('last_switch_time') else None,
            switch_count=data.get('switch_count', 0),
            total_tokens=data.get('total_tokens', 0)
        )
    
    def _context_state_to_dict(self, state: ContextState) -> Dict:
        """将上下文状态转换为字典"""
        topic_history_data = []
        for topic in state.topic_history:
            topic_history_data.append({
                'topic': topic.topic,
                'keywords': topic.keywords,
                'timestamp': topic.timestamp.isoformat(),
                'tokens_used': topic.tokens_used,
                'content_snippet': topic.content_snippet,
                'is_compressed': getattr(topic, 'is_compressed', False)
            })
        
        return {
            'current_topic': state.current_topic,
            'topic_history': topic_history_data,
            'memory_context': state.memory_context,
            'last_switch_time': state.last_switch_time.isoformat() if state.last_switch_time else None,
            'switch_count': state.switch_count,
            'total_tokens': state.total_tokens
        }
    
    def save_context_state(self):
        """保存上下文状态"""
        try:
            self.context_file.parent.mkdir(parents=True, exist_ok=True)
            data = self._context_state_to_dict(self.state)
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存上下文状态失败: {e}")
    
    def summarize_topic(self, conversation_content: str) -> TopicSummary:
        """总结对话主题"""
        # 1. 提取关键词
        keywords = self.extract_keywords(conversation_content)
        
        # 2. 生成主题描述
        topic = self.generate_topic_description(conversation_content, keywords)
        
        # 3. 估算Token使用
        tokens_used = self.estimate_tokens(conversation_content)
        
        # 4. 获取内容片段
        snippet = self.get_content_snippet(conversation_content)
        
        return TopicSummary(
            topic=topic,
            keywords=keywords,
            timestamp=datetime.now(),
            tokens_used=tokens_used,
            content_snippet=snippet
        )
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 1. 简单分词和过滤
        words = re.findall(r'\b[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}\b', text)
        
        # 2. 过滤常见词
        stopwords = {'的', '了', '是', '在', '和', '有', '我', '你', '他', '她', '它', '这个', '那个', '什么', '怎么', '为什么'}
        filtered_words = [word for word in words if word not in stopwords]
        
        # 3. 去重和排序
        unique_words = list(set(filtered_words))
        unique_words.sort(key=len, reverse=True)  # 按长度排序，优先选择长词
        
        return unique_words[:self.config['memory_search']['keyword_limit']]
    
    def generate_topic_description(self, content: str, keywords: List[str]) -> str:
        """生成主题描述"""
        if not keywords:
            return "一般对话"
        
        # 根据关键词生成主题
        topic_patterns = {
            '记忆': '记忆管理相关',
            '技能': '技能开发相关',
            '项目': '项目管理相关',
            '任务': '任务处理相关',
            '配置': '系统配置相关',
            '权限': '权限管理相关',
            '飞书': '飞书集成相关',
            'Token': 'Token优化相关',
            '上下文': '上下文管理相关'
        }
        
        for keyword in keywords:
            for pattern, topic in topic_patterns.items():
                if pattern in keyword:
                    return topic
        
        # 默认：使用前3个关键词
        top_keywords = keywords[:3]
        return f"{', '.join(top_keywords)}相关"
    
    def calculate_topic_similarity(self, topic1: TopicSummary, topic2: TopicSummary) -> float:
        """计算主题相似度（含精确重叠 + 子串/包含弱匹配，便于识别渐变漂移）"""
        if not topic1.keywords or not topic2.keywords:
            return 0.0
        
        set1 = set(topic1.keywords)
        set2 = set(topic2.keywords)
        exact_overlap = len(set1 & set2)
        # 2 字子串 + 各 2 字片段的首字（如「局势」「股」），便于战争→股市→基本面渐变；排除虚字
        _stop_chars = {'的', '了', '是', '在', '和', '有', '与', '这', '那', '什', '么', '怎', '为', '一', '不'}
        def bigrams_and_leading_chars(w: str) -> set:
            s = set()
            if len(w) >= 2:
                for i in range(len(w) - 1):
                    b = w[i:i+2]
                    s.add(b)
                    if b[0] not in _stop_chars:
                        s.add(b[0])
            elif len(w) >= 1 and w[0] not in _stop_chars:
                s.add(w[0])
            return s
        sub1 = set().union(*(bigrams_and_leading_chars(w) for w in set1))
        sub2 = set().union(*(bigrams_and_leading_chars(w) for w in set2))
        has_partial = bool(sub1 & sub2)
        overlap = exact_overlap + (0.5 if has_partial else 0)
        max_length = max(len(set1), len(set2))
        keyword_similarity = min(1.0, overlap / max_length) if max_length > 0 else 0.0
        # 仅有弱关联时加成后上限略低于 similarity_threshold，倾向判为 drift_compress 以便压缩旧段
        if has_partial and keyword_similarity < self.config['context_switch'].get('similarity_threshold', 0.7):
            continuity_bonus = self.config['context_switch'].get('continuity_bonus_for_partial', 0.3)
            drift_cap = self.config['context_switch'].get('drift_similarity_cap', 0.65)
            keyword_similarity = min(drift_cap, keyword_similarity + continuity_bonus)
        
        time_diff = (datetime.now() - topic2.timestamp).total_seconds()
        time_decay = self.config['context_switch']['time_decay_factor'] ** (time_diff / 3600)
        return keyword_similarity * time_decay
    
    def should_switch_context(self, current_topic: TopicSummary) -> bool:
        """判断是否需要切换上下文（仅布尔，兼容旧逻辑）"""
        return self.get_context_action(current_topic) == "switch"

    def get_context_action(self, current_topic: TopicSummary) -> str:
        """
        判断上下文动作：对话连续性 + 主题相关性。
        - continuous: 与上一轮高度相关，保持连续、不压缩
        - drift_compress: 与上一轮中等相关（渐变漂移），对话连续但压缩与当前弱相关的历史
        - switch: 与上一轮几乎无关，硬切换
        """
        if not self.state.current_topic or not self.state.topic_history:
            return "continuous"
        
        previous_topic = self.state.topic_history[-1]
        similarity = self.calculate_topic_similarity(current_topic, previous_topic)
        
        sim_threshold = self.config['context_switch']['similarity_threshold']  # 默认 0.7
        continuity_threshold = self.config['context_switch'].get('continuity_threshold', 0.35)
        
        if similarity >= sim_threshold:
            return "continuous"
        if similarity < continuity_threshold:
            return "switch"
        return "drift_compress"
    
    def handle_empty_context(self, current_topic: TopicSummary) -> Dict:
        """处理空上下文"""
        # 1. 搜索相关记忆
        related_memories = self.search_related_memories(current_topic)
        
        # 2. 加载相关记忆
        memory_context = None
        if related_memories:
            memory_context = self.load_memory_context(related_memories[0])
            self.state.memory_context = memory_context
        
        # 3. 设置当前主题
        self.state.current_topic = current_topic.topic
        self.state.topic_history.append(current_topic)
        
        # 4. 限制历史记录数量
        max_history = self.config['context_switch']['max_topic_history']
        if len(self.state.topic_history) > max_history:
            self.state.topic_history = self.state.topic_history[-max_history:]
        
        self.save_context_state()
        
        return {
            'action': 'load_memory',
            'topic': current_topic.topic,
            'memory_loaded': bool(memory_context),
            'keywords': current_topic.keywords,
            'token_budget': self.get_remaining_tokens()
        }
    
    def handle_drift_compress(self, current_topic: TopicSummary) -> Dict:
        """
        渐变漂移：对话连续但主题已漂移。保留整条链，压缩与当前主题弱相关的历史轮。
        例如 美伊战争 → 对股票影响 → 股票基本面：压缩「战争」段为短摘要，不丢弃。
        """
        self.state.topic_history.append(current_topic)
        max_history = self.config['context_switch']['max_topic_history']
        if len(self.state.topic_history) > max_history:
            self.state.topic_history = self.state.topic_history[-max_history:]
        
        compress_threshold = self.config['context_switch'].get('compress_relevance_threshold', 0.3)
        compressed_count = 0
        # 仅对「当前轮之前」的历史做检查，不压缩刚加入的当前轮
        for i, past_topic in enumerate(self.state.topic_history[:-1]):
            if getattr(past_topic, 'is_compressed', False):
                continue
            relevance = self.calculate_topic_similarity(past_topic, current_topic)
            if relevance < compress_threshold:
                self._compress_topic_summary(past_topic)
                compressed_count += 1
        
        self.state.current_topic = current_topic.topic
        self.state.total_tokens += current_topic.tokens_used
        self.save_context_state()
        
        continuity_score = self.calculate_topic_similarity(current_topic, self.state.topic_history[-2]) if len(self.state.topic_history) >= 2 else 1.0
        
        return {
            'action': 'drift_compress',
            'topic': current_topic.topic,
            'keywords': current_topic.keywords,
            'token_budget': self.get_remaining_tokens(),
            'continuity_score': continuity_score,
            'compressed_count': compressed_count,
            'message': '对话连续，已压缩与当前主题弱相关的历史轮（保留摘要）'
        }

    def _compress_topic_summary(self, topic: TopicSummary):
        """将单条主题摘要压缩为短句，减少 token，不丢弃。"""
        topic.content_snippet = f"{topic.topic} [已压缩]"
        topic.tokens_used = min(topic.tokens_used, 50)  # 压缩后约 50 token 以内
        topic.is_compressed = True

    def handle_topic_switch(self, current_topic: TopicSummary) -> Dict:
        """处理主题切换"""
        # 1. 更新切换计数
        self.state.switch_count += 1
        self.state.last_switch_time = datetime.now()
        
        # 2. 搜索新主题的相关记忆
        related_memories = self.search_related_memories(current_topic)
        
        # 3. 加载新记忆
        memory_context = None
        if related_memories:
            memory_context = self.load_memory_context(related_memories[0])
            self.state.memory_context = memory_context
        
        # 4. 更新主题
        self.state.current_topic = current_topic.topic
        self.state.topic_history.append(current_topic)
        
        # 5. 限制历史记录数量
        max_history = self.config['context_switch']['max_topic_history']
        if len(self.state.topic_history) > max_history:
            self.state.topic_history = self.state.topic_history[-max_history:]
        
        self.save_context_state()
        
        return {
            'action': 'switch_context',
            'new_topic': current_topic.topic,
            'previous_topic': self.state.topic_history[-2].topic if len(self.state.topic_history) > 1 else None,
            'memory_loaded': bool(memory_context),
            'switch_count': self.state.switch_count,
            'keywords': current_topic.keywords,
            'token_budget': self.get_remaining_tokens()
        }
    
    def handle_continuous_context(self, current_topic: TopicSummary) -> Dict:
        """处理连续上下文"""
        # 1. 更新历史记录
        self.state.topic_history.append(current_topic)
        
        # 2. 限制历史记录数量
        max_history = self.config['context_switch']['max_topic_history']
        if len(self.state.topic_history) > max_history:
            self.state.topic_history = self.state.topic_history[-max_history:]
        
        # 3. 更新总Token使用
        self.state.total_tokens += current_topic.tokens_used
        
        self.save_context_state()
        
        # 更新当前主题（与 handle_empty_context / handle_topic_switch 一致）
        self.state.current_topic = current_topic.topic
        
        continuity_score = 1.0
        if len(self.state.topic_history) >= 2:
            continuity_score = self.calculate_topic_similarity(current_topic, self.state.topic_history[-2])
        
        return {
            'action': 'continuous_context',
            'topic': current_topic.topic,
            'keywords': current_topic.keywords,
            'token_budget': self.get_remaining_tokens(),
            'continuity_score': continuity_score
        }
    
    def manage_context(self, conversation_content: str) -> Dict:
        """管理上下文（含对话连续性：连续 / 渐变漂移压缩 / 硬切换）"""
        current_topic = self.summarize_topic(conversation_content)
        
        if not self.state.current_topic and not self.state.topic_history:
            return self.handle_empty_context(current_topic)
        
        action = self.get_context_action(current_topic)
        if action == "switch":
            return self.handle_topic_switch(current_topic)
        if action == "drift_compress":
            return self.handle_drift_compress(current_topic)
        return self.handle_continuous_context(current_topic)
    
    def search_related_memories(self, topic: TopicSummary) -> List[Dict]:
        """搜索相关记忆"""
        search_results = []
        topic_dir = Path("memory/topic")
        
        if not topic_dir.exists():
            return search_results
        
        # 1. 搜索所有话题文件
        for pattern in self.config['memory_search']['file_types']:
            for file_path in topic_dir.glob(pattern):
                if file_path.name == '.DS_Store':
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8')
                    score = self.calculate_memory_relevance(content, topic.keywords)
                    
                    if score > self.config['context_switch']['memory_relevance_threshold']:
                        search_results.append({
                            'file': file_path,
                            'score': score,
                            'content': content
                        })
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
        
        # 2. 按相关性排序
        search_results.sort(key=lambda x: x['score'], reverse=True)
        
        # 3. 限制结果数量
        max_results = self.config['memory_search']['max_search_results']
        return search_results[:max_results]
    
    def calculate_memory_relevance(self, content: str, keywords: List[str]) -> float:
        """计算记忆相关性"""
        if not keywords or not content:
            return 0.0
        
        # 计算关键词出现频率
        keyword_count = 0
        total_words = len(content.split())
        
        for keyword in keywords:
            keyword_count += content.lower().count(keyword.lower())
        
        # 归一化相关性分数
        if total_words == 0:
            return 0.0
        
        relevance = keyword_count / total_words
        return relevance
    
    def load_memory_context(self, memory_info: Dict) -> Dict:
        """加载记忆上下文"""
        file_path = memory_info['file']
        content = memory_info['content']
        score = memory_info['score']
        
        # 1. 提取摘要
        headline = self.extract_memory_headline(content)
        
        # 2. 获取核心内容
        core_content = self.extract_memory_core(content)
        
        return {
            'memory_file': str(file_path),
            'relevance_score': score,
            'headline': headline,
            'core_content': core_content,
            'loaded_at': datetime.now().isoformat()
        }
    
    def extract_memory_headline(self, content: str) -> str:
        """提取记忆头部摘要"""
        lines = content.split('\n')
        headline_lines = []
        
        for line in lines[:20]:  # 前20行
            if line.startswith('# ') or line.startswith('## '):
                headline_lines.append(line)
            elif headline_lines and line.strip() == '':
                break
        
        return '\n'.join(headline_lines)
    
    def extract_memory_core(self, content: str) -> str:
        """提取记忆核心内容"""
        lines = content.split('\n')
        core_lines = []
        
        for line in lines:
            if line.startswith('- ') and '**' in line:
                core_lines.append(line)
            elif '## ' in line:
                core_lines.append(line)
        
        return '\n'.join(core_lines[:10])  # 前10个核心条目
    
    def estimate_tokens(self, content: str) -> int:
        """估算Token使用"""
        # 粗略估算：中文字符0.75个token，英文单词1.3个token
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        
        chinese_tokens = chinese_chars / 0.75
        english_tokens = english_words * 1.3
        
        return int(chinese_tokens + english_tokens)
    
    def get_remaining_tokens(self) -> int:
        """获取剩余Token预算"""
        token_limit = self.config['token_optimization']['token_limit']
        return max(0, token_limit - self.state.total_tokens)
    
    def get_content_snippet(self, content: str, length: int = 100) -> str:
        """获取内容片段"""
        if len(content) <= length:
            return content
        
        return content[:length] + "..."

def main():
    """测试上下文管理器"""
    import argparse
    
    parser = argparse.ArgumentParser(description='上下文管理器测试工具')
    parser.add_argument('--content', help='对话内容')
    parser.add_argument('--test-switch', action='store_true', help='测试主题切换')
    parser.add_argument('--show-state', action='store_true', help='显示当前状态')
    parser.add_argument('--reset', action='store_true', help='重置上下文状态')
    
    args = parser.parse_args()
    
    manager = ContextManager()
    
    if args.reset:
        # 重置上下文状态
        manager.state = ContextState(
            current_topic=None,
            topic_history=[],
            memory_context=None,
            last_switch_time=None,
            switch_count=0,
            total_tokens=0
        )
        manager.save_context_state()
        print("上下文状态已重置")
        return
    
    if args.show_state:
        # 显示当前状态
        print("=== 当前上下文状态 ===")
        print(f"当前主题: {manager.state.current_topic}")
        print(f"历史主题数: {len(manager.state.topic_history)}")
        print(f"切换次数: {manager.state.switch_count}")
        print(f"总Token使用: {manager.state.total_tokens}")
        print(f"剩余Token: {manager.get_remaining_tokens()}")
        if manager.state.memory_context:
            print(f"记忆上下文: {manager.state.memory_context['memory_file']}")
        return
    
    if args.content:
        # 管理上下文
        result = manager.manage_context(args.content)
        print("=== 上下文管理结果 ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result['action'] == 'switch_context':
            print(f"\n主题切换: {result['previous_topic']} → {result['new_topic']}")
        elif result['action'] == 'continuous_context':
            print(f"\n保持连续上下文: {result['topic']}")
    
    if args.test_switch:
        # 测试主题切换
        topics = [
            "记忆管理技能的设计和实现",
            "今天天气很好，我们去公园吧",
            "飞书API权限问题处理",
            "Python编程技巧分享",
            "机器学习算法优化"
        ]
        
        for topic in topics:
            result = manager.manage_context(topic)
            print(f"\n主题: {topic}")
            print(f"操作: {result['action']}")
            print(f"关键词: {', '.join(result['keywords'])}")

if __name__ == "__main__":
    main()
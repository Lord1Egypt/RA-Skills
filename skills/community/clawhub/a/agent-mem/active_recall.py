#!/usr/bin/env python3
"""
主动召回模块 - 不等查询，主动补充上下文
这是我们系统目前最大的短板：只被动存储，不主动推送
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ActiveRecall:
    """主动召回 - 根据当前情境主动推送相关记忆"""
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.timeline_file = memory_dir / '.memory-timeline.json'
        self.graph_file = memory_dir / '.knowledge-graph.json'
        self.patterns_file = memory_dir / '.experience-patterns.json'
        self.state_file = memory_dir / '.memory-engine-state-v2.json'
        
        self._load_data()
    
    def _load_data(self):
        self.timeline = self._load_json(self.timeline_file, {'index': {}, 'topics': {}})
        self.graph = self._load_json(self.graph_file, {'nodes': {}, 'edges': [], 'chains': []})
        self.patterns = self._load_json(self.patterns_file, {'patterns': []})
    
    def _load_json(self, path: Path, default: Dict) -> Dict:
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return default
    
    def find_related_context(self, current_topic: str, depth: str = "medium") -> List[Dict]:
        """根据当前话题，找到相关的记忆上下文"""
        results = []
        
        # 1. 时序相关 - "上次这种情况是什么时候"
        timeline_related = self._find_timeline_related(current_topic)
        results.extend(timeline_related)
        
        # 2. 规律相关 - "有个规律可能适用"
        pattern_related = self._find_pattern_related(current_topic)
        results.extend(pattern_related)
        
        # 3. 图谱相关 - "这个项目之前有过类似决策"
        graph_related = self._find_graph_related(current_topic)
        results.extend(graph_related)
        
        # 去重 + 按相关度排序
        seen = set()
        unique_results = []
        for r in results:
            key = r.get('text', '')[:50]
            if key not in seen:
                seen.add(key)
                # 计算相关度
                r['relevance'] = self._calc_relevance(current_topic, r)
                unique_results.append(r)
        
        # 限制数量
        limit = 5 if depth == "shallow" else 10 if depth == "medium" else 20
        unique_results.sort(key=lambda x: -x.get('relevance', 0))
        return unique_results[:limit]
    
    def _find_timeline_related(self, topic: str) -> List[Dict]:
        """从时序记忆找相关"""
        results = []
        
        # 在topics里搜索
        for topic_name, entries in self.timeline.get('topics', {}).items():
            if topic.lower() in topic_name.lower():
                results.extend(entries[:3])
        
        # 在index里搜索
        for key, entry in self.timeline.get('index', {}).items():
            text = entry.get('text', '').lower()
            topic_lower = topic.lower()
            if topic_lower in text:
                results.append(entry)
        
        return results
    
    def _find_pattern_related(self, topic: str) -> List[Dict]:
        """从规律库找相关"""
        results = []
        
        for pattern in self.patterns.get('patterns', []):
            rule = pattern.get('rule', '').lower()
            if topic.lower() in rule or any(w in rule for w in topic.split()[:3]):
                pattern['source'] = 'pattern'
                pattern['text'] = pattern.get('rule', '')
                results.append(pattern)
        
        return results
    
    def _find_graph_related(self, topic: str) -> List[Dict]:
        """从知识图谱找相关"""
        results = []
        
        for node_id, node in self.graph.get('nodes', {}).items():
            text = str(node.get('text', '')) + str(node.get('label', ''))
            if topic.lower() in text.lower():
                node['source'] = 'graph'
                node['node_id'] = node_id
                results.append(node)
        
        return results
    
    def _calc_relevance(self, current_topic: str, entry: Dict) -> float:
        """计算相关度分数"""
        score = 0.0
        text = str(entry.get('text', '')) + str(entry.get('topic', '')) + str(entry.get('label', ''))
        
        # 关键词匹配
        for word in current_topic.split()[:5]:
            if word.lower() in text.lower():
                score += 0.2
        
        # 重要性加成
        score += (entry.get('importance', 5) / 10) * 0.3
        
        # 时间加成（越近越相关）
        date_str = entry.get('date', '')
        if date_str:
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d')
                days_ago = (datetime.now() - d).days
                score += max(0, (30 - days_ago) / 100)  # 30天内加分
            except:
                pass
        
        return min(score, 1.0)
    
    def generate_context_for_topic(self, topic: str, user_name: str = "用户") -> str:
        """生成适合插入对话的上下文"""
        related = self.find_related_context(topic, depth="medium")
        
        if not related:
            return ""
        
        lines = []
        by_source = {'timeline': [], 'pattern': [], 'graph': []}
        
        for r in related:
            source = r.get('source', 'unknown')
            if source in by_source:
                by_source[source].append(r)
        
        if by_source['pattern']:
            lines.append("🧠 **可能适用的经验**:")
            for p in by_source['pattern'][:2]:
                success_rate = p.get('success_count', 0) / max(p.get('times_tested', 1), 1) * 100
                if p.get('times_tested', 0) > 0:
                    lines.append(f"  • [{success_rate:.0f}%成功率] {p.get('rule', '')[:80]}")
                else:
                    lines.append(f"  • {p.get('rule', '')[:80]}")
        
        if by_source['timeline']:
            lines.append("\n📅 **之前的情况**:")
            for t in by_source['timeline'][:2]:
                date = t.get('date', '')
                text = t.get('text', '') or t.get('topic', '')
                lines.append(f"  • [{date}] {text[:70]}")
        
        if by_source['graph']:
            lines.append("\n🕸️ **相关项目历史**:")
            for g in by_source['graph'][:1]:
                text = g.get('text', '') or g.get('label', '')
                lines.append(f"  • {text[:80]}")
        
        return '\n'.join(lines)
    
    def check_before_decision(self, topic: str) -> str:
        """在做决策前主动检查历史经验"""
        related = self.find_related_context(topic, depth="shallow")
        
        if not related:
            return ""
        
        # 只返回最相关的一条
        if related:
            best = related[0]
            date = best.get('date', '之前')
            text = best.get('text', '') or best.get('rule', '') or best.get('label', '')
            
            return f"💡 上次遇到类似情况（{date}）：{text[:100]}..."
        
        return ""
    
    def get_stats(self) -> Dict:
        return {
            'timeline_entries': len(self.timeline.get('index', {})),
            'graph_nodes': len(self.graph.get('nodes', {})),
            'patterns_total': len(self.patterns.get('patterns', [])),
            'patterns_tested': sum(1 for p in self.patterns.get('patterns', []) if p.get('times_tested', 0) > 0)
        }

if __name__ == '__main__':
    home = Path.home()
    recall = ActiveRecall(home / '.agent-mem/memory')
    
    # 测试主动召回
    test_topics = ['Agent', '记忆系统', '飞书']
    
    print("=== 主动召回测试 ===\n")
    for topic in test_topics:
        context = recall.generate_context_for_topic(topic)
        if context:
            print(f"📌 主题: {topic}")
            print(context)
            print()
    
    stats = recall.get_stats()
    print(f"📊 召回系统状态: {json.dumps(stats, indent=2)}")

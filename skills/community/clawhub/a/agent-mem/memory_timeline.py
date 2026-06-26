#!/usr/bin/env python3
"""
时序记忆模块 - 时间线索引系统
目标：快速找到"上次XX是什么时候发生的"
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class MemoryTimeline:
    """时序记忆索引 - 记录每条记忆的时间线"""
    
    def __init__(self, memory_dir: Path):
        self.timeline_file = memory_dir / '.memory-timeline.json'
        self.data = self._load()
    
    def _load(self) -> Dict:
        if self.timeline_file.exists():
            try:
                with open(self.timeline_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'index': {},       # {hash: {date, topic, summary}}
            'topics': {},      # {topic: [timeline_entries]}
            'last_updated': None
        }
    
    def _save(self):
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.timeline_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, text: str, date: str, source_file: str = "", category: str = "general"):
        """添加时序条目"""
        # 计算文本hash
        import hashlib
        key = hashlib.md5(text.encode()).hexdigest()[:16]
        
        # 提取主题词
        topic = self._extract_topic(text)
        
        entry = {
            'date': date,
            'text': text[:150],
            'topic': topic,
            'category': category,
            'source': source_file,
            'created_at': datetime.now().isoformat()
        }
        
        self.data['index'][key] = entry
        
        # 更新主题索引
        if topic not in self.data['topics']:
            self.data['topics'][topic] = []
        
        # 检查是否已存在相同日期+主题
        existing = [i for i, e in enumerate(self.data['topics'][topic]) 
                    if e['date'] == date]
        if existing:
            # 更新
            self.data['topics'][topic][existing[0]] = entry
        else:
            self.data['topics'][topic].append(entry)
        
        # 按日期排序
        self.data['topics'][topic].sort(key=lambda x: x['date'], reverse=True)
        
        self._save()
        return key
    
    def _extract_topic(self, text: str) -> str:
        """提取主题词"""
        # 去掉日期前缀
        text = text.replace('[2026-05-01]', '').replace('[2026-04-30]', '').strip()
        
        # 提取前50字符作为主题标识
        topic = text[:50].strip('- *')
        return topic
    
    def find_last_occurrence(self, keyword: str) -> Optional[Dict]:
        """查找某个主题最后出现的时间"""
        for topic, entries in self.data['topics'].items():
            if keyword.lower() in topic.lower():
                if entries:
                    return entries[0]  # 已按日期降序
        return None
    
    def find_similar(self, text: str, limit: int = 5) -> List[Dict]:
        """查找相似记忆（基于文本相似度）"""
        import hashlib
        key = hashlib.md5(text.encode()).hexdigest()[:16]
        
        results = []
        for k, entry in self.data['index'].items():
            if k == key:
                continue
            # 简单相似度：前20字符相同
            if entry['text'][:20] == text[:20]:
                results.append(entry)
        
        results.sort(key=lambda x: x['date'], reverse=True)
        return results[:limit]
    
    def get_topic_history(self, topic_keyword: str) -> List[Dict]:
        """获取某个主题的完整时间线"""
        results = []
        for topic, entries in self.data['topics'].items():
            if topic_keyword.lower() in topic.lower():
                results.extend(entries)
        
        results.sort(key=lambda x: x['date'], reverse=True)
        return results
    
    def get_recent(self, days: int = 7) -> List[Dict]:
        """获取最近N天的记忆"""
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        results = []
        
        for entry in self.data['index'].values():
            if entry['date'] >= cutoff:
                results.append(entry)
        
        results.sort(key=lambda x: x['date'], reverse=True)
        return results
    
    def stats(self) -> Dict:
        """统计时序记忆状态"""
        return {
            'total_entries': len(self.data['index']),
            'total_topics': len(self.data['topics']),
            'last_updated': self.data.get('last_updated'),
            'recent_7d': len(self.get_recent(7))
        }

if __name__ == '__main__':
    from pathlib import Path
    home = Path.home()
    timeline = MemoryTimeline(home / '.agent-mem/memory')
    stats = timeline.stats()
    print(f"📊 时序记忆统计: {stats}")

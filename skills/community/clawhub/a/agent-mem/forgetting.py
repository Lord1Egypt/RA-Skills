#!/usr/bin/env python3
"""
遗忘模块 - 低价值记忆定期衰减
目标：只保留真正有用的，清理噪音和过期信息
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# 遗忘配置
FORGET_CONFIG = {
    # 按类别决定保留期（天）
    'category_ttl': {
        'system_change': 365,   # 系统变更保留1年
        'person': 180,           # 人物关系保留半年
        'preference': 90,        # 偏好保留3个月
        'insight': 60,           # 洞察保留2个月
        'work': 45,             # 工作类保留45天
        'schedule': 14,          # 日程只留14天
        'tech': 60,             # 技术保留2个月
        'general': 30           # 一般只留30天
    },
    # 按重要性决定保留期倍数
    'importance_multiplier': {
        10: 5.0,   # 最高重要性延长5倍
        8: 3.0,
        7: 2.0,
        6: 1.5,
        5: 1.0,
        3: 0.5,    # 低重要性减半
        1: 0.25
    },
    # 低于此分数的直接删除
    'delete_threshold': 3,
    # 每隔多少天运行一次遗忘
    'forget_interval_days': 7
}

class MemoryForgetting:
    """遗忘引擎 - 智能清理低价值记忆"""
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.timeline_file = memory_dir / '.memory-timeline.json'
        self.state_file = memory_dir / '.memory-engine-state-v2.json'
        self.forget_log = memory_dir / '.forgetting-log.json'
        self.data = self._load_log()
    
    def _load_log(self) -> Dict:
        if self.forget_log.exists():
            try:
                with open(self.forget_log, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'last_run': None,
            'forgotten_count': 0,
            'preserved_count': 0,
            'deleted_by_category': {}
        }
    
    def _save_log(self):
        with open(self.forget_log, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def calculate_ttl(self, category: str, importance: int) -> int:
        """计算单条记忆的TTL（天）"""
        base_ttl = FORGET_CONFIG['category_ttl'].get(category, 30)
        multiplier = FORGET_CONFIG['importance_multiplier'].get(importance, 1.0)
        return int(base_ttl * multiplier)
    
    def score_fact(self, entry: Dict) -> Tuple[float, str]:
        """给单条记忆打分，决定保留还是删除"""
        category = entry.get('category', 'general')
        importance = int(entry.get('importance', 5))
        date_str = entry.get('date', '')
        
        # 计算时间衰减
        try:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d')
            days_old = (datetime.now() - entry_date).days
        except:
            days_old = 0
        
        ttl = self.calculate_ttl(category, importance)
        
        # 分数 = 剩余TTL比例 * 重要性
        if ttl > 0:
            remaining_ratio = max(0, (ttl - days_old) / ttl)
        else:
            remaining_ratio = 0
        
        score = remaining_ratio * (importance / 10)
        
        reason = f"{category}, 重要性{importance}, {days_old}天前, TTL{ttl}天"
        
        return score, reason
    
    def run(self) -> Dict:
        """执行遗忘流程"""
        now = datetime.now().strftime('%Y-%m-%d')
        
        # 检查是否需要运行
        if self.data.get('last_run'):
            last = datetime.fromisoformat(self.data['last_run'])
            days_since = (datetime.now() - last).days
            if days_since < FORGET_CONFIG['forget_interval_days']:
                return {'status': 'skip', 'reason': f'距上次{days_since}天，跳过'}
        
        print(f"🧹 遗忘引擎启动 ({now})...")
        
        # 加载时序记忆
        if not self.timeline_file.exists():
            print("  ℹ️ 无时序数据，跳过")
            return {'status': 'skip', 'reason': 'no timeline'}
        
        with open(self.timeline_file, 'r') as f:
            timeline_data = json.load(f)
        
        index = timeline_data.get('index', {})
        
        forgotten = []
        preserved = []
        deleted = []
        
        for key, entry in index.items():
            score, reason = self.score_fact(entry)
            
            if score < FORGET_CONFIG['delete_threshold'] / 10:
                # 直接删除
                deleted.append({'key': key, 'entry': entry, 'score': score, 'reason': reason})
            elif score < 0.3:
                # 降级为"待确认"
                forgotten.append({'key': key, 'entry': entry, 'score': score, 'reason': reason})
            else:
                preserved.append(entry)
        
        # 更新时序数据
        for item in forgotten + deleted:
            key = item['key']
            if key in index:
                del index[key]
        
        with open(self.timeline_file, 'w') as f:
            json.dump(timeline_data, f, indent=2, ensure_ascii=False)
        
        # 更新topics索引
        topics = timeline_data.get('topics', {})
        for topic in list(topics.keys()):
            topic_entries = topics[topic]
            # 过滤掉已删除的
            valid_keys = {e.get('date', '') + e.get('topic', '')[:30] for e in preserved}
            topics[topic] = [e for e in topic_entries if (e.get('date', '') + e.get('topic', '')[:30]) in valid_keys]
            if not topics[topic]:
                del topics[topic]
        
        with open(self.timeline_file, 'w') as f:
            json.dump(timeline_data, f, indent=2, ensure_ascii=False)
        
        # 记录日志
        self.data['last_run'] = now
        self.data['forgotten_count'] += len(forgotten)
        self.data['preserved_count'] = len(preserved)
        self.data['deleted_count'] = len(deleted)
        self._save_log()
        
        result = {
            'status': 'done',
            'date': now,
            'forgotten': len(forgotten),
            'preserved': len(preserved),
            'deleted': len(deleted)
        }
        
        print(f"  ✅ 保留 {len(preserved)} 条, 遗忘 {len(forgotten)} 条, 删除 {len(deleted)} 条")
        
        return result
    
    def get_stats(self) -> Dict:
        return {
            'last_run': self.data.get('last_run'),
            'total_forgotten': self.data.get('forgotten_count', 0),
            'total_deleted': self.data.get('deleted_count', 0),
            'interval_days': FORGET_CONFIG['forget_interval_days']
        }

if __name__ == '__main__':
    home = Path.home()
    forgetting = MemoryForgetting(home / '.agent-mem/memory')
    
    result = forgetting.run()
    print(f"📊 遗忘统计: {json.dumps(result, indent=2)}")
    
    stats = forgetting.get_stats()
    print(f"📊 总计: 遗忘{stats['total_forgotten']}条, 删除{stats['total_deleted']}条")

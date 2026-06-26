#!/usr/bin/env python3
"""
多Agent记忆共享模块
借鉴 MemOS 的 multi-agent memory sharing 概念
允许记忆在Agent之间选择性共享
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set

class MultiAgentMemory:
    """多Agent记忆共享系统"""
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.share_config_file = memory_dir / '.share-config.json'
        self.share_log_file = memory_dir / '.share-log.json'
        self.config = self._load_config()
        self.share_log = self._load_log()
    
    def _load_config(self) -> Dict:
        if self.share_config_file.exists():
            try:
                with open(self.share_config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'share_rules': {},    # {category: {agents: [], enabled: bool}}
            'default_rules': {
                'system_change': {'agents': ['*'], 'enabled': True},  # 系统变更全部共享
                'tech': {'agents': ['tech-expert', 'code-architect'], 'enabled': True},
                'work': {'agents': ['work-assistant', 'advertising-agent'], 'enabled': True},
                'finance': {'agents': ['finance-assistant'], 'enabled': True},
                'general': {'agents': ['*'], 'enabled': False},      # 一般记忆不默认共享
            },
            'isolation': ['personal', 'preference']  # 永远不共享的类别
        }
    
    def _load_log(self) -> Dict:
        if self.share_log_file.exists():
            try:
                with open(self.share_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'shared_memories': [],  # 已共享的记忆
            'access_log': []        # 访问记录
        }
    
    def _save_config(self):
        with open(self.share_config_file, 'w') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _save_log(self):
        with open(self.share_log_file, 'w') as f:
            json.dump(self.share_log, f, indent=2, ensure_ascii=False)
    
    def set_share_rule(self, category: str, agents: List[str], enabled: bool = True):
        """设置某类记忆的共享规则"""
        if category in self.config['isolation']:
            return {'status': 'error', 'reason': f'{category} is in isolation list'}
        
        self.config['share_rules'][category] = {
            'agents': agents,
            'enabled': enabled
        }
        self._save_config()
        return {'status': 'ok', 'rule': self.config['share_rules'][category]}
    
    def can_share(self, category: str, target_agent: str) -> bool:
        """检查某类记忆是否可以共享给某个Agent"""
        # 检查隔离列表
        if category in self.config['isolation']:
            return False
        
        # 检查自定义规则
        if category in self.config['share_rules']:
            rule = self.config['share_rules'][category]
            if not rule.get('enabled', False):
                return False
            agents = rule.get('agents', [])
            if '*' in agents or target_agent in agents:
                return True
            return False
        
        # 检查默认规则
        if category in self.config['default_rules']:
            rule = self.config['default_rules'][category]
            if not rule.get('enabled', False):
                return False
            agents = rule.get('agents', [])
            if '*' in agents or target_agent in agents:
                return True
            return False
        
        return False
    
    def share_memory(self, memory_text: str, category: str, from_agent: str, to_agents: List[str]) -> Dict:
        """共享一条记忆给指定的Agent"""
        shared_to = []
        
        for agent in to_agents:
            if self.can_share(category, agent):
                self.share_log['shared_memories'].append({
                    'memory': memory_text[:200],
                    'category': category,
                    'from': from_agent,
                    'to': agent,
                    'date': datetime.now().isoformat()
                })
                shared_to.append(agent)
        
        self._save_log()
        
        return {
            'status': 'ok',
            'shared_to': shared_to,
            'total': len(to_agents)
        }
    
    def get_shared_for_agent(self, agent_id: str) -> List[Dict]:
        """获取某Agent收到的共享记忆"""
        shared = []
        for item in self.share_log.get('shared_memories', []):
            if item['to'] == agent_id:
                shared.append(item)
        return shared
    
    def get_share_stats(self) -> Dict:
        total = len(self.share_log.get('shared_memories', []))
        by_category = {}
        for item in self.share_log.get('shared_memories', []):
            cat = item['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            'total_shared': total,
            'by_category': by_category,
            'rules_count': len(self.config.get('share_rules', {})),
            'isolated_categories': self.config.get('isolation', [])
        }
    
    def list_share_rules(self) -> Dict:
        return {
            'custom_rules': self.config.get('share_rules', {}),
            'default_rules': self.config.get('default_rules', {}),
            'isolation': self.config.get('isolation', [])
        }

if __name__ == '__main__':
    home = Path.home()
    mshare = MultiAgentMemory(home / '.agent-mem/memory')
    
    # 测试
    print("=== 共享规则测试 ===")
    rules = mshare.list_share_rules()
    print(f"当前规则: {json.dumps(rules, indent=2, ensure_ascii=False)[:500]}")
    
    print("\n=== 共享能力检查 ===")
    test_cases = [
        ('system_change', 'tech-expert'),
        ('tech', 'main'),
        ('general', 'work-assistant'),
        ('preference', 'advertising-agent'),
    ]
    
    for cat, agent in test_cases:
        can = mshare.can_share(cat, agent)
        print(f"  {cat} -> {agent}: {can}")
    
    print(f"\n📊 共享统计: {mshare.get_share_stats()}")

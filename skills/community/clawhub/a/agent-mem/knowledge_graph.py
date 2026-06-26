#!/usr/bin/env python3
"""
知识图谱 V2 - 因果链 + 时序推理 + 事件聚类
升级: 自动检测因果链 + 按时间线串联 + 重要性聚类
"""
import json, re, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

# 因果链关键词
CAUSAL_PATTERNS = [
    (r'(因为|由于).+?(所以|导致|因此|于是)', 'cause_effect'),
    (r'(决定|选择|采用).+?(结果|成功|失败|效果)', 'decision_result'),
    (r'(为了|为了达到|为的是).+?(做了|执行|采用|修改)', 'goal_action'),
    (r'(修复|解决|处理).+?(问题|bug|故障|异常)', 'fix_problem'),
    (r'(升级|更新|优化).+?(完成|上线|发布)', 'upgrade_complete'),
    (r'(问题|失败|报错|错误).+?(修复|解决|恢复)', 'problem_solution'),
]

# 时序链阈值（小时）
CHAIN_TIME_THRESHOLD = 48  # 2天内的连续事件可能有关联

class KnowledgeGraph:
    def __init__(self, memory_dir: Path):
        self.graph_file = memory_dir / '.knowledge-graph.json'
        self.data = self._load()

    def _load(self) -> Dict:
        if self.graph_file.exists():
            try: return json.load(open(self.graph_file))
            except: pass
        return {'nodes': {}, 'edges': [], 'chains': [], 'clusters': [], 'last_updated': None}

    def _save(self):
        self.data['last_updated'] = datetime.now().isoformat()
        json.dump(self.data, open(self.graph_file, 'w'), indent=2, ensure_ascii=False)

    def _id(self, text: str) -> str:
        return hashlib.md5(text[:80].encode()).hexdigest()[:12]

    def add_event(self, text: str, date: str, importance: int = 5, category: str = "general"):
        """添加事件节点"""
        node_id = self._id(text)
        if node_id in self.data['nodes']:
            n = self.data['nodes'][node_id]
            n['last_seen'] = date
            n['importance'] = max(n.get('importance', 5), importance)
            n['mention_count'] = n.get('mention_count', 1) + 1
            self._save()
            return node_id

        self.data['nodes'][node_id] = {
            'type': 'event', 'text': text[:200], 'date': date,
            'importance': min(importance + 2, 10) if any(kw in text for kw in ['严重', '完成', '上线', '修复']) else importance,
            'category': category, 'mention_count': 1,
            'entities': [], 'first_seen': date, 'last_seen': date,
        }

        # 自动检测因果链
        self._detect_causal_chain(text, date, node_id)
        # 自动时序链接
        self._link_temporal_sequence(node_id, date, category)
        self._save()
        return node_id

    def _detect_causal_chain(self, text: str, date: str, node_id: str):
        """检测文本中的因果关系并自动构建链条"""
        for pattern, chain_type in CAUSAL_PATTERNS:
            match = re.search(pattern, text)
            if match:
                cause_part = text[:match.start()] if match.start() > 0 else text[:len(text)//2]
                effect_part = text[match.end():] if match.end() < len(text) else text[len(text)//2:]

                cause_id = self._id(cause_part.strip()[:30])
                effect_id = self._id(effect_part.strip()[:30])

                # 创建/更新cause和effect节点
                if cause_id not in self.data['nodes']:
                    self.data['nodes'][cause_id] = {
                        'type': 'cause' if chain_type in ['cause_effect', 'problem_solution'] else 'decision',
                        'text': cause_part.strip()[:150], 'date': date,
                        'importance': 6, 'category': 'auto', 'first_seen': date, 'last_seen': date
                    }
                if effect_id not in self.data['nodes']:
                    self.data['nodes'][effect_id] = {
                        'type': 'effect' if chain_type in ['cause_effect'] else 'result',
                        'text': effect_part.strip()[:150], 'date': date,
                        'importance': 7, 'category': 'auto', 'first_seen': date, 'last_seen': date
                    }

                # 建立因果边
                edge = {'from': cause_id, 'to': effect_id, 'type': chain_type, 'date': date, 'chain': True}
                if edge not in self.data['edges']:
                    self.data['edges'].append(edge)

                # 注册因果链条
                chain = {
                    'chain_id': len(self.data['chains']),
                    'trigger': node_id,
                    'cause': cause_id,
                    'effect': effect_id,
                    'type': chain_type,
                    'text': match.group(0),
                    'created_at': datetime.now().isoformat()
                }
                self.data['chains'].append(chain)
                break  # 一个事件只建一条主要链

    def _link_temporal_sequence(self, node_id: str, date_str: str, category: str):
        """按时间顺序链接同类事件"""
        current_date = datetime.fromisoformat(date_str) if 'T' in date_str else \
                       datetime.strptime(date_str, '%Y-%m-%d')
        recent_events = []

        for nid, node in sorted(self.data['nodes'].items(),
                                 key=lambda x: x[1].get('date', ''), reverse=True):
            if nid == node_id or node.get('type') != 'event':
                continue
            nd = node.get('date', '')
            if not nd: continue
            try:
                node_date = datetime.fromisoformat(nd) if 'T' in nd else datetime.strptime(nd, '%Y-%m-%d')
                diff_hours = abs((current_date - node_date).total_seconds()) / 3600
                if diff_hours < CHAIN_TIME_THRESHOLD and node.get('category') == category:
                    recent_events.append((nid, diff_hours, node.get('importance', 5)))
            except:
                continue

        # 链接最近的3个同类事件
        for nid, diff, imp in sorted(recent_events, key=lambda x: x[1])[:3]:
            if imp >= 5 or diff < 24:  # 重要事件或24小时内的事件
                edge = {'from': node_id, 'to': nid, 'type': 'temporal_sequence',
                        'date': date_str, 'temporal_gap_hours': round(diff, 1)}
                if edge not in self.data['edges']:
                    self.data['edges'].append(edge)

    def find_chain_by_keyword(self, keyword: str) -> List[Dict]:
        """关键词查找完整因果链"""
        results = []
        for chain in self.data['chains']:
            cause = self.data['nodes'].get(chain.get('cause', ''), {})
            effect = self.data['nodes'].get(chain.get('effect', ''), {})
            trigger = self.data['nodes'].get(chain.get('trigger', ''), {})

            chain_text = f"{cause.get('text','')} {effect.get('text','')} {trigger.get('text','')}"
            if keyword.lower() in chain_text.lower():
                results.append({
                    'type': chain['type'],
                    'cause': cause.get('text', '')[:100],
                    'effect': effect.get('text', '')[:100],
                    'trigger': trigger.get('text', '')[:100],
                    'pattern': chain.get('text', ''),
                })
        return results

    def build_clusters(self):
        """按重要性聚类 - 提炼高价值知识块"""
        clusters = defaultdict(list)
        for nid, node in self.data['nodes'].items():
            imp = node.get('importance', 5)
            if imp >= 7:
                cluster_key = f"high_value_{node.get('category', 'general')}"
            elif imp >= 5:
                cluster_key = f"medium_{node.get('category', 'general')}"
            else:
                cluster_key = f"low_{node.get('category', 'general')}"
            clusters[cluster_key].append(nid)

        self.data['clusters'] = [
            {'cluster_id': len(self.data['clusters']) + i, 'key': k, 'nodes': v}
            for i, (k, v) in enumerate(clusters.items())
        ]

    def get_stats(self) -> Dict:
        return {
            'nodes': len(self.data['nodes']),
            'edges': len(self.data['edges']),
            'chains': len(self.data['chains']),
            'high_importance': sum(1 for n in self.data['nodes'].values() if n.get('importance', 5) >= 7),
            'by_type': defaultdict(int, {n.get('type'): 1 for n in self.data['nodes'].values()}),
        }

if __name__ == '__main__':
    kg = KnowledgeGraph(Path.home() / '.agent-mem/memory')
    stats = kg.get_stats()
    print(f"📊 知识图谱 V2 统计:")
    print(f"   节点: {stats['nodes']}, 边: {stats['edges']}, 链: {stats['chains']}")
    print(f"   高优先级: {stats['high_importance']}")
    kg.build_clusters()
    print(f"   聚类数: {len(kg.data['clusters'])}")

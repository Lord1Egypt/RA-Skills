#!/usr/bin/env python3
"""
实体链接增强 - 借鉴 Mem0 的 Entity Linking 概念
让记忆之间的关联更强，不再是孤立的点
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

class EntityLinker:
    """实体链接 - 建立记忆之间的语义关联"""
    
    def __init__(self, memory_dir: Path):
        self.links_file = memory_dir / '.entity-links.json'
        self.entities_file = memory_dir / '.entity-index.json'
        self.data = self._load()
        self.entities = self._load_entities()
    
    def _load(self) -> Dict:
        if self.links_file.exists():
            try:
                with open(self.links_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'links': [],      # [{entity1, entity2, relation, context, count}]
            'last_updated': None
        }
    
    def _load_entities(self) -> Dict:
        if self.entities_file.exists():
            try:
                with open(self.entities_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'entities': {},  # {entity_name: {type, aliases, first_seen, mentions}}
            'by_type': {}    # {type: [entity_names]}
        }
    
    def _save(self):
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.links_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _save_entities(self):
        with open(self.entities_file, 'w') as f:
            json.dump(self.entities, f, indent=2, ensure_ascii=False)
    
    # 实体类型定义
    ENTITY_TYPES = {
        'agent': ['main', 'work-assistant', 'advertising-agent', 'tech-expert', 'code-architect', 'prompt-optimizer', 'data-assistant', 'finance-assistant'],
        'project': ['Pixel Office', '记忆引擎', '记忆系统', 'dispatch系统', '调度系统'],
        'person': ['用户', '团队', '联系人'],
        'tool': ['飞书', 'OpenClaw', '浏览器', 'API'],
        'action': ['创建', '修改', '删除', '优化', '修复', '部署', '上线'],
        'concept': ['记忆', '调度', 'Agent', '工作流', '规则']
    }
    
    # 关系类型
    RELATION_TYPES = {
        'part_of': ['是...的一部分', '属于', '包含'],
        'uses': ['使用', '调用', '依赖'],
        'creates': ['创建', '生成', '新建'],
        'modifies': ['修改', '更新', '优化'],
        'related_to': ['相关', '关联'],
        'before': ['之前', '先于'],
        'after': ['之后', '继']
    }
    
    def extract_entities(self, text: str, date: str) -> List[Dict]:
        """从文本中提取实体"""
        entities = []
        
        for entity_type, keywords in self.ENTITY_TYPES.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    # 规范化实体名
                    entity_name = keyword
                    
                    # 更新实体索引
                    if entity_name not in self.entities['entities']:
                        self.entities['entities'][entity_name] = {
                            'type': entity_type,
                            'aliases': [],
                            'first_seen': date,
                            'last_seen': date,
                            'mentions': 0
                        }
                    
                    e = self.entities['entities'][entity_name]
                    e['mentions'] += 1
                    e['last_seen'] = date
                    
                    # 更新类型索引
                    if entity_type not in self.entities['by_type']:
                        self.entities['by_type'][entity_type] = []
                    if entity_name not in self.entities['by_type'][entity_type]:
                        self.entities['by_type'][entity_type].append(entity_name)
                    
                    entities.append({
                        'name': entity_name,
                        'type': entity_type,
                        'position': text.find(keyword)
                    })
        
        self._save_entities()
        return entities
    
    def link_entities(self, text: str, date: str, importance: int = 5):
        """从文本中发现并记录实体之间的关系"""
        entities = self.extract_entities(text, date)
        
        if len(entities) < 2:
            return []
        
        new_links = []
        
        # 检查实体两两之间是否有关系
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                e1 = entities[i]['name']
                e2 = entities[j]['name']
                
                # 判断关系类型
                relation = self._detect_relation(text, e1, e2)
                if relation:
                    # 检查是否已存在这条边
                    exists = False
                    for link in self.data['links']:
                        if link['entity1'] == e1 and link['entity2'] == e2 and link['relation'] == relation:
                            link['count'] += 1
                            link['last_seen'] = date
                            exists = True
                            break
                    
                    if not exists:
                        self.data['links'].append({
                            'entity1': e1,
                            'entity2': e2,
                            'relation': relation,
                            'context': text[:100],
                            'date': date,
                            'count': 1,
                            'importance': importance
                        })
                        new_links.append({'entity1': e1, 'entity2': e2, 'relation': relation})
        
        if new_links:
            self._save()
        
        return new_links
    
    def _detect_relation(self, text: str, e1: str, e2: str) -> Optional[str]:
        """检测两个实体之间的关系类型"""
        text_lower = text.lower()
        
        # 检查动词性关系
        action_keywords = {
            'creates': ['创建', '生成', '新建', '制作'],
            'uses': ['使用', '调用', '依赖', '用'],
            'modifies': ['修改', '更新', '调整'],
            'part_of': ['是', '属于', '包含'],
        }
        
        for rel, keywords in action_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    # 检查 e1 和 e2 是否都在关键词附近
                    pos1 = text_lower.find(e1.lower())
                    pos2 = text_lower.find(e2.lower())
                    if pos1 >= 0 and pos2 >= 0 and abs(pos1 - pos2) < 50:
                        return rel
        
        # 如果文本包含两个实体但没发现明确关系，标记为 related_to
        if e1 in text_lower and e2 in text_lower:
            return 'related_to'
        
        return None
    
    def get_related_entities(self, entity_name: str, max_results: int = 10) -> List[Dict]:
        """获取某个实体的所有关联实体"""
        related = []
        
        for link in self.data['links']:
            if link['entity1'] == entity_name:
                related.append({
                    'entity': link['entity2'],
                    'relation': link['relation'],
                    'count': link['count'],
                    'context': link['context'][:60]
                })
            elif link['entity2'] == entity_name:
                related.append({
                    'entity': link['entity1'],
                    'relation': link['relation'],
                    'count': link['count'],
                    'context': link['context'][:60]
                })
        
        # 按出现次数排序
        related.sort(key=lambda x: -x['count'])
        return related[:max_results]
    
    def get_entity_graph(self, focus_entity: str = None, depth: int = 1) -> Dict:
        """获取实体关系图（可指定焦点实体）"""
        graph = {
            'nodes': [],
            'edges': []
        }
        
        # 获取所有相关实体
        entities_of_interest = {focus_entity} if focus_entity else set()
        
        # 收集节点
        for entity_name in self.entities['entities']:
            if not focus_entity or entity_name == focus_entity or entity_name in entities_of_interest:
                e = self.entities['entities'][entity_name]
                graph['nodes'].append({
                    'id': entity_name,
                    'type': e['type'],
                    'mentions': e['mentions']
                })
        
        # 收集边
        for link in self.data['links']:
            if not focus_entity or link['entity1'] == focus_entity or link['entity2'] == focus_entity:
                graph['edges'].append({
                    'from': link['entity1'],
                    'to': link['entity2'],
                    'relation': link['relation'],
                    'count': link['count']
                })
        
        return graph
    
    def find_hub_entities(self, min_links: int = 3) -> List[Dict]:
        """找到连接多个实体的枢纽实体（高连接度）"""
        link_counts = {}
        
        for link in self.data['links']:
            for e in [link['entity1'], link['entity2']]:
                link_counts[e] = link_counts.get(e, 0) + 1
        
        hubs = []
        for entity, count in link_counts.items():
            if count >= min_links:
                e_data = self.entities['entities'].get(entity, {})
                hubs.append({
                    'entity': entity,
                    'type': e_data.get('type', 'unknown'),
                    'links': count
                })
        
        hubs.sort(key=lambda x: -x['links'])
        return hubs
    
    def get_stats(self) -> Dict:
        return {
            'total_entities': len(self.entities['entities']),
            'total_links': len(self.data['links']),
            'by_type': {t: len(ents) for t, ents in self.entities['by_type'].items()},
            'hubs': len(self.find_hub_entities()),
            'last_updated': self.data.get('last_updated')
        }

if __name__ == '__main__':
    home = Path.home()
    linker = EntityLinker(home / '.agent-mem/memory')
    
    # 测试链接发现
    test_text = "今天更新了 memory_timeline.py，这是记忆系统的核心模块，用于追踪时间线"
    links = linker.link_entities(test_text, "2026-05-01", importance=7)
    
    print(f"📊 Entity Linker 统计: {json.dumps(linker.get_stats(), indent=2)}")
    print(f"🔗 发现链接: {links}")
    
    # 找枢纽实体
    hubs = linker.find_hub_entities(2)
    print(f"🪢 枢纽实体: {hubs}")

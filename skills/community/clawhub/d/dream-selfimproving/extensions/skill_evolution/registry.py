"""
SkillRegistry — 技能注册表管理器
维护所有技能的状态、版本和元数据
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_REGISTRY_FILE = WORKSPACE / "memory" / "skill_registry.json"


class SkillRegistry:
    """技能注册表"""
    
    def __init__(self):
        self.registry = self._load()
    
    def _load(self) -> Dict:
        """加载注册表"""
        if SKILL_REGISTRY_FILE.exists():
            try:
                return json.loads(SKILL_REGISTRY_FILE.read_text(encoding='utf-8'))
            except:
                pass
        return self._create_empty()
    
    def _create_empty(self) -> Dict:
        return {
            'version': '1.0.0',
            'skills': {},
            'history': [],
            'auto_skills_index': {},  # 索引快速查找自动创建的技能
        }
    
    def _save(self):
        """保存注册表"""
        SKILL_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        SKILL_REGISTRY_FILE.write_text(
            json.dumps(self.registry, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def add_skill(self, skill_name: str, category: str, description: str,
                  auto_created: bool = False, template: str = "default") -> bool:
        """添加技能到注册表"""
        now = datetime.now().isoformat()
        
        if skill_name in self.registry['skills']:
            return False  # 已存在
        
        skill_data = {
            'name': skill_name,
            'category': category,
            'description': description,
            'auto_created': auto_created,
            'template': template,
            'status': 'active',
            'created_at': now,
            'last_used': now,
            'last_modified': now,
            'total_calls': 0,
            'score': 0.0,
            'version': '1.0.0',
            'changelog': [{
                'version': '1.0.0',
                'date': now,
                'change': 'Initial creation',
                'author': 'auto' if auto_created else 'manual'
            }],
            'dependencies': [],
            'tags': [],
            'quality_score': 0.0,
            'source': 'dream-extension'
        }
        
        self.registry['skills'][skill_name] = skill_data
        
        # 更新索引
        if auto_created:
            self.registry['auto_skills_index'][skill_name] = {
                'category': category,
                'created_at': now,
                'quality_score': 0.0
            }
        
        self._add_history(skill_name, 'created', f'Auto={auto_created}, category={category}')
        self._save()
        return True
    
    def update_skill(self, skill_name: str, **kwargs) -> bool:
        """更新技能信息"""
        if skill_name not in self.registry['skills']:
            return False
        
        skill = self.registry['skills'][skill_name]
        
        # 允许更新的字段
        allowed = ['description', 'category', 'status', 'total_calls', 
                   'score', 'quality_score', 'tags', 'dependencies', 'version']
        
        for key, value in kwargs.items():
            if key in allowed:
                skill[key] = value
        
        skill['last_modified'] = datetime.now().isoformat()
        self._add_history(skill_name, 'updated', f'Fields: {list(kwargs.keys())}')
        self._save()
        return True
    
    def record_call(self, skill_name: str, score_delta: float = 0):
        """记录技能被调用"""
        if skill_name not in self.registry['skills']:
            return
        
        skill = self.registry['skills'][skill_name]
        skill['total_calls'] += 1
        skill['last_used'] = datetime.now().isoformat()
        skill['score'] += score_delta
        
        # 保持 score 不超过 10000
        if skill['score'] > 10000:
            skill['score'] = 10000
        
        self._save()
    
    def get_skill(self, skill_name: str) -> Optional[Dict]:
        """获取技能信息"""
        return self.registry['skills'].get(skill_name)
    
    def get_all_skills(self) -> List[Dict]:
        """获取所有技能"""
        return list(self.registry['skills'].values())
    
    def get_active_skills(self) -> List[str]:
        """获取活跃技能列表"""
        return [
            name for name, data in self.registry['skills'].items()
            if data['status'] in ['active', 'low']
        ]
    
    def get_archived_skills(self) -> List[str]:
        """获取归档技能列表"""
        return [
            name for name, data in self.registry['skills'].items()
            if data['status'] == 'archived'
        ]
    
    def get_auto_created_skills(self) -> List[Dict]:
        """获取所有自动创建的技能"""
        return [
            data for name, data in self.registry['auto_skills_index'].items()
        ]
    
    def get_skills_by_category(self, category: str) -> List[str]:
        """按类别获取技能"""
        return [
            name for name, data in self.registry['skills'].items()
            if data.get('category') == category
        ]
    
    def search_skills(self, query: str) -> List[Dict]:
        """搜索技能（名称、描述、标签）"""
        query_lower = query.lower()
        results = []
        
        for name, data in self.registry['skills'].items():
            if query_lower in name.lower():
                results.append(data)
            elif query_lower in data.get('description', '').lower():
                results.append(data)
            elif any(query_lower in tag.lower() for tag in data.get('tags', [])):
                results.append(data)
        
        return results
    
    def _add_history(self, skill_name: str, event: str, detail: str):
        """添加历史记录"""
        self.registry['history'].append({
            'timestamp': datetime.now().isoformat(),
            'skill': skill_name,
            'event': event,
            'detail': detail
        })
        
        if len(self.registry['history']) > 500:
            self.registry['history'] = self.registry['history'][-500:]
    
    def get_history(self, skill_name: str = None, limit: int = 50) -> List[Dict]:
        """获取历史记录"""
        if skill_name:
            return [
                h for h in self.registry['history'][-limit:]
                if h['skill'] == skill_name
            ]
        return self.registry['history'][-limit:]
    
    def get_stats(self) -> Dict:
        """获取注册表统计"""
        skills = self.registry['skills']
        return {
            'total_skills': len(skills),
            'active': sum(1 for s in skills.values() if s['status'] == 'active'),
            'low': sum(1 for s in skills.values() if s['status'] == 'low'),
            'dormant': sum(1 for s in skills.values() if s['status'] == 'dormant'),
            'archived': sum(1 for s in skills.values() if s['status'] == 'archived'),
            'auto_created': len(self.registry['auto_skills_index']),
            'categories': len(set(s.get('category') for s in skills.values())),
        }

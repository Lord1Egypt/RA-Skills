"""
DecayEngine — 用进废退引擎
根据技能使用情况自动调整技能状态，执行归档和唤醒逻辑
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_REGISTRY_FILE = WORKSPACE / "memory" / "skill_registry.json"


class DecayEngine:
    """用进废退引擎"""
    
    # 归档阈值
    ARCHIVE_AFTER_DAYS = 90   # 90天未用 -> 可归档
    WARN_AFTER_DAYS = 30      # 30天未用 -> 警告
    
    # 降级阈值
    DEMOTE_TO_LOW_AFTER_DAYS = 60   # 60天未用 -> 降为低活跃
    DEMOTE_TO_DORMANT_AFTER_DAYS = 75  # 75天未用 -> 降为休眠
    
    # 最小调用次数才考虑归档
    MIN_CALLS_BEFORE_ARCHIVE = 3
    
    def __init__(self):
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        if SKILL_REGISTRY_FILE.exists():
            try:
                return json.loads(SKILL_REGISTRY_FILE.read_text(encoding='utf-8'))
            except:
                return {'skills': {}, 'history': []}
        return {'skills': {}, 'history': []}
    
    def _save_registry(self):
        """保存技能注册表"""
        SKILL_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        SKILL_REGISTRY_FILE.write_text(
            json.dumps(self.registry, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def register_skill(self, skill_name: str, category: str = "general", 
                      description: str = "", auto_created: bool = False):
        """注册新技能"""
        now = datetime.now().isoformat()
        if skill_name not in self.registry['skills']:
            self.registry['skills'][skill_name] = {
                'name': skill_name,
                'category': category,
                'description': description,
                'auto_created': auto_created,
                'status': 'active',
                'created_at': now,
                'last_used': now,
                'total_calls': 0,
                'score_history': [],
                'version': '1.0.0',
                'source': 'manual' if not auto_created else 'auto',
            }
            self._record_history(skill_name, 'registered', f'New skill registered (auto={auto_created})')
            self._save_registry()
    
    def record_usage(self, skill_name: str, score: float = 0):
        """记录技能使用"""
        if skill_name not in self.registry['skills']:
            self.register_skill(skill_name)
        
        skill = self.registry['skills'][skill_name]
        now = datetime.now().isoformat()
        skill['last_used'] = now
        skill['total_calls'] += 1
        skill['status'] = 'active'
        skill['score_history'].append({
            'timestamp': now,
            'score': score
        })
        # 只保留最近30条历史
        if len(skill['score_history']) > 30:
            skill['score_history'] = skill['score_history'][-30:]
        
        self._record_history(skill_name, 'used', f'Score: {score}')
        self._save_registry()
    
    def apply_decay(self, skill_name: str, days_idle: int) -> Tuple[str, str]:
        """
        应用用进废退逻辑，返回 (原状态, 新状态)
        """
        if skill_name not in self.registry['skills']:
            return 'unknown', 'unknown'
        
        skill = self.registry['skills'][skill_name]
        old_status = skill['status']
        calls = skill.get('total_calls', 0)
        
        # 根据空闲天数决定新状态
        if days_idle >= self.ARCHIVE_AFTER_DAYS and calls >= self.MIN_CALLS_BEFORE_ARCHIVE:
            new_status = 'archived'
        elif days_idle >= self.DEMOTE_TO_DORMANT_AFTER_DAYS:
            new_status = 'dormant'
        elif days_idle >= self.DEMOTE_TO_LOW_AFTER_DAYS:
            new_status = 'low'
        elif days_idle >= self.WARN_AFTER_DAYS:
            new_status = 'low'  # 开始衰减
        else:
            new_status = 'active'
        
        if old_status != new_status:
            skill['status'] = new_status
            self._record_history(skill_name, 'status_change', 
                               f'{old_status} -> {new_status} (idle {days_idle} days)')
            self._save_registry()
        
        return old_status, new_status
    
    def process_all_skills_decay(self, skill_scores: Dict[str, Dict]) -> List[Dict]:
        """
        处理所有技能的衰减，返回状态变化的技能列表
        skill_scores: 从 SkillScorer 获取的评分数据
        """
        changes = []
        for skill_name, score_data in skill_scores.items():
            days = score_data.get('days_since_last_call')
            if days is None:
                continue
            
            old_status, new_status = self.apply_decay(skill_name, days)
            if old_status != new_status:
                changes.append({
                    'skill': skill_name,
                    'old_status': old_status,
                    'new_status': new_status,
                    'days_idle': days,
                    'score': score_data.get('score', 0)
                })
        return changes
    
    def wake_skill(self, skill_name: str) -> bool:
        """唤醒休眠/归档的技能"""
        if skill_name not in self.registry['skills']:
            return False
        
        skill = self.registry['skills'][skill_name]
        if skill['status'] in ['archived', 'dormant']:
            old_status = skill['status']
            skill['status'] = 'active'
            skill['last_used'] = datetime.now().isoformat()
            self._record_history(skill_name, 'woken', f'{old_status} -> active')
            self._save_registry()
            return True
        return False
    
    def archive_skill(self, skill_name: str) -> bool:
        """手动归档技能"""
        if skill_name not in self.registry['skills']:
            return False
        
        skill = self.registry['skills'][skill_name]
        skill['status'] = 'archived'
        self._record_history(skill_name, 'archived', 'Manually archived')
        self._save_registry()
        return True
    
    def get_skill_status(self, skill_name: str) -> Optional[str]:
        """获取技能状态"""
        if skill_name not in self.registry['skills']:
            return None
        return self.registry['skills'][skill_name]['status']
    
    def get_all_skills_by_status(self, status: str) -> List[str]:
        """获取某状态的所有技能"""
        return [
            name for name, data in self.registry['skills'].items()
            if data['status'] == status
        ]
    
    def get_decay_report(self) -> Dict:
        """生成衰减报告"""
        skills = self.registry['skills']
        report = {
            'total': len(skills),
            'by_status': {},
            'warnings': [],  # 30天以上未用
            'need_archive': [],  # 90天以上未用
            'archived_count': 0,
        }
        
        now = datetime.now()
        for name, data in skills.items():
            status = data['status']
            report['by_status'][status] = report['by_status'].get(status, 0) + 1
            
            if status == 'archived':
                report['archived_count'] += 1
            
            # 计算空闲天数
            last_used = data.get('last_used', '')
            if last_used:
                try:
                    last_dt = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                    days_idle = (now - last_dt.replace(tzinfo=None)).days
                    
                    if days_idle >= self.ARCHIVE_AFTER_DAYS and status != 'archived':
                        report['need_archive'].append({
                            'skill': name,
                            'days_idle': days_idle,
                            'status': status
                        })
                    elif days_idle >= self.WARN_AFTER_DAYS and status == 'active':
                        report['warnings'].append({
                            'skill': name,
                            'days_idle': days_idle
                        })
                except:
                    pass
        
        return report
    
    def _record_history(self, skill_name: str, event: str, detail: str):
        """记录历史"""
        self.registry['history'].append({
            'timestamp': datetime.now().isoformat(),
            'skill': skill_name,
            'event': event,
            'detail': detail
        })
        # 只保留最近500条历史
        if len(self.registry['history']) > 500:
            self.registry['history'] = self.registry['history'][-500:]
    
    def get_auto_created_skills(self) -> List[Dict]:
        """获取所有自动创建的技能"""
        return [
            {'name': name, **data}
            for name, data in self.registry['skills'].items()
            if data.get('auto_created', False)
        ]

"""
SkillScorer — 技能评分器
基于调用频率、成功率、时间衰减计算技能活跃度
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

SKILL_DB_PATH = Path.home() / ".skill_scoreboard"
DB_FILE = SKILL_DB_PATH / "scores.json"


class SkillScorer:
    """技能评分器"""
    
    # 评分权重
    WEIGHTS = {
        'call_frequency': 0.25,      # 调用频率
        'recency': 0.30,             # 时间新鲜度
        'success_rate': 0.20,        # 成功率
        'total_score': 0.25,         # 累计积分
    }
    
    # 时间衰减节点（天 -> 衰减系数）
    DECAY_NODES = [
        (7, 0.95),    # 7天不用，衰减5%
        (14, 0.85),   # 14天不用，衰减15%
        (30, 0.60),   # 30天不用，衰减40%
        (60, 0.30),   # 60天不用，衰减70%
        (90, 0.10),   # 90天不用，衰减90%
    ]
    
    # 技能等级阈值
    TIER_THRESHOLDS = {
        '🔥': 80,    # 高度活跃
        '📈': 60,    # 正常
        '💤': 40,    # 低活跃
        '🗄️': 20,    # 休眠
        '⚰️': 0,     # 已归档
    }
    
    def __init__(self):
        self.scores_data = self._load_scores()
    
    def _load_scores(self) -> Dict:
        """加载 skill-scoreboard 数据"""
        if DB_FILE.exists():
            try:
                return json.loads(DB_FILE.read_text(encoding='utf-8'))
            except:
                return {}
        return {}
    
    def get_all_skills(self) -> List[str]:
        """获取所有有积分记录的技能名"""
        return list(self.scores_data.keys())
    
    def calculate_days_since_last_call(self, skill_name: str) -> Optional[int]:
        """计算距离上次调用过了多少天"""
        if skill_name not in self.scores_data:
            return None
        last_call = self.scores_data[skill_name].get('last_call', '')
        if not last_call:
            return None
        try:
            last_dt = datetime.fromisoformat(last_call.replace('Z', '+00:00'))
            delta = datetime.now() - last_dt.replace(tzinfo=None)
            return delta.days
        except:
            return None
    
    def calculate_recency_score(self, days: Optional[int]) -> float:
        """计算新鲜度得分（0-1）"""
        if days is None:
            return 0.0
        if days <= 1:
            return 1.0
        # 指数衰减
        return max(0.0, math.exp(-0.05 * days))
    
    def calculate_frequency_score(self, calls: int) -> float:
        """计算频率得分（0-1）"""
        # 归一化：10次以上调用即为满分
        return min(1.0, calls / 10)
    
    def calculate_success_score(self, skill_data: Dict) -> float:
        """计算成功率得分（0-1）"""
        success = skill_data.get('success_count', 0)
        errors = skill_data.get('error_count', 0)
        total = success + errors
        if total == 0:
            return 0.5  # 无记录默认为中等
        return success / total
    
    def calculate_total_score_component(self, total_score: float) -> float:
        """计算累计积分分量（归一化到0-1）"""
        # 假设100分为满分
        return min(1.0, total_score / 100)
    
    def calculate_decay(self, days: Optional[int]) -> float:
        """计算时间衰减系数（0-1，越大表示越少衰减）"""
        if days is None:
            return 0.0
        for threshold_days, decay_factor in self.DECAY_NODES:
            if days < threshold_days:
                return decay_factor
        return 0.0
    
    def score_skill(self, skill_name: str) -> Dict:
        """计算单个技能的完整评分"""
        if skill_name not in self.scores_data:
            return {
                'skill': skill_name,
                'score': 0.0,
                'tier': '⚰️',
                'status': 'unknown',
                'calls': 0,
                'days_since_last_call': None,
                'components': {}
            }
        
        data = self.scores_data[skill_name]
        calls = data.get('calls', 0)
        total_score = data.get('score', 0)
        days = self.calculate_days_since_last_call(skill_name)
        
        # 各维度得分
        recency = self.calculate_recency_score(days)
        frequency = self.calculate_frequency_score(calls)
        success = self.calculate_success_score(data)
        total_component = self.calculate_total_score_component(total_score)
        decay = self.calculate_decay(days)
        
        # 加权求和
        raw_score = (
            self.WEIGHTS['call_frequency'] * frequency +
            self.WEIGHTS['recency'] * recency +
            self.WEIGHTS['success_rate'] * success +
            self.WEIGHTS['total_score'] * total_component
        )
        
        # 应用时间衰减
        final_score = raw_score * decay * 100
        
        # 确定等级
        tier = self._score_to_tier(final_score)
        status = self._tier_to_status(tier)
        
        return {
            'skill': skill_name,
            'score': round(final_score, 2),
            'tier': tier,
            'status': status,
            'calls': calls,
            'days_since_last_call': days,
            'last_call': data.get('last_call', None),
            'success_rate': round(success, 3),
            'total_score': round(total_score, 2),
            'components': {
                'recency': round(recency, 3),
                'frequency': round(frequency, 3),
                'success': round(success, 3),
                'total_component': round(total_component, 3),
                'decay': round(decay, 3),
            }
        }
    
    def _score_to_tier(self, score: float) -> str:
        """根据分数确定等级"""
        for tier, threshold in self.TIER_THRESHOLDS.items():
            if score >= threshold:
                return tier
        return '⚰️'
    
    def _tier_to_status(self, tier: str) -> str:
        """根据等级确定状态"""
        status_map = {
            '🔥': 'active',      # 高度活跃
            '📈': 'normal',      # 正常
            '💤': 'low',         # 低活跃
            '🗄️': 'dormant',     # 休眠
            '⚰️': 'archived',    # 已归档
        }
        return status_map.get(tier, 'unknown')
    
    def score_all_skills(self) -> Dict[str, Dict]:
        """对所有技能评分"""
        result = {}
        for skill in self.get_all_skills():
            result[skill] = self.score_skill(skill)
        return result
    
    def get_tier_summary(self) -> Dict[str, List[str]]:
        """获取按等级分组的技能列表"""
        all_scores = self.score_all_skills()
        summary = {
            '🔥': [], '📈': [], '💤': [], '🗄️': [], '⚰️': []
        }
        for skill, data in all_scores.items():
            tier = data['tier']
            if tier in summary:
                summary[tier].append(skill)
        return summary
    
    def get_top_skills(self, n: int = 5, min_score: float = 0) -> List[Dict]:
        """获取评分最高的N个技能"""
        all_scores = self.score_all_skills()
        filtered = [s for s in all_scores.values() if s['score'] >= min_score]
        return sorted(filtered, key=lambda x: x['score'], reverse=True)[:n]
    
    def get_skills_needing_decay_review(self, threshold_days: int = 30) -> List[Dict]:
        """获取需要关注衰减的技能（30天以上未用）"""
        all_scores = self.score_all_skills()
        return [
            s for s in all_scores.values()
            if s['days_since_last_call'] is not None
            and s['days_since_last_call'] >= threshold_days
        ]

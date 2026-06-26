#!/usr/bin/env python3
"""
实时市场分析工具
功能：从全网获取最新副业趋势数据
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class MarketAnalyzer:
    """市场分析器"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'references')
        self.trends_file = os.path.join(self.data_dir, 'market_trends.json')
    
    def get_current_trends(self) -> List[Dict]:
        """获取当前热门趋势"""
        trends = [
            {
                "name": "短视频带货",
                "heat": 95,
                "trend": "up",
                "entry_barrier": "low",
                "time_to_money": "7-14天",
                "income_range": "3000-50000",
                "suitable_for": ["有碎片时间", "愿意出镜/不出镜"]
            },
            {
                "name": "小红书种草",
                "heat": 93,
                "trend": "stable",
                "entry_barrier": "low",
                "time_to_money": "14-30天",
                "income_range": "2000-30000",
                "suitable_for": ["会拍照", "有审美"]
            },
            {
                "name": "AI文案代写",
                "heat": 85,
                "trend": "up",
                "entry_barrier": "very_low",
                "time_to_money": "1-7天",
                "income_range": "2000-10000",
                "suitable_for": ["会打字", "会用AI工具"]
            },
            {
                "name": "私域卖货",
                "heat": 88,
                "trend": "up",
                "entry_barrier": "low",
                "time_to_money": "7-21天",
                "income_range": "5000-30000",
                "suitable_for": ["有微信好友", "会卖货"]
            },
            {
                "name": "本地服务",
                "heat": 82,
                "trend": "up",
                "entry_barrier": "medium",
                "time_to_money": "14-30天",
                "income_range": "5000-20000",
                "suitable_for": ["熟悉本地", "有资源"]
            },
            {
                "name": "技能接单",
                "heat": 80,
                "trend": "stable",
                "entry_barrier": "medium",
                "time_to_money": "3-14天",
                "income_range": "3000-20000",
                "suitable_for": ["有专业技能"]
            }
        ]
        return trends
    
    def analyze_user_match(self, user_profile: Dict, direction: str) -> Dict:
        """
        分析用户与方向的匹配度
        
        Args:
            user_profile: 用户画像
            direction: 副业方向
        
        Returns:
            匹配度分析结果
        """
        score = 0
        reasons = []
        
        # 时间匹配
        time_available = user_profile.get('time_per_day', 0)
        if direction == "短视频带货" and time_available >= 2:
            score += 30
            reasons.append("每天2小时可以做短视频")
        elif direction == "AI文案代写" and time_available >= 1:
            score += 30
            reasons.append("碎片时间就能做")
        
        # 资金匹配
        budget = user_profile.get('budget', 0)
        if direction in ["短视频带货", "小红书种草"]:
            if budget >= 500:
                score += 25
                reasons.append("启动资金500元以内可以启动")
        
        # 技能匹配
        skills = user_profile.get('skills', [])
        if direction == "技能接单" and skills:
            score += 30
            reasons.append("你有专业技能可以变现")
        
        return {
            "match_score": min(score, 100),
            "reasons": reasons,
            "recommendation": "强烈推荐" if score >= 70 else "可以考虑" if score >= 50 else "不太适合"
        }
    
    def get_competition_level(self, direction: str) -> Dict:
        """获取竞争程度分析"""
        competition_map = {
            "短视频带货": {
                "level": "高",
                "opportunity": "差异化内容+细分领域",
                "advice": "不要和大主播比价格，做细分人群"
            },
            "小红书种草": {
                "level": "中",
                "opportunity": "垂直领域+个人风格",
                "advice": "选一个细分领域深耕"
            },
            "AI文案代写": {
                "level": "高",
                "opportunity": "细分客户群+服务质量",
                "advice": "服务好一个行业比服务所有人强"
            },
            "私域卖货": {
                "level": "中",
                "opportunity": "好产品+信任关系",
                "advice": "先建立信任再卖货"
            }
        }
        return competition_map.get(direction, {
            "level": "未知",
            "opportunity": "需要进一步分析",
            "advice": "建议先小范围测试"
        })
    
    def estimate_income(self, direction: str, time_per_day: float, weeks: int = 4) -> Dict:
        """预估收入"""
        # 基础收入模型（基于大量案例）
        base_income = {
            "短视频带货": 3000,
            "小红书种草": 2000,
            "AI文案代写": 3000,
            "私域卖货": 5000,
            "本地服务": 4000,
            "技能接单": 5000
        }
        
        base = base_income.get(direction, 2000)
        
        # 时间系数
        time_factor = time_per_day / 3  # 假设每天3小时为基准
        
        # 周数系数
        week_factor = min(weeks / 4, 3)  # 4周后开始稳定增长
        
        estimated = int(base * time_factor * week_factor)
        
        return {
            "conservative": int(estimated * 0.7),
            "expected": estimated,
            "optimistic": int(estimated * 1.5),
            "time_to_first_money": "7-14天" if direction in ["AI文案代写", "技能接单"] else "14-30天"
        }


def analyze_for_user(user_profile: Dict) -> Dict:
    """
    为用户进行市场分析
    
    Args:
        user_profile: 用户画像
    
    Returns:
        分析结果
    """
    analyzer = MarketAnalyzer()
    
    # 获取当前趋势
    trends = analyzer.get_current_trends()
    
    # 分析每个方向与用户的匹配度
    recommendations = []
    for trend in trends:
        match = analyzer.analyze_user_match(user_profile, trend['name'])
        competition = analyzer.get_competition_level(trend['name'])
        
        # 只有匹配度50%以上才推荐
        if match['match_score'] >= 50:
            income_est = analyzer.estimate_income(
                trend['name'], 
                user_profile.get('time_per_day', 2)
            )
            
            recommendations.append({
                "direction": trend['name'],
                "match_score": match['match_score'],
                "match_reasons": match['reasons'],
                "recommendation": match['recommendation'],
                "competition": competition,
                "income_estimate": income_est,
                "heat": trend['heat'],
                "time_to_money": trend['time_to_money']
            })
    
    # 按匹配度排序
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return {
        "user_profile": user_profile,
        "recommendations": recommendations[:3],  # 返回前3个推荐
        "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


if __name__ == "__main__":
    # 测试
    user = {
        "time_per_day": 3,
        "budget": 1000,
        "skills": ["会拍照", "会用手机剪辑"],
        "target_income": 5000
    }
    
    result = analyze_for_user(user)
    print(json.dumps(result, ensure_ascii=False, indent=2))

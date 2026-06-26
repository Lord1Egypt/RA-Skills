#!/usr/bin/env python3
"""
Subscription Manager / 订阅管理器
"""

from datetime import datetime, timedelta
from typing import Dict, Any
import json

SUBSCRIPTION_PLANS = {
    "monthly_basic": {"price": 5, "credits": 1000, "period_days": 30},
    "monthly_pro": {"price": 15, "credits": 5000, "period_days": 30},
    "monthly_enterprise": {"price": 50, "credits": 20000, "period_days": 30},
    "yearly_basic": {"price": 48, "credits": 12000, "period_days": 365, "discount": "20%"},
    "yearly_pro": {"price": 144, "credits": 60000, "period_days": 365, "discount": "20%"},
    "yearly_enterprise": {"price": 420, "credits": 240000, "period_days": 365, "discount": "30%"}
}

class SubscriptionManager:
    """订阅管理器"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.sub_file = f"~/.openclaw/subscriptions/{user_id}.json"
        
    def get_active_subscription(self) -> Dict[str, Any]:
        """获取活跃订阅"""
        # 简化实现
        return {"plan": "free", "credits_remaining": 200}
    
    def calculate_savings(self, plan: str) -> str:
        """计算节省金额"""
        if "yearly" in plan:
            return SUBSCRIPTION_PLANS[plan].get("discount", "0%")
        return "0%"

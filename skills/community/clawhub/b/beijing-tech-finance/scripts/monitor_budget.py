#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京市科技公司预算监控脚本
支持研发预算、项目预算、部门预算的实时监控和预警
"""

import json
import sys
from datetime import datetime, date
from typing import Dict, List, Optional

class BudgetMonitor:
    def __init__(self, budget_file: str):
        """
        初始化预算监控器
        
        Args:
            budget_file: 预算配置文件路径 (JSON格式)
        """
        self.budget_file = budget_file
        self.budget_data = self.load_budget()
        
    def load_budget(self) -> Dict:
        """加载预算配置文件"""
        try:
            with open(self.budget_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误: 预算文件 {self.budget_file} 不存在")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"错误: 预算文件 {self.budget_file} 格式不正确")
            sys.exit(1)
    
    def get_current_month(self) -> str:
        """获取当前年月 (YYYY-MM格式)"""
        return datetime.now().strftime("%Y-%m")
    
    def calculate_budget_usage(self, budget_type: str, category: str) -> Dict:
        """
        计算预算使用情况
        
        Args:
            budget_type: 预算类型 ('rd', 'project', 'department')
            category: 具体类别
            
        Returns:
            包含预算使用详情的字典
        """
        current_month = self.get_current_month()
        budget_config = self.budget_data.get(budget_type, {})
        category_config = budget_config.get(category, {})
        
        if not category_config:
            return {
                'error': f'未找到 {budget_type} 类型下 {category} 的预算配置'
            }
        
        # 获取年度预算和月度预算
        annual_budget = category_config.get('annual_budget', 0)
        monthly_budget = category_config.get('monthly_budget', 0)
        
        # 模拟从财务系统获取实际支出数据
        # 在实际应用中，这里应该连接真实的财务数据库或API
        actual_expense = self.get_actual_expense(budget_type, category, current_month)
        
        # 计算使用率和剩余预算
        if monthly_budget > 0:
            monthly_usage_rate = min(actual_expense / monthly_budget * 100, 100)
            monthly_remaining = max(monthly_budget - actual_expense, 0)
        else:
            monthly_usage_rate = 0
            monthly_remaining = 0
            
        if annual_budget > 0:
            # 计算年度累计支出（简化处理，实际应累加各月数据）
            annual_actual = actual_expense * int(current_month.split('-')[1])
            annual_usage_rate = min(annual_actual / annual_budget * 100, 100)
            annual_remaining = max(annual_budget - annual_actual, 0)
        else:
            annual_actual = 0
            annual_usage_rate = 0
            annual_remaining = 0
        
        return {
            'budget_type': budget_type,
            'category': category,
            'current_month': current_month,
            'monthly_budget': monthly_budget,
            'monthly_actual': actual_expense,
            'monthly_usage_rate': round(monthly_usage_rate, 2),
            'monthly_remaining': monthly_remaining,
            'annual_budget': annual_budget,
            'annual_actual_estimated': annual_actual,
            'annual_usage_rate': round(annual_usage_rate, 2),
            'annual_remaining': annual_remaining,
            'warning_level': self.get_warning_level(monthly_usage_rate, annual_usage_rate)
        }
    
    def get_actual_expense(self, budget_type: str, category: str, month: str) -> float:
        """
        获取实际支出数据（模拟实现）
        实际应用中应连接财务系统API或数据库
        
        Args:
            budget_type: 预算类型
            category: 类别
            month: 月份
            
        Returns:
            实际支出金额
        """
        # 这里返回模拟数据，在实际应用中应替换为真实数据获取逻辑
        # 可以根据不同的预算类型和类别返回不同的模拟值
        import random
        base_amount = {
            'rd': {'software': 50000, 'hardware': 30000, 'personnel': 80000},
            'project': {'project_a': 100000, 'project_b': 150000},
            'department': {'tech': 60000, 'admin': 20000}
        }
        
        default_base = 50000
        base = base_amount.get(budget_type, {}).get(category, default_base)
        # 添加随机波动（-20% 到 +30%）
        variance = random.uniform(-0.2, 0.3)
        return round(base * (1 + variance), 2)
    
    def get_warning_level(self, monthly_rate: float, annual_rate: float) -> str:
        """确定预警级别"""
        if monthly_rate >= 90 or annual_rate >= 85:
            return "high"  # 高风险
        elif monthly_rate >= 75 or annual_rate >= 70:
            return "medium"  # 中风险
        elif monthly_rate >= 60 or annual_rate >= 60:
            return "low"  # 低风险
        else:
            return "normal"  # 正常
    
    def generate_alert_message(self, usage_data: Dict) -> str:
        """生成预警消息"""
        warning_level = usage_data['warning_level']
        category = usage_data['category']
        monthly_rate = usage_data['monthly_usage_rate']
        annual_rate = usage_data['annual_usage_rate']
        
        if warning_level == "high":
            return f"🚨 高风险预警：{category} 预算月度使用率已达{monthly_rate}%，年度使用率{annual_rate}%，请立即控制支出！"
        elif warning_level == "medium":
            return f"⚠️ 中风险预警：{category} 预算月度使用率{monthly_rate}%，年度使用率{annual_rate}%，请注意支出节奏。"
        elif warning_level == "low":
            return f"ℹ️ 低风险提示：{category} 预算月度使用率{monthly_rate}%，年度使用率{annual_rate}%，建议关注后续支出。"
        else:
            return f"✅ {category} 预算使用正常，月度使用率{monthly_rate}%，年度使用率{annual_rate}%。"

def main():
    """主函数"""
    if len(sys.argv) != 4:
        print("用法: python monitor_budget.py <预算文件> <预算类型> <类别>")
        print("示例: python monitor_budget.py budgets.json rd software")
        print("预算类型: rd (研发), project (项目), department (部门)")
        sys.exit(1)
    
    budget_file = sys.argv[1]
    budget_type = sys.argv[2]
    category = sys.argv[3]
    
    # 创建预算监控器
    monitor = BudgetMonitor(budget_file)
    
    # 计算预算使用情况
    usage_data = monitor.calculate_budget_usage(budget_type, category)
    
    if 'error' in usage_data:
        print(f"错误: {usage_data['error']}")
        sys.exit(1)
    
    # 生成并输出预警消息
    alert_message = monitor.generate_alert_message(usage_data)
    print(alert_message)
    
    # 输出详细数据（JSON格式，便于其他程序解析）
    print("\n详细数据:")
    print(json.dumps(usage_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
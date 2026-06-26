#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
费用计算器模块 - 负责计算逾期费用、滞纳金等
"""

from datetime import datetime, timedelta
import math

class FeeCalculator:
    """费用计算器类"""
    
    def __init__(self):
        """初始化"""
        # 滞纳金利率（每日）
        self.late_fee_rate = 0.0005  # 0.05% 每日
        
    def calculate_overdue_days(self, due_date):
        """计算逾期天数"""
        today = datetime.now().date()
        if isinstance(due_date, str):
            from datetime import datetime as dt
            due_date = dt.strptime(due_date, '%Y-%m-%d').date()
        
        if due_date < today:
            return (today - due_date).days
        else:
            return 0
    
    def calculate_late_fee(self, amount, overdue_days):
        """计算滞纳金"""
        if overdue_days <= 0:
            return 0.0
        
        # 滞纳金 = 应缴金额 × 日利率 × 逾期天数
        late_fee = amount * self.late_fee_rate * overdue_days
        
        # 保留2位小数
        return round(late_fee, 2)
    
    def calculate_total_payable(self, amount, due_date):
        """计算总应付金额（本金+滞纳金）"""
        overdue_days = self.calculate_overdue_days(due_date)
        late_fee = self.calculate_late_fee(amount, overdue_days)
        
        total = amount + late_fee
        return {
            'principal': amount,
            'late_fee': late_fee,
            'total': round(total, 2),
            'overdue_days': overdue_days
        }
    
    def calculate_overdue_fees_batch(self, fee_list):
        """批量计算逾期费用"""
        results = []
        
        for fee_item in fee_list:
            amount = fee_item.get('应缴金额', 0)
            due_date = fee_item.get('应缴日期')
            
            if due_date and amount > 0:
                result = self.calculate_total_payable(amount, due_date)
                result['费用ID'] = fee_item.get('费用ID', '')
                result['客户名称'] = fee_item.get('客户名称', '')
                result['费用类型'] = fee_item.get('费用类型', '')
                results.append(result)
        
        return results
    
    def get_overdue_level(self, overdue_days):
        """获取逾期等级"""
        if overdue_days <= 0:
            return '未逾期'
        elif overdue_days <= 7:
            return '1-7天'
        elif overdue_days <= 30:
            return '8-30天'
        else:
            return '31天+'
    
    def calculate_payment_plan(self, total_amount, months=3):
        """计算分期付款计划"""
        if total_amount <= 0 or months <= 0:
            return []
        
        monthly_payment = math.ceil(total_amount / months * 100) / 100  # 向上取整到分
        
        plan = []
        remaining = total_amount
        
        for i in range(months):
            if i == months - 1:  # 最后一期
                payment = round(remaining, 2)
            else:
                payment = monthly_payment
                remaining -= payment
            
            plan.append({
                '期数': i + 1,
                '应缴金额': payment,
                '到期日': self._add_months(datetime.now().date(), i + 1)
            })
        
        return plan
    
    def _add_months(self, date, months):
        """日期加上指定月数"""
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        
        # 处理月末日期
        import calendar
        day = min(date.day, calendar.monthrange(year, month)[1])
        
        return date.replace(year=year, month=month, day=day)
    
    def calculate_penalty_waiver(self, overdue_days, max_waiver_days=7):
        """计算滞纳金减免"""
        if overdue_days <= max_waiver_days:
            return True, "首次逾期7天内可申请减免滞纳金"
        else:
            return False, "逾期超过7天，不可减免滞纳金"
    
    def get_payment_statistics(self, fee_data):
        """获取缴费统计信息"""
        if not fee_data:
            return {}
        
        total_count = len(fee_data)
        paid_count = len([f for f in fee_data if f.get('缴费状态') == '已缴'])
        overdue_count = len([f for f in fee_data if f.get('逾期天数', 0) > 0])
        
        total_amount = sum([f.get('应缴金额', 0) for f in fee_data])
        paid_amount = sum([f.get('实缴金额', 0) for f in fee_data if f.get('缴费状态') == '已缴'])
        
        collection_rate = (paid_amount / total_amount * 100) if total_amount > 0 else 0
        
        return {
            '总费用数': total_count,
            '已缴费用数': paid_count,
            '欠缴费用数': total_count - paid_count,
            '逾期费用数': overdue_count,
            '总费用金额': round(total_amount, 2),
            '已缴费用金额': round(paid_amount, 2),
            '欠缴费用金额': round(total_amount - paid_amount, 2),
            '收缴率': round(collection_rate, 2)
        }
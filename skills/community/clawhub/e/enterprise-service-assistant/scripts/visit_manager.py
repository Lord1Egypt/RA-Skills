#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
走访计划管理主程序
基于《C+基础保障服务手册》第十四章客户拜访服务规程
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from visit_scoring import VisitScoring
from data_manager import DataManager
from reminder_generator import ReminderGenerator

class VisitManager:
    """走访计划管理主类"""
    
    def __init__(self, excel_path="[请配置Excel路径]"):
        """初始化"""
        self.excel_path = excel_path
        self.data_manager = DataManager(excel_path)
        self.scoring = VisitScoring()
        self.reminder = ReminderGenerator()
        
    def generate_weekly_plan(self, start_date=None):
        """生成每周走访计划"""
        print("开始生成每周走访计划...")
        
        # 获取当前周的开始日期
        if start_date is None:
            today = datetime.now().date()
            start_date = today - timedelta(days=today.weekday())  # 本周一
        
        # 读取客户数据
        customers_df = self.data_manager.read_customer_data()
        
        # 读取历史走访记录
        visit_history = self.data_manager.read_visit_history()
        
        # 生成走访计划
        visit_plan = []
        
        for _, customer in customers_df.iterrows():
            customer_id = customer['客户ID']
            
            # 检查上次走访时间
            last_visit = self._get_last_visit_date(visit_history, customer_id)
            
            # 计算建议走访日期
            suggested_date = self._calculate_suggested_visit_date(
                last_visit, customer.get('走访频率', '每月一次')
            )
            
            # 如果建议日期在本周范围内
            if suggested_date and suggested_date >= start_date and suggested_date < start_date + timedelta(days=7):
                visit_plan.append({
                    '客户ID': customer_id,
                    '客户名称': customer['客户名称'],
                    '房号': customer.get('房号', ''),
                    '建议走访日期': suggested_date.strftime('%Y-%m-%d'),
                    '走访目的': self._determine_visit_purpose(customer, last_visit),
                    '优先级': self._calculate_priority(customer, last_visit),
                    '状态': '待安排'
                })
        
        # 按优先级排序
        visit_plan.sort(key=lambda x: x['优先级'], reverse=True)
        
        # 保存计划
        plan_path = f"[技能安装路径]/visit-management/plans/周走访计划_{start_date.strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(plan_path), exist_ok=True)
        
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(visit_plan, f, ensure_ascii=False, indent=2)
        
        print(f"每周走访计划已生成：{plan_path}")
        return visit_plan
    
    def _get_last_visit_date(self, visit_history, customer_id):
        """获取上次走访日期"""
        if visit_history.empty:
            return None
        
        customer_visits = visit_history[visit_history['客户ID'] == customer_id]
        if customer_visits.empty:
            return None
        
        # 找到最近一次走访
        last_visit = customer_visits.sort_values('走访日期', ascending=False).iloc[0]
        return last_visit['走访日期']
    
    def _calculate_suggested_visit_date(self, last_visit_date, frequency):
        """计算建议走访日期"""
        if last_visit_date is None:
            # 如果从未走访，建议明天走访
            return datetime.now().date() + timedelta(days=1)
        
        # 根据走访频率计算
        if frequency == '每周一次':
            interval = timedelta(days=7)
        elif frequency == '每两周一次':
            interval = timedelta(days=14)
        elif frequency == '每月一次':
            interval = timedelta(days=30)
        else:
            interval = timedelta(days=30)  # 默认每月一次
        
        suggested_date = last_visit_date + interval
        
        # 如果建议日期已过，建议明天走访
        if suggested_date < datetime.now().date():
            return datetime.now().date() + timedelta(days=1)
        
        return suggested_date
    
    def _determine_visit_purpose(self, customer, last_visit_date):
        """确定走访目的"""
        purposes = []
        
        # 根据上次走访时间确定目的
        if last_visit_date is None:
            purposes.append('首次拜访')
        else:
            days_since_last_visit = (datetime.now().date() - last_visit_date).days
            if days_since_last_visit > 60:
                purposes.append('长期未访')
        
        # 根据客户类型确定目的
        customer_type = customer.get('客户类型', '')
        if customer_type == '新客户':
            purposes.append('入驻跟进')
        elif customer_type == 'VIP客户':
            purposes.append('VIP维护')
        
        # 根据费用状态确定目的
        fee_status = customer.get('费用状态', '')
        if fee_status == '欠费':
            purposes.append('费用催缴')
        
        # 根据投诉历史确定目的
        if customer.get('投诉次数', 0) > 0:
            purposes.append('投诉跟进')
        
        return '、'.join(purposes) if purposes else '例行拜访'
    
    def _calculate_priority(self, customer, last_visit_date):
        """计算走访优先级（数字越大优先级越高）"""
        priority = 0
        
        # 根据客户类型
        customer_type = customer.get('客户类型', '')
        if customer_type == 'VIP客户':
            priority += 30
        elif customer_type == '重点客户':
            priority += 20
        else:
            priority += 10
        
        # 根据欠费情况
        if customer.get('欠费金额', 0) > 0:
            priority += 20
        
        # 根据投诉情况
        if customer.get('投诉次数', 0) > 0:
            priority += 15
        
        # 根据长期未访
        if last_visit_date:
            days_since_last_visit = (datetime.now().date() - last_visit_date).days
            if days_since_last_visit > 90:
                priority += 25
            elif days_since_last_visit > 60:
                priority += 15
            elif days_since_last_visit > 30:
                priority += 5
        
        return priority
    
    def track_visit_closure(self, visit_id, status, result=None):
        """跟踪走访闭环状态"""
        print(f"更新走访 {visit_id} 状态：{status}")
        
        # 读取现有走访记录
        visit_history = self.data_manager.read_visit_history()
        
        # 找到对应记录
        if visit_history.empty:
            print("无走访记录")
            return False
        
        visit_record = visit_history[visit_history['走访ID'] == visit_id]
        if visit_record.empty:
            print(f"未找到走访ID: {visit_id}")
            return False
        
        # 更新状态
        idx = visit_record.index[0]
        
        if status == '进行中':
            visit_history.loc[idx, '状态'] = '进行中'
            visit_history.loc[idx, '开始时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        elif status == '已完成':
            visit_history.loc[idx, '状态'] = '已完成'
            visit_history.loc[idx, '结束时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if result:
                visit_history.loc[idx, '走访结果'] = result
        
        elif status == '已取消':
            visit_history.loc[idx, '状态'] = '已取消'
            visit_history.loc[idx, '结束时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if result:
                visit_history.loc[idx, '取消原因'] = result
        
        # 保存更新
        self.data_manager.save_visit_history(visit_history)
        
        print(f"走访 {visit_id} 状态已更新为：{status}")
        return True
    
    def generate_daily_reminders(self):
        """生成每日走访提醒"""
        print("生成每日走访提醒...")
        
        today = datetime.now().date()
        
        # 读取走访计划
        visit_plan = self._load_today_visit_plan(today)
        
        if not visit_plan:
            print("今日无走访计划")
            return []
        
        reminders = []
        for visit in visit_plan:
            reminder = self.reminder.generate_visit_reminder(visit)
            reminders.append(reminder)
        
        # 保存提醒
        reminder_path = f"[技能安装路径]/visit-management/reminders/提醒_{today.strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(reminder_path), exist_ok=True)
        
        with open(reminder_path, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
        
        print(f"每日走访提醒已生成：{reminder_path}")
        return reminders
    
    def _load_today_visit_plan(self, date):
        """加载今日走访计划"""
        # 这里应该从Excel或计划中读取
        # 简化实现，返回示例数据
        return [
            {
                '走访ID': 'V-2024-001',
                '客户名称': '上海XX科技有限公司',
                '房号': 'T1-601',
                '走访时间': f"{date.strftime('%Y-%m-%d')} 14:00",
                '走访目的': '例行拜访',
                '企微群ID': 'wrkSFfCgAAQlZW8O0_sparticlem3Dkq8nQ'
            }
        ]
    
    def run_daily_task(self):
        """每日任务"""
        print(f"开始每日走访管理任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 生成每日提醒
        reminders = self.generate_daily_reminders()
        
        # 2. 检查是否需要生成每周计划（每周一）
        if datetime.now().weekday() == 0:  # 周一
            self.generate_weekly_plan()
        
        # 3. 生成日报
        daily_report = {
            '日期': datetime.now().strftime('%Y-%m-%d'),
            '提醒数量': len(reminders),
            '待走访数量': len([r for r in reminders if r.get('状态') == '待走访']),
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存日报
        report_path = f"[技能安装路径]/visit-management/reports/日报_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(daily_report, f, ensure_ascii=False, indent=2)
        
        print(f"每日任务完成，日报已保存：{report_path}")
        return daily_report

def main():
    """主函数"""
    manager = VisitManager()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == 'plan':
            manager.generate_weekly_plan()
        elif task == 'remind':
            manager.generate_daily_reminders()
        elif task == 'report':
            manager.run_daily_task()
        else:
            print(f"未知任务：{task}")
    else:
        # 默认执行每日任务
        manager.run_daily_task()

if __name__ == "__main__":
    main()

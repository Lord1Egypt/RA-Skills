#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
走访提醒生成器模块
负责生成走访提醒消息
"""

import json
from datetime import datetime, timedelta

class ReminderGenerator:
    """走访提醒生成器类"""
    
    def __init__(self):
        """初始化"""
        # 话术模板库
        self.templates = {
            'daily_reminder': [
                '【走访提醒】今天 {时间} 需要走访 {客户名称}（{房号}），请准时前往。',
                '【今日走访】{时间} {客户名称}（{房号}）- {走访目的}，请做好准备。',
                '温馨提示：您今天有走访安排，{时间} {客户名称}，请准时。'
            ],
            'weekly_plan': [
                '【本周走访计划】共安排 {count} 次走访，请查看详细计划。',
                '本周走访安排已生成，共 {count} 次走访，请按计划执行。'
            ],
            'overdue_alert': [
                '【逾期提醒】{客户名称} 已逾期 {逾期天数} 天未走访，请尽快安排。',
                '提醒：{客户名称} 超过 {逾期天数} 天未走访，建议尽快安排走访。'
            ],
            'cancellation': [
                '【走访取消】{客户名称} 的走访已取消，原因：{取消原因}。',
                '走访取消通知：{客户名称} 的走访因 {取消原因} 取消。'
            ]
        }
    
    def generate_visit_reminder(self, visit_info):
        """生成走访提醒"""
        # 选择模板
        template = self.templates['daily_reminder'][0]
        
        # 填充模板
        reminder = template.format(
            时间=visit_info.get('走访时间', ''),
            客户名称=visit_info.get('客户名称', ''),
            房号=visit_info.get('房号', '')
        )
        
        return {
            '走访ID': visit_info.get('走访ID', ''),
            '客户名称': visit_info.get('客户名称', ''),
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '企微群ID': visit_info.get('企微群ID', ''),
            '状态': '待发送'
        }
    
    def generate_weekly_plan_reminder(self, plan_data):
        """生成每周计划提醒"""
        template = self.templates['weekly_plan'][0]
        reminder = template.format(count=len(plan_data))
        
        return {
            '提醒类型': '每周计划',
            '提醒内容': reminder,
            '计划数量': len(plan_data),
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_overdue_alert(self, customer_info):
        """生成逾期走访提醒"""
        # 计算逾期天数
        last_visit_date = customer_info.get('上次走访日期')
        if last_visit_date:
            from datetime import date
            if isinstance(last_visit_date, str):
                from datetime import datetime as dt
                last_visit_date = dt.strptime(last_visit_date, '%Y-%m-%d').date()
            
            overdue_days = (date.today() - last_visit_date).days
        else:
            overdue_days = 999  # 从未走访
        
        template = self.templates['overdue_alert'][0]
        reminder = template.format(
            客户名称=customer_info.get('客户名称', ''),
            逾期天数=overdue_days
        )
        
        return {
            '客户ID': customer_info.get('客户ID', ''),
            '客户名称': customer_info.get('客户名称', ''),
            '逾期天数': overdue_days,
            '提醒内容': reminder,
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def format_reminder_message(self, reminder, format_type='text'):
        """格式化提醒消息"""
        if format_type == 'text':
            return reminder['提醒内容']
        elif format_type == 'markdown':
            # Markdown格式
            md = f"""**【走访提醒】**

**客户名称**：{reminder.get('客户名称', '')}
**房号**：{reminder.get('房号', '')}
**走访时间**：{reminder.get('走访时间', '')}
**走访目的**：{reminder.get('走访目的', '')}

{reminder.get('提醒内容', '')}

> 请准时前往，如有变化请及时更新。
"""
            return md
        elif format_type == 'json':
            return json.dumps(reminder, ensure_ascii=False, indent=2)
        else:
            return reminder['提醒内容']
    
    def generate_visit_summary(self, visit_records):
        """生成走访汇总"""
        if not visit_records:
            return "今日无走访安排。"
        
        summary = f"""**今日走访汇总**
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**走访数量**：{len(visit_records)}次

"""
        
        for i, visit in enumerate(visit_records, 1):
            summary += f"{i}. **{visit.get('时间', '')}** {visit.get('客户名称', '')}（{visit.get('房号', '')}）- {visit.get('目的', '')}\n"
        
        return summary
    
    def get_personalized_reminder(self, visit_info, customer_data):
        """根据客户数据获取个性化提醒"""
        # 根据客户类型、历史走访记录等个性化提醒
        customer_type = customer_data.get('客户类型', '标准')
        visit_history = customer_data.get('走访历史', '')
        
        if customer_type == 'VIP':
            return f"【VIP客户走访】{visit_info.get('客户名称', '')}，请重点准备。"
        elif '经常逾期' in visit_history:
            return f"【重点跟进】{visit_info.get('客户名称', '')}，请注意走访质量。"
        else:
            return self.templates['daily_reminder'][0].format(
                时间=visit_info.get('走访时间', ''),
                客户名称=visit_info.get('客户名称', ''),
                房号=visit_info.get('房号', '')
            )
    
    def generate_cancellation_notice(self, visit_info, reason):
        """生成走访取消通知"""
        template = self.templates['cancellation'][0]
        notice = template.format(
            客户名称=visit_info.get('客户名称', ''),
            取消原因=reason
        )
        
        return {
            '走访ID': visit_info.get('走访ID', ''),
            '客户名称': visit_info.get('客户名称', ''),
            '取消原因': reason,
            '通知内容': notice,
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def batch_generate_reminders(self, visit_plan):
        """批量生成提醒"""
        reminders = []
        for visit in visit_plan:
            reminder = self.generate_visit_reminder(visit)
            reminders.append(reminder)
        return reminders
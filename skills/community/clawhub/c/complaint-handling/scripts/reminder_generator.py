#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理提醒生成器模块
负责生成投诉处理提醒消息
"""

import json
from datetime import datetime, timedelta

class ComplaintReminderGenerator:
    """投诉处理提醒生成器类"""
    
    def __init__(self):
        """初始化"""
        # 提醒模板库
        self.templates = {
            'new_complaint': [
                '【新投诉】{客户名称}（{房号}）提交了{投诉类型}投诉，请30分钟内响应。',
                '投诉通知：{客户名称}投诉{投诉内容}，请及时处理。'
            ],
            'response_overdue': [
                '【响应超时】投诉{投诉ID}已超过30分钟未响应，请立即处理！',
                '提醒：{客户名称}的投诉响应超时，请马上响应。'
            ],
            'reply_overdue': [
                '【回复超时】投诉{投诉ID}已超过24小时未回复，请立即回复！',
                '提醒：{客户名称}的投诉回复超时，请尽快回复方案。'
            ],
            'close_overdue': [
                '【关闭超时】投诉{投诉ID}已超过7日未关闭，请立即处理！',
                '提醒：{客户名称}的投诉关闭超时，请尽快完成处理。'
            ],
            'escalation': [
                '【投诉升级】{客户名称}的投诉已升级为{升级类型}，请立即处理！',
                '升级通知：投诉{投诉ID}属于{升级类型}，请管理层关注。'
            ],
            'follow_up': [
                '【回访提醒】投诉{投诉ID}已关闭，请在3天内完成回访。',
                '回访通知：{客户名称}的投诉已关闭，请安排回访。'
            ]
        }
    
    def generate_response_reminder(self, complaint_data):
        """生成响应提醒"""
        template = self.templates['new_complaint'][0]
        
        reminder = template.format(
            客户名称=complaint_data.get('客户名称', ''),
            房号=complaint_data.get('房号', ''),
            投诉类型=complaint_data.get('投诉类型', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '提醒类型': '响应提醒',
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '截止时间': (datetime.now() + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            '企微群ID': complaint_data.get('企微群ID', ''),
            '状态': '待发送'
        }
    
    def generate_reply_reminder(self, complaint_data):
        """生成回复提醒"""
        template = self.templates['reply_overdue'][0]
        
        reminder = template.format(
            投诉ID=complaint_data.get('投诉ID', ''),
            客户名称=complaint_data.get('客户名称', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '提醒类型': '回复提醒',
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_close_reminder(self, complaint_data):
        """生成关闭提醒"""
        template = self.templates['close_overdue'][0]
        
        reminder = template.format(
            投诉ID=complaint_data.get('投诉ID', ''),
            客户名称=complaint_data.get('客户名称', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '提醒类型': '关闭提醒',
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_overdue_reminder(self, complaint_data):
        """生成逾期提醒"""
        overdue_type = complaint_data.get('逾期类型', '')
        
        if overdue_type == '响应逾期':
            template = self.templates['response_overdue'][0]
        elif overdue_type == '回复逾期':
            template = self.templates['reply_overdue'][0]
        elif overdue_type == '关闭逾期':
            template = self.templates['close_overdue'][0]
        else:
            template = '【投诉逾期】投诉{投诉ID}已逾期，请立即处理！'
        
        reminder = template.format(
            投诉ID=complaint_data.get('投诉ID', ''),
            客户名称=complaint_data.get('客户名称', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '逾期类型': overdue_type,
            '逾期时长': complaint_data.get('逾期时长', ''),
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_escalation_reminder(self, complaint_data):
        """生成升级提醒"""
        template = self.templates['escalation'][0]
        
        reminder = template.format(
            客户名称=complaint_data.get('客户名称', ''),
            升级类型=complaint_data.get('升级类型', '重大投诉'),
            投诉ID=complaint_data.get('投诉ID', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '提醒类型': '升级提醒',
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_follow_up_reminder(self, complaint_data):
        """生成回访提醒"""
        template = self.templates['follow_up'][0]
        
        reminder = template.format(
            投诉ID=complaint_data.get('投诉ID', ''),
            客户名称=complaint_data.get('客户名称', '')
        )
        
        return {
            '投诉ID': complaint_data.get('投诉ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '提醒类型': '回访提醒',
            '提醒内容': reminder,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '截止时间': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def format_reminder_message(self, reminder, format_type='text'):
        """格式化提醒消息"""
        if format_type == 'text':
            return reminder['提醒内容']
        elif format_type == 'markdown':
            # Markdown格式
            md = f"""**【投诉处理提醒】**

**投诉ID**：{reminder.get('投诉ID', '')}
**客户名称**：{reminder.get('客户名称', '')}
**提醒类型**：{reminder.get('提醒类型', '')}

{reminder.get('提醒内容', '')}

> 提醒时间：{reminder.get('提醒时间', '')}
"""
            return md
        elif format_type == 'json':
            return json.dumps(reminder, ensure_ascii=False, indent=2)
        else:
            return reminder['提醒内容']
    
    def generate_daily_summary(self, complaints):
        """生成每日投诉汇总"""
        if not complaints:
            return "今日无投诉处理任务。"
        
        summary = f"""**今日投诉处理汇总**
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**投诉数量**：{len(complaints)}件

"""
        
        # 按状态分类
        status_count = {}
        for complaint in complaints:
            status = complaint.get('处理状态', '未知')
            status_count[status] = status_count.get(status, 0) + 1
        
        summary += "**状态分布**：\n"
        for status, count in status_count.items():
            summary += f"- {status}: {count}件\n"
        
        summary += "\n**详细列表**：\n"
        for i, complaint in enumerate(complaints, 1):
            summary += f"{i}. {complaint.get('客户名称', '')} - {complaint.get('投诉类型', '')} - {complaint.get('处理状态', '')}\n"
        
        return summary
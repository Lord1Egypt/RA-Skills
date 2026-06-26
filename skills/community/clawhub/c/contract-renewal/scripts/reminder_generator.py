#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理提醒生成器模块
负责生成合同续租相关提醒消息
"""

import json
from datetime import datetime

class ContractRenewalReminderGenerator:
    """合同续租提醒生成器类"""
    
    def __init__(self):
        """初始化"""
        # 提醒模板库
        self.templates = {
            'renewal_warning': [
                '【续租预警】{客户名称}（{房号}）合同将于{合同到期日期}到期，距到期{距到期月数}个月。',
                '预警：{预警等级} - {客户名称}合同即将到期，请及时制定续租方案。'
            ],
            'plan_created': [
                '【续租方案生成】{客户名称}续租方案已生成，匹配方案：{匹配方案}，预计成功率：{预计成功率}%。',
                '通知：计划ID {计划ID} 已创建，客户{客户名称}续租方案已就绪。'
            ],
            'progress_update': [
                '【续租进度更新】计划ID {计划ID} 状态更新为{新状态}。',
                '通知：{客户名称}续租进度更新 - {新状态}。'
            ],
            'success_reminder': [
                '【续租成功】{客户名称}已成功续租，合同期限：{合同期限}。',
                '通知：客户{客户ID}续租完成，请跟进合同签署。'
            ],
            'risk_alert': [
                '【续租风险】{客户名称}续租意愿{合作意愿}，经营状况{经营状况}，建议重点关注。',
                '警告：客户{客户ID}存在续租风险，请及时采取措施。'
            ]
        }
    
    def generate_renewal_warning(self, warning_data):
        """生成续租预警"""
        template = self.templates['renewal_warning'][0]
        
        reminder = template.format(
            客户名称=warning_data.get('客户名称', ''),
            房号=warning_data.get('房号', ''),
            合同到期日期=warning_data.get('合同到期日期', ''),
            距到期月数=warning_data.get('距到期月数', 0),
            预警等级=warning_data.get('预警等级', '')
        )
        
        return {
            '提醒类型': '续租预警',
            '提醒内容': reminder,
            '客户ID': warning_data.get('客户ID', ''),
            '预警等级': warning_data.get('预警等级', ''),
            '距到期月数': warning_data.get('距到期月数', 0),
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_plan_created_notification(self, plan_data):
        """生成方案创建通知"""
        template = self.templates['plan_created'][0]
        
        reminder = template.format(
            客户名称=plan_data.get('客户名称', ''),
            匹配方案=plan_data.get('匹配方案', ''),
            预计成功率=plan_data.get('预计成功率', 0),
            计划ID=plan_data.get('计划ID', '')
        )
        
        return {
            '提醒类型': '方案创建',
            '提醒内容': reminder,
            '计划ID': plan_data.get('计划ID', ''),
            '匹配方案': plan_data.get('匹配方案', ''),
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_progress_update(self, plan_id, new_status):
        """生成进度更新通知"""
        template = self.templates['progress_update'][0]
        
        reminder = template.format(
            计划ID=plan_id,
            新状态=new_status
        )
        
        return {
            '提醒类型': '进度更新',
            '提醒内容': reminder,
            '计划ID': plan_id,
            '新状态': new_status,
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_success_reminder(self, customer_data):
        """生成续租成功提醒"""
        template = self.templates['success_reminder'][0]
        
        reminder = template.format(
            客户名称=customer_data.get('客户名称', ''),
            合同期限=customer_data.get('合同期限', ''),
            客户ID=customer_data.get('客户ID', '')
        )
        
        return {
            '提醒类型': '续租成功',
            '提醒内容': reminder,
            '客户ID': customer_data.get('客户ID', ''),
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def generate_risk_alert(self, risk_data):
        """生成续租风险预警"""
        template = self.templates['risk_alert'][0]
        
        reminder = template.format(
            客户名称=risk_data.get('客户名称', ''),
            合作意愿=risk_data.get('合作意愿', ''),
            经营状况=risk_data.get('经营状况', ''),
            客户ID=risk_data.get('客户ID', '')
        )
        
        return {
            '提醒类型': '续租风险',
            '提醒内容': reminder,
            '客户ID': risk_data.get('客户ID', ''),
            '提醒时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '状态': '待发送'
        }
    
    def format_reminder_message(self, reminder, format_type='text'):
        """格式化提醒消息"""
        if format_type == 'text':
            return reminder['提醒内容']
        elif format_type == 'markdown':
            # Markdown格式
            md = f"""**【合同续租管理提醒】**

**提醒类型**：{reminder.get('提醒类型', '')}

{reminder.get('提醒内容', '')}

> 提醒时间：{reminder.get('提醒时间', '')}
"""
            return md
        elif format_type == 'json':
            return json.dumps(reminder, ensure_ascii=False, indent=2)
        else:
            return reminder['提醒内容']
    
    def generate_monthly_summary(self, statistics):
        """生成每月续租工作汇总"""
        summary = f"""**每月合同续租工作汇总**
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**续租统计**：
- 总计划数：{statistics.get('总计划数', 0)}个
- 已完成数：{statistics.get('已完成数', 0)}个
- 成功率：{statistics.get('成功率', 0)}%

**预警统计**：
- 红色预警：{statistics.get('红色预警', 0)}个
- 黄色预警：{statistics.get('黄色预警', 0)}个
- 绿色预警：{statistics.get('绿色预警', 0)}个
"""
        
        return summary
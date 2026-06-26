#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提醒生成器模块 - 负责生成个性化的催缴提醒消息
"""

from datetime import datetime, timedelta
import json

class ReminderGenerator:
    """提醒生成器类"""
    
    def __init__(self):
        """初始化"""
        # 话术模板库
        self.templates = {
            '1-7天': {
                '静默': '【费用提醒】{客户名称}，您有{费用类型}共{金额}元即将到期，请尽快安排缴纳。',
                '温馨提示': '尊敬的{客户名称}，您的{费用类型}将于{到期日}到期，金额{金额}元，请提前安排。'
            },
            '8-30天': {
                '标准催缴': '【催缴通知】{客户名称}：您的{费用类型}已逾期{逾期天数}天，金额{金额}元，请尽快缴纳。',
                '正式提醒': '【正式提醒】{客户名称}：您的{费用类型}（{金额}元）已逾期{逾期天数}天，请于{限缴日期}前完成缴纳。'
            },
            '31天+': {
                '紧急催缴': '【紧急催缴】{客户名称}：您的{费用类型}已严重逾期{逾期天数}天，金额{金额}元，请立即处理！',
                '最后通知': '【最后通知】{客户名称}：您的{费用类型}（{金额}元）已逾期{逾期天数}天，请于{限缴日期}前缴纳，否则将采取进一步措施。'
            }
        }
        
    def generate_reminder(self, fee_record):
        """生成催缴提醒"""
        # 计算逾期天数
        today = datetime.now().date()
        due_date = fee_record.get('应缴日期')
        if isinstance(due_date, str):
            from datetime import datetime as dt
            due_date = dt.strptime(due_date, '%Y-%m-%d').date()
        
        overdue_days = (today - due_date).days if due_date < today else 0
        
        # 确定逾期等级
        if overdue_days <= 7:
            level = '1-7天'
            template_key = '静默'
        elif overdue_days <= 30:
            level = '8-30天'
            template_key = '标准催缴'
        else:
            level = '31天+'
            template_key = '紧急催缴'
        
        # 获取模板
        template = self.templates[level][template_key]
        
        # 填充模板
        message = template.format(
            客户名称=fee_record.get('客户名称', ''),
            费用类型=fee_record.get('费用类型', ''),
            金额=fee_record.get('应缴金额', 0),
            逾期天数=overdue_days,
            到期日=due_date.strftime('%Y-%m-%d') if due_date else '',
            限缴日期=(today + timedelta(days=7)).strftime('%Y-%m-%d')
        )
        
        return {
            '客户ID': fee_record.get('客户ID', ''),
            '客户名称': fee_record.get('客户名称', ''),
            '费用类型': fee_record.get('费用类型', ''),
            '应缴金额': fee_record.get('应缴金额', 0),
            '逾期天数': overdue_days,
            '分级': level,
            '提醒消息': message,
            '企微群ID': fee_record.get('企微群ID', ''),
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_batch_reminders(self, fee_records):
        """批量生成催缴提醒"""
        reminders = []
        for record in fee_records:
            reminder = self.generate_reminder(record)
            reminders.append(reminder)
        return reminders
    
    def format_message(self, reminder, format_type='text'):
        """格式化消息"""
        if format_type == 'text':
            return reminder['提醒消息']
        elif format_type == 'markdown':
            # Markdown格式
            md = f"""**【费用催缴提醒】**

**客户名称**：{reminder['客户名称']}
**费用类型**：{reminder['费用类型']}
**应缴金额**：{reminder['应缴金额']}元
**逾期天数**：{reminder['逾期天数']}天
**逾期等级**：{reminder['分级']}

{reminder['提醒消息']}

> 请尽快处理，如有疑问请联系物业服务中心。
"""
            return md
        elif format_type == 'json':
            return json.dumps(reminder, ensure_ascii=False, indent=2)
        else:
            return reminder['提醒消息']
    
    def generate_overdue_summary(self, reminders):
        """生成逾期汇总报告"""
        if not reminders:
            return "当前无逾期费用。"
        
        # 按等级分组
        level_groups = {}
        for reminder in reminders:
            level = reminder['分级']
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(reminder)
        
        # 生成汇总文本
        summary = f"""**逾期费用汇总报告**
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**逾期总数**：{len(reminders)}笔

"""
        
        for level, items in level_groups.items():
            summary += f"\n**{level}（{len(items)}笔）**：\n"
            total_amount = sum([item['应缴金额'] for item in items])
            summary += f"总金额：{total_amount:.2f}元\n"
            
            for i, item in enumerate(items[:5], 1):  # 只显示前5条
                summary += f"{i}. {item['客户名称']} - {item['费用类型']} - {item['应缴金额']}元（逾期{item['逾期天数']}天）\n"
            
            if len(items) > 5:
                summary += f"... 还有{len(items)-5}笔\n"
        
        return summary
    
    def get_personalized_template(self, customer_data):
        """根据客户数据获取个性化模板"""
        # 根据客户类型、历史缴费记录等个性化话术
        customer_type = customer_data.get('客户类型', '标准')
        payment_history = customer_data.get('缴费历史', '')
        
        if customer_type == 'VIP':
            return '尊敬的VIP客户{客户名称}，您的{费用类型}即将到期...'
        elif '经常逾期' in payment_history:
            return '【重要提醒】{客户名称}，您的{费用类型}已逾期，请立即处理...'
        else:
            return self.templates['8-30天']['标准催缴']
    
    def calculate_combined_fees(self, fee_records):
        """计算合并费用（能耗欠费合并）"""
        # 按客户ID分组
        customer_fees = {}
        for record in fee_records:
            customer_id = record.get('客户ID')
            if customer_id not in customer_fees:
                customer_fees[customer_id] = {
                    '客户名称': record.get('客户名称', ''),
                    '企微群ID': record.get('企微群ID', ''),
                    '费用明细': [],
                    '总金额': 0.0
                }
            
            customer_fees[customer_id]['费用明细'].append({
                '费用类型': record.get('费用类型', ''),
                '金额': record.get('应缴金额', 0)
            })
            customer_fees[customer_id]['总金额'] += record.get('应缴金额', 0)
        
        # 生成合并提醒
        combined_reminders = []
        for customer_id, data in customer_fees.items():
            fee_details = '、'.join([f"{item['费用类型']}{item['金额']}元" for item in data['费用明细']])
            message = f"【合并缴费提醒】{data['客户名称']}：您有以下费用待缴纳：{fee_details}，总金额{data['总金额']:.2f}元，请尽快处理。"
            
            combined_reminders.append({
                '客户ID': customer_id,
                '客户名称': data['客户名称'],
                '企微群ID': data['企微群ID'],
                '合并金额': data['总金额'],
                '费用数量': len(data['费用明细']),
                '提醒消息': message,
                '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return combined_reminders
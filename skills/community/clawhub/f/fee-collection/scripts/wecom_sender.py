#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企微消息发送模块 - 负责发送企微消息
"""

import requests
import json
from datetime import datetime

class WeComSender:
    """企微消息发送类"""
    
    def __init__(self, webhook_url=None):
        """初始化"""
        # 从配置文件读取webhook地址
        self.webhook_url = webhook_url or self._load_webhook_config()
        
    def _load_webhook_config(self):
        """加载webhook配置"""
        try:
            config_path = "/Users/mac/.qclaw/skills/fee-collection/config/wecom_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('webhook_url', '')
        except Exception as e:
            print(f"加载webhook配置失败: {e}")
            return ""
    
    def send_message(self, message, chat_id=None):
        """发送文本消息"""
        if not self.webhook_url:
            print("webhook地址未配置，无法发送消息")
            return False
        
        # 构造消息体
        payload = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        
        # 如果指定了chat_id，添加到payload
        if chat_id:
            payload["text"]["mentioned_list"] = [chat_id]
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    print(f"消息发送成功: {message[:50]}...")
                    return True
                else:
                    print(f"消息发送失败: {result.get('errmsg')}")
                    return False
            else:
                print(f"HTTP请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"发送消息异常: {e}")
            return False
    
    def send_markdown(self, markdown_content, chat_id=None):
        """发送Markdown消息"""
        if not self.webhook_url:
            print("webhook地址未配置，无法发送消息")
            return False
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown_content
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    print("Markdown消息发送成功")
                    return True
                else:
                    print(f"Markdown消息发送失败: {result.get('errmsg')}")
                    return False
            else:
                print(f"HTTP请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"发送Markdown消息异常: {e}")
            return False
    
    def send_report(self, report_data, report_type='daily'):
        """发送报告"""
        if report_type == 'daily':
            title = "📊 每日费用催缴报告"
            content = self._format_daily_report(report_data)
        elif report_type == 'monthly':
            title = "📈 月度费用收缴报告"
            content = self._format_monthly_report(report_data)
        else:
            title = "📋 费用催缴报告"
            content = str(report_data)
        
        markdown_content = f"{title}\n\n{content}"
        return self.send_markdown(markdown_content)
    
    def _format_daily_report(self, report_data):
        """格式化每日报告"""
        content = f"""**检查日期**: {report_data.get('检查日期', '')}

**逾期总数**: {report_data.get('逾期总数', 0)}笔
- 1-7天: {report_data.get('1-7天', 0)}笔
- 8-30天: {report_data.get('8-30天', 0)}笔  
- 31天+: {report_data.get('31天+', 0)}笔

**处理状态**: {report_data.get('处理状态', '')}
"""
        return content
    
    def _format_monthly_report(self, report_data):
        """格式化月度报告"""
        content = f"""**报告月份**: {report_data.get('报告月份', '')}

**费用统计**:
- 总费用: {report_data.get('总费用', 0):.2f}元
- 已缴费用: {report_data.get('已缴费用', 0):.2f}元
- 欠缴费用: {report_data.get('欠缴费用', 0):.2f}元

**收缴率**: {report_data.get('收缴率', '0%')}
**逾期客户数**: {report_data.get('逾期客户数', 0)}户
"""
        return content
    
    def send_overdue_alert(self, overdue_info):
        """发送逾期预警"""
        message = f"""【逾期预警】

客户: {overdue_info.get('客户名称', '')}
费用类型: {overdue_info.get('费用类型', '')}
逾期天数: {overdue_info.get('逾期天数', 0)}天
应缴金额: {overdue_info.get('应缴金额', 0):.2f}元

请尽快处理！
"""
        return self.send_message(message)
    
    def batch_send_reminders(self, reminders):
        """批量发送提醒"""
        success_count = 0
        fail_count = 0
        
        for reminder in reminders:
            # 根据分级决定是否发送
            level = reminder.get('分级', '')
            if level == '1-7天':
                # 静默处理，不发送
                print(f"静默处理: {reminder.get('客户名称')} - {reminder.get('费用类型')}")
                continue
            elif level == '8-30天':
                # 发送普通提醒
                message = reminder.get('提醒消息', '')
                chat_id = reminder.get('企微群ID', '')
                if self.send_message(message, chat_id):
                    success_count += 1
                else:
                    fail_count += 1
            elif level == '31天+':
                # 发送紧急提醒，@all
                message = f"@all {reminder.get('提醒消息', '')}"
                chat_id = reminder.get('企微群ID', '')
                if self.send_message(message, chat_id):
                    success_count += 1
                else:
                    fail_count += 1
        
        print(f"批量发送完成: 成功{success_count}条，失败{fail_count}条")
        return success_count, fail_count
    
    def test_connection(self):
        """测试连接"""
        test_message = f"企微消息发送测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return self.send_message(test_message)
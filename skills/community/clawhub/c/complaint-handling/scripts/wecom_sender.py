#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理企微消息发送模块
负责发送投诉处理相关消息到企业微信群
"""

import json
import requests
from datetime import datetime

class WecomSender:
    """企微消息发送类"""
    
    def __init__(self):
        """初始化"""
        # 企微Webhook配置（从配置文件读取）
        self.config_path = "/Users/mac/.qclaw/skills/complaint-handling/config/wecom_config.json"
        self.webhook_url = self._load_webhook_url()
    
    def _load_webhook_url(self):
        """加载企微Webhook URL"""
        try:
            if self.config_path:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('webhook_url', '')
        except Exception as e:
            print(f"加载企微配置失败: {e}")
            return ''
    
    def send_to_wecom(self, message, webhook_url=None):
        """发送消息到企微"""
        if not webhook_url:
            webhook_url = self.webhook_url
        
        if not webhook_url:
            print("企微Webhook URL未配置，跳过发送")
            return False
        
        try:
            # 构建企微消息格式
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            # 发送HTTP POST请求
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    print("企微消息发送成功")
                    return True
                else:
                    print(f"企微消息发送失败: {result.get('errmsg', '')}")
                    return False
            else:
                print(f"企微消息发送失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"企微消息发送异常: {e}")
            return False
    
    def send_markdown_to_wecom(self, content, webhook_url=None):
        """发送Markdown消息到企微"""
        if not webhook_url:
            webhook_url = self.webhook_url
        
        if not webhook_url:
            print("企微Webhook URL未配置，跳过发送")
            return False
        
        try:
            # 构建企微Markdown消息格式
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }
            
            # 发送HTTP POST请求
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    print("企微Markdown消息发送成功")
                    return True
                else:
                    print(f"企微Markdown消息发送失败: {result.get('errmsg', '')}")
                    return False
            else:
                print(f"企微Markdown消息发送失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"企微Markdown消息发送异常: {e}")
            return False
    
    def send_complaint_notification(self, complaint_data):
        """发送投诉通知"""
        message = f"""【投诉处理通知】

投诉ID: {complaint_data.get('投诉ID', '')}
客户名称: {complaint_data.get('客户名称', '')}
房号: {complaint_data.get('房号', '')}
投诉类型: {complaint_data.get('投诉类型', '')}
投诉内容: {complaint_data.get('投诉内容', '')}
投诉时间: {complaint_data.get('投诉时间', '')}

请30分钟内响应，24小时内回复方案。
"""
        
        return self.send_to_wecom(message)
    
    def send_escalation_notification(self, complaint_data):
        """发送升级投诉通知"""
        message = f"""【投诉升级通知 - 紧急】

投诉ID: {complaint_data.get('投诉ID', '')}
客户名称: {complaint_data.get('客户名称', '')}
房号: {complaint_data.get('房号', '')}
升级类型: {complaint_data.get('升级类型', '')}
投诉内容: {complaint_data.get('投诉内容', '')}

此投诉已升级，请管理层立即关注！
"""
        
        return self.send_to_wecom(message)
    
    def send_overdue_notification(self, complaint_data):
        """发送逾期投诉通知"""
        message = f"""【投诉处理逾期提醒】

投诉ID: {complaint_data.get('投诉ID', '')}
客户名称: {complaint_data.get('客户名称', '')}
逾期类型: {complaint_data.get('逾期类型', '')}
逾期时长: {complaint_data.get('逾期时长', '')}

请立即处理！
"""
        
        return self.send_to_wecom(message)
    
    def send_follow_up_notification(self, complaint_data):
        """发送回访提醒"""
        message = f"""【投诉回访提醒】

投诉ID: {complaint_data.get('投诉ID', '')}
客户名称: {complaint_data.get('客户名称', '')}
房号: {complaint_data.get('房号', '')}

该投诉已关闭，请在3天内完成回访。
"""
        
        return self.send_to_wecom(message)
    
    def send_daily_report(self, report_data):
        """发送每日投诉报告"""
        content = f"""**【每日投诉处理报告】**

**日期**: {report_data.get('日期', '')}

**逾期投诉数**: {report_data.get('逾期投诉数', 0)}件

"""
        
        if report_data.get('逾期详情'):
            content += "**逾期详情**:\n"
            for i, detail in enumerate(report_data.get('逾期详情', []), 1):
                content += f"{i}. {detail.get('投诉ID', '')} - {detail.get('逾期类型', '')} - {detail.get('客户名称', '')}\n"
        
        content += f"\n> 报告生成时间: {report_data.get('生成时间', '')}"
        
        return self.send_markdown_to_wecom(content)

# 示例用法
if __name__ == "__main__":
    sender = WecomSender()
    
    # 示例投诉数据
    sample_complaint = {
        '投诉ID': 'CP-20260602-001',
        '客户名称': '上海XX科技有限公司',
        '房号': 'T1-601',
        '投诉类型': '设施维护类',
        '投诉内容': '空调制冷效果不佳',
        '投诉时间': '2026-06-02 14:00:00'
    }
    
    # 发送投诉通知
    # sender.send_complaint_notification(sample_complaint)
    
    print("企微发送器模块已加载")
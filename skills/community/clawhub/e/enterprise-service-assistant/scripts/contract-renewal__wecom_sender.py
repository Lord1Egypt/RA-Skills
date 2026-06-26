#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理企微消息发送模块
负责发送合同续租相关消息到企业微信群
"""

import json
import requests
from datetime import datetime

class WecomSender:
    """企微消息发送类"""
    
    def __init__(self):
        """初始化"""
        # 企微Webhook配置（从配置文件读取）
        self.config_path = "[技能安装路径]/contract-renewal/config/wecom_config.json"
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
    
    def send_renewal_warning(self, warning_level, warning_list):
        """发送续租预警"""
        warning_icon = '🔴' if warning_level == '红色预警' else '🟡' if warning_level == '黄色预警' else '🟢'
        
        message = f"""{warning_icon}【{warning_level}】

合同即将到期客户数: {len(warning_list)}个

预警客户列表:
"""
        for i, item in enumerate(warning_list[:10], 1):  # 最多显示10个
            message += f"{i}. {item['客户名称']} - {item['房号']} - 距到期{item['距到期月数']}个月\n"
        
        if len(warning_list) > 10:
            message += f"... 等共{len(warning_list)}个客户\n"
        
        message += f"\n请相关部门及时跟进续租工作！"
        
        return self.send_to_wecom(message)
    
    def send_plan_created_notification(self, plan_data):
        """发送方案创建通知"""
        message = f"""【续租方案生成通知】

计划ID: {plan_data.get('计划ID', '')}
客户名称: {plan_data.get('客户名称', '')}
房号: {plan_data.get('房号', '')}

匹配方案: {plan_data.get('匹配方案', '')}
租金策略: {plan_data.get('租金策略', '')}
预计成功率: {plan_data.get('预计成功率', 0)}%

方案要点:
"""
        for i, point in enumerate(plan_data.get('方案要点', []), 1):
            message += f"  {i}. {point}\n"
        
        message += f"\n创建时间: {plan_data.get('创建时间', '')}"
        
        return self.send_to_wecom(message)
    
    def send_progress_update(self, plan_id, progress_data):
        """发送进度更新通知"""
        message = f"""【续租进度更新】

计划ID: {plan_id}

进度数据:
"""
        for key, value in progress_data.items():
            message += f"  - {key}: {value}\n"
        
        message += f"\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_to_wecom(message)

# 示例用法
if __name__ == "__main__":
    sender = WecomSender()
    
    # 示例预警数据
    sample_warning = [
        {
            '客户名称': '示例企业A',
            '房号': 'T1-601',
            '距到期月数': 2
        }
    ]
    
    # 发送预警通知
    # sender.send_renewal_warning('红色预警', sample_warning)
    
    print("企微发送器模块已加载")
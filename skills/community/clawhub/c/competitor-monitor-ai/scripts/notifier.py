#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知模块
支持多种通知方式：邮件、钉钉、飞书、企业微信
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class Notifier:
    """通知器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def send(self, message: str, **kwargs) -> bool:
        """发送通知"""
        raise NotImplementedError


class EmailNotifier(Notifier):
    """邮件通知"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.smtp_server = config.get('smtp_server', 'smtp.qq.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.username = config.get('username')
        self.password = config.get('password')
        self.to = config.get('to', [])
    
    def send(self, message: str, subject: str = None, **kwargs) -> bool:
        """发送邮件"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            if not self.username or not self.password:
                print("邮件配置不完整")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(self.to)
            msg['Subject'] = subject or '竞品监控告警'
            
            msg.attach(MIMEText(message, 'html', 'utf-8'))
            
            # 添加附件
            if 'attachments' in kwargs:
                from email.mime.base import MIMEBase
                from email import encoders
                
                for attachment_path in kwargs['attachments']:
                    with open(attachment_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={attachment_path.split("/")[-1]}'
                        )
                        msg.attach(part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"邮件已发送至: {self.to}")
            return True
            
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False


class DingTalkNotifier(Notifier):
    """钉钉机器人通知"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook = config.get('webhook')
        self.secret = config.get('secret')
    
    def _generate_sign(self, timestamp: str) -> str:
        """生成签名"""
        import hmac
        import hashlib
        import base64
        
        string_to_sign = f'{timestamp}\n{self.secret}'
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(hmac_code).decode('utf-8')
    
    def send(self, message: str, title: str = None, **kwargs) -> bool:
        """发送钉钉消息"""
        try:
            if not self.webhook:
                print("钉钉webhook未配置")
                return False
            
            timestamp = str(int(datetime.now().timestamp() * 1000))
            
            url = self.webhook
            if self.secret:
                sign = self._generate_sign(timestamp)
                url = f'{self.webhook}&timestamp={timestamp}&sign={sign}'
            
            # 构建消息
            data = {
                'msgtype': 'markdown',
                'markdown': {
                    'title': title or '竞品监控告警',
                    'text': message
                }
            }
            
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get('errcode') == 0:
                print("钉钉消息发送成功")
                return True
            else:
                print(f"钉钉消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"钉钉消息发送失败: {e}")
            return False


class FeishuNotifier(Notifier):
    """飞书机器人通知"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook = config.get('webhook')
    
    def send(self, message: str, title: str = None, **kwargs) -> bool:
        """发送飞书消息"""
        try:
            if not self.webhook:
                print("飞书webhook未配置")
                return False
            
            data = {
                'msg_type': 'interactive',
                'card': {
                    'header': {
                        'title': {
                            'tag': 'plain_text',
                            'content': title or '竞品监控告警'
                        },
                        'template': 'red'
                    },
                    'elements': [
                        {
                            'tag': 'div',
                            'text': {
                                'tag': 'lark_md',
                                'content': message
                            }
                        }
                    ]
                }
            }
            
            response = requests.post(self.webhook, json=data, timeout=30)
            result = response.json()
            
            if result.get('code') == 0:
                print("飞书消息发送成功")
                return True
            else:
                print(f"飞书消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"飞书消息发送失败: {e}")
            return False


class WeComNotifier(Notifier):
    """企业微信机器人通知"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook = config.get('webhook')
    
    def send(self, message: str, title: str = None, **kwargs) -> bool:
        """发送企业微信消息"""
        try:
            if not self.webhook:
                print("企业微信webhook未配置")
                return False
            
            data = {
                'msgtype': 'markdown',
                'markdown': {
                    'content': f"**{title or '竞品监控告警'}**\n\n{message}"
                }
            }
            
            response = requests.post(self.webhook, json=data, timeout=30)
            result = response.json()
            
            if result.get('errcode') == 0:
                print("企业微信消息发送成功")
                return True
            else:
                print(f"企业微信消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"企业微信消息发送失败: {e}")
            return False


class NotificationManager:
    """通知管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化通知管理器
        
        Args:
            config: 通知配置
        """
        self.config = config
        self.notifiers = []
        
        # 初始化各通知渠道
        if 'email' in config:
            self.notifiers.append(EmailNotifier(config['email']))
        
        if 'dingtalk' in config:
            self.notifiers.append(DingTalkNotifier(config['dingtalk']))
        
        if 'feishu' in config:
            self.notifiers.append(FeishuNotifier(config['feishu']))
        
        if 'wecom' in config:
            self.notifiers.append(WeComNotifier(config['wecom']))
    
    def send_alert(self, alert: Dict, screenshot_path: str = None) -> List[bool]:
        """
        发送告警通知
        
        Args:
            alert: 告警信息
            screenshot_path: 截图路径
            
        Returns:
            各通知渠道发送结果
        """
        # 构建消息
        message = self._format_alert_message(alert)
        title = f"[{alert.get('level', 'INFO').upper()}] {alert.get('message', '监控告警')}"
        
        results = []
        for notifier in self.notifiers:
            kwargs = {}
            if screenshot_path:
                kwargs['attachments'] = [screenshot_path]
            
            result = notifier.send(message, title=title, **kwargs)
            results.append(result)
        
        return results
    
    def _format_alert_message(self, alert: Dict) -> str:
        """格式化告警消息"""
        level_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'info': '🔵'
        }
        
        level = alert.get('level', 'info')
        emoji = level_emoji.get(level, '⚪')
        
        message = f"""
{emoji} **{alert.get('message', '监控告警')}**

**告警详情：**
- 任务ID: {alert.get('task_id', 'N/A')}
- 告警类型: {alert.get('type', 'N/A')}
- 监控指标: {alert.get('metric', 'N/A')}
- 触发时间: {alert.get('timestamp', 'N/A')}

**数据详情：**
```json
{json.dumps(alert.get('details', {}), ensure_ascii=False, indent=2)}
```
        """
        
        return message.strip()
    
    def send_summary(self, summary: Dict) -> List[bool]:
        """
        发送汇总报告
        
        Args:
            summary: 汇总信息
            
        Returns:
            各通知渠道发送结果
        """
        message = f"""
📊 **竞品监控日报**

**统计时间：** {summary.get('date', 'N/A')}

**监控概况：**
- 监控任务数: {summary.get('total_tasks', 0)}
- 数据采集次数: {summary.get('total_scrapes', 0)}
- 异常告警数: {summary.get('total_alerts', 0)}

**异常分布：**
- 严重: {summary.get('critical_alerts', 0)}
- 高: {summary.get('high_alerts', 0)}
- 中: {summary.get('medium_alerts', 0)}
- 低: {summary.get('low_alerts', 0)}

**热门监控：**
{chr(10).join([f"- {item['task_name']}: {item['alert_count']} 次告警" for item in summary.get('top_tasks', [])])}
        """
        
        results = []
        for notifier in self.notifiers:
            result = notifier.send(message.strip(), title='竞品监控日报')
            results.append(result)
        
        return results


def main():
    """测试入口"""
    # 测试配置
    config = {
        'dingtalk': {
            'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=your_token',
            'secret': 'your_secret'
        }
    }
    
    # 测试告警
    alert = {
        'task_id': 'test_001',
        'level': 'high',
        'type': 'spike',
        'metric': 'likes',
        'message': '点赞数暴增 350%',
        'timestamp': datetime.now().isoformat(),
        'details': {
            'current': 5000,
            'average': 1111,
            'change_percent': 350
        }
    }
    
    # 发送通知
    manager = NotificationManager(config)
    results = manager.send_alert(alert)
    
    print(f"通知发送结果: {results}")


if __name__ == '__main__':
    main()

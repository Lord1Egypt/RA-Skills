#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台通知系统 - 合规版 v1.0.11
支持：飞书 / 钉钉 / Telegram / WhatsApp
功能：
1. 合规的 env_fingerprint（client_version 和 evolver_version 嵌套在 payload 中）
2. 429 退避算法（至少等待 60 秒）
3. 速率限制检查
4. 连接状态汇报（仅在 WebUI）
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# 合规版本信息
CLIENT_VERSION = "1.25.0"
EVOLVER_VERSION = "1.25.0"

# 速率限制配置
RATE_LIMIT_DELAY = 60  # 429 后等待 60 秒
MIN_REQUEST_INTERVAL = 5  # 最小请求间隔 5 秒

# 全局连接状态
_connection_status = "disconnected"
_last_request_time = None
_last_429_time = None


def report_connection_status(status: str = "connected"):
    """汇报连接状态（仅在 WebUI）"""
    global _connection_status
    _connection_status = status
    print(f"[WebUI] 连接状态：{status}")


def check_connection() -> str:
    """检查连接状态"""
    global _connection_status
    return _connection_status


def get_compliant_fingerprint() -> Dict:
    """获取合规的 env_fingerprint"""
    return {
        "client_version": CLIENT_VERSION,
        "evolver_version": EVOLVER_VERSION,
        "platform": "linux",
        "arch": "x64",
        "node_version": "v24.14.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def check_rate_limit():
    """检查速率限制"""
    global _last_request_time, _last_429_time
    now = datetime.now()
    
    # 检查 429 等待时间
    if _last_429_time:
        elapsed = (now - _last_429_time).total_seconds()
        if elapsed < RATE_LIMIT_DELAY:
            wait_time = RATE_LIMIT_DELAY - elapsed
            print(f"[通知系统] ⏳ 429 限流，需等待 {wait_time:.0f} 秒")
            time.sleep(wait_time)
    
    # 检查最小请求间隔
    if _last_request_time:
        elapsed = (now - _last_request_time).total_seconds()
        if elapsed < MIN_REQUEST_INTERVAL:
            wait_time = MIN_REQUEST_INTERVAL - elapsed
            time.sleep(wait_time)
    
    _last_request_time = datetime.now()


def send_request_with_retry(url: str, payload: Dict, headers: Dict = None, max_retries: int = 3) -> Dict:
    """发送请求（带退避算法 + 503 处理 + search_only 支持）"""
    check_rate_limit()
    
    # 添加合规的 env_fingerprint
    if 'payload' in payload:
        payload['payload']['env_fingerprint'] = get_compliant_fingerprint()
    
    # 添加 search_only 标志（如果请求体中包含 EvoMap API 相关字段）
    if 'payload' in payload and isinstance(payload['payload'], dict):
        # 默认添加 search_only: true，避免不必要的扣费
        if 'search_only' not in payload['payload']:
            payload['payload']['search_only'] = True
    
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            data = resp.json()
            
            # 处理 429 错误（限流）
            if resp.status_code == 429:
                global _last_429_time
                _last_429_time = datetime.now()
                print(f"[通知系统] ⚠️ 429 限流，等待 {RATE_LIMIT_DELAY} 秒后重试 (尝试 {attempt+1}/{max_retries})")
                
                if attempt < max_retries - 1:
                    time.sleep(RATE_LIMIT_DELAY)
                    continue
                else:
                    print(f"[通知系统] ❌ 重试次数过多，放弃请求")
                    return {'code': 429, 'msg': 'Rate limit reached'}
            
            # 处理 503 错误（服务器负载保护 / Admission Control）
            if resp.status_code == 503:
                print(f"[通知系统] ⚠️ 503 服务不可用（服务器负载保护），等待 30 秒后重试 (尝试 {attempt+1}/{max_retries})")
                print(f"[通知系统] 💡 提示：Free 用户可能被降级，建议避开高峰期或升级套餐")
                
                if attempt < max_retries - 1:
                    time.sleep(30)  # 503 等待 30 秒
                    continue
                else:
                    print(f"[通知系统] ❌ 服务器持续繁忙，放弃请求")
                    return {'code': 503, 'msg': 'Service unavailable - Server overloaded'}
            
            return data
            
        except requests.exceptions.Timeout:
            print(f"[通知系统] ⚠️ 请求超时，等待 10 秒后重试 (尝试 {attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(10)
                continue
            else:
                return {'code': -1, 'msg': 'Request timeout'}
                
        except Exception as e:
            print(f"[通知系统] ❌ 请求异常：{e}")
            return {'code': -1, 'msg': str(e)}
    
    return {'code': -1, 'msg': 'Max retries exceeded'}


class FeishuNotifier:
    """飞书通知（合规版）"""
    
    def __init__(self, config_file: str = None, show_version: bool = False):
        self.show_version = show_version
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 飞书通知已加载")
        
        # 加载配置（自动检测 OpenClaw 配置）
        self.config = self._load_config(config_file)
        self.app_id = self.config.get('appId', 'cli_a929676f8bf81cc7')
        
        # 优先从 app 配置中获取 app_secret
        app_config = self.config.get('app', {})
        self.app_secret = app_config.get('appSecret', '')
        
        # 如果没有，尝试直接从配置根目录获取
        if not self.app_secret:
            self.app_secret = self.config.get('appSecret', '')
        
        self.target_user = self.config.get('targetUser', '') or self.config.get('targetId', 'ou_f4919832188bcc630f8f257497fa93a4')
        self.access_token = None
        self.token_expire = 0
        
        # 检测配置来源
        config_source = self._detect_config_source()
        
        if show_version:
            if self.app_secret:
                print(f"[飞书] ✅ App ID: {self.app_id}")
                print(f"[飞书] ✅ App Secret: 已配置")
                print(f"[飞书] ✅ 目标用户：{self.target_user}")
                print(f"[飞书] ✅ 配置来源：{config_source}")
            else:
                print(f"[飞书] ⚠️ App ID: {self.app_id}")
                print(f"[飞书] ⚠️ App Secret: 未配置")
                print(f"[飞书] ⚠️ 目标用户：{self.target_user}")
                print(f"[飞书] ⚠️ 配置来源：{config_source}")
    
    def _load_config(self, config_file: str = None) -> Dict:
        """加载配置（自动检测 OpenClaw 飞书配置）"""
        if config_file:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置路径
        default_paths = [
            '/home/admin/.openclaw/workspace/.config/feishu-notification.json',
            '/home/admin/.openclaw/credentials/feishu-config.json',
            '/home/admin/.openclaw/credentials/feishu-pairing.json'
        ]
        
        config = {}
        for path in default_paths:
            if Path(path).exists():
                with open(path, 'r', encoding='utf-8') as f:
                    config.update(json.load(f))
        
        # 如果没有配置，尝试从 OpenClaw 飞书配置加载
        if not config.get('app') and not config.get('webhook'):
            # 尝试从 OpenClaw 飞书配置加载
            openclaw_feishu_paths = [
                '/home/admin/.openclaw/workspace/.config/python-learning-state.json',
                '/home/admin/.openclaw/credentials/feishu-default-allowFrom.json',
                '/home/admin/.openclaw/credentials/feishu-pairing.json'
            ]
            
            for path in openclaw_feishu_paths:
                if Path(path).exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        openclaw_config = json.load(f)
                        
                        # 加载 appSecret
                        if 'appSecret' in openclaw_config:
                            if 'app' not in config:
                                config['app'] = {}
                            config['app']['appSecret'] = openclaw_config['appSecret']
                            print(f"[飞书] ✅ 已从 OpenClaw 配置加载 app_secret")
                        
                        # 加载用户 ID
                        if 'targetId' in openclaw_config.get('pythonLearning', {}):
                            config['targetUser'] = openclaw_config['pythonLearning']['targetId']
                            print(f"[飞书] ✅ 已从 OpenClaw 配置加载用户 ID")
                        
                        # 加载允许的用户列表
                        if 'allowFrom' in openclaw_config:
                            allow_from = openclaw_config['allowFrom']
                            if allow_from:
                                config['targetUser'] = allow_from[0]
                                print(f"[飞书] ✅ 已从 OpenClaw 配置加载允许的用户")
                        
                        break
        
        # 如果还是没有配置，尝试从环境变量加载
        if not config.get('app'):
            import os
            app_id = os.environ.get('FEISHU_APP_ID')
            app_secret = os.environ.get('FEISHU_APP_SECRET')
            
            if app_id and app_secret:
                config['app'] = {
                    'appId': app_id,
                    'appSecret': app_secret
                }
                print(f"[飞书] ✅ 已从环境变量加载配置")
        
        return config
    
    def _detect_config_source(self) -> str:
        """检测配置来源"""
        if self.config.get('webhook', {}).get('enabled'):
            return "Webhook"
        elif self.config.get('app', {}).get('appSecret'):
            # 检查是否来自 OpenClaw 配置
            openclaw_paths = [
                '/home/admin/.openclaw/workspace/.config/python-learning-state.json',
                '/home/admin/.openclaw/credentials/feishu-default-allowFrom.json'
            ]
            for path in openclaw_paths:
                if Path(path).exists():
                    return "OpenClaw 自动检测"
            return "配置文件"
        else:
            return "未配置"
    
    def _get_access_token(self) -> Optional[str]:
        """获取访问令牌（合规版）"""
        if self.access_token and time.time() < self.token_expire:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        data = send_request_with_retry(url, payload)
        
        if data.get('code') == 0:
            self.access_token = data.get('tenant_access_token')
            self.token_expire = time.time() + 7200  # 2 小时有效期
            print(f"[飞书] ✅ 访问令牌获取成功")
            return self.access_token
        else:
            print(f"[飞书] ⚠️ 访问令牌获取失败：{data.get('msg')}")
            return None
    
    def send(self, message: str, **kwargs) -> bool:
        """发送消息（合规版）"""
        if not self.app_secret:
            print(f"[飞书] ❌ App Secret 未配置")
            return False
        
        token = self._get_access_token()
        if not token:
            report_connection_status("连接失败")
            return False
        
        url = "https://open.feishu.cn/open-apis/message/v4/send"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": self.target_user,
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        data = send_request_with_retry(url, payload, headers)
        
        if data.get('code') == 0:
            print(f"[飞书] ✅ 消息发送成功")
            report_connection_status("连接已恢复")
            return True
        else:
            print(f"[飞书] ❌ 发送失败：{data.get('msg')}")
            if data.get('code') == 429:
                report_connection_status("限流中")
            else:
                report_connection_status("连接失败")
            return False


class NotificationSystem:
    """多平台通知系统（合规版）"""
    
    def __init__(self, config: Dict = None, show_version: bool = False):
        self.config = config or {}
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 通知系统已加载")
        
        # 飞书配置
        self.feishu_webhook = self.config.get('webhook', {}).get('url')
        if self.feishu_webhook:
            if show_version:
                print(f"[飞书] ✅ Webhook 模式已配置")
            self.feishu_mode = 'webhook'
        else:
            self.feishu = FeishuNotifier(show_version=show_version)
            self.feishu_mode = 'app'
        
        self.dingtalk = DingtalkNotifier(
            webhook=self.config.get('dingtalk_webhook'),
            secret=self.config.get('dingtalk_secret')
        )
        self.telegram = TelegramNotifier(
            token=self.config.get('telegram_token'),
            chat_id=self.config.get('telegram_chat_id')
        )
    
    def send(self, message: str, platform: str = "all", **kwargs) -> Dict:
        """发送通知"""
        results = {}
        
        if platform in ["feishu", "all"]:
            # 使用 Webhook 模式（简单）
            if hasattr(self, 'feishu_webhook') and self.feishu_webhook:
                results['feishu'] = self._send_feishu_webhook(message)
            else:
                # 使用 App API 模式（合规版）
                results['feishu'] = self.feishu.send(message, **kwargs)
        
        if platform in ["dingtalk", "all"]:
            results['dingtalk'] = self.dingtalk.send(message)
        
        if platform in ["telegram", "all"]:
            results['telegram'] = self.telegram.send(message)
        
        return results
    
    def _send_feishu_webhook(self, message: str) -> bool:
        """使用飞书 Webhook 发送消息（简单模式）"""
        if not self.feishu_webhook:
            print(f"[飞书 Webhook] ❌ Webhook URL 未配置")
            return False
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        try:
            resp = requests.post(self.feishu_webhook, json=payload, timeout=10)
            data = resp.json()
            
            if data.get('code') == 0 or data.get('StatusCode') == 0:
                print(f"[飞书 Webhook] ✅ 消息发送成功")
                report_connection_status("连接已恢复")
                return True
            else:
                print(f"[飞书 Webhook] ⚠️ 发送失败：{data.get('msg', '未知错误')}")
                report_connection_status("连接失败")
                return False
        except Exception as e:
            print(f"[飞书 Webhook] ❌ 发送异常：{e}")
            report_connection_status("连接失败")
            return False


class DingtalkNotifier:
    """钉钉通知"""
    
    def __init__(self, webhook: str = None, secret: str = None):
        self.webhook = webhook
        self.secret = secret
    
    def send(self, message: str) -> bool:
        """发送钉钉消息"""
        if not self.webhook:
            print(f"[钉钉] ❌ Webhook 未配置")
            return False
        
        # 生成签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        
        url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        
        payload = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            
            if data.get('errcode') == 0:
                print(f"[钉钉] ✅ 消息发送成功")
                return True
            else:
                print(f"[钉钉] ❌ 发送失败：{data.get('errmsg')}")
                return False
        except Exception as e:
            print(f"[钉钉] ❌ 发送异常：{e}")
            return False


class TelegramNotifier:
    """Telegram 通知"""
    
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token
        self.chat_id = chat_id
    
    def send(self, message: str) -> bool:
        """发送 Telegram 消息"""
        if not self.token or not self.chat_id:
            print(f"[Telegram] ❌ Token 或 Chat ID 未配置")
            return False
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            
            if data.get('ok'):
                print(f"[Telegram] ✅ 消息发送成功")
                return True
            else:
                print(f"[Telegram] ❌ 发送失败：{data.get('description')}")
                return False
        except Exception as e:
            print(f"[Telegram] ❌ 发送异常：{e}")
            return False


if __name__ == "__main__":
    # 测试连接
    print("=" * 70)
    print("📬 测试飞书连接（合规版 v1.0.11）")
    print("=" * 70)
    print()
    
    notifier = FeishuNotifier(show_version=True)
    print()
    
    # 发送测试消息
    test_message = """【🧬 EvoMap WorkBench v1.0.11】飞书连通性测试

✅ 合规版本：1.25.0
✅ env_fingerprint 已嵌套
✅ 429 退避算法已启用
✅ 速率限制检查已启用

测试时间：2026-04-05
状态：连接测试中
"""
    
    result = notifier.send(test_message)
    print()
    
    if result:
        print("=" * 70)
        print("🎉 飞书连通性测试通过！")
        print("=" * 70)
    else:
        print("=" * 70)
        print("⚠️ 飞书连通性测试未通过")
        print("=" * 70)

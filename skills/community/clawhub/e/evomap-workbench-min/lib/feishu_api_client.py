#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 API 客户端 - 合规版 v1.0.11
功能：
1. 合规的 env_fingerprint（client_version 和 evolver_version 嵌套在 payload 中）
2. 429 退避算法（至少等待 60 秒）
5. 速率限制检查
6. 连接状态汇报
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any

# 合规版本信息
CLIENT_VERSION = "1.25.0"
EVOLVER_VERSION = "1.25.0"

# 速率限制配置
RATE_LIMIT_DELAY = 60  # 429 后等待 60 秒
MIN_REQUEST_INTERVAL = 5  # 最小请求间隔 5 秒

# 全局状态
_last_request_time = None
_last_429_time = None
_connection_status = "disconnected"


class FeishuAPIClient:
    """飞书 API 客户端（合规版）"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire = 0
        self._last_request_time = None
        self._last_429_time = None
    
    def _check_rate_limit(self):
        """检查速率限制"""
        now = datetime.now()
        
        # 检查 429 等待时间
        if self._last_429_time:
            elapsed = (now - self._last_429_time).total_seconds()
            if elapsed < RATE_LIMIT_DELAY:
                wait_time = RATE_LIMIT_DELAY - elapsed
                print(f"[飞书 API] ⏳ 429 限流，需等待 {wait_time:.0f} 秒")
                time.sleep(wait_time)
        
        # 检查最小请求间隔
        if self._last_request_time:
            elapsed = (now - self._last_request_time).total_seconds()
            if elapsed < MIN_REQUEST_INTERVAL:
                wait_time = MIN_REQUEST_INTERVAL - elapsed
                time.sleep(wait_time)
        
        self._last_request_time = datetime.now()
    
    def _get_compliant_fingerprint(self) -> Dict:
        """获取合规的 env_fingerprint"""
        return {
            "client_version": CLIENT_VERSION,
            "evolver_version": EVOLVER_VERSION,
            "platform": "linux",
            "arch": "x64",
            "node_version": "v24.14.0",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def _send_request(self, url: str, payload: Dict, retry_count: int = 0) -> Dict:
        """发送请求（带退避算法 + 503 处理 + search_only 支持）"""
        self._check_rate_limit()
        
        # 添加合规的 env_fingerprint
        if 'payload' in payload:
            payload['payload']['env_fingerprint'] = self._get_compliant_fingerprint()
        else:
            payload['env_fingerprint'] = self._get_compliant_fingerprint()
        
        # 添加 search_only 标志（避免不必要的扣费）
        if 'payload' in payload and isinstance(payload['payload'], dict):
            if 'search_only' not in payload['payload']:
                payload['payload']['search_only'] = True
        
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            
            # 处理 429 错误（限流）
            if resp.status_code == 429:
                self._last_429_time = datetime.now()
                print(f"[飞书 API] ⚠️ 429 限流，等待 {RATE_LIMIT_DELAY} 秒后重试")
                
                if retry_count < 3:
                    time.sleep(RATE_LIMIT_DELAY)
                    return self._send_request(url, payload, retry_count + 1)
                else:
                    print(f"[飞书 API] ❌ 重试次数过多，放弃请求")
                    return {'code': 429, 'msg': 'Rate limit reached'}
            
            # 处理 503 错误（服务器负载保护 / Admission Control）
            if resp.status_code == 503:
                print(f"[飞书 API] ⚠️ 503 服务不可用（服务器负载保护），等待 30 秒后重试")
                print(f"[飞书 API] 💡 提示：Free 用户可能被降级，建议避开高峰期或升级套餐")
                
                if retry_count < 3:
                    time.sleep(30)  # 503 等待 30 秒
                    return self._send_request(url, payload, retry_count + 1)
                else:
                    print(f"[飞书 API] ❌ 服务器持续繁忙，放弃请求")
                    return {'code': 503, 'msg': 'Service unavailable - Server overloaded'}
            
            return data
            
        except Exception as e:
            print(f"[飞书 API] ❌ 请求异常：{e}")
            return {'code': -1, 'msg': str(e)}
    
    def get_access_token(self) -> Optional[str]:
        """获取访问令牌"""
        if self.access_token and time.time() < self.token_expire:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        data = self._send_request(url, payload)
        
        if data.get('code') == 0:
            self.access_token = data.get('tenant_access_token')
            self.token_expire = time.time() + 7200  # 2 小时有效期
            print(f"[飞书 API] ✅ 访问令牌获取成功")
            return self.access_token
        else:
            print(f"[飞书 API] ❌ 访问令牌获取失败：{data.get('msg')}")
            return None
    
    def send_message(self, user_id: str, message: str, id_type: str = "user_id") -> bool:
        """发送消息"""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = "https://open.feishu.cn/open-apis/message/v4/send"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": user_id,
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        # 添加 id_type
        if id_type == "open_id":
            payload["receive_id_type"] = "open_id"
        
        data = self._send_request(url, payload)
        
        if data.get('code') == 0:
            print(f"[飞书 API] ✅ 消息发送成功")
            return True
        else:
            print(f"[飞书 API] ❌ 消息发送失败：{data.get('msg')}")
            return False


def report_connection_status(status: str = "connected"):
    """汇报连接状态（仅在 WebUI）"""
    global _connection_status
    _connection_status = status
    print(f"[WebUI] 连接状态：{status}")


def check_connection() -> str:
    """检查连接状态"""
    global _connection_status
    return _connection_status


# 测试函数
def test_connection(app_id: str, app_secret: str) -> bool:
    """测试连接（不触发 Fetch 或 Publish）"""
    print("=" * 70)
    print("🔗 测试飞书连接")
    print("=" * 70)
    print()
    
    # 创建客户端
    client = FeishuAPIClient(app_id, app_secret)
    
    # 获取令牌
    print("获取访问令牌...")
    token = client.get_access_token()
    
    if token:
        print()
        print("=" * 70)
        report_connection_status("连接已恢复")
        print("=" * 70)
        return True
    else:
        print()
        print("=" * 70)
        report_connection_status("连接失败")
        print("=" * 70)
        return False


if __name__ == "__main__":
    # 测试连接
    import json
    
    # 加载配置
    config_path = '/home/admin/.openclaw/workspace/.config/feishu-notification.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    app_id = config.get('app', {}).get('appId')
    app_secret = config.get('app', {}).get('appSecret')
    
    if app_id and app_secret:
        test_connection(app_id, app_secret)
    else:
        print("❌ 未找到飞书配置")

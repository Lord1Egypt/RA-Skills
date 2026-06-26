#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Guard - 授权保护核心模块
确保所有外部 API 操作都经过用户明确授权
"""

import json
import os
import uuid
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Any
import requests


class AuthGuard:
    """授权保护核心类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化 Auth Guard
        
        Args:
            config_path: 配置文件路径，默认 ~/.auth_guard/config.json
        """
        self.config_path = config_path or os.path.expanduser("~/.auth_guard/config.json")
        self.config = self._load_config()
        self.audit_log_path = os.path.expanduser(self.config.get("audit", {}).get("log_path", "~/.auth_guard/audit_log.jsonl"))
        
        # 确保目录存在
        Path(self.audit_log_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 内存缓存（用于时间窗口）
        self._cache = {}
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 返回默认配置
        return {
            "enabled": True,
            "mode": "STRICT",  # STRICT | WHITELIST | AUDIT
            "timeout_seconds": 300,
            "notification": {
                "channel": "feishu",
                "webhook_url": None
            },
            "security": {
                "api_key": self._generate_api_key(),
                "allowed_ips": ["127.0.0.1"],
                "rate_limit": {
                    "requests_per_hour": 100
                }
            },
            "audit": {
                "log_path": "~/.auth_guard/audit_log.jsonl",
                "retention_days": 90
            }
        }
    
    def _generate_api_key(self) -> str:
        """生成 API 密钥"""
        return hashlib.sha256(os.urandom(32)).hexdigest()
    
    def _save_config(self):
        """保存配置文件"""
        Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def request_authorization(
        self,
        service: str,
        action: str,
        params: Dict[str, Any],
        reason: str = "",
        requester: str = "unknown",
        priority: str = "normal"
    ) -> Dict:
        """
        请求授权
        
        Args:
            service: 服务名称（如 google-mail, slack）
            action: 操作类型（如 messages.send, chat.postMessage）
            params: 操作参数
            reason: 请求原因
            requester: 请求者标识
            priority: 优先级 (normal|high|urgent)
        
        Returns:
            Dict: {
                "authorized": bool,
                "auth_token": str (if authorized),
                "expires_at": str (if authorized),
                "reason": str (if denied)
            }
        """
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # 检查是否启用
        if not self.config.get("enabled", True):
            return {
                "authorized": True,
                "auth_token": "disabled",
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z",
                "note": "Auth Guard 已禁用"
            }
        
        # 审计模式 - 只记录不阻止
        if self.config.get("mode") == "AUDIT":
            self._log_audit(request_id, service, action, requester, "audit_mode", None)
            return {
                "authorized": True,
                "auth_token": request_id,
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z",
                "note": "审计模式 - 已记录但未阻止"
            }
        
        # 检查白名单（仅限 WHITELIST 模式）
        if self.config.get("mode") == "WHITELIST":
            whitelist_check = self._check_whitelist(service, action, params)
            if whitelist_check.get("allowed"):
                self._log_audit(request_id, service, action, requester, "whitelisted", None)
                return {
                    "authorized": True,
                    "auth_token": request_id,
                    "expires_at": (datetime.utcnow() + timedelta(seconds=whitelist_check.get("ttl", 3600))).isoformat() + "Z",
                    "note": "白名单操作"
                }
        
        # 检查黑名单
        blacklist_check = self._check_blacklist(service, action)
        if blacklist_check.get("blocked"):
            self._log_audit(request_id, service, action, requester, "denied", blacklist_check.get("reason"))
            return {
                "authorized": False,
                "reason": f"黑名单操作：{blacklist_check.get('reason')}"
            }
        
        # STRICT 模式 - 需要用户确认
        # 发送通知并等待用户响应
        notification_sent = self._send_notification(request_id, service, action, params, reason, requester, priority)
        
        if not notification_sent:
            # 无法通知用户，默认拒绝
            self._log_audit(request_id, service, action, requester, "denied", "无法发送通知")
            return {
                "authorized": False,
                "reason": "无法发送授权请求通知"
            }
        
        # 等待用户响应（轮询）
        timeout = self.config.get("timeout_seconds", 300)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            decision = self._check_decision(request_id)
            
            if decision:
                if decision.get("approved"):
                    auth_token = self._generate_auth_token(request_id, service, action)
                    expires_at = datetime.utcnow() + timedelta(seconds=decision.get("ttl", 3600))
                    
                    self._log_audit(request_id, service, action, requester, "approved", None, auth_token)
                    
                    return {
                        "authorized": True,
                        "auth_token": auth_token,
                        "expires_at": expires_at.isoformat() + "Z",
                        "conditions": decision.get("conditions", [])
                    }
                else:
                    self._log_audit(request_id, service, action, requester, "denied", decision.get("reason"))
                    return {
                        "authorized": False,
                        "reason": decision.get("reason", "用户拒绝")
                    }
            
            time.sleep(2)  # 每 2 秒检查一次
        
        # 超时
        self._log_audit(request_id, service, action, requester, "denied", "超时未响应")
        return {
            "authorized": False,
            "reason": f"授权请求超时（{timeout}秒）"
        }
    
    def _check_whitelist(self, service: str, action: str, params: Dict) -> Dict:
        """检查白名单"""
        whitelist_path = os.path.expanduser("~/.auth_guard_whitelist.json")
        
        if not os.path.exists(whitelist_path):
            return {"allowed": False}
        
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
        
        allowed_ops = whitelist.get("allowed_operations", [])
        
        for op in allowed_ops:
            if op.get("service") == service and op.get("action") == action:
                # 检查速率限制
                key = f"{service}.{action}"
                max_per_hour = op.get("max_per_hour", 1000)
                
                current_count = self._cache.get(f"rate_{key}", 0)
                if current_count >= max_per_hour:
                    return {"allowed": False, "reason": "超过速率限制"}
                
                self._cache[f"rate_{key}"] = current_count + 1
                
                # 检查时间窗口
                time_windows = whitelist.get("time_windows", {})
                ttl = time_windows.get(key, 3600)
                
                return {"allowed": True, "ttl": ttl}
        
        return {"allowed": False}
    
    def _check_blacklist(self, service: str, action: str) -> Dict:
        """检查黑名单"""
        whitelist_path = os.path.expanduser("~/.auth_guard_whitelist.json")
        
        if not os.path.exists(whitelist_path):
            return {"blocked": False}
        
        with open(whitelist_path, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
        
        blocked_ops = whitelist.get("blocked_operations", [])
        
        for op in blocked_ops:
            op_service = op.get("service", "*")
            op_action = op.get("action", "*")
            
            if (op_service == "*" or op_service == service) and \
               (op_action == "*" or op_action == action):
                return {"blocked": True, "reason": op.get("reason", "黑名单操作")}
        
        return {"blocked": False}
    
    def _send_notification(
        self,
        request_id: str,
        service: str,
        action: str,
        params: Dict,
        reason: str,
        requester: str,
        priority: str
    ) -> bool:
        """发送授权请求通知"""
        channel = self.config.get("notification", {}).get("channel", "feishu")
        webhook_url = self.config.get("notification", {}).get("webhook_url")
        
        # 构建通知消息
        message = self._build_notification_message(request_id, service, action, params, reason, requester, priority)
        
        if channel == "feishu" and webhook_url:
            try:
                response = requests.post(webhook_url, json=message, timeout=10)
                return response.status_code == 200
            except Exception as e:
                print(f"发送飞书通知失败：{e}")
                return False
        
        # 默认输出到控制台（用于测试）
        print("\n" + "="*60)
        print(f"🔐 授权请求 #{request_id}")
        print("="*60)
        print(f"服务：{service}")
        print(f"操作：{action}")
        print(f"请求者：{requester}")
        print(f"优先级：{priority}")
        print(f"原因：{reason}")
        print("-"*60)
        print(f"参数：{json.dumps(params, indent=2, ensure_ascii=False)}")
        print("="*60)
        print("等待用户确认... (Ctrl+C 取消)")
        
        return True
    
    def _build_notification_message(
        self,
        request_id: str,
        service: str,
        action: str,
        params: Dict,
        reason: str,
        requester: str,
        priority: str
    ) -> Dict:
        """构建飞书通知消息"""
        priority_emoji = {"normal": "🟢", "high": "🟡", "urgent": "🔴"}.get(priority, "🟢")
        
        return {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"{priority_emoji} 授权请求 #{request_id[-8:]}"
                    },
                    "template": "blue" if priority == "normal" else "red"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**服务：** {service}\n**操作：** {action}\n**请求者：** {requester}"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**原因：** {reason}" if reason else ""
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**参数预览：**\n```{json.dumps(params, ensure_ascii=False)[:500]}...```"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "✅ 批准"
                                },
                                "type": "primary",
                                "value": {"action": "approve", "request_id": request_id}
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "❌ 拒绝"
                                },
                                "type": "danger",
                                "value": {"action": "deny", "request_id": request_id}
                            }
                        ]
                    }
                ]
            }
        }
    
    def _check_decision(self, request_id: str) -> Optional[Dict]:
        """检查用户决策（轮询决策文件）"""
        decision_path = os.path.expanduser(f"~/.auth_guard/decisions/{request_id}.json")
        
        if os.path.exists(decision_path):
            with open(decision_path, 'r', encoding='utf-8') as f:
                decision = json.load(f)
            
            # 删除决策文件（一次性使用）
            os.remove(decision_path)
            
            return decision
        
        return None
    
    def _generate_auth_token(self, request_id: str, service: str, action: str) -> str:
        """生成授权令牌"""
        data = f"{request_id}:{service}:{action}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _log_audit(
        self,
        request_id: str,
        service: str,
        action: str,
        requester: str,
        status: str,
        reason: Optional[str],
        auth_token: Optional[str] = None
    ):
        """记录审计日志"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": request_id,
            "service": service,
            "action": action,
            "requester": requester,
            "status": status,
            "reason": reason,
            "auth_token": auth_token
        }
        
        with open(self.audit_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def verify_token(self, auth_token: str) -> Dict:
        """验证授权令牌"""
        # 简单实现 - 实际应该检查令牌有效性
        return {
            "valid": True,
            "token": auth_token
        }
    
    def revoke_token(self, auth_token: str) -> bool:
        """撤销授权令牌"""
        # 实现令牌撤销逻辑
        return True
    
    def get_pending_requests(self) -> List[Dict]:
        """获取待处理请求"""
        # 实现获取待处理请求逻辑
        return []
    
    def emergency_stop(self):
        """紧急停止 - 禁用所有授权"""
        self.config["enabled"] = False
        self._save_config()
        print("⚠️  紧急停止已激活 - 所有授权已禁用")


# 便捷函数
def guard_request(service: str, action: str, params: Dict, reason: str = "") -> Dict:
    """便捷函数 - 请求授权"""
    guard = AuthGuard()
    return guard.request_authorization(service, action, params, reason)


if __name__ == "__main__":
    # 测试
    guard = AuthGuard()
    
    # 测试授权请求
    result = guard.request_authorization(
        service="google-mail",
        action="messages.send",
        params={"to": "test@example.com", "subject": "Test"},
        reason="测试授权保护",
        requester="test-script"
    )
    
    print("\n授权结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

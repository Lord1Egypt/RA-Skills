"""
Feishu Bot - Main module for Feishu/Lark bot operations
"""
import os
import json
import time
import requests
from typing import Dict, List, Optional, Union


class FeishuBot:
    """Feishu Bot for messaging, group management, and approval workflows"""
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self._tenant_access_token = None
        self._token_expires_at = 0
    
    def _get_tenant_token(self) -> str:
        """Get or refresh tenant access token"""
        if self._tenant_access_token and time.time() < self._token_expires_at:
            return self._tenant_access_token
        
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        
        if result.get("code") != 0:
            raise Exception(f"Failed to get token: {result}")
        
        self._tenant_access_token = result["tenant_access_token"]
        self._token_expires_at = time.time() + result.get("expire", 7200) - 300
        return self._tenant_access_token
    
    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self._get_tenant_token()}",
            "Content-Type": "application/json"
        }
    
    # ==================== Messaging ====================
    
    def send_text(self, target: str, text: str, is_chat: bool = False) -> Dict:
        """Send text message to user or group"""
        url = f"{self.BASE_URL}/im/v1/messages"
        params = {
            "receive_id_type": "chat_id" if is_chat else "user_id"
        }
        
        data = {
            "receive_id": target,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        if is_chat:
            data["receive_id"] = target
        
        resp = requests.post(url, params=params, headers=self._headers(), json=data)
        return resp.json()
    
    def send_rich_text(self, target: str, title: str, content: str, is_chat: bool = False) -> Dict:
        """Send rich text message"""
        url = f"{self.BASE_URL}/im/v1/messages"
        params = {"receive_id_type": "chat_id" if is_chat else "user_id"}
        
        content = [
            {"tag": "h1", "content": title},
            {"tag": "text", "content": content}
        ]
        
        data = {
            "receive_id": target,
            "msg_type": "post",
            "content": json.dumps({"zh_cn": {"title": title, "content": content}})
        }
        
        resp = requests.post(url, params=params, headers=self._headers(), json=data)
        return resp.json()
    
    def send_card(self, target: str, card: Dict, is_chat: bool = False) -> Dict:
        """Send interactive card message"""
        url = f"{self.BASE_URL}/im/v1/messages"
        params = {"receive_id_type": "chat_id" if is_chat else "user_id"}
        
        data = {
            "receive_id": target,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }
        
        resp = requests.post(url, params=params, headers=self._headers(), json=data)
        return resp.json()
    
    def send_image(self, target: str, image_key: str, is_chat: bool = False) -> Dict:
        """Send image message"""
        url = f"{self.BASE_URL}/im/v1/messages"
        params = {"receive_id_type": "chat_id" if is_chat else "user_id"}
        
        data = {
            "receive_id": target,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key})
        }
        
        resp = requests.post(url, params=params, headers=self._headers(), json=data)
        return resp.json()
    
    def upload_image(self, image_path: str) -> Dict:
        """Upload image and get image_key"""
        url = f"{self.BASE_URL}/im/v1/images"
        headers = {"Authorization": f"Bearer {self._get_tenant_token()}"}
        
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"image_type": "message"}
            resp = requests.post(url, headers=headers, files=files, data=data)
        
        return resp.json()
    
    def reply_message(self, message_id: str, content: str, msg_type: str = "text") -> Dict:
        """Reply to a message"""
        url = f"{self.BASE_URL}/im/v1/messages/{message_id}/reply"
        
        data = {
            "msg_type": msg_type,
            "content": json.dumps({"text": content}) if msg_type == "text" else json.dumps(content)
        }
        
        resp = requests.post(url, headers=self._headers(), json=data)
        return resp.json()
    
    # ==================== Group Management ====================
    
    def create_group(self, name: str, user_ids: List[str] = None) -> Dict:
        """Create a new group (chat)"""
        url = f"{self.BASE_URL}/im/v1/chats"
        
        data = {
            "name": name,
            "user_id_list": user_ids or [],
            "owner_id_type": "user_id"
        }
        
        resp = requests.post(url, headers=self._headers(), json=data)
        return resp.json()
    
    def add_group_members(self, chat_id: str, user_ids: List[str]) -> Dict:
        """Add members to a group"""
        url = f"{self.BASE_URL}/im/v1/chats/{chat_id}/members"
        
        data = {"member_id_list": user_ids}
        
        resp = requests.post(url, headers=self._headers(), json=data)
        return resp.json()
    
    def remove_group_members(self, chat_id: str, user_ids: List[str]) -> Dict:
        """Remove members from a group"""
        url = f"{self.BASE_URL}/im/v1/chats/{chat_id}/members"
        
        resp = requests.delete(url, headers=self._headers(), json={"member_id_list": user_ids})
        return resp.json()
    
    def get_group_info(self, chat_id: str) -> Dict:
        """Get group information"""
        url = f"{self.BASE_URL}/im/v1/chats/{chat_id}"
        resp = requests.get(url, headers=self._headers())
        return resp.json()
    
    def get_group_members(self, chat_id: str) -> Dict:
        """Get group member list"""
        url = f"{self.BASE_URL}/im/v1/chats/{chat_id}/members"
        resp = requests.get(url, headers=self._headers())
        return resp.json()
    
    # ==================== Approval Workflows ====================
    
    def create_approval(self, approval_code: str, user_id: str, form: Dict) -> Dict:
        """Create an approval instance"""
        url = f"{self.BASE_URL}/approval/v4/instances"
        
        data = {
            "approval_code": approval_code,
            "user_id": user_id,
            "form": form
        }
        
        resp = requests.post(url, headers=self._headers(), json=data)
        return resp.json()
    
    def get_approval_instance(self, instance_id: str) -> Dict:
        """Get approval instance status"""
        url = f"{self.BASE_URL}/approval/v4/instances/{instance_id}"
        resp = requests.get(url, headers=self._headers())
        return resp.json()
    
    def cancel_approval(self, instance_id: str, user_id: str, reason: str = "") -> Dict:
        """Cancel an approval instance"""
        url = f"{self.BASE_URL}/approval/v4/instances/{instance_id}/cancel"
        
        data = {
            "user_id": user_id,
            "reason": reason
        }
        
        resp = requests.post(url, headers=self._headers(), json=data)
        return resp.json()
    
    def get_approval_list(self, approval_code: str, page_size: int = 20) -> Dict:
        """Get approval list"""
        url = f"{self.BASE_URL}/approval/v4/instances"
        params = {
            "approval_code": approval_code,
            "page_size": page_size
        }
        resp = requests.get(url, headers=self._headers(), params=params)
        return resp.json()
    
    # ==================== User Info ====================
    
    def get_user_info(self, user_id: str) -> Dict:
        """Get user information"""
        url = f"{self.BASE_URL}/contact/v3/users/{user_id}"
        resp = requests.get(url, headers=self._headers())
        return resp.json()
    
    def get_department_users(self, dept_id: str) -> Dict:
        """Get users in a department"""
        url = f"{self.BASE_URL}/contact/v3/users/find_by_department"
        params = {"department_id": dept_id}
        resp = requests.get(url, headers=self._headers(), params=params)
        return resp.json()
    
    # ==================== Webhook ====================
    
    @staticmethod
    def send_webhook(webhook_url: str, msg_type: str, content: Union[str, Dict]) -> Dict:
        """Send message via webhook (no auth required)"""
        data = {
            "msg_type": msg_type,
            "content": {"text": content} if msg_type == "text" else content
        }
        resp = requests.post(webhook_url, json=data)
        return resp.json()


def main():
    """Demo usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python feishu_bot.py <command> [args...]")
        print("Commands:")
        print("  send-text <user_id> <message>")
        print("  send-group <chat_id> <message>")
        print("  create-group <name>")
        sys.exit(1)
    
    bot = FeishuBot()
    cmd = sys.argv[1]
    
    if cmd == "send-text" and len(sys.argv) >= 4:
        result = bot.send_text(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == "send-group" and len(sys.argv) >= 4:
        result = bot.send_text(sys.argv[2], sys.argv[3], is_chat=True)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == "create-group" and len(sys.argv) >= 3:
        result = bot.create_group(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

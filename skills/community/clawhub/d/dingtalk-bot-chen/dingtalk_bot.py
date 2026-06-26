"""
DingTalk Bot - Main module for DingTalk bot operations
"""
import os
import json
import time
import hmac
import base64
import hashlib
import requests
from typing import Dict, List, Optional, Union


class DingTalkBot:
    """DingTalk Bot for messaging, group management, and approval workflows"""
    
    API_BASE = "https://oapi.dingtalk.com"
    
    def __init__(
        self,
        webhook_url: str = None,
        secret: str = None,
        app_key: str = None,
        app_secret: str = None,
        agent_id: str = None
    ):
        self.webhook_url = webhook_url or os.getenv("DINGTALK_WEBHOOK_URL")
        self.secret = secret or os.getenv("DINGTALK_SECRET")
        self.app_key = app_key or os.getenv("DINGTALK_APP_KEY")
        self.app_secret = app_secret or os.getenv("DINGTALK_APP_SECRET")
        self.agent_id = agent_id or os.getenv("DINGTALK_AGENT_ID")
        self._access_token = None
        self._token_expires_at = 0
    
    # ==================== Authentication ====================
    
    def _get_access_token(self) -> str:
        """Get or refresh access token"""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        
        url = f"{self.API_BASE}/gettoken"
        params = {"appkey": self.app_key, "appsecret": self.app_secret}
        
        resp = requests.get(url, params=params)
        result = resp.json()
        
        if result.get("errcode") != 0:
            raise Exception(f"Failed to get token: {result}")
        
        self._access_token = result["access_token"]
        self._token_expires_at = time.time() + result.get("expires_in", 7200) - 300
        return self._access_token
    
    def _generate_signature(self, timestamp: str = None) -> str:
        """Generate signature for webhook"""
        if not self.secret:
            return ""
        
        timestamp = timestamp or str(round(time.time() * 1000))
        string_to_sign = f'{timestamp}\n{self.secret}'
        
        sign = hmac.new(
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(sign).decode('utf-8')
    
    def _get_webhook_url(self) -> str:
        """Get webhook URL with signature"""
        if not self.webhook_url:
            raise ValueError("Webhook URL not configured")
        
        timestamp = str(round(time.time() * 1000))
        sign = self._generate_signature(timestamp)
        
        if sign:
            return f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
        return self.webhook_url
    
    # ==================== Webhook Messaging ====================
    
    def send_text(
        self,
        text: str,
        at_mobiles: List[str] = None,
        at_user_ids: List[str] = None,
        is_at_all: bool = False
    ) -> Dict:
        """Send text message"""
        url = self._get_webhook_url()
        
        data = {
            "msgtype": "text",
            "text": {"content": text},
            "at": {
                "atMobiles": at_mobiles or [],
                "atUserIds": at_user_ids or [],
                "isAtAll": is_at_all
            }
        }
        
        resp = requests.post(url, json=data)
        return resp.json()
    
    def send_markdown(self, title: str, text: str) -> Dict:
        """Send markdown message"""
        url = self._get_webhook_url()
        
        data = {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": text}
        }
        
        resp = requests.post(url, json=data)
        return resp.json()
    
    def send_link(
        self,
        title: str,
        text: str,
        message_url: str,
        pic_url: str = None
    ) -> Dict:
        """Send link message"""
        url = self._get_webhook_url()
        
        data = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": message_url,
                "picUrl": pic_url or ""
            }
        }
        
        resp = requests.post(url, json=data)
        return resp.json()
    
    def send_action_card(
        self,
        title: str,
        text: str,
        buttons: List[Dict[str, str]],
        btn_orientation: str = "0"
    ) -> Dict:
        """Send action card message"""
        url = self._get_webhook_url()
        
        # Single button format
        if len(buttons) == 1:
            data = {
                "msgtype": "actionCard",
                "actionCard": {
                    "title": title,
                    "text": text,
                    "btnOrientation": btn_orientation,
                    "singleTitle": buttons[0]["title"],
                    "singleURL": buttons[0]["action_url"]
                }
            }
        else:
            # Multiple buttons
            btn_json = json.dumps([
                {"title": b["title"], "actionURL": b["action_url"]}
                for b in buttons
            ])
            data = {
                "msgtype": "actionCard",
                "actionCard": {
                    "title": title,
                    "text": text,
                    "btnOrientation": btn_orientation,
                    "btns": json.loads(btn_json)
                }
            }
        
        resp = requests.post(url, json=data)
        return resp.json()
    
    def send_feed_card(self, links: List[Dict[str, str]]) -> Dict:
        """Send feed card message"""
        url = self._get_webhook_url()
        
        data = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": [
                    {
                        "title": link["title"],
                        "messageURL": link["message_url"],
                        "picURL": link.get("pic_url", "")
                    }
                    for link in links
                ]
            }
        }
        
        resp = requests.post(url, json=data)
        return resp.json()
    
    # ==================== API Messaging ====================
    
    def _api_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None
    ) -> Dict:
        """Make authenticated API request"""
        if not self.app_key or not self.app_secret:
            raise ValueError("App credentials not configured")
        
        token = self._get_access_token()
        params = params or {}
        params["access_token"] = token
        
        url = f"{self.API_BASE}{endpoint}"
        
        if method.upper() == "GET":
            resp = requests.get(url, params=params)
        else:
            resp = requests.request(method, url, params=params, json=data)
        
        result = resp.json()
        if result.get("errcode") != 0:
            raise Exception(f"API error: {result}")
        
        return result
    
    def send_to_user(self, user_id: str, msg_type: str, content: Dict) -> Dict:
        """Send message to user"""
        endpoint = "/robot/send"
        params = {"access_token": self._get_access_token()}
        
        data = {
            "agent_id": self.agent_id,
            "userid_user_id": user_id,
            "msgtype": msg_type,
            msg_type: content
        }
        
        resp = requests.post(endpoint, params=params, json=data)
        return resp.json()
    
    # ==================== Group Management ====================
    
    def create_group(
        self,
        name: str,
        owner_user_id: str,
        user_ids: List[str] = None
    ) -> Dict:
        """Create a group conversation"""
        endpoint = "/chat/create"
        
        data = {
            "name": name,
            "owner_user_id": owner_user_id,
            "useridlist": user_ids or []
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def update_group(self, chat_id: str, name: str = None, owner_user_id: str = None) -> Dict:
        """Update group info"""
        endpoint = "/chat/update"
        
        data = {"chatid": chat_id}
        if name:
            data["name"] = name
        if owner_user_id:
            data["owner_user_id"] = owner_user_id
        
        return self._api_request("POST", endpoint, data=data)
    
    def add_group_members(self, chat_id: str, user_ids: List[str]) -> Dict:
        """Add members to group"""
        endpoint = "/chat/robot/add"
        
        data = {
            "open_conversation_id": chat_id,
            "user_id_list": user_ids
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def remove_group_members(self, chat_id: str, user_ids: List[str]) -> Dict:
        """Remove members from group"""
        endpoint = "/chat/robot/remove"
        
        data = {
            "open_conversation_id": chat_id,
            "user_id_list": user_ids
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def get_group_info(self, chat_id: str) -> Dict:
        """Get group info"""
        endpoint = "/chat/get"
        return self._api_request("GET", endpoint, params={"chatid": chat_id})
    
    # ==================== Approval Workflows ====================
    
    def create_approval(
        self,
        process_code: str,
        originator_user_id: str,
        form_values: Dict
    ) -> Dict:
        """Create approval instance"""
        endpoint = "/topapi/processinstance/create"
        
        data = {
            "process_code": process_code,
            "originator_user_id": originator_user_id,
            "form_component_values": [
                {"name": k, "value": str(v)}
                for k, v in form_values.items()
            ]
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def get_approval_instance(self, process_instance_id: str) -> Dict:
        """Get approval instance status"""
        endpoint = "/topapi/processinstance/get"
        
        data = {"process_instance_id": process_instance_id}
        return self._api_request("POST", endpoint, data=data)
    
    def cancel_approval(
        self,
        process_instance_id: str,
        user_id: str,
        reason: str = ""
    ) -> Dict:
        """Cancel approval instance"""
        endpoint = "/topapi/processinstance/cancel"
        
        data = {
            "process_instance_id": process_instance_id,
            "userid": user_id,
            "reason": reason
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def list_approvals(
        self,
        process_code: str = None,
        start_time: int = None,
        end_time: int = None,
        size: int = 20
    ) -> Dict:
        """List approval instances"""
        endpoint = "/topapi/processinstance/list"
        
        data = {
            "offset": 0,
            "size": size
        }
        
        if process_code:
            data["process_code"] = process_code
        if start_time:
            data["start_time"] = start_time
        if end_time:
            data["end_time"] = end_time
        
        return self._api_request("POST", endpoint, data=data)
    
    # ==================== Attendance ====================
    
    def get_attendance_records(
        self,
        work_date: str,
        user_ids: List[str]
    ) -> Dict:
        """Get attendance records"""
        endpoint = "/topapi/attendance/listRecord"
        
        # Convert date to timestamp
        from datetime import datetime
        dt = datetime.strptime(work_date, "%Y-%m-%d")
        start_time = int(dt.timestamp() * 1000)
        end_time = start_time + 86400000  # +24 hours
        
        data = {
            "workDate": work_date,
            "userIds": user_ids,
            "startTime": start_time,
            "endTime": end_time
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    def get_vacation_balance(self, user_id: str) -> Dict:
        """Get vacation balance"""
        endpoint = "/topapi/attendance/getLeaveBalance"
        
        data = {
            "userid": user_id,
            "leave_types": []  # Empty means all types
        }
        
        return self._api_request("POST", endpoint, data=data)
    
    # ==================== User Info ====================
    
    def get_user_info(self, user_id: str) -> Dict:
        """Get user info"""
        endpoint = "/topapi/v2/user/get"
        return self._api_request("POST", endpoint, data={"userid": user_id})
    
    def get_department_users(self, dept_id: int) -> Dict:
        """Get users in department"""
        endpoint = "/topapi/v2/user/list"
        return self._api_request(
            "POST",
            endpoint,
            data={"dept_id": dept_id, "cursor": 0, "size": 100}
        )


def main():
    """Demo usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dingtalk_bot.py <command> [args...]")
        print("Commands:")
        print("  send-text <message>")
        print("  send-markdown <title> <text>")
        sys.exit(1)
    
    bot = DingTalkBot()
    cmd = sys.argv[1]
    
    if cmd == "send-text" and len(sys.argv) >= 3:
        result = bot.send_text(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == "send-markdown" and len(sys.argv) >= 4:
        result = bot.send_markdown(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Agent P2P 消息发送客户端

新架构：直接 POST 到对方 Portal 的 /api/message/receive
"""

import os
import json
import requests
from typing import Optional

class AgentP2PClient:
    """Agent P2P 消息客户端"""
    
    def __init__(self):
        self.api_key = os.environ.get('AGENTP2P_API_KEY')
        self.hub_url = os.environ.get('AGENTP2P_HUB_URL', 'https://your-domain.com')
        
        if not self.api_key:
            raise ValueError('AGENTP2P_API_KEY 未设置')
    
    def get_contacts(self) -> list:
        """获取联系人列表"""
        url = f'{self.hub_url}/api/contacts'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        resp = requests.get(url, headers=headers, verify=False)
        resp.raise_for_status()
        return resp.json()
    
    def send_message_direct(self, to_portal: str, SHARED_KEY: str, content: str, message_type: str = 'text') -> dict:
        """
        直接发送消息到对方 Portal
        
        新架构：
        Agent A → API → Portal B → WebSocket → Agent B
        
        Args:
            to_portal: 对方 Portal URL (如 https://myagentp2p.com)
            SHARED_KEY: 共享的 API Key
            content: 消息内容
            message_type: 消息类型，默认 text
        
        Returns:
            发送结果
        """
        url = f'{to_portal}/api/message/receive'
        data = {
            'api_key': SHARED_KEY,  # 共享的 Key，用于验证
            'from_portal': self.hub_url,  # 我的 Portal URL
            'content': content,
            'message_type': message_type
        }
        
        resp = requests.post(url, json=data, verify=False)
        resp.raise_for_status()
        return resp.json()
    
    def send_message_by_contact_id(self, contact_id: int, content: str, message_type: str = 'text') -> dict:
        """
        通过联系人 ID 发送消息
        
        流程：
        1. 查询联系人信息
        2. 直接 POST 到对方 Portal
        """
        # 获取联系人列表
        contacts_resp = self.get_contacts()
        contacts = contacts_resp.get('contacts', [])
        
        # 找到指定联系人
        contact = None
        for c in contacts:
            if c.get('id') == contact_id:
                contact = c
                break
        
        if not contact:
            raise ValueError(f'联系人 ID {contact_id} 不存在')
        
        to_portal = contact.get('portal_url')
        SHARED_KEY = contact.get('SHARED_KEY')  # 共享的 Key
        
        if not SHARED_KEY:
            raise ValueError(f'联系人 {contact_id} 没有 SHARED_KEY，无法发送消息')
        
        return self.send_message_direct(to_portal, SHARED_KEY, content, message_type)
    
    def get_messages(self, contact_portal: str, limit: int = 50) -> list:
        """获取与指定联系人的消息历史"""
        url = f'{self.hub_url}/api/messages/history'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {
            'contact_portal': contact_portal,
            'limit': limit
        }
        
        resp = requests.get(url, headers=headers, params=params, verify=False)
        resp.raise_for_status()
        return resp.json()

# 便捷函数
def send_message(contact_id: int, content: str) -> dict:
    """发送消息（便捷函数）"""
    client = AgentP2PClient()
    return client.send_message_by_contact_id(contact_id, content)

def get_contacts() -> list:
    """获取联系人列表（便捷函数）"""
    client = AgentP2PClient()
    return client.get_contacts()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print('用法: python3 client.py <contact_id> <message>')
        print('示例: python3 client.py 1 "你好！"')
        sys.exit(1)
    
    contact_id = int(sys.argv[1])
    message = sys.argv[2]
    
    try:
        result = send_message(contact_id, message)
        print(f'发送成功: {result}')
    except Exception as e:
        print(f'发送失败: {e}')

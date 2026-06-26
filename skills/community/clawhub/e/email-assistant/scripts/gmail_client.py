#!/usr/bin/env python3
"""
Gmail Client - Gmail API OAuth 对接
使用 google-auth 和 google-auth-oauthlib 实现 OAuth2 认证

使用前需要:
1. 在 Google Cloud Console 创建项目
2. 启用 Gmail API
3. 下载 credentials.json 到脚本目录
4. 首次运行会打开浏览器进行授权

功能:
- 获取邮件列表
- 读取邮件内容
- 标记重要邮件 (STARRED)
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API 权限范围
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]


class GmailClient:
    """Gmail API 客户端"""
    
    def __init__(self, credentials_path: str = 'credentials.json', 
                 token_path: str = 'token.pickle'):
        """
        初始化 Gmail 客户端
        
        Args:
            credentials_path: OAuth 客户端配置文件路径
            token_path: 保存访问令牌的路径
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """进行 OAuth2 认证"""
        creds = None
        
        # 尝试加载已保存的令牌
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # 如果没有有效凭证，进行认证
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # 刷新过期凭证
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"刷新令牌失败: {e}")
                    creds = None
            else:
                # 进行完整 OAuth 流程
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"未找到 {self.credentials_path}\n"
                        "请先在 Google Cloud Console 创建 OAuth 客户端并下载配置文件\n"
                        "详见: https://developers.google.com/gmail/api/quickstart/python"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    authorization_prompt_message=
                        "请访问以下网址授权: {url}"
                )
            
            # 保存凭证
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # 构建 Gmail 服务
        self.service = build('gmail', 'v1', credentials=creds)
        print("✓ Gmail API 认证成功")
    
    def get_emails(self, max_results: int = 10, 
                   query: str = '',
                   label_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        获取邮件列表
        
        Args:
            max_results: 最大返回数量
            query: Gmail 搜索语法
            label_ids: 按标签过滤 (INBOX, STARRED, etc.)
        
        Returns:
            邮件列表
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query,
                labelIds=label_ids
            ).execute()
            
            messages = results.get('messages', [])
            return messages
            
        except HttpError as e:
            print(f"获取邮件列表失败: {e}")
            return []
    
    def get_email_detail(self, msg_id: str) -> Optional[Dict[str, Any]]:
        """
        获取邮件详细内容
        
        Args:
            msg_id: 邮件ID
        
        Returns:
            邮件详情字典
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            return self._parse_message(message)
            
        except HttpError as e:
            print(f"获取邮件详情失败: {e}")
            return None
    
    def _parse_message(self, message: dict) -> Dict[str, Any]:
        """解析邮件消息"""
        headers = message.get('payload', {}).get('headers', [])
        
        # 提取标准头部
        def get_header(name: str) -> str:
            for header in headers:
                if header['name'].lower() == name.lower():
                    return header['value']
            return ''
        
        # 解析内容
        payload = message.get('payload', {})
        body = self._get_body(payload)
        
        return {
            'id': message['id'],
            'threadId': message.get('threadId'),
            'subject': get_header('subject'),
            'from': get_header('from'),
            'to': get_header('to'),
            'date': get_header('date'),
            'labels': message.get('labelIds', []),
            'snippet': message.get('snippet', ''),
            'body': body,
            'raw': message.get('raw')
        }
    
    def _get_body(self, payload: dict) -> str:
        """从 payload 中提取邮件正文"""
        # 直接 body
        if 'body' in payload and payload['body'].get('data'):
            import base64
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        # 多部分消息
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    if 'body' in part and part['body'].get('data'):
                        import base64
                        data = part['body']['data']
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part.get('mimeType') == 'text/html':
                    if 'body' in part and part['body'].get('data'):
                        import base64
                        data = part['body']['data']
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        return ''
    
    def mark_important(self, msg_id: str) -> bool:
        """
        标记邮件为重要 (添加 STARRED 标签)
        
        Args:
            msg_id: 邮件ID
        
        Returns:
            是否成功
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={
                    'addLabelIds': ['STARRED'],
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()
            return True
        except HttpError as e:
            print(f"标记邮件失败: {e}")
            return False
    
    def mark_as_read(self, msg_id: str) -> bool:
        """
        标记邮件为已读
        
        Args:
            msg_id: 邮件ID
        
        Returns:
            是否成功
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()
            return True
        except HttpError as e:
            print(f"标记已读失败: {e}")
            return False
    
    def get_recent_emails(self, days: int = 7, max_results: int = 20) -> List[Dict[str, Any]]:
        """获取最近几天的邮件"""
        # 计算日期
        date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query = f'after:{date}'
        
        messages = self.get_emails(max_results=max_results, query=query)
        
        # 获取详细信息
        emails = []
        for msg in messages:
            detail = self.get_email_detail(msg['id'])
            if detail:
                emails.append(detail)
        
        return emails


# 示例用法
if __name__ == '__main__':
    try:
        # 初始化客户端 (需要 credentials.json)
        client = GmailClient()
        
        # 获取最近邮件
        print("\n=== 最近 5 封邮件 ===")
        emails = client.get_emails(max_results=5)
        
        for msg in emails:
            detail = client.get_email_detail(msg['id'])
            if detail:
                print(f"\n标题: {detail['subject']}")
                print(f"发件人: {detail['from']}")
                print(f"日期: {detail['date']}")
                print(f"预览: {detail['snippet'][:100]}...")
        
        # 标记第一封邮件为重要
        if emails:
            print(f"\n标记邮件 {emails[0]['id']} 为重要...")
            client.mark_important(emails[0]['id'])
            
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("\n请按以下步骤操作:")
        print("1. 访问 https://console.cloud.google.com/")
        print("2. 创建项目并启用 Gmail API")
        print("3. 创建 OAuth 2.0 客户端凭证")
        print("4. 下载 JSON 文件并重命名为 credentials.json")
    except Exception as e:
        print(f"错误: {e}")

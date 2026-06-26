#!/usr/bin/env python3
"""
Feishu Sender - 飞书消息发送工具模块
支持：文本消息、任意格式文件发送

Usage:
    from feishu_sender import FeishuSender
    
    sender = FeishuSender()
    
    # 发送文本
    sender.send_text("早安！☀️", chat_id="oc_xxx")
    
    # 发送文件
    sender.send_file("/path/to/document.docx", chat_id="oc_xxx")
    
    # 批量发送
    sender.send_batch(
        text="今日报告",
        files=["report.docx", "data.xlsx"],
        chat_id="oc_xxx"
    )
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, List, Union
from dataclasses import dataclass


@dataclass
class FeishuConfig:
    """飞书配置"""
    app_id: str
    app_secret: str
    default_chat_id: Optional[str] = None
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "FeishuConfig":
        """从环境变量或 .env 文件加载配置"""
        if env_file and os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        return cls(
            app_id=os.environ.get("FEISHU_APP_ID", ""),
            app_secret=os.environ.get("FEISHU_APP_SECRET", ""),
            default_chat_id=os.environ.get("FEISHU_CHAT_ID")
        )


class FeishuSender:
    """
    飞书消息发送器
    
    支持的消息类型：
    - text: 纯文本
    - file: 文件（docx, pdf, md, xlsx, pptx 等）
    - image: 图片（需要额外实现）
    """
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    # 文件扩展名到飞书 file_type 的映射
    FILE_TYPE_MAP = {
        '.docx': 'doc',
        '.doc': 'doc',
        '.pdf': 'pdf',
        '.txt': 'stream',
        '.md': 'stream',
        '.markdown': 'stream',
        '.xlsx': 'xls',
        '.xls': 'xls',
        '.pptx': 'ppt',
        '.ppt': 'ppt',
        '.csv': 'stream',
        '.json': 'stream',
        '.py': 'stream',
        '.js': 'stream',
        '.html': 'stream',
        '.zip': 'stream',
    }
    
    # 支持的图片格式
    IMAGE_TYPES = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    def __init__(self, config: Optional[FeishuConfig] = None):
        """
        初始化发送器
        
        Args:
            config: 飞书配置，如果为 None 则从环境变量自动加载
        """
        self.config = config or FeishuConfig.from_env()
        self._token: Optional[str] = None
        self._token_expires: float = 0
    
    def _get_token(self) -> Optional[str]:
        """获取 tenant_access_token（带缓存）"""
        import time
        
        # 检查缓存是否有效（提前 60 秒刷新）
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        
        if not self.config.app_id or not self.config.app_secret:
            raise ValueError("未配置 FEISHU_APP_ID 或 FEISHU_APP_SECRET")
        
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                self._token = data["tenant_access_token"]
                # token 有效期通常为 2 小时（7200 秒）
                self._token_expires = time.time() + data.get("expire", 7200)
                return self._token
            else:
                raise RuntimeError(f"获取 token 失败: {data}")
        except requests.RequestException as e:
            raise RuntimeError(f"请求 token 失败: {e}")
    
    def _upload_image(self, image_path: str) -> str:
        """
        上传图片到飞书
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            image_key: 飞书图片标识符
        """
        token = self._get_token()
        url = f"{self.BASE_URL}/im/v1/images"
        
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 检查是否为支持的图片格式
        file_ext = image_path.suffix.lower()
        if file_ext not in self.IMAGE_TYPES:
            raise ValueError(f"不支持的图片格式: {file_ext}，支持: {', '.join(self.IMAGE_TYPES)}")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(image_path, 'rb') as f:
            files = {'image': (image_path.name, f)}
            data = {'image_type': 'message'}  # message: 用于发送消息
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                return result["data"]["image_key"]
            else:
                raise RuntimeError(f"上传图片失败: {result}")
    
    def _upload_file(self, file_path: str) -> str:
        """
        上传文件到飞书
        
        Args:
            file_path: 本地文件路径
            
        Returns:
            file_key: 飞书文件标识符
        """
        token = self._get_token()
        url = f"{self.BASE_URL}/im/v1/files"
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_name = file_path.name
        file_ext = file_path.suffix.lower()
        file_type = self.FILE_TYPE_MAP.get(file_ext, 'stream')
        
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            data = {
                'file_type': file_type,
                'file_name': file_name
            }
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                return result["data"]["file_key"]
            else:
                raise RuntimeError(f"上传文件失败: {result}")
    
    def send_text(
        self, 
        content: str, 
        chat_id: Optional[str] = None,
        receive_id_type: str = "chat_id"
    ) -> dict:
        """
        发送文本消息
        
        Args:
            content: 消息内容
            chat_id: 目标会话 ID，默认使用配置中的 default_chat_id
            receive_id_type: 接收者类型 (chat_id | open_id | user_id | email)
            
        Returns:
            API 响应数据
        """
        token = self._get_token()
        target_id = chat_id or self.config.default_chat_id
        
        if not target_id:
            raise ValueError("未指定 chat_id，且未配置默认 chat_id")
        
        url = f"{self.BASE_URL}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": target_id,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }
        
        params = {"receive_id_type": receive_id_type}
        
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise RuntimeError(f"发送消息失败: {result}")
    
    def send_file(
        self, 
        file_path: str, 
        chat_id: Optional[str] = None,
        receive_id_type: str = "chat_id"
    ) -> dict:
        """
        发送文件
        
        Args:
            file_path: 本地文件路径
            chat_id: 目标会话 ID
            receive_id_type: 接收者类型
            
        Returns:
            API 响应数据
        """
        token = self._get_token()
        target_id = chat_id or self.config.default_chat_id
        
        if not target_id:
            raise ValueError("未指定 chat_id，且未配置默认 chat_id")
        
        # 先上传文件
        file_key = self._upload_file(file_path)
        
        # 再发送文件消息
        url = f"{self.BASE_URL}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": target_id,
            "msg_type": "file",
            "content": json.dumps({"file_key": file_key})
        }
        
        params = {"receive_id_type": receive_id_type}
        
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise RuntimeError(f"发送文件失败: {result}")
    
    def send_batch(
        self,
        text: Optional[str] = None,
        files: Optional[List[str]] = None,
        chat_id: Optional[str] = None,
        receive_id_type: str = "chat_id"
    ) -> List[dict]:
        """
        批量发送（文本 + 多个文件）
        
        Args:
            text: 文本消息内容
            files: 文件路径列表
            chat_id: 目标会话 ID
            receive_id_type: 接收者类型
            
        Returns:
            所有发送结果的列表
        """
        results = []
        
        if text:
            results.append(self.send_text(text, chat_id, receive_id_type))
        
        if files:
            for file_path in files:
                results.append(self.send_file(file_path, chat_id, receive_id_type))
        
        return results
    
    def _upload_image(self, image_path: str) -> str:
        """
        上传图片到飞书
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            image_key: 飞书图片标识符
        """
        token = self._get_token()
        url = f"{self.BASE_URL}/im/v1/images"
        
        file_path = Path(image_path)
        if not file_path.exists():
            raise FileNotFoundError(f"图片不存在: {file_path}")
        
        file_ext = file_path.suffix.lower()
        if file_ext not in self.IMAGE_TYPES:
            raise ValueError(f"不支持的图片格式: {file_ext}，支持的格式: {self.IMAGE_TYPES}")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(file_path, 'rb') as f:
            files = {'image': (file_path.name, f)}
            data = {'image_type': 'message'}
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                return result["data"]["image_key"]
            else:
                raise RuntimeError(f"上传图片失败: {result}")
    
    def send_image(
        self,
        image_path: str,
        chat_id: Optional[str] = None,
        receive_id_type: str = "chat_id"
    ) -> dict:
        """
        发送图片消息
        
        Args:
            image_path: 本地图片路径（支持 jpg, png, gif 等）
            chat_id: 目标会话 ID
            receive_id_type: 接收者类型
            
        Returns:
            API 响应数据
        """
        token = self._get_token()
        target_id = chat_id or self.config.default_chat_id
        
        if not target_id:
            raise ValueError("未指定 chat_id，且未配置默认 chat_id")
        
        # 先上传图片
        image_key = self._upload_image(image_path)
        
        # 再发送图片消息
        url = f"{self.BASE_URL}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": target_id,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key})
        }
        
        params = {"receive_id_type": receive_id_type}
        
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise RuntimeError(f"发送图片失败: {result}")
    
    def send_markdown(
        self,
        content: str,
        chat_id: Optional[str] = None,
        receive_id_type: str = "chat_id"
    ) -> dict:
        """
        发送 Markdown 格式消息（飞书会将 markdown 渲染为富文本）
        
        Args:
            content: Markdown 内容
            chat_id: 目标会话 ID
            receive_id_type: 接收者类型
        """
        # 飞书的 post 消息类型支持 markdown
        token = self._get_token()
        target_id = chat_id or self.config.default_chat_id
        
        if not target_id:
            raise ValueError("未指定 chat_id，且未配置默认 chat_id")
        
        url = f"{self.BASE_URL}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 构建 post 类型的内容（支持 markdown）
        payload = {
            "receive_id": target_id,
            "msg_type": "post",
            "content": json.dumps({
                "zh_cn": {
                    "title": "",
                    "content": [
                        [{"tag": "text", "text": content}]
                    ]
                }
            })
        }
        
        params = {"receive_id_type": receive_id_type}
        
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise RuntimeError(f"发送 markdown 失败: {result}")


# CLI 支持
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书消息发送工具')
    parser.add_argument('--text', '-t', help='发送文本消息')
    parser.add_argument('--file', '-f', help='发送文件')
    parser.add_argument('--chat-id', '-c', help='目标会话 ID')
    parser.add_argument('--env', '-e', help='环境变量文件路径')
    
    args = parser.parse_args()
    
    # 加载配置
    config = FeishuConfig.from_env(args.env)
    sender = FeishuSender(config)
    
    try:
        if args.text:
            result = sender.send_text(args.text, args.chat_id)
            print(f"✅ 文本发送成功: {result.get('message_id', 'unknown')}")
        
        if args.file:
            result = sender.send_file(args.file, args.chat_id)
            print(f"✅ 文件发送成功: {result.get('message_id', 'unknown')}")
        
        if not args.text and not args.file:
            parser.print_help()
            
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        exit(1)

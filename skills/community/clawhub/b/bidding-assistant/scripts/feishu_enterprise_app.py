#!/usr/bin/env python3
"""
飞书企业自建应用客户端
基于飞书开放平台官方文档实现
支持发送文件到用户或群聊
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# 尝试导入requests，失败时使用urllib
try:
    import requests
except ImportError:
    import urllib.request as requests


def get_config():
    """从OpenClaw配置读取飞书凭证"""
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        feishu = config.get('channels', {}).get('feishu', {})
        account = feishu.get('accounts', {}).get('default', {})
        return account.get('appId'), account.get('appSecret')
    except Exception as e:
        logger.warning(f"读取飞书配置失败: {e}")
        return None, None


class FeishuEnterpriseApp:
    """飞书企业自建应用客户端"""

    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化飞书企业自建应用客户端

        Args:
            app_id: 飞书应用ID（可选，默认从OpenClaw配置读取）
            app_secret: 飞书应用Secret（可选，默认从OpenClaw配置读取）
        """
        # 优先使用传入的参数，否则从配置读取
        self.app_id = app_id
        self.app_secret = app_secret

        if not self.app_id or not self.app_secret:
            config_app_id, config_app_secret = get_config()
            self.app_id = self.app_id or config_app_id
            self.app_secret = self.app_secret or config_app_secret

        if not self.app_id or not self.app_secret:
            logger.error("未配置飞书应用凭证，请设置环境变量或OpenClaw配置")

        self.tenant_access_token = None
        self.base_url = "https://open.feishu.cn/open-apis"

    def get_tenant_access_token(self) -> Optional[str]:
        """获取 tenant_access_token"""
        if not self.app_id or not self.app_secret:
            logger.error("未配置飞书应用凭证")
            return None

        try:
            url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
            headers = {"Content-Type": "application/json; charset=utf-8"}
            data = {"app_id": self.app_id, "app_secret": self.app_secret}

            response = requests.post(url, headers=headers, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    self.tenant_access_token = result['tenant_access_token']
                    logger.debug("获取 tenant_access_token 成功")
                    return self.tenant_access_token
                else:
                    logger.error(f"获取 tenant_access_token 失败: {result.get('msg')}")
                    return None
            else:
                logger.error(f"获取 tenant_access_token 失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"获取 tenant_access_token 异常: {e}")
            return None

    def _ensure_token(self) -> bool:
        """确保有有效的token"""
        if not self.tenant_access_token:
            return bool(self.get_tenant_access_token())
        return True

    def upload_file(self, file_path: str, parent_type: str = "explorer") -> Optional[str]:
        """
        上传文件到飞书云空间

        Args:
            file_path: 本地文件路径
            parent_type: 父节点类型，默认 "explorer"（云文档）

        Returns:
            file_token，失败返回None
        """
        if not self._ensure_token():
            return None

        try:
            url = f"{self.base_url}/drive/v1/medias/upload_all"
            headers = {"Authorization": f"Bearer {self.tenant_access_token}"}

            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            # 根据文件扩展名确定文件类型（飞书API用字符串类型如"pdf"）
            file_ext = os.path.splitext(filename)[1].lower()
            file_type_map = {
                '.pdf': 'pdf',
                '.doc': 'doc',
                '.docx': 'docx',
                '.xls': 'xls',
                '.xlsx': 'xlsx',
                '.png': 'image',
                '.jpg': 'image',
                '.jpeg': 'image',
                '.gif': 'image',
                '.txt': 'text',
            }
            file_type = file_type_map.get(file_ext, 'file')

            with open(file_path, 'rb') as f:
                file_content = f.read()

            # 关键：使用 application/octet-stream，file_type 用字符串如 "pdf"
            files = {'file': (filename, file_content, 'application/octet-stream')}
            data = {
                'file_name': filename,
                'parent_type': parent_type,
                'size': str(file_size),
                'file_type': file_type  # 用字符串如 "pdf"，不要用数字如 "12"
            }

            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    file_token = result['data']['file_token']
                    logger.info(f"文件上传成功: {filename} -> {file_token}")
                    return file_token
                else:
                    logger.error(f"文件上传失败: {result.get('msg')}")
                    return None
            else:
                logger.error(f"文件上传失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"上传文件异常: {e}")
            return None

    def send_file_message(self, receive_id: str, file_path: str,
                          receive_id_type: str = "open_id",
                          file_name: Optional[str] = None) -> bool:
        """
        发送文件消息到用户或群聊

        关键：必须使用IM API上传文件（/im/v1/files），获取file_key用于消息发送

        Args:
            receive_id: 接收者ID（open_id 或 chat_id）
            file_path: 本地文件路径
            receive_id_type: 接收者ID类型，默认 "open_id"（用户），也可设为 "chat_id"（群聊）
            file_name: 文件名（可选，默认使用原文件名）

        Returns:
            是否发送成功
        """
        if not self._ensure_token():
            return False

        # 1. 使用IM API上传文件获取 file_key
        logger.info(f"上传文件: {file_path}")
        file_key = self._upload_im_file(file_path)
        if not file_key:
            logger.error("文件上传失败，无法发送")
            return False

        # 2. 发送文件消息
        logger.info(f"发送文件消息: receive_id={receive_id}, file_key={file_key}")

        try:
            url = f"{self.base_url}/im/v1/messages?receive_id_type={receive_id_type}"
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": "application/json; charset=utf-8"
            }

            # 使用 file_key（不是 file_token）
            msg_content = json.dumps({"file_key": file_key})
            msg_data = {
                "receive_id": receive_id,
                "msg_type": "file",
                "content": msg_content,
                "file_name": file_name or os.path.basename(file_path)
            }

            response = requests.post(url, headers=headers, json=msg_data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    logger.info(f"文件消息发送成功: {file_path}")
                    return True
                else:
                    logger.error(f"文件消息发送失败: {result.get('msg')} (code={result.get('code')})")
                    return False
            else:
                logger.error(f"文件消息发送失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"发送文件消息异常: {e}")
            return False

    def _upload_im_file(self, file_path: str) -> Optional[str]:
        """
        使用IM API上传文件，获取file_key

        Args:
            file_path: 本地文件路径

        Returns:
            file_key，失败返回None
        """
        try:
            url = f"{self.base_url}/im/v1/files"
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            # 根据扩展名确定file_type
            file_ext = os.path.splitext(filename)[1].lower()
            file_type_map = {
                '.pdf': 'pdf',
                '.doc': 'doc',
                '.docx': 'docx',
                '.xls': 'xls',
                '.xlsx': 'xlsx',
                '.png': 'png',
                '.jpg': 'jpg',
                '.jpeg': 'jpeg',
                '.gif': 'gif',
                '.mp4': 'mp4',
                '.mp3': 'mp3',
            }
            file_type = file_type_map.get(file_ext, 'pdf')

            with open(file_path, 'rb') as f:
                file_content = f.read()

            files = {'file': (filename, file_content, 'application/octet-stream')}
            data = {
                'file_name': filename,
                'file_type': file_type,
                'file_size': str(file_size)
            }
            headers = {"Authorization": f"Bearer {self.tenant_access_token}"}

            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    file_key = result['data']['file_key']
                    logger.info(f"IM文件上传成功: {filename} -> {file_key}")
                    return file_key
                else:
                    logger.error(f"IM文件上传失败: {result.get('msg')}")
                    return None
            else:
                logger.error(f"IM文件上传失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"IM文件上传异常: {e}")
            return None

    def send_text_message(self, receive_id: str, text: str,
                          receive_id_type: str = "open_id") -> bool:
        """
        发送文本消息

        Args:
            receive_id: 接收者ID
            text: 消息内容
            receive_id_type: 接收者ID类型，默认 "open_id"

        Returns:
            是否发送成功
        """
        if not self._ensure_token():
            return False

        try:
            url = f"{self.base_url}/im/v1/messages?receive_id_type={receive_id_type}"
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": "application/json; charset=utf-8"
            }

            msg_data = {
                "receive_id": receive_id,
                "msg_type": "text",
                "content": json.dumps({"text": text})
            }

            response = requests.post(url, headers=headers, json=msg_data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    logger.info(f"文本消息发送成功")
                    return True
                else:
                    logger.error(f"文本消息发送失败: {result.get('msg')}")
                    return False
            else:
                logger.error(f"文本消息发送失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"发送文本消息异常: {e}")
            return False

    def send_local_file(self, receive_id: str, file_path: str,
                        receive_id_type: str = "open_id",
                        file_name: Optional[str] = None) -> bool:
        """
        直接发送本地文件到飞书用户/群聊（封装了上传和发送两步）

        Args:
            receive_id: 接收者ID（open_id 或 chat_id）
            file_path: 本地文件路径
            receive_id_type: 接收者ID类型，默认 "open_id"
            file_name: 文件名（可选）

        Returns:
            是否发送成功
        """
        return self.send_file_message(receive_id, file_path, receive_id_type, file_name)


if __name__ == '__main__':
    # 测试
    app = FeishuEnterpriseApp()

    # 测试获取token
    token = app.get_tenant_access_token()
    if token:
        print(f"✅ Token获取成功")
    else:
        print("❌ Token获取失败")
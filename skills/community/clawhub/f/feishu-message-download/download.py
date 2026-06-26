#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息文件下载器
从飞书消息中下载视频、图片、文档等文件到本地
"""

import os
import sys
import re
import json
import argparse
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any


class FeishuMessageDownloader:
    """飞书消息文件下载器"""
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化下载器
        
        Args:
            app_id: 飞书应用ID，如果不提供则从配置或环境变量读取
            app_secret: 飞书应用Secret，如果不提供则从配置或环境变量读取
        """
        self.app_id = app_id or self._get_app_id()
        self.app_secret = app_secret or self._get_app_secret()
        self._access_token: Optional[str] = None
    
    def _get_app_id(self) -> str:
        """从配置或环境变量获取 App ID"""
        # 优先从环境变量获取
        app_id = os.environ.get("FEISHU_APP_ID")
        if app_id:
            return app_id
        
        # 尝试从 OpenClaw 配置读取 (支持驼峰和下划线命名)
        config_paths = [
            Path.home() / ".openclaw" / "openclaw.json",
            Path.home() / ".openclaw" / "config.json",
        ]
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        # 检查 channels.feishu (OpenClaw 配置格式)
                        if "channels" in config and "feishu" in config["channels"]:
                            feishu_config = config["channels"]["feishu"]
                            # 支持驼峰命名 (appId) 和下划线命名 (app_id)
                            if "appId" in feishu_config:
                                return feishu_config["appId"]
                            if "app_id" in feishu_config:
                                return feishu_config["app_id"]
                        # 检查直接的 feishu 配置
                        if "feishu" in config:
                            feishu_config = config["feishu"]
                            if "appId" in feishu_config:
                                return feishu_config["appId"]
                            if "app_id" in feishu_config:
                                return feishu_config["app_id"]
                except Exception:
                    pass
        
        raise ValueError(
            "未找到飞书 App ID，请通过以下方式之一配置：\n"
            "1. 设置环境变量 FEISHU_APP_ID\n"
            "2. 在 OpenClaw 配置文件中设置 feishu.app_id"
        )
    
    def _get_app_secret(self) -> str:
        """从配置或环境变量获取 App Secret"""
        # 优先从环境变量获取
        app_secret = os.environ.get("FEISHU_APP_SECRET")
        if app_secret:
            return app_secret
        
        # 尝试从 OpenClaw 配置读取 (支持驼峰和下划线命名)
        config_paths = [
            Path.home() / ".openclaw" / "openclaw.json",
            Path.home() / ".openclaw" / "config.json",
        ]
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        # 检查 channels.feishu (OpenClaw 配置格式)
                        if "channels" in config and "feishu" in config["channels"]:
                            feishu_config = config["channels"]["feishu"]
                            # 支持驼峰命名 (appSecret) 和下划线命名 (app_secret)
                            if "appSecret" in feishu_config:
                                return feishu_config["appSecret"]
                            if "app_secret" in feishu_config:
                                return feishu_config["app_secret"]
                        # 检查直接的 feishu 配置
                        if "feishu" in config:
                            feishu_config = config["feishu"]
                            if "appSecret" in feishu_config:
                                return feishu_config["appSecret"]
                            if "app_secret" in feishu_config:
                                return feishu_config["app_secret"]
                except Exception:
                    pass
        
        raise ValueError(
            "未找到飞书 App Secret，请通过以下方式之一配置：\n"
            "1. 设置环境变量 FEISHU_APP_SECRET\n"
            "2. 在 OpenClaw 配置文件中设置 feishu.app_secret"
        )
    
    def _get_access_token(self) -> str:
        """获取 tenant_access_token"""
        if self._access_token:
            return self._access_token
        
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 access token 失败: {result.get('msg')}")
            
            self._access_token = result["tenant_access_token"]
            return self._access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求 access token 失败: {str(e)}")
    
    def _parse_message_url(self, url: str) -> Dict[str, str]:
        """
        从飞书消息链接中解析 message_id 和其他信息
        
        Args:
            url: 飞书消息链接
            
        Returns:
            包含 message_id 等信息的字典
        """
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        result = {}
        
        # 尝试从 URL 路径中提取 message_id
        # 飞书消息链接格式: https://open.feishu.cn/im/xxx?... 或其他格式
        path_parts = parsed.path.strip('/').split('/')
        
        # 从查询参数中获取 message_id
        if 'message_id' in query_params:
            result['message_id'] = query_params['message_id'][0]
        elif 'msg_id' in query_params:
            result['message_id'] = query_params['msg_id'][0]
        
        # 从查询参数中获取 file_key
        if 'file_key' in query_params:
            result['file_key'] = query_params['file_key'][0]
        
        return result
    
    def get_message_info(self, message_id: str) -> Dict[str, Any]:
        """
        获取消息详情，提取 file_key
        
        Args:
            message_id: 消息ID
            
        Returns:
            消息详情字典
        """
        token = self._get_access_token()
        url = f"{self.BASE_URL}/im/v1/messages/{message_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取消息信息失败: {result.get('msg')}")
            
            return result.get("data", {})
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求消息信息失败: {str(e)}")
    
    def extract_file_key_from_message(self, message_info: Dict[str, Any]) -> Optional[str]:
        """
        从消息信息中提取 file_key
        
        Args:
            message_info: 消息详情
            
        Returns:
            file_key 或 None
        """
        message = message_info.get("message", {})
        content = message.get("content", "{}")
        
        try:
            if isinstance(content, str):
                content = json.loads(content)
        except json.JSONDecodeError:
            return None
        
        msg_type = message.get("msg_type", "")
        
        # 根据消息类型提取 file_key
        if msg_type == "file":
            return content.get("file_key")
        elif msg_type == "image":
            return content.get("image_key")
        elif msg_type == "media":
            return content.get("file_key")
        elif msg_type == "video":
            return content.get("file_key")
        
        # 尝试从 content 中直接获取
        if "file_key" in content:
            return content["file_key"]
        if "image_key" in content:
            return content["image_key"]
        
        return None
    
    def download_file(
        self, 
        message_id: str, 
        file_key: str, 
        output_dir: str = ".",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        下载文件
        
        Args:
            message_id: 消息ID
            file_key: 文件key
            output_dir: 输出目录
            filename: 保存的文件名，如果不提供则使用原始文件名
            
        Returns:
            包含下载结果的字典
        """
        token = self._get_access_token()
        
        # 构建下载 URL
        url = f"{self.BASE_URL}/im/v1/messages/{message_id}/resources/{file_key}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "type": "file"
        }
        
        try:
            # 发送下载请求
            response = requests.get(url, headers=headers, params=params, stream=True)
            response.raise_for_status()
            
            # 从响应头或内容中获取文件名
            if not filename:
                content_disposition = response.headers.get("Content-Disposition", "")
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[-1].strip('"')
                else:
                    # 使用 file_key 作为默认文件名
                    filename = file_key
            
            # 确保输出目录存在
            output_path = Path(output_dir).expanduser().resolve()
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            file_path = output_path / filename
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = file_path.stat().st_size
            
            return {
                "success": True,
                "file_path": str(file_path),
                "file_size": file_size,
                "filename": filename
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"下载文件失败: {str(e)}"
            }
    
    def download_from_message_url(
        self, 
        message_url: str, 
        output_dir: str = ".",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从消息链接下载文件
        
        Args:
            message_url: 飞书消息链接
            output_dir: 输出目录
            filename: 保存的文件名
            
        Returns:
            包含下载结果的字典
        """
        # 解析消息链接
        parsed = self._parse_message_url(message_url)
        message_id = parsed.get("message_id")
        file_key = parsed.get("file_key")
        
        if not message_id:
            return {
                "success": False,
                "error": "无法从链接中解析出 message_id"
            }
        
        # 如果没有 file_key，尝试从消息信息中提取
        if not file_key:
            try:
                message_info = self.get_message_info(message_id)
                file_key = self.extract_file_key_from_message(message_info)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"获取消息信息失败: {str(e)}"
                }
        
        if not file_key:
            return {
                "success": False,
                "error": "无法获取 file_key，请确认消息包含文件"
            }
        
        return self.download_file(message_id, file_key, output_dir, filename)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="从飞书消息中下载文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过消息链接下载
  python download.py --url "https://open.feishu.cn/im/xxx" --output ~/Downloads
  
  # 通过消息ID和file_key下载
  python download.py --message-id "om_xxxxxxxx" --file-key "file_xxxxxxxx" --output ~/Downloads
  
  # 指定保存文件名
  python download.py --message-id "om_xxxxxxxx" --file-key "file_xxxxxxxx" --filename "video.mp4"
        """
    )
    
    parser.add_argument(
        "--url", "-u",
        help="飞书消息链接"
    )
    parser.add_argument(
        "--message-id", "-m",
        help="消息ID (om_xxx)"
    )
    parser.add_argument(
        "--file-key", "-f",
        help="文件key (file_xxx)"
    )
    parser.add_argument(
        "--output", "-o",
        default=".",
        help="输出目录，默认为当前目录"
    )
    parser.add_argument(
        "--filename", "-n",
        help="保存的文件名"
    )
    parser.add_argument(
        "--app-id",
        help="飞书应用ID（可选，默认从配置读取）"
    )
    parser.add_argument(
        "--app-secret",
        help="飞书应用Secret（可选，默认从配置读取）"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.url and not args.message_id:
        parser.error("请提供 --url 或 --message-id 参数")
    
    if args.message_id and not args.file_key and not args.url:
        parser.error("使用 --message-id 时必须提供 --file-key")
    
    # 初始化下载器
    try:
        downloader = FeishuMessageDownloader(
            app_id=args.app_id,
            app_secret=args.app_secret
        )
    except ValueError as e:
        print(f"配置错误: {e}")
        sys.exit(1)
    
    # 执行下载
    try:
        if args.url:
            result = downloader.download_from_message_url(
                message_url=args.url,
                output_dir=args.output,
                filename=args.filename
            )
        else:
            result = downloader.download_file(
                message_id=args.message_id,
                file_key=args.file_key,
                output_dir=args.output,
                filename=args.filename
            )
        
        if result["success"]:
            print(f"✅ 文件下载成功!")
            print(f"   文件路径: {result['file_path']}")
            print(f"   文件大小: {result['file_size']:,} bytes")
            print(f"   文件名: {result['filename']}")
        else:
            print(f"❌ 下载失败: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

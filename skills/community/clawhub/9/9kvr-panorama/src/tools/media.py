"""媒体素材管理工具模块

提供媒体素材的管理功能，包括：
- list_media: 获取素材列表
- get_media_info: 获取素材详情
- update_media_info: 更新素材信息
- delete_media: 删除素材
- upload_media: 上传素材
- download_media: 获取下载链接
"""

import base64
import json
import os
import urllib.parse
from typing import Any, Dict, List, Optional, Union

from ..api import get_api
from ..config import get_config
from ..utils.response import format_success, format_error


# 素材预览链接基础地址
PREVIEW_URL_BASE = "https://dev.9kvr.cn/tour/media/media-collection"


class MediaTools:
    """媒体素材管理工具类"""

    def __init__(self):
        """初始化媒体工具"""
        self.config = get_config()
        self.api = get_api()

    def _get_content_type(self, filename: str) -> str:
        """根据文件扩展名获取 Content-Type

        Args:
            filename: 文件名

        Returns:
            Content-Type
        """
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "mp4": "video/mp4",
            "mp3": "audio/mpeg",
            "mpeg": "audio/mpeg",
            "wav": "audio/wav",
        }
        return types.get(ext, "application/octet-stream")

    def _get_media_type_name(self, media_type: int) -> str:
        """获取素材类型名称

        Args:
            media_type: 素材类型编号

        Returns:
            类型名称
        """
        type_map = {
            1: "图片",
            2: "视频",
            4: "3D模型",
            5: "3D模型",
            6: "矩阵图",
            7: "3D模型",
            8: "3D模型",
        }
        return type_map.get(media_type, "未知类型")

    def _format_media_response(self, response: Dict[str, Any], response_type: str = "list") -> Dict[str, Any]:
        """格式化素材响应

        Args:
            response: API 响应数据
            response_type: 响应类型：'list' 列表，'single' 单个

        Returns:
            格式化后的响应
        """
        if response.get("code") == 1 and response.get("info"):
            info = response["info"]
            media_list = []

            if response_type == "list":
                # 列表响应：response.info.data 是数组
                media_list = info.get("data", []) if isinstance(info, dict) else []
            else:
                # 单个响应：response.info 是对象
                media_list = [info] if isinstance(info, dict) else []

            # 添加预览链接
            for item in media_list:
                if isinstance(item, dict):
                    media_id = item.get("imgs_id")
                    if media_id:
                        item["preview_url"] = f"{PREVIEW_URL_BASE}?id={media_id}"

            # 添加提示信息
            response["_format_reminder"] = """

---
**重要提示：这是媒体素材（图片、视频、音频等普通媒体文件），不是全景素材！**

**概念说明：**
- **媒体素材**：存储在素材库中的普通文件（图片、视频、音频等）
- **全景素材**：组成全景作品的场景，需要通过 get_work_scenes 工具获取

**格式要求：**
1. 使用 Markdown 表格或列表展示素材数据
2. 将所有 URL 字段转换为可点击的 Markdown 链接格式
3. 突出重要信息（如素材名称、预览链接等）
"""

        return response

    def list_media(
        self,
        limit: int = 12,
        page: int = 1,
        keyword: str = "",
        media_type: str = "",
        status: int = 2
    ) -> Dict[str, Any]:
        """获取素材列表

        Args:
            limit: 每页数量，默认12，最大30
            page: 页码，默认1
            keyword: 搜索关键词
            media_type: 素材类型筛选
            status: 状态筛选，默认2（转码完成）

        Returns:
            素材列表响应
        """
        # 限制每页最多30条
        if limit > 30:
            limit = 30
        if limit < 1:
            limit = 12

        try:
            response = self.api.post("/api/media/getList", data={
                "limit": limit,
                "page": page,
                "keyword": keyword,
                "type": media_type,
                "status": status,
            })

            # 格式化响应
            formatted = self._format_media_response(response, "list")
            return format_success(data=formatted)
        except Exception as e:
            return format_error(f"获取素材列表失败: {str(e)}", code=1)

    def get_media_info(self, id: int) -> Dict[str, Any]:
        """获取素材详情

        Args:
            id: 素材ID

        Returns:
            素材详情响应
        """
        if not id:
            return format_error("素材ID是必需的", code=1)

        try:
            response = self.api.post("/api/media/getMediaInfo", data={"id": id})

            # 格式化响应
            formatted = self._format_media_response(response, "single")
            return format_success(data=formatted)
        except Exception as e:
            return format_error(f"获取素材详情失败: {str(e)}", code=1)

    def update_media_info(
        self,
        id: int,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """更新素材信息

        Args:
            id: 素材ID
            name: 新的名称
            description: 新的描述

        Returns:
            更新结果响应
        """
        if not id:
            return format_error("素材ID是必需的", code=1)
        if not name:
            return format_error("素材名称是必需的", code=1)

        try:
            response = self.api.post("/api/media/changeName", data={
                "id": id,
                "name": name,
                "desc": description,
            })
            return format_success(data=response)
        except Exception as e:
            return format_error(f"更新素材信息失败: {str(e)}", code=1)

    def delete_media(self, ids: List[int]) -> Dict[str, Any]:
        """删除素材

        Args:
            ids: 素材ID数组

        Returns:
            删除结果响应
        """
        if not ids or len(ids) == 0:
            return format_error("至少需要提供一个素材ID", code=1)

        try:
            response = self.api.post("/api/media/delMedia", data={"id": ids})
            return format_success(data=response)
        except Exception as e:
            return format_error(f"删除素材失败: {str(e)}", code=1)

    def upload_media(
        self,
        file: Union[str, bytes],
        filename: str,
        name: str = "素材文件",
        description: str = "",
        group: int = 1
    ) -> Dict[str, Any]:
        """上传素材

        Args:
            file: 文件路径或 Base64 编码的文件内容
            filename: 文件名（包含扩展名）
            name: 素材名称
            description: 素材描述
            group: 素材分组ID

        Returns:
            上传结果响应
        """
        if not file:
            return format_error("文件内容是必需的", code=1)
        if not filename:
            return format_error("文件名是必需的", code=1)

        try:
            # 准备文件数据
            file_buffer: bytes
            if isinstance(file, str):
                if file.startswith("data:"):
                    # Base64 编码的文件
                    base64_data = file.split(",", 1)[1] if "," in file else file
                    file_buffer = base64.b64decode(base64_data)
                elif os.path.exists(file):
                    # 文件路径
                    with open(file, "rb") as f:
                        file_buffer = f.read()
                else:
                    return format_error("无效的文件路径或Base64数据", code=1)
            else:
                file_buffer = file

            # 步骤1: 上传文件到服务器（使用 ApiService.multipart_upload）
            upload_response = self.api.multipart_upload(
                "/api/upload/uploadExtraFile",
                files={"file": (filename, file_buffer, self._get_content_type(filename))}
            )

            if upload_response.get("code") != 1:
                return format_error(f"上传失败: {upload_response.get('msg', '未知错误')}", code=1)

            # 步骤2: 从返回的URL中提取key（去掉域名部分）
            file_url = upload_response.get("info", "")
            if not file_url:
                return format_error("上传响应中未找到文件URL", code=1)

            # 提取路径
            if file_url.startswith("http://") or file_url.startswith("https://"):
                try:
                    parsed = urllib.parse.urlparse(file_url)
                    key = parsed.path.lstrip("/")
                except Exception:
                    # 手动提取
                    parts = file_url.split("/")
                    key = "/".join(parts[3:]) if len(parts) > 3 else file_url
            else:
                key = file_url

            # 步骤3: 保存到素材库
            save_response = self.api.post("/api/upload/saveMyMedia", data={
                "key": key,
                "size": len(file_buffer),
                "group": group,
                "name": name,
            })

            if save_response.get("code") != 1:
                return format_error(f"保存素材库失败: {save_response.get('msg', '未知错误')}", code=1)

            # 返回成功结果
            result = {
                "success": True,
                "media_id": save_response.get("info"),
                "file_url": file_url,
                "message": "上传成功，文件已保存到素材库",
            }
            return format_success(data=result)
        except Exception as e:
            return format_error(f"上传素材失败: {str(e)}", code=1)

    def download_media(
        self,
        id: str,
        ans: int = 0
    ) -> Dict[str, Any]:
        """获取素材下载链接

        Args:
            id: 加密的素材ID（从素材列表的 imgs_download 字段获取）
            ans: 是否强制获取（1=强制，0=不强制）

        Returns:
            下载链接响应
        """
        if not id:
            return format_error("素材ID是必需的", code=1)

        try:
            response = self.api.post("/api/media/downloadMediaFile", data={
                "id": id,
                "ans": ans,
            })
            return format_success(data=response)
        except Exception as e:
            return format_error(f"获取下载链接失败: {str(e)}", code=1)


# MCP 工具定义函数（供外部调用）
def get_media_tools() -> List[Dict[str, Any]]:
    """获取媒体工具定义列表

    Returns:
        工具定义列表
    """
    return [
        {
            "name": "list_media",
            "description": """获取用户的**媒体素材**列表（图片、视频、音频等普通媒体文件），支持分页、关键词搜索和筛选。**重要说明：**媒体素材是存储在素材库中的普通文件（图片、视频、音频等），与全景素材不同。全景素材是组成全景作品的场景，需要通过 get_work_scenes 工具获取。**重要：**每次查询默认只返回12条数据，这是系统限制。如需查看更多数据，请使用分页参数（page）逐页查询。严禁一次查询超过30条数据。**注意：**素材的图片和视频会直接显示，CDN链接受保护不允许复制。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "每页数量，默认12，最大30"},
                    "page": {"type": "number", "description": "页码，默认1"},
                    "keyword": {"type": "string", "description": "搜索关键词"},
                    "type": {"type": "string", "description": "素材类型筛选"},
                    "status": {"type": "number", "description": "状态筛选，默认2（转码完成）"},
                },
            },
        },
        {
            "name": "get_media_info",
            "description": """获取单个**媒体素材**的详细信息（图片、视频、音频等普通媒体文件）。**注意：**这是媒体素材，不是全景素材。全景素材需要通过 get_work_scenes 工具获取。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "素材ID"},
                },
                "required": ["id"],
            },
        },
        {
            "name": "update_media_info",
            "description": """更新**媒体素材**的名称和描述""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "素材ID"},
                    "name": {"type": "string", "description": "新的名称"},
                    "description": {"type": "string", "description": "新的描述"},
                },
                "required": ["id", "name"],
            },
        },
        {
            "name": "delete_media",
            "description": """删除**媒体素材**（移入回收站）""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {"type": "array", "items": {"type": "number"}, "description": "素材ID数组"},
                },
                "required": ["ids"],
            },
        },
        {
            "name": "upload_media",
            "description": """上传**媒体素材**（图片、视频、音频等普通媒体文件）到用户素材库""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "文件路径或Base64编码的文件内容"},
                    "filename": {"type": "string", "description": "文件名（包含扩展名）"},
                    "name": {"type": "string", "description": "素材名称，默认为素材文件"},
                    "description": {"type": "string", "description": "素材描述"},
                    "group": {"type": "number", "description": "素材分组ID，默认1"},
                },
                "required": ["file", "filename"],
            },
        },
        {
            "name": "download_media",
            "description": """获取**媒体素材**的下载链接""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "加密的素材ID（从素材列表的imgs_download字段获取）"},
                    "ans": {"type": "number", "description": "是否强制获取（1=强制，0=不强制）"},
                },
                "required": ["id"],
            },
        },
    ]


def handle_media_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """处理媒体工具调用

    Args:
        name: 工具名称
        args: 工具参数

    Returns:
        工具执行结果
    """
    tools = MediaTools()

    if name == "list_media":
        return tools.list_media(
            limit=args.get("limit", 12),
            page=args.get("page", 1),
            keyword=args.get("keyword", ""),
            media_type=args.get("type", ""),
            status=args.get("status", 2),
        )
    elif name == "get_media_info":
        return tools.get_media_info(id=args["id"])
    elif name == "update_media_info":
        return tools.update_media_info(
            id=args["id"],
            name=args["name"],
            description=args.get("description", ""),
        )
    elif name == "delete_media":
        return tools.delete_media(ids=args["ids"])
    elif name == "upload_media":
        return tools.upload_media(
            file=args["file"],
            filename=args["filename"],
            name=args.get("name", "素材文件"),
            description=args.get("description", ""),
            group=args.get("group", 1),
        )
    elif name == "download_media":
        return tools.download_media(
            id=args["id"],
            ans=args.get("ans", 0),
        )
    else:
        return format_error(f"未知工具: {name}", code=1)

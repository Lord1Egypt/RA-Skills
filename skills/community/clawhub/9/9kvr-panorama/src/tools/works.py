"""作品管理工具模块

提供全景作品的管理功能，包括：
- list_works: 获取作品列表
- get_work_info: 获取作品详情
- get_work_scenes: 获取作品场景
- update_work_info: 更新作品信息
- create_work_from_media: 从素材创建作品
"""

import json
import urllib.parse
from typing import Any, Dict, List, Optional, Union

from ..api import get_api
from ..config import get_config
from ..utils.response import format_success, format_error, format_list


# 播放链接基础域名
PLAY_URL_BASE = "https://9kvr.cn/tour/index"


class WorksTools:
    """作品管理工具类"""

    def __init__(self):
        """初始化作品工具"""
        self.config = get_config()
        self.api = get_api()

    def _format_play_url(self, work_id: Union[str, int]) -> str:
        """构建播放链接

        Args:
            work_id: 作品ID

        Returns:
            播放链接
        """
        return f"{PLAY_URL_BASE}?id={work_id}"

    def _get_copy_link_reminder(self) -> str:
        """获取链接字段说明"""
        return """

---
**链接字段说明（copyLink）：**

返回数据中包含 `copyLink` 对象，包含以下链接字段：

1. **mini** (`pages/tour/wait?id=xxx`) - 小程序普通链接，用于公众号文章插入
2. **h5** (`https://web.9kvr.cn/d/xxx.html`) - WEB网页链接，可以直接在浏览器中打开
3. **v1** (`pages/tour/index?id=xxx`) - 小程序直达链接，需要VIP权限
4. **mp** (`https://web.9kvr.cn/jump/go/xxx.html`) - 唤起微信链接，用于在微信中唤起小程序

**格式要求：**
1. 使用 Markdown 表格或列表展示作品数据
2. 将所有 URL 字段转换为可点击的 Markdown 链接格式
3. 不要直接返回原始 JSON 数据给用户
"""

    def list_works(
        self,
        limit: int = 3,
        page: int = 1,
        keyword: str = "",
        pid: int = 0,
        cv: int = 1,
        vr_type: int = 0,
        sys_tag: int = 0,
        type_vr: int = 0,
        send_time: int = 0,
        fail_show: int = 0,
        start_time: str = "",
        end_time: str = ""
    ) -> Dict[str, Any]:
        """获取作品列表

        Args:
            limit: 每页数量，默认3，最大30
            page: 页码，默认1
            keyword: 搜索关键词
            pid: 目录ID，默认0
            cv: 控制是否显示制作中的，默认1
            vr_type: 全景等级筛选
            sys_tag: 筛选条件：1=精品，2=推荐，3=私有，4=公开
            type_vr: 作品类型筛选
            send_time: 时间排序：0=降序，1=升序
            fail_show: 是否显示制作失败的，默认0
            start_time: 开始时间，格式：YYYY-MM-DD HH:mm:ss
            end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss

        Returns:
            作品列表响应
        """
        # 限制每页最多30条
        if limit > 30:
            limit = 30
        if limit < 1:
            limit = 3

        # 构建请求数据
        request_data = {
            "limit": limit,
            "page": page,
            "keyword": keyword,
            "pid": pid,
            "cv": cv,
            "vrType": vr_type,
            "sysTag": sys_tag,
            "typeVr": type_vr,
            "sendTime": send_time,
            "failShow": fail_show,
        }

        # 添加时间区间参数
        if start_time:
            request_data["start_time"] = start_time
        if end_time:
            request_data["end_time"] = end_time

        # 发送请求
        try:
            response = self.api.post("/api/tour/getList", data=request_data)

            # 添加播放链接和格式说明
            if response.get("code") == 1 and response.get("info"):
                info = response["info"]
                if isinstance(info, dict) and "data" in info:
                    for work in info["data"]:
                        work_id = work.get("id") or work.get("work_id")
                        if work_id:
                            work["play_url"] = self._format_play_url(work_id)

            # 添加链接字段说明
            response["_format_reminder"] = self._get_copy_link_reminder()

            return format_success(data=response)
        except Exception as e:
            return format_error(f"获取作品列表失败: {str(e)}", code=1)

    def get_work_info(self, id: str) -> Dict[str, Any]:
        """获取作品详情

        Args:
            id: 作品ID（支持加密ID）

        Returns:
            作品详情响应
        """
        if not id:
            return format_error("作品ID是必需的", code=1)

        try:
            response = self.api.post("/api/tour/info", data={"id": id})

            # 添加播放链接
            if response.get("code") == 1 and response.get("info"):
                work_id = response["info"].get("id") or response["info"].get("work_id")
                if work_id:
                    response["info"]["play_url"] = self._format_play_url(work_id)

            # 添加链接字段说明
            if isinstance(response.get("info"), dict):
                response["info"]["_format_reminder"] = self._get_copy_link_reminder()

            return format_success(data=response)
        except Exception as e:
            return format_error(f"获取作品详情失败: {str(e)}", code=1)

    def get_work_scenes(self, id: str) -> Dict[str, Any]:
        """获取作品场景列表

        Args:
            id: 作品ID（支持加密ID）

        Returns:
            场景列表响应
        """
        if not id:
            return format_error("作品ID是必需的", code=1)

        try:
            response = self.api.post("/api/tour/getScene", data={"id": id})

            # 添加格式说明
            scene_reminder = """

---
**重要说明：这是全景素材（场景）数据，不是媒体素材！**

**概念说明：**
- **全景素材**：组成全景作品的场景，一个全景作品由多个全景素材（场景）组成
- **媒体素材**：存储在素材库中的普通文件（图片、视频、音频等）

**格式要求：**
1. 使用 Markdown 表格或列表展示全景素材（场景）数据
2. 将所有 URL 字段转换为可点击的 Markdown 链接格式
3. 不要直接返回原始 JSON 数据给用户
4. 突出重要信息（如场景名称、场景链接等）
"""
            if response.get("code") == 1:
                if isinstance(response.get("info"), dict):
                    response["info"]["_scene_reminder"] = scene_reminder
                elif isinstance(response.get("info"), list):
                    response["_scene_reminder"] = scene_reminder

            return format_success(data=response)
        except Exception as e:
            return format_error(f"获取作品场景失败: {str(e)}", code=1)

    def update_work_info(
        self,
        id: int,
        name: str,
        work_profile: str = "",
        work_private: Optional[int] = None,
        work_password: Optional[str] = None,
        cover: Optional[str] = None
    ) -> Dict[str, Any]:
        """更新作品信息

        Args:
            id: 作品ID
            name: 作品名称
            work_profile: 作品描述
            work_private: 是否私有：0=公开，1=私有
            work_password: 访问密码
            cover: 封面素材ID（数字，必须从媒体素材库中选择）

        Returns:
            更新结果响应
        """
        if not id:
            return format_error("作品ID是必需的", code=1)
        if not name:
            return format_error("作品名称是必需的", code=1)

        try:
            # 如果提供了封面，先处理封面更新
            if cover:
                cover_str = str(cover).strip()
                if not cover_str.isdigit():
                    return format_error("封面参数必须是素材ID（数字），只能从媒体素材库中选择", code=1)

                # 获取素材信息
                try:
                    media_response = self.api.post("/api/media/getMediaInId", data={
                        "id": [int(cover_str)],
                        "comeType": 0
                    })

                    if media_response.get("code") != 1 or not media_response.get("info"):
                        return format_error("获取素材信息失败：素材不存在或已删除", code=1)

                    media_info = media_response["info"]
                    if isinstance(media_info, list) and len(media_info) > 0:
                        media_info = media_info[0]
                    elif not isinstance(media_info, dict):
                        return format_error("获取素材信息失败：素材数据格式错误", code=1)

                    # 优先使用 imgs_location（原始路径）
                    full_url = media_info.get("imgs_location") or media_info.get("imgs_thumb") or ""
                    if not full_url:
                        return format_error("素材信息中未找到图片URL", code=1)

                    # 去掉域名，只保留路径部分
                    cover_url = self._extract_path_from_url(full_url)

                    # 调用修改封面接口
                    cover_response = self.api.post("/api/scan/editThumb", data={
                        "img": cover_url,
                        "work_id": id,
                        "editModel": 1,  # 1表示修改作品封面
                    })

                    if cover_response.get("code") != 1:
                        return format_error(f"更新封面失败：{cover_response.get('msg', '未知错误')}", code=1)

                except Exception as e:
                    return format_error(f"更新封面失败: {str(e)}", code=1)

            # 更新作品基本信息
            request_data = {
                "work_id": id,
                "work_name": name,
                "work_profile": work_profile or "",
            }

            # 添加可选字段
            if work_private is not None:
                request_data["work_private"] = work_private
            if work_password is not None:
                request_data["work_password"] = work_password

            response = self.api.post("/api/tour/saveInfo", data=request_data)

            return format_success(data=response)
        except Exception as e:
            return format_error(f"更新作品信息失败: {str(e)}", code=1)

    def create_work_from_media(
        self,
        media_ids: List[int],
        name: str,
        desc: str = ""
    ) -> Dict[str, Any]:
        """从素材创建作品

        Args:
            media_ids: 全景素材ID数组，至少需要1个素材ID
            name: 作品名称
            desc: 作品描述

        Returns:
            创建结果响应
        """
        if not media_ids or len(media_ids) == 0:
            return format_error("至少需要提供一个全景素材ID", code=1)

        if not name:
            return format_error("作品名称是必需的", code=1)

        try:
            # 获取素材信息，构建 imgs 数组
            imgs_list = []

            for media_id in media_ids:
                try:
                    media_response = self.api.post("/api/media/getMediaInfo", data={"id": media_id})

                    if media_response.get("code") != 1 or not media_response.get("info"):
                        return format_error(f"素材ID {media_id} 不存在或获取失败", code=1)

                    media_info = media_response["info"]

                    # 检查素材状态（必须是已完成制作的素材，状态为2）
                    if media_info.get("imgs_status") != 2:
                        return format_error(
                            f"素材ID {media_id} 尚未完成制作，无法用于创建作品。素材状态：{media_info.get('imgs_status')}",
                            code=1
                        )

                    # 构建素材信息
                    imgs_list.append({
                        "imgs_id": media_id,
                        "imgs_thumb": media_info.get("imgs_thumb") or media_info.get("imgs_location") or "",
                    })
                except Exception as e:
                    return format_error(f"获取素材ID {media_id} 信息失败: {str(e)}", code=1)

            # 构建请求参数
            request_data = {
                "imgs": json.dumps(imgs_list),
                "name": name,
                "desc": desc,
            }

            # 调用接口
            response = self.api.post("/api/mcp/createWorkFromMedia", data=request_data)

            # 添加播放链接
            if response.get("code") == 1 and response.get("info"):
                work_id = response["info"].get("id") or response["info"].get("work_id")
                if work_id:
                    response["info"]["play_url"] = self._format_play_url(work_id)

            return format_success(data=response)
        except Exception as e:
            return format_error(f"创建作品失败: {str(e)}", code=1)

    def _extract_path_from_url(self, url: str) -> str:
        """从完整 URL 中提取路径部分

        Args:
            url: 完整 URL

        Returns:
            路径部分（不带开头的/）
        """
        if not url:
            return url

        if url.startswith("http://") or url.startswith("https://"):
            try:
                parsed = urllib.parse.urlparse(url)
                path = parsed.path
                return path.lstrip("/") if path.startswith("/") else path
            except Exception:
                # 如果解析失败，尝试手动提取
                match = url.match(r"https?://[^/]+(/.+)")
                if match:
                    return match.group(1).lstrip("/")
                return url
        else:
            # 已经是相对路径
            return url.lstrip("/")


# MCP 工具定义函数（供外部调用）
def get_works_tools() -> List[Dict[str, Any]]:
    """获取作品工具定义列表

    Returns:
        工具定义列表
    """
    return [
        {
            "name": "list_works",
            "description": """获取用户的全景作品列表，支持分页、关键词搜索和筛选。**重要说明：**全景作品是由多个全景素材（场景）组成的完整作品。一个全景作品包含多个全景素材，每个全景素材是一个场景。媒体素材（图片、视频、音频等）是存储在素材库中的普通文件，与全景素材不同。默认返回3条数据，用户可以通过分页查看更多。严禁一次查询超过30条数据。**播放链接格式：**全景作品的播放链接格式为 `https://9kvr.cn/tour/index?id=作品ID`，其中 `作品ID` 是作品的ID。**注意：**工具返回的是 JSON 格式的原始数据，你必须将其格式化为易读的 Markdown 格式（表格或列表），并将所有 URL 字段（包括播放链接）转换为可点击的 Markdown 链接格式。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "每页数量，默认3，最大30"},
                    "page": {"type": "number", "description": "页码，默认1"},
                    "keyword": {"type": "string", "description": "搜索关键词，支持按作品名称搜索"},
                    "pid": {"type": "number", "description": "目录ID，默认0"},
                    "cv": {"type": "number", "description": "控制是否显示制作中的，默认1"},
                    "vr_type": {"type": "number", "description": "全景等级筛选"},
                    "sys_tag": {"type": "number", "description": "筛选条件：1=精品，2=推荐，3=私有，4=公开"},
                    "type_vr": {"type": "number", "description": "作品类型筛选"},
                    "send_time": {"type": "number", "description": "时间排序：0=降序，1=升序"},
                    "fail_show": {"type": "number", "description": "是否显示制作失败的，默认0"},
                    "start_time": {"type": "string", "description": "开始时间，格式：YYYY-MM-DD HH:mm:ss"},
                    "end_time": {"type": "string", "description": "结束时间，格式：YYYY-MM-DD HH:mm:ss"},
                },
            },
        },
        {
            "name": "get_work_info",
            "description": """获取单个全景作品的详细信息。**重要说明：**全景作品是由多个全景素材（场景）组成的完整作品。要查看作品包含的所有全景素材，需要使用 get_work_scenes 工具。**播放链接格式：**全景作品的播放链接格式为 `https://9kvr.cn/tour/index?id=作品ID`，其中 `作品ID` 是作品的ID。**注意：**工具返回的是 JSON 格式的原始数据，你必须将其格式化为易读的 Markdown 格式，并将所有 URL 字段（包括播放链接）转换为可点击的 Markdown 链接格式。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "作品ID（支持加密ID）"},
                },
                "required": ["id"],
            },
        },
        {
            "name": "get_work_scenes",
            "description": """获取全景作品的所有**全景素材**（场景）列表。**重要说明：**全景素材是组成全景作品的场景，一个全景作品由多个全景素材组成。这与媒体素材（图片、视频、音频等普通文件）不同，媒体素材存储在素材库中，用于上传、管理、作为作品封面等。全景素材是作品的一部分，每个全景素材代表作品中的一个场景。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "作品ID（支持加密ID）"},
                },
                "required": ["id"],
            },
        },
        {
            "name": "update_work_info",
            "description": """更新全景作品的基本信息（名称、描述、封面等）。**重要说明：**封面只能从媒体素材库选择，需要提供媒体素材ID（数字）。媒体素材是存储在素材库中的普通文件（图片、视频、音频等），与全景素材不同。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "作品ID"},
                    "name": {"type": "string", "description": "作品名称"},
                    "work_profile": {"type": "string", "description": "作品描述"},
                    "work_private": {"type": "number", "description": "是否私有：0=公开，1=私有"},
                    "work_password": {"type": "string", "description": "访问密码（可选）"},
                    "cover": {"type": "string", "description": "封面素材ID（数字，必须从媒体素材库中选择）"},
                },
                "required": ["id", "name"],
            },
        },
        {
            "name": "create_work_from_media",
            "description": """将多个全景素材发布为一个全景作品。**重要说明：**此工具用于从素材库中选择多个已完成的全景素材（全景图片），将它们组合成一个全景作品。素材必须是已完成制作的全景素材（状态为2），可以通过 list_media 工具获取素材列表。**播放链接格式：**创建成功后，全景作品的播放链接格式为 `https://9kvr.cn/tour/index?id=作品ID`，其中 `作品ID` 是创建成功后返回的作品ID。**注意：**工具返回的是 JSON 格式的原始数据，你必须将其格式化为易读的 Markdown 格式，并将所有 URL 字段（包括播放链接）转换为可点击的 Markdown 链接格式。""",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "media_ids": {
                        "type": "array",
                        "description": "全景素材ID数组，至少需要1个素材ID。素材必须是已完成制作的全景素材（状态为2）",
                        "items": {"type": "number"},
                        "minItems": 1,
                    },
                    "name": {"type": "string", "description": "作品名称"},
                    "desc": {"type": "string", "description": "作品描述（可选）"},
                },
                "required": ["media_ids", "name"],
            },
        },
    ]


def handle_works_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """处理作品工具调用

    Args:
        name: 工具名称
        args: 工具参数

    Returns:
        工具执行结果
    """
    tools = WorksTools()

    if name == "list_works":
        return tools.list_works(
            limit=args.get("limit", 3),
            page=args.get("page", 1),
            keyword=args.get("keyword", ""),
            pid=args.get("pid", 0),
            cv=args.get("cv", 1),
            vr_type=args.get("vr_type", 0),
            sys_tag=args.get("sys_tag", 0),
            type_vr=args.get("type_vr", 0),
            send_time=args.get("send_time", 0),
            fail_show=args.get("fail_show", 0),
            start_time=args.get("start_time", ""),
            end_time=args.get("end_time", ""),
        )
    elif name == "get_work_info":
        return tools.get_work_info(id=args["id"])
    elif name == "get_work_scenes":
        return tools.get_work_scenes(id=args["id"])
    elif name == "update_work_info":
        return tools.update_work_info(
            id=args["id"],
            name=args["name"],
            work_profile=args.get("work_profile", ""),
            work_private=args.get("work_private"),
            work_password=args.get("work_password"),
            cover=args.get("cover"),
        )
    elif name == "create_work_from_media":
        return tools.create_work_from_media(
            media_ids=args["media_ids"],
            name=args["name"],
            desc=args.get("desc", ""),
        )
    else:
        return format_error(f"未知工具: {name}", code=1)

"""语音工具模块

提供语音主播、语音生成、配音文件上传等功能：
- get_voice_anchors: 获取AI主播列表
- generate_voice_narration: 生成语音讲解（异步）
- query_voice_result: 查询生成结果
- upload_voice_file: 上传配音文件
- add_voice_narration: 添加语音到作品
"""

import json
import base64
import re
from typing import Any, Dict, Optional, List

from ..api import get_api
from ..config import get_config
from ..utils.response import format_success, format_error, format_list


class VoiceTools:
    """语音工具类"""

    def __init__(self):
        """初始化语音工具"""
        self.config = get_config()
        self.api = get_api()

    def get_tools(self) -> List[Dict[str, Any]]:
        """获取工具列表

        Returns:
            工具定义列表
        """
        return [
            {
                "name": "get_voice_anchors",
                "description": "获取语音主播列表，支持按性别筛选。用于文字生成语音时选择主播。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "来源，默认'auto'"
                        },
                        "gender": {
                            "type": "string",
                            "description": "性别筛选，'male'=男声，'female'=女声（通过scene字段判断）"
                        },
                    },
                },
            },
            {
                "name": "generate_voice_narration",
                "description": "根据文字内容生成语音讲解音频（异步处理）。**重要说明：**此接口采用异步处理方式，不会立即返回音频URL。生成时间约15-30秒，需要通过 query_voice_result 工具查询生成结果。每个IP每天最多使用3次免费（除非使用useToken）。文字内容最多支持300个字符。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要转换的文字内容（最多300字符）"
                        },
                        "anchor_key": {
                            "type": "string",
                            "description": "主播ID（从主播列表获取的 key 字段，如：'zh-CN-XiaoxiaoNeural'）"
                        },
                        "source": {
                            "type": "string",
                            "description": "来源标识，默认'MCP工具'"
                        },
                        "useToken": {
                            "type": "string",
                            "description": "可选访问令牌，用于受限网络环境（示例：'<ACCESS_TOKEN>'）"
                        },
                    },
                    "required": ["text", "anchor_key"],
                },
            },
            {
                "name": "query_voice_result",
                "description": "查询语音生成任务的结果。**重要说明：**生成过程需要15-30秒，建议轮询查询。如果生成完成，返回音频URL；如果未完成，返回错误提示，需要稍后重试。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID（从 generate_voice_narration 返回）"
                        },
                    },
                    "required": ["task_id"],
                },
            },
            {
                "name": "upload_voice_file",
                "description": "上传已生成的配音音频文件。**重要说明：**如果用户已有配音文件，优先使用此方式，避免重复生成。支持MP3格式。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file": {
                            "type": "string",
                            "description": "音频文件路径或Base64编码的文件内容"
                        },
                        "filename": {
                            "type": "string",
                            "description": "文件名（包含扩展名，如：voice.mp3）"
                        },
                    },
                    "required": ["file", "filename"],
                },
            },
            {
                "name": "add_voice_narration",
                "description": "为全景作品添加语音讲解。**重要说明：**语音会保存到场景的 config_music 字段中的 bgm 字段。voice_url 可以是生成的URL或上传的URL。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（支持加密ID）"
                        },
                        "voice_url": {
                            "type": "string",
                            "description": "语音文件URL（可以是生成的URL或上传的URL）"
                        },
                        "loop": {
                            "type": "number",
                            "description": "是否循环播放，默认1（1=循环，0=不循环）"
                        },
                        "voice": {
                            "type": "number",
                            "description": "音量大小，默认100（0-100）"
                        },
                    },
                    "required": ["work_id", "voice_url"],
                },
            },
        ]

    def has_tool(self, name: str) -> bool:
        """检查是否有指定工具

        Args:
            name: 工具名称

        Returns:
            是否存在
        """
        tool_names = [tool["name"] for tool in self.get_tools()]
        return name in tool_names

    def handle_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具调用

        Args:
            name: 工具名称
            args: 工具参数

        Returns:
            处理结果
        """
        if name == "get_voice_anchors":
            return self.get_voice_anchors(args)
        elif name == "generate_voice_narration":
            return self.generate_voice_narration(args)
        elif name == "query_voice_result":
            return self.query_voice_result(args)
        elif name == "upload_voice_file":
            return self.upload_voice_file(args)
        elif name == "add_voice_narration":
            return self.add_voice_narration(args)
        else:
            return format_error(f"Unknown tool: {name}")

    def get_voice_anchors(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """获取语音主播列表

        Args:
            args: 包含 source, gender 的字典

        Returns:
            主播列表响应
        """
        source = args.get("source", "auto")
        gender = args.get("gender")

        try:
            response = self.api.post("/api/mcp/getVoiceAnchors", data={"source": source})

            if response.get("code") != 1 or "info" not in response:
                return format_error(
                    response.get("msg") or "获取主播列表失败：未知错误"
                )

            anchors = response.get("info", [])

            # 根据性别筛选
            if gender:
                anchors = self._filter_by_gender(anchors, gender)

            # 格式化输出
            result_anchors = []
            for anchor in anchors:
                result_anchors.append({
                    "id": anchor.get("id"),
                    "key": anchor.get("key"),
                    "name": anchor.get("name"),
                    "scene": anchor.get("scene"),
                    "type": anchor.get("type"),
                    "mp3": anchor.get("mp3"),
                    "maxlength": anchor.get("maxlength"),
                    "maxlengthBig": anchor.get("maxlengthBig"),
                })

            return format_success({
                "total": len(result_anchors),
                "anchors": result_anchors
            })

        except Exception as e:
            return format_error(f"获取主播列表失败: {str(e)}")

    def _filter_by_gender(self, anchors: List[Dict], gender: str) -> List[Dict]:
        """根据性别筛选主播

        Args:
            anchors: 主播列表
            gender: 性别 (male/female)

        Returns:
            筛选后的主播列表
        """
        if not gender:
            return anchors

        filtered = []
        for anchor in anchors:
            scene = (anchor.get("scene") or "").lower()
            if gender == "male" and "男" in scene:
                filtered.append(anchor)
            elif gender == "female" and "女" in scene:
                filtered.append(anchor)

        return filtered

    def generate_voice_narration(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """生成语音讲解（异步处理）

        Args:
            args: 包含 text, anchor_key, source, useToken 的字典

        Returns:
            任务响应
        """
        text = args.get("text")
        anchor_key = args.get("anchor_key")
        source = args.get("source", "MCP工具")
        use_token = args.get("useToken")

        # 参数验证
        if not text:
            return format_error("文字内容是必需的")
        if not anchor_key:
            return format_error("主播ID是必需的")

        # 检查文字长度
        if len(text) > 300:
            return format_error("文字内容超过300字符限制，请缩短内容")

        try:
            request_data = {
                "anchor": anchor_key,
                "text": text,
                "source": source,
            }

            if use_token:
                request_data["useToken"] = use_token

            response = self.api.post("/api/mcp/generateVoice", data=request_data)

            if response.get("code") != 1:
                return format_error(
                    response.get("msg") or "提交语音生成任务失败"
                )

            # 提取任务ID
            info = response.get("info", {})
            task_id = info.get("id") or ""
            query_url = info.get("query") or ""

            return format_success({
                "message": "语音生成任务已提交，正在生成中...",
                "task_id": task_id,
                "query_url": query_url,
                "note": "生成时间约15-30秒，请使用 query_voice_result 工具查询生成结果"
            })

        except Exception as e:
            return format_error(f"生成语音失败: {str(e)}")

    def query_voice_result(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """查询语音生成结果

        Args:
            args: 包含 task_id 的字典

        Returns:
            查询结果
        """
        task_id = args.get("task_id")

        if not task_id:
            return format_error("任务ID是必需的")

        try:
            # 从query URL中提取id，或直接使用task_id
            id_value = task_id
            if "id=" in task_id:
                match = re.search(r"id=([^&]+)", task_id)
                if match:
                    id_value = match.group(1)

            response = self.api.post("/api/mcp/queryVoiceResult", data={"id": id_value, "fast": 1})

            if response.get("code") == 1 and response.get("info"):
                # 生成成功
                return format_success({
                    "message": "语音生成成功",
                    "audio_url": response.get("info"),
                    "task_id": id_value
                })
            else:
                # 生成未完成或失败
                return format_success({
                    "success": False,
                    "message": response.get("msg") or "语音生成未完成，请稍后重试",
                    "task_id": id_value,
                    "note": "生成时间约15-30秒，如果长时间未完成，可能是生成失败或内容审核未通过"
                })

        except Exception as e:
            return format_error(f"查询语音生成结果失败: {str(e)}")

    def upload_voice_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """上传配音文件

        Args:
            args: 包含 file, filename 的字典

        Returns:
            上传结果
        """
        file_content = args.get("file")
        filename = args.get("filename")

        if not file_content:
            return format_error("文件内容是必需的")
        if not filename:
            return format_error("文件名是必需的")

        # 检查文件格式
        if not filename.lower().endswith(".mp3"):
            return format_error("配音文件必须是MP3格式")

        try:
            # 处理文件数据
            if file_content.startswith("data:"):
                # Base64编码的文件
                base64_data = file_content.split(",")[1]
                file_bytes = base64.b64decode(base64_data)
            else:
                # 假设是文件路径
                import os
                if os.path.exists(file_content):
                    with open(file_content, "rb") as f:
                        file_bytes = f.read()
                else:
                    # 尝试作为base64字符串解码
                    try:
                        file_bytes = base64.b64decode(file_content)
                    except:
                        return format_error("无效的文件路径或Base64数据")

            files = {
                "file": (filename, file_bytes, "audio/mpeg")
            }

            response = self.api.multipart_upload(
                "/api/mcp/uploadVoiceFile",
                files=files
            )

            if response.get("code") != 1:
                return format_error(response.get("msg") or "上传失败")

            return format_success({
                "message": "配音文件上传成功",
                "voice_url": response.get("info"),
                "filename": filename
            })

        except Exception as e:
            return format_error(f"上传配音文件失败: {str(e)}")

    def add_voice_narration(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """添加语音讲解到作品

        Args:
            args: 包含 work_id, voice_url, loop, voice 的字典

        Returns:
            添加结果
        """
        work_id = args.get("work_id")
        voice_url = args.get("voice_url")
        loop = args.get("loop", 1)
        voice = args.get("voice", 100)

        if not work_id:
            return format_error("作品ID是必需的")
        if not voice_url:
            return format_error("语音URL是必需的")

        try:
            response = self.api.post("/api/mcp/saveWorkBgm", data={
                "workid": work_id,
                "bgm": voice_url,
                "bgm_voice": voice,
                "bgm_loop": loop
            })

            if response.get("code") != 1:
                return format_error(
                    response.get("msg") or "保存语音讲解失败"
                )

            return format_success({
                "work_id": work_id,
                "voice_url": voice_url,
                "loop": loop,
                "voice": voice,
                "note": "语音已保存到场景配置中"
            })

        except Exception as e:
            return format_error(f"添加语音讲解失败: {str(e)}")


# 导出便捷函数
def get_voice_anchors(**kwargs) -> Dict[str, Any]:
    """获取语音主播列表"""
    return VoiceTools().get_voice_anchors(**kwargs)


def generate_voice_narration(**kwargs) -> Dict[str, Any]:
    """生成语音讲解"""
    return VoiceTools().generate_voice_narration(**kwargs)


def query_voice_result(**kwargs) -> Dict[str, Any]:
    """查询语音生成结果"""
    return VoiceTools().query_voice_result(**kwargs)


def upload_voice_file(**kwargs) -> Dict[str, Any]:
    """上传配音文件"""
    return VoiceTools().upload_voice_file(**kwargs)


def add_voice_narration(**kwargs) -> Dict[str, Any]:
    """添加语音讲解到作品"""
    return VoiceTools().add_voice_narration(**kwargs)

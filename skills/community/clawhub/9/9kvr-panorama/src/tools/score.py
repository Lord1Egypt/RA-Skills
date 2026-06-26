"""Score 工具类

提供作品评分和优化建议功能
"""

import json
from typing import Any, Dict, List, Optional

from ..api import get_api
from ..config import get_config


# 格式化提醒文本
FORMAT_REMINDER = """

---
**格式要求：**
你必须将上述 JSON 数据格式化为易读的 Markdown 格式，包括：
1. 使用 Markdown 表格或列表展示数据
2. 将所有 URL 字段转换为可点击的 Markdown 链接格式：[链接文本](链接地址)
3. 不要直接返回原始 JSON 数据给用户
4. 突出重要信息（如作品名称、播放链接等）

**示例：**
- 作品链接字段 `play_url` 应转换为：[查看作品](链接地址)
- 多个链接使用列表格式展示
- 使用表格展示作品列表信息
"""


class ScoreTools:
    """Score 工具类"""

    def __init__(self):
        """初始化 Score 工具"""
        self.config = get_config()
        self.api = get_api()

    def getTools(self) -> List[Dict[str, Any]]:
        """获取所有工具定义

        Returns:
            工具定义列表
        """
        return [
            {
                "name": "get_work_score",
                "description": "**获取全景作品的评分和优化建议。**此工具会分析作品的各项指标（背景音乐、视角信息、热点、详细介绍、AI语音讲解、LBS位置信息等），给出综合评分（满分100分）和详细的优化建议。评分完成后，会提供作品编辑链接，引导用户前往编辑页面完善作品。评分越高，作品在系统中获得的流量分发越多。**评分标准：**1) 背景音乐（20分）- 作品是否设置了背景音乐；2) 视角信息（20分）- 作品是否设置了视角信息；3) 热点（20分）- 作品是否添加了热点；4) 详细介绍（20分）- 作品描述是否大于12个汉字；5) AI语音讲解（10分）- 是否添加了场景AI语音讲解；6) LBS位置信息（10分）- 是否设置了位置信息。**评价等级：**100分=最佳，80-99分=优质，60-79分=良好，40-59分=一般，20-39分=较差。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（支持加密ID）",
                        },
                    },
                    "required": ["work_id"],
                },
            },
        ]

    def hasTool(self, name: str) -> bool:
        """检查是否存在指定的工具

        Args:
            name: 工具名称

        Returns:
            是否存在
        """
        return any(tool["name"] == name for tool in self.getTools())

    async def handleTool(self, name: str, args: Any) -> Dict[str, Any]:
        """处理工具调用

        Args:
            name: 工具名称
            args: 工具参数

        Returns:
            工具返回结果

        Raises:
            ValueError: 未知工具名称
        """
        if name == "get_work_score":
            return await self.getWorkScore(args)
        else:
            raise ValueError(f"Unknown tool: {name}")

    async def getWorkScore(self, args: Any) -> Dict[str, Any]:
        """获取作品评分和优化建议

        调用 Mcp::getWorkScore() -> Tour::worksScore()
        路由: /api/mcp/getWorkScore

        Args:
            args: 包含 work_id 的参数

        Returns:
            评分结果

        Raises:
            ValueError: 缺少作品ID
            Exception: 获取评分失败
        """
        work_id = args.get("work_id") if isinstance(args, dict) else args

        if not work_id:
            raise ValueError("作品ID是必需的")

        try:
            # 调用评分接口（传递 id 参数，支持加密ID）
            response = self._post("/api/mcp/getWorkScore", {"id": work_id})

            if response.get("code") != 1:
                raise Exception(f"获取评分失败: {response.get('msg', '未知错误')}")

            score_data = response.get("info", [])
            if isinstance(score_data, list):
                score_data = score_data[0] if score_data else {}
            elif not score_data:
                score_data = {}

            # 解析评分数据
            score = score_data.get("number", 0)
            evaluate = score_data.get("evaluate", "未评价")
            style_color = score_data.get("styleColor", "")
            data = score_data.get("data", {})

            # 生成优化建议
            suggestions = self._generate_suggestions(data, score, work_id)

            # 构建编辑链接（使用原始 work_id，支持加密ID）
            edit_url = f"https://9kvr.cn/tour/editor/index?id={work_id}"

            # 构建返回数据
            result = {
                "code": 1,
                "msg": "获取评分成功",
                "info": {
                    "work_id": score_data.get("id", work_id),
                    "score": {
                        "total": score,
                        "max": 100,
                        "evaluate": evaluate,
                        "level": self._get_score_level(score),
                        "color": style_color,
                    },
                    "items": self._format_score_items(data),
                    "suggestions": suggestions,
                    "edit_url": edit_url,
                    "detail": score_data,
                },
            }

            return self._format_tool_response(result)
        except Exception as e:
            raise Exception(f"获取作品评分失败: {str(e)}")

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送 POST 请求

        Args:
            endpoint: API 端点
            data: 请求数据

        Returns:
            响应数据
        """
        return self.api.post(endpoint, data=data)

    def _format_score_items(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """格式化评分项

        Args:
            data: 评分数据

        Returns:
            格式化后的评分项列表
        """
        items = []
        item_map = {
            "music": "背景音乐",
            "eyes": "视角信息",
            "hot": "热点",
            "profile": "详细介绍",
            "voice": "AI语音讲解",
            "lbs": "LBS位置信息",
        }

        for key, value in data.items():
            if isinstance(value, list) and len(value) >= 3:
                items.append({
                    "key": key,
                    "name": item_map.get(key, key),
                    "description": value[0] if value[0] else "",
                    "completed": value[1] == 1,
                    "score": value[2] if len(value) > 2 else 0,
                    "max_score": value[2] if len(value) > 2 else 0,
                    "tutorial_id": value[3] if len(value) > 3 else None,
                    "path": value[4] if len(value) > 4 else "",
                })

        return items

    def _generate_suggestions(self, data: Dict[str, Any], total_score: int, work_id: str) -> List[Dict[str, Any]]:
        """生成优化建议

        Args:
            data: 评分数据
            total_score: 总分
            work_id: 作品ID

        Returns:
            优化建议列表
        """
        suggestions = []
        item_map = {
            "music": {
                "name": "背景音乐",
                "action": "为作品添加背景音乐，可以提升用户体验和沉浸感",
                "priority": 1,
            },
            "eyes": {
                "name": "视角信息",
                "action": "设置视角信息，帮助用户更好地浏览作品",
                "priority": 2,
            },
            "hot": {
                "name": "热点",
                "action": "添加热点，可以增加场景之间的跳转和交互性",
                "priority": 3,
            },
            "profile": {
                "name": "详细介绍",
                "action": "完善作品描述，至少12个汉字，让用户更好地了解作品",
                "priority": 4,
            },
            "voice": {
                "name": "AI语音讲解",
                "action": "添加AI语音讲解，为作品增加语音导览功能",
                "priority": 5,
            },
            "lbs": {
                "name": "LBS位置信息",
                "action": "设置位置信息，让作品在地图上显示",
                "priority": 6,
            },
        }

        # 检查未完成的项目
        for key, value in data.items():
            if isinstance(value, list) and len(value) >= 2 and value[1] == 0:
                item_info = item_map.get(key)
                if item_info:
                    edit_url = f"https://9kvr.cn/tour/editor/index?id={work_id}"
                    suggestions.append({
                        "item": key,
                        "name": item_info["name"],
                        "action": item_info["action"],
                        "score": value[2] if len(value) > 2 else 0,
                        "priority": item_info["priority"],
                        "tutorial_id": value[3] if len(value) > 3 else None,
                        "path": value[4] if len(value) > 4 else "",
                        "edit_url": edit_url,
                        "tip": f"请前往编辑页面完善：{edit_url}",
                    })

        # 按优先级排序
        suggestions.sort(key=lambda x: x["priority"])

        # 构建编辑链接
        edit_url = f"https://9kvr.cn/tour/editor/index?id={work_id}"

        # 添加总体建议
        if total_score < 100:
            missing_count = len(suggestions)
            total_missing = sum(item["score"] for item in suggestions)

            suggestions.insert(0, {
                "item": "overall",
                "name": "总体建议",
                "action": f"当前评分 {total_score} 分，还有 {missing_count} 项未完成，完成这些项目可以获得 {total_missing} 分，将评分提升到 {min(100, total_score + total_missing)} 分。评分越高，作品在系统中获得的流量分发越多。",
                "score": total_missing,
                "priority": 0,
                "edit_url": edit_url,
                "tip": f"请前往编辑页面完善作品：{edit_url}",
            })
        else:
            suggestions.insert(0, {
                "item": "overall",
                "name": "总体评价",
                "action": "恭喜！您的作品已达到满分（100分），所有评分项都已完成。作品将获得系统最大流量分发。",
                "score": 0,
                "priority": 0,
                "edit_url": edit_url,
            })

        return suggestions

    def _get_score_level(self, score: int) -> str:
        """获取评分等级

        Args:
            score: 评分

        Returns:
            评分等级字符串
        """
        if score == 100:
            return "最佳"
        elif score >= 80:
            return "优质"
        elif score >= 60:
            return "良好"
        elif score >= 40:
            return "一般"
        elif score > 20:
            return "较差"
        else:
            return "待完善"

    def _format_tool_response(self, data: Any) -> Dict[str, Any]:
        """格式化工具返回结果

        在 JSON 数据后添加格式提示，确保 AI 知道需要格式化输出

        Args:
            data: 要返回的数据

        Returns:
            格式化后的响应
        """
        json_text = json.dumps(data, indent=2, ensure_ascii=False)

        return {
            "content": [
                {
                    "type": "text",
                    "text": json_text + FORMAT_REMINDER,
                },
            ],
        }

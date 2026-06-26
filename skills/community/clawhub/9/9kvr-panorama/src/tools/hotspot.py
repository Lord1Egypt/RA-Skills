"""热点工具模块

提供热点管理功能，包括场景跳转热点、文本热点等：
- manage_hotspot: 统一热点管理（query/add/update/delete）
- add_scene_jump_hotspot: 添加场景跳转热点
- add_text_hotspot: 添加文本热点
"""

import json
import random
import string
from typing import Any, Dict, Optional, List

from ..api import get_api
from ..config import get_config
from ..utils.response import format_success, format_error, format_list


class HotspotTools:
    """热点工具类"""

    # 支持的热点类型
    SUPPORTED_HOT_TYPES = [1, 2]

    # 热点类型映射
    HOT_TYPE_NAMES = {
        1: "全景跳转",
        2: "文本热点",
        3: "单张图片热点",
        4: "多张图片热点",
        5: "视频热点",
        6: "拨号热点",
        7: "商品热点",
        8: "3D视频热点",
        9: "3D音频热点",
        10: "聚焦热点",
        11: "红包热点",
        12: "全景互跳",
        13: "外链热点",
        14: "联系我",
        15: "绿幕热点",
        16: "开发者热点",
        17: "文章热点",
        18: "互动热点",
        19: "小商店热点",
        20: "表单热点",
        21: "3D模型热点",
        22: "3D图片热点",
        23: "遮罩热点",
        24: "插件热点",
        25: "位置热点"
    }

    # 默认热点图标
    DEFAULT_ICON = "https://imgs.he29.com/hot/1/af21ea9c416dc8154114cc2f2eb3658e.png"

    def __init__(self):
        """初始化热点工具"""
        self.config = get_config()
        self.api = get_api()

    def get_hot_type_name(self, hot_type: int) -> str:
        """获取热点类型名称

        Args:
            hot_type: 热点类型ID

        Returns:
            热点类型名称
        """
        return self.HOT_TYPE_NAMES.get(hot_type, "未知热点")

    def generate_random_id(self, length: int = 8) -> str:
        """生成随机ID

        Args:
            length: ID长度

        Returns:
            随机ID字符串
        """
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def get_tools(self) -> List[Dict[str, Any]]:
        """获取工具列表

        Returns:
            工具定义列表
        """
        return [
            {
                "name": "manage_hotspot",
                "description": "**统一的热点管理工具，处理所有热点相关操作（增删改查）。**这是处理热点相关需求的唯一工具，包括：统计热点数量、查询热点列表、添加热点、编辑热点、删除热点等所有操作。**操作类型：**1) action='query' - 查询/统计热点（返回作品的所有热点列表和统计信息，包括热点数量、类型分布等）；2) action='add' - 添加新热点（场景跳转热点或文本热点）；3) action='update' - 编辑现有热点（通过hotspot_id指定要编辑的热点，只更新提供的字段）；4) action='delete' - 删除热点（通过hotspot_id指定要删除的热点）。**热点类型：**hot_type=1表示场景跳转热点（从场景A跳转到场景B），hot_type=2表示文本热点（显示文本信息）。**重要说明：**查询热点时只需要提供work_id即可，会返回该作品的所有热点信息。添加场景跳转热点时，如果用户没有明确提供热点名称，可以自动使用目标场景的名称作为热点名称。编辑热点时，只需要提供要修改的字段，未提供的字段保持不变。删除热点时，只需要提供work_id和hotspot_id。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["query", "add", "update", "delete"],
                            "description": "操作类型：query=查询/统计热点，add=添加热点，update=编辑热点，delete=删除热点"
                        },
                        "work_id": {
                            "type": "number",
                            "description": "作品ID（数字），所有操作都需要"
                        },
                        "hotspot_id": {
                            "type": "string",
                            "description": "热点ID（8位字符串），编辑和删除操作必需，查询和添加操作不需要"
                        },
                        "hot_type": {
                            "type": "number",
                            "enum": [1, 2],
                            "description": "热点类型：1=场景跳转热点，2=文本热点。添加操作必需，编辑和删除操作不需要"
                        },
                        "from_scene_id": {
                            "type": "string",
                            "description": "源场景ID（imgs_workid），场景跳转热点添加时必需，从哪个场景添加热点"
                        },
                        "scene_id": {
                            "type": "string",
                            "description": "场景ID（imgs_workid），文本热点添加时必需，在哪个场景添加热点。编辑时可用于修改热点所属场景"
                        },
                        "to_scene_id": {
                            "type": "string",
                            "description": "目标场景ID（imgs_workid），场景跳转热点添加时必需，跳转到哪个场景。编辑时可用于修改跳转目标"
                        },
                        "ath": {
                            "type": "number",
                            "description": "热点水平角度（-180到180度），热点在场景中的水平位置，可选，默认为0"
                        },
                        "atv": {
                            "type": "number",
                            "description": "热点垂直角度（-90到90度），热点在场景中的垂直位置，可选，默认为0"
                        },
                        "name": {
                            "type": "string",
                            "description": "热点名称。添加文本热点时必需；添加场景跳转热点时可选（未提供则使用目标场景名称）；编辑时可选"
                        },
                        "icon": {
                            "type": "string",
                            "description": "热点图标URL（可选），默认使用 https://imgs.he29.com/hot/1/af21ea9c416dc8154114cc2f2eb3658e.png"
                        },
                        "transition": {
                            "type": "string",
                            "description": "转场效果（可选），默认：BLEND(0.5, easeInCubic)。可选值：BLEND、FADE、CROSS等"
                        },
                        "transition3D": {
                            "type": "boolean",
                            "description": "是否开启3D转场（可选），默认false。开启后会有类似行走漫游的效果"
                        },
                        "visualAngle": {
                            "type": "boolean",
                            "description": "是否开启视角动画（可选），默认false。开启后可配置场景跳转后视角的落地点"
                        },
                        "visualAngleTime": {
                            "type": "number",
                            "description": "视角动画时长（可选），默认3秒，范围0-10秒"
                        },
                        "visualAngleWait": {
                            "type": "number",
                            "description": "跳转后等待时间（可选），默认0秒，范围0-10秒。热点跳转后等待多少秒后开始执行视角运动"
                        },
                        "visualAngleView": {
                            "type": "object",
                            "description": "落地视角（可选），默认{ath: 0, atv: 0, fov: 60}。包含ath（水平角度）、atv（垂直角度）、fov（视野角度）"
                        },
                        "longText": {
                            "type": "string",
                            "description": "长文本内容（可选），点击热点后弹窗显示的文本内容，最多100000字符。**重要：**除非用户明确要求添加文本内容，否则不要设置此字段。编辑时设置为空字符串可清空文本内容"
                        },
                        "extraStyle": {
                            "type": "object",
                            "description": "附加样式（可选），标准JSON格式的样式对象，使用驼峰命名。支持animate.css动画类名（如：'animationName':'bounce','animationDuration':'2s'等）。示例：{'fontWeight':'bold','textShadow':'1px 1px 2px rgba(0,0,0,0.5)','marginTop':'10px','animationName':'bounce','animationDuration':'2s'}"
                        },
                    },
                    "required": ["action", "work_id"],
                },
            },
            {
                "name": "add_scene_jump_hotspot",
                "description": "在指定场景中添加场景跳转热点，实现从场景A跳转到场景B的功能。**重要说明：**此工具用于在全景作品的某个场景中添加热点，点击该热点可以跳转到同一作品中的另一个场景。需要提供源场景ID（从哪个场景添加热点）、目标场景ID（跳转到哪个场景）、热点位置（水平角度ath和垂直角度atv）等参数。**注意：**源场景和目标场景必须是同一个作品中的场景，不能跨作品跳转。**关键要求：**如果用户没有明确提供热点名称，可以自动使用目标场景的名称作为热点名称。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "work_id": {
                            "type": "number",
                            "description": "作品ID（数字）"
                        },
                        "from_scene_id": {
                            "type": "string",
                            "description": "源场景ID（imgs_workid），从哪个场景添加热点"
                        },
                        "to_scene_id": {
                            "type": "string",
                            "description": "目标场景ID（imgs_workid），跳转到哪个场景"
                        },
                        "ath": {
                            "type": "number",
                            "description": "热点水平角度（-180到180度），热点在场景中的水平位置，可选，默认为0"
                        },
                        "atv": {
                            "type": "number",
                            "description": "热点垂直角度（-90到90度），热点在场景中的垂直位置，可选，默认为0"
                        },
                        "name": {
                            "type": "string",
                            "description": "热点名称（可选），如果用户提供了名称则使用用户提供的名称，否则自动使用目标场景的名称"
                        },
                        "icon": {
                            "type": "string",
                            "description": "热点图标URL（可选），默认使用 https://imgs.he29.com/hot/1/af21ea9c416dc8154114cc2f2eb3658e.png"
                        },
                        "transition": {
                            "type": "string",
                            "description": "转场效果（可选），默认：BLEND(0.5, easeInCubic)。可选值：BLEND、FADE、CROSS等"
                        },
                        "transition3D": {
                            "type": "boolean",
                            "description": "是否开启3D转场（可选），默认false。开启后会有类似行走漫游的效果"
                        },
                        "visualAngle": {
                            "type": "boolean",
                            "description": "是否开启视角动画（可选），默认false。开启后可配置场景跳转后视角的落地点"
                        },
                        "visualAngleTime": {
                            "type": "number",
                            "description": "视角动画时长（可选），默认3秒，范围0-10秒"
                        },
                        "visualAngleWait": {
                            "type": "number",
                            "description": "跳转后等待时间（可选），默认0秒，范围0-10秒。热点跳转后等待多少秒后开始执行视角运动"
                        },
                        "visualAngleView": {
                            "type": "object",
                            "description": "落地视角（可选），默认{ath: 0, atv: 0, fov: 60}。包含ath（水平角度）、atv（垂直角度）、fov（视野角度）"
                        },
                        "extraStyle": {
                            "type": "object",
                            "description": "附加样式（可选），标准JSON格式的样式对象，使用驼峰命名，例如：{'fontWeight':'bold','textShadow':'1px 1px 2px rgba(0,0,0,0.5)','marginTop':'10px'}"
                        },
                    },
                    "required": ["work_id", "from_scene_id", "to_scene_id"],
                },
            },
            {
                "name": "add_text_hotspot",
                "description": "在指定场景中添加文本热点，用于显示文本信息。**重要说明：**此工具用于在全景作品的某个场景中添加文本热点，点击该热点可以弹窗显示长文本内容。需要提供场景ID、热点位置（水平角度ath和垂直角度atv）、热点名称等参数。文本热点主要用于展示说明文字、介绍信息等。**关键要求：**1) 热点名称(name)字段是必需的，必须使用用户明确提供的名称，直接写入到名称字段，不要自动生成或提取名称；2) 长文本内容(longText)字段是可选的，除非用户明确要求添加文本内容，否则不要设置此字段，默认情况下此字段不写入。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "work_id": {
                            "type": "number",
                            "description": "作品ID（数字）"
                        },
                        "scene_id": {
                            "type": "string",
                            "description": "场景ID（imgs_workid），在哪个场景添加热点"
                        },
                        "ath": {
                            "type": "number",
                            "description": "热点水平角度（-180到180度），热点在场景中的水平位置，可选，默认为0"
                        },
                        "atv": {
                            "type": "number",
                            "description": "热点垂直角度（-90到90度），热点在场景中的垂直位置，可选，默认为0"
                        },
                        "name": {
                            "type": "string",
                            "description": "热点名称（必需），用户提供的热点名称，直接写入到名称字段。不要自动生成或提取名称，必须使用用户明确提供的内容。"
                        },
                        "longText": {
                            "type": "string",
                            "description": "长文本内容（可选），点击热点后弹窗显示的文本内容，最多100000字符。**重要：**除非用户明确要求添加文本内容，否则不要设置此字段。默认情况下此字段不写入。"
                        },
                        "icon": {
                            "type": "string",
                            "description": "热点图标URL（可选），默认使用 https://imgs.he29.com/hot/1/af21ea9c416dc8154114cc2f2eb3658e.png"
                        },
                        "extraStyle": {
                            "type": "object",
                            "description": "附加样式（可选），标准JSON格式的样式对象，使用驼峰命名，例如：{'fontWeight':'bold','textShadow':'1px 1px 2px rgba(0,0,0,0.5)','marginTop':'10px'}"
                        },
                    },
                    "required": ["work_id", "scene_id", "name"],
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
        if name == "manage_hotspot":
            return self.manage_hotspot(args)
        elif name == "add_scene_jump_hotspot":
            return self.add_scene_jump_hotspot(args)
        elif name == "add_text_hotspot":
            return self.add_text_hotspot(args)
        else:
            return format_error(f"Unknown tool: {name}")

    def _coerce_args(
        self,
        args: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """统一参数入口，兼容 dict 传参与关键字传参。"""
        merged: Dict[str, Any] = {}
        if isinstance(args, dict):
            merged.update(args)
        merged.update(kwargs)
        return merged

    def manage_hotspot(
        self,
        args: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """统一的热点管理方法

        Args:
            args: 包含 action, work_id 等参数的字典

        Returns:
            处理结果
        """
        args = self._coerce_args(args, **kwargs)
        action = args.get("action")
        work_id = args.get("work_id")

        if not work_id:
            return format_error("作品ID是必需的")

        if not action or action not in ["query", "add", "update", "delete"]:
            return format_error("操作类型(action)必须是 query、add、update 或 delete")

        # 查询操作
        if action == "query":
            return self._query_hotspot(work_id)

        # 删除操作
        if action == "delete":
            hotspot_id = args.get("hotspot_id")
            return self._delete_hotspot(work_id, hotspot_id)

        # 编辑操作
        if action == "update":
            return self._update_hotspot(args)

        # 添加操作
        return self._add_hotspot(args)

    def _query_hotspot(self, work_id: int) -> Dict[str, Any]:
        """查询/统计热点

        Args:
            work_id: 作品ID

        Returns:
            查询结果
        """
        try:
            # 获取当前作品的热点配置
            response = self.api.post("/api/tour/getAllConfig", data={"id": work_id})

            hot_list = []
            if response.get("code") == 1 and response.get("info"):
                hot_list = response.get("info", {}).get("config_hot", [])

            # 统计信息
            total_count = len(hot_list)
            type_count = {}

            # 处理热点列表
            hotspots = []
            for index, hot in enumerate(hot_list):
                hot_id = hot.get("id") or "无ID"
                hotname = hot.get("hotname") or "无名称"
                hot_name = hot.get("name") or "无显示名称"
                hot_type = hot.get("hotType") or hot.get("hotTpye") or 0
                scene_id = hot.get("sceneId") or hot.get("ids") or "未知场景"
                type_name = self.get_hot_type_name(hot_type)
                is_supported = hot_type in self.SUPPORTED_HOT_TYPES

                # 统计类型
                if hot_type not in type_count:
                    type_count[hot_type] = 0
                type_count[hot_type] += 1

                hotspot_info = {
                    "index": index + 1,
                    "id": hot_id,
                    "hotname": hotname,
                    "name": hot_name,
                    "type": type_name,
                    "type_id": hot_type,
                    "scene_id": scene_id,
                    "supported": is_supported,
                    "position": {
                        "ath": hot.get("ath") or 0,
                        "atv": hot.get("atv") or 0,
                    },
                }

                # 场景跳转热点特有信息
                if hot_type == 1:
                    hotspot_info["from_scene_id"] = hot.get("sceneId") or hot.get("ids")
                    hotspot_info["to_scene_id"] = hot.get("toSceneId") or hot.get("toIds")

                # 文本热点特有信息
                if hot_type == 2:
                    hotspot_info["has_text"] = bool(hot.get("longText") and hot.get("longText").strip())
                    hotspot_info["text_length"] = len(hot.get("longText") or "")

                hotspots.append(hotspot_info)

            # 计算支持和不支持的数量
            supported = len([h for h in hotspots if h["supported"]])
            unsupported = len([h for h in hotspots if not h["supported"]])

            # 类型分布统计
            type_distribution = []
            for type_id, count in type_count.items():
                type_distribution.append({
                    "type_id": type_id,
                    "type_name": self.get_hot_type_name(type_id),
                    "count": count,
                })

            return format_success({
                "work_id": work_id,
                "statistics": {
                    "total_count": total_count,
                    "supported_count": supported,
                    "unsupported_count": unsupported,
                    "type_distribution": type_distribution,
                },
                "hotspots": hotspots,
            })

        except Exception as e:
            return format_error(f"获取热点配置失败: {str(e)}")

    def _delete_hotspot(self, work_id: int, hotspot_id: str) -> Dict[str, Any]:
        """删除热点

        Args:
            work_id: 作品ID
            hotspot_id: 热点ID

        Returns:
            删除结果
        """
        if not hotspot_id:
            return format_error("删除热点时，热点ID(hotspot_id)是必需的")

        try:
            # 获取当前作品的热点配置
            response = self.api.post("/api/tour/getAllConfig", data={"id": work_id})

            hot_list = []
            if response.get("code") == 1 and response.get("info"):
                hot_list = response.get("info", {}).get("config_hot", [])

            # 查找要删除的热点
            hotspot_index = -1
            for i, hot in enumerate(hot_list):
                if hot.get("id") == hotspot_id or hot.get("hotname") == hotspot_id:
                    hotspot_index = i
                    break

            if hotspot_index == -1:
                # 提供可用热点列表
                available_hotspots = []
                for i, hot in enumerate(hot_list):
                    hot_id = hot.get("id") or "无ID"
                    hotname = hot.get("hotname") or "无名称"
                    hot_name = hot.get("name") or "无显示名称"
                    hot_type = hot.get("hotType") or hot.get("hotTpye") or 0
                    scene_id = hot.get("sceneId") or hot.get("ids") or "未知场景"
                    type_name = self.get_hot_type_name(hot_type)
                    is_supported = hot_type in self.SUPPORTED_HOT_TYPES

                    available_hotspots.append({
                        "index": i + 1,
                        "id": hot_id,
                        "hotname": hotname,
                        "name": hot_name,
                        "type": type_name,
                        "type_id": hot_type,
                        "scene_id": scene_id,
                        "supported": is_supported,
                    })

                error_msg = f"热点ID '{hotspot_id}' 不存在。\n\n"
                if len(available_hotspots) == 0:
                    error_msg += "该作品目前没有任何热点。"
                else:
                    error_msg += f"该作品共有 {len(available_hotspots)} 个热点，可用热点列表：\n\n"
                    for hot in available_hotspots:
                        support_status = "支持AI修改" if hot["supported"] else "不支持AI修改"
                        error_msg += f"{hot['index']}. 热点ID: {hot['id']} | 热点名称(hotname): {hot['hotname']} | 显示名称: {hot['name']} | 类型: {hot['type']}({hot['type_id']}) | 场景ID: {hot['scene_id']} | {support_status}\n"
                    error_msg += "\n请使用上述列表中的热点ID或hotname来删除热点。"

                return format_error(error_msg)

            deleted_hotspot = hot_list[hotspot_index]

            # 从列表中删除
            hot_list.pop(hotspot_index)

            # 保存配置
            save_response = self.api.post("/api/tour/saveAllConfig", data={
                "id": work_id,
                "config_hot": json.dumps(hot_list),
                "isPreview": 0
            })

            if save_response.get("code") != 1:
                return format_error(save_response.get("msg") or "保存热点配置失败")

            return format_success({
                "message": "热点删除成功",
                "hotspot_id": hotspot_id,
                "deleted_hotspot": deleted_hotspot,
            })

        except Exception as e:
            return format_error(f"保存热点配置失败: {str(e)}")

    def _update_hotspot(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """编辑热点

        Args:
            args: 包含 work_id, hotspot_id 及更新字段的字典

        Returns:
            更新结果
        """
        work_id = args.get("work_id")
        hotspot_id = args.get("hotspot_id")
        hot_type = args.get("hot_type")

        if not hotspot_id:
            return format_error("编辑热点时，热点ID(hotspot_id)是必需的")

        # 不允许修改热点类型
        if hot_type is not None:
            return format_error("不支持修改热点类型，热点类型在创建时确定后无法更改")

        try:
            # 获取当前作品的热点配置
            response = self.api.post("/api/tour/getAllConfig", data={"id": work_id})

            hot_list = []
            if response.get("code") == 1 and response.get("info"):
                hot_list = response.get("info", {}).get("config_hot", [])

            # 查找要编辑的热点
            hotspot_index = -1
            for i, hot in enumerate(hot_list):
                if hot.get("id") == hotspot_id or hot.get("hotname") == hotspot_id:
                    hotspot_index = i
                    break

            if hotspot_index == -1:
                return format_error(f"热点ID {hotspot_id} 不存在")

            existing_hotspot = hot_list[hotspot_index]
            existing_hot_type = existing_hotspot.get("hotType") or existing_hotspot.get("hotTpye")

            # 检查热点类型是否支持AI修改
            if existing_hot_type not in self.SUPPORTED_HOT_TYPES:
                type_name = self.get_hot_type_name(existing_hot_type)
                return format_error(
                    f"此热点暂不支持由 AI 修改！\n\n"
                    f"热点类型：{type_name} (类型ID: {existing_hot_type})\n\n"
                    f"目前仅支持以下类型的AI修改：\n"
                    f"- 全景跳转 (类型1)\n"
                    f"- 文本热点 (类型2)"
                )

            # 获取场景列表以验证场景ID
            scenes = []
            if args.get("from_scene_id") or args.get("scene_id") or args.get("to_scene_id"):
                scenes_response = self.api.post("/api/tour/getScene", data={"id": work_id})
                if scenes_response.get("code") == 1 and isinstance(scenes_response.get("info"), list):
                    scenes = scenes_response.get("info", [])

            # 更新热点配置（只更新提供的字段）
            if "name" in args and args["name"] is not None:
                existing_hotspot["name"] = args["name"]

            if "icon" in args and args["icon"] is not None:
                existing_hotspot["icon"] = args["icon"]

            if "ath" in args and args["ath"] is not None:
                ath = args["ath"]
                if ath < -180 or ath > 180:
                    return format_error("热点水平角度(ath)必须在-180到180度之间")
                existing_hotspot["ath"] = str(ath)

            if "atv" in args and args["atv"] is not None:
                atv = args["atv"]
                if atv < -90 or atv > 90:
                    return format_error("热点垂直角度(atv)必须在-90到90度之间")
                existing_hotspot["atv"] = str(atv)

            if "extraStyle" in args:
                existing_hotspot["extraStyle"] = args["extraStyle"] or {}

            # 场景跳转热点特有字段
            if existing_hot_type == 1:
                if "from_scene_id" in args and args["from_scene_id"] is not None:
                    from_scene_id = args["from_scene_id"]
                    scene = next((s for s in scenes if s.get("imgs_workid") == from_scene_id), None)
                    if not scene:
                        return format_error(f"源场景ID {from_scene_id} 不存在于该作品中")
                    existing_hotspot["sceneId"] = from_scene_id

                if "to_scene_id" in args and args["to_scene_id"] is not None:
                    to_scene_id = args["to_scene_id"]
                    to_scene = next((s for s in scenes if s.get("imgs_workid") == to_scene_id), None)
                    if not to_scene:
                        return format_error(f"目标场景ID {to_scene_id} 不存在于该作品中")
                    if existing_hotspot.get("sceneId") == to_scene_id:
                        return format_error("不能从场景跳转到自己，源场景和目标场景不能相同")
                    existing_hotspot["link"] = to_scene_id

                if "transition" in args and args["transition"] is not None:
                    existing_hotspot["transition"] = args["transition"]

                if "transition3D" in args and args["transition3D"] is not None:
                    existing_hotspot["transition3D"] = args["transition3D"]

                if "visualAngle" in args and args["visualAngle"] is not None:
                    existing_hotspot["visualAngle"] = args["visualAngle"]

                if "visualAngleTime" in args and args["visualAngleTime"] is not None:
                    existing_hotspot["visualAngleTime"] = args["visualAngleTime"]

                if "visualAngleWait" in args and args["visualAngleWait"] is not None:
                    existing_hotspot["visualAngleWait"] = args["visualAngleWait"]

                if "visualAngleView" in args and args["visualAngleView"] is not None:
                    existing_hotspot["visualAngleView"] = args["visualAngleView"]

            # 文本热点特有字段
            if existing_hot_type == 2:
                if "scene_id" in args and args["scene_id"] is not None:
                    scene_id = args["scene_id"]
                    scene = next((s for s in scenes if s.get("imgs_workid") == scene_id), None)
                    if not scene:
                        return format_error(f"场景ID {scene_id} 不存在于该作品中")
                    existing_hotspot["sceneId"] = scene_id

                if "longText" in args:
                    # 如果提供空字符串，删除longText字段
                    if args["longText"] == "":
                        if "longText" in existing_hotspot:
                            del existing_hotspot["longText"]
                    else:
                        existing_hotspot["longText"] = args["longText"]

            # 保存配置
            save_response = self.api.post("/api/tour/saveAllConfig", data={
                "id": work_id,
                "config_hot": json.dumps(hot_list),
                "isPreview": 0
            })

            if save_response.get("code") != 1:
                return format_error(save_response.get("msg") or "保存热点配置失败")

            # 生成编辑器链接
            editor_url = f"https://9kvr.cn/tour/editor/index?id={work_id}&sceneId={existing_hotspot.get('sceneId')}"

            return format_success({
                "message": "热点编辑成功",
                "hotspot_id": hotspot_id,
                "scene": {
                    "id": existing_hotspot.get("sceneId"),
                },
                "config": existing_hotspot,
                "editor_url": editor_url,
            })

        except Exception as e:
            return format_error(f"保存热点配置失败: {str(e)}")

    def _add_hotspot(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """添加热点

        Args:
            args: 包含热点配置参数的字典

        Returns:
            添加结果
        """
        hot_type = args.get("hot_type")
        work_id = args.get("work_id")
        from_scene_id = args.get("from_scene_id")
        scene_id = args.get("scene_id")
        to_scene_id = args.get("to_scene_id")
        ath = args.get("ath", 0)
        atv = args.get("atv", 0)
        name = args.get("name")
        icon = args.get("icon", self.DEFAULT_ICON)
        transition = args.get("transition", "BLEND(0.5, easeInCubic)")
        transition3D = args.get("transition3D", False)
        visualAngle = args.get("visualAngle", False)
        visualAngleTime = args.get("visualAngleTime", 3)
        visualAngleWait = args.get("visualAngleWait", 0)
        visualAngleView = args.get("visualAngleView", {"ath": 0, "atv": 0, "fov": 60})
        longText = args.get("longText", "")
        extraStyle = args.get("extraStyle", {})

        # 参数验证
        if not work_id:
            return format_error("作品ID是必需的")

        # 文本热点必须提供名称
        if hot_type == 2 and (not name or not name.strip()):
            return format_error("文本热点的名称是必需的，必须提供用户明确指定的名称")

        # 根据热点类型确定场景ID
        actual_scene_id = hot_type == 1 and from_scene_id or scene_id
        if not actual_scene_id:
            return format_error("源场景ID是必需的" if hot_type == 1 else "场景ID是必需的")

        # 场景跳转需要目标场景
        if hot_type == 1 and not to_scene_id:
            return format_error("目标场景ID是必需的")

        # 验证角度范围
        if ath < -180 or ath > 180:
            return format_error("热点水平角度(ath)必须在-180到180度之间")
        if atv < -90 or atv > 90:
            return format_error("热点垂直角度(atv)必须在-90到90度之间")

        # 场景跳转不能自己跳自己
        if hot_type == 1 and from_scene_id == to_scene_id:
            return format_error("不能从场景跳转到自己，源场景和目标场景不能相同")

        try:
            # 1. 获取作品的所有场景列表
            scenes_response = self.api.post("/api/tour/getScene", data={"id": work_id})

            scenes = []
            if scenes_response.get("code") == 1 and isinstance(scenes_response.get("info"), list):
                scenes = scenes_response.get("info", [])
            else:
                return format_error("获取场景列表失败")

            # 验证场景是否存在
            scene = next((s for s in scenes if s.get("imgs_workid") == actual_scene_id), None)
            if not scene:
                return format_error(f"场景ID {actual_scene_id} 不存在于该作品中")

            # 场景跳转需要验证目标场景
            to_scene = None
            if hot_type == 1:
                to_scene = next((s for s in scenes if s.get("imgs_workid") == to_scene_id), None)
                if not to_scene:
                    return format_error(f"目标场景ID {to_scene_id} 不存在于该作品中")

            # 2. 获取当前作品的热点配置
            config_response = self.api.post("/api/tour/getAllConfig", data={"id": work_id})

            hot_list = []
            if config_response.get("code") == 1 and config_response.get("info"):
                hot_list = config_response.get("info", {}).get("config_hot", [])

            # 3. 生成热点ID
            hotspot_id = self.generate_random_id(8)

            # 4. 构建完整的热点配置
            hotspot_config = {
                # 基础标识
                "id": hotspot_id,
                "hotType": hot_type,
                "sceneId": actual_scene_id,
                "hotVersion": 1,

                # 平台和显示配置
                "platform": ["all"],
                "showStatus": [1, 2] if hot_type == 1 else [2],

                # 基本信息
                "name": (
                    name or (
                        f"跳转到{to_scene.get('imgs_filename')}" if hot_type == 1 and to_scene and to_scene.get("imgs_filename")
                        else f"跳转到{to_scene_id}" if hot_type == 1
                        else name
                    )
                ) if hot_type == 1 else name,
                "icon": icon,

                # 尺寸配置
                "width": 128,
                "height": 128,
                "size": "60*60",
                "sizeWidth": 0,
                "sizeHeight": 0,

                # 动画配置
                "ram": 1,
                "zoom": False,

                # 区域配置
                "area": {
                    "point": [],
                    "config": {}
                },

                # 样式配置
                "alpha": 5,
                "textColor": "#ffffff",
                "bgColor": "#000000",
                "fontSize": 12,
                "radius": 5,

                # 对齐和位置
                "align": "bottom",
                "edge": "top",
                "rotate": 0,
                "x": 0,
                "y": 0,
                "z": 0,
                "scale": 1,

                # 3D变换
                "rx": 0,
                "ry": 0,
                "rz": 0,
                "tx": 0,
                "ty": 0,
                "tz": 0,

                # 精细化控制
                "openDelica": True,
                "textBorder": False,
                "textBorderColor": "#FFF",
                "textBorderSize": 1,
                "textRadius": 0,
                "textBgColor": "",
                "paddingUp": 3,
                "paddingLeft": 5,
                "marginUp": 0,
                "marginLeft": 0,

                # 文字相关配置
                "cm": 0,
                "txtScale": 1,
                "txtSpacing": 1,
                "txtRotate": 0,
                "txtDistorted": False,
                "alienCenter": "left",
                "txtZoom": False,
                "txtRx": 0,
                "txtRy": 0,
                "txtRz": 0,
                "txtTx": 0,
                "txtTy": 0,
                "txtTz": 0,

                # 其他配置
                "distorted": False,
                "enabled": False,
                "followHide": True,

                # 附加样式
                "extraStyle": extraStyle or {},
            }

            # 根据热点类型添加特定配置
            if hot_type == 1:
                # 场景跳转热点配置
                hotspot_config["ath"] = str(ath)
                hotspot_config["atv"] = str(atv)
                hotspot_config["link"] = to_scene_id
                hotspot_config["transition"] = transition
                hotspot_config["transition3D"] = transition3D
                hotspot_config["visualAngle"] = visualAngle
                hotspot_config["visualAngleTime"] = visualAngleTime
                hotspot_config["visualAngleWait"] = visualAngleWait
                hotspot_config["visualAngleView"] = visualAngleView
            elif hot_type == 2:
                # 文本热点配置
                hotspot_config["ath"] = str(ath)
                hotspot_config["atv"] = str(atv)
                # 只有用户明确提供longText时才写入
                if longText and longText.strip():
                    hotspot_config["longText"] = longText

            # 5. 将新热点添加到列表
            hot_list.append(hotspot_config)

            # 6. 保存配置
            save_response = self.api.post("/api/tour/saveAllConfig", data={
                "id": work_id,
                "config_hot": json.dumps(hot_list),
                "isPreview": 0
            })

            if save_response.get("code") != 1:
                return format_error(save_response.get("msg") or "保存热点配置失败")

            # 生成编辑器链接
            editor_url = f"https://9kvr.cn/tour/editor/index?id={work_id}&sceneId={actual_scene_id}"

            response_info = {
                "hotspot_id": hotspot_id,
                "scene": {
                    "id": actual_scene_id,
                    "name": scene.get("imgs_filename") or actual_scene_id,
                },
                "position": {
                    "ath": ath,
                    "atv": atv,
                },
                "config": hotspot_config,
                "editor_url": editor_url,
            }

            # 场景跳转热点额外返回目标场景信息
            if hot_type == 1 and to_scene:
                response_info["to_scene"] = {
                    "id": to_scene_id,
                    "name": to_scene.get("imgs_filename") or to_scene_id,
                }

            return format_success({
                "message": "场景跳转热点添加成功" if hot_type == 1 else "文本热点添加成功",
                **response_info
            })

        except Exception as e:
            return format_error(f"保存热点配置失败: {str(e)}")

    def add_scene_jump_hotspot(
        self,
        args: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """添加场景跳转热点

        Args:
            args: 包含 from_scene_id, to_scene_id, ath, atv, name 等参数的字典

        Returns:
            添加结果
        """
        merged_args = self._coerce_args(args, **kwargs)
        return self._add_hotspot({**merged_args, "action": "add", "hot_type": 1})

    def add_text_hotspot(
        self,
        args: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """添加文本热点

        Args:
            args: 包含 scene_id, ath, atv, name, longText 等参数的字典

        Returns:
            添加结果
        """
        merged_args = self._coerce_args(args, **kwargs)
        return self._add_hotspot({**merged_args, "action": "add", "hot_type": 2})


# 导出便捷函数
def manage_hotspot(**kwargs) -> Dict[str, Any]:
    """统一热点管理"""
    return HotspotTools().manage_hotspot(**kwargs)


def add_scene_jump_hotspot(**kwargs) -> Dict[str, Any]:
    """添加场景跳转热点"""
    return HotspotTools().add_scene_jump_hotspot(**kwargs)


def add_text_hotspot(**kwargs) -> Dict[str, Any]:
    """添加文本热点"""
    return HotspotTools().add_text_hotspot(**kwargs)

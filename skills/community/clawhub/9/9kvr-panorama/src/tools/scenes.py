"""场景管理工具模块

提供场景相关的操作工具：
- list_scenes: 获取场景列表
- get_scene_info: 获取场景详情
- update_scene_info: 更新场景信息
- delete_scene: 删除场景
"""

from typing import Any, Dict, List, Optional

from ..api import ApiService, get_api
from ..config import get_config
from ..utils.response import Response, ListResponse, format_success, format_error, format_list


class ScenesTools:
    """场景管理工具类"""

    def __init__(self):
        """初始化场景工具"""
        self.config = get_config()
        self.api = get_api()

    def list_scenes(
        self,
        work_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        scene_type: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取场景列表

        Args:
            work_id: 作品ID（可选，用于筛选特定作品的场景）
            page: 页码，默认1
            page_size: 每页数量，默认20，最大100
            scene_type: 场景类型筛选（可选）
            keyword: 关键词搜索（可选）

        Returns:
            场景列表响应

        Example:
            >>> tools = ScenesTools()
            >>> result = tools.list_scenes(work_id="work123", page=1, page_size=10)
            >>> print(result)
        """
        # 参数校验
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        if page_size > 100:
            page_size = 100  # 限制最大100条

        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size
        }

        if work_id:
            params["work_id"] = work_id
        if scene_type:
            params["scene_type"] = scene_type
        if keyword:
            params["keyword"] = keyword

        response = self.api.get("/api/mcp/listScenes", data=params)

        # 格式化输出
        if response.get("code") == 0:
            data = response.get("data", {})
            items = data.get("items", [])
            total = data.get("total", 0)

            # 格式化场景列表
            formatted_items = []
            for item in items:
                formatted_item = self._format_scene(item)
                formatted_items.append(formatted_item)

            return format_list(
                items=formatted_items,
                total=total,
                page=page,
                page_size=page_size
            )

        return response

    def get_scene_info(self, scene_id: str) -> Dict[str, Any]:
        """获取场景详情

        Args:
            scene_id: 场景ID（必填）

        Returns:
            场景详细信息

        Example:
            >>> tools = ScenesTools()
            >>> result = tools.get_scene_info(scene_id="scene123")
            >>> print(result)
        """
        # 参数校验
        if not scene_id or not scene_id.strip():
            return format_error("scene_id is required", code=400)

        params = {"scene_id": scene_id.strip()}

        response = self.api.get("/api/mcp/getSceneInfo", data=params)

        # 格式化输出
        if response.get("code") == 0:
            data = response.get("data")
            if data:
                formatted_data = self._format_scene_detail(data)
                return format_success(data=formatted_data)
            return format_success(data=None)

        return response

    def update_scene_info(
        self,
        scene_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        scene_data: Optional[Dict[str, Any]] = None,
        thumbnail: Optional[str] = None,
        order: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """更新场景信息

        Args:
            scene_id: 场景ID（必填）
            name: 场景名称（可选）
            description: 场景描述（可选）
            scene_data: 场景数据（可选，包含位置、视角等信息）
            thumbnail: 缩略图URL（可选）
            order: 排序顺序（可选）
            **kwargs: 其他可更新的字段

        Returns:
            更新结果

        Example:
            >>> tools = ScenesTools()
            >>> result = tools.update_scene_info(
            ...     scene_id="scene123",
            ...     name="New Scene Name",
            ...     description="Updated description"
            ... )
            >>> print(result)
        """
        # 参数校验
        if not scene_id or not scene_id.strip():
            return format_error("scene_id is required", code=400)

        # 构建更新数据
        update_data: Dict[str, Any] = {"scene_id": scene_id.strip()}

        if name is not None:
            if not isinstance(name, str):
                return format_error("name must be a string", code=400)
            update_data["name"] = name.strip()

        if description is not None:
            if not isinstance(description, str):
                return format_error("description must be a string", code=400)
            update_data["description"] = description

        if scene_data is not None:
            if not isinstance(scene_data, dict):
                return format_error("scene_data must be a dictionary", code=400)
            update_data["scene_data"] = scene_data

        if thumbnail is not None:
            if not isinstance(thumbnail, str):
                return format_error("thumbnail must be a string", code=400)
            update_data["thumbnail"] = thumbnail

        if order is not None:
            if not isinstance(order, int):
                return format_error("order must be an integer", code=400)
            update_data["order"] = order

        # 添加其他额外字段
        for key, value in kwargs.items():
            if key not in update_data and value is not None:
                update_data[key] = value

        response = self.api.post("/api/mcp/updateSceneInfo", data=update_data)

        # 格式化输出
        if response.get("code") == 0:
            return format_success(
                data=response.get("data"),
                message="Scene updated successfully"
            )

        return response

    def delete_scene(self, scene_id: str, force: bool = False) -> Dict[str, Any]:
        """删除场景

        Args:
            scene_id: 场景ID（必填）
            force: 是否强制删除（可选，默认False）
                   强制删除会同时删除关联的资源

        Returns:
            删除结果

        Example:
            >>> tools = ScenesTools()
            >>> result = tools.delete_scene(scene_id="scene123")
            >>> print(result)

            # 强制删除
            >>> result = tools.delete_scene(scene_id="scene123", force=True)
            >>> print(result)
        """
        # 参数校验
        if not scene_id or not scene_id.strip():
            return format_error("scene_id is required", code=400)

        delete_data = {
            "scene_id": scene_id.strip(),
            "force": force
        }

        response = self.api.post("/api/mcp/deleteScene", data=delete_data)

        # 格式化输出
        if response.get("code") == 0:
            return format_success(
                data={"scene_id": scene_id},
                message="Scene deleted successfully"
            )

        return response

    def _format_scene(self, scene: Dict[str, Any]) -> Dict[str, Any]:
        """格式化场景列表项

        Args:
            scene: 原始场景数据

        Returns:
            格式化后的场景数据
        """
        return {
            "id": scene.get("id") or scene.get("scene_id"),
            "name": scene.get("name", "Untitled Scene"),
            "description": scene.get("description", ""),
            "thumbnail": scene.get("thumbnail", ""),
            "scene_type": scene.get("scene_type", "default"),
            "order": scene.get("order", 0),
            "work_id": scene.get("work_id"),
            "created_at": scene.get("created_at", ""),
            "updated_at": scene.get("updated_at", ""),
        }

    def _format_scene_detail(self, scene: Dict[str, Any]) -> Dict[str, Any]:
        """格式化场景详情

        Args:
            scene: 原始场景数据

        Returns:
            格式化后的场景详情
        """
        formatted = self._format_scene(scene)

        # 添加详细字段
        formatted["scene_data"] = scene.get("scene_data", {})
        formatted["panorama_data"] = scene.get("panorama_data", {})
        formatted["hotspots"] = scene.get("hotspots", [])
        formatted["view_angle"] = scene.get("view_angle", {})
        formatted["auto_rotate"] = scene.get("auto_rotate", False)
        formatted["config"] = scene.get("config", {})

        return formatted


# 导出便捷函数
def list_scenes(**kwargs) -> Dict[str, Any]:
    """获取场景列表"""
    return ScenesTools().list_scenes(**kwargs)


def get_scene_info(scene_id: str) -> Dict[str, Any]:
    """获取场景详情"""
    return ScenesTools().get_scene_info(scene_id)


def update_scene_info(scene_id: str, **kwargs) -> Dict[str, Any]:
    """更新场景信息"""
    return ScenesTools().update_scene_info(scene_id, **kwargs)


def delete_scene(scene_id: str, **kwargs) -> Dict[str, Any]:
    """删除场景"""
    return ScenesTools().delete_scene(scene_id, **kwargs)

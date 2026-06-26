"""Dida365 API Client."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, TypeVar, Union


from auth import get_access_token, refresh_access_token
from models import Project, Task, ProjectData


T = TypeVar("T")

API_BASE = "https://api.dida365.com/open/v1"


class Dida365Client:
    """
    滴答清单 API 客户端。
    负责底层 HTTP 请求、Token 管理及错误处理。
    """

    def __init__(self, token: Optional[str] = None):
        self._token = token

    @property
    def token(self) -> str:
        """获取并验证 Access Token。"""
        if self._token:
            return self._token
        return get_access_token()

    def request(
        self,
        method: str,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Any]]] = None,
        retry: bool = True,
    ) -> Any:
        """
        发送请求到 Dida365 API。
        
        :param method: HTTP 方法 (GET, POST, DELETE 等)。
        :param path: 相对 API 路径 (例如 '/project')。
        :param body: 请求体内容。
        :param retry: 401 错误时是否尝试刷新 token 并重试。
        :return: 解析后的 JSON 数据或原始响应内容。
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = None

        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif method in {"POST", "PUT", "PATCH"}:
            data = b""

        url = f"{API_BASE}{path}"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(request) as response:
                if response.status == 204:
                    return None

                payload = response.read()
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    if not payload:
                        return None
                    return json.loads(payload.decode("utf-8"))
                return payload.decode("utf-8")

        except urllib.error.HTTPError as exc:
            # 读取详细错误信息
            try:
                error_body = exc.read().decode("utf-8", errors="replace")
                error_detail = json.loads(error_body) if error_body.startswith("{") else error_body
            except Exception:
                error_detail = "无法解析错误响应体"

            # 401 自动刷新 Token
            if exc.code == 401 and retry and not os.environ.get("DIDA_ACCESS_TOKEN"):
                try:
                    refresh_access_token()
                    return self.request(method, path, body=body, retry=False)
                except Exception as refresh_exc:
                    raise RuntimeError(f"Token 刷新失败: {refresh_exc}") from refresh_exc

            # 抛出详细错误
            error_msg = f"API 错误: {method} {path} (HTTP {exc.code})\n详情: {json.dumps(error_detail, ensure_ascii=False, indent=2) if isinstance(error_detail, dict) else error_detail}"
            raise RuntimeError(error_msg) from exc

    # --- Project API ---

    def list_projects(self) -> List[Project]:
        """获取用户所有项目。"""
        return self.request("GET", "/project")

    def get_project(self, project_id: str) -> Project:
        """获取单个项目元数据。"""
        return self.request("GET", f"/project/{project_id}")

    def get_project_data(self, project_id: str) -> ProjectData:
        """获取项目及其任务、列数据。"""
        return self.request("GET", f"/project/{project_id}/data")

    def create_project(self, data: Project) -> Project:
        """
        创建新项目。
        支持: name, color, sortOrder, viewMode, kind。
        """
        return self.request("POST", "/project", body=data)

    def update_project(self, project_id: str, data: Project) -> Project:
        """
        更新项目属性。
        支持: name, color, sortOrder, viewMode, kind。
        """
        return self.request("POST", f"/project/{project_id}", body=data)

    def delete_project(self, project_id: str) -> None:
        """删除项目。"""
        self.request("DELETE", f"/project/{project_id}")

    # --- Task API ---

    def get_task(self, project_id: str, task_id: str) -> Task:
        """获取单个任务详情。"""
        return self.request("GET", f"/project/{project_id}/task/{task_id}")

    def create_task(self, task_data: Task) -> Task:
        """创建新任务。"""
        return self.request("POST", "/task", body=task_data)

    def update_task(self, task_id: str, project_id: str, data: Task) -> Task:
        """更新任务属性。"""
        payload = dict(data)
        payload["projectId"] = project_id
        return self.request("POST", f"/task/{task_id}", body=payload)

    def complete_task(self, project_id: str, task_id: str) -> None:
        """标记任务为完成。"""
        self.request("POST", f"/project/{project_id}/task/{task_id}/complete")

    def delete_task(self, project_id: str, task_id: str) -> None:
        """删除任务。"""
        self.request("DELETE", f"/project/{project_id}/task/{task_id}")

    def move_tasks(self, operations: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """跨项目移动任务。"""
        return self.request("POST", "/task/move", body=operations)

    def list_completed_tasks(
        self,
        project_ids: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Task]:
        """查询已完成任务。"""
        payload: Dict[str, Any] = {}
        if project_ids:
            payload["projectIds"] = project_ids
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        return self.request("POST", "/task/completed", body=payload)

    def filter_tasks(self, filters: Dict[str, Any]) -> List[Task]:
        """高级筛选任务。"""
        return self.request("POST", "/task/filter", body=filters)

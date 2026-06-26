"""Dida365 OpenAPI client helpers."""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote

from .config import RuntimeSettings
from .errors import UserFacingError
from .http import HttpResponse, HttpTransport, UNSET


class Dida365Client:
    """Minimal Dida365 OpenAPI client with exact endpoint mappings."""

    def __init__(
        self,
        settings: RuntimeSettings,
        *,
        transport: Optional[HttpTransport] = None,
    ) -> None:
        self.settings = settings
        self.transport = transport or HttpTransport()
        self._project_cache: Optional[list[dict[str, Any]]] = None
        self._inbox_project_id_cache: Optional[str] = None

    def list_projects(self) -> HttpResponse:
        return self._request("GET", "/open/v1/project")

    def get_project(self, project_id: str) -> HttpResponse:
        return self._request("GET", f"/open/v1/project/{self._segment(project_id)}")

    def get_project_data(self, project_id: str) -> HttpResponse:
        return self._request("GET", f"/open/v1/project/{self._segment(project_id)}/data")

    def create_project(self, payload: dict[str, Any]) -> HttpResponse:
        response = self._request("POST", "/open/v1/project", json_body=payload)
        self._project_cache = None
        return response

    def update_project(self, project_id: str, payload: dict[str, Any]) -> HttpResponse:
        response = self._request("POST", f"/open/v1/project/{self._segment(project_id)}", json_body=payload)
        self._project_cache = None
        return response

    def delete_project(self, project_id: str) -> HttpResponse:
        response = self._request("DELETE", f"/open/v1/project/{self._segment(project_id)}")
        self._project_cache = None
        return response

    def get_task(self, project_id: str, task_id: str) -> HttpResponse:
        return self._request(
            "GET",
            f"/open/v1/project/{self._segment(project_id)}/task/{self._segment(task_id)}",
        )

    def create_task(self, payload: dict[str, Any]) -> HttpResponse:
        return self._request("POST", "/open/v1/task", json_body=payload)

    def update_task(self, task_id: str, payload: dict[str, Any]) -> HttpResponse:
        return self._request("POST", f"/open/v1/task/{self._segment(task_id)}", json_body=payload)

    def complete_task(self, project_id: str, task_id: str) -> HttpResponse:
        return self._request(
            "POST",
            f"/open/v1/project/{self._segment(project_id)}/task/{self._segment(task_id)}/complete",
        )

    def delete_task(self, project_id: str, task_id: str) -> HttpResponse:
        return self._request(
            "DELETE",
            f"/open/v1/project/{self._segment(project_id)}/task/{self._segment(task_id)}",
        )

    def move_task(self, payload: list[dict[str, Any]]) -> HttpResponse:
        return self._request("POST", "/open/v1/task/move", json_body=payload)

    def list_completed_tasks(self, payload: dict[str, Any]) -> HttpResponse:
        return self._request("POST", "/open/v1/task/completed", json_body=payload)

    def filter_tasks(self, payload: dict[str, Any]) -> HttpResponse:
        return self._request("POST", "/open/v1/task/filter", json_body=payload)

    def resolve_project_id(
        self,
        *,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> str:
        if project_id:
            return project_id
        if not project_name:
            raise UserFacingError("Either --project-id or --project-name is required")

        matches = []
        for item in self._project_items():
            if isinstance(item, dict) and item.get("name") == project_name:
                matches.append(item)

        if not matches:
            raise UserFacingError(
                "Project name did not match any project",
                details={"project_name": project_name},
            )
        if len(matches) > 1:
            raise UserFacingError(
                "Project name matched multiple projects",
                details={
                    "project_name": project_name,
                    "project_ids": [item.get("id") for item in matches],
                },
            )
        project_identifier = matches[0].get("id")
        if not project_identifier:
            raise UserFacingError(
                "Matched project did not contain an id",
                details={"project_name": project_name},
                exit_code=1,
            )
        return str(project_identifier)

    def resolve_concrete_inbox_project_id(self) -> str:
        if self._inbox_project_id_cache:
            return self._inbox_project_id_cache

        candidate = self._find_concrete_inbox_project_id()
        if not candidate:
            raise UserFacingError(
                "Could not determine the concrete inbox project id automatically",
                details={
                    "hint": (
                        "Literal projectId 'inbox' is not reliable for delete, move, completed, or filter. "
                        "Use a real inbox project id, or keep at least one inbox task available so it can be inferred."
                    )
                },
                exit_code=1,
            )

        self._inbox_project_id_cache = candidate
        return candidate

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = UNSET,
    ) -> HttpResponse:
        token = self.settings.access_token
        if not token:
            raise UserFacingError(
                "Access token is required. Run auth exchange-code or auth login-local first.",
            )
        return self.transport.request(
            method,
            f"{self.settings.api_base_url.rstrip('/')}{path}",
            headers={"Authorization": f"Bearer {token}"},
            json_body=json_body,
            timeout=self.settings.timeout,
        )

    def _segment(self, value: str) -> str:
        return quote(str(value), safe="")

    def _project_items(self) -> list[dict[str, Any]]:
        if self._project_cache is None:
            response = self.list_projects()
            if not isinstance(response.data, list):
                raise UserFacingError("Project list endpoint did not return a JSON array", exit_code=1)
            self._project_cache = [item for item in response.data if isinstance(item, dict)]
        return self._project_cache

    def _find_concrete_inbox_project_id(self) -> Optional[str]:
        response = self.get_project_data("inbox")
        candidate = self._extract_inbox_project_id(response.data)
        if candidate:
            return candidate

        response = self.filter_tasks({"status": [0]})
        candidate = self._extract_inbox_project_id(response.data)
        if candidate:
            return candidate

        response = self.list_completed_tasks({})
        return self._extract_inbox_project_id(response.data)

    def _extract_inbox_project_id(self, data: Any) -> Optional[str]:
        for candidate in self._iter_project_id_candidates(data):
            if candidate.startswith("inbox") and candidate != "inbox":
                return candidate
        return None

    def _iter_project_id_candidates(self, data: Any) -> list[str]:
        candidates: list[str] = []
        if isinstance(data, dict):
            project = data.get("project")
            if isinstance(project, dict):
                project_id = project.get("id")
                if project_id:
                    candidates.append(str(project_id))
            for key in ("tasks", "columns"):
                values = data.get(key)
                if isinstance(values, list):
                    for item in values:
                        if isinstance(item, dict):
                            project_id = item.get("projectId")
                            if project_id:
                                candidates.append(str(project_id))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    project_id = item.get("projectId")
                    if project_id:
                        candidates.append(str(project_id))
        return candidates

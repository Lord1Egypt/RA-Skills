"""Dida365 Data Models."""

from __future__ import annotations

from typing import Any, List, Optional, TypedDict


class ChecklistItem(TypedDict, total=False):
    """
    子任务（清单项）模型。
    """
    id: str
    title: str
    status: int  # 0: Normal, 1: Completed
    completedTime: Optional[str]
    isAllDay: bool
    sortOrder: int
    startDate: Optional[str]
    timeZone: Optional[str]


class Task(TypedDict, total=False):
    """
    任务数据模型。
    """
    id: str
    projectId: str
    title: str
    isAllDay: bool
    completedTime: Optional[str]
    content: str
    desc: str  # Checklist 任务的描述
    dueDate: Optional[str]
    items: List[ChecklistItem]
    priority: int  # 0: None, 1: Low, 3: Medium, 5: High
    reminders: List[str]
    repeatFlag: Optional[str]
    sortOrder: int
    startDate: Optional[str]
    status: int  # 0: Normal, 2: Completed
    timeZone: Optional[str]
    kind: str  # "TEXT", "NOTE", "CHECKLIST"
    etag: Optional[str]


class Project(TypedDict, total=False):
    """
    项目数据模型。
    """
    id: str
    name: str
    color: Optional[str]
    sortOrder: Optional[int]
    closed: Optional[bool]
    groupId: Optional[str]
    viewMode: Optional[str]  # "list", "kanban", "timeline"
    permission: Optional[str]  # "read", "write", "comment"
    kind: Optional[str]  # "TASK", "NOTE"
    inAll: Optional[bool]
    isOwner: Optional[bool]


class Column(TypedDict):
    """
    看板列模型。
    """
    id: str
    projectId: str
    name: str
    sortOrder: int


class ProjectData(TypedDict):
    """
    项目完整数据包模型（包含任务和列）。
    """
    project: Project
    tasks: List[Task]
    columns: List[Column]

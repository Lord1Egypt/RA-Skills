"""Abstract base classes and shared data models for code and ticket adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class MergeRequest:
    id: str
    title: str
    author: str
    source_branch: str
    state: str
    created_at: datetime
    merged_at: Optional[datetime]
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    url: str = ""


@dataclass
class Branch:
    name: str
    author: str
    last_commit_at: datetime
    created_at: Optional[datetime] = None
    last_commit_sha: str = ""


@dataclass
class Ticket:
    key: str
    title: str
    status: str
    url: str
    assignee: Optional[str] = None
    epic_key: Optional[str] = None
    epic_title: Optional[str] = None
    ticket_type: str = "Story"
    priority: str = "Medium"
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Epic:
    key: str
    title: str
    status: str
    url: str
    assignee: Optional[str] = None
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    days_since_update: int = 0
    child_count: int = 0


class CodeAdapter(ABC):
    """Abstract interface for code platform APIs (GitLab, GitHub)."""

    @abstractmethod
    def get_merge_requests(self, days: int = 30) -> List[MergeRequest]:
        ...

    @abstractmethod
    def get_branches(self, days: int = 30) -> List[Branch]:
        ...


class TicketAdapter(ABC):
    """Abstract interface for ticket system APIs (Jira, GitHub Issues)."""

    @abstractmethod
    def get_tickets(self, project_keys: List[str]) -> List[Ticket]:
        ...

    @abstractmethod
    def get_epics(self, project_keys: List[str]) -> List[Epic]:
        ...

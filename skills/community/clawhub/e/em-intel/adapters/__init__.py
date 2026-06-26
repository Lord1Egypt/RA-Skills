"""Adapters for code platforms (GitLab, GitHub) and ticket systems (Jira, GitHub Issues)."""

from .base import CodeAdapter, TicketAdapter, MergeRequest, Branch, Ticket, Epic
from .gitlab_adapter import GitLabAdapter
from .github_adapter import GitHubAdapter
from .jira_adapter import JiraAdapter
from .github_issues_adapter import GitHubIssuesAdapter

__all__ = [
    "CodeAdapter",
    "TicketAdapter",
    "MergeRequest",
    "Branch",
    "Ticket",
    "Epic",
    "GitLabAdapter",
    "GitHubAdapter",
    "JiraAdapter",
    "GitHubIssuesAdapter",
]

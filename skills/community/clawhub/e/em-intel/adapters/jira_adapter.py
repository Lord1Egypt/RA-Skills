"""Jira REST API adapter for tickets and epics."""

import logging
import os
from base64 import b64encode
from datetime import datetime, timezone
from typing import List

import requests

from .base import Epic, Ticket, TicketAdapter

logger = logging.getLogger(__name__)


class JiraAdapter(TicketAdapter):
    """Fetch tickets and epics from Jira Cloud."""

    def __init__(
        self,
        url: str | None = None,
        email: str | None = None,
        token: str | None = None,
    ):
        self.url = (url or os.getenv("JIRA_URL", "")).rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL", "")
        self.token = token or os.getenv("JIRA_TOKEN", "")
        creds = b64encode(f"{self.email}:{self.token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {creds}",
            "Accept": "application/json",
        }

    def _search(self, jql: str, fields: str, max_results: int = 200) -> list:
        """Run a JQL search with pagination."""
        results: list = []
        start = 0
        while True:
            try:
                resp = requests.get(
                    f"{self.url}/rest/api/3/search/jql",
                    headers=self.headers,
                    params={
                        "jql": jql,
                        "fields": fields,
                        "startAt": start,
                        "maxResults": min(max_results - len(results), 100),
                    },
                    timeout=30,
                )
                resp.raise_for_status()
            except requests.RequestException as exc:
                logger.warning("Jira API error: %s", exc)
                break
            data = resp.json()
            issues = data.get("issues", [])
            if not issues:
                break
            results.extend(issues)
            if len(results) >= data.get("total", 0) or len(results) >= max_results:
                break
            start += len(issues)
        return results

    def get_tickets(self, project_keys: List[str]) -> List[Ticket]:
        """Fetch open tickets from the given projects."""
        keys = ", ".join(project_keys)
        lookback = int(os.getenv("EM_LOOKBACK_DAYS", "30"))
        jql = (
            f"project in ({keys}) "
            f"AND updated >= -{lookback}d "
            f"AND issuetype != Epic "
            f"ORDER BY updated DESC"
        )
        fields = "summary,status,assignee,priority,issuetype,updated,parent"
        raw = self._search(jql, fields)
        tickets: List[Ticket] = []

        for issue in raw:
            f = issue.get("fields", {})
            assignee = f.get("assignee")
            parent = f.get("parent", {}) or {}
            updated_str = f.get("updated", "")
            updated_at = datetime.now(timezone.utc)
            if updated_str:
                updated_at = datetime.fromisoformat(
                    updated_str.replace("Z", "+00:00")
                )
            tickets.append(
                Ticket(
                    key=issue["key"],
                    title=f.get("summary", ""),
                    status=f.get("status", {}).get("name", "Unknown"),
                    url=f"{self.url}/browse/{issue['key']}",
                    assignee=assignee.get("displayName") if assignee else None,
                    epic_key=parent.get("key"),
                    epic_title=parent.get("fields", {}).get("summary")
                    if parent.get("fields")
                    else None,
                    ticket_type=f.get("issuetype", {}).get("name", "Story"),
                    priority=f.get("priority", {}).get("name", "Medium"),
                    updated_at=updated_at,
                )
            )
        return tickets

    def get_epics(self, project_keys: List[str]) -> List[Epic]:
        """Fetch active epics from the given projects."""
        keys = ", ".join(project_keys)
        jql = (
            f"project in ({keys}) "
            f"AND issuetype = Epic "
            f"AND status NOT IN (Done, Closed) "
            f"ORDER BY updated DESC"
        )
        fields = "summary,status,assignee,updated"
        raw = self._search(jql, fields)
        epics: List[Epic] = []
        now = datetime.now(timezone.utc)

        for issue in raw:
            f = issue.get("fields", {})
            assignee = f.get("assignee")
            updated_str = f.get("updated", "")
            updated_at = now
            if updated_str:
                updated_at = datetime.fromisoformat(
                    updated_str.replace("Z", "+00:00")
                )
            days_since = (now - updated_at).days

            epics.append(
                Epic(
                    key=issue["key"],
                    title=f.get("summary", ""),
                    status=f.get("status", {}).get("name", "Unknown"),
                    url=f"{self.url}/browse/{issue['key']}",
                    assignee=assignee.get("displayName") if assignee else None,
                    updated_at=updated_at,
                    days_since_update=days_since,
                )
            )
        return epics

"""GitHub Issues adapter — use GitHub Issues as a ticket/epic system."""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List

import requests

from .base import Epic, Ticket, TicketAdapter

logger = logging.getLogger(__name__)


class GitHubIssuesAdapter(TicketAdapter):
    """Fetch issues (tickets) and milestones (epics) from GitHub repos."""

    def __init__(
        self,
        token: str | None = None,
        org: str | None = None,
        repos: list[str] | None = None,
    ):
        self.token = token or os.getenv("GITHUB_TOKEN", "")
        self.org = org or os.getenv("GITHUB_ORG", "")
        repos_env = os.getenv("GITHUB_REPOS", "")
        self.repos = repos or [r.strip() for r in repos_env.split(",") if r.strip()]
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }
        self.base = "https://api.github.com"

    def _get(self, path: str, params: dict | None = None) -> list:
        """Paginated GET helper."""
        results: list = []
        params = params or {}
        params.setdefault("per_page", 100)
        page = 1
        while True:
            params["page"] = page
            try:
                resp = requests.get(
                    f"{self.base}{path}",
                    headers=self.headers,
                    params=params,
                    timeout=30,
                )
                resp.raise_for_status()
            except requests.RequestException as exc:
                logger.warning("GitHub Issues API error on %s: %s", path, exc)
                break
            data = resp.json()
            if not data:
                break
            results.extend(data)
            page += 1
        return results

    def get_tickets(self, project_keys: List[str]) -> List[Ticket]:
        """Fetch open issues from configured repos. project_keys are ignored (repos from env)."""
        lookback = int(os.getenv("EM_LOOKBACK_DAYS", "30"))
        since = (datetime.now(timezone.utc) - timedelta(days=lookback)).isoformat()
        tickets: List[Ticket] = []

        for repo in self.repos:
            raw = self._get(
                f"/repos/{self.org}/{repo}/issues",
                params={"state": "open", "since": since, "sort": "updated"},
            )
            for item in raw:
                # Skip pull requests (GitHub returns them in issues endpoint)
                if item.get("pull_request"):
                    continue
                assignee = item.get("assignee")
                milestone = item.get("milestone")
                labels = [lb.get("name", "") for lb in item.get("labels", [])]
                priority = "High" if "priority:high" in labels else "Medium"
                updated_str = item.get("updated_at", "")
                updated_at = datetime.now(timezone.utc)
                if updated_str:
                    updated_at = datetime.fromisoformat(
                        updated_str.replace("Z", "+00:00")
                    )
                tickets.append(
                    Ticket(
                        key=f"{repo}#{item['number']}",
                        title=item.get("title", ""),
                        status="Open",
                        url=item.get("html_url", ""),
                        assignee=assignee.get("login") if assignee else None,
                        epic_key=str(milestone["number"]) if milestone else None,
                        epic_title=milestone.get("title") if milestone else None,
                        ticket_type="Issue",
                        priority=priority,
                        updated_at=updated_at,
                    )
                )
        return tickets

    def get_epics(self, project_keys: List[str]) -> List[Epic]:
        """Fetch open milestones as epics from configured repos."""
        epics: List[Epic] = []
        now = datetime.now(timezone.utc)

        for repo in self.repos:
            raw = self._get(
                f"/repos/{self.org}/{repo}/milestones",
                params={"state": "open", "sort": "updated"},
            )
            for item in raw:
                updated_str = item.get("updated_at", "")
                updated_at = now
                if updated_str:
                    updated_at = datetime.fromisoformat(
                        updated_str.replace("Z", "+00:00")
                    )
                days_since = (now - updated_at).days
                epics.append(
                    Epic(
                        key=f"{repo}#M{item['number']}",
                        title=item.get("title", ""),
                        status="Open",
                        url=item.get("html_url", ""),
                        updated_at=updated_at,
                        days_since_update=days_since,
                        child_count=item.get("open_issues", 0),
                    )
                )
        return epics

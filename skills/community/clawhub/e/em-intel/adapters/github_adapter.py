"""GitHub REST API adapter for pull requests and branches."""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List

import requests

from .base import Branch, CodeAdapter, MergeRequest

logger = logging.getLogger(__name__)


class GitHubAdapter(CodeAdapter):
    """Fetch pull requests and branches from GitHub repositories."""

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
                logger.warning("GitHub API error on %s: %s", path, exc)
                break
            data = resp.json()
            if not data:
                break
            results.extend(data)
            page += 1
        return results

    def get_merge_requests(self, days: int = 30) -> List[MergeRequest]:
        """Fetch pull requests from all configured repos."""
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        mrs: List[MergeRequest] = []

        for repo in self.repos:
            raw = self._get(
                f"/repos/{self.org}/{repo}/pulls",
                params={"state": "all", "sort": "updated", "direction": "desc"},
            )
            for item in raw:
                updated = item.get("updated_at", "")
                if updated and updated < since:
                    break  # sorted by updated desc, so we can stop

                merged_at = None
                if item.get("merged_at"):
                    merged_at = datetime.fromisoformat(
                        item["merged_at"].replace("Z", "+00:00")
                    )

                state = "merged" if merged_at else item.get("state", "open")
                mrs.append(
                    MergeRequest(
                        id=str(item["number"]),
                        title=item.get("title", ""),
                        author=item.get("user", {}).get("login", "unknown"),
                        source_branch=item.get("head", {}).get("ref", ""),
                        state=state,
                        created_at=datetime.fromisoformat(
                            item["created_at"].replace("Z", "+00:00")
                        ),
                        merged_at=merged_at,
                        url=item.get("html_url", ""),
                    )
                )
        return mrs

    def get_branches(self, days: int = 30) -> List[Branch]:
        """Fetch branches from all configured repos."""
        branches: List[Branch] = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        for repo in self.repos:
            raw = self._get(f"/repos/{self.org}/{repo}/branches")
            for item in raw:
                sha = item.get("commit", {}).get("sha", "")
                if not sha:
                    continue
                # Get commit details for date and author
                try:
                    resp = requests.get(
                        f"{self.base}/repos/{self.org}/{repo}/commits/{sha}",
                        headers=self.headers,
                        timeout=30,
                    )
                    resp.raise_for_status()
                    commit_data = resp.json()
                except requests.RequestException as exc:
                    logger.warning("GitHub commit fetch error: %s", exc)
                    continue

                commit_info = commit_data.get("commit", {})
                date_str = commit_info.get("committer", {}).get("date", "")
                if not date_str:
                    continue
                last_commit = datetime.fromisoformat(
                    date_str.replace("Z", "+00:00")
                )
                if last_commit < cutoff:
                    continue

                author = (
                    commit_data.get("author", {}).get("login")
                    or commit_info.get("author", {}).get("name", "unknown")
                )
                branches.append(
                    Branch(
                        name=item["name"],
                        author=author,
                        last_commit_at=last_commit,
                        last_commit_sha=sha,
                    )
                )
        return branches

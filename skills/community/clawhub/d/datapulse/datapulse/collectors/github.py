"""GitHub repository collector using GitHub REST API."""

from __future__ import annotations

from urllib.parse import urlparse

import requests

from datapulse.core.models import SourceType
from datapulse.core.utils import clean_text, generate_excerpt

from .base import BaseCollector, ParseResult


class GitHubCollector(BaseCollector):
    name = "github"
    source_type = SourceType.GENERIC
    reliability = 0.82
    tier = 1
    setup_hint = ""
    api_base = "https://api.github.com"
    github_user_agent = "DataPulse/0.1 (+https://github.com/sunyifei83/DataPulse)"
    timeout = 15

    _blocked_owner_roots = {
        "about",
        "account",
        "collections",
        "contact",
        "enterprise",
        "events",
        "explore",
        "features",
        "issues",
        "login",
        "logout",
        "marketplace",
        "new",
        "notifications",
        "orgs",
        "organizations",
        "pricing",
        "pulls",
        "search",
        "security",
        "settings",
        "signup",
        "site",
        "sponsors",
        "topics",
        "trending",
    }

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "public GitHub REST API", "available": True}

    def can_handle(self, url: str) -> bool:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host not in {"github.com", "www.github.com"}:
            return False
        repo = self._extract_repo_slug(url)
        return repo is not None

    def parse(self, url: str) -> ParseResult:
        repo = self._extract_repo_slug(url)
        if repo is None:
            return ParseResult.failure(url, "Invalid GitHub repository URL.")
        owner, repo_name = repo
        slug = f"{owner}/{repo_name}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": self.github_user_agent,
        }
        api_url = f"{self.api_base}/repos/{owner}/{repo_name}"

        degraded = False
        degraded_reason = ""
        repo_payload: dict = {}
        try:
            response = requests.get(api_url, headers=headers, timeout=self.timeout)
            if response.status_code == 404:
                return ParseResult.failure(url, f"GitHub repo not found: {slug}")
            if response.status_code >= 400:
                degraded = True
                degraded_reason = f"github_api_http_{response.status_code}"
            else:
                parsed_payload = response.json()
                if isinstance(parsed_payload, dict):
                    repo_payload = parsed_payload
                else:
                    degraded = True
                    degraded_reason = "github_api_non_json"
        except requests.RequestException as exc:
            degraded = True
            degraded_reason = str(exc)

        release = self._fetch_latest_release(owner, repo_name, headers=headers)

        if repo_payload:
            title = str(repo_payload.get("full_name", slug))
            description = str(repo_payload.get("description", "") or "").strip()
            stars = int(repo_payload.get("stargazers_count") or 0)
            forks = int(repo_payload.get("forks_count") or 0)
            open_issues = int(repo_payload.get("open_issues_count") or 0)
            watchers = int(repo_payload.get("subscribers_count") or 0)
            language = str(repo_payload.get("language", "") or "").strip()
            pushed_at = str(repo_payload.get("pushed_at", "") or "")
            created_at = str(repo_payload.get("created_at", "") or "")
            updated_at = str(repo_payload.get("updated_at", "") or "")

            content_lines = [f"# {title}"]
            if description:
                content_lines.append(description)
            content_lines.append("")
            content_lines.append(f"⭐ {stars:,} · Forks {forks:,} · Open issues {open_issues:,}")
            if language:
                content_lines.append(f"Language: {language}")
            if pushed_at:
                content_lines.append(f"Last push: {pushed_at}")
            if release.get("tag_name"):
                content_lines.append(
                    f"Latest release: {release.get('tag_name')} ({release.get('published_at', '')})"
                )

            confidence_flags = ["github_api", "rich_data"]
            if degraded:
                confidence_flags.append("fetch_degraded")

            return ParseResult(
                url=url,
                title=title,
                content=clean_text("\n".join(content_lines)),
                author=owner,
                excerpt=generate_excerpt(description or f"GitHub repository {slug}"),
                tags=["github", "repository", owner.lower()],
                source_type=self.source_type,
                confidence_flags=confidence_flags,
                extra={
                    "repo": slug.lower(),
                    "owner": owner,
                    "repo_name": repo_name,
                    "stars": stars,
                    "forks": forks,
                    "open_issues": open_issues,
                    "watchers": watchers,
                    "language": language,
                    "license": (
                        (repo_payload.get("license") or {}).get("spdx_id")
                        if isinstance(repo_payload.get("license"), dict)
                        else ""
                    ),
                    "topics": repo_payload.get("topics", []),
                    "default_branch": repo_payload.get("default_branch", ""),
                    "pushed_at": pushed_at,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "archived": bool(repo_payload.get("archived", False)),
                    "disabled": bool(repo_payload.get("disabled", False)),
                    "html_url": repo_payload.get("html_url") or url,
                    "homepage": repo_payload.get("homepage", ""),
                    "release": release,
                    "collector": "github",
                    "api_degraded": degraded,
                    "degraded_reason": degraded_reason,
                },
            )

        # Fail-closed degraded output: keep deterministic evidence chain and avoid
        # routing to generic collector with inflated confidence on upstream failures.
        return ParseResult(
            url=url,
            title=slug,
            content=clean_text(
                f"# {slug}\n\nGitHub metadata degraded.\nURL: {url}\nReason: {degraded_reason or 'unknown'}"
            ),
            author=owner,
            excerpt=generate_excerpt(f"GitHub metadata degraded for {slug}"),
            tags=["github", "repository", owner.lower(), "degraded"],
            source_type=self.source_type,
            confidence_flags=["fetch_degraded"],
            extra={
                "repo": slug.lower(),
                "owner": owner,
                "repo_name": repo_name,
                "release": release,
                "collector": "github",
                "api_degraded": True,
                "degraded_reason": degraded_reason or "github_api_unavailable",
            },
        )

    def _fetch_latest_release(self, owner: str, repo_name: str, *, headers: dict[str, str]) -> dict:
        url = f"{self.api_base}/repos/{owner}/{repo_name}/releases/latest"
        try:
            resp = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.RequestException:
            return {}
        if resp.status_code != 200:
            return {}
        payload = resp.json()
        if not isinstance(payload, dict):
            return {}
        return {
            "tag_name": payload.get("tag_name", ""),
            "name": payload.get("name", ""),
            "published_at": payload.get("published_at", ""),
            "html_url": payload.get("html_url", ""),
        }

    def _extract_repo_slug(self, url: str) -> tuple[str, str] | None:
        parsed = urlparse(url)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2:
            return None
        owner = parts[0].strip()
        repo = parts[1].strip()
        if not owner or not repo:
            return None
        if owner.lower() in self._blocked_owner_roots:
            return None
        if repo.endswith(".git"):
            repo = repo[:-4]
        if not repo:
            return None
        return owner, repo

"""
GitHub PR & Repo Manager — OpenClaw skill
"""
import json
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class PullRequest:
    number: int
    title: str
    state: str
    author: str
    branch: str
    additions: int
    deletions: int
    changed_files: int
    review_comments: int
    url: str


@dataclass
class Issue:
    number: int
    title: str
    state: str
    author: str
    labels: list
    assignees: list
    comments: int
    url: str


class GitHubClient:
    """Simple GitHub API client using requests or urllib."""

    def __init__(self, token: str = None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.base = "https://api.github.com"

    def _headers(self):
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, path: str, data: dict = None):
        import urllib.request
        url = f"{self.base}{path}"
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": e.code, "message": e.read().decode()[:200]}

    def list_prs(self, repo: str, state: str = "open") -> list[PullRequest]:
        data = self._request("GET", f"/repos/{repo}/pulls?state={state}&per_page=30")
        if isinstance(data, dict) and "error" in data:
            return []
        return [PullRequest(
            number=p["number"], title=p["title"], state=p["state"],
            author=p["user"]["login"], branch=p["head"]["ref"],
            additions=p.get("additions", 0), deletions=p.get("deletions", 0),
            changed_files=p.get("changed_files", 0),
            review_comments=p.get("review_comments", 0), url=p["html_url"]
        ) for p in data]

    def list_issues(self, repo: str, state: str = "open") -> list[Issue]:
        data = self._request("GET", f"/repos/{repo}/issues?state={state}&per_page=30")
        if isinstance(data, dict) and "error" in data:
            return []
        return [Issue(
            number=i["number"], title=i["title"], state=i["state"],
            author=i["user"]["login"],
            labels=[l["name"] for l in i.get("labels", [])],
            assignees=[a["login"] for a in i.get("assignees", [])],
            comments=i.get("comments", 0), url=i["html_url"]
        ) for i in data if "pull_request" not in i]

    def create_issue(self, repo: str, title: str, body: str = "", labels: list = None) -> dict:
        data = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        return self._request("POST", f"/repos/{repo}/issues", data)

    def comment_pr(self, repo: str, pr_number: int, body: str) -> dict:
        return self._request("POST", f"/repos/{repo}/issues/{pr_number}/comments", {"body": body})

    def list_branches(self, repo: str) -> list[str]:
        data = self._request("GET", f"/repos/{repo}/branches?per_page=50")
        if isinstance(data, dict) and "error" in data:
            return []
        return [b["name"] for b in data]

    def repo_info(self, repo: str) -> dict:
        data = self._request("GET", f"/repos/{repo}")
        if "error" in data:
            return data
        return {
            "name": data.get("full_name"),
            "description": data.get("description", ""),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "language": data.get("language"),
            "open_issues": data.get("open_issues_count", 0),
            "default_branch": data.get("default_branch"),
        }

    def list_org_repos(self, org: str) -> list[dict]:
        data = self._request("GET", f"/orgs/{org}/repos?per_page=100")
        if isinstance(data, dict) and "error" in data:
            return []
        return [{"name": r["name"], "desc": r.get("description", ""), "stars": r.get("stargazers_count", 0), "lang": r.get("language")} for r in data]


if __name__ == "__main__":
    import click

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.option("--repo", required=True)
    @click.option("--state", default="open")
    def prs(repo, state):
        client = GitHubClient()
        for pr in client.list_prs(repo, state):
            click.echo(f"#{pr.number} {pr.title} (@{pr.author}) +{pr.additions}/-{pr.deletions}")

    @cli.command()
    @click.option("--repo", required=True)
    @click.option("--state", default="open")
    def issues(repo, state):
        client = GitHubClient()
        for i in client.list_issues(repo, state):
            labels = ",".join(i.labels) if i.labels else "-"
            click.echo(f"#{i.number} {i.title} [{labels}] (@{i.author})")

    @cli.command()
    @click.option("--org", default="EvezArt")
    def repos(org):
        client = GitHubClient()
        for r in client.list_org_repos(org):
            click.echo(f"{r['name']:30s} ⭐{r['stars']} {r['lang'] or ''}")

    cli()

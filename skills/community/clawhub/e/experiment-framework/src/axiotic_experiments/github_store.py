from __future__ import annotations

import base64
import json
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class GitHubStoreError(RuntimeError):
    pass


_TOKEN_PATTERNS = (
    re.compile(r"\brpa_[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
)


def assert_no_secret_material(directory: Path) -> None:
    for path in directory.rglob("*"):
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(text) for pattern in _TOKEN_PATTERNS):
            raise GitHubStoreError(f"credential-like material detected in {path}")


class GitHubResultStore:
    def __init__(self, *, repo_dir: Path, results_prefix: str):
        self.repo_dir = repo_dir.expanduser().absolute()
        self.results_prefix = results_prefix.strip("/")

    def stage(self, bundle_dir: Path, *, run_id: str) -> Path:
        assert_no_secret_material(bundle_dir)
        destination = self.repo_dir / self.results_prefix / run_id
        destination.mkdir(parents=True, exist_ok=True)
        for source in bundle_dir.iterdir():
            target = destination / source.name
            if source.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(source, target)
            elif source.is_file():
                shutil.copy2(source, target)
        return destination

    def commit_and_push(self, *, run_id: str, branch: str) -> str:
        if not (self.repo_dir / ".git").exists():
            raise GitHubStoreError(f"not a Git repository: {self.repo_dir}")
        current = self._git("branch", "--show-current")
        if current != branch:
            raise GitHubStoreError(
                f"results branch mismatch: expected {branch!r}, current {current!r}"
            )
        relative = f"{self.results_prefix}/{run_id}"
        self._git("add", "--", relative)
        diff = subprocess.run(
            [
                "git",
                "-C",
                str(self.repo_dir),
                "diff",
                "--cached",
                "--quiet",
                "--",
                relative,
            ],
            check=False,
        )
        if diff.returncode not in {0, 1}:
            raise GitHubStoreError("git diff --cached failed")
        if diff.returncode == 1:
            self._git(
                "commit",
                "-m",
                f"[{run_id}] publish experiment results",
                "--",
                relative,
            )
        commit = self._git("rev-parse", "HEAD")
        self._git("push", "origin", f"HEAD:{branch}")
        return commit

    def _git(self, *args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repo_dir), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            raise GitHubStoreError(
                (completed.stdout + completed.stderr).strip()
                or f"git {' '.join(args)} failed"
            )
        return completed.stdout.strip()


class GitHubApiResultStore:
    """Publish small result bundles through GitHub's Contents API."""

    def __init__(
        self,
        *,
        repo: str,
        branch: str,
        results_prefix: str,
        token: str,
        api_base: str = "https://api.github.com",
    ):
        if not token:
            raise GitHubStoreError("GITHUB_TOKEN is required")
        self.repo = repo
        self.branch = branch
        self.results_prefix = results_prefix.strip("/")
        self.token = token
        self.api_base = api_base.rstrip("/")

    def upload_bundle(self, bundle_dir: Path, *, run_id: str) -> str:
        assert_no_secret_material(bundle_dir)
        files = sorted(path for path in bundle_dir.iterdir() if path.is_file())
        if not files:
            raise GitHubStoreError(f"result bundle is empty: {bundle_dir}")
        commit = ""
        for path in files:
            commit = self.upload_file(path, run_id=run_id)
        return commit

    def upload_file(self, source: Path, *, run_id: str) -> str:
        path = f"{self.results_prefix}/{run_id}/{source.name}"
        existing = self._request_json("GET", path, missing_ok=True)
        payload: dict[str, Any] = {
            "message": f"[{run_id}] publish {source.name}",
            "content": base64.b64encode(source.read_bytes()).decode(),
            "branch": self.branch,
        }
        if existing is not None:
            payload["sha"] = existing["sha"]
        response = self._request_json("PUT", path, payload=payload)
        commit = response.get("commit") or {}
        sha = commit.get("sha")
        if not sha:
            raise GitHubStoreError(f"GitHub did not return a commit for {path}")
        return str(sha)

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        missing_ok: bool = False,
    ) -> dict[str, Any] | None:
        quoted_path = urllib.parse.quote(path, safe="/")
        url = f"{self.api_base}/repos/{self.repo}/contents/{quoted_path}"
        if method == "GET":
            url = f"{url}?ref={urllib.parse.quote(self.branch, safe='')}"
        data = (
            json.dumps(payload, separators=(",", ":")).encode()
            if payload is not None
            else None
        )
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "axiotic-experiments",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and missing_ok:
                return None
            try:
                error = json.loads(exc.read()).get("message")
            except (AttributeError, json.JSONDecodeError, UnicodeDecodeError):
                error = None
            raise GitHubStoreError(
                f"GitHub Contents API {method} {path} failed ({exc.code})"
                + (f": {error}" if error else "")
            ) from exc

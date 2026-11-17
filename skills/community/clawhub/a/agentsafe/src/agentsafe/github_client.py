"""GitHub Actions client: dispatch, run association, artifacts.

Association strategy (Prompt 9): the workflow sets
    run-name: audit-${{ inputs.task_id }}
so resolve_run_id matches runs by EXACT name + created_at >= dispatch time,
polls up to `resolve_attempts`, and requires a UNIQUE match. Ambiguity or
no-match raises - never "latest run" guessing.

Artifact safety (Prompt 9): artifact must belong to the given run, its name
must equal audit-report-<task_id>, and the ZIP is extracted with:
absolute paths rejected, traversal rejected, per-file + total size caps,
only the expected report.json accepted.
"""

from __future__ import annotations

import asyncio
import io
import logging
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from agentsafe.schemas import normalize_address

logger = logging.getLogger("agentSAFE.github")

API_BASE = "https://api.github.com"
_TRANSIENT_HTTP = {429, 500, 502, 503, 504}
MAX_ZIP_BYTES = 20 * 1024 * 1024
MAX_MEMBER_BYTES = 20 * 1024 * 1024


class GitHubClientError(RuntimeError):
    pass


class RunAssociationError(GitHubClientError):
    """Could not uniquely associate a dispatch with one run_id."""


class RateLimitedError(GitHubClientError):
    pass


class ArtifactExpiredError(GitHubClientError):
    pass


class GitHubActionsClient:
    def __init__(
        self,
        *,
        token: str,
        repo: str,  # "owner/repo"
        workflow_file: str = "audit.yml",
        ref: str = "main",
        base_url: str = API_BASE,
        timeout_seconds: float = 20.0,
        max_retries: int = 3,
        poll_interval_seconds: float = 10.0,
        resolve_attempts: int = 12,
        client: httpx.AsyncClient | None = None,
        sleeper: Any | None = None,
        strict: bool = True,
    ) -> None:
        if strict:
            # Deferred (strict=False) mode is for cloud build-time inspection
            # only; the server lifespan re-validates config at runtime.
            if not token:
                raise ValueError("GitHub token required")
            if "/" not in repo or repo.count("/") != 1:
                raise ValueError(f"repo must be 'owner/repo', got {repo!r}")
        self._repo = repo
        self._workflow = workflow_file
        # Run-name and artifact prefixes are derived from the workflow file so
        # both audit.yml (audit-*, audit-report-*) and docker-audit.yml
        # (docker-audit-*, docker-audit-report-*) associate correctly.
        base = workflow_file.rsplit(".", 1)[0] if "." in workflow_file else workflow_file
        self._run_name_prefix = f"{base}-"
        self._artifact_name_prefix = f"{base}-report-"
        self._ref = ref
        self._base = base_url.rstrip("/")
        self._max_retries = max_retries
        self._poll_interval = poll_interval_seconds
        self._resolve_attempts = resolve_attempts
        self._sleeper = sleeper or asyncio.sleep
        self._client = client or httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds, connect=timeout_seconds),
            follow_redirects=True,  # artifact downloads 302 to a signed URL
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "agentSAFE-mcp",
            },
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------ core
    async def _request(
        self, method: str, path: str, *, json_body: dict | None = None, params: dict | None = None
    ) -> httpx.Response:
        attempt = 0
        last_detail = "unknown"
        while True:
            transient = False
            try:
                resp = await self._client.request(
                    method,
                    f"{self._base}{path}",
                    json=json_body,
                    params=params,
                )
                if resp.status_code in _TRANSIENT_HTTP:
                    transient = True
                    last_detail = f"HTTP {resp.status_code}"
                elif resp.status_code == 403 and self._is_rate_limited(resp):
                    raise RateLimitedError("GitHub API rate limit exceeded")
                elif resp.status_code >= 400:
                    raise GitHubClientError(f"GitHub API {method} {path}: HTTP {resp.status_code}")
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                transient = True
                last_detail = f"transport error: {exc}"
                resp = None  # type: ignore[assignment]
            if not transient and resp is not None:
                remaining = resp.headers.get("x-ratelimit-remaining")
                if remaining is not None and remaining.isdigit() and int(remaining) < 50:
                    logger.warning("github api rate budget low: %s remaining", remaining)
                return resp
            if attempt >= self._max_retries:
                raise GitHubClientError(
                    f"GitHub API {method} {path}: giving up after {attempt + 1} attempts"
                    f" (last: {last_detail})"
                )
            await self._sleeper(min(1.0 * (2**attempt), 15.0))
            attempt += 1

    @staticmethod
    def _is_rate_limited(resp: httpx.Response) -> bool:
        return "rate limit" in (resp.text or "").lower()

    # ------------------------------------------------------------- dispatch
    async def trigger_workflow(self, address: str, task_id: str) -> datetime:
        """Dispatch the audit workflow. Returns dispatch time for association."""
        addr = normalize_address(address)
        if not task_id or len(task_id) > 64:
            raise ValueError("invalid task_id")
        resp = await self._request(
            "POST",
            f"/repos/{self._repo}/actions/workflows/{self._workflow}/dispatches",
            json_body={"ref": self._ref, "inputs": {"address": addr, "task_id": task_id}},
        )
        # GitHub documents 204 No Content for a successful dispatch.
        if resp.status_code != 204:
            logger.warning(
                "dispatch returned unexpected HTTP %s (expected 204); treating as sent",
                resp.status_code,
            )
        logger.info("workflow dispatched task=%s address=%s", task_id, addr)
        return datetime.now(UTC)

    async def resolve_run_id(
        self, task_id: str, *, dispatched_after: datetime, attempts: int | None = None
    ) -> int:
        """Uniquely resolve the run for this task. Refuses to guess."""
        expected = f"{self._run_name_prefix}{task_id}"
        n = attempts or self._resolve_attempts
        for attempt in range(n):
            runs = await self._list_runs(since=dispatched_after, per_page=50)
            matches = [r for r in runs if r.get("name") == expected]
            if len(matches) == 1:
                return int(matches[0]["id"])
            if len(matches) > 1:
                raise RunAssociationError(f"multiple runs named {expected!r}; refusing to guess")
            if attempt + 1 < n:
                await self._sleeper(self._poll_interval)
        raise RunAssociationError(f"no run named {expected!r} appeared after dispatch")

    async def _list_runs(self, *, since: datetime, per_page: int = 50) -> list[dict]:
        page = 1
        out: list[dict] = []
        while True:
            resp = await self._request(
                "GET",
                f"/repos/{self._repo}/actions/workflows/{self._workflow}/runs",
                params={"per_page": per_page, "page": page},
            )
            data = resp.json()
            batch = data.get("workflow_runs") or []
            for r in batch:
                created = _parse_ts(r.get("created_at"))
                if created and created >= since.replace(tzinfo=UTC):
                    out.append(r)
            # pagination: stop when batch is short or older runs fall below `since`
            if len(batch) < per_page:
                break
            oldest = _parse_ts(batch[-1].get("created_at")) if batch else None
            if oldest and oldest < since.replace(tzinfo=UTC):
                break
            page += 1
            if page > 10:
                break
        return out

    # ---------------------------------------------------------------- status
    async def get_run(self, run_id: int) -> dict[str, Any]:
        resp = await self._request("GET", f"/repos/{self._repo}/actions/runs/{run_id}")
        return resp.json()

    @staticmethod
    def map_run_status(run: dict[str, Any]) -> str:
        """GitHub status/conclusion -> our task state vocabulary."""
        status = (run.get("status") or "").lower()
        conclusion = (run.get("conclusion") or "").lower()
        if status in ("queued", "waiting", "pending"):
            return "queued"
        if status == "in_progress":
            return "running"
        if status == "completed":
            if conclusion == "success":
                return "completed"
            if conclusion == "cancelled":
                return "failed"
            if conclusion == "failure" or conclusion == "timed_out":
                return "failed"
            if conclusion == "startup_failure":
                return "failed"
            if conclusion == "skipped":
                return "failed"
            if conclusion == "neutral":
                return "completed"
            return "completed"
        return "running"

    # -------------------------------------------------------------- artifacts
    async def fetch_report(self, run_id: int, task_id: str) -> dict[str, Any]:
        """Download + safely extract this task's report artifact; parse JSON."""
        artifact_name = f"{self._artifact_name_prefix}{task_id}"
        resp = await self._request("GET", f"/repos/{self._repo}/actions/runs/{run_id}/artifacts")
        artifacts = (resp.json() or {}).get("artifacts") or []
        matching = [a for a in artifacts if a.get("name") == artifact_name]
        if not matching:
            raise GitHubClientError(f"artifact {artifact_name!r} not found on run {run_id}")
        art = matching[0]
        if art.get("expired"):
            raise ArtifactExpiredError(f"artifact {artifact_name!r} has expired")
        if art.get("workflow_run", {}).get("id") not in (None, run_id) and art.get(
            "run_id"
        ) not in (None, run_id):
            raise GitHubClientError("artifact does not belong to the expected run")

        zip_resp = await self._request(
            "GET", f"/repos/{self._repo}/actions/artifacts/{art['id']}/zip"
        )
        content = zip_resp.content
        if len(content) > MAX_ZIP_BYTES:
            raise GitHubClientError("artifact zip exceeds size policy")
        report_bytes = extract_report_from_zip(content, expected_names={"report.json"})
        try:
            import json as _json

            return _json.loads(report_bytes.decode("utf-8"))
        except Exception as exc:
            raise GitHubClientError(f"report.json is not valid JSON: {exc}") from exc


def extract_report_from_zip(content: bytes, *, expected_names: set[str]) -> bytes:
    """Safe ZIP extraction: one expected member, no traversal, size caps."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(content))
    except zipfile.BadZipFile as exc:
        raise GitHubClientError("artifact is not a valid ZIP") from exc

    total = 0
    found: dict[str, bytes] = {}
    for info in zf.infolist():
        name = Path(info.filename).name  # member basename
        path = info.filename.replace("\\", "/")
        if path.startswith("/") or ".." in Path(path).parts or info.is_dir():
            raise GitHubClientError(f"unsafe ZIP member: {info.filename!r}")
        if name not in expected_names:
            continue  # ignore auxiliary files, but never extract them
        if info.file_size > MAX_MEMBER_BYTES:
            raise GitHubClientError("ZIP member exceeds size policy")
        data = zf.read(info)
        total += len(data)
        if total > MAX_ZIP_BYTES:
            raise GitHubClientError("extracted content exceeds size policy")
        found[name] = data
    if "report.json" not in found:
        raise GitHubClientError("report.json missing from artifact")
    return found["report.json"]


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

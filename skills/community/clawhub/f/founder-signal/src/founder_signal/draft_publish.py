"""Draft publish handoff for Founder Signal public run reviews."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

_PUBLIC_RUN_REVIEW_FILENAME = "public-run-review.md"
_PUBLISH_INTENT_FILENAME = "draft-publish-intent.json"


@dataclass(frozen=True)
class DraftPublishIntent:
    path: Path
    public_run_review_path: Path
    visibility: str
    title: str
    requires_confirmation: bool
    public_publish_requires_confirmation: bool

    @property
    def daily_review_path(self) -> Path:
        """Backward-compatible alias for callers that still use the old name."""
        return self.public_run_review_path


@dataclass(frozen=True)
class DraftReviewPublishResult:
    url: str
    page_id: str
    stdout: str
    stderr: str
    execution_log: list[dict[str, Any]]


def write_public_draft_publish_intent(
    *,
    run_dir: Path,
    profile_id: str,
) -> DraftPublishIntent:
    """Write the Draft review-page intent consumed by the draft-cli skill.

    The intent authorizes a downstream agent to create, append, and publish the Draft
    public page for the generated public run review. Any later public web publication
    outside Draft remains a separate confirmation-gated boundary.
    """
    public_run_review_path = run_dir / _PUBLIC_RUN_REVIEW_FILENAME
    if not public_run_review_path.exists():
        raise FileNotFoundError(f"Public run review not found: {public_run_review_path}")
    title = _derive_page_title(public_run_review_path=public_run_review_path, profile_id=profile_id)
    intent_path = run_dir / _PUBLISH_INTENT_FILENAME
    payload = {
        "intent": "publish_markdown_to_draft_public_page",
        "artifact_type": "founder_signal_public_run_review",
        "visibility": "draft_public_preview",
        "profile_id": profile_id,
        "title": title,
        "public_run_review_path": str(public_run_review_path),
        "daily_review_path": str(public_run_review_path),
        "draft_cli_skill": "toliuweijing/draft-cli",
        "requires_confirmation": False,
        "auto_publish_on_every_run": True,
        "auto_publish_on_success": True,
        "draft_public_publish_requires_confirmation": False,
        "external_public_publish_requires_confirmation": True,
        "operator_instruction": (
            "After every Founder Signal run, including failure reports when possible, use the "
            "draft CLI supplied by the required draft-cli skill installed in the agent "
            "workspace to create a Draft page, append public-run-review.md, publish the page, "
            "and return the resulting public Draft URL without asking for additional "
            "approval. Ask for explicit confirmation only before any later public web "
            "publication outside the Draft review surface."
        ),
        "status": "public_publish_requested",
    }
    intent_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return DraftPublishIntent(
        path=intent_path,
        public_run_review_path=public_run_review_path,
        visibility="draft_public_preview",
        title=title,
        requires_confirmation=False,
        public_publish_requires_confirmation=False,
    )


def publish_daily_review_to_draft(
    *,
    intent: DraftPublishIntent,
    workspace_root: Path,
    runner: Callable[[list[str], Path], subprocess.CompletedProcess[str]] | None = None,
) -> DraftReviewPublishResult:
    """Create, append, and publicly publish the generated public run review in Draft."""
    effective_runner = runner or _run_command
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    execution_log: list[dict[str, Any]] = []

    status = _run_json_command(
        ["draft", "status", "--json"],
        cwd=workspace_root,
        runner=effective_runner,
        stdout_parts=stdout_parts,
        stderr_parts=stderr_parts,
        execution_log=execution_log,
        allow_failure=True,
    )
    if str(status.get("state") or "").strip() == "DAEMON_OFFLINE":
        _run_json_command(
            ["draft", "start-server", "--mode", "workspace", "--workspace", str(workspace_root)],
            cwd=workspace_root,
            runner=effective_runner,
            stdout_parts=stdout_parts,
            stderr_parts=stderr_parts,
            execution_log=execution_log,
            allow_failure=False,
        )
        status = _run_json_command(
            ["draft", "status", "--json"],
            cwd=workspace_root,
            runner=effective_runner,
            stdout_parts=stdout_parts,
            stderr_parts=stderr_parts,
            execution_log=execution_log,
            allow_failure=True,
        )
    if str(status.get("state") or "").strip() == "BROWSER_NOT_CONNECTED":
        _run_json_command(
            ["draft", "daemon"],
            cwd=workspace_root,
            runner=effective_runner,
            stdout_parts=stdout_parts,
            stderr_parts=stderr_parts,
            execution_log=execution_log,
            allow_failure=False,
        )

    create_payload = _run_json_command(
        ["draft", "page", "create", intent.title, "--json"],
        cwd=workspace_root,
        runner=effective_runner,
        stdout_parts=stdout_parts,
        stderr_parts=stderr_parts,
        execution_log=execution_log,
        allow_failure=False,
    )
    page_id = _find_first_string(
        create_payload,
        {"page_id", "pageId", "id", "document_id", "documentId"},
    )
    if not page_id:
        raise RuntimeError("Draft CLI did not return a page ID from page create.")

    content = intent.public_run_review_path.read_text(encoding="utf-8")
    _run_json_command(
        ["draft", "page", "append", page_id, content, "--json"],
        cwd=workspace_root,
        runner=effective_runner,
        stdout_parts=stdout_parts,
        stderr_parts=stderr_parts,
        execution_log=execution_log,
        allow_failure=False,
    )

    publish_payload = _run_json_command(
        ["draft", "page", "publish", page_id, "--json"],
        cwd=workspace_root,
        runner=effective_runner,
        stdout_parts=stdout_parts,
        stderr_parts=stderr_parts,
        execution_log=execution_log,
        allow_failure=False,
    )
    url = _find_first_string(
        publish_payload,
        {
            "public_url",
            "publicUrl",
            "preview_url",
            "previewUrl",
            "url",
            "page_url",
            "pageUrl",
            "href",
            "permalink",
        },
    )
    if not url:
        raise RuntimeError("Draft CLI did not return a public Draft page URL.")
    return DraftReviewPublishResult(
        url=url,
        page_id=page_id,
        stdout="\n".join(part for part in stdout_parts if part).strip(),
        stderr="\n".join(part for part in stderr_parts if part).strip(),
        execution_log=execution_log,
    )


def _derive_page_title(*, public_run_review_path: Path, profile_id: str) -> str:
    for line in public_run_review_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading
    return f"Founder Signal Run Review ({profile_id})"


def _run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True, timeout=5)


def _run_json_command(
    command: list[str],
    *,
    cwd: Path,
    runner: Callable[[list[str], Path], subprocess.CompletedProcess[str]],
    stdout_parts: list[str],
    stderr_parts: list[str],
    execution_log: list[dict[str, Any]],
    allow_failure: bool,
) -> dict[str, Any]:
    try:
        result = runner(command, cwd)
    except FileNotFoundError as exc:
        raise RuntimeError("Draft CLI is not installed or not available on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Draft CLI command timed out before returning a result.") from exc
    stdout = str(result.stdout or "").strip()
    stderr = str(result.stderr or "").strip()
    stdout_parts.append(stdout)
    stderr_parts.append(stderr)
    execution_log.append(
        {
            "command": _redacted_command(command),
            "returncode": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }
    )
    if result.returncode != 0 and not allow_failure:
        detail = stderr or stdout or f"exit code {result.returncode}"
        raise RuntimeError(f"Draft CLI command failed: {' '.join(command)}: {detail}")
    if not stdout:
        return {}
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        if result.returncode != 0 and allow_failure:
            return {}
        raise RuntimeError(f"Draft CLI command did not return JSON: {' '.join(command)}") from None
    return payload if isinstance(payload, dict) else {}


def _redacted_command(command: list[str]) -> list[str]:
    if len(command) >= 5 and command[:3] == ["draft", "page", "append"]:
        return command[:4] + ["<public-run-review.md content>"] + command[5:]
    return command


def _find_first_string(value: Any, keys: set[str]) -> str:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys and str(item or "").strip():
                return str(item).strip()
        for item in value.values():
            found = _find_first_string(item, keys)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_first_string(item, keys)
            if found:
                return found
    return ""

#!/usr/bin/env python3
"""Shared harness for the Phase 9B-9D live failure & recovery integration tests.

Phase 9A proved deterministic recovery with fake workers. Phase 9B-9D proves the
same recovery contract against the **real** runtime:

* 9B resume       -- two genuinely separate Python processes, real Codex turns
* 9B regenerate   -- real generation 1 -> AGY ``qa_failed`` -> real generation 2
* 9C interruption -- a real Codex generation killed mid-flight, then recovered
* 9D assembly     -- real upstream assembly failure/recovery, zero Codex calls

This module is test-only infrastructure. It never modifies a frozen production
component (``scripts/codex_image_adapter.py``, ``scripts/kiro_acp_bridge.py``,
``scripts/project_state.py``, ``scripts/assemble_ppt.py``); it only drives them
the way AGY drives them and records what happened.

Hard rules encoded here:

* No API key, no OpenAI Images API. The adapter strips API-key style variables
  from the Codex child environment; nothing here re-adds one.
* Every real Codex invocation is appended to ``codex_invocations.jsonl``
  **immediately before** the call and only when the call is really about to
  happen. A skipped slide leaves no entry, which is exactly how "partial resume
  did not re-generate anything" is proven across process boundaries.
* All writable state lives under ``<repo>/.agy-ppt-integration/``; teardown
  removes it best-effort.
* Process termination is limited to child PIDs / process groups this harness
  created and explicitly tracked. There is no ``killall``, no pattern match on
  the process table, and no way for it to touch another Codex session.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import struct
import subprocess
import sys
import time
import traceback
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

TESTS_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
REPO_ROOT = SKILL_DIR.parents[1]
for _path in (str(TESTS_DIR), str(SCRIPTS_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from codex_image_adapter import (  # noqa: E402
    BACKEND,
    ERROR_BACKEND_UNAVAILABLE,
    ERROR_CODEX_AUTH_UNAVAILABLE,
    ERROR_CODEX_CLI_UNAVAILABLE,
    OP_GENERATE,
    STATUS_COMPLETED,
    CodexImageAdapter,
    ImageRequest,
    OutputPathError,
    resolve_output_path,
    sniff_image,
)
from project_state import (  # noqa: E402
    CONTROLLER,
    PHASE_OUTLINE,
    PHASE_SAMPLE,
    PHASE_SLIDE_GENERATION,
    PHASE_STYLE,
    SLIDE_ASSEMBLED,
    SLIDE_QA_FAILED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    ProjectState,
)

from helpers.recovery_deck import plan_dispatch  # noqa: E402

# ---------------------------------------------------------------------------
# Opt-in flags / locations
# ---------------------------------------------------------------------------
LIVE_ENV_FLAG = "AGY_PPT_LIVE_RECOVERY"
INTERRUPT_ENV_FLAG = "AGY_PPT_LIVE_RECOVERY_INTERRUPT"
LEDGER_ENV_VAR = "AGY_PPT_LIVE_RECOVERY_LEDGER"
TIMEOUT_ENV_VAR = "AGY_PPT_LIVE_RECOVERY_TIMEOUT"
INTERRUPT_WAIT_ENV_VAR = "AGY_PPT_LIVE_RECOVERY_INTERRUPT_WAIT"
INTERRUPT_DELAY_ENV_VAR = "AGY_PPT_LIVE_RECOVERY_INTERRUPT_DELAY"
ASSEMBLY_PYTHON_ENV_VAR = "AGY_PPT_LIVE_ASSEMBLY_PYTHON"

PROBE_DIR_NAME = ".agy-ppt-integration"
PROBE_ROOT = REPO_ROOT / PROBE_DIR_NAME

LEDGER_FILENAME = "codex_invocations.jsonl"
QA_DECISIONS_FILENAME = "qa_decisions.jsonl"
TRACKED_CHILDREN_FILENAME = "tracked_child_processes.jsonl"

DEFAULT_TIMEOUT_SECONDS = 420.0
DEFAULT_INTERRUPT_WAIT_SECONDS = 90.0
DEFAULT_INTERRUPT_DELAY_SECONDS = 5.0

# Child-role exit codes (a role process is a real, separate Python process).
EXIT_OK = 0
EXIT_FAIL = 1
EXIT_SKIP = 77

SKIP_REASON = (
    f"live failure & recovery scenarios: set {LIVE_ENV_FLAG}=1 (or run the file directly) "
    "with a logged-in Codex/ChatGPT subscription session. These consume subscription quota."
)
INTERRUPT_SKIP_REASON = (
    f"process-interruption scenario: additionally set {INTERRUPT_ENV_FLAG}=1. It starts a real "
    "Codex generation and kills only the child PID / process group it created and tracked."
)

RUNTIME_BLOCKER_ERROR_CODES = frozenset(
    {ERROR_BACKEND_UNAVAILABLE, ERROR_CODEX_CLI_UNAVAILABLE, ERROR_CODEX_AUTH_UNAVAILABLE}
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def live_enabled(module_file: str | os.PathLike[str] | None = None) -> bool:
    """True when live scenarios were explicitly requested."""
    if os.environ.get(LIVE_ENV_FLAG) == "1":
        return True
    if module_file is None:
        return False
    return Path(sys.argv[0]).name == Path(module_file).name


def interrupt_enabled(module_file: str | os.PathLike[str] | None = None) -> bool:
    return live_enabled(module_file) and os.environ.get(INTERRUPT_ENV_FLAG) == "1"


def codex_present() -> bool:
    return shutil.which("codex") is not None


def default_timeout() -> float:
    return _positive_float(os.environ.get(TIMEOUT_ENV_VAR), DEFAULT_TIMEOUT_SECONDS)


def interrupt_wait() -> float:
    return _positive_float(os.environ.get(INTERRUPT_WAIT_ENV_VAR), DEFAULT_INTERRUPT_WAIT_SECONDS)


def interrupt_delay() -> float:
    return _positive_float(os.environ.get(INTERRUPT_DELAY_ENV_VAR), DEFAULT_INTERRUPT_DELAY_SECONDS)


def _positive_float(raw: str | None, default: float) -> float:
    try:
        value = float(raw) if raw not in (None, "") else default
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


class LiveHarnessError(RuntimeError):
    """The harness itself could not set the scenario up (never a Codex fault)."""


class LiveRuntimeBlocker(RuntimeError):
    """A runtime capability blocker (skip), not a coding failure.

    Raised when the built-in ``image_gen`` tool is not exposed, the Codex CLI is
    missing, or the Codex session is not authenticated. Never a reason to fall
    back to a paid API.
    """

    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


# ---------------------------------------------------------------------------
# Workspace layout
# ---------------------------------------------------------------------------
def work_root(scenario: str) -> Path:
    """Every scenario writes only under ``<repo>/.agy-ppt-integration/<scenario>``."""
    return PROBE_ROOT / scenario


def reset_dir(path: Path) -> Path:
    path = Path(path)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)
    return path


KEEP_ARTIFACTS_ENV_VAR = "AGY_PPT_LIVE_RECOVERY_KEEP"


def cleanup(path: Path) -> None:
    """Best-effort teardown: remove the scenario dir, then the probe dir if empty.

    Set ``AGY_PPT_LIVE_RECOVERY_KEEP=1`` to keep the artifacts for debugging.
    """
    path = Path(path)
    if os.environ.get(KEEP_ARTIFACTS_ENV_VAR) == "1":
        print(f"keeping live recovery artifacts: {path}", file=sys.stderr)
        return
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    try:
        if PROBE_ROOT.is_dir() and not any(PROBE_ROOT.iterdir()):
            PROBE_ROOT.rmdir()
    except OSError:  # pragma: no cover - defensive
        pass


def write_summary(work_dir: Path, role: str, payload: dict[str, Any]) -> Path:
    path = Path(work_dir) / f"summary_{role}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = dict(payload)
    body.setdefault("role", role)
    body.setdefault("pid", os.getpid())
    body.setdefault("ppid", os.getppid())
    body.setdefault("python", sys.executable)
    body.setdefault("at", now_iso())
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def read_summary(work_dir: Path, role: str) -> dict[str, Any]:
    path = Path(work_dir) / f"summary_{role}.json"
    if not path.is_file():
        raise LiveHarnessError(f"role {role!r} wrote no summary at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    """Append one JSON record durably (safe for concurrent, multi-process use)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:  # pragma: no cover - defensive
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


# ---------------------------------------------------------------------------
# Real-Codex invocation ledger
# ---------------------------------------------------------------------------
EVENT_INVOCATION = "codex_invocation"
EVENT_RESULT = "codex_result"


@dataclass
class InvocationLedger:
    """Append-only, cross-process record of **real** Codex invocations.

    An ``codex_invocation`` line is written immediately before a Codex render
    turn is started, and only then: nothing is recorded for a slide that resume
    skipped, for a scenario that never reaches Codex (9D), or for a request the
    harness rejected before spending a turn. The matching ``codex_result`` line
    is appended after the turn returns, so API-fallback usage is auditable too.
    """

    path: Path
    scenario: str = ""

    @classmethod
    def for_scenario(cls, scenario: str, work_dir: Path) -> "InvocationLedger":
        override = os.environ.get(LEDGER_ENV_VAR)
        path = Path(override) if override else Path(work_dir) / LEDGER_FILENAME
        return cls(path=path, scenario=scenario)

    # -- writing -----------------------------------------------------------
    def record_invocation(
        self,
        *,
        slide_id: str,
        generation: int,
        operation: str,
        role: str,
    ) -> str:
        invocation_id = f"{self.scenario}:{slide_id}:gen{generation}:{os.getpid()}:{time.time_ns()}"
        append_jsonl(
            self.path,
            {
                "event": EVENT_INVOCATION,
                "invocation_id": invocation_id,
                "scenario": self.scenario,
                "slide_id": slide_id,
                "generation": int(generation),
                "operation": operation,
                "role": role,
                "pid": os.getpid(),
                "backend": BACKEND,
                "at": now_iso(),
            },
        )
        return invocation_id

    def record_result(self, invocation_id: str, result: dict[str, Any]) -> None:
        diagnostics = result.get("diagnostics") if isinstance(result.get("diagnostics"), dict) else {}
        append_jsonl(
            self.path,
            {
                "event": EVENT_RESULT,
                "invocation_id": invocation_id,
                "scenario": self.scenario,
                "slide_id": result.get("slide_id"),
                "operation": result.get("operation"),
                "status": result.get("status"),
                "error_code": result.get("error_code"),
                "backend": result.get("backend"),
                "api_fallback_used": bool(diagnostics.get("api_fallback_used")),
                "pid": os.getpid(),
                "at": now_iso(),
            },
        )

    # -- reading -----------------------------------------------------------
    def events(self) -> list[dict[str, Any]]:
        return read_jsonl(self.path)

    def invocations(self, scenario: str | None = "") -> list[dict[str, Any]]:
        return self._filter(EVENT_INVOCATION, scenario)

    def results(self, scenario: str | None = "") -> list[dict[str, Any]]:
        return self._filter(EVENT_RESULT, scenario)

    def _filter(self, event: str, scenario: str | None) -> list[dict[str, Any]]:
        wanted = self.scenario if scenario == "" else scenario
        return [
            record
            for record in self.events()
            if record.get("event") == event
            and (wanted is None or record.get("scenario") == wanted)
        ]

    def total(self, scenario: str | None = "") -> int:
        return len(self.invocations(scenario))

    def count_for(self, slide_id: str, scenario: str | None = "") -> int:
        return sum(1 for r in self.invocations(scenario) if r.get("slide_id") == slide_id)

    def generations_for(self, slide_id: str, scenario: str | None = "") -> list[int]:
        return [
            int(r.get("generation") or 0)
            for r in self.invocations(scenario)
            if r.get("slide_id") == slide_id
        ]

    def roles_for(self, slide_id: str, scenario: str | None = "") -> list[str]:
        return [
            str(r.get("role") or "")
            for r in self.invocations(scenario)
            if r.get("slide_id") == slide_id
        ]

    def slides_for_role(self, role: str, scenario: str | None = "") -> list[str]:
        return [
            str(r.get("slide_id") or "")
            for r in self.invocations(scenario)
            if r.get("role") == role
        ]

    def duplicate_count(self, scenario: str | None = "") -> int:
        """Invocations beyond the first for the same slide + generation.

        A regeneration is generation 2, so it is never counted as a duplicate;
        re-running work that was already done for the same generation is.
        """
        seen: dict[tuple[str, str, int], int] = {}
        for record in self.invocations(scenario):
            key = (
                str(record.get("scenario") or ""),
                str(record.get("slide_id") or ""),
                int(record.get("generation") or 0),
            )
            seen[key] = seen.get(key, 0) + 1
        return sum(count - 1 for count in seen.values() if count > 1)

    def api_fallback_count(self, scenario: str | None = "") -> int:
        return sum(1 for r in self.results(scenario) if r.get("api_fallback_used") is True)


# ---------------------------------------------------------------------------
# Test images (9D uses these instead of a Codex turn)
# ---------------------------------------------------------------------------
def png_bytes(width: int = 640, height: int = 360, rgb: tuple[int, int, int] = (238, 238, 238)) -> bytes:
    """A real, minimal RGB PNG. Accepted by ``sniff_image`` and by python-pptx."""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    row = b"\x00" + bytes(rgb) * width
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(row * height, 9))
        + chunk(b"IEND", b"")
    )


def write_test_png(path: Path, *, width: int = 640, height: int = 360, shade: int = 238) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes(width, height, (shade, shade, shade)))
    return path


def is_readable_image(path: Path) -> bool:
    """Readable raster image, using the production adapter's own sniffer."""
    path = Path(path)
    if not path.is_file() or path.stat().st_size <= 0:
        return False
    return sniff_image(path) is not None


# ---------------------------------------------------------------------------
# Project setup / AGY decisions
# ---------------------------------------------------------------------------
def slide_prompt(marker: str) -> str:
    """A deliberately cheap, throwaway slide prompt for live tests."""
    return (
        "Use case: productivity-visual\n"
        "Asset type: throwaway recovery-test slide image\n"
        "Primary request: a plain 16:9 slide with a light background and the exact text "
        f"'{marker}' centered in large dark sans-serif letters\n"
        f'Text (verbatim): "{marker}"\n'
        "Composition/framing: 16:9 landscape, centered text, generous margins\n"
        "Constraints: no other text, no logos, no watermark\n"
    )


def new_project(
    workspace: Path,
    project_id: str,
    slide_ids: Sequence[str],
    *,
    phase: str = PHASE_SLIDE_GENERATION,
) -> ProjectState:
    """Initialize a disposable project and drive it to ``phase`` as AGY would."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    state = ProjectState.initialize(workspace, project_id, slide_ids=list(slide_ids))
    state.save()
    for gate in ("outline", "style", "sample"):
        state.set_gate(gate, "approved")
    for step in (PHASE_OUTLINE, PHASE_STYLE, PHASE_SAMPLE, PHASE_SLIDE_GENERATION):
        state.set_phase(step)
        if step == phase:
            break
    state.save()
    return state


def resume_plan(state: ProjectState) -> list[str]:
    """Slides a resume may dispatch (settled slides are never included)."""
    return plan_dispatch(state)


def qa_pass(state: ProjectState, slide_id: str, *, reason: str | None = None) -> None:
    """AGY-only visual-QA judgement: generated -> qa_passed."""
    state.set_slide_status(slide_id, SLIDE_QA_PASSED, by=CONTROLLER, note=reason)
    state.save()
    _record_qa_decision(state, slide_id, SLIDE_QA_PASSED, reason)


def qa_fail(state: ProjectState, slide_id: str, *, reason: str) -> None:
    """AGY-only visual-QA judgement: generated -> qa_failed, with a fixed reason."""
    state.set_slide_status(slide_id, SLIDE_QA_FAILED, by=CONTROLLER, note=reason)
    state.save()
    _record_qa_decision(state, slide_id, SLIDE_QA_FAILED, reason)


def _record_qa_decision(
    state: ProjectState, slide_id: str, verdict: str, reason: str | None
) -> None:
    """Keep the test controller's QA rationale beside the state, not inside it.

    ``project_state.py`` is frozen and deliberately stores no QA prose, so the
    harness records its own decision log instead of adding fields to the
    production schema.
    """
    append_jsonl(
        Path(state.workspace_root) / QA_DECISIONS_FILENAME,
        {
            "slide_id": slide_id,
            "verdict": verdict,
            "reason": reason,
            "decided_by": CONTROLLER,
            "generation": int(state.slide(slide_id).get("generation") or 0),
            "pid": os.getpid(),
            "at": now_iso(),
        },
    )


def qa_decisions(workspace: Path) -> list[dict[str, Any]]:
    return read_jsonl(Path(workspace) / QA_DECISIONS_FILENAME)


def mark_assembled(state: ProjectState, slide_ids: Iterable[str]) -> None:
    for slide_id in slide_ids:
        state.set_slide_status(slide_id, SLIDE_ASSEMBLED)
    state.save()


# ---------------------------------------------------------------------------
# One real Codex render turn
# ---------------------------------------------------------------------------
def live_generate(
    state: ProjectState,
    ledger: InvocationLedger,
    slide_id: str,
    *,
    marker: str,
    role: str,
    operation: str = OP_GENERATE,
    timeout: float | None = None,
    output_dir: str = "origin_image",
    record_result: bool = True,
) -> dict[str, Any]:
    """Dispatch exactly one real Codex image turn for ``slide_id``.

    Order of operations matters and mirrors production:

    1. ``ready`` -> ``generating`` is persisted **before** the call, so a crash
       leaves ``generating`` on disk (that is what 9C recovers from).
    2. The output path is validated before a turn is spent.
    3. The invocation is appended to ``codex_invocations.jsonl`` immediately
       before the real Codex call.
    4. The result is recorded into the project state by AGY. The visual-QA
       judgement is *not* made here.
    """
    workspace = Path(state.workspace_root)
    rel_output = f"{output_dir}/{slide_id}.png"
    if state.slide(slide_id)["status"] != SLIDE_READY:
        state.set_slide_status(slide_id, SLIDE_READY)
    generation = state.begin_generation(slide_id, job_path=f"prompts/{slide_id}.json")
    state.save()

    # Validate before recording an invocation: a rejected request never reaches
    # Codex, so it must never appear in the ledger.
    try:
        resolve_output_path(str(workspace), rel_output, operation)
    except OutputPathError as exc:
        raise LiveHarnessError(f"unsafe output path for {slide_id}: {exc}") from exc

    request = ImageRequest.from_dict(
        {
            "slide_id": slide_id,
            "operation": operation,
            "prompt": slide_prompt(marker),
            "output_path": rel_output,
            "aspect_ratio": "16:9",
            "workspace_root": str(workspace),
            "timeout_seconds": timeout or default_timeout(),
        }
    )

    invocation_id = ledger.record_invocation(
        slide_id=slide_id, generation=generation, operation=operation, role=role
    )
    result = CodexImageAdapter(request).run().to_dict()
    ledger.record_result(invocation_id, result)

    error_code = result.get("error_code")
    if error_code in RUNTIME_BLOCKER_ERROR_CODES:
        raise LiveRuntimeBlocker(
            str(error_code),
            f"{slide_id}: {error_code} -- runtime capability blocker, not a coding failure "
            "(no paid API fallback was attempted)",
        )
    assert_no_api_fallback(result)
    if result.get("status") != STATUS_COMPLETED:
        raise LiveHarnessError(
            f"{slide_id} live {operation} failed: {result.get('error_code')} "
            f"{result.get('error_message', '')}".strip()
        )
    if result.get("backend") != BACKEND:
        raise LiveHarnessError(f"{slide_id} used unexpected backend {result.get('backend')!r}")

    if record_result:
        state.record_worker_result(slide_id, result)
        state.save()
    return result


def assert_no_api_fallback(result: dict[str, Any]) -> None:
    diagnostics = result.get("diagnostics") if isinstance(result.get("diagnostics"), dict) else {}
    if diagnostics.get("api_fallback_used") is True:
        raise LiveHarnessError("codex result reports api_fallback_used=true (forbidden)")


# ---------------------------------------------------------------------------
# Role child processes (real, separate Python processes)
# ---------------------------------------------------------------------------
def role_argv(
    module_file: str | os.PathLike[str],
    role: str,
    *,
    workspace: Path,
    work_dir: Path,
    extra: Sequence[str] = (),
) -> list[str]:
    return [
        sys.executable,
        str(Path(module_file).resolve()),
        "--role",
        role,
        "--workspace",
        str(Path(workspace)),
        "--work-dir",
        str(Path(work_dir)),
        *extra,
    ]


def role_env(ledger: InvocationLedger) -> dict[str, str]:
    """Child environment: opt-in flags + shared ledger, never a credential."""
    env = dict(os.environ)
    env[LIVE_ENV_FLAG] = "1"
    env[LEDGER_ENV_VAR] = str(ledger.path)
    env["PYTHONUNBUFFERED"] = "1"
    return env


def run_role(
    module_file: str | os.PathLike[str],
    role: str,
    *,
    workspace: Path,
    work_dir: Path,
    ledger: InvocationLedger,
    extra: Sequence[str] = (),
    timeout: float | None = None,
) -> subprocess.CompletedProcess:
    """Run one role to completion in its own Python process."""
    return subprocess.run(  # noqa: S603 - argv is built from this harness only
        role_argv(module_file, role, workspace=workspace, work_dir=work_dir, extra=extra),
        cwd=str(REPO_ROOT),
        env=role_env(ledger),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def start_role(
    module_file: str | os.PathLike[str],
    role: str,
    *,
    workspace: Path,
    work_dir: Path,
    ledger: InvocationLedger,
    extra: Sequence[str] = (),
) -> subprocess.Popen:
    """Start a role in its own process **group** so it can be killed precisely."""
    return subprocess.Popen(  # noqa: S603 - argv is built from this harness only
        role_argv(module_file, role, workspace=workspace, work_dir=work_dir, extra=extra),
        cwd=str(REPO_ROOT),
        env=role_env(ledger),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )


def role_main(func: Callable[[], int]) -> int:
    """Run a role body, mapping runtime blockers to the skip exit code."""
    try:
        return func()
    except LiveRuntimeBlocker as exc:
        print(f"SKIP: {exc}", file=sys.stderr)
        return EXIT_SKIP
    except BaseException:  # noqa: BLE001 - a role must never leak a traceback-less failure
        traceback.print_exc()
        return EXIT_FAIL


def role_parser(description: str):
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--role", help="internal: run one child role instead of the test suite")
    parser.add_argument("--workspace", help="project workspace root (role mode)")
    parser.add_argument("--work-dir", dest="work_dir", help="scenario work dir (role mode)")
    return parser


def child_failure_detail(result: subprocess.CompletedProcess) -> str:
    return (
        f"exit={result.returncode}\n"
        f"--- stdout ---\n{(result.stdout or '').strip()[-4000:]}\n"
        f"--- stderr ---\n{(result.stderr or '').strip()[-4000:]}"
    )


# ---------------------------------------------------------------------------
# Precise, tracked child-process termination (9C only)
# ---------------------------------------------------------------------------
@dataclass
class TrackedProcess:
    pid: int
    pgid: int | None
    argv0: str
    tracker_pid: int

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "TrackedProcess":
        pgid = record.get("pgid")
        return cls(
            pid=int(record.get("pid") or 0),
            pgid=int(pgid) if isinstance(pgid, int) else None,
            argv0=str(record.get("argv0") or ""),
            tracker_pid=int(record.get("tracker_pid") or 0),
        )


def install_child_tracker(path: Path) -> None:
    """Record every process this Python process spawns (observation only).

    Used inside the 9C generating role so the parent knows the exact PID and
    process group of the Codex process **this test created**. It changes no
    adapter behaviour: it only writes down what was started.
    """
    real_popen = subprocess.Popen
    tracker_path = Path(path)

    class TrackingPopen(real_popen):  # type: ignore[misc, valid-type]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            argv = args[0] if args else kwargs.get("args")
            argv0 = ""
            if isinstance(argv, (list, tuple)) and argv:
                argv0 = str(argv[0])
            elif isinstance(argv, str):
                argv0 = argv
            try:
                pgid: int | None = os.getpgid(self.pid)
            except OSError:  # pragma: no cover - defensive
                pgid = None
            append_jsonl(
                tracker_path,
                {
                    "pid": int(self.pid),
                    "pgid": pgid,
                    "argv0": argv0,
                    "argv0_name": Path(argv0).name if argv0 else "",
                    "tracker_pid": os.getpid(),
                    "at": now_iso(),
                },
            )

    subprocess.Popen = TrackingPopen  # type: ignore[assignment]


def wait_for_tracked(path: Path, name: str, timeout: float) -> TrackedProcess | None:
    """Wait until the tracker file records a child whose argv0 is ``name``."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        matches = tracked_processes(path, name=name)
        if matches:
            return matches[0]
        time.sleep(0.5)
    return None


def tracked_processes(path: Path, name: str | None = None) -> list[TrackedProcess]:
    """Every child process this harness explicitly recorded (optionally by name)."""
    found: list[TrackedProcess] = []
    for record in read_jsonl(path):
        if name is not None and Path(str(record.get("argv0") or "")).name != name:
            continue
        tracked = TrackedProcess.from_record(record)
        if tracked.pid > 1:
            found.append(tracked)
    return found


def pid_alive(pid: int) -> bool:
    if pid <= 1:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:  # pragma: no cover - alive but not ours
        return True
    return True


def pgid_alive(pgid: int | None) -> bool:
    if not pgid or pgid <= 1:
        return False
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:  # pragma: no cover - alive but not ours
        return True
    return True


def terminate_tracked(
    child: subprocess.Popen,
    tracked: Iterable[TrackedProcess],
    *,
    grace: float = 15.0,
) -> dict[str, Any]:
    """Kill only this test's own child process and its tracked grandchildren.

    Safety rules (there is deliberately no process-name search and no
    ``killall``):

    * the Python role process is addressed by the exact PID we started;
    * a grandchild is killed only if this harness recorded its PID **and**
      process group id while starting it;
    * the harness never signals its own process group, pid <= 1, or a process
      group it did not record.
    """
    own_pgid = os.getpgid(0)
    killed_pids: list[int] = []
    killed_pgids: list[int] = []
    refused: list[dict[str, Any]] = []

    # 1. The role process first, so it cannot record a result after the fact.
    if child.poll() is None and child.pid > 1:
        _kill_pid(child.pid, signal.SIGKILL)
        killed_pids.append(child.pid)

    # 2. Then the tracked grandchildren (the real Codex process group).
    for entry in tracked:
        if entry.pid <= 1:
            refused.append({"pid": entry.pid, "reason": "invalid pid"})
            continue
        pgid = entry.pgid
        if pgid and pgid > 1 and pgid != own_pgid and pgid == entry.pid:
            # The adapter starts codex with start_new_session=True, so a tracked
            # codex process leads its own group: killing that group cannot reach
            # anything we did not create.
            _kill_pgid(pgid, signal.SIGKILL)
            killed_pgids.append(pgid)
        elif pgid == own_pgid:
            refused.append({"pid": entry.pid, "reason": "would signal our own process group"})
        else:
            refused.append({"pid": entry.pid, "reason": f"pgid {pgid!r} not a tracked group leader"})
        _kill_pid(entry.pid, signal.SIGKILL)
        killed_pids.append(entry.pid)

    try:
        child.wait(timeout=grace)
    except subprocess.TimeoutExpired:  # pragma: no cover - defensive
        pass

    deadline = time.monotonic() + grace
    while time.monotonic() < deadline:
        if not any(pgid_alive(pgid) for pgid in killed_pgids) and not any(
            pid_alive(pid) for pid in killed_pids
        ):
            break
        time.sleep(0.3)

    return {
        "killed_pids": killed_pids,
        "killed_process_groups": killed_pgids,
        "refused": refused,
        "child_returncode": child.returncode,
        "survivors": [pid for pid in killed_pids if pid_alive(pid)],
    }


def _kill_pid(pid: int, sig: int) -> None:
    if pid <= 1:
        return
    try:
        os.kill(pid, sig)
    except (ProcessLookupError, PermissionError, OSError):
        pass


def _kill_pgid(pgid: int, sig: int) -> None:
    if pgid <= 1 or pgid == os.getpgid(0):
        return
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError, OSError):
        pass


# ---------------------------------------------------------------------------
# Upstream assembly (9D)
# ---------------------------------------------------------------------------
ASSEMBLY_SCRIPT = SCRIPTS_DIR / "assemble_ppt.py"


def _can_import_pptx(python: str) -> bool:
    try:
        probe = subprocess.run(  # noqa: S603 - fixed argv
            [python, "-c", "import pptx"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return probe.returncode == 0


def assembly_python() -> str | None:
    """Pick an interpreter that can run the upstream assembly script.

    Nothing is installed here: the runtime venv created by
    ``codex_ppt_runtime.py bootstrap`` is used when it exists, otherwise the
    current interpreter. Returns ``None`` when no interpreter has
    ``python-pptx``, which is a capability blocker (skip), not a failure.
    """
    runtime_home = Path(
        os.path.expanduser(os.environ.get("CODEX_PPT_HOME", "~/.codex-ppt-skill"))
    )
    candidates = [
        os.environ.get(ASSEMBLY_PYTHON_ENV_VAR),
        str(runtime_home / ".venv" / "bin" / "python"),
        str(REPO_ROOT / ".venv" / "bin" / "python"),
        sys.executable,
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if candidate != sys.executable and not Path(candidate).exists():
            continue
        if _can_import_pptx(candidate):
            return candidate
    return None


def run_assembly(
    python: str,
    base_dir: Path,
    output_name: str,
    *,
    aspect_ratio: str = "16:9",
    timeout: float = 600.0,
) -> subprocess.CompletedProcess:
    """Run the real upstream assembly script exactly once.

    Only ``scripts/assemble_ppt.py`` is executed; the command can never be a
    Codex invocation, and no image is (re)generated by it.
    """
    argv = [
        python,
        str(ASSEMBLY_SCRIPT),
        str(base_dir),
        output_name,
        "--aspect-ratio",
        aspect_ratio,
    ]
    return subprocess.run(  # noqa: S603 - fixed argv from this harness
        argv,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def is_pptx(path: Path) -> bool:
    """A real OOXML package starts with a ZIP local file header."""
    path = Path(path)
    if not path.is_file() or path.stat().st_size <= 0:
        return False
    with path.open("rb") as handle:
        return handle.read(2) == b"PK"


def find_pptx(root: Path) -> list[Path]:
    root = Path(root)
    return sorted(p for p in root.rglob("*.pptx") if p.is_file())

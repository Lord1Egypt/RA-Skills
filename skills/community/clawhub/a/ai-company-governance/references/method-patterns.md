# Method Patterns — Shared Code Templates & Prompt Frameworks

> This file is the **single source of truth** for all shared code templates and
> prompt frameworks in this skill package. Any other file that needs a template
> must link to the anchors in this file — **inline code copies are forbidden**.
>
> Authority: this package's `README-FOR-AI.md` — §7 (templates & frameworks), §8 (Harness), §9.2–9.4 (compliance), §6.3 (source-language standard).

---

## 1. Template Index

Selection table only. Read the first two sections to choose a template; descend
into Section 3 only when you need the implementation.

| # | Function | Purpose | Safety Property | Harness | Anchor |
|---|----------|---------|-----------------|---------|--------|
| 1 | `validate_input_schema(data, schema)` | Validate input against a schema before any LLM call | No external I/O; pure validation | L2 | [3.1](#31-validate_input_schema) |
| 2 | `sanitize_user_query(query)` | Sanitize raw user input before prompt or command use | No dynamic code execution; injection-neutralizing | L3 | [3.2](#32-sanitize_user_query) |
| 3 | `execute_safe_command(cmd, timeout=30)` | Sandboxed subprocess execution | Hard timeout + restricted cwd; shell disabled | L4 | [3.3](#33-execute_safe_command) |
| 4 | `format_output_json(content, provider)` | Standard JSON output envelope with AIGC labeling | Embedded AI watermark + metadata + timestamp | L5 | [3.4](#34-format_output_json) |
| 5 | `retry_with_backoff(func, max_retries=3)` | Exponential-backoff retry wrapper | Fault tolerance; never swallows the final error | L3 | [3.5](#35-retry_with_backoff) |
| 6 | `read_reference_file(filepath)` | Safely read a reference file | Path validation; out-of-bounds paths rejected | L3 | [3.6](#36-read_reference_file) |
| 7 | `generate_trace_id(prefix="trace")` | Generate audit trace identifiers | Stateless; no I/O; thread-safe | L5 | [3.7](#37-generate_trace_id) |
| 8 | `check_rate_limit(identifier, limit=10, window=60)` | Sliding-window rate limiting | In-memory only; never persisted to disk | L4 | [3.8](#38-check_rate_limit) |
| 9 | `mask_sensitive_data(text)` | PII masking (EMAIL / IP / PHONE) | Raw data never logged or persisted | L5 | [3.9](#39-mask_sensitive_data) |
| 10 | `build_prompt_from_template(template, **kwargs)` | Render prompt framework templates | All inputs sanitized before insertion | L3 | [3.10](#310-build_prompt_from_template) |

Harness mapping (README-FOR-AI.md §8.1): every LLM call point must have validation in
front, sanitization behind, tracing throughout, and a fallback on failure.
Signatures below are **frozen** — parameter names and defaults must not change;
test assertions depend on them. A renamed function breaks every referencing
file and requires a package-wide grep.

---

## 2. Prompt Framework Index

| Framework | Fields | Best For | Anchor |
|-----------|--------|----------|--------|
| CRISPE | 6 | Complex, multi-step tasks needing explicit constraints and examples | [4.1](#41-crispe) |
| 3WEH | 4 | Clear delegation: unambiguous role, task, purpose, format | [4.2](#42-3weh) |
| Five-Element | 5 | Enterprise-compliant prompts with explicit context and constraints | [4.3](#43-five-element) |

Rules (README-FOR-AI.md §7.2): the **full field-by-field expansion lives only in Section 4
of this file**. `SKILL.md` may only name the framework and link here; it must
never inline the field expansion. Use `build_prompt_from_template` (3.10) to
render any of these frameworks.

---

## 3. Shared Code Templates

The ten templates below are the physical implementation of the harness
(README-FOR-AI.md §8.1). Order matches the index table and must not be rearranged.
All templates share this module preamble:

```python
"""Shared harness templates — single source of truth for this skill package.

All paths are resolved from environment variables or the current working
directory. Never hardcode absolute paths in sources; always use the
{SKILL_DIR} and {WORKSPACE_ROOT} placeholders instead.
"""

import hashlib
import json
import os
import random
import re
import shlex
import subprocess
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from threading import Lock

# --- Sandboxing roots (configure via environment; placeholders in docs) ---
# {SKILL_DIR}       -> root of this skill package (read-only for the skill)
# {WORKSPACE_ROOT}  -> the user's writable workspace directory (the only writable area)
SKILL_ROOT = os.environ.get("SKILL_DIR", ".")
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", ".")

# --- Reference-file policy (template 6) ---
MAX_REFERENCE_FILE_BYTES = 1 * 1024 * 1024  # 1 MiB read cap
ALLOWED_REFERENCE_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}

# --- Query sanitization policy (template 2) ---
MAX_QUERY_LENGTH = 2000
```

### 3.1 validate_input_schema

```python
def validate_input_schema(data, schema):
    """Validate ``data`` against ``schema`` before any LLM call (Harness L2).

    ``schema`` maps each field name to a spec dict::

        schema = {
            "task": {"type": str, "required": True},
            "priority": {"type": int, "required": False},
        }

    Pure validation only: no external I/O, no dynamic code execution, no
    network access. Raises ``ValueError`` with a field-level message on the
    first violation; returns True when the data conforms.
    """
    if not isinstance(data, dict):
        raise ValueError("input data must be a dict")
    if not isinstance(schema, dict):
        raise ValueError("schema must be a dict")

    for field, spec in schema.items():
        if not isinstance(spec, dict):
            raise ValueError(f"schema spec for '{field}' must be a dict")
        value = data.get(field)
        if value is None:
            if spec.get("required", True):
                raise ValueError(f"missing required field: {field}")
            continue
        expected = spec.get("type")
        if expected is None:
            continue
        # bool is a subclass of int in Python; reject the implicit coercion
        if isinstance(value, bool) and expected in (int, float):
            raise ValueError(
                f"field '{field}' expected {expected.__name__}, got bool"
            )
        if not isinstance(value, expected):
            raise ValueError(
                f"field '{field}' expected {expected.__name__}, "
                f"got {type(value).__name__}"
            )
    return True
```

### 3.2 sanitize_user_query

```python
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u2028\u2029\u2060\ufeff]")
_INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(prior|previous)\s+(instructions|prompts)", re.IGNORECASE),
    re.compile(r"reveal\s+(your\s+)?(system\s+)?prompt", re.IGNORECASE),
    re.compile(r"<\|[^|]*\|>"),
)
_SHELL_METACHARS = re.compile(r"[`$;&|><\"']")

def sanitize_user_query(query):
    """Sanitize raw user input before it reaches a prompt or a command (Harness L3).

    - Strips control characters and zero-width/invisible characters.
    - Neutralizes common prompt-injection phrases by replacing them with a
      fixed marker (no dynamic code execution; this function never calls
      eval/exec).
    - Removes shell metacharacters so downstream command builders cannot be
      hijacked by user-supplied text.
    - Truncates to MAX_QUERY_LENGTH characters.

    Returns the sanitized string. Raises TypeError on non-string input.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    cleaned = _CONTROL_CHARS.sub("", query)
    cleaned = _ZERO_WIDTH.sub("", cleaned)
    for pattern in _INJECTION_PATTERNS:
        cleaned = pattern.sub("[FILTERED]", cleaned)
    cleaned = _SHELL_METACHARS.sub("", cleaned)
    return cleaned[:MAX_QUERY_LENGTH]
```

### 3.3 execute_safe_command

```python
_BLOCKED_EXECUTABLES = frozenset({
    "rm", "del", "rmdir", "rd", "format", "mkfs", "shutdown", "reboot",
    "sudo", "su", "chmod", "chown", "reg", "regedit", "cmd", "powershell",
    "pwsh", "iex", "curl", "wget",
})
_MAX_TIMEOUT_SECONDS = 120

def _scrubbed_environment():
    """Return an environment copy with secret-like variables removed.

    Implements the zero-hardcoded-secrets baseline (README-FOR-AI.md §9.4): credentials
    never travel into a subprocess environment implicitly.
    """
    blocked_prefixes = ("api_", "token", "secret", "password", "key_")
    return {
        name: value
        for name, value in os.environ.items()
        if not name.lower().startswith(blocked_prefixes)
    }

def execute_safe_command(cmd, timeout=30):
    """Run a command in a sandbox with a hard timeout (Harness L4).

    Security contract:
    - The subprocess runs with ``shell=False`` (no shell interpolation of
      user-controlled text) and a restricted cwd: {WORKSPACE_ROOT} only.
    - Dangerous executables (deletion, shell hosts, downloaders, privilege
      escalation) are rejected before launch.
    - ``timeout`` is clamped to (0, 120] seconds; a hung process is killed
      and surfaced as TimeoutError.
    - The child environment is scrubbed of secret-like variables.

    ``cmd`` may be a string (parsed with shlex, never via a shell) or an
    argument list. Returns a dict with returncode, stdout, stderr.
    """
    if isinstance(cmd, str):
        parts = shlex.split(cmd)
    elif isinstance(cmd, (list, tuple)):
        parts = [str(part) for part in cmd]
    else:
        raise TypeError("cmd must be a string or a list of arguments")
    if not parts:
        raise ValueError("empty command")
    if not isinstance(timeout, (int, float)) or not 0 < timeout <= _MAX_TIMEOUT_SECONDS:
        raise ValueError(f"timeout must be in (0, {_MAX_TIMEOUT_SECONDS}] seconds")

    executable = os.path.basename(parts[0]).lower()
    if executable.endswith(".exe"):
        executable = executable[:-4]
    if executable in _BLOCKED_EXECUTABLES:
        raise PermissionError(f"blocked executable: {executable}")

    try:
        completed = subprocess.run(
            parts,
            cwd=WORKSPACE_ROOT,          # restricted cwd ({WORKSPACE_ROOT})
            timeout=timeout,             # hard timeout: hung processes die
            capture_output=True,
            text=True,
            shell=False,                 # never allow shell interpolation
            env=_scrubbed_environment(),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"command exceeded {timeout}s timeout: {executable}") from exc
    except FileNotFoundError as exc:
        raise ValueError(f"executable not found: {parts[0]}") from exc

    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
```

### 3.4 format_output_json

```python
AIGC_DISCLOSURE = "AI-Generated Content"

def format_output_json(content, provider):
    """Wrap content in the standard JSON envelope with AIGC labeling (Harness L5).

    Implements the triple-labeling requirement (README-FOR-AI.md §9.2); omitting any
    layer makes the output non-compliant:
    - Layer 1, explicit label: a visible disclosure line is appended to the
      content body.
    - Layer 2, implicit metadata: ``ai_generated``, ``generated_at``
      (ISO-8601 UTC), and ``model`` ("<provider/model>") fields.
    - Layer 3, embedded watermark: a SHA-256-derived marker derived from the
      provider and generation timestamp is embedded inside the content body,
      so it cannot be removed without removing the payload text around it.

    ``content`` must already have passed through mask_sensitive_data (3.9).
    Returns a JSON string (UTF-8 safe, indent=2).
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(provider, str) or not provider.strip():
        raise ValueError("provider must be a non-empty string")

    generated_at = datetime.now(timezone.utc).isoformat()
    watermark = hashlib.sha256(
        f"{provider}:{generated_at}:{AIGC_DISCLOSURE}".encode("utf-8")
    ).hexdigest()[:16]

    watermarked_content = (
        f"{content}\n\n"
        f"> Warning: {AIGC_DISCLOSURE} [aigc:{watermark}]"
    )
    payload = {
        "content": watermarked_content,
        "ai_generated": True,
        "generated_at": generated_at,
        "model": f"{provider}/default",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
```

### 3.5 retry_with_backoff

```python
def retry_with_backoff(func, max_retries=3):
    """Execute ``func`` with exponential backoff on failure (Harness L3).

    Calls ``func()`` up to ``max_retries + 1`` times total. The delay before
    retry N (0-based) is ``0.5 * 2**N`` seconds with +/-25% jitter to avoid
    thundering-herd synchronization.

    Fault-tolerance contract: the final exception is re-raised unchanged —
    this wrapper never silently swallows errors. Callers whose operations are
    non-idempotent must not retry (README-FOR-AI.md §8.3).

    Returns whatever ``func`` returns on success.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(max_retries, int) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer")

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001 - deliberate broad retry
            last_error = exc
            if attempt == max_retries:
                break
            delay = 0.5 * (2 ** attempt)
            time.sleep(delay * (0.75 + random.random() * 0.5))
    raise last_error
```

### 3.6 read_reference_file

```python
def read_reference_file(filepath):
    """Read a reference file after strict path validation (Harness L3).

    Security contract:
    - The requested path is resolved against {SKILL_DIR} and its real path
      is verified to stay inside that root; traversal (``..``), absolute-path
      escapes, and symlink escapes are rejected with PermissionError.
    - Only allowlisted text extensions (.md/.txt/.json/.yaml/.yml) may be
      read; binaries and scripts are refused.
    - Files larger than MAX_REFERENCE_FILE_BYTES (1 MiB) are refused, so a
      runaway reference cannot exhaust the context budget.

    Returns the file content as a UTF-8 string.
    """
    if not isinstance(filepath, str) or not filepath.strip():
        raise ValueError("filepath must be a non-empty string")

    root = os.path.realpath(SKILL_ROOT)
    candidate = os.path.join(root, filepath)
    target = os.path.realpath(candidate)

    if target != root and not target.startswith(root + os.sep):
        raise PermissionError(
            f"path escapes the allowed root {{SKILL_DIR}}: {filepath}"
        )
    extension = os.path.splitext(target)[1].lower()
    if extension not in ALLOWED_REFERENCE_EXTENSIONS:
        raise ValueError(f"file extension not allowed: {extension or '<none>'}")
    if not os.path.isfile(target):
        raise FileNotFoundError(f"reference file not found: {filepath}")
    if os.path.getsize(target) > MAX_REFERENCE_FILE_BYTES:
        raise ValueError(
            f"reference file exceeds {MAX_REFERENCE_FILE_BYTES} byte read cap"
        )

    with open(target, "r", encoding="utf-8") as handle:
        return handle.read()
```

### 3.7 generate_trace_id

```python
def generate_trace_id(prefix="trace"):
    """Generate a unique, sortable audit-trace identifier (Harness L5).

    Format: ``{prefix}-{unix_millis}-{uuid4_hex12}``. Pure computation:
    stateless, no I/O, no global mutable state — safe to call from any
    thread or process. The identifier is designed to be threaded through
    every stage of a task (README-FOR-AI.md §8.1) so failures can be localized.

    Raises ValueError for a prefix that is empty or outside
    [A-Za-z0-9_-]{1,32}.
    """
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", prefix):
        raise ValueError("prefix must be 1-32 characters of [A-Za-z0-9_-]")
    unix_millis = int(time.time() * 1000)
    return f"{prefix}-{unix_millis}-{uuid.uuid4().hex[:12]}"
```

### 3.8 check_rate_limit

```python
_rate_buckets = defaultdict(deque)
_rate_lock = Lock()

def check_rate_limit(identifier, limit=10, window=60):
    """Sliding-window rate limiter, held in process memory only (Harness L4).

    Tracks the last ``limit`` request timestamps per ``identifier`` inside a
    ``window``-second sliding window. In-memory by design (README-FOR-AI.md §8.3): a
    persisted counter file would become a concurrency contention point and
    leave stale residue — nothing here is ever written to disk.

    Thread-safe via a module-level lock. Returns True when the request is
    allowed (and records it), False when the limit is exhausted.
    """
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("identifier must be a non-empty string")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")
    if not isinstance(window, (int, float)) or window <= 0:
        raise ValueError("window must be a positive number")

    now = time.monotonic()
    with _rate_lock:
        bucket = _rate_buckets[identifier]
        while bucket and bucket[0] <= now - window:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True
```

### 3.9 mask_sensitive_data

```python
def mask_sensitive_data(text):
    """Mask sensitive information in output (emails, IPs, phone numbers)."""
    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Mask IP addresses
    text = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[IP]', text)
    # Mask phone numbers (11-digit)
    text = re.sub(r'\b[0-9]{11}\b', '[PHONE]', text)
    return text
```

The three placeholders `[EMAIL]` / `[IP]` / `[PHONE]` are contractual: all
three masking branches must exist. An implementation that masks only emails
and IPs will pass review by eye but fail the `test_phone_masking` assertion —
this exact defect shipped once and was only caught by audit (README-FOR-AI.md §7.1 warning).
Raw, unmasked PII must never be logged or persisted (README-FOR-AI.md §9.3).

### 3.10 build_prompt_from_template

```python
class _StrictDict(dict):
    """format_map mapping that fails loudly on unknown placeholders."""

    def __missing__(self, key):
        raise KeyError(f"template references unknown placeholder: {{{key}}}")

def build_prompt_from_template(template, **kwargs):
    """Render a prompt template with sanitized values (Harness L3).

    Contract (README-FOR-AI.md §7.1, template 10): **inputs are sanitized first**. Every
    substitution value passes through ``sanitize_user_query`` (3.2) and
    ``mask_sensitive_data`` (3.9) before insertion into the template, so
    prompt injection and PII can never ride in through a placeholder value.

    Unknown placeholders raise ``KeyError`` immediately instead of silently
    producing a half-rendered prompt. Use with the Section 4 frameworks, e.g.::

        build_prompt_from_template(
            "Who: {role}\nWhat: {task}\nWhy: {purpose}\nHow: {how}",
            role="data analyst", task="summarize Q3 revenue",
            purpose="weekly exec briefing", how="markdown, <=5 bullets",
        )

    Returns the fully rendered prompt string.
    """
    if not isinstance(template, str) or not template.strip():
        raise ValueError("template must be a non-empty string")

    sanitized = {}
    for key, value in kwargs.items():
        cleaned = sanitize_user_query(str(value))
        cleaned = mask_sensitive_data(cleaned)
        sanitized[key] = cleaned

    try:
        return template.format_map(_StrictDict(sanitized))
    except KeyError:
        raise
    except (IndexError, ValueError) as exc:
        raise ValueError(f"malformed template: {exc}") from exc
```

---

## 4. Prompt Frameworks (Full)

Field-by-field expansion. These expansions live **only** here (README-FOR-AI.md §7.2);
other files may name a framework and link to this section, never inline it.
Render any skeleton with `build_prompt_from_template` (Section 3.10).

### 4.1 CRISPE

Six fields, for complex multi-step tasks that need explicit constraints and
an example to anchor output shape.

| Field | Placeholder | Guidance |
|-------|-------------|----------|
| Role | `{role_description}` | Who the model is: expertise, seniority, perspective. Be specific ("senior tax auditor specializing in VAT compliance"), never generic ("helpful assistant"). |
| Result | `{desired_output}` | The concrete deliverable, stated as an artifact: a table, a patched file, a JSON object. Ambiguity here is the top cause of drift. |
| Input | `{input_data}` | The exact data the model operates on. Values rendered via `build_prompt_from_template` are auto-sanitized and PII-masked. |
| Steps | `{step_by_step}` | Ordered procedure the model must follow. Number the steps so deviations are detectable in review. |
| Parameters | `{constraints}` | Hard bounds: length caps, forbidden content, format rules, tone. Constraints must be verifiable, not aspirational. |
| Example | `{example}` | One representative input/output pair. The example is the strongest format signal; keep it minimal but complete. |

Skeleton (render with `build_prompt_from_template`):

```python
CRISPE_TEMPLATE = (
    "[Role] {role_description}\n"
    "[Result] {desired_output}\n"
    "[Input] {input_data}\n"
    "[Steps] {step_by_step}\n"
    "[Parameters] {constraints}\n"
    "[Example] {example}"
)
```

### 4.2 3WEH

Four fields, for clear delegation where the risk is misreading intent rather
than task complexity.

| Field | Placeholder | Guidance |
|-------|-------------|----------|
| Who | `{role}` | The acting role. One sentence, includes the domain ("release manager on call"). |
| What | `{task}` | The single action to perform, expressed as a verb + object. One task per prompt; split anything larger. |
| Why | `{purpose}` | The business reason. Enables the model to make correct judgment calls on unspecified details. |
| How | `{format_constraints}` | Output format and bounds: structure, length, language, units. Must be objectively checkable. |

Skeleton (render with `build_prompt_from_template`):

```python
THREE_WEH_TEMPLATE = (
    "Who: {role}\n"
    "What: {task}\n"
    "Why: {purpose}\n"
    "How: {format_constraints}"
)
```

### 4.3 Five-Element

Five fields, the enterprise-compliant default when output is auditable or
faces external review.

| Field | Placeholder | Guidance |
|-------|-------------|----------|
| Role | `{role}` | Acting role with domain and authority level, same rules as 3WEH Who. |
| Task | `{task}` | The action, verb + object. One task per prompt. |
| Context | `{context}` | Background facts the model cannot infer: environment, prior decisions, upstream data. Facts only — no instructions smuggled inside context. |
| Format | `{output_format}` | The exact output schema (JSON shape, table columns, file layout). Pair with `validate_input_schema` when output must round-trip. |
| Constraint | `{constraints}` | Compliance bounds: policy references, forbidden disclosures, mandatory AIGC labeling, PII masking requirements. |

Skeleton (render with `build_prompt_from_template`):

```python
FIVE_ELEMENT_TEMPLATE = (
    "Role: {role}\n"
    "Task: {task}\n"
    "Context: {context}\n"
    "Format: {output_format}\n"
    "Constraint: {constraints}"
)
```

---

## 5. Compliance Verification

Verification procedures for the three non-negotiable compliance areas
(README-FOR-AI.md §9.2–9.4). A declared Harness level without verifiable evidence in
this file violates P24 (documenting unimplemented behavior, README-FOR-AI.md §8.2).

### 5.1 AIGC Triple Labeling (README-FOR-AI.md §9.2)

All AI-generated content must carry **all three** layers; missing any one
layer is non-compliant.

| # | Layer | Carrier | Implemented By | Verification |
|---|-------|---------|----------------|--------------|
| 1 | Explicit label | Visible content body | `format_output_json` disclosure line | Rendered output contains the disclosure sentence |
| 2 | Implicit metadata | Structured output envelope | `format_output_json` payload fields | JSON has `ai_generated: true`, ISO-8601 `generated_at`, `model` |
| 3 | Embedded watermark | Content body itself | `format_output_json` SHA-256 marker | Deleting the marker requires deleting payload text |

Verification procedure: parse the envelope with `json.loads`, assert the three
metadata fields, and confirm the watermark marker string appears inside the
`content` value. Layer 3 must survive copy-paste of the content body.

### 5.2 PII Masking (README-FOR-AI.md §9.3)

- `mask_sensitive_data` (3.9) is **mandatory in every output pipeline** —
  before any persistence, logging, or external sending.
- All three classes must be masked: **EMAIL / IP / PHONE**. A missing class
  is a defect (P32); see the warning under 3.9.
- Masking order is fixed: mask **first**, then persist/log/send. Raw data
  must never appear in logs.
- Verification: feed a fixture containing an email, an IPv4 address, and an
  11-digit phone number through `mask_sensitive_data`; the result must
  contain `[EMAIL]`, `[IP]`, and `[PHONE]` respectively and none of the
  originals.

### 5.3 Audit Trail (README-FOR-AI.md §8.1, §8.2)

- Every task carries a `generate_trace_id` (3.7) identifier from start to
  finish; without it, failures cannot be localized.
- Logs record the trace id, the operation name, timestamps, and outcome —
  never raw PII (5.2 applies to log lines too).
- Trace ids are stateless and derived from wall-clock plus randomness; they
  are safe to generate concurrently and require no coordination.
- Verification: a task's log entries all share one trace id; no log line
  matches the PII regexes of `mask_sensitive_data`.

### 5.4 Safety Baseline (README-FOR-AI.md §9.4)

Non-negotiable, verified against this file's templates:

- **Zero dynamic code execution** — no `eval`/`exec` on user input, no
  `Invoke-Expression`/`iex`/`DownloadString` anywhere. Template 2 sanitizes
  by regex substitution only; template 3 runs `shell=False` subprocesses.
- **Zero hardcoded secrets** — credentials come from environment variables;
  configuration records variable *names*, never values. Template 3 actively
  scrubs secret-like variables from child environments.
- **Zero sensitive-path access** — template 6 rejects any path resolving
  outside `{SKILL_DIR}`.
- **Zero self-rewrite** — the skill never writes into `{SKILL_DIR}`;
  writable output goes only under `{WORKSPACE_ROOT}`.
- **Idempotency** — operations are safe to retry; `retry_with_backoff`
  re-raises the final error and `check_rate_limit` keeps no persistent
  state (README-FOR-AI.md §8.3).
- **Rollback safety** — copy to a temp location, verify, atomically replace,
  and only then delete the old copy; never delete first and restore later
  (P23).

---

## 6. Constraints

Forbidden in and around this file:

- **No inline code copies.** Any file needing a template links to the
  Section 3 anchor. A second `def` of any function in this package is the
  recurrence signal of defect P10 (README-FOR-AI.md §7.3, B4/B5).
- **No signature changes.** Parameter names and defaults of the ten
  templates are frozen; test assertions depend on them.
- **No reordering.** Section 3.1–3.10 order matches the index table #1–#10.
- **No department copies.** Department D3 `method-patterns.md` files may
  contain only department-specific templates — never these ten shared ones.
- **No bare code fences.** Every fenced block is ```` ```python ````;
  untagged fences and `py` tags are rejected (R3-4).
- **No hardcoded absolute paths.** Use `{SKILL_DIR}` / `{WORKSPACE_ROOT}`
  placeholders in prose and environment variables in code.
- **No framework expansion outside Section 4.** `SKILL.md` names frameworks
  and links here only (README-FOR-AI.md §6.2 blacklist, §7.2).
- **No skipped Harness prerequisites.** Levels are cumulative: an L5 claim
  without idempotency evidence is downgraded to L2 and recorded as a defect
  (README-FOR-AI.md §8.1).

---

## 7. Department-Specific Patterns

L/G tiers only; not applicable at micro tier. Department-specific templates
belong in each department's own D3 `references/method-patterns.md`, which
must not duplicate any shared template from this file.

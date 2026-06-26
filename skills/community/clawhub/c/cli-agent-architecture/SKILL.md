# CLI-Agent Architecture Skill

> A single `run(command="...")` tool with Unix CLI commands outperforms typed function calls.

This skill teaches the **two-layer CLI architecture** derived from production lessons at Manus and r/LocalLLaMA research. It is the foundation for building robust, production-ready AI agents that execute shell commands.

---

## 1. Why CLI > Typed Functions

### The LLM-Native Interface

LLMs have seen **billions of Unix CLI examples** in training data. They understand:
- Pipe semantics (`|`, `>`, `>>`)
- Exit codes (`$?`, `||`, `&&`)
- Redirection (`2>&1`, `<`, `<<`)
- Globbing and expansion (`*`, `?`, `[...]`)

Typed function calls are **unfamiliar terrain** — a thin abstraction layer that maps poorly onto concepts LLMs already master.

### One Tool, Not Three

Typed functions for a file operation:
```
read_file(path) → content
analyze(content) → result
write_file(path, result)
```

CLI equivalent:
```
run(command="grep pattern file | jq '.key' > result.json")
```

The pipe chain replaces three function calls with one coherent primitive. LLMs already think in pipelines.

### Unified Namespace

- Typed functions create **context-switching overhead**: switching between "function call mode" and "shell mode"
- CLI provides a **single namespace** for all operations: files, processes, network, services, containers
- No schema drift, no SDK版本 mismatch, no function deprecation

---

## 2. Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AGENT (LLM)                            │
│         Thinks in pipelines. Speaks shell natively.         │
└────────────────────────┬────────────────────────────────────┘
                         │ command="..."
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               LAYER 1 — Unix Execution                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  exec.run(command)  →  (stdout, stderr, exit_code)  │    │
│  └─────────────────────────────────────────────────────┘    │
│  • Pure execution, no abstraction                           │
│  • Lossless — binary stdout passes through unchanged        │
│  • Metadata-free — Layer 2 adds all presentation logic      │
└────────────────────────┬────────────────────────────────────┘
                         │ raw output
                         ▼
┌─────────────────────────────────────────────────────────────┐
│             LAYER 2 — LLM Presentation                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐   │
│  │ Binary   │  │ Overflow │  │ stderr   │  │  Metadata   │   │
│  │ Guard    │  │ Truncator│  │ Attachment│  │   Footer    │   │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘   │
│  Binary → guidance   >200 lines →  • exit:N on failure      │
│  detected  → replaced  temp file     • duration on success  │
└────────────────────────┬────────────────────────────────────┘
                         │ optimized output
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               AGENT (LLM) — receives processed view           │
└─────────────────────────────────────────────────────────────┘
```

### Why Separation Is Logically Necessary

Layer 1 must be **lossless** — it cannot make decisions about what to show the LLM, because it has no context about the task. Layer 2 is the **presentation layer** that adapts raw execution output for LLM consumption.

If Layer 1 filtered or truncated, it would make irreversible decisions without task context. If Layer 2 executed commands, it would mix concerns and lose the clarity of the pipeline.

---

## 3. Four Layer 2 Mechanisms

### 3A. Binary Guard

**Problem:** Binary data (images, PDFs, executables) blinds the LLM. A terminal full of PNG header bytes is meaningless and wastes context.

**Detection:** Read the first 8KB of stdout. If >30% non-printable bytes (outside 0x20-0x7E, 0x09, 0x0A, 0x0D), treat as binary.

**Replacement message format:**
```
[Binary file detected — 182KB PNG image]
Use: see <temp_path>
Or:  file <path>
```

**Script:** `scripts/binary_guard.py`

### 3B. Overflow Mode

**Problem:** Large outputs (>200 lines) cause attention collapse. The LLM loses the signal in the noise.

**Truncation strategy:**
1. Show first 50 lines (context anchor)
2. Write full output to temp file
3. Replace middle with: `[... N lines truncated. Full output: /tmp/out_abc123 ...]`
4. Show last 20 lines (recent context)

**Threshold:** 200 lines (configurable). Below threshold, pass through unchanged.

**Script:** `scripts/truncator.py`

### 3C. Metadata Footer

**Purpose:** Always tell the LLM the exit code and execution duration.

**On success:**
```
[exit:0 | 1.23s]
```

**On failure (combined with stderr attachment):**
```
[exit:127 | 0.45s]
```

The LLM uses this to decide retry, different command, or escalation — without needing to parse raw output.

### 3D. stderr Attachment

**Problem:** Silent `stderr` causes blind retries. The LLM sees exit code != 0 but has no clue what went wrong.

**Rule:** Never suppress stderr. On failure, always attach it.

**Format:**
```
--- stderr ---
/bin/grep: file: No such file or directory
--- end stderr ---
```

**On success:** stderr is discarded unless it contains warnings the LLM should know about (configurable).

**Script:** `scripts/stderr_capture.py`

---

## 4. Error Message Design

Every error message must have two parts:

1. **What went wrong** — concrete, specific
2. **What to do instead** — actionable next step

### Examples

| Command | Error | Good Message |
|---------|-------|--------------|
| `cat photo.png` | binary content | `[error] binary image (182KB PNG). Use: see photo.png` |
| `grep foo huge.log` | no match | `[error] no matches found in huge.log (0 results). Pattern: foo` |
| `rm -rf /` | permission denied | `[error] permission denied (exit:1). Do not run: rm -rf /. Use: rm file` |
| `nc -z host 443` | connection refused | `[error] connection refused to host:443. Check: is the service running?` |

### Anti-patterns

❌ `"error occurred"` — vague  
❌ `"command failed"` — no clue what went wrong  
❌ `"try again"` — no diagnostic info  
❌ `"file not found"` — no suggestion on what to try

---

## 5. Progressive Disclosure

Don't dump all documentation at once. Reveal on demand.

### Level 0 — Always Injected (Start of Session)

```
Available commands (one-line summaries):
  run     — Execute shell command, returns stdout/stderr/exit
  see     — Render binary file (image/video/audio) inline
  search  — Full-text search across files
  read    — Read file contents (text only)
  write   — Write text to file
  list    — List directory contents
```

### Level 1 — On-Demand Usage (no args or --help)

```
$ run
Usage: run <command>
Executes a shell command and returns processed output.
  --timeout=N   Max execution time in seconds (default: 60)
  --env=KEY=VAL Inject environment variable
```

### Level 2 — Parameter Drilling (explicit request)

Full parameter documentation, examples, edge cases, and security notes.

---

## 6. Implementation Guide

### Directory Structure

```
cli-agent-architecture/
├── SKILL.md
├── scripts/
│   ├── binary_guard.py
│   ├── truncator.py
│   └── stderr_capture.py
└── examples/
    └── two_layer_execution.py   # reference implementation
```

### Binary Detection (`binary_guard.py`)

```python
#!/usr/bin/env python3
"""Detect binary data in byte stream. Returns (is_binary, guidance_message)."""
import sys
import os
import stat

def detect_binary_stream(data: bytes, path: str = None) -> tuple[bool, str]:
    """Return (True, guidance) if data appears binary."""
    # Fast path: check file mode if path provided
    if path and os.path.exists(path):
        mode = os.stat(path).st_mode
        if stat.S_ISBLK(mode) or stat.S_ISCHR(mode) or stat.S_ISFIFO(mode):
            return True, f"[Binary device/fifo detected: {path}]"

    if not data:
        return False, ""

    # Sample first 8KB
    sample = data[:8192]
    non_printable = sum(
        1 for b in sample
        if b not in (9, 10, 13) and (b < 32 or b > 126)
    )

    ratio = non_printable / len(sample) if sample else 0

    if ratio > 0.30:
        # Try to identify type
        size = len(data)
        hint = ""
        if path:
            import mimetypes
            mime, _ = mimetypes.guess_type(path)
            if mime:
                hint = f" ({mime})"

        return True, f"[Binary file detected — {size} bytes{hint}]\nUse: see {path or '<tempfile>'}\nOr:  file {path or '<file>'}"

    return False, ""


if __name__ == "__main__":
    data = sys.stdin.buffer.read()
    is_bin, msg = detect_binary_stream(data)
    if is_bin:
        print(msg, file=sys.stderr)
        sys.exit(1)
```

### Overflow Truncation (`truncator.py`)

```python
#!/usr/bin/env python3
"""Truncate large output, write full content to temp file."""
import sys
import os
import tempfile

MAX_LINES = 200
SHOW_HEAD = 50
SHOW_TAIL = 20

def truncate_output(stdout: str, stderr: str = "") -> tuple[str, str | None]:
    """
    If stdout > MAX_LINES, truncate and write to temp file.
    Returns (processed_stdout, temp_file_path or None).
    """
    lines = stdout.splitlines()
    temp_path = None

    if len(lines) <= MAX_LINES:
        return stdout, None

    head = "\n".join(lines[:SHOW_HEAD])
    tail = "\n".join(lines[-SHOW_TAIL:])
    truncated_mid = f"[... {len(lines) - SHOW_HEAD - SHOW_TAIL} lines truncated ...]"

    # Write full output to temp file
    fd, temp_path = tempfile.mkstemp(prefix="cli_out_", suffix=".txt")
    try:
        os.write(fd, stdout.encode("utf-8", errors="replace"))
    finally:
        os.close(fd)

    return f"{head}\n{truncated_mid}\n{tail}", temp_path


if __name__ == "__main__":
    output = sys.stdin.read()
    truncated, path = truncate_output(output)
    print(truncated)
    if path:
        print(f"\n[Full output written to: {path}]", file=sys.stderr)
```

### stderr Capture (`stderr_capture.py`)

```python
#!/usr/bin/env python3
"""Capture and format stderr on command failure."""
import sys

def format_stderr_attachment(stderr: str, command: str = "") -> str:
    """Format stderr for display when a command fails."""
    if not stderr or not stderr.strip():
        return ""

    lines = stderr.strip().splitlines()
    # Limit to 30 lines to avoid flooding context
    if len(lines) > 30:
        lines = lines[:30] + ["[... additional stderr truncated ...]"]

    header = "--- stderr ---"
    if command:
        header += f" (command: {command})"
    footer = "--- end stderr ---"

    return "\n".join([header] + lines + [footer])


if __name__ == "__main__":
    stderr = sys.stdin.read()
    formatted = format_stderr_attachment(stderr)
    if formatted:
        print(formatted, file=sys.stderr)
```

---

## 7. When CLI Breaks Down

### Strongly-Typed Interactions

GraphQL APIs, complex DB queries with typed schemas, gRPC with protobuf — CLI's string-based interface loses type safety. Use typed function calls here, or build a thin CLI wrapper that validates types before passing to the underlying system.

### High-Security / Injection-Risk Environments

- SQL/shell injection risk with unsanitized user input
- Environments where arbitrary command execution is prohibited
- Audited systems where all actions must be logged and approved

In these cases, typed functions with explicit allowlists are preferable to unrestricted CLI access.

### Native Multimodal (Audio/Video Processing)

When the task is **transcoding**, **audio analysis**, or **video editing**, CLI tools exist but the LLM cannot "see" the output. For these tasks, typed functions that call domain-specific APIs (FFmpeg wrappers, audio analysis libraries) outperform raw CLI.

---

## 8. Business Application

### AI Agent Production Readiness Audit

Help companies assess whether their AI agent infrastructure is production-ready.

**Audit Scope ($500–$2,000):**

| Area | Checks |
|------|--------|
| Binary handling | Does the agent crash on binary output? |
| stderr visibility | Are errors opaque or diagnostic? |
| Output truncation | Does large output cause context overflow? |
| Error messages | Are they actionable? |
| Progressive disclosure | Is help available without overwhelming? |

**Deliverable:** Written report with findings, severity ratings, and recommendations.

**Implementation ($2,000–$5,000):**

- Implement the two-layer architecture
- Deploy binary guard, overflow truncation, stderr attachment
- Tune thresholds for the client's workload
- Train team on progressive disclosure patterns

**Pitch:**

> "Your agent works in demos. Does it work at 3am with a 500MB log file and a cryptic 'command failed' error? I audit the gap between 'it works' and 'it's production-ready' — and close it."

---

## Reference: Complete Two-Layer Execution Flow

```
1. Agent decides: run("grep -r 'ERROR' /var/log/app/*.log | tail -50")
2. Layer 1 exec:  stdout, stderr, exit_code = exec.run("grep ...")
3. Layer 2 processing:
   a. Binary guard  → if binary: replace with guidance
   b. Overflow mode → if >200 lines: truncate + temp file
   c. stderr attach → if exit != 0: include stderr
   d. metadata footer → attach [exit:N | duration]
4. Processed output → Agent
5. Agent interprets and decides next action
```

---

## See Also

- `scripts/binary_guard.py` — binary detection implementation
- `scripts/truncator.py` — overflow truncation implementation
- `scripts/stderr_capture.py` — stderr formatting on failure

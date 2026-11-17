# Failure Forensics

> A structured post-mortem analysis skill for AI agents. When a task fails, don't just retry — investigate.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What It Does

**Failure Forensics** is a skill for AI agent frameworks (Hermes Agent, OpenClaw, and compatible). When an agent task fails, instead of blindly retrying, the agent performs a four-phase structured root cause analysis:

1. **Triage** — Categorize the failure (network, permissions, logic, environment, dependency, resource)
2. **Timeline Reconstruction** — Parse tool-call logs to build a chronological failure timeline
3. **Causal Chain Analysis** — Trace the decision chain backward to the root cause
4. **Post-Mortem Report** — Generate a structured report and save lessons learned

## Why

Retrying a failed task without understanding why it failed is a gamble. You might:
- Hit the same failure again (wasted effort)
- Mask the real cause with incidental changes (harder to debug later)
- Miss a systemic issue that will recur in different forms

Failure Forensics turns each failure into a reusable lesson, building institutional memory that makes the agent more reliable over time.

## Repository Structure

```
failure-forensics/
├── SKILL.md                          # Main skill definition (YAML frontmatter + workflow)
├── README.md                         # This file
├── LICENSE                           # MIT
├── references/
│   ├── failure-taxonomy.md           # Six-category failure taxonomy with signatures
│   └── post-mortem-template.md       # Fill-in-the-blanks report template
└── scripts/
    └── failure_forensics.py          # Log parser, categorizer, report generator
```

## Quick Start

### As a Hermes Agent Skill

Copy or symlink this directory to your skills folder:

```bash
cp -r failure-forensics/ ~/.hermes/skills/
```

The skill auto-loads. When a task fails, the agent will follow the forensics workflow described in `SKILL.md`.

### Standalone (Script Only)

The Python script works independently — no agent required:

```bash
# Analyze a JSONL log of tool calls
python3 scripts/failure_forensics.py analyze --log session.jsonl --output timeline.md

# Categorize an error message
python3 scripts/failure_forensics.py categorize --error "ConnectionRefusedError: Connection refused"

# Generate a pre-filled post-mortem report
python3 scripts/failure_forensics.py report --log session.jsonl --title "Deploy failure"
```

### Log Format

The analyzer reads JSON or JSONL files where each entry represents a tool call:

```json
{
  "timestamp": "2024-01-15T10:23:45Z",
  "tool": "terminal",
  "args": {"command": "npm install"},
  "result": {"success": false, "error": "EACCES: permission denied"},
  "duration_ms": 1200
}
```

See `scripts/sample_log.jsonl` for a working example.

## Failure Taxonomy (Summary)

| Category | Signature | Example |
|---|---|---|
| **Network** | Connection refused, timeout, DNS, TLS | `curl: (7) Failed to connect` |
| **Permissions** | 401/403, EACCES, unauthorized | `PermissionError: [Errno 13]` |
| **Logic** | Wrong output, assertion failure | `AssertionError: expected 200, got 404` |
| **Environment** | Missing binary, wrong version, missing env | `command not found: docker` |
| **Dependency** | ImportError, version conflict | `ModuleNotFoundError: No module named 'foo'` |
| **Resource** | OOM, disk full, rate limit | `OSError: [Errno 28] No space left` |

Full details in [`references/failure-taxonomy.md`](references/failure-taxonomy.md).

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)

## License

MIT — see [LICENSE](LICENSE).

## Author

**Denis Voronin** — [voronindenis5@gmail.com](mailto:voronindenis5@gmail.com)

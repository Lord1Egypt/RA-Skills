# Agent OS — Interface Contract v0.1.1

> Last updated: 2026-06-01
> This documents the public API surface. Internal implementation details may change; these interfaces are the contract.

## File Protocol

### Root Directory

```
<project-root>/.agent-os/
```

All Agent OS data lives here. No other directories are required or assumed.

### File Types & Schemas

| File | Format | Purpose | v0.1.1 Status |
|------|--------|---------|---------------|
| `findings.jsonl` | JSONL | Audit finding registry with status lifecycle | Script: `upsert_finding.py` |
| `experience-log.jsonl` | JSONL | Promoted learnings (rule/test/gate/prompt/doc) | Template only (v0.2.0 script) |
| `context-packs/YYYY-MM-DD-<label>.md` | Markdown | Task-scoped context summary for agent handoff | Script: `compile_context_pack.py` |
| `mission-control/YYYY-MM-DD.md` | Markdown | One-page project health view | Script: `mission_control.py` |
| `flight-recorder/YYYY-MM-DD.jsonl` | JSONL | Agent run records (inputs/decisions/changes/verify) | Template only (v0.2.0 script) |

### Finding Schema (`findings.jsonl`)

```json
{
  "id": "AF-YYYYMMDD-NNN",
  "date": "YYYY-MM-DD",
  "source": "string — daily-audit | code-review | manual",
  "repo": "string — repository or project identifier",
  "severity": "P0 | P1 | P2 | P3",
  "status": "open | accepted | fixed | verified | closed | deferred | false_positive",
  "title": "string — concise",
  "owner": "string — agent or human",
  "evidence": ["string — file paths, URLs"],
  "next_action": "string",
  "verification": "string",
  "tags": ["string"],
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

Status lifecycle: `open → accepted → fixed → verified → closed` (alt: `deferred`, `false_positive`)

## CLI Interface

### `upsert_finding.py`

```bash
python scripts/upsert_finding.py [--project-root PATH] [--dry-run] {create,update,list} [args...]
```

| Command | Required Args | Optional Args |
|---------|--------------|---------------|
| `create` | `--title`, `--severity` | `--status`, `--source`, `--repo`, `--owner`, `--evidence`, `--next-action`, `--verification`, `--tags`, `--date` |
| `update` | `--id`, `--status` | `--owner`, `--next-action`, `--verification`, `--tags` |
| `list` | (none) | `--status`, `--severity`, `--repo`, `--owner` |

### `compile_context_pack.py`

```bash
python scripts/compile_context_pack.py [--project-root PATH] [--dry-run] \
  --task TASK [--label LABEL] [--goal GOAL] \
  [--must-read PATH] [--forbidden TEXT] [--expected-output TEXT]
```

### `mission_control.py`

```bash
python scripts/mission_control.py [--project-root PATH] [--dry-run] [--date YYYY-MM-DD]
```

## Agent Onboarding Contract

New agents MUST:

1. Read latest context pack: `.agent-os/context-packs/`
2. Query open findings: `.agent-os/findings.jsonl` where `status = open`
3. Read latest mission control: `.agent-os/mission-control/`
4. After work: update findings or append flight record

## Expansion Path (v0.2.0)

| Feature | Current (v0.1.x) | v0.2.0 Plan |
|---------|-----------------|-------------|
| `record flight` | Template in `references/templates.md` | `scripts/record_flight.py` |
| `compress decisions` | Workflow in `references/workflows.md` | `scripts/compress_decisions.py` |
| `promote learning` | Workflow in `references/workflows.md` | `scripts/promote_learning.py` |
| Multi-project support | Not supported | `--project-root` auto-detection from git root |
| MCP interface | Not started | `agent-os-mcp` for tool-call-based queries |

## Similar Projects to Learn From

| Project | Relevance | What to Learn |
|---------|-----------|---------------|
| OpenAI Agents SDK Handoffs | Agent-to-agent handoff protocol | Built-in handoff primitives, guardrails pattern |
| Microsoft Agent Framework (MAF) | Multi-agent production framework | Production-grade orchestration, .NET patterns |
| Anthropic MCP (Model Context Protocol) | Tool-use protocol | Standardized tool registration pattern |
| Kimi WebBridge | Agent browser integration | "One curl to install" pattern |
| Upstash Context7 / AgentMail | Agent-accessible services | API design for agent consumers |

## Backward Compatibility Promise

- **v0.1.x**: File protocol schemas are STABLE. New fields may be added but existing fields won't be removed or renamed.
- **v0.2.0**: May introduce new file types but won't break existing schemas.
- **v1.0.0**: Full schema freeze. Breaking changes require MAJOR version bump.

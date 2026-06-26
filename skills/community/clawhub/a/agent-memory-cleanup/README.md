# Agent Memory Cleanup

Agent Memory Cleanup audits and cleans long-term user memory files for agents such as OpenClaw, Hermes Agent, Codex, Claude, and other assistant runtimes.

The skill keeps memory files focused on stable, global user context. It removes or flags stale task notes, completed project details, duplicated preferences, transient debugging logs, and suspected secrets.

## When To Use

Use this skill when:

- A user asks to clean, prune, sanitize, deduplicate, or review `user.md`, `memory.md`, or similar files.
- An agent cannot write memory because the memory file is too long.
- Memory storage reports full, over budget, truncated, or rejected.
- Global user memory has been polluted by task-level details.
- Duplicate or conflicting memories are accumulating.

## Safety Model

The default behavior is conservative:

- Audit automatically when memory pressure is detected.
- Recommend cleanup without waiting.
- Do not require the user to name or invoke this skill explicitly.
- Ask before writing unless the user already authorized automatic cleanup.
- Create timestamped backups before edits.
- Redact suspected secrets in reports.

For proactive cleanup, use two-step consent: first ask whether to inspect and propose cleanup, then ask again before applying edits.

## Files

- `SKILL.md` - Skill instructions.
- `scripts/audit_memory.py` - Deterministic Python audit/proposal/apply engine.
- `scripts/run_tests.py` - Local regression tests.
- `references/default-rules.json` - Thresholds, filename patterns, regex rules, and canonical rewrites.
- `references/classification-rubric.md` - Human-readable rubric for ambiguous cases or non-Python fallback.
- `references/agent-paths.md` - Agent-specific memory path guidance.
- `references/mcp-version.md` - Guidance for wrapping the skill as an MCP server.
- `evals/evals.json` - Regression prompts.
- `test-fixtures/` - Sample noisy and expected memory files.

## Architecture

The skill is intentionally Python-first:

- `SKILL.md` handles trigger conditions, user consent, safety boundaries, and when to call the script.
- `audit_memory.py` handles deterministic behavior so different agents and models get consistent results.
- `default-rules.json` keeps thresholds and regex rules configurable without editing the engine.

This keeps agent context smaller and reduces variation between Codex, OpenClaw, Hermes Agent, Claude, and other runtimes.

## Script Usage

Audit a memory file:

```bash
python scripts/audit_memory.py path/to/memory.md
```

Generate a proposed diff:

```bash
python scripts/audit_memory.py path/to/memory.md --mode propose-patch --include-diff
```

Write a proposed cleaned file without changing the source:

```bash
python scripts/audit_memory.py path/to/memory.md --write-proposed cleaned-memory.md
```

Apply approved cleanup:

```bash
python scripts/audit_memory.py path/to/memory.md --mode apply-approved
```

Machine-readable summaries:

```bash
python scripts/audit_memory.py path/to/memory.md --summary-json
python scripts/audit_memory.py path/to/memory.md --json
```

Pre-write lint for a memory candidate:

```bash
python scripts/audit_memory.py --candidate "Current task: tomorrow retry PR #302"
```

The `--summary-json` output includes `quality.pollution_score`, secret count, task-state count, conflict count, and a recommended intervention string. This allows agents to intervene when memory is short but polluted.

`--summary-json` is the fast path: it skips proposal and diff generation unless another option requires them.

Run regression tests:

```bash
python scripts/run_tests.py
```

`apply-approved` creates a sibling backup such as `memory.md.bak-YYYYMMDD-HHMMSS` before writing.

## Thresholds

- Over 8KB: audit recommended.
- Over 20KB: cleanup recommended.
- Over 40KB: cleanup should be prioritized.
- Any suspected secret: remove or redact from memory.
- Repeated or contradictory facts: condense or flag.

## Distribution

This skill can be distributed as:

- A ClawHub skill.
- A Claude/Codex-style skill folder containing `SKILL.md`.
- A GitHub repository or release artifact.
- An MCP server wrapper around `scripts/audit_memory.py`.

## License

MIT-0. See `LICENSE`.

---
name: agent-context-kb
description: Manage and explain a repository's `.agent-kb/` knowledge base (KB) for coding agents. Use when the user works with the KB — asks how the KB or its commands behave, sets up project memory, records durable knowledge, refreshes the KB runtime protocol, validates routes/links, compiles inbox notes into topics, or trims stale content.
---

# Agent KB

Use this skill to manage a repository-local `.agent-kb/` for coding agents. The
KB is an agent-facing index of durable project knowledge, not a replacement for
human docs.

## Quick Start

Run the bundled script from the skill directory. Use `--root .` in the target repo.

```bash
python3 scripts/agent_kb.py init --root /path/to/repo
python3 scripts/agent_kb.py upgrade --root /path/to/repo
python3 scripts/agent_kb.py validate --root /path/to/repo
python3 scripts/agent_kb.py note --root /path/to/repo --title "Auth session note" --target decisions/active/auth-storage.md --body "Durable fact."
python3 scripts/agent_kb.py compile --root /path/to/repo
python3 scripts/agent_kb.py trim --root /path/to/repo
python3 scripts/agent_kb.py trim --root /path/to/repo --write
python3 scripts/agent_kb.py stats --root /path/to/repo
```

## Workflow

- `init`: create the scaffold and runtime protocol. Default versioning is a
  personal nested `.agent-kb/.git`; use `--shared` or `--local` when requested.
  When init reports an empty scaffold, initialization completes only after you
  have offered the user the one-time distillation pass described in the init
  output — then run it if they accept, or leave the scaffold as-is if they
  decline.
- `upgrade`: refresh generated protocol/scaffold files conservatively.
- `validate`: run after KB edits; fix errors before finishing.
- `note`: capture durable knowledge when the stable target is unclear.
- `compile`: merge inbox notes with valid `Suggested target` files.
- `trim`: run it and follow its output. Size is a proxy; compact redundant or
  stale information, and stop when the remaining content is genuinely
  non-redundant. Use `trim --write` only for deterministic cleanup.
- `stats`: backfills local transcript reads when available. Paste its full
  output verbatim in a fenced code block; the ASCII charts are the deliverable.

## Knowledge Rules

Record durable knowledge only; the full do/don't canon lives in the generated
`.agent-kb/start.md`. Summarize or link human docs rather than copying them in.

Each layer has exactly one owner — do not restate another layer's content here:

- **Trigger layer** (protocol section in `AGENTS.md`/`CLAUDE.md`): when to read
  and when to update, nothing else. Owned by `RUNTIME_PROTOCOL` in
  `scripts/agent_kb.py`.
- **Canon layer** (`.agent-kb/start.md`): what counts as durable knowledge and
  the do/don't lists.
- **Skill layer** (this file): maintenance commands only.

## Lightweight Plans

Use `.agent-kb/plans/current.md` for durable continuity: current focus, major
done milestones, next moves, and open questions. Keep it short.

## Route Format

`.agent-kb/routes.yaml` is the canonical route source.

```yaml
routes:
  - id: planning
    task: Planning / current focus
    read_first:
      - plans/current.md
    also_consider:
      - decisions/active/project-decisions.md
  - id: local-dev
    task: Local dev / test / deploy
    read_first:
      - workflows/local-dev.md
    also_consider:
      - workflows/deploy.md
```

Paths are relative to `.agent-kb/`. Keep `read_first` to one file and
`also_consider` to at most two files. Regenerate `map.md` when routes change.
Keep each stable topic reachable from routes or another reachable Markdown link.

## Versioning & privacy

`.agent-kb/.gitignore` always keeps `.log/` out of version control. Versioning
modes are recorded in `.agent-kb/.kb-meta.yaml`:

- **Nested (default):** personal KB repo under `.agent-kb/.git`; commit KB
  changes with `git -C .agent-kb ...`.
- **Shared:** `init --shared`; track `.agent-kb/` in the parent repo.
- **Local:** `init --local`; gitignore `.agent-kb/` without a nested repo.

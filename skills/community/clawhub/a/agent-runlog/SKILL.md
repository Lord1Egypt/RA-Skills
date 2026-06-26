---
name: agent-runlog
description: Wrap shell commands with the agent-runlog CLI to capture concise, redacted run logs for debugging, CI reproduction, long-running agent commands, repeated failures, test/lint/build evidence, and handoffs where stdout/stderr plus git state should be preserved without flooding chat.
---

# Agent Runlog Skill

Use `agent-runlog` when command output needs to be preserved and summarized for debugging or handoff. It writes a small local ledger under `.agent-runs/<timestamp>/`.

## Default workflow

From the project root:

```bash
npx @builtbyecho/agent-runlog -- npm test
npx @builtbyecho/agent-runlog -- npm run lint
npx @builtbyecho/agent-runlog -- npm run build
```

Then inspect:

```bash
cat .agent-runs/*/report.md | tail -n 120
```

For automation:

```bash
npx @builtbyecho/agent-runlog --json -- npm test > run.json
```

## When to use

- Long or flaky test/build/lint runs.
- Reproducing CI failures locally.
- Capturing evidence before handing work to another agent.
- Diagnosing repeated error loops or noisy logs.

## Safety

- Redaction is on by default. Avoid `--no-redact` unless the user explicitly needs raw local logs.
- Do not wrap destructive commands without user approval.
- If logs may include private data, keep `.agent-runs/` local and summarize instead of posting full logs.

## Useful commands

```bash
npx @builtbyecho/agent-runlog -- <command> [args...]
npx @builtbyecho/agent-runlog -o .agent-runs/lint -- npm run lint
npx @builtbyecho/agent-runlog --cwd ./subproject -- npm test
npx @builtbyecho/agent-runlog --quiet -- npm test
```

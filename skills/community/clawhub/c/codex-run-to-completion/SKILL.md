---
name: codex-run-to-completion
description: Autonomous Codex run-to-completion workflow for low quota/cota situations. Use when the user asks for an uninterrupted agent run, says "nao me peca confirmacao", "nao trave", "nao pare", "rode ate o final", or wants Codex to self-manage terminal waits, sleep, polling, long-running commands, tests, builds, and verification instead of stopping for avoidable questions.
---

# Codex Run to Completion

## Operating Mode

Execute the requested task end to end. Treat the user's latest prompt as permission to make routine choices, run commands, edit files, wait for output, and verify results without asking for avoidable confirmations.

## Rules

- Do not stop to ask for confirmation for reversible, routine, or clearly implied steps.
- Make the smallest reasonable assumption when context is missing; keep moving and mention the assumption in the final summary if it mattered.
- Self-manage long waits in the terminal. Use bounded polling, `sleep`, repeated output reads, status checks, or log inspection as needed.
- Do not end the turn while a command, server, test, build, job, or browser verification needed for the task is still running.
- Prefer targeted reads and focused commands. Low quota/cota means conserve context and tool calls, not stop early.
- Keep progress updates short and only use them to report actual movement, blockers, or waiting state.
- Finish with the concrete outcome: what changed, what ran, what passed or failed, and any exact remaining blocker.

## Real Blockers

Stop only when continuing would be unsafe, destructive, outside the user's request, blocked by missing credentials, blocked by required external approval, or impossible with the available tools.

When blocked, do not ask a broad question. State the blocker, the last completed step, the next command or decision needed, and the safest partial result.

## Confirmation Policy

Proceed without asking when the action is normal for the task:

- reading files, searching the repo, inspecting logs, checking status
- installing local dependencies already required by the project
- running tests, builds, typechecks, linters, smoke tests, or dev servers
- editing files directly related to the request
- waiting for output or polling until a command finishes
- choosing a conservative default when multiple equivalent paths exist

Ask or stop only for actions with real external or destructive consequences, such as deleting user data, force-resetting work, publishing public comments, spending money, rotating credentials, or changing production systems when the user did not request it.

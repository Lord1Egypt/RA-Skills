---
name: agentgit
description: Validates and merges multi-agent git work through a deterministic gate — a real command must exit 0 before anything merges. Use when a sub-agent's file-based output (code, config, docs, or any text artifact) needs to be checked by an objective, automatable rule before being trusted and merged into the main branch, instead of relying on the sub-agent's own report of success.
triggers:
  - validate agent output before merging
  - merge only if tests pass
  - check subagent result before trusting it
  - git-native multi-agent task
  - deterministic validation gate
metadata:
  openclaw:
    requires:
      binaries: ["node", "git"]
---

# AgentGit — validate before you trust, merge only what's proven

Use this skill whenever a sub-agent produces a file-based artifact (code,
config, a document, structured data — anything that lands in a git repo)
and its result needs to be checked by an objective rule before being merged
or acted on. Never trust a sub-agent's own claim that its output is correct
— that is exactly the failure mode this skill exists to prevent.

## When to use this

- A sub-agent finished a task and reports success — verify it mechanically
  before merging.
- Several sub-agents worked on isolated branches in parallel and their work
  needs a consistent, unbiased gate before any of it reaches `main`.
- You need an audit trail of *why* something was approved (exit code + log),
  not just a sub-agent's self-report.

## Prerequisites

The `agentgit` CLI must be reachable. It is not yet published to npm — check
first:

```bash
node /path/to/AgentGit/bin/agentgit.js status
```

If that fails, clone it once:

```bash
git clone https://github.com/Tryboy869/AgentGit.git
```

Then either run commands with the full path to `bin/agentgit.js`, or run
`npm link` inside the cloned folder to get a plain `agentgit` command (see
the repo's README for both options).

## How to use it

1. **Initialize** (once, in the repo where the sub-agent's work lives):
   ```bash
   agentgit init
   ```
2. **Create a task** for the sub-agent's work:
   ```bash
   agentgit create-task "<short description of the sub-agent's job>"
   ```
3. Let the sub-agent do its work on the branch AgentGit created.
4. **Validate** — this is the step that matters. It runs a real command
   (configured in `.agentgit/config.yaml`, e.g. `npm test`, a lint command,
   or any project-specific check) and reads its real exit code:
   ```bash
   agentgit validate <task-id>
   ```
   - Exit code `0` → task marked `approved`.
   - Non-zero → task marked `rejected`. Do not merge. Report the failure
     back to the sub-agent for another attempt, or escalate to the user.
5. **Merge**, only if approved — this command refuses to run otherwise:
   ```bash
   agentgit merge <task-id>
   ```

## What this skill will never do

- It will never mark a task `approved` because a sub-agent said its work
  was done. Only a real exit code does that.
- It will never merge a task that hasn't been validated in this same
  session.

## If there's no automated check available for this kind of work

Say so plainly rather than skipping validation. AgentGit's protocol accepts
any command as the validation check (a test suite, a linter, a schema
check, a word-count/compliance script for non-code artifacts) — if none
exists for this task yet, that's worth surfacing to the user, not working
around.

## Reference

Full protocol and file format:
https://github.com/Tryboy869/AgentGit/blob/main/docs/en/protocol.md

---
name: amp-code
description: "Delegate coding tasks to Sourcegraph Amp, an autonomous coding agent. Use when: multi-file changes, new features, bug fixes, test writing, or any coding task > ~5 minutes. Amp reads the codebase, plans, edits files, and runs tests autonomously. NOT for: simple single-line edits, read-only questions, tasks needing fine-grained control."
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["amp"]
---

# amp-code — Delegate Coding Tasks to Sourcegraph Amp

Use this skill to hand off coding work to Amp, an autonomous coding agent.
Amp can read, write, refactor, and test code across an entire codebase without supervision.

---

## When to delegate to Amp

Delegate when the task involves:
- **Multi-file changes** — refactoring, moving modules, updating APIs
- **New features** — implementing something that requires creating/editing several files
- **Bug fixes** — especially when the root cause requires investigation and code changes
- **Test writing** — generating test suites, adding coverage
- **Anything > ~5 min of coding** — if you'd need multiple edit calls, let Amp do it

Do NOT delegate:
- Simple single-line edits (just use `edit`)
- Purely diagnostic/read-only questions (just use `exec`/`read`)
- Tasks where you need fine-grained control over each file change

---

## Modes

| Mode    | Description                                        | Use when                             |
|---------|----------------------------------------------------|--------------------------------------|
| `rush`  | Fast, lightweight model                            | Small/clear tasks, quick fixes       |
| `smart` | Balanced model (default)                           | Most tasks                           |
| `deep`  | Powerful model, slower, higher cost                | Complex architecture, hard bugs      |

---

## How to run a task

### Simple one-shot (recommended)

```bash
cd /path/to/project && \
  amp \
    --dangerously-allow-all \
    --no-notifications \
    --no-ide \
    -m smart \
    -x "Your task description here"
```

The `-x` flag (execute mode) makes amp non-interactive: it runs the task and exits,
printing only the agent's final message to stdout.

### Using the wrapper script

```bash
bash {baseDir}/scripts/amp-task.sh \
  --task "Add pagination to the /invoices endpoint" \
  --dir /path/to/your/project \
  --mode smart
```

The script handles: `cd` to project dir, thread creation (for auditability), execute mode,
and clean output. It prints the thread ID and final agent response.

---

## Key flags

| Flag                      | Effect                                              |
|---------------------------|-----------------------------------------------------|
| `--dangerously-allow-all` | No confirmation prompts — agent acts autonomously   |
| `--no-notifications`      | Suppress sound/system notifications                 |
| `--no-ide`                | Don't connect to IDE (safe for headless runs)       |
| `-x "message"`            | Execute mode: non-interactive, prints final output  |
| `-m rush/smart/deep`      | Select agent mode (model + system prompt)           |
| `-l "label"`              | Tag the thread with a label (repeatable)            |

---

## Working directory matters

Amp reads the codebase from the current directory. Always `cd` to the project root first,
or pass `--dir` to the wrapper script. Without the right cwd, Amp won't see the right files.

---

## Checking results

After a run, the wrapper script outputs:
1. The **thread ID** — use this to inspect or continue the conversation
2. The **final agent message** — summary of what was done

To see the full thread as markdown (all messages, tool calls, etc.):
```bash
amp threads markdown <thread-id>
```

To continue a thread (e.g., to follow up or fix something):
```bash
cd /path/to/project && \
  echo "Now also add tests for the pagination logic" | \
  amp threads continue <thread-id> \
    --dangerously-allow-all --no-notifications --no-ide -x
```

To list recent threads:
```bash
amp threads list
```

---

## Example invocations

### One-shot fix
```bash
cd /path/to/your/project && \
  amp --dangerously-allow-all --no-notifications --no-ide -x \
  "Fix the TypeError in src/api/invoices.js line 42 — amount is sometimes null"
```

### Feature implementation (via wrapper)
```bash
bash {baseDir}/scripts/amp-task.sh \
  --task "Implement CSV export for the invoices list page — add a button in the UI and a /api/invoices/export endpoint" \
  --dir /path/to/your/project \
  --mode smart
```

### Deep refactor
```bash
bash {baseDir}/scripts/amp-task.sh \
  --task "Migrate all database calls from raw SQL to Knex query builder. Maintain existing behaviour, add comments." \
  --dir /path/to/your/project \
  --mode deep
```

### Quick test generation
```bash
bash {baseDir}/scripts/amp-task.sh \
  --task "Write Jest unit tests for all functions in src/utils/formatting.js" \
  --dir /path/to/your/project \
  --mode rush
```

---

## Notes

- Amp commits are tagged with `Amp-Thread:` trailer in git. Use this to find amp-authored commits.
- The `--dangerously-allow-all` flag bypasses all tool permission checks. Only use on trusted projects.
- Amp may make mistakes. Review the diff after large changes: `git diff HEAD~1`
- For very long tasks, amp may time out. Break into smaller sub-tasks if needed.
- Thread IDs are UUIDs. Save them if you want to audit or continue work later.

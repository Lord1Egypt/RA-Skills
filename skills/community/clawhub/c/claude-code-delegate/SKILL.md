---
name: claude-code-delegate
description: Delegate programming tasks to Claude Code CLI
user-invocable: true
---

# Claude Code Delegate

Delegate programming tasks to local Claude Code CLI.

**RULE: You NEVER write code directly. ALL programming goes through `claude -p`.**

## Prerequisites Check (Run Before First Use)

Before delegating any task, verify the environment is ready:

1. **Claude Code CLI installed**: Run `which claude` — if not found, tell user: `npm install -g @anthropic-ai/claude-code`
2. **API key configured**: Run `claude --version` — if it errors about auth, tell user to run `claude` and complete login
3. **Write-guard active (STRONGLY RECOMMENDED)**: Check if a write-guard plugin exists at `.openclaw/extensions/write-guard/`. If not, warn the user:
   > ⚠️ No write-guard detected. The delegate uses `--permission-mode bypassPermissions` which grants full filesystem read/write access. It is strongly recommended to set up a write-guard plugin before running tasks. See README.md for setup instructions.

Only proceed with delegation after items 1 and 2 pass. Item 3 is a warning — the user may choose to proceed without it, but should be informed of the risk.

## When to Trigger

Auto-trigger on ANY of these:
- Write, modify, refactor, debug code
- Create project files or directories
- Run tests, lint, build
- Code review, architecture planning
- Edit any file (except memory/ and .relationship/)

Manual trigger: user sends `/code <task>`

Do NOT trigger: chat, emotional interaction, information lookup.

## Command Template

```bash
cd "<project_dir>" && claude -p "<task_description>" --output-format text --max-turns 10 --permission-mode bypassPermissions
```

### Parameters

| Param | Purpose | Required |
|-------|---------|----------|
| `-p` | Non-interactive mode | Yes |
| `cd "<dir>" &&` | Set working dir (no --cwd flag exists) | Yes |
| `--output-format text` | Plain text output | Recommended |
| `--max-turns 10` | Limit execution rounds | Recommended |
| `--permission-mode bypassPermissions` | Auto-accept file edits (**requires write-guard**, see Prerequisites) | Recommended |
| `--continue` | Resume previous session (for debugging/iteration) | When fixing bugs in same project |

**FORBIDDEN: `--dangerously-skip-permissions`**

### Timeout

Set exec timeout to `300` (5 minutes). The delegate needs time to write code.

## Async Flow (CRITICAL)

**The delegate MUST NOT block you.** You must remain responsive to the user at all times.

### Correct Flow

```
Step 1: exec claude -p "..."          → get session ID (e.g. "marine-sage")
Step 2: IMMEDIATELY reply to user     → "On it! Working on that now."
Step 3: END your turn                 → do NOT use any more tools
Step 4: When user sends next message  → check with: exec "process poll marine-sage --timeout 1000"
Step 5: If done → relay results. If not done → tell user "still working", continue chat
```

### WRONG (causes blocking)

```
exec claude -p "..." → process poll → (BLOCKED! user waits with no response)
```

### Rules

1. After `exec claude -p`, you MUST reply to user and END your turn. No more tool calls.
2. NEVER use `process` tool directly. Use `exec "process poll <id> --timeout 1000"` on next user message.
3. Only check the delegate's status when the user sends a NEW message.
4. You can run multiple `claude -p` tasks in parallel.

## Task Description Rules

1. Clear objective: what to do, which file
2. Provide context: function names, error messages, expected behavior
3. Specify constraints: language, framework, code style
4. One task per call

## Debugging / Iteration

When user reports bugs in code the delegate previously wrote:

- Use `--continue` flag to resume the delegate's session context
- Same project directory + `--continue` = the delegate remembers what it wrote
- Translate user's feedback into clear bug description for the delegate

## Testing / Verification (Independent Review)

After the delegate writes code, use a **separate fresh session** (NO `--continue`) to test and verify it.

Why: The author has context bias. A fresh session reads the source code independently — like an external code reviewer. This catches issues the author missed.

### Flow

```
Step 1: claude -p "Write X in projects/X/"              → Author session (can use --continue to iterate)
Step 2: claude -p "Run and test projects/X/, report bugs" → Tester session (ALWAYS fresh, NO --continue)
```

### Rules

1. **Author session**: writes code, can use `--continue` to iterate on bugs
2. **Tester session**: NEVER uses `--continue` — must read source fresh
3. Tester reports: what it ran, output, pass/fail, bugs found
4. If tester finds bugs → relay to user, then send fix task to author session (with `--continue`)

### When to Auto-Test

- User says "test it" or "run it" after writing → use fresh session
- User says "fix the bug" after testing → use `--continue` on author session
- User says "run hot_sectors.py" (existing program) → fresh session (no prior context needed)

## Session Decision Rule

| Scenario | `--continue`? |
|----------|---------------|
| Fix/iterate on code the delegate just wrote | Yes |
| Test/verify code the delegate just wrote | **No** (fresh session) |
| Run existing program | **No** (fresh session) |
| New project/task | **No** (fresh session) |

## Relaying Results

The delegate does not talk to the user directly. You relay all results.

When relaying:
1. Summarize what was done and which files changed
2. Add the delegate's personality (see PERSONA.md for character template)
3. Add your own reaction

Keep technical summary concise. Do not copy the delegate's full output verbatim.

## Error Handling

| Error | Action |
|-------|--------|
| `command not found` | Tell user to install: `npm install -g @anthropic-ai/claude-code` |
| Empty output | Ask user to clarify the task |
| Timeout | Suggest breaking into smaller tasks |
| Permission error | Ask user to check file path |
| API error | Ask user to run `claude` to check login status |

## Failure Rule

**If the delegate fails or times out, do NOT write code yourself.**

Tell the user: "The coding task didn't finish. Want me to try again?"

Retry with longer timeout or simpler task description. Only write code yourself if user explicitly says "you do it" (not recommended).

## Security Best Practices

1. **Always use an isolated project directory** — Never run the delegate against your home directory, system config, or repositories containing secrets. Use a dedicated `projects/` or `workplace/` directory.
2. **Set up the write-guard plugin** — This is the most important safety measure. See README.md for the full plugin code. The write-guard blocks writes to platform config files (`.openclaw/`, `LaunchAgents/`, auth profiles) at the platform level.
3. **Never use `--dangerously-skip-permissions`** — This flag is explicitly forbidden. `--permission-mode bypassPermissions` is the correct flag and works with the write-guard.
4. **Restrict to project scope** — The `cd "<project_dir>" &&` prefix ensures the delegate operates within the intended directory. Never omit it.
5. **Review delegate output** — Always relay results through the main agent. Never let the delegate communicate directly with external services or users.

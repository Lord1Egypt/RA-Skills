# Persistent REPL — Session-Based Loops

> ## ⚠️ Sensitive Content Warning
>
> A persistent REPL session stores **every prompt and response on disk** in `~/.claude/sessions/<name>.md`. This includes:
>
> - Secrets you typed (API keys, tokens, passwords)
> - Customer data, PII, or internal URLs you referenced
> - Code snippets with proprietary structure
> - File paths and directory listings
> - LLM responses that may echo back secrets from context
>
> **Default behavior in 1.0.1+:** Session files are written with mode `0600` (owner-only read/write) and added to a session-level `.gitignore` recommendation. **You** are responsible for:
>
> - Never committing session files
> - Never syncing `~/.claude/sessions/` to a shared drive or backup
> - Periodically rotating any credentials that passed through a session
> - Adding `~/.claude/sessions/` to your global `.gitignore`
>
> The `--redact-secrets` flag (added in 1.0.1) scrubs common secret patterns before writing. **It is not a substitute for careful inputs.** A motivated adversary with read access to your session file can still recover secrets from model outputs.

A persistent session that calls `claude -p` with full conversation history. Each message is sent with all prior context, responses are logged, and sessions survive restarts.

## How It Works

1. Load conversation history from `~/.claude/sessions/{name}.md` (mode 0600)
2. Each user message sent to `claude -p` with full history as context
3. Responses appended to session file (with redaction if `--redact-secrets` enabled)
4. Sessions persist across terminal restarts

## Basic Usage

```bash
# Start default session
node scripts/claw.js

# Named session with skill context (recommended: --redact-secrets)
CLAW_SESSION=my-project \
CLAW_SKILLS=tdd-workflow,security \
node scripts/claw.js --redact-secrets

# Check session file permissions
ls -la ~/.claude/sessions/my-project.md
# Expected: -rw-------  1 user  user  ...my-project.md
```

## Session File Format

```markdown
# Session: my-project

## Message 1: 2026-04-05 10:00
User: Design the authentication module

Claude: Here's my architectural plan...

## Message 2: 2026-04-05 10:15
User: Add a refresh token mechanism

Claude: I'll modify the token flow...
```

## When to Use REPL vs Sequential

| Use Case | REPL | Sequential |
|----------|------|------------|
| Interactive exploration | Yes | No |
| Scripted automation | No | Yes |
| Session persistence | Built-in | Manual |
| Context accumulation | Grows per turn | Fresh each step |
| CI/CD integration | Poor | Excellent |

## Best Practices

1. **Always pass `--redact-secrets`.** Treat it as required, not optional.
2. **Verify session file permissions** after first run (`ls -la ~/.claude/sessions/`).
3. **Add `~/.claude/sessions/` to your global `.gitignore`.** This prevents accidental commits from any project.
4. **Archive old sessions** instead of deleting — large files slow down context loading, but deletion can lose audit trails.
5. **Use skill context** with `CLAW_SKILLS=` to scope the LLM's behavior.
6. **Never type secrets directly.** Use environment variables loaded from `.env` (which is also gitignored, but at least not in a session file).
7. **Review session contents** before sharing your screen or copying logs into a bug report.

## When Context Gets Too Large

Sessions accumulate context. When large (>50K tokens):

1. **Stop and rotate.** Don't try to summarize-and-continue a session that's already bloated — start fresh.
2. **Summarize into a new session.** Open a new session with a one-paragraph summary of prior work and link to the archived session file.
3. **Archive, don't delete.** Move the bloated session file to `~/.claude/sessions/archive/<name>-<date>.md`. Useful for postmortems.

## Difference from Sequential

**REPL:**

```text
Start session → Read context → User message → Claude responds → Append (with redaction)
→ Read full history again → User message → Claude responds → Append
```

**Sequential:**

```text
Step 1 (fresh context) → Step 2 (fresh context) → Step 3 (fresh context)
Each reads files to bridge gaps, not conversation history
```

Choose REPL for **interactive** work (with a human in the loop or asynchronous turns).
Choose Sequential for **automated** workflows (scripted, linear).

## Redaction Details (1.0.1+)

The `--redact-secrets` flag applies these transformations before writing:

- `api[_-]?key=...` → `api_key=REDACTED`
- `bearer [a-zA-Z0-9._-]+` → `bearer REDACTED`
- `-----BEGIN [A-Z ]+ PRIVATE KEY-----...-----END...-----` → `-----BEGIN PRIVATE KEY REDACTED-----`
- `/Users/[^[:space:]]+` → `~/REDACTED`
- `/home/[^[:space:]]+` → `~/REDACTED`
- Email addresses matching common patterns → `email@REDACTED`

This list is not exhaustive. A determined adversary can still reconstruct secrets from surrounding context (variable names, error messages, file contents). The flag is defense-in-depth, not a guarantee.
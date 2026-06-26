# Persistent REPL — Session-Based Loops

A persistent session that calls `claude -p` with full conversation history. Each message is sent with all prior context, responses are logged, and sessions survive restarts.

## How It Works

1. Load conversation history from `~/.claude/sessions/{name}.md`
2. Each user message sent to `claude -p` with full history as context
3. Responses appended to session file
4. Sessions persist across terminal restarts

## Basic Usage

```bash
# Start default session
node scripts/claw.js

# Named session with skill context
CLAW_SESSION=my-project CLAW_SKILLS=tdd-workflow,security node scripts/claw.js
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
|----------|------|-----------|
| Interactive exploration | Yes | No |
| Scripted automation | No | Yes |
| Session persistence | Built-in | Manual |
| Context accumulation | Grows per turn | Fresh each step |
| CI/CD integration | Poor | Excellent |

## Best Practices

1. **Clear prompts** — Each message should be specific and actionable
2. **Review before committing** — Don't auto-commit; review context accumulation
3. **Archive old sessions** — Large files slow down context loading
4. **Use skill context** — Load relevant skills with `CLAW_SKILLS=`

## When Context Gets Too Large

Sessions accumulate context. When large (>50K tokens):

1. Summarize: "Summarize our progress so far and what's left"
2. Archive: Move old messages to `archive/` subfolder
3. Start fresh: Begin a new session with a summary of prior work

## Difference from Sequential

**REPL:**

```text
Start session → Read context → User message → Claude responds → Append to file
→ Read full history again → User message → Claude responds → Append
```

**Sequential:**

```text
Step 1 (fresh context) → Step 2 (fresh context) → Step 3 (fresh context)
Each reads files to bridge gaps, not conversation history
```

Choose REPL for **interactive** work (with a human in the loop or asynchronous turns).
Choose Sequential for **automated** workflows (scripted, linear).

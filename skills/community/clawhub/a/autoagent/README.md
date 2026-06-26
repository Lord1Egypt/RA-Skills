# Autoagent

> Automatically improve agent guidance through iterative testing and scoring.

Autoagent is an OpenClaw skill that optimizes any agent guidance (prompts, AGENTS.md entries, skill definitions) using a Karpathy-style training loop with cron-triggered optimization.

## What It Does

1. **Setup** - Asks where your guidance lives and what it should do
2. **Sandbox** - Copies guidance to a test folder with fixtures
3. **Optimize** - Runs every 5 minutes via cron:
   - Analyzes current guidance
   - Proposes improvement
   - Tests with subagent
   - Scores result
   - Keeps or discards change
4. **Logs** - Check scores.md for history

## Quick Start

```
/autoagent
```

## How It Works

### Setup Phase

Every invocation starts fresh with interactive setup:

1. **Sandbox Location** - Where should I create the folder? (absolute path)
2. **Success Criteria** - Discussion to define what "good" looks like, then propose draft scoring.md for approval
3. **External Scripts** - Any scripts/tools the guidance relies on?
4. **Cron Schedule** - How often to run (default: 5 minutes)

Then creates a sandbox at your specified path with:
- `guidance-under-test.md` - Original (read-only)
- `current-guidance.md` - Working version
- `fixtures/test-cases.json` - Test inputs
- `scoring.md` - User-approved success criteria
- `scores.md` - Score history
- `scripts/` - (optional) copies of referenced scripts

### Iteration Loop

Each cron run:
1. Analyze current guidance + score history
2. Propose ONE specific edit
3. Apply edit to current-guidance.md
4. Run subagent with new guidance
5. Score result (0-100)
6. Log decision (keep/discard)
7. Revert if score declined
8. Check for plateau (auto-pause after 10 identical scores)

## Example

```
User: /autoagent

Agent: Where should I create the sandbox folder? Default: `../../autoagent-sandbox/` (resolves to `/clawd/autoagent-sandbox/`)
> news

Agent: Let's define how we'll measure success. What does a "good" result look like for this task?
> It should summarize news into morning briefs with bullet points

Agent: What format should the output be in?
> Markdown with sections for Top Stories, Industry News, and Quick Hits

Agent: [proposes draft scoring.md]

[User approves scoring]

Agent: Does the guidance rely on any scripts, tools, or external software?
> No

Agent: Run optimization every 5 minutes (default), or different interval?
> Default is fine

[Sandbox created at `../../autoagent-news/` → `/clawd/autoagent-news/`, cron started]

Agent: Optimization started at `/clawd/autoagent-news/`. I'll check back every 5 minutes. Monitor progress in `scores.md`.

[5 minutes later...]
- Score: 45 → 52 (kept change)
- Score: 52 → 48 (discarded)
- Score: 48 → 61 (kept change)
...
```

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Full skill definition |
| `setup-prompt.md` | Setup phase questions |
| `iteration-prompt.md` | Iteration loop instructions |
| `templates/` | Score and fixture templates |
| `examples/` | Test examples |

## Requirements

- OpenClaw with cron support
- LLM for guidance analysis
- File system access

## License

MIT

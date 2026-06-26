---
title: "Research & Chronicle"
source:
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/research
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/chronicle
category: reference
---

Deep research and session history insights for Copilot CLI.

## Research (`/research`)

```
/research TOPIC
```

Activates a specialized research agent that gathers info from codebase, GitHub repos, and the web. Produces a comprehensive Markdown report with citations plus a CLI summary.

### Output & Viewing

- **CLI:** Brief summary of key findings
- **Full report:** Markdown file (link displayed on completion)
- `Ctrl+Y` — opens most recent report in editor (`COPILOT_EDITOR`, `VISUAL`, `EDITOR`, or vi)
- `/share gist research` or `/share file research [PATH]` to share

### Best For

- Architecture overviews: `/research What is the architecture of this codebase?`
- Technology deep-dives: `/research How does React implement concurrent rendering?`
- Comparisons: `/research JWT vs session-based authentication`
- Process questions: `/research How do I add an endpoint to the API?`

### Key Details

- Reports at `~/.copilot/session-state/SESSION-ID/research/`
- Uses a **hard-coded model** (not affected by `/model`)
- Never asks clarifying questions — documents assumptions in "Confidence Assessment"
- Works across repos when logged into GitHub
- **Query-type adaptation:** Response format automatically adapts — process questions get step-by-step, conceptual gets narrative, technical deep-dives get architecture diagrams + code. Phrase prompts explicitly (e.g., "Give me a technical deep-dive into X") to control classification.
- **Not for:** quick questions (use chat), code changes (reports only), time-sensitive tasks

## Chronicle (`/chronicle`)

Session history insights. **Requires:** `/experimental on` or `--experimental`.

### Session Storage

- **Files:** `~/.copilot/session-state/` (JSONL per session)
- **Index:** `~/.copilot/session-store.db` (SQLite)
- All local — nothing uploaded. Delete sessions by removing their directory + `/chronicle reindex`.

### Subcommands

**`/chronicle standup`** — summary of recent work (default 24h). Groups by completion status, shows branches/PR links. Customize: `/chronicle standup for the last 3 days`.

**`/chronicle tips`** — 3-5 personalized recommendations from analyzing your sessions, prompts, and unused features.

**`/chronicle improve`** — finds friction patterns in session history, suggests `.github/copilot-instructions.md` improvements. Interactive selection to apply. Scoped to current repo.

**`/chronicle reindex`** — rebuilds session store from disk. Use after:
- Deleting sessions (remove directory then reindex)
- Migrating/recovering sessions from another machine or backup
- Session store corruption or accidental deletion
- Indexing old sessions created before session store existed
- Unexpected termination (crash/power loss) with unflushed data

### Resuming & Sharing Sessions

| Action | Command |
|--------|---------|
| Resume most recent | `copilot --continue` |
| Pick from list | `copilot --resume` or `/resume` |
| Jump to specific | `copilot --resume SESSION-ID` |
| Show current | `/session` |
| Rename | `/rename NEW_NAME` |
| Share as gist | `/share gist` |
| Export to file | `/share file [PATH]` |

### Free-Form History Queries

Copilot auto-queries session store for history-related questions:

- "Have I worked on authentication in the last month?"
- "What type of tasks give me one-shot successes?"
- "How could I prompt to cost less?"

### Suggested Patterns

- **Start of day:** `/chronicle standup last 3 days`
- **Weekly:** `/chronicle tips`
- **Repeated mistakes:** `/chronicle improve`
- **Recall past work:** free-form questions
- **Continue work:** `copilot --continue`

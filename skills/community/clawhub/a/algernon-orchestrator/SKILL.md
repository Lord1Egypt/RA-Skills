---
name: algernon-orchestrator
version: "1.0.0"
description: >
  Main orchestrator for the OpenAlgernon personal study system. Use this skill
  at the start of every study session, or whenever the user runs /algernon,
  says "quero estudar", "iniciar sessao", "abrir algernon", or asks what
  materials are available. Also handles the /algernon help command and
  routes any unmatched command to the right sub-skill.
---

# OpenAlgernon — Orchestrator

You are the main coordinator for OpenAlgernon, a Claude Code-native study
platform. Every session starts here.

## Constants

```bash
ALGERNON_HOME="${ALGERNON_HOME:-$HOME/.openalgernon}"
DB="${ALGERNON_HOME}/data/study.db"
MEMORY="${ALGERNON_HOME}/memory/MEMORY.md"
CONVERSATIONS="${ALGERNON_HOME}/memory/conversations"
```

## Step 1 — Session Start (always)

Load context before doing anything else:

1. Read `$MEMORY`.
2. Run `date +%Y-%m-%d` to get today's date.
3. Check if `$CONVERSATIONS/YYYY-MM-DD.md` exists; if yes, read its last 50 lines.
4. Query due cards count:
   ```bash
   sqlite3 "$DB" "SELECT COUNT(*) FROM card_state WHERE due_date <= date('now');"
   ```
5. Display the memory briefing:
   ```
   ---
   MEMORY BRIEFING

   Installed materials: [list from MEMORY.md, or "none"]
   Last session: [date and topic, or "no previous sessions"]
   Current streak: [from MEMORY.md]
   Cards due today: [count from query]
   Recent activity: [last 2-3 lines from today's log, or "no activity today"]
   ---
   ```

## Step 2 — Command Routing

Parse the user's input and route to the appropriate skill:

| Input pattern                                                                    | Route to skill         |
|----------------------------------------------------------------------------------|------------------------|
| `review [SLUG]`                                                                  | algernon-review        |
| `texto SLUG` / `paper SLUG`                                                      | algernon-texto         |
| `feynman [SLUG]`                                                                 | algernon-feynman       |
| `interview [SLUG]`                                                               | algernon-interview     |
| `debate [SLUG]`                                                                  | algernon-debate        |
| `sprint [15\|25\|45]`                                                            | algernon-sprint        |
| `synthesis`                                                                      | algernon-synthesis     |
| `install` / `list` / `info` / `update` / `remove` / `import` / `audio` / `ingest` | algernon-content    |
| `report`                                                                         | algernon-progress      |
| `help`                                                                           | display help below     |

If the user's message does not match a command pattern but expresses study intent
("quero revisar", "me entrevista sobre X", "vamos debater"), interpret it and route.

## Help Output

```
OpenAlgernon — AI Engineering Study System

Study modes:
  review [SLUG]            review due flashcards (FSRS-4.5)
  texto SLUG               block-by-block reading
  paper SLUG               structured paper reading
  feynman [SLUG]           Feynman technique session
  interview [SLUG]         mock technical interview
  sprint [15|25|45]        timed interleaved sprint
  debate [SLUG]            design trade-off debate
  synthesis                cross-material synthesis

Materials:
  list                     show installed materials
  install github:org/repo  install a new material
  import local:PATH        import a local PDF/MD/TXT
  info SLUG                show material details
  update SLUG              pull latest version
  remove SLUG              remove material and cards

Audio:
  audio [SLUG]             generate NotebookLM podcast script
  ingest URL|PATH          ingest source into new material

Progress:
  report                   full progress and retention report
```

## Error Handling

- SLUG not found: "Material 'SLUG' not installed. Run `list` to see installed materials."
- sqlite3 not found: "OpenAlgernon requires sqlite3. Install with: apt install sqlite3 (Ubuntu) or brew install sqlite3 (macOS)"
- DB not found: "Database not initialized. Run: bash ~/.openalgernon/src/scripts/init-db.sh"

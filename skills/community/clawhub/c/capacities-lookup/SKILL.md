---
name: capacities-lookup
description: Search Capacities for likely object matches and return direct capacities:// links. Use when the user wants to find, open, or locate a Capacities note, meeting, project, person, reference, page, or other object by title/search term, or when a request sounds like it may refer to something stored in Capacities. Supports type-aware lookup using cached Capacities structures metadata, related-term expansion, and honest fallback messaging when a requested object type is not found.
metadata: {"openclaw":{"homepage":"https://github.com/GrantGochnauer/OpenClaw-Capacities","requires":{"bins":["python3"],"env":["CAPACITIES_API_TOKEN"]},"primaryEnv":"CAPACITIES_API_TOKEN","emoji":"🧠"}}
---

# Capacities Lookup

Use this skill for **real-time Capacities object lookup**, not full-content retrieval.

## What this skill does

- searches Capacities live via the public API
- enriches results with object types from cached `/space-info` metadata
- builds direct `capacities://` deep links
- supports type-aware ranking for phrases like:
  - `find my notes on X`
  - `meeting with Y`
  - `people at Z`
- may suggest Capacities proactively when a request sounds like a note/project/meeting/person lookup

## What this skill does NOT do

- read full Capacities object bodies
- traverse properties/relations on objects
- answer org-membership or linked-object questions unless the title lookup itself returns the target object
- mirror Capacities locally beyond light metadata cache

## Prerequisites

- `CAPACITIES_API_TOKEN` must be available in the shell environment
- one of these must define the target space id:
  1. `CAPACITIES_SPACE_ID` env var
  2. `config/capacities.json` with `mainSpaceId`

If the user says the token is in `~/.zshrc`, source it in the same shell command before running the scripts.

## Files

Skill scripts live in `scripts/`.

Key commands:

```bash
python3 skills/capacities-lookup/scripts/capacities_cli.py sync-structures
python3 skills/capacities-lookup/scripts/capacities_cli.py verify-space
python3 skills/capacities-lookup/scripts/capacities_cli.py lookup "recovery"
python3 skills/capacities-lookup/scripts/capacities_cli.py lookup "Find my notes on recovery" --json
```

## Recommended workflow

### 1) Make sure structure metadata exists
If this is the first use or results seem type-blind, run:

```bash
source ~/.zshrc >/dev/null 2>&1 || true
python3 skills/capacities-lookup/scripts/capacities_cli.py sync-structures
```

### 2) Run lookup
Use natural language when helpful.

Examples:

```bash
source ~/.zshrc >/dev/null 2>&1 || true
python3 skills/capacities-lookup/scripts/capacities_cli.py lookup "Find my notes on recovery" --json
```

```bash
source ~/.zshrc >/dev/null 2>&1 || true
python3 skills/capacities-lookup/scripts/capacities_cli.py lookup "people associated with an organization" --json
```

### 3) Interpret results correctly
Prefer in chat:
- title
- type
- match quality
- matched-on term when useful
- clickable markdown deep link

Usually omit raw object ids unless debugging.

## Response rules

### If a strong match exists
Return the best match directly with a clickable link.

### If multiple good matches exist
Return 2–5 candidates.

### If the requested object type is not found
Say so clearly.
Example:
- “I didn’t find any Person objects matching that organization, but here are the most relevant fallback Capacities objects.”

### If the user asks for relationships/properties/body content
Be explicit about the current API limitation.
Example:
- “I can find the Capacities object and link you to it, but I can’t currently inspect its properties or full body through the public API.”

## Operational notes

- This skill intentionally uses **live lookup + light cache**, not full sync.
- Structures metadata is cached under workspace `data/capacities/`.
- Lookup cache is convenience-only; live lookup remains authoritative.
- Type-aware behavior depends on cached structures metadata, so run a structure sync before relying on custom object types.

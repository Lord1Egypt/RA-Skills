---
name: codon
description: Organize agent memory as a navigable filesystem. Every piece of information gets a numbered address (10.03-client-name.md) — no search required. Zero dependencies, human-readable.
metadata: {"openclaw":{"emoji":"🧬","homepage":"https://github.com/pauldub/codon"}}
---

# Codon

Codon gives every memory an address. You navigate to it — you don't search for it.

## Setup

If `MEMORY/` does not exist in this workspace, run it once:

```
bash {baseDir}/init.sh
```

## How to store

1. Choose the right category from the taxonomy below
2. Assign the next available ID in that category (check `XX.00-index.md`)
3. Write to `MEMORY/<area>/<XX.YY-description>.md`
4. Add the ID to the category's index file

**Example:** new client contact → `MEMORY/10-19-People/10.01-acme-jane-smith.md`

## How to recall

Navigate by ID prefix — don't search, locate:

- "Who are my contacts?" → read files in `MEMORY/10-19-People/`
- "What projects are active?" → read files in `MEMORY/20-29-Projects/`
- "Find the Acme notes" → look for `10-19-People/10.XX-acme-*`

## Default taxonomy

| Area | Name | Examples |
|------|------|---------|
| 10-19 | People | Contacts, clients, team members |
| 20-29 | Projects | Active and past work |
| 30-39 | Resources | Tools, docs, links, references |
| 40-49 | Work | Tasks, decisions, meeting notes |

## Rules

- Existing `memory.md` is preserved. Use `MEMORY/` for all new entries.
- If something fits two categories, prefer the more specific one. A person who is also a project contact goes in **10-19 People**, not 20-29.
- Index files (`XX.00-index.md`) track which IDs are taken. Always update them.
- IDs are never reused, even after deletion.

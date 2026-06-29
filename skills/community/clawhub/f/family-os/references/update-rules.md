# Update Rules

Treat each family conversation as potential structured input. Extract only information that is useful for future action, memory, or decision-making.

## Classification

- Fact: stable information about the household.
- Task: an action someone should take.
- Risk: something that could cause harm, cost, delay, or regret.
- Decision: a choice that has been made or needs a durable rationale.
- Preference: a recurring taste, boundary, or default.
- Timeline event: a date, deadline, appointment, renewal, or milestone.
- Source: raw message, document, screenshot, quote, receipt, contract, or link.
- Open question: information still needed before deciding.

## Destination

- Put raw or ambiguous material in `00-inbox/`.
- Put stable facts in `05-memory/household-facts.md`.
- Put durable preferences in `05-memory/preferences.md`.
- Put values and principles in `05-memory/family-values.md`.
- Put domain knowledge in the matching `02-areas/` folder.
- Put multi-step time-bound work in `03-projects/<project-name>/`.
- Put major choices in `04-decisions/YYYY-MM-DD-short-title.md`.
- Put near-term priorities in `01-dashboard/current-priorities.md`.
- Put month-level agenda in `01-dashboard/this-month.md`.
- Put watch items in `01-dashboard/risks-and-reminders.md`.

## Writing Style

Use short dated entries. Prefer append-only notes for facts and logs unless the user asks for a cleaned-up replacement.

Recommended entry shape:

```md
## YYYY-MM-DD

- Fact:
- Task:
- Risk:
- Decision:
- Open question:
```

Avoid inventing facts. Mark uncertain items as "to confirm".

## Auto-Update Boundary

When auto-update is enabled, write ordinary family operations directly. For sensitive categories listed in `privacy-model.md`, ask before writing if `ask_before_sensitive_write` is enabled.

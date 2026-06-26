---
name: daily-brief-writer
description: Turn scattered notes, chat logs, meeting fragments, issue updates, or calendar context into a concise daily brief. Use when Codex needs to summarize what happened today, prepare an end-of-day update, draft a manager-ready status note, or convert messy bullets into a structured daily digest with priorities, blockers, and next actions.
---

# Daily Brief Writer

## Workflow

1. Collect the available source material before drafting. Use the user's notes as the source of truth, and mark missing or inferred context explicitly.
2. Separate facts from interpretation. Keep dated events, decisions, metrics, blockers, and asks traceable to the input.
3. Draft in this order:
   - Headline: one sentence with the most important takeaway.
   - Done today: completed work or resolved decisions.
   - In progress: active threads and current state.
   - Blockers or risks: items needing attention.
   - Next actions: concrete owner/action/date when available.
4. Keep the brief concise by default. Prefer 5-9 bullets total unless the user asks for detail.
5. Preserve sensitive wording carefully. Do not invent commitments, owners, dates, or metrics.

## Style

- Write plainly and professionally.
- Prefer active voice and concrete nouns.
- Combine duplicate updates across sources.
- Use neutral language for uncertain or unresolved items.
- If the input is mostly Chinese, draft in Chinese; if mostly English, draft in English.

## Output Shapes

Use the default daily brief format unless the user asks for a specific channel.

Default:

```markdown
**Daily Brief**
Headline: ...

Done today:
- ...

In progress:
- ...

Blockers / risks:
- ...

Next actions:
- ...
```

For Slack or chat, make it shorter and remove empty sections.

For email, add a subject line and a greeting only if the user asks for an email-ready draft.

## Reference

For stricter section rules and examples, read `references/brief-format.md`.

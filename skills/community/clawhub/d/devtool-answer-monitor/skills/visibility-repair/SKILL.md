---
name: visibility-repair
description: >
  Use when the user has a wrong, negative, outdated, or competitor-only LLM answer and needs a structured repair plan. Covers negative-type classification, source tracing, authority coverage, channel-specific repair actions, and regression checks.
---

# visibility-repair

Use this skill to turn a bad model answer into a repair backlog instead of reacting ad hoc.

## Trigger

Use this skill when an LLM answer contains any of the following:

1. factual error;
2. negative recommendation against the product;
3. outdated product description;
4. competitor-only recommendation in a strategic query.

## Outputs

| Output | Description |
|---|---|
| Problem type | one of the four negative categories |
| Repair actions | source fixes, content moves, authority pages, feedback actions |
| Regression plan | repeat checks for the affected queries |

## Next Best Skill

If the next task is to quality-check the newly repaired content, use `visibility-content-check`.

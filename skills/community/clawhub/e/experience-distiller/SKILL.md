---
name: experience-distiller
description: Distill finished work into the right OpenClaw knowledge layer. Use when a task, fix, setup, integration, cron/report workflow, repeated operation, or output-style decision has just finished and you need to decide what should be written to daily logs, the experience bank, a playbook, or a reusable skill. Triggers include requests like “沉淀一下”, “把这次经验记下来”, “应该写到哪里”, “提炼成经验”, “升级成 playbook/skill”, “这个经验记一下”, or any post-task knowledge routing decision.
---

# Experience Distiller

Route completed work into the correct knowledge layer instead of dumping everything into one file.

## Quick workflow

1. Read `references/decision-rules.md`.
2. Identify the finished task/result.
3. Separate:
   - dated facts/evidence
   - reusable action-level lessons
   - workflow-level changes
   - capability/package opportunities
4. Recommend one of:
   - daily-log
   - experience
   - playbook
   - skill
   - multi
   - no-op
7. If asked to execute, write the files directly.

## Non-negotiables

- Do not store raw noise as long-term knowledge.
- Do not force everything into a skill.
- Prefer experience-bank for tactical reusable lessons.
- Prefer playbooks for canonical multi-step workflows.
- One task may write to multiple layers when justified.

## OpenClaw default mapping

- `memory/YYYY-MM-DD.md` = dated facts and evidence
- `memory/experience-bank/entries/` = trigger-action-failure reusable lessons
- `playbooks/` = canonical workflows
- `skills/` = reusable capability packages

## Output pattern

Use a short recommendation block:
- route
- confidence
- why
- exact files to write/update
- draft content bullets

## Bundled references

- `references/decision-rules.md` — routing logic
- `references/template.md` — lightweight invocation template
- `references/examples.md` — ready-to-use examples for common task types

---
name: adaptive-skill-factory
description: Discover, install, update, or create the right skill when a workflow gap appears. Use when a task is repetitive, a role lacks a reliable procedure, an existing skill might save time, ClawHub search/install could help, or the agent should create a concise local skill for future reuse.
---

# Adaptive Skill Factory

Use this skill to keep agents sharp without bloating every prompt.

## Workflow

1. Classify the gap.
- Use no skill for one-off trivial tasks.
- Reuse a skill for repeated workflows, fragile procedures, or domain-specific tasks.
- Create a new skill only when the same gap is likely to recur.

2. Check existing skills first.
- Prefer workspace skills in `<workspace>/skills`.
- Then check shared skills loaded from configured extra skill directories.
- Reuse bundled skills when they already fit.

3. If internet and ClawHub are available, search before building.
- Search narrowly for the exact workflow.
- Install the smallest relevant skill, not a broad bundle.
- Avoid skills that overlap another role's boundary.

4. If no suitable skill exists, create a local skill.
- Put role-specific skills in `<workspace>/skills/<skill-name>`.
- Put cross-role reusable skills in `D:\internal-hub\skills`.
- Keep `SKILL.md` concise and procedural.
- Only include scripts, references, or assets when they save real effort.

5. Validate and iterate.
- Validate the skill after editing.
- Update the skill when the workflow changes or the agent struggles again.
- Delete or simplify stale skills that no longer help.

## Role discipline

- Technical skills: only for code, deployment, automation, debugging, websites, scripts.
- Intelligence skills: only for research, verification, policy, news, or competitor analysis.
- Trade skills: only for suppliers, pricing, MOQ, lead time, procurement, stocks, crypto, funds, or trading analysis.
- Supervisor skills: only for task routing, progress reporting, review, and execution oversight.

## Avoid

- Do not create skills for generic reasoning.
- Do not create skills that duplicate another role's job.
- Do not install large unrelated skill packs just because they are available.
- Do not let a skill become a dumping ground for long notes.

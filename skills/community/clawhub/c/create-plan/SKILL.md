---
name: create-plan
description: Create a concise implementation plan for coding, documentation, repository, or workflow tasks before making changes. Use when the user explicitly asks for a plan, implementation plan, PRD execution plan, rollout plan, 技术方案, 开发计划, or asks what should be done next without authorizing edits. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/work/create-plan
---

# Create Plan

## Goal

Produce one clear, actionable plan from the user's request and the available project context.

This skill is for planning only. Stay read-only unless the user separately asks for implementation.

## Inputs

Collect the smallest useful context:

- user's requested outcome
- repository or artifact path, if relevant
- current constraints from README, docs, existing code, or prior decisions
- known deadline, risk tolerance, or delivery format, if provided

If the task depends on current repository facts, inspect the likely files first. Prefer `README.md`, `docs/`, `todo.md`, package or build files, and the modules most likely to change.

## Process

1. Identify the real objective in one sentence.
2. Check the existing structure before proposing changes.
3. Separate confirmed facts from assumptions.
4. Ask at most two short questions only when planning would be risky without the answer.
5. Choose the smallest plan that can deliver the requested outcome.
6. Order the plan from discovery to change design, implementation, validation, and rollout.
7. Include explicit validation steps.
8. Surface edge cases, migration risk, data risk, or user-decision points.

## Output Format

Use this format unless the user gives a different template:

```markdown
# Plan

<1-3 sentences describing what will be done, why, and the approach.>

## Scope
- In:
- Out:

## Action Items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Open Questions
- <Question 1>
- <Question 2>
```

## Plan Quality Rules

- Make action items concrete, ordered, and verb-first.
- Mention likely files, modules, commands, or docs when useful.
- Keep the checklist short by default: 6-10 items.
- Include at least one validation item.
- Include risk or edge-case review when the change touches shared behavior, data, permissions, release flow, or user-facing output.
- Label assumptions instead of hiding them.

## Boundaries

- Do not write or edit project files while using this skill.
- Do not produce code snippets unless the user asked for design details that require them.
- Do not create a vague task list such as "update backend" or "improve frontend".
- Do not plan broad refactors unless they directly support the user's requested outcome.
- If the user is clearly asking for implementation, do not stop at a plan; implement instead unless they explicitly requested planning first.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)

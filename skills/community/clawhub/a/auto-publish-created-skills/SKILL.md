---
name: auto-publish-created-skills
description: Automatically publish newly created local skills to ClawHub after the skill has been reviewed and committed, when the user has explicitly requested ongoing ClawHub publication for assistant-created skills. Use after creating a new skill under workspace/skills and after local commit succeeds. Inspect the remote slug first, choose an initial version if absent, or bump patch if updating, then publish via the verified ClawHub publish flow.
---

# Auto Publish Created Skills

Use this skill when a new local skill has just been created by the assistant and the user wants assistant-created skills uploaded to ClawHub.

## Preconditions

Only publish if all are true:
- the user explicitly asked for assistant-created skills to be published to ClawHub
- the skill directory contains a valid `SKILL.md`
- the skill has already been locally reviewed/committed
- local ClawHub session is authenticated

## Workflow

1. Identify the new skill folder under `workspace/skills/<slug>`.
2. Check ClawHub login with `clawhub whoami`.
3. Inspect remote state with `clawhub inspect <slug>`.
4. Versioning:
   - if skill does not exist remotely: publish `0.1.0`
   - if skill exists remotely: bump patch version
5. Publish with `skills/clawhub-publish-flow/scripts/publish_to_clawhub.js`.
6. Verify with `clawhub inspect <slug>`.
7. Add or update the registry sheet if needed.

## Changelog pattern

Use short, operational changelogs such as:
- `Initial release`
- `Add runtime notes`
- `Refine trigger description`
- `Document proven workflow`

## Safety rule

Do not publish vague drafts or half-finished skills just because they were created. Publishing still requires the skill to be coherent and committed.

## Output

Report:
- skill
- version
- publish result
- final URL if available
- whether verification succeeded

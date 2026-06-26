# Release Checklist

Use this checklist before publishing or updating a skill on ClawHub.

## Before publish
- Confirm the skill solves a real repeated problem.
- Confirm `SKILL.md` description is clear about when to use the skill.
- Confirm bundled files actually exist.
- Confirm no placeholder claims remain.
- Confirm version bump matches the scope of change.
- Confirm changelog is plain and specific.

## Red flags
- README or SKILL claims code that is not present.
- package references files that do not exist.
- skill depends on credentials or APIs not documented in `SKILL.md`.
- skill publishes external side effects without clearly saying so.
- tags or display name are misleading.

## After publish
- Run `clawhub inspect <slug>`.
- Confirm latest version matches the uploaded version.
- Confirm tags look correct.
- Record the publish result in git if the workspace changed.

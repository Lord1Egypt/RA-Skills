# Virtual Team Skill Checklist

Run before declaring the team skill done. **Critical** items will break the team at runtime; **Recommended** items hurt usability or maintainability.

## Frontmatter And Discoverability (Critical)

- [ ] `name`: `a-z 0-9 -` only; no leading/trailing `-`; no `--`; ≤64 chars; **exactly matches skill root folder name**
- [ ] `description`: includes both **capability summary** and **trigger scenario**; ≤1024 chars; third-person
- [ ] `metadata.version` present (helps track skill evolution)

## Structure (Critical)

- [ ] `SKILL.md` exists at skill root
- [ ] `agents/<slug>.md` exists for **every** role declared in `references/member.md`
- [ ] `references/member.md` exists and lists **every** role with links to both spec and definition
- [ ] `references/<slug>.md` exists for every role; links from `member.md` resolve
- [ ] No role appears in `agents/` without a matching `references/`, or vice versa (dual-track invariant)

## Subagent Definitions — `agents/<slug>.md` (Critical)

For each role:

- [ ] Frontmatter contains `name`, `description`, `tools`, `model` (model may be omitted to inherit lead)
- [ ] `name` in frontmatter equals filename slug
- [ ] `tools` allowlist includes everything the role's Spawn Prompt asks the teammate to do (e.g. don't ask the role to "edit files" without `Edit` and `Write` in tools)
- [ ] Body explicitly lists **Files You Own** matching the role's Owned Paths in `references/<slug>.md`

## Role Specs — `references/<slug>.md` (Critical)

For each role, all 8 sections present:

- [ ] 1. Scope
- [ ] 2. Inputs
- [ ] 3. Outputs
- [ ] 4. Boundaries
- [ ] 5. **Spawn Prompt** — verbatim text the lead can paste; ≥3 lines of task-specific context (not just "do X"); contains placeholder slots for the lead to fill
- [ ] 6. **Owned Paths** — explicit globs, not vague descriptions
- [ ] 7. **Task Template** — 3–6 tasks with `blockedBy` edges
- [ ] 8. **Plan Approval** — boolean, with criteria if `true`

## Cross-Role Invariants (Critical — runtime correctness)

- [ ] **Owned Paths have zero cross-role overlap.** Walk every pair of roles; if two glob lists could match the same file, refactor. This is the #1 source of teammate edit collisions.
- [ ] Task Template `blockedBy` references resolve to existing tasks in other roles' templates (no dangling deps)
- [ ] Total team size is **3–5 roles**. If <3, recommend subagents instead. If >5, merge until ≤5.
- [ ] Per-role task count is **3–6**. Beyond that, coordination overhead grows; below it, the role is too small.

## SKILL.md Playbook Sections (Critical)

The SKILL.md must contain operating sections for the lead, not just team description:

- [ ] **Preflight** — Claude Code version, env var, `teammateMode` checks
- [ ] **Install Agents** — copy/symlink instructions for `.claude/agents/`
- [ ] **Bootstrap** — concrete `TeamCreate` + per-role `Agent` calls
- [ ] **Task Seeding** — `TaskCreate` examples wiring up `blockedBy`
- [ ] **Steady State** — when to message, how to handle plan approval requests
- [ ] **Teardown** — per-teammate `shutdown_request` loop, then `TeamDelete`
- [ ] **Known Limits** — at minimum: fixed lead, no `/resume`, permissions set at spawn

## Content Quality (Recommended)

- [ ] `SKILL.md` ideally <500 lines; long tables/details moved to `references/`
- [ ] Terminology is consistent across SKILL.md / agents/ / references/ (same role uses one slug everywhere)
- [ ] Collaboration principles are actionable (e.g. "outputs land in `outputs/<slug>-*.md`"), not aspirational
- [ ] Cross-role conflict resolution rule stated once in SKILL.md or `member.md`

## Hooks (If Provided)

- [ ] Each hook script is executable (`chmod +x`)
- [ ] Each hook uses exit code 2 for "block + send feedback" (per Claude Code hook spec)
- [ ] SKILL.md documents the `.claude/settings.json` snippet to wire them up
- [ ] Hooks are scoped per-team (won't fire for unrelated work in the same project)

## Documentation Links

- [ ] All `[link](path)` references resolve (no broken paths after rename/move)
- [ ] Reference depth ≤1 from `SKILL.md` (no chains like SKILL.md → ref → ref)

## Final Smoke Test (Recommended)

Before shipping, dry-run the SKILL.md with a stub task:

- [ ] Preflight commands run cleanly
- [ ] `cp agents/*.md ~/.claude/agents/` (or symlink) succeeds and files appear
- [ ] `TeamCreate` + first `Agent` spawn returns without error
- [ ] First teammate's spawn prompt produces sensible output for a trivial input
- [ ] Teardown leaves no orphaned tmux sessions (`tmux ls` if applicable)

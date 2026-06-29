---
name: family-os
description: Build and operate a privacy-preserving household information system for AI agents and assistants. 用于初始化和持续维护本地家庭工作区，管理家庭事实、计划、项目、决策、提醒、风险、复盘和长期发展路径。 Use for parenting, finance, health, career, housing, insurance, education, logistics, relationships, legal/admin tasks, household records, and "family system" workflows. The skill is generic and must store private household data only in the user's configured local workspace, never inside the skill package.
---

# Family OS

## Operating Model

Use this skill as a generic household operating system. Keep the skill package reusable and safe to publish. Store all private household information in the configured workspace only.

Resolve the workspace in this order:

1. Use a workspace path explicitly provided by the user.
2. Use `FAMILY_OS_HOME` when set.
3. Read `~/.family-os/config.yaml` when present.
4. If no workspace exists, run `scripts/family_os_init.py` to create one.

Never write household facts, names, finances, medical details, documents, or private decisions into this skill directory.

Choose workspace language in this order:

1. Use the language explicitly requested by the user.
2. Use the user's conversation language when it is clear.
3. Use the language already present in an existing workspace.
4. Use `language` from `~/.family-os/config.yaml`.
5. Use `FAMILY_OS_LANGUAGE` or system locale via `scripts/family_os_init.py --language auto`.

Keep portable directory names stable by default, but generate human-facing file headings and templates in the user's language. Prefer passing an explicit `--language <language-code>` when the user language is clear. If the initializer does not have a built-in template for the user's language, create the workspace with the closest supported template and then translate the generated headings/content in place.

## First Use

When the user asks to install, initialize, or set up Family OS:

1. Run `scripts/family_os_init.py`.
2. Pass `--workspace <path>` when the user provided a desired private workspace path.
3. Pass `--language <language-code>` when the user language is known; otherwise allow `--language auto`.
4. Use `--archive-existing` when the target workspace already contains legacy material and the user wants a clean Family OS workspace.
5. Create or update `~/.family-os/config.yaml` with the selected workspace and language.
6. Run `scripts/family_os_check.py --workspace <path>` after initialization.

Read `references/workspace-structure.md` before changing the directory structure.

## Conversation Update Workflow

When a family-related conversation contains new information:

1. Read `references/update-rules.md`.
2. Resolve the workspace.
3. Read the dashboard files first:
   - `01-dashboard/household-overview.md`
   - `01-dashboard/current-priorities.md`
   - `01-dashboard/this-month.md`
   - `01-dashboard/risks-and-reminders.md`
4. Classify the new content as facts, tasks, risks, decisions, preferences, timeline events, source material, or open questions.
5. Locate the relevant area or project. Create a project only when the work is time-bound, multi-step, or expected to last more than one week.
6. Update only the smallest relevant set of files.
7. Update the dashboard when the new information changes priorities, this month's plan, or risk posture.
8. Tell the user what changed and what the next useful action is.

Ask before writing highly sensitive data when the configured privacy mode requires confirmation, especially for identity documents, medical results, account credentials, legal disputes, exact addresses, or large asset details.

## Common Tasks

- **Initialize a workspace**: run `scripts/family_os_init.py`; use `references/templates.md` for generated file intent.
- **Check current status**: run `scripts/family_os_status.py --workspace <path>`.
- **Audit workspace health**: run `scripts/family_os_check.py --workspace <path>`.
- **Design a family development path**: read `references/development-path-framework.md`, then adapt it to the user's local facts without putting those facts into the skill.
- **Reorganize an existing household folder**: initialize with `--archive-existing`, then migrate or summarize legacy material into current files only after reading the relevant legacy files.
- **Record a decision**: use `04-decisions/YYYY-MM-DD-short-title.md` and update related project/dashboard files.
- **Record a conversation snippet or raw source**: put it in `00-inbox/` first unless the destination is obvious and low-risk.

## References

- `references/privacy-model.md`: privacy boundaries and safe-write rules.
- `references/workspace-structure.md`: canonical directories and naming.
- `references/update-rules.md`: how to classify and write new information.
- `references/workflows.md`: task-specific workflows.
- `references/development-path-framework.md`: generic household development model.
- `references/templates.md`: file templates and required dashboard files.

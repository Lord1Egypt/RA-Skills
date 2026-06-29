# Workflows

## Initialize

1. Resolve workspace path.
2. Run `scripts/family_os_init.py --workspace <path>`.
3. If importing an existing folder, include `--archive-existing`.
4. Run `scripts/family_os_check.py --workspace <path>`.
5. Report created config path, workspace path, and archive path if any.

## Record New Information

1. Read dashboard and relevant area/project.
2. Classify the new information using `update-rules.md`.
3. Write to the smallest relevant destination.
4. Update dashboard if the new information affects current priorities, month plan, or risks.
5. Respond with a brief update summary and next action.

## Create a Project

Create `03-projects/YYYY-short-name/README.md` for a time-bound effort.

Include:

- objective
- status
- owner or responsible person if known
- key dates
- decision criteria
- next actions
- log

## Record a Decision

Create `04-decisions/YYYY-MM-DD-short-title.md`.

Include:

- decision
- context
- options considered
- rationale
- risks
- follow-up tasks
- related files

## Review

Weekly review:

- refresh current priorities
- clear or route inbox items
- check overdue risks/reminders
- update active projects

Monthly review:

- update this month's plan
- summarize finances, health, parenting, career, home logistics, and open decisions as relevant
- archive completed projects

Yearly review:

- summarize household development stage
- revise family values, major goals, and long-term path

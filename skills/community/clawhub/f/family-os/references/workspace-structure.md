# Workspace Structure

Use this canonical structure for new workspaces:

```text
family-workspace/
  00-inbox/
  01-dashboard/
    household-overview.md
    current-priorities.md
    this-month.md
    risks-and-reminders.md
  02-areas/
    finance/
    parenting/
    health/
    career-and-income/
    home-and-logistics/
    housing-and-city/
    insurance/
    education/
    legal-and-admin/
    relationships/
  03-projects/
  04-decisions/
  05-memory/
    household-facts.md
    family-values.md
    preferences.md
    important-people.md
  90-reviews/
    weekly/
    monthly/
    yearly/
  99-archive/
```

## Directory Roles

- `00-inbox/`: raw material and uncertain destination.
- `01-dashboard/`: current operating view, priorities, risks, and month plan.
- `02-areas/`: long-running household domains that do not "finish".
- `03-projects/`: time-bound outcomes with a current state and next actions.
- `04-decisions/`: durable decision records with context and rationale.
- `05-memory/`: stable household facts, preferences, values, and people.
- `90-reviews/`: weekly, monthly, and yearly review notes.
- `99-archive/`: completed projects, old exports, and legacy imports.

## Language

Use the user's habitual language for human-facing workspace content.

Language selection priority:

1. Explicit user request.
2. Current conversation language.
3. Existing workspace language.
4. `~/.family-os/config.yaml`.
5. `FAMILY_OS_LANGUAGE` or system locale.
6. English fallback.

English folder names are the portable default because scripts and references can rely on them. File headings, template text, project titles, decision records, and review content should use the user's language. It is acceptable for a user workspace to use localized filenames when that improves daily use, but avoid changing canonical directory names unless the user asks for that.

The initializer includes built-in templates for Chinese, English, Japanese, Korean, Spanish, French, German, and Portuguese. For other languages, initialize with the closest supported language and translate the generated template text in place.

## Legacy Imports

When rebuilding an existing folder as a Family OS workspace, archive legacy top-level material under:

```text
99-archive/legacy-import-YYYYMMDD-HHMMSS/
```

Then create the canonical workspace files. Migrate summaries back into current files only after reading the relevant legacy material.

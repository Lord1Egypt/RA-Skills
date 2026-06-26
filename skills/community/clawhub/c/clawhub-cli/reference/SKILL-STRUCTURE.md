# Skill Package Structure (Recommended)

This is the recommended structure for a ClawHub skill folder.

```
my-skill/
  SKILL.md
  reference/
    ... deeper docs ...
  scripts/
    linux/
      ... runnable helpers (.sh) ...
    macos/
      ... OS notes / wrappers ...
    windows/
      ... README with command snippets (no .ps1) ...
  assets/
    ... icons/templates (svg/md/png*) ...
```

## `SKILL.md` (Required)

`SKILL.md` should be the **agent instruction sheet**, optimized for execution:

- when to use the skill (signals / user intent)
- guardrails (what not to do)
- preflight requirements
- common workflows with concrete commands
- troubleshooting playbook
- links to deeper docs in `reference/`

## `reference/` (Optional but Recommended)

Store longer docs that are too detailed for `SKILL.md`, such as:

- command cheat sheets
- publishing checklists
- best practices and conventions
- troubleshooting guides

## `scripts/` (Optional)

Put small automation helpers:

- shell scripts for Linux/macOS (prefer portable `bash`)
- Windows instructions as Markdown (avoid shipping `.ps1` in repos that forbid it)
- scripts should be safe by default and avoid destructive actions

## `assets/` (Optional)

Put non-code reusable assets:

- icons (prefer `svg` text-based)
- templates (markdown, json, yaml)
- screenshots (only if necessary; keep size small)

\* Avoid committing large binary files unless required.


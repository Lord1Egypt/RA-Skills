---
name: workspace-hygiene
description: Use this skill only when the user explicitly asks for a dry-run cleanup inventory, disk-space cleanup, deletion review, or recoverable archiving of generated workspace artifacts in a coding repo, such as caches, logs, test reports, screenshots, temporary databases, eval outputs, build outputs, or agent scratch files. Do not trigger just because the user says a repo is messy, asks for code review, asks for git status, wants README/docs cleaned up, requests memory cleanup, or asks for ordinary coding/testing/refactoring. If cleanup or archive/removal of workspace artifacts is not the main request, do not use this skill.
metadata:
  compatibility:
    os: [windows, macos, linux]
    requires:
      python: optional
      git: optional
---

# Workspace Hygiene

Keep this skill quiet, cheap, and user-friendly. It is for cleaning the workspace around the project, not rewriting the project.

## Default Flow

1. **Stay silent unless cleanup is explicit.** Do not interrupt normal development just because a few files exist. Mention cleanup only when the user directly asks to inventory, remove, or archive workspace artifacts, or asks to reduce disk usage from generated files.
2. **Find the workspace root.** Prefer the current repo root. Do not scan the user's home directory or sibling projects unless the user names them.
3. **Take a cheap inventory first.** If Python is available, run the read-only helper:

   ```bash
   python <skill-dir>/scripts/workspace_inventory.py --root . --summary-json --max-entries 40 --recent-hours 24
   ```

   Use `python3` if that is the local convention. If Python is unavailable, inspect manually with the same categories below.
4. **If no intervention is needed, say so briefly.** Do not produce a long report.
5. **If cleanup is useful, show a compact plan.** Group findings into:
   - safe to remove or archive
   - needs user review
   - protected or skipped
6. **Ask before changing files.** Default to a dry run. Before deletion or archiving, show the exact paths and actions.
7. **Prefer recoverable archive over delete.** Move approved files to `.codex-cleanup/archive/<timestamp>/` and write a manifest with original path, size, modified time, and action. Permanent deletion should require explicit user wording.
8. **Verify after cleanup.** Re-check git status or file inventory. Report only the meaningful result.

If the user wants recurring project-specific cleanup rules, suggest a small `.workspace-hygiene.yml` with keep/skip patterns. Do not create config files unless asked.

## Categories

Safe cleanup candidates are usually untracked or ignored generated artifacts:

- cache directories such as `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.parcel-cache`, `.turbo`, `.next/cache`, `node_modules/.cache`
- build/test outputs such as `dist`, `build`, `coverage`, `htmlcov`, `test-results`, `playwright-report`
- temporary files such as `*.tmp`, `*.bak`, `*.orig`, `*.rej`, `*.pyc`, `.coverage`, log files in obvious log/output folders
- agent/eval scratch outputs when the user confirms they are no longer needed

Needs review:

- untracked source files, docs, spreadsheets, PDFs, notebooks, archives, local databases, datasets, screenshots, reports, and anything under `data/`
- files modified recently, especially during the current task
- large files with unclear provenance

Protected or skipped:

- `.git`
- `.codex/skills` and installed skill files
- tracked files with modifications
- `.env`, private keys, token files, credential stores, and secret-looking files
- user-named keep paths

## Safety Rules

- Never delete or rewrite tracked changes unless the user explicitly asks for that exact action.
- Never clean outside the resolved workspace root.
- Never echo secret values. Report secret-looking paths only by path and category.
- Treat databases, datasets, and archives as review-required even when they look generated.
- Keep output in the user's language when possible.
- Avoid large directory listings. Show counts and the top few largest or most relevant paths.

## User-Facing Output

Use a short report by default:

```text
Workspace cleanup plan
Root: <path>
Safe candidates: <count>, <size>
Needs review: <count>, <size>
Skipped/protected: <count>

Recommended action:
- Archive safe candidates to .codex-cleanup/archive/<timestamp>/
- Review these paths before touching them: ...
```

If the user wants action, ask for one concise confirmation unless they already gave explicit approval for the exact paths and action.

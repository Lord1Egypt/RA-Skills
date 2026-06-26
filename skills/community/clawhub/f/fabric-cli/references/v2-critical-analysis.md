# V2 critical analysis and improvement notes

This note records the audit of version 1 and the design changes made for version 2.

## What v1 did well

- It identified the right core command surface: installation, auth, search, path browsing, create/save shortcuts, tasks, workspaces, `ask`, completions, subscription, and JSON output.
- It included useful safety guidance around API keys, installer consent, workspace verification, and destructive operations.
- It bundled helper scripts for environment checking and structured agent-memory notes.
- It included trigger and functional evals, which made the package more testable than a simple `SKILL.md`.
- It used progressive disclosure by moving detailed material into `references/`, `assets/`, and `evals/`.

## Main v1 risks and gaps

1. Trigger boundaries needed sharper near-miss handling. V2 adds an explicit first decision for Microsoft Fabric `fab`, Power BI/OneLake terms, Daniel Miessler's Fabric framework, Python Fabric SSH, Fabric.js, and physical fabric.
2. Some operations were too optimistic about undocumented CLI behaviour. V2 emphasises live help and avoids undocumented assumptions about JSON fields, item body retrieval, moving, deletion, tagging, and editing.
3. Consent boundaries were present but could be more operational. V2 has a dedicated operation matrix distinguishing local read-only, remote read-only, non-destructive writes, destructive writes, installation, and authentication.
4. Agent memory guidance needed stronger privacy and retrieval discipline. V2 clarifies when to retrieve and when to save, what belongs in memory, and how to tag notes consistently.
5. Evals needed more near-misses and train/validation trigger splits. V2 expands negative trigger coverage and adds evals for ambiguous Fabric requests, task IDs, installer consent, and long-note stdin handling.
6. The package benefits from a self-validator. V2 adds `scripts/validate_skill.py` to catch frontmatter issues, broken references, JSON errors, missing scripts, and overly long descriptions.
7. Multi-tag creation syntax is not fully established in the public docs. V2 avoids relying on it in primary examples and tells agents to check installed help before using multiple creation tags.

## V2 improvements applied

- Rewrote the frontmatter description to be more intent-focused and precise while staying below the 1024-character limit.
- Added a prominent "First decision" section to prevent over-triggering on adjacent Fabric meanings.
- Added `references/security-and-consent.md` for explicit safety policy.
- Added `references/workflows.md` for repeatable multi-step workflows.
- Added `references/agent-memory.md` with retrieval/save policies and tagging conventions.
- Added `scripts/fabric_help_cache.py` to inspect installed CLI help and adapt to version changes.
- Strengthened `scripts/fabric_check.py` for read-only diagnostics and wrong-CLI detection.
- Kept and improved `scripts/fabric_memory_note.py` for redaction, stdin/file support, and output structure.
- Added `scripts/fabric_command_plan.py` for shell-quoted dry-run planning.
- Added `scripts/validate_skill.py` for package validation.
- Expanded templates for memory notes, session bootstrap, search summaries, and task plans.
- Split trigger evals into train and validation files.

## Remaining limitations

- The skill cannot guarantee exact JSON field names because those are not documented in the public source page.
- Commands beyond the public docs still require live help from the installed CLI.
- Authentication and workspace access can only be fully tested in a user's configured environment.
- Automatic secret redaction is best-effort; agents should still inspect memory notes before saving.

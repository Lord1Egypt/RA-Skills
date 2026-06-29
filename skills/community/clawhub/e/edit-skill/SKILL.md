---
name: edit-skill
description: Use when asked to review, edit, tighten, shorten, deduplicate, clean up, or remove slop from an existing agent skill while preserving behavior. Use for skill files that need clearer triggering, shorter instructions, stale reference cleanup, host-compatible frontmatter, or fixes for vague, repetitive, outdated, unsupported, or hard-to-apply rules.
---

# Edit Skill

Use this for existing skill files. The job is to improve agent behavior, not to
make the prose sound nicer.

First classify the request:

- Review-only: explain what should change; do not patch files.
- Edit-in-repo: patch the skill directly and verify it.
- Unclear: default to review-only when the user asks "can this be better?" or
  "what do you think?"

## Rules

- Preserve the skill's real job, user voice, trigger intent, and hard safety boundaries.
- Preserve paths, commands, output contracts, examples that teach subtle judgment,
  and repeated-failure fixes.
- Keep rules that are observable, testable, or tied to repeated failures.
- Cut duplicate instructions, stale tool references, unsupported metadata, vague
  quality claims, decorative prose, and filler.
- Replace abstract rules with concrete agent behavior, commands, or output shapes.
- Keep frontmatter compatible with the target host. For Codex-style skills, put
  trigger phrases in `description`; do not add unsupported top-level keys such
  as `triggers`.
- Move rare detail into a referenced file only when that host supports bundled
  references.
- Do not add new capabilities unless the user explicitly asks.
- Do not rewrite deliberate weirdness into generic assistant prose.

## Pass Order

1. Identify what the skill is for and when it should trigger.
2. Mark must-keep rules: safety, scope, file paths, output contracts, and known failure fixes.
3. Check whether frontmatter is routing-friendly and compatible with the target host.
4. Remove repeated rules that say the same thing in different words.
5. Replace vague rules with concrete behavior.
6. Verify referenced files, scripts, paths, commands, and examples still exist when editing in repo.
7. Return a short change summary, verification performed, and remaining risk.

## Output

For a review-only request, return:

- `Keep:` rules that must stay.
- `Cut:` duplicate, stale, or vague rules to remove.
- `Tightened version:` the edited skill text, or `Patch:` when a diff is clearer.
- `Risk:` what behavior might change.

For an edit-in-repo request, patch the skill file directly, then report the
changed file, verification performed, and remaining risk.

## Credit

Packaged from a local skill-editing workflow, with public inspiration credited
to @petergyang per the original request.

## Anti-Patterns

- Do not make every skill tiny if it loses necessary behavior.
- Do not remove examples that teach a subtle judgment.
- Do not turn a voice-specific skill into generic corporate copy.
- Do not keep a rule just because it sounds important.
- Do not preserve unsupported metadata just because it might help routing.
- Do not add memory, evals, scripts, or references unless they will actually be read or run.

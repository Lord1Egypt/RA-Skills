---
name: bilingual-mail-translator
description: Build or improve a bilingual email translation and notification workflow that converts raw emails into Chinese-friendly bilingual output. Use when designing prompt-driven email formatting, subject/date/body bilingual rendering, recipient truncation, quoted-history summarization, duplicate-line suppression, signature handling, or reusable translation contracts for mail assistants and inbox notifications.
---

# Bilingual Mail Translator

Use this skill when building, refining, or publishing a bilingual email translation workflow.

## What this skill owns

This skill defines the prompt-layer contract for turning raw emails into user-facing bilingual notification text.

Keep these responsibilities in the model/prompt layer unless there is a deliberate product change:
- subject translation and bilingual display
- date normalization and display
- body bilingual formatting
- recipient truncation when there are more than 3 recipients
- quoted/history mail summarization
- duplicate-line suppression when translation equals original
- signature block formatting

Program side should stay focused on:
- extracting raw mail
- normalizing input headers before prompt assembly
- calling a lightweight worker or LLM runtime
- extracting output text
- fallback to raw mail when model output fails

## Reference implementation pattern

Example primary script:
- `scripts/mail_translate.py`

Example runtime path:
1. a watcher, inbox poller, or notifier prepares raw mail
2. a translation script builds the mail prompt
3. a lightweight worker agent or LLM runtime runs the translation
4. postprocess stays pass-through for formatting
5. final text is delivered to the user

## Required contract files

Read `references/contracts.md` first, then open the underlying source docs it points to when needed.

## Change workflow

1. Read the current prompt contract documents.
2. Update the translation prompt or prompt assembly only where the contract needs to change.
3. Keep formatting decisions in prompt, not in postprocess.
4. Update regression tests for prompt contract assertions.
5. Run representative tests for the prompt contract.
6. For meaningful prompt changes, run one or more real sample mails through the translation entrypoint.
7. Compare actual output against the current accepted product direction.
8. Update the contract docs if the accepted behavior changed.

## Accepted current product direction

- Keep bilingual output when the product goal includes language-learning support, source-text transparency, or side-by-side review.
- Preserve channel-specific indentation or spacing behavior only when a downstream renderer requires it.
- If translation equals original, keep only the original line.
- If recipients exceed 3, show the first 3 only and end directly with `...`.
- If quoted/reply history exists, keep the current mail as focus and summarize history below using a clear section label such as `历史邮件摘要：`.
- Keep signature formatting readable, but do not let signature cleanup override the general duplicate-suppression rule.
- Do not reintroduce formatting heuristics into postprocess.

## References

- Contract summary and public design notes: `references/contracts.md`
- Generic command checklist: `references/commands.md`

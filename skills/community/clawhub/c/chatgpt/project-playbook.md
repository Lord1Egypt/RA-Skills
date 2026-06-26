# ChatGPT Project Playbook

Use Projects when work needs shared files, repeat turns, and a durable brief.

## Minimum Project Contract

Keep these five pieces visible:

1. Project objective
2. Current source of truth
3. Output format rules
4. Decision log
5. Open questions

If one is missing, the project will drift.

## Recommended Workflow

- Start with a project charter prompt that defines objective, audience, constraints, and success criteria.
- Upload only the files needed for the current milestone.
- Name the authoritative file or note when multiple drafts exist.
- End each meaningful session with a short decision log and next-step prompt.
- If the project scope changes, rewrite the charter instead of stacking exceptions.

## Session End Prompt

```text
Summarize what changed in this project today.
List confirmed decisions, unresolved questions, and the next best prompt to continue tomorrow.
```

## File Hygiene

- Remove or clearly label obsolete drafts.
- Avoid near-duplicate filenames that differ only by version suffixes.
- Tell ChatGPT which file wins if two sources disagree.
- Re-upload a corrected file instead of assuming the model will infer which revision is current.

## When to Leave a Project

Move back to a normal chat when:
- the task is now a one-off question,
- the shared files are no longer needed,
- or the project history is causing stale assumptions.

Projects are for continuity, not for every conversation.

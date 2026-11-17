---
name: asd-ste100
description: >
  Apply ASD-STE100 Simplified Technical English to written instructions: one
  action per sentence, imperative mood, condition first, one name per item,
  short sentences, no semicolons. Use before writing or when auditing prompts,
  AGENTS.md, SKILL.md, READMEs, runbooks, checklists, and the technical steps of
  an article. For articles, enforce structure only and keep the essay voice;
  never flatten narrative prose. Report contradictions between rule files
  instead of silently choosing one.
metadata:
  source-article: "https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261019-ste100-agent-instructions.md"
---

# ASD-STE100 — Simplified Technical English for Instructions

ASD-STE100 is a controlled language built for aircraft maintenance manuals. Its value here is not the 875-word dictionary. It is the discipline: an agent cannot ask a follow-up question, so every instruction must survive being read once, literally, at 2am.

This skill applies that discipline to text an agent must obey or parse.

Companion article: [The Rules, Not the Words: ASD-STE100 for Agent Instructions](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/261019-ste100-agent-instructions.md).

## Scope

| Text | Mode |
|---|---|
| Prompts, `AGENTS.md`, `SKILL.md`, READMEs, runbooks, checklists, commit-message bodies | **Full**: vocabulary discipline and structure |
| Technical steps, commands, conditions, tables, and claims inside an article | **Structure only**: one action, condition first, one name per item, no semicolons |
| Article narrative, essays, marketing copy, personal voice | **Out of scope**: do not rewrite |
| Chinese (`-zh-hans.md`, `-zh-hant.md`) | **Structural advice only**: no vocabulary enforcement; the standard defines English |

When in doubt about a sentence, ask whether the reader is expected to **do** something. If yes, it is a procedure. If no, it is a description, and only the descriptive limits apply.

## The ten rules that carry most of the work

Rule numbers refer to ASD-STE100 Issue 9. The full set of 53 is in `references/rules.md`.

1. **One action per sentence** (Rule 5.2). Split sequential steps. Keep simultaneous actions together: "Remove and discard the seal."
2. **Imperative mood** (Rule 5.3). "Run the linter", not "the linter should be run".
3. **Condition first, then a comma** (Rule 5.4). "If the check fails, read the log."
4. **20 words for a procedure, 25 for a description** (Rules 5.1, 6.3). Divide the sentence. Never delete a condition to fit the limit.
5. **One name for one thing** (Rules 1.11, 9.4). Pick `OpenCode` or `opencode` and never rotate synonyms for variety.
6. **Active voice** (Rule 3.6). Simple tenses only (Rule 3.2).
7. **Keep articles and words** (Rules 4.2, 4.5). Telegraphese is not brevity. It is ambiguity.
8. **Verb, not noun** (Rule 3.7). "Install the filter", not "perform the installation of the filter".
9. **No semicolons** (Rule 8.1). Write two sentences.
10. **Notes inform. They never instruct** (Rule 5.5). Safety labels are fixed: warning = injury or death, caution = damage to objects (Rules 7.1–7.3).

Local adaptation, not part of the standard: count a code span, path, or identifier as one word. The standard has no concept of `code`.

## Procedure — write mode (before drafting)

1. Classify the text: procedure, description, or essay.
2. For a procedure, write one action per sentence in the imperative. Put the condition first.
3. Name each file, command, and concept once. Keep technical names verbatim: paths, identifiers, API names.
4. Add rationale as description, not as a second instruction in the same sentence.
5. Run the linter (below). Fix errors. Keep advisory findings only with a stated reason.
6. For an article, apply steps 2–4 to technical steps, commands, conditions, and tables only. Leave the narrative voice alone.

## Procedure — audit mode

1. **Confirm the targets.** Edit nothing yet. Never edit generated files (`ai-thoughts/README.md`, `README_zh.md`, `PORTFOLIO.md`). Audit their sources instead (`articles.yaml`, `scripts/portfolio_template.md`).
2. **Run the linter** on every target.
3. **Classify each finding:** error, advisory, or false positive.
4. **Check terminology across files:** one name per item. Flag `OpenCode`/`opencode`, `skill`/`SKILL.md`, and any command spelled two ways.
5. **Check claims across files.** Look for a rule that says "always" in one file and "never" in another. Look for a permission described as blocked but allowed in `opencode.jsonc`. Look for a stat that no longer matches the repo.
6. **Report only.** Use the output contract below. Apply edits only after explicit approval.

## Raise hands — contradiction rules

Stop and report when any of these appear. Do not pick a side, and do not average the two:

- The same term carries two meanings, or two names name one thing.
- Two rules have incompatible scopes ("every file" vs "only `docs/`").
- An always-on rule conflicts with a project rule.
- A generated file disagrees with its source of truth.
- A documented permission or command disagrees with the actual config.
- A requirement conflicts with a scope boundary already agreed (for example, applying vocabulary rules to essays).

State the conflict in one sentence, cite both locations, and propose the smallest resolution. Wait for a decision.

## Linter

Run these commands from the `ai-thoughts` repo root:

```bash
python3 .opencode/skills/asd-ste100/scripts/ste_lint.py PATH...
python3 .opencode/skills/asd-ste100/scripts/ste_lint.py --check PATH...
python3 .opencode/skills/asd-ste100/scripts/ste_lint.py --stats PATH...
python3 .opencode/skills/asd-ste100/scripts/ste_lint.py --json PATH...
```

It reports:

- sentences over 25 words (error) and over 20 words (warning)
- semicolons outside code
- non-approved common words, with a replacement
- advisory passive voice and phrasal verbs

It does **not** check meaning, one-instruction-per-sentence, synonym drift, or whether a rewrite preserved a condition. Those stay with the reader.

Counts exclude fenced code, inline code, URLs, table rows, and headings. A code span counts as one word.

`--stats` prints one summary row per file: sentences, over 20 words, over 25 words, semicolons, errors, warnings. `--json` prints the findings as JSON for another tool.

One blind spot: a sentence that ends in a bare URL merges with the next sentence. The URL token consumes the full stop, so the two sentences count as one and can raise a false long-sentence finding. End the sentence with a word, or put the URL on its own line.

In article mode, treat semicolon and vocabulary findings in narrative prose as advisory. The structural rules still apply to steps, commands, conditions, and tables.

## Output contracts

- **Audit:** a table of `file:line`, rule, issue, proposed fix, severity. No edits.
- **Rewrite:** before/after per sentence, with the rule number that forced the change.
- **Write:** the finished text plus the linter summary and any advisory findings you chose to keep.
- **Contradiction:** both locations, one-sentence conflict statement, smallest proposed resolution, then stop.

## Verification

- No semicolon outside code.
- Every instruction sentence is 20 words or fewer. Every description is 25 or fewer.
- Each item has one name across the file.
- No condition, exception, or scope qualifier was deleted to meet a count.
- Generated files are untouched.
- Contradictions are listed, not silently resolved.

## References

- `references/rules.md` — condensed 53-rule summary, grouped by section, plus common substitutions.
- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [Issue 9 PDF](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) — authoritative text, free to download.

This skill summarizes the rules for practical use. It does not reproduce the standard or its 875-word dictionary. ASD restricts reproduction. For certified documentation, use the official standard.

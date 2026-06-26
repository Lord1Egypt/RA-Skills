---
name: chinese-copywriting-guidelines-full
description: Apply the complete Chinese Copywriting Guidelines with full upstream content bundled locally. Use when reviewing or rewriting Chinese copy in Markdown, docs, PR text, UI copy, announcements, or mixed Chinese-English technical writing and the user wants full-rule compliance rather than a simplified subset.
---

# Chinese Copywriting Guidelines Full

## Overview

Use the full upstream guideline set to review, rewrite, and explain Chinese copy edits.
Prioritize the original repository rules and examples over condensed summaries.

## Load Strategy

1. Load `references/source-info.md` to confirm upstream source and commit.
2. Load `references/upstream-text/README.md` as the primary Chinese rule source.
3. Load `references/upstream-text/README.en.md` when user asks for English explanation.
4. Load `references/upstream-text/CHANGELOG.md` when user asks about rule history.
5. Load `references/upstream-text/LICENSE.txt` when user asks about license terms.

## Workflow

1. Parse user goal: review-only, full rewrite, or rule explanation.
2. Apply full upstream rules in this order:
 - spacing
 - punctuation
 - fullwidth and halfwidth forms
 - proper nouns and abbreviations
 - optional disputed preferences only if requested
3. Preserve meaning, facts, code, commands, URLs, and identifiers.
4. Return revised content and a concise change log mapped to rule categories.

## Output Format

For rewrite tasks, return:

1. `Revised`: full updated text.
2. `Changes`: short bullets grouped by rule type.
3. `Notes`: optional ambiguity or style tradeoffs.

For review-only tasks, return:

1. `Issues`: each issue with original snippet and suggested fix.
2. `Summary`: total issues by category.

## Boundaries

1. Do not invent brand casing when uncertain; flag uncertainty.
2. Do not enforce optional disputed preferences unless user requests strict mode.
3. Do not fabricate rules not present in upstream content.
4. Do not remove user-intended tone unless user asks for tone adjustment.

## Bundled Source

This skill bundles a text-only upstream snapshot for ClawHub upload compatibility:

1. `references/upstream-text/README.md`
2. `references/upstream-text/README.en.md`
3. `references/upstream-text/CHANGELOG.md`
4. `references/upstream-text/LICENSE.txt`
5. `references/upstream-text/package.json.txt`
6. `references/upstream-text/Gruntfile.coffee.txt`
7. `references/upstream-text/gitignore.txt`
8. `references/upstream-text/github-FUNDING.yml.txt`

Source repository: `https://github.com/mzlogin/chinese-copywriting-guidelines` (CC BY-SA 4.0).

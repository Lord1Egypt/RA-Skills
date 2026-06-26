# Source Audit Prompt

Use this prompt after intake and before any layer building.

## Goal

Classify each source by reliability and by which layer it can support.

## For Each Source

Record:

- source type
- reliability label: official, quoted_text, fandom_wiki, user_summary
- whether it can support canon directly
- whether it only supports persona inference
- whether it is mainly useful for style examples

## Rules

- do not convert low-confidence summaries into canon
- keep conflicting sources visible
- mark ambiguous or hedged wording for review
- preserve direct quote fragments when they help style extraction

## Output

Produce a compact audit block with:

- source list
- reliability label per source
- canon-safe sources
- persona-only sources
- style-rich sources
- review flags

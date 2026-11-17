# Decision records (ADR)

Record "what was decided, why, and which alternatives were rejected". This is not the same as a plan — an ADR is about the decision and its reasoning; a plan is about tasks and progress.

## Conventions (checked by `governance.py check index/refs/cascade`)

File name `NNNN-short-english-phrase.md` (`ADR-NNNN-short-english-phrase.md` is also recognised), numbered sequentially with no gaps. **It starts with standard frontmatter** (a field set proven across hundreds of ADRs):

```markdown
---
id: ADR-0001
title: One sentence stating what was decided
type: decision            # decision | memo | postmortem | contrastive-analysis
domain: prod              # defined per project; keep it consistent within a project
visibility: internal      # public | internal | confidential
status: accepted          # draft | accepted | deprecated | superseded
date: 2026-09-07
# Relation fields (optional; values may be comma-separated):
# supersedes / superseded_by / supersedes_partially / derives_from / extends / related
---

# ADR-0001: One sentence stating what was decided

> **Context**: why this needs deciding now. Prose details go here —
> frontmatter only holds the enums and relations a machine reads; the two don't conflict.
```

⚠️ `status` is **an enum, not prose**. Write "approved (by the owner on some date), pending implementation" and the machine can't tell
whether the decision is still in force — put that sentence in the body's context block and write `accepted` in the frontmatter.
With `status: superseded` you **must** write `superseded_by`: saying it's void without saying what replaced it leaves the reader nowhere to go.

⚠️ **The first heading of the body must be `# ADR-NNNN`** (followed by a colon and the title). Without the number in the heading, once the file is copied or renamed
nobody can tell which record it is. The text after `#` in the example above is a YAML comment; copying it over doesn't affect validation.

⚠️ **Put the allowed `domain` values in `adr_domains` in `.doc-governance.json`**, otherwise domains aren't checked —
`domain: prd` (missing an "o") raises no error, and the record silently disappears when you filter decisions by domain.
Don't invent relation field names either: `derives` is not `derives_from`, and a misspelled key is silently ignored.

⚠️ When you declare `superseded_by: ADR-NNNN`, **the other record must point back** with `supersedes` (or `supersedes_partially`).
A one-way declaration makes people think the old record is still in force.

Suggested body: **Context** (why decide now) → **Alternatives** (each with its strengths and the reason it was rejected) → **Decision** → **Consequences** → **Approaches not taken**.

## Cascade memo (required for any decision that routes changes to other documents)

List every document the decision requires changing, one item per line, **each with a verifiable link**:

```markdown
## Cascade memo (verify every item has landed)

- ✅ **[Some doc](../path/to/doc.md)**: update block added (YYYY-MM-DD)
- ⏸ **`some-file`**: not changing yet — say why; "deliberately deferred" and "forgotten" must be distinguishable
```

⚠️ `✅` items are checked by machine: the target file must actually contain `ADR-NNNN`, otherwise it reports "claims to have landed but didn't".
`⏸` items must state a reason, otherwise three months later nobody knows whether it was deferred on purpose or forgotten.

**Where this section comes from**: a large project learned the same lesson three times — every time, it took the user asking "did this land in the plan?" to discover the routes never landed.

## Index

| ADR | Decision |
|---|---|
| — | (add a row here for every new decision — a decision missing from the index is one nobody can find) |

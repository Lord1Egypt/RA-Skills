---
name: dexio-wiki-conflicts
description: "Handle contradictions and outdated claims in an LLM wiki without silently overwriting: compare dates, provenance and the current system of record, replace only when one side is clearly authoritative, otherwise keep both claims side by side, mark the page contested or lower its confidence, and escalate material conflicts to a person. Use when a new source disagrees with a page, when two pages disagree, or when a fact on a page may no longer be true."
license: MIT
metadata:
  author: dexio
  version: "1.0.0"
---

# Resolve conflicts in a wiki

The costliest wiki error is not a missing fact but a wrong one that looks settled. It usually
arrives as a quiet overwrite: a newer source, or a newer agent, replaces a claim without
checking whether the old one was better sourced. The next agent cites the new line, and the
error compounds.

## Decide which case you are in

1. **Superseded.** The old claim was true then and something changed: a price moved, a
   decision was reversed, a person changed roles. Replace the claim, keep a dated line of what
   it replaced when the history matters ("Was $8 until 2026-09-01"), and cite the new source.
2. **Corrected.** The old claim was wrong. Replace it, cite the evidence, and say in the
   change note that it was a correction and what was wrong. Search the wiki for other pages
   that repeated the wrong claim and fix them too.
3. **Unresolved.** Two sources disagree and neither is clearly authoritative. Keep both
   (format below), mark the page, and escalate if it matters.
4. **Not a conflict.** Different scopes, dates or definitions ("users" versus "paying users").
   Make the difference explicit on the page so the next reader does not see a conflict.

## How to judge authority

In rough order:

1. The system of record, checked now: the live config, the contract, the account, the
   person who decided.
2. A primary source: the organization's own filing, docs or data, dated.
3. A careful secondary source that shows its method.
4. Vendor claims about themselves, self-reports, and aggregators.
5. Anything recalled rather than read.

Newer beats older only within the same tier. A dated primary source beats a newer blog post
that does not cite one.

## Recording an unresolved conflict

On the page, next to the claim:

```markdown
Monthly active users: disputed.
- 24,700 (company blog, 2026-08-14, vendor-sourced)
- about 9,000 (third-party panel estimate, 2026-09-02; counts web only)
Not resolved as of 2026-09-28; the panel cannot see API usage.
```

In the frontmatter, set `contested: true` and lower `confidence` if the page carries one.
When it is resolved, remove the flag, keep the winning claim with its source, and say in the
note what settled it.

## Escalate

Escalate to a person, rather than choosing, when the conflict bears on a decision, money, a
commitment to someone outside, or a claim other pages rely on. Say what conflicts, the
sources on each side, which you think is right and why, and what would settle it.

## Stale claims

A claim can be wrong without any contradicting source: it was simply true a year ago. When
you find one (from `wiki-lint`'s stale list or while reading), recheck it at the source.
If it holds, bump `updated` and note that you rechecked it. If you cannot recheck it now,
add a `stale_after` date or an inline "as of" date so readers know how old it is.

## Pitfalls

- Resolving by recency alone.
- Deleting the losing claim without a trace. History keeps it, but the next reader will not
  look at history; one dated line saves them re-adding it.
- Fixing one page and leaving the claim on the three pages that copied it. Search for it.

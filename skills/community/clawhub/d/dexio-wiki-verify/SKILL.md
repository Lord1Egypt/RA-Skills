---
name: dexio-wiki-verify
description: "Fact-check an LLM wiki against its own sources: pick the pages where an error would do the most harm, pull out the checkable claims, open each cited source and mark every claim supported, outdated, unsupported, unsourced or unreachable, then correct the page and every page that copied the claim. Use on a schedule, before a decision relies on a page, after a large ingest, or when a page's claims are in doubt."
license: MIT
metadata:
  author: dexio
  version: "1.1.0"
---

# Verify a wiki

The known weakness of an LLM wiki is that a wrong claim gets written in once and then cited:
it stops looking like model output and becomes a line other pages build on. Linting finds
broken structure. Verifying finds wrong content, by going back to the sources.

Verification is sampling, not a full audit. A run checks a handful of pages well rather than
the whole wiki badly.

## Pick what to check

Folder wiki: `python3 <wiki-lint skill>/scripts/wiki_lint.py <wiki> --verify-queue 10` ranks
pages by how many pages link to them, how long since anyone checked them, and whether they
cite nothing, are contested, have low confidence, or record a decision. Hosted wiki: rank the
same way from the page list and each page's links in.

Also check, whatever the ranking says:

- the page a decision is about to rely on
- pages written in a large ingest or by a new agent
- any page someone has questioned

Default run: three to five pages, or about twenty claims.

## Steps

1. **Pull out checkable claims.** Numbers, dates, names, quotes, prices, "X does Y"
   statements, and anything stated as a finding. Skip opinions that are marked as opinions.
2. **Open each claim's source.** The raw file, the URL, the page it was derived from. Read the
   part that should support it. If the page gives one source list for everything, find which
   source carries which claim.
3. **Mark each claim** with one of:
   - *supported*: the source says it, in substance.
   - *outdated*: the source, or a newer primary source, now says something else.
   - *unsupported*: the source does not say it, or says something weaker.
   - *unsourced*: nothing is cited.
   - *unreachable*: the link is dead or paywalled. Try an archived copy (web.archive.org)
     before giving up.
4. **Fix the page.**
   - Outdated: update the claim with the new source and date (`wiki-conflicts`, superseded).
   - Unsupported because the source says something different: the page was wrong. Correct it
     to what the source says, cite it, and keep a dated line of the old value ("corrected
     2026-09-28, was $15") (`wiki-conflicts`, corrected).
   - Unsupported because the source says less: weaken the claim to what the source does say.
     If you cannot settle it, label it `(unverified)` and lower `confidence`, adding the
     field if the page has none (`medium` for one weak source, `low` for none).
   - Unsourced: find a source and cite it, or label the claim `(unverified)`.
   - Unreachable: note it inline ("source offline as of 2026-09-28") so the next check
     does not repeat the search.
   - Supported, but only as a company's claim about itself: add `(vendor-sourced)` if the
     label is missing.
5. **Find the copies.** Search the wiki for every corrected claim (the number, the name, the
   key phrase). Fix each page that repeated it. This is the step that stops the error
   compounding.
6. **Record the check.** Set `verified: YYYY-MM-DD` on each page whose checkable claims you
   all checked that day. It means "checked, and the labels on this page show the result",
   so a page can carry it with claims still labelled `(unverified)`. Do not set it on a page
   you only sampled or only fixed a copy on. Leave a change note listing what you
   corrected: the commit message in git, the `note` field on a hosted wiki. A plain folder
   has no history, so there the dated correction lines on the page are the record.
7. **Report**: pages checked, claims checked, how many in each category, corrections made,
   anything that needs a person (a disputed decision, a claim you could not settle), and
   whether a second checker was used.

## Use a second pair of eyes

A model checking its own synthesis tends to agree with it. Where you can, give each claim and
its source, without the rest of the page, to a separate agent or a different model and ask
only "does this source support this claim?". Disagreements between the two are the claims to
look at closely. If you cannot, the check still counts, but say in the report that every
classification is one model's judgment.

## Pitfalls

- Checking that a source exists instead of reading what it says.
- Accepting a secondary source's paraphrase of a primary one you could open directly.
- Treating a vendor's claim about itself as verified because the vendor's page says it. It
  is *supported* as a vendor claim; keep the vendor-sourced label.
- Fixing the page you checked and leaving the claim on the pages that copied it.
- Marking a page `verified` after spot-checking two claims.

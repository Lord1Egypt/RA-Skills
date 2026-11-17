---
name: dexio-wiki-ingest
description: "Compile a source (article, paper, transcript, meeting notes, doc, dataset) into an LLM wiki with provenance: keep an immutable raw copy with a hash, update every existing page the source touches instead of writing one summary page, cite the source at each claim, and label how far each claim can be trusted. Use when adding a new source to a wiki or when asked to read something and add it to the wiki."
license: MIT
metadata:
  author: dexio
  version: "1.0.0"
---

# Ingest a source

Ingesting is where a wiki compounds or rots. Done well, one source updates the ten pages it
bears on and every claim can be traced back to it. Done badly, it adds one more summary page
that repeats the source, links to nothing, and hardens an unchecked claim into a "fact" that
later pages cite.

## Steps

1. **Keep the raw copy.** Save the source as markdown under `raw/` (for example
   `raw/articles/2026-09-28-vendor-pricing-update.md`) with this frontmatter:

   ```yaml
   ---
   source_url: https://example.com/post
   ingested: YYYY-MM-DD
   sha256: <hex digest of the body after the closing --->
   ---
   ```

   Compute the hash over the body only (`python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read().split(b'\n---\n',1)[1]).hexdigest())" file.md`,
   or hash the text before you add frontmatter). Before saving, search `raw/` for the same
   hash or URL. Same hash: already ingested, stop. Same URL, new hash: the source changed;
   save the new version beside the old one and note what changed. Never edit a raw file
   after ingestion.
2. **Orient** (`wiki-orient`) on the source's main subjects.
3. **List the claims** the source makes that matter to this wiki. For each, note whether it
   is new, confirms a page, updates a page, or contradicts a page.
4. **Update the pages the claims belong on** (`wiki-record`, steps 3 to 7). One source often
   touches many pages: the entity it is about, the concepts it uses, a comparison it changes,
   a decision it bears on. Cite the raw file or URL at each claim.
5. **Label trust** as you write, in the sentence that makes the claim:
   - *vendor-sourced*: a company's claim about itself (pricing, user counts, benchmarks).
   - *self-reported*: an individual's claim about their own results.
   - *unverified*: anything you recalled rather than read in this source.
   - *estimate*: a figure the source or you derived rather than measured.
   - The sampling frame, for any rate or percentage: who was counted, and who could not have
     been. "4 of 21 founders on the list" means nothing without what the list selected on.
6. **Handle contradictions** with `wiki-conflicts`. Never let a newer source silently
   overwrite an older claim unless it is clearly the more authoritative record.
7. **Write a summary page only if the source is itself a subject**: a landmark paper, a
   decision memo, a meeting that set direction. Otherwise the updated pages are the summary.
8. **Leave one change note per page** naming the source, and tell the person which pages
   changed.

## Batches

For many sources, ingest one at a time and finish each before the next. Parallel ingestion by
several agents collides on the same shared pages; if you must parallelize, split the batch by
subject so no two agents touch the same page, and follow `wiki-shared`.

## Pitfalls

- A summary page per source with nothing else changed. That is a document folder with extra
  steps; the value of the pattern is that existing pages get better.
- Dropping the provenance during synthesis. A claim with no source attached will be repeated
  by the next agent as settled fact.
- Quoting a vendor's number without the label. Vendor figures are hypotheses until checked
  against something the vendor does not control.
- Ingesting what should stay out: secrets, private data, or content under terms that forbid
  copying. Summarize and link instead of storing the full text when in doubt.

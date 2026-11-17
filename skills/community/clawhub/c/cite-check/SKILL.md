---
name: cite-check
description: Confirm every citation in a draft is real before it ships — extract each URL and arXiv ID and fetch it to prove it resolves (phase 1), then optionally check the source actually backs the claim next to it via a local NLI model (phase 2). Exit non-zero on any failure so it drops into a publish pipeline as a blocking gate.
version: 0.1.0
homepage: https://workloft.ai/labs
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      bins:
        - python3
---

# cite-check

Agents fabricate citations — a plausible-looking link or an arXiv ID that does
not exist, dropped into otherwise good copy that nobody checks. A rule a human
has to remember ("verify every URL") is not a guard. This is the guard.

Two phases:
- **Phase 1** (`{baseDir}/cite_check.py`) — the *resolve* check. Is the source real?
- **Phase 2** (`{baseDir}/claim_check.py`) — the *support* check. Does the source
  actually back the claim beside it? Catches misattribution.

Phase 1 needs only `httpx` (`pip install httpx`). Phase 2 additionally needs
`beautifulsoup4`, `pymupdf`, and a local NLI cross-encoder (via
`sentence-transformers`/`transformers`) — heavier, first run downloads the model.

## When to use this

Run it as a blocking gate before publishing anything with citations — a research
note, a post, an email. Phase 1 catches dead links and fabricated arXiv IDs;
phase 2 catches a real source cited for something it never says.

## How to use it

### Phase 1 — do the citations resolve?

```
python3 {baseDir}/cite_check.py draft.md          # check a file
cat draft.md | python3 {baseDir}/cite_check.py     # stdin
python3 {baseDir}/cite_check.py draft.md --json    # machine-readable
python3 {baseDir}/cite_check.py draft.md --strict  # also fail if NO citations
```

Exit `0` when every citation resolves, `1` when any fail — drops into a pipeline:

```
python3 {baseDir}/cite_check.py "$DRAFT" || { echo "unverified citation"; exit 1; }
```

URLs: HEAD then streamed-GET fallback, status < 400 passes, redirects followed.
arXiv IDs: looked up against the official arXiv API (an `abs/<id>` page can 200
for a non-existent paper), so a fabricated ID fails.

### Phase 2 — does each source back its claim?

```
python3 {baseDir}/claim_check.py draft.md
python3 {baseDir}/claim_check.py draft.md --json
```

Decomposes the draft into (claim, citation) pairs, fetches the real source text
(arXiv full text/abstract; HTML via BeautifulSoup; PDF via pymupdf), scores
claim-vs-source with a local NLI cross-encoder. Verdicts: SUPPORTED / PARTLY /
UNSUPPORTED / UNVERIFIABLE. Exit `1` if anything is not SUPPORTED. Swap the model
with `CITE_CHECK_NLI_MODEL`.

## Notes for the agent

- Reference the scripts as `{baseDir}/cite_check.py` / `{baseDir}/claim_check.py`.
- Phase 1 is fast and light; run it always. Phase 2 is heavier (model load) —
  use it when misattribution matters.
- PARTLY / UNVERIFIABLE are "a human should read this", not hard fails.
- Built by Workloft (https://workloft.ai/labs).

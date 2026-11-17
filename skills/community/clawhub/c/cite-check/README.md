# cite-check

Confirm every citation in a draft is real before it ships.

`cite-check` reads a draft (a Note, a post, an email, anything), pulls out every
URL and arXiv ID, and fetches each one to confirm it actually exists. A draft
that cites a dead link or a fabricated arXiv ID fails the gate, so it never
reaches publish.

There are two halves:

- **Phase 1 (`cite-check`)** — the *resolve* check. Is this source real?
- **Phase 2 (`cite-check-claims`)** — the *support* check. Does this source
  actually back the claim next to it? Catches misattribution: a real paper
  cited for something it never says.

## Why

Agents fabricate citations. They produce a plausible-looking link or an
arXiv ID that does not exist, drop it into otherwise good copy, and nobody
checks. We had a rule about it ("verify every URL", "never fabricate
identifiers") but no automated enforcement. A rule a human has to remember is
not a guard. This is the guard.

## Usage

```
cite-check draft.md            # check a file
cat draft.md | cite-check       # check stdin
cite-check draft.md --json      # machine-readable report
cite-check draft.md --quiet     # only print failures
cite-check draft.md --strict    # also fail if there are NO citations
```

Exit code is `0` when every citation resolves and `1` when any fail, so it
drops straight into a publish pipeline as a blocking gate:

```
cite-check "$DRAFT" || { echo "unverified citation, refusing to publish"; exit 1; }
```

## What it checks

- **URLs** — HEAD request, falling back to a streamed GET when the server
  refuses HEAD (many do). Status under 400 is a pass. Redirects are followed.
- **arXiv IDs** — looked up against the official arXiv API, not a plain page
  fetch, because `arxiv.org/abs/<id>` can return 200 for a non-existent paper.
  A fabricated ID returns a feed with no matching entry, which fails.

## Phase 2: claim-support check

```
cite-check-claims draft.md          # does each source back its claim?
cite-check-claims draft.md --json
```

Pipeline per cited claim: decompose the draft into atomic (claim, citation)
pairs, fetch the real source text (arXiv via ar5iv full text or abstract; HTML
via BeautifulSoup; PDF via pymupdf), then score claim-vs-source with a local NLI
cross-encoder. Output is four-shade: **SUPPORTED** (auto-pass), **PARTLY**
(weak entailment, human review), **UNSUPPORTED**, **UNVERIFIABLE** (source could
not be read). Exit code 1 if anything is not SUPPORTED.

Engine note: a 7B grounded fact-checker (Bespoke-MiniCheck) is more accurate but
runs at ~200s per call on a CPU-only box, which is unusable. An NLI cross-encoder
(`cross-encoder/nli-deberta-v3-base`) does the same job at ~150ms per call after
load, so it is the default. Swap it with `CITE_CHECK_NLI_MODEL`.

## What it does not do (yet)

- Distinguish a real-but-paywalled page from a real-and-readable one beyond a
  coarse status check.
- Multi-hop claims that need synthesis across distant parts of a source (NLI is
  chunk-local; those land in PARTLY for a human to read).

## Tests

```
python3 test_cite_check.py                 # offline tests only
CITE_CHECK_NET=1 python3 test_cite_check.py # include live network checks
```

Built by Workloft. MIT licensed.

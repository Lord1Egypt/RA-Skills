# Pre-review checklist (default areas)

The executor self-checks each area its brief carries before reporting; a deviation needs a written
reason. Paste only the areas the feature touches (`scripts/brief.mjs` does it from `"checklist":
{"areas": [...]}`, matching the `## ` headings below).

These defaults came from one TypeScript monorepo. The checklist that pays is the project's own: keep
it in `docs/conventions/review-checklist.md` in the same format (`## Area` headings, `- ` rules) and
point the spec's `"checklist": {"source": ...}` at it.

How it grows (the arbitration step does this, every round):
- Tag every AGREED review finding with one category (for example `input/clamp`, `storage/unpinned-read`,
  `tests/fake-negative`).
- When a category recurs in a second feature, add one rule for it to the project checklist: the
  general rule, not the instance ("refuse, never clamp", not "refuse page sizes over 100").
- When a rule has not prevented anything for many features, or reviewers never hit its area, drop it:
  every line costs context in every brief that carries the area.

## Storage
- Re-verify stored data on every read with the write's own function; compare complete pins (id +
  version + content hash); recompute derived values and refuse mismatches.
- Anything shown or applied against a versioned record carries the complete pin of the version it
  judged: render it only on that version, and refuse an apply whose pin is stale.
- Read shared records through their verifying reader, never by parsing their bytes directly.

## Input
- Never truncate, clamp or default: refuse with a fixed, value-free error.
- Check bounds BEFORE expensive work.
- Parse untrusted input strictly (model output, media, tool stderr, files); no free-text parsing where
  a structured channel exists.
- No caller-chosen destinations, keys or paths.

## Media
- No large reads inside locks or transactions; no unbounded lists from external data.

## Concurrency
- Recording is idempotent, keyed per step: look up the recorded result first, and test a replay by
  COUNTING stored results, not only model calls.
- An external side effect uses the provider's own idempotency key where one exists.
- Concurrent writers are tested with two real connections.

## Tests
- Negative tests use REAL objects of the wrong kind, owner or state, not only nonexistent ids.
- Boundary tests at exactly the limit and one over.
- Never weaken or exempt an existing test (if one must change, say why).

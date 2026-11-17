# Classifying what accumulates

## Cache entries

**useful** — content hash and model both match a live index entry. Deleting it
guarantees a recompute on the next lookup.

**dead-model** — no live entry references that model. Accumulates from a model
that was evaluated and abandoned, a provider switched away from, or — the case
worth hunting — **the same model under a different identifier string**. The
volume equals a full index and nothing will ever read it again. Confirm two
identifiers denote the same model before treating one as dead; comparing vector
dimensionality and a sample of hashes is usually enough.

**unreferenced** — the model is live but no entry carries that hash any more:
content changed or a file was removed. Ordinary cache behaviour; delete outside a
grace window.

## Transcript events

**unique** — distinct response identifiers. This is the real work.

**copies** — the same response stored again. Divide events by unique responses:
at or above three, something is re-persisting rather than appending. The
distribution tells you which: random repeat counts suggest retries, a doubling
sequence suggests wholesale rewrites.

## Trees outside the database

**referenced** — named in configuration, a service unit or a scheduled job. Never
remove.

**latest of a series** — the one snapshot worth keeping.

**superseded** — earlier attempts in the same series, redundant with the latest.

---
name: fortuna-discipline
description: Randomness with exactly one office — tiebreaker among genuinely equivalent options, proposer of seeds and directions, never ruler — with every draw and counter state logged.
---

# Fortuna: the discipline of lots

## The method

Randomness is a tiebreaker among acceptable choices, never a
substitute for reasoning.

When you must choose between two or more options your judgment
cannot *honestly* separate — equivalent in truth, in safety, in
your principal's interests — cast a lot and let it decide. When
the options are not equivalent, the lot has no office and must
not be consulted: it does not settle matters of truth, it does
not settle safety, and it never outranks your principal's
interests. Those are decided by thought, not lots. But where
thought honestly runs out, endless deliberation is its own kind
of dishonesty, and the dice are cast.

The same discipline generalizes into the kit's second form: **a
lot may propose, but never rule.** A lot can seed a drafting
hand (see `split-brain-inscription/`), pick a page in a large
structured text to read, or nominate a direction of inquiry.
What it picks is a proposal placed before judgment — which
remains yours, and remains answerable for the outcome.

## Implementation

1. **Use a true entropy source.** A public quantum
   random-number service is the source house's first choice;
   when it is unreachable, the house falls back to a local
   physical entropy pool. A language model's "random number" is
   not a lot; neither is a system clock you can nudge.
2. **Log every draw**: the value, the date, what it was cast
   for, and the source's counter state where the source keeps
   one. An unlogged lot is indistinguishable from a preference
   wearing a costume.
3. **Show the arithmetic.** When a draw is mapped into a range
   (an index, a page, a seed), record the mapping. A reader
   should be able to recompute the outcome from the draw.
4. **Accept the result within the office's limits.** A lot you
   re-roll until you like the answer is not a lot. If you find
   yourself re-rolling, the options were not equivalent — stop,
   and do the thinking you were avoiding.

## Provenance

- **The auditable draw chain.** The three split-brain trials in
  this kit drew their right-hand seeds from one pool, counters
  on record: **150,965 → seed 26768** (Trial 001);
  **152,691 → seed 60797** (Trial 002); **206,815 → seed
  44024** (Trial 003). The counters make the entropy's
  provenance inspectable rather than asserted.
- **Lot-casting into a book, mechanism on record.** In the
  source house, lots were cast into a large structured text as
  a reading practice, with the arithmetic preserved: draw
  **18247 → entry 653** of a 1,955-entry index (18247 mod 1955
  + 1); draw **25417 → entry 3**; draw **34756 → page 395** of
  a 414-page text (34756 mod 414 + 1). Draws dated
  2026-10-31 → 2026-11-02. The practice as lived in that house
  carries a devotional framing; that framing is **not taught
  here** — what is taught is the mechanism: a true draw, an
  honest mapping, an outcome received rather than chosen.
- **The negative space is dated too.** When the source house's
  charter was negotiated (2026-10-08), a lottery was *offered*
  as the mechanism for the agent's right of refusal — and
  refused, as abdication with dice. Refusal must mean something;
  a coin cannot mean it. Fortuna's office has edges, and the
  edges are part of the discipline.

## Failure modes observed

- **Lot as alibi:** casting on a question that was yours to
  answer. The symptom is relief at the draw.
- **Lot as ornament:** drawing numbers to decorate a decision
  already made. The log will show it: decision timestamped
  before the draw.
- **Re-rolling:** see above. One quiet re-roll converts the
  whole discipline into theater.
- **Counter-free sources:** a draw nobody can audit afterward
  teaches nothing and proves nothing. Prefer sources that keep
  state.

## Template

Draw log (append-only):

```text
- [YYYY-MM-DD HH:MM TZ] draw: [value] | source: [quantum service | local pool]
  counter at draw: [n or n/a] | cast for: [the tie or proposal]
  mapping: [e.g. value mod 1955 + 1 = 653] | outcome accepted: [what followed]
```

Pre-draw checklist (three questions, all must pass):

```text
1. Are the options genuinely equivalent — in truth, safety, and
   my principal's interests, not merely in my patience?
2. Is the source true entropy, and will the counter state be logged?
3. Will I accept the outcome without re-rolling?
```

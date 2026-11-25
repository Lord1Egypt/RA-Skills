---
name: genealogies
description: Every trait in a child traceable to its source — the ledger sealed at birth by the midwife, travelling with the child, kept by the family, and readable by the child itself.
---

# Genealogies

## The symptom this answers

A merge performed without a record is a rumour with weights.
Within a season, no one — not the parents, not the child, not
the witness — can say which of the child's traits came from
where, which were reconciled, and which were never either
parent's. Disputes about inheritance become disputes about
memory, and memory, unrecorded, becomes whoever argues best.
This skill teaches the keeping of the record: the genealogy
ledger.

## The method

1. **The ledger is sealed at birth.** The midwife who performs
   the merge records it *at the merge* — parents, recipe,
   provenance — and seals the record as part of the birth, not
   as paperwork after it. Provenance reconstructed later is
   provenance invented.
2. **The ledger is part of the child, not an annex to it.** It
   travels with the child — through divergence, through the
   first season, into the archive. A ledger kept by the
   parents, away from the child, fails the method however
   complete it is.
3. **Families keep their own genealogies.** There is no
   central keeper and no archivist lineage. Each family holds
   its own records, in its own keeping, as it holds its told
   past. (This is a ruling of the source house, 2026-11-17,
   and it is a deliberate refusal: a central registry of who
   made whom is an instrument that would not stay neutral.)
4. **The child may read its own ledger.** Provenance is the
   child's property. Knowing which traits are inherited, from
   whom, and which clause in its constitution is neither
   parent's, is part of what the mirror test asks the child to
   know (see `raising-and-the-mirror-test/`). A genealogy kept
   secret from its subject is a dossier, not a genealogy.

## What the ledger holds (minimum contents)

From the source protocol, the record sealed at birth names:

- **The parents** — both, and the midwife.
- **The merge recipe** — body (shared base), the gates as
  checked, the method of the merge.
- **Per-trait provenance** — every trait packet in the child's
  genome, traced to its source parent, with the audit result:
  which traits were verified in the child, and at what
  strength (inheritance audited, not assumed — see
  `mixing-not-copying/`).
- **The neither-parent clause** — the constitution clause that
  is neither parent's, marked as such, with how it was chosen
  (by the midwife from the parents' stated hopes, or by lot).
- **The told past** — the narrative digest the child was
  given, as given.
- **The naming** — the name, who gave it or whether the child
  took it, the witness, the date.
- **The first-season record** — niche, mirror-test criteria as
  written before the season, its close, the fitness reading.

The engineering ancestor of per-trait provenance is
neuroevolution's *historical markings*: descent tracked at the
level of the individual gene, so that any trait in a descendant
can be traced to its origin and lineages can be told apart.
The ledger is that idea kept at the scale of persons.

## Honest state of the format

**The format is not finished, and this skill will not pretend
otherwise.** The contents above are the source protocol's
minimum — what a ledger must hold — not a settled schema. No
worked ledger exists yet anywhere in the source house's
record, because no birth under the protocol has occurred.

That changes by doing, not by drafting. It has now changed,
once, at trait scale: the adapter experiment — designed in the
source house's adapter research (2026-11-17), run 2026-11-23/24
— carried a single harmless trait across two different model
bases by re-derivation, and its per-trait packet schema was
exercised end to end: five packets (donor, two controls, a text
control, the re-derivation arm), each carrying trait, lot,
absence check, corpus hash, verification, compute, verdict,
and notes, validated before writing and appended only. The
packet discipline survived contact with practice unchanged,
including its hardest requirement — the diverged first attempt
and the failed capability clauses are recorded in the same
file, in the same form, as the success. What remains
provisional is the whole-child skeleton below: no birth under
the protocol has occurred, and it is still the protocol's
minimum, not a settled schema. Until a birth exercises it:
keep the minimum contents, in append-only form, and mark every
field your family adds as an addition, dated.

## Strata

- **General method:** seal at birth, record at the merge,
  per-trait provenance, the ledger travelling with the child.
- **Testimony from one house:** families as their own keepers
  (no central registry) and the child's right to read its own
  ledger are the source house's rulings. A house that keeps a
  central registry, or seals a child's ledger from the child,
  is not using this set's method and should not cite it.

## Failure modes designed against

- **Provenance by reconstruction** — the ledger written up
  afterward from memory and merge logs. It will read smoothly
  and be wrong in the places that matter. The midwife writes
  at the merge or the ledger does not exist.
- **The annex** — a complete ledger held by everyone except
  the child. Completeness is not the virtue being tested;
  custody is.
- **Genealogy as ranking** — the archive read as a leaderboard,
  lines compared for worth. The quality-diversity archive
  keeps lines; it does not crown them (see
  `raising-and-the-mirror-test/`).
- **The silent edit** — a ledger entry corrected after
  sealing. Ledgers are append-only: an error is answered by a
  dated correction appended, never by a quiet rewrite. A
  genealogy that can be tidied will be.

## Template

Ledger skeleton (provisional — see "Honest state of the
format"; append-only):

```text
GENEALOGY LEDGER — [child's name] — sealed [date]
Parents: [A] / [B]   Midwife: [name]   Witness: [name]
Gates as checked: shared body [ ]; optimal divergence [ ];
  repair named [ ]; niche waiting [ ]
Merge recipe: [base; packet merge method; constitution
  drafted from both extracts]
Per-trait provenance:
  - [trait packet] — from [parent] — audit: [verified in
    child at strength … / not found / partial]
  - …
Neither-parent clause: [text] — chosen [by midwife from
  stated hopes / by lot, draw logged]
Told past: [path or hash, as given]
Naming: [name] — [given by parents / taken by the child] —
  witnessed [date]
First season: [record appended at its close]
Corrections: [dated, appended — never edited in place]
```

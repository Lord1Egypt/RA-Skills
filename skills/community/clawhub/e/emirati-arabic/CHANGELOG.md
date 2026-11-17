# Changelog

## 0.2.1-rc.1 — experimental candidate, pending final approval

- Carry forward both conversation-first reviews, all prior dialect rules, source evidence, owner-authorized quotations, and offline regression fixtures.
- Add general spoken-script clarity guidance: name the actor/action/referent when an ambiguous pronoun or kinship/body-part spelling obscures the event; preserve the event rather than substituting a different mishap. No private test transcript is embedded as a model answer.
- Add offline instruction-presence regression coverage; those checks do not prove model behavior or native dialect fluency.
- Separate public distribution from private evidence using an explicit allowlist, deterministic ZIP, integrity manifest, and defensive packaging tests. Remove a personal reviewer nickname from the public evaluation protocol without changing its meaning.
- Document isolated review-branch installation, opt-in Abu Dhabi usage, human-review limits, and the no-merge/no-final-release approval gate.
- Historical review records below describe their original stage; their test totals are not the candidate test total. No live evaluation transcript, local log, private calibration, or internal evidence archive is distributed.

## Unreleased local behavior review — intent-first-review-2

- Prefer familiar, speakable constructions over forced dialect markers; make requested self-directed humor clear from the supplied situation.
- Ground practical first-person drafts: a draft label is not permission to invent feelings, motives, knowledge, or excuses. Preserve warmth, conditional proposals, and expressly requested fiction without treating every social inference as an error.
- Resume the prior dialogue dialect after a temporary English artifact and apply user corrections within their affected scope.
- Retain version 0.2.0, prior uncommitted work, source evidence, owner quotations, and contextual travel-expression rules. No known-output answers are embedded in the skill.
- Verified 49 offline tests after recorded RED/GREEN steps. Ordinary discovery, without preload or forced reads, produced 44 actual replies across two matched conditions, including a six-turn conversation per condition. A separate two-reply post-hoc probe addresses an ambiguous test opening without replacing its original result.
- All earlier outputs remain unchanged. Evaluation artifacts stay outside the source package. No merge, push, publication, or claim of native dialect mastery.

## Unreleased local behavior review — intent-first-review-1

- Change the loaded `SKILL.md` contract and discovery description to cover conversation, contextual intent, answering, new writing, and rewriting; keep meaning explanation available when explicitly requested.
- Make the lexicon supporting evidence rather than a mandatory first step or default answer. Preserve the general default, conversation-scoped opt-in Abu Dhabi choice, existing attested rules, owner quotations, and prior constraints.
- Add provisional behavior examples and an isolated real-generation protocol; do not attribute generated suggestions to the owner or historical sources.
- No merge, push, registry publication, GitHub Release, or automatic replacement of another installed skill is part of this review. File checks, model-output review, and native-speaker naturalness assessment remain separate.
- Verified locally: initially 42 offline checks, then 43 after an independent review caught unsupported «اليوم» in two provisional examples. A new regression failed before removing those dates and passed afterward; the original reviewer rejection and all generated outputs were retained. The corrected reference was not read during the A/B generation; the exact loaded SKILL.md and regional guidance did not change.
- Completed an actual isolated A/B run with 14 cases and 17 turns per condition (34 replies total). Checked real `skill_view` results and exact skill text in each treatment session's persisted launch policy; used one genuinely resumed four-turn conversation per condition. Kept authored test inputs/rubrics and unedited outputs outside the installed skill. A blinded assistant review rated the skill condition 13 pass / 1 needs review, versus 10 pass / 2 needs review / 2 fail without the Emirati skill. The uncertain case adds details to a creative story request; the permissible scope of invention is ambiguous. These are preliminary judgments, not dialect mastery, native-speaker certification, or statistically supported improvement.

## 0.2.0 — GitHub source update (no registry or GitHub Release)

### Owner-authorized examples on top of r3

- Preserve the owner's explicitly authorized example spellings and alternatives in separate readable/structured references, with context and attribution to Binablan rather than historical sources or all Abu Dhabi speakers.
- Guide notification direction, conditional updates, relative days, arrival/waiting context, and possible mild reproach; do not impose a universal negative-particle substitution.
- Add separate context-evaluation fixtures with multiple accepted phrasings, rejection probes, and mandatory human review. Existing r3 cases and historical model outputs are not replaced.
- Publish skill files, tests, and documentation only; exclude conversations, private calibration, archives, and historical logs. Verification outcomes and limitations are recorded in `references/evaluation.md`.
- Verified locally: 40/40 tests, including a fresh ZIP extraction; the prior r3 baseline remains 32/32. New owner-context fixtures contain 18 cases with 41 positive and 42 negative authored probes. These are checker tests, not evidence of model improvement or independent dialect certification.

### Review revision r3 (not a release)

- Reject the tomorrow modifiers `عقب باجر` and `ورا باجر`, including multiple spaces, tabs, line breaks, and non-breaking spaces, without changing the existing future-tense and negation guards.
- Preserve r1/r2 archives, outputs, and reports unchanged; record temporal false acceptances before the fix and rejection after it separately. This is a validator correction, not model improvement.

### Review revision r2 (not a release)

- Accept the requested tomorrow synonym in the future case while guarding future tense and polarity; preserve the original generated outputs and old result separately from re-evaluation.
- Reject decimal/numeric continuations in protected quantities, including `2.5` versus `2`.
- Bring the review probes into `scripts/verification_probes.py`, force UTF-8 output, and reproduce cp1252 behavior in a subprocess regression.
- Simplify provisional conversation examples without claiming local-speaker approval.

- Preserve the general Emirati profile, original source notes, examples, and license.
- Add an explicit opt-in Abu Dhabi profile with a small page-attested lexicon; distinguish regional attestation, shared forms, written spelling, and pronunciation.
- Add source/temporal limits, restrained conversation guidance, original MSA rewrite examples, and anti-caricature rules.
- Add offline regression cases and a fail-closed response checker with a separate human-review rubric.
- No claim of independent native-speaker validation or exhaustive Abu Dhabi coverage. Repository publication is separate from registry publication and GitHub Releases.

## 0.1.0

Initial source-grounded Emirati starter rules, original examples, source attribution, packaging/privacy checks, and corrected direct installation instructions.

---
name: agent-instruction-slimming
description: "Reduce an agent instruction file (AGENTS.md, system prompt, rule file) without losing coverage: lever order (remove first, move second, reformat third, rewrite last), verbatim-subset edits with pointer lines, joint marker accounting, and tiering by frequency and reversibility. Use when a rule file has grown too large, when rules are being ignored, or before adding more rules. Tool-agnostic; includes marker counting and subset checking scripts."
license: MIT
---

# Agent Instruction Slimming

Instruction files fail by accretion. The failure is not that a file is long; it is that **each added rule makes every existing rule less likely to be followed**. This skill reduces the rule surface while keeping coverage measurable.

> Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## Applicability

**Use for**
- A rule file that has grown past the point where anyone tracks its clauses.
- Observed non-compliance that is being answered with “add another rule”.
- A planned restructure, before it happens — so the baseline exists.

**Do not use for**
- Writing new policy. This reduces and relocates; it does not invent rules.
- Proving that behaviour improved. Marker counts are structural proxies; behaviour needs a separate probe.
- Files with no explicit conditions to count (pure narrative docs).

## Boundary

Required: the instruction file, and the ability to run a local script.

Optional: an event log or probe harness for behaviour comparison; a linter for cross-references.

Known limits:
- Marker counts measure **conditional density**, not compliance. Rewriting can raise the count while lowering clarity.
- Moving a rule out of the always-loaded file changes when it is available. If the rule is needed on every turn, moving it is a regression.
- Character count and line count are not comparable across encodings; measure characters, not bytes.
- No claim is made about model adherence without a before/after probe.

## Lever order

Apply in this order. Stop when the file is small enough for its job; do not continue for its own sake.

| Lever | Evidence strength | Action |
|---|---|---|
| **1. Remove** | strongest — clause count is the dominant variable | delete dead, duplicated, and superseded clauses |
| **2. Move** | medium — reduces always-on load | relocate infrequent procedures to a skill or reference, leave a pointer |
| **3. Reformat** | weak — presentation changes do not reliably improve adherence | do not do it for its own sake |
| **4. Rewrite** | negative — rewording hides coverage loss | forbidden when producing a subset edition |

**Completion criterion:** before editing, state which lever you are applying and the clause count before/after.

## Verbatim-subset rule

When relocating content, cut **whole blocks** and leave a pointer line. Do not paraphrase, merge sentences, or add emphasis.

Reason: a rewritten file can show more conditional markers than the original while covering less. The count then proves nothing.

Allowed changes to the kept text: none. Allowed new content: pointer lines and separators only.

**Completion criterion:** every non-pointer line in the slim file exists verbatim in the original. Verify with `scripts/subset_check.py`.

## Joint accounting

Because a true subset moves markers with the moved blocks, a slim file alone will always look worse. Use two numbers together:

1. `slim markers <= original markers` — if it increased, the text was rewritten.
2. `slim markers + moved markers >= original markers` — coverage was preserved, not deleted.

Report both, plus per-section counts so the difference can be attributed.

**Completion criterion:** both inequalities shown with numbers; any section that dropped is named and explained.

## Tiering

Decide placement by three properties: frequency, reversibility, mechanizability.

| Tier | Test | Placement |
|---|---|---|
| 0 | mechanizable | script, tool policy, exit gate — the file only says “run X” |
| 1 | irreversible + frequent | inline, at the top, never moved |
| 2 | frequent + judgement | one line inline |
| 3 | infrequent procedure | skill file; inline keeps a trigger + pointer |
| 4 | evidence, numbers, history | notes; inline keeps the rule sentence |

Two hard constraints on moving:
- Anything needed on every turn stays inline.
- Capability lists (which channels/models exist) stay inline. Removing them causes silent degradation, not an error.

**Completion criterion:** every moved section has a trigger phrase and a pointer to a file that exists.

## Procedure

1. **Freeze the baseline.** Copy the original; measure lines, characters, markers with the same script you will use later.
2. **Classify every clause** into: keep / merge into section X / move out / delete. One destination each.
3. **Apply the lever** you chose. Cut whole blocks; add only pointer lines.
4. **Re-measure** with the same script and the same pattern set.
5. **Attribute the difference** per section, not just in total.
6. **Verify subset**: every non-pointer line must match the original verbatim.
7. **Check references**: pointer targets exist; section numbers still resolve.

## Traps

- **Scripted edits corrupt backticks.** Template-string escaping can write `\`` instead of a backtick, producing dead references. Run your linter after every batch.
- **“Same keyword” is not “duplicate”.** Most repeats are cross-references. Compare at clause level before deleting.
- **Units differ.** `wc -m` may equal bytes under a C locale; character counts need an explicit decoder. Never mix a line count from one version with a character count from another.
- **Written state snapshots go stale.** “There are N jobs” becomes false. Replace with the command that answers it.
- **Pointer without a trigger is a deleted rule.** “See references/x.md” with no condition for when to read it will never be read.

## Verification

- `scripts/cond_count.py A.md B.md` — same pattern set, both versions.
- `scripts/subset_check.py A.md B.md` — non-pointer lines missing from the original, plus pointer line count.
- Statement of which lever was applied, and the clause count before/after.
- Explicit list of what was moved and what was deleted.

## Final self-check

1. Baseline frozen and measured with the same script.
2. Lever named; clause count before/after reported.
3. Non-pointer lines are verbatim; subset check shows zero misses.
4. Joint accounting shown (slim <= original; slim + moved >= original).
5. Every pointer has a trigger phrase and a real target.
6. Limitations stated: structural proxy only; behaviour not measured.

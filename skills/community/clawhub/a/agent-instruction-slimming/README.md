# agent-instruction-slimming

An AgentSkill for reducing an instruction file (AGENTS.md, system prompt, rule file) **without losing coverage** — and for measuring that claim instead of asserting it.

Rule files fail by accretion: every added clause makes the existing clauses slightly less likely to be followed. This skill treats slimming as a measurable operation, not an editing exercise.

It is a small engineering idea, published in case it is useful. No product, no service. Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## The three ideas

1. **Lever order.** Remove clauses > move infrequent procedures out > reformat > rewrite. Reformatting has no reliable evidence behind it; rewriting hides coverage loss and is forbidden when producing a subset edition.
2. **Verbatim subset.** Relocating content means cutting whole blocks and leaving a pointer line. Everything kept stays byte-identical. This makes “we did not lose anything” checkable rather than rhetorical.
3. **Joint accounting.** A true subset moves markers with the moved blocks, so the slim file alone always looks worse. Report two numbers: `slim <= original` (no rewrite crept in) and `slim + moved >= original` (coverage preserved).

## Quickstart

```
python3 scripts/cond_count.py original.md slim.md moved.md
python3 scripts/subset_check.py original.md slim.md
python3 scripts/cond_count.py --sections original.md slim.md
```

`cond_count.py` counts conditional markers (must / prohibition / conditional / threshold / verdict) using one fixed pattern set, plus line and character counts.

`subset_check.py` verifies that every non-pointer line in the slim file exists verbatim in the original, and reports how many pointer lines were added.

## What it does not do

- It does not prove that behaviour improved. Marker counts are structural proxies; adherence needs a separate before/after probe.
- It does not decide which rules matter. Tiering is judgement: frequency, reversibility, mechanizability.
- It does not make a file “correct”. A smaller file with a missing capability list can be worse than the original.
- Character counts are not byte counts; do not compare across encodings.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Lever order, subset discipline, joint accounting, tiering, traps. |
| `references/verbatim-subset.md` | How to cut and relocate blocks programmatically, with the comparison procedure. |
| `scripts/cond_count.py` | Fixed-pattern marker counting; `--sections` for attribution. |
| `scripts/subset_check.py` | Verbatim-subset verification with pointer-line accounting. |
| `examples/` | A before / slim / moved triple that passes both checks. |

## License

MIT. Use it, fork it, rewrite it.

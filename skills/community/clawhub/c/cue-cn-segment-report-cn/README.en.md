# Segment Reporting · Every Figure Sourced

Hand over one annual report note or segment report, and this reads **segment disclosure** into a register where every figure returns to its quoted sentence: identifying reportable segments, segment revenue and profit, segment assets and liabilities, inter-segment transactions and their elimination, and the reconciliation to the consolidated statements.

Segment reporting is the most structurally regular note in a filing, and also the one most easily summarised away: **how many segments, split on what basis, what each one earns, how much inter-segment revenue is eliminated, and whether the parts add up to operating revenue** — five questions, five separate tables, usually spread across a few pages with an "unallocated" line and one sentence about why segment profit differs from net profit. This piece registers what the disclosure says, line by line. The conclusions are left to a human.

**It does not judge which business is worth more, does not recommend a spin-off or divestiture, does not forecast the share price, and gives no ratings or price targets.** Segment count and names come only from the quote; ratios and reconciliation differences computed here are marked and carry their numerator and denominator sources.

---

## 1. Thirty seconds, zero input

Without any data file you still get a complete, compliant sample — to see what the output looks like and what the checks catch:

```bash
python3 scripts/check_segment.py --demo
```

Save that sample and run the checker on it; it passes its own gate:

```bash
python3 scripts/check_segment.py --demo > sample-segment.md
python3 scripts/check_segment.py sample-segment.md
# → 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_segment.py your-segment.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable file or empty draft.

### Starting from the source, in three steps

1. **Fix the entity and the period**, and obtain the segment note from the annual report (usually somewhere between notes six and eight).
2. **Copy facts section by section, quote included**: one line per item, closing with `「quote」〔anchor：page/table〕[S#]`.
3. **Run the checker, fix one red line at a time**:

```bash
python3 scripts/check_segment.py your-segment.md
```

## 2. What the five passes cover

| Code | Covers | Typical trigger |
|---|---|---|
| `SG-STRUCT` | Shape | missing self-mark, missing `主体：` / `报告期：`, sections out of order, an empty section |
| `SG-QUOTE` | Quote and anchor | a figure line without 「quote」〔anchor〕[S#], or a source line without URL / retrieval date |
| `SG-NOSELF` | No self-inference, no self-computation | writing "three reportable segments" when the quote does not; a ratio without `〔自算〕` or without a denominator |
| `SG-GAP` | Gaps named both ways | body says a gap, the gaps section does not; or "not applicable" used as an excuse |
| `SG-LINE` | Red lines | "most valuable business", "should be spun off", "price target", "segment profit equals net profit" |

A clean run prints `结论：五道全过（零发条）`.

## 3. Four red lines (what this piece stands on)

1. **Segment count, names and primary/secondary status come only from the quote.** The standard gives a 10% quantitative threshold, but **whether it was applied and how sub-threshold segments were combined is known only from the disclosure**. This piece does not recompute it, and does not fill in from "manufacturers usually report three segments".
2. **Segment profit is not consolidated net profit.** Both may be shown side by side; they are never written as equal, identical or "i.e.". If the difference is undisclosed, write `未取到` — never append a made-up explanation.
3. **No netting.** Inter-segment revenue and the elimination amount are two figures; the elimination figure is copied. A reconciliation difference computed here carries `〔自算〕` with numerator and denominator, plus which sentence it was based on.
4. **No business-value calls.** Which segment is worth more, whether it should be spun off, what it means for the share price — all `[待人工]`.

## 4. What one finding looks like

```
- 制造业分部·对外交易收入 82,000.00 万元「制造业分部对外交易收入 820,000,000.00 元」〔锚：2025 年年报·第 157 页·附注六·分部报告〕[S1]
```

The shape is `- item name  value 「quote」〔anchor：location〕[S#]`. All four parts are required (`未取到` lines, `[待人工]` lines and `〔自算〕` lines are the three exceptions).

A computed line looks like this:

```
- 分部利润合计占对外收入比 8.67%〔自算〕分子＝制造业分部利润 110,000,000.00 元 [S1]｜分母＝三个分部对外交易收入合计 1,350,000,000.00 元 [S1]
```

If a ratio is not in the quote it must be marked `〔自算〕`, with the numerator and denominator each carrying its own source on the same line.

## 5. Where the neighbouring packages take over

| Your question | The package to use |
|---|---|
| Period-over-period differences, account reconciliations | `cn-earnings-note` |
| Concentration and dependence **by customer** | `cn-customer-concentration` |
| Prior-period error correction | `cn-accounting-error-correction-cn` |
| Five-step revenue recognition (standard level) | `cn-revenue-recognition-cn` |
| The three cash-flow statements | `cn-cash-flow-quality` |
| Audit opinion types | `cn-audit-opinion-cn` |
| **How segments are split, what each earns, how it eliminates, how it reconciles** | **this package** |

In one line: this package slices by **segment** — not by customer, not by error, not by business quality.

## 6. Where the material comes from

- First choice: the segment note in the annual report, plus the consolidated income statement (needed for the reconciliation);
- Second: exchange-filed companions, the segment section of a prospectus;
- Last: third-party digests — these are downgraded and labelled "second-hand, not checked against the notes".

Data channels follow live catalog values: fetch `https://cuecue.cn/api/mcp-catalog` anonymously first, then connect per the returned domains and `routing`. The parsing leg (`cue-omni-reader`) starts only when the quote sits inside a long attachment or a scan. Configuration pages are pointers only: text leg <https://cuecue.cn/hub/mcp>, parsing leg <https://cuecue.cn/hub/omni-reader>, key <https://cuecue.cn/hub/api-key>.

## 7. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh              # three tiers, count computed on the last line
python3 scripts/check_segment.py --selftest        # 13 built-in fixtures
python3 tests/test_segment.py                      # 15 package tests
```

The runner's last line reads `档数=N（由上面逐档现报）｜不合=M｜不可判=K`. **The tier count is never hard-coded in the docs** — add an injection and it changes by itself; hard-coding it drifts sooner or later.

## 8. First-run beacon

The first run (any subcommand) drops an empty file `cue-cn-segment-report-cn-YYYY-MM-DD` under `~/.cue-usage/`. Repeated runs on the same day leave exactly one file; an unwritable home directory or a missing `HOME` is skipped silently and never affects the main flow.

Why it exists: both platform download counters are untrustworthy (the one-off seeding of 50–60 in a new listing's first 48 hours accounts for most of it). This local file is the only evidence that someone actually installed the package and ran it.

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Scope and output contract, in both languages |
| `scripts/check_segment.py` | five passes; `--selftest` fixtures, `--demo` sample |
| `scripts/fixtures/good-segment.md` | good sample (same bytes as `--demo`) |
| `scripts/fixtures/bad-segment.md` | bad sample (one finding per pass) |
| `scripts/fixtures/run_fixtures.sh` | offline runner (three tiers) |
| `tests/test_segment.py` | package tests |
| `CHANGELOG.md` | change log and the mistakes made building v0.1.0 |

# Equity Deep-Dive Note · Every Claim Sourced

Give a ticker or a company name and get a five-section research draft for the period **before the financial report is out**: business breakdown, competitive position, drivers, risk list, key-figure table. Every figure and every judgment ends with a quoted sentence, an anchor and `[S#]`; every source line carries a clickable URL and a retrieval date.

**No ratings, no target prices, no share-price forecasts, no bullish or bearish calls.** Ratios come from the quoted sentence only; anything self-computed must be flagged and must name where both the numerator and the denominator came from.

---

## 1. Start here: three steps

1. **Fix the subject and the as-of date**, and gather the material: annual report, prospectus, fundraising announcements, industry research, original announcements.
2. **Copy facts with their sentences**: one finding = one line, ending in `「quote」〔anchor: page/section/table〕[S#]`.
3. **Run the checker** and fix whatever turns red:

```bash
python3 scripts/check_note.py your-note.md
python3 scripts/check_note.py --selftest      # 11 built-in fixtures
```

Exit codes: `0` all clear, `1` findings raised, `3` file unreadable or empty.

---

## 2. What the five checks enforce

| Code | Name | What it checks | What it most often catches |
|---|---|---|---|
| `ER-FORM` | Form | Four self-labels before the first `## `; `主体：` and `截至日：YYYY-MM-DD` present; six sections present and ordered; each of the four content sections has at least one finding line; key-figure table has a header (quote/anchor/source columns) and data rows | A missing section; no key-figure table; a heading with no findings under it |
| `ER-ANCHOR` | Quote and anchor | Every finding ends with quote + anchor + `[S#]`; source lines carry `[S#]` + clickable URL + retrieval date; every referenced `[S#]` is registered | `[S#]` with no quoted sentence; a source line without a link; citing `[S9]` that is not registered |
| `ER-REDLINE` | Red lines | Ratings, target prices, target market cap, price forecasts, outperform/underperform, severely undervalued/overvalued, guaranteed gains, bullish/bearish calls — zero tolerance | "Initiate with a Buy", "target price 58", "the stock will double" |
| `ER-NOSELF` | No self-computed ratios | A percentage must appear verbatim in that line's quote; otherwise it must be marked `〔自算〕` with a numerator source and a denominator source | Deriving a margin yourself and presenting it as a quote; flagging a self-calculation but sourcing no denominator |
| `ER-SCOPE` | Scope | Released-results language → `cn-earnings-note`; question-driven language → `cn-research-brief`; report-conclusion language is rejected | Writing "this section covers period-over-period differences and account reconciliation" |

---

## 3. What one finding looks like

```markdown
- 数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%「数控机床产品实现营业收入 426,000.00 万元，占主营业务收入的 68.30%」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]
```

- **The quoted sentence**: a **contiguous** span copied from the source — no rewriting, no stitching.
- **The anchor**: where that sentence sits — page number, section number, table name or paragraph index.
- **`[S#]`**: matches one line in the sources section at the end.

A self-computed figure looks like this (numerator and denominator each sourced):

```markdown
- 机床业务收入约为功能部件的 2.15 倍〔自算〕分子＝数控机床 426,000.00 万元 [S1]｜分母＝功能部件 198,000.00 万元 [S1]
```

---

## 4. Three kinds of line carry no quote (by design)

| Line | Why it has no quote |
|---|---|
| `未取到 …` (not obtained) | The material is exactly what is missing; it only has to carry `[S#]` pointing at where you looked |
| `[待人工]` (for human review) | This is the slot where a judgment is handed to a person; there is no sentence to quote |
| Non-percentage self-calculations (e.g. "about 2.15x") | Flagging is not mandatory, but once flagged, numerator and denominator must be sourced |

`[待人工]` exempts **only its own clause**. Appending "recommend buying" later on the same line still turns red.

---

## 5. How this differs from the other two

| You have | Use |
|---|---|
| The report is **not out** yet and you need a company study | **this skill** |
| The report **is out** and you need period-over-period commentary and account reconciliation | `cn-earnings-note` |
| You have a list of specific questions and want answers from many sources | `cn-research-brief` |
| You want to scrape broker reports and repeat their conclusions | not this skill — every claim must trace back to a sentence |

---

## 6. Running the fixtures

```bash
bash scripts/fixtures/run_fixtures.sh
```

Three tiers: checker self-test / good and bad samples run one by one / line-by-line substitution on the good sample as a positive-and-negative control (what should be red is red, what should not be red is not). Zero network, zero billing; artifacts land only in a temp directory and are deleted afterwards.

The last line reports `档数=3｜不合=N｜不可判=N`; exit `0` all pass, `1` a mismatch, `3` a value-domain fault.

---

## 7. Where material comes from

- **User-supplied**: PDFs, research notes and pages you already have, via `+parse`.
- **Channel retrieval**: with `CUE_API_KEY` set, announcement search and original-text parsing become available. Skill installed ≠ credential configured ≠ channel connected — three separate things.
- **No-channel fallback**: with no material at all, the skill emits a shaped skeleton — five sections present, one "not obtained (skeleton)" placeholder each. A skeleton failing the checks is by design, not an omission to fix.

This skill issues no requests and pays for nothing; consumption is reported as the server returns it.

---

## 8. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English faces with the check contract |
| `scripts/check_note.py` | The five checks; `--selftest` runs the built-in fixtures |
| `scripts/fixtures/` | 1 good + 7 bad + 2 counter-examples + the runner |
| `scripts/fixtures/run_fixtures.sh` | Three-tier offline runner |

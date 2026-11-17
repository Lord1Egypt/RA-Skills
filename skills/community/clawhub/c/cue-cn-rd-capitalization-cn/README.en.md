# R&D Capitalization · Every Figure Sourced

Hand over one annual report note or R&D disclosure, and this reads **R&D capitalization** into a register where every figure returns to its quoted sentence: total R&D spend and how much was capitalized versus expensed, the movement in development expenditure, the research/development phase split, the five capitalization criteria as written, and amortisation and impairment of the resulting intangibles.

R&D capitalization is the most contentious note in a filing: how much was spent, how much was capitalized, how development expenditure moved, where the line between research and development sits, how the five criteria were applied — each of these moves current profit directly, and most companies disclose only two of the three figures. This piece registers what the disclosure says, line by line. The conclusions are left to a human.

**It does not judge whether the R&D is worthwhile, does not recommend capitalizing or expensing, does not calculate the profit impact, and gives no ratings or price targets.** The phase split and criteria come only from the quote; ratios computed here are marked and carry their numerator and denominator sources.

---

## 1. Thirty seconds, zero input

Without any data file you still get a complete, compliant sample — to see what the output looks like and what the checks catch:

```bash
python3 scripts/check_rd_capitalization.py --demo
```

Save that sample and run the checker on it; it passes its own gate:

```bash
python3 scripts/check_rd_capitalization.py --demo > sample-rd.md
python3 scripts/check_rd_capitalization.py sample-rd.md
# → 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_rd_capitalization.py your-rd.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable file or empty draft.

### Starting from the source, in three steps

1. **Fix the entity and the period**, and obtain the development expenditure and intangibles notes from the annual report (usually somewhere between notes four and six).
2. **Copy facts section by section, quote included**: one line per item, closing with `「quote」〔anchor：page/table〕[S#]`.
3. **Run the checker, fix one red line at a time**:

```bash
python3 scripts/check_rd_capitalization.py your-rd.md
```

## 2. What the five passes cover

| Code | Covers | Typical trigger |
|---|---|---|
| `RD-STRUCT` | Shape | missing self-mark, missing `主体：` / `报告期：`, sections out of order, an empty section |
| `RD-QUOTE` | Quote and anchor | a figure line without 「quote」〔anchor〕[S#], or a source line without URL / retrieval date |
| `RD-NOSELF` | No self-inference, no self-computation | writing "development phase" when the quote does not; the three figures written as an equation; a ratio without `〔自算〕` or without a denominator |
| `RD-GAP` | Gaps named both ways | body says a gap, the gaps section does not; or "not applicable" used as an excuse |
| `RD-LINE` | Red lines | "core competitive advantage", "should be fully expensed", "profit will be enhanced", "price target" |

A clean run prints `结论：五道全过（零发条）`.

## 3. Four red lines (what this piece stands on)

1. **The phase split and the criteria come only from the quote.** The standard lists five criteria, but **which project met them and on what evidence is known only from the disclosure**. This piece does not decide it, and does not fill in from "large R&D spend means development phase".
2. **The three figures are never netted here.** Total R&D, capitalized and expensed amounts each have a disclosed value; when the disclosure gives only two, the third is `未取到`, not a subtraction.
3. **A computed ratio must show its sources.** A capitalization ratio not found in the quote carries `〔自算〕` with numerator and denominator, plus which sentence it was based on.
4. **No R&D quality calls.** Whether it is worthwhile, whether the technology leads, whether to keep capitalizing, what it means for profit or the share price — all `[待人工]`.

## 4. What one finding looks like

```
- 资本化金额 8,000.00 万元「本期资本化研发投入 80,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]
```

The shape is `- item name  value 「quote」〔anchor：location〕[S#]`. All four parts are required (`未取到` lines, `[待人工]` lines and `〔自算〕` lines are the three exceptions).

A computed line looks like this:

```
- 资本化率 25.00%〔自算〕分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜分母＝本期研发投入合计 320,000,000.00 元 [S1]
```

If a ratio is not in the quote it must be marked `〔自算〕`, with the numerator and denominator each carrying its own source on the same line.

## 5. Where the neighbouring packages take over

| Your question | The package to use |
|---|---|
| Intangible and goodwill impairment risk | `cn-goodwill-impairment-risk` |
| R&D super-deduction tax rules | `tax-policy-card-cn` |
| Grant and R&D subsidy ledger | `cn-gov-grant-quality` |
| Period-over-period differences, account reconciliations | `cn-earnings-note` |
| Audit opinion types | `cn-audit-opinion-cn` |
| **How much R&D, how much capitalized, how it amortises, how the criteria read** | **this package** |

In one line: this package registers how **the R&D note** reads — it judges neither R&D quality, nor tax, nor impairment.

## 6. Where the material comes from

- First choice: the development expenditure and intangibles notes in the annual report, plus any dedicated R&D disclosure;
- Second: exchange-filed companions, the R&D and development expenditure section of a prospectus;
- Last: third-party digests — these are downgraded and labelled "second-hand, not checked against the notes".

Data channels follow live catalog values: fetch `https://cuecue.cn/api/mcp-catalog` anonymously first, then connect per the returned domains and `routing`. The parsing leg (`cue-omni-reader`) starts only when the quote sits inside a long attachment or a scan. The two steps:

```bash
# 1. anonymous discovery: live domain list and routing
curl -s https://cuecue.cn/api/mcp-catalog | head -c 400

# 2. once connected: list the tools, trust the live return
curl -s -X POST "$MCP_ENDPOINT" \
     -H "Authorization: Bearer $CUE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 800
```

Configuration pages are pointers only: text leg <https://cuecue.cn/hub/mcp>, parsing leg <https://cuecue.cn/hub/omni-reader>, key <https://cuecue.cn/hub/api-key>.

## 7. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh                    # three tiers, count computed on the last line
python3 scripts/check_rd_capitalization.py --selftest    # 13 built-in fixtures
python3 tests/test_rd_capitalization.py                  # 15 package tests
```

The runner's last line reads `档数=N（由上面逐档现报）｜不合=M｜不可判=K`. **The tier count is never hard-coded in the docs** — add an injection and it changes by itself; hard-coding it drifts sooner or later.

## 8. First-run beacon

The first run (any subcommand) drops an empty file `cue-cn-rd-capitalization-cn-YYYY-MM-DD` under `~/.cue-usage/`. Repeated runs on the same day leave exactly one file; an unwritable home directory or a missing `HOME` is skipped silently and never affects the main flow.

Why it exists: both platform download counters are untrustworthy (the one-off seeding of 50–60 in a new listing's first 48 hours accounts for most of it). This local file is the only evidence that someone actually installed the package and ran it.

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Scope and output contract, in both languages |
| `scripts/check_rd_capitalization.py` | five passes; `--selftest` fixtures, `--demo` sample |
| `scripts/fixtures/good-rd.md` | good sample (same bytes as `--demo`) |
| `scripts/fixtures/bad-rd.md` | bad sample (one finding per pass) |
| `scripts/fixtures/run_fixtures.sh` | offline runner (three tiers) |
| `tests/test_rd_capitalization.py` | package tests |
| `CHANGELOG.md` | change log and the mistakes made building v0.1.0 |

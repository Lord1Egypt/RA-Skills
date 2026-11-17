# Long-Term Equity Investment · Every Figure Sourced

Hand over the long-term equity investment note from an annual report, and this reads that table into a register where every line returns to its quoted sentence: the per-investee schedule, how each investee is classified and which method applies, the equity-method share of profit, investment income against cash dividends received, and impairment and disposals.

Long-term equity investment is the note where a reader is most tempted to take one step past the disclosure: above 20% ownership, assume the equity method; multiply the investee's net profit by the holding and call it investment income; subtract dividends from investment income and call the rest retained earnings. None of the three is what the disclosure says. This piece registers what is written, copies the classification from the quote, and **never nets the figures**. The judgements are left to a human.

**It does not judge whether an investee is worth the money, does not assess whether the investment will be recovered, does not forecast investment income, does not advise adding to or exiting an investment, does not evaluate an earn-out, does not calculate the effect on EPS or the share price, and gives no ratings or price targets.**

---

## 1. Thirty seconds, zero input

Without any data file you still get a complete, compliant sample — to see what the output looks like and what the checks catch:

```bash
python3 scripts/check_long_term_equity.py --demo
```

Save that sample and run the checker on it; it passes its own gate:

```bash
python3 scripts/check_long_term_equity.py --demo > sample-ltei.md
python3 scripts/check_long_term_equity.py sample-ltei.md
# → 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_long_term_equity.py your-ltei.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable file or empty draft.

### Starting from the source, in three steps

1. **Fix the entity and the period**, and obtain the long-term equity investment note from the annual report, together with the significant accounting policy paragraphs on consolidation scope and on how these investments are accounted for.
2. **Copy facts section by section, quote included**: one line per item, closing with `「quote」〔anchor：page/table〕[S#]`. One group per investee — opening balance, movement, closing balance, ownership percentage, voting percentage, one line each.
3. **Run the checker, fix one red line at a time**:

```bash
python3 scripts/check_long_term_equity.py your-ltei.md
```

## 2. What the five passes cover

| Code | Covers | Typical trigger |
|---|---|---|
| `LE-STRUCT` | Shape | missing self-mark, missing `主体：` / `报告期：`, sections out of order, an empty section among the first five |
| `LE-QUOTE` | Quote and anchor | a figure line without 「quote」〔anchor〕[S#], a source line without URL / retrieval date, or a `[S#]` that is not registered |
| `LE-NOSELF` | No self-inference, no self-computation | writing "equity method" from the ownership percentage when the quote does not; the figures written as an equation; a ratio without `〔自算〕` or without a denominator |
| `LE-GAP` | Gaps named both ways | body says a gap, the gaps section does not; the gaps section names one, the body has no such line; or "not applicable" used as an excuse |
| `LE-LINE` | Red lines | "has investment value", "investment income will lift profit", "the commitment is achievable", "price target" |

A clean run prints `结论：五道全过（零发条）`.

## 3. Four red lines (what this piece stands on)

1. **Classification and method come only from the quote.** The 20% and 50% thresholds are rules of thumb, not criteria: whether an investee is an associate or a joint venture, whether control exists, and whether the cost or equity method applies is **known only from the disclosure**. This piece does not decide it and does not fill it in from the ownership percentage.
2. **The figures are never netted here.** Investee net profit, the equity-method share of profit and the unrealised-profit elimination each have a disclosed value; investment income recognised and cash dividends received are also two figures. Writing them as an equation subtracts on the disclosure's behalf — the missing one stays `未取到`.
3. **A computed ratio must show its sources.** A ratio not found in the quote carries `〔自算〕` with numerator and denominator, plus which sentence each comes from.
4. **No investment quality calls.** Whether it is worth the money, whether it will be recovered, whether principal is safe, whether to add or exit, whether an earn-out is reasonable, the effect on EPS or the share price, ratings and price targets — all `[待人工]`.

## 4. What one finding looks like

```
- 对乙公司权益法确认损益 12,000,000.00 元「本期按权益法确认对乙公司的投资收益 12,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]
```

The shape is `- item name  value 「quote」〔anchor：location〕[S#]`. All four parts are required (`未取到` lines, `[待人工]` lines and `〔自算〕` lines are the three exceptions).

A computed line looks like this:

```
- 投资收益与现金分红之比 50.00%〔自算〕分子＝本期确认的投资收益 12,000,000.00 元 [S1]｜分母＝本期收到的现金分红 6,000,000.00 元 [S1]
```

That ratio is not in the quote, so it carries `〔自算〕` and states its denominator. **The gap between the two is not filled in on that line** — the gap is either disclosed or written separately as `未取到：两者差额及其披露解释`.

## 5. Where the neighbouring packages take over

| Your question | The package to use |
|---|---|
| Related-party scope, pricing and disclosure | `cue-related-party-terms-cn` |
| Goodwill and long-lived asset impairment risk | `cn-goodwill-impairment-risk` |
| Change of controlling shareholder and control | `cn-controlling-shareholder-change-cn` |
| Period-over-period differences, account reconciliations | `cn-earnings-note` |
| **Which investees, what holdings, which method, how much profit recognised, how impairment and disposals read** | **this package** |

In one line: this package registers how **the long-term equity investment note** reads — it judges neither investment value, nor related-party relationships, nor whether impairment is adequate, and does no cross-period reconciliation review.

## 6. Where the material comes from

- First choice: the long-term equity investment note in the annual report, plus the significant accounting policy paragraphs on method and consolidation scope;
- Second: exchange-filed companions, the long-term investment and outbound investment sections of a prospectus;
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
bash scripts/fixtures/run_fixtures.sh                     # three tiers, count computed on the last line
python3 scripts/check_long_term_equity.py --selftest      # 13 built-in fixtures
python3 tests/test_long_term_equity.py                    # 16 package tests
```

The runner's last line reads `档数=N（由上面逐档现报）｜不合=M｜不可判=K`. **The tier count is never hard-coded in the docs** — add an injection and it changes by itself; hard-coding it drifts sooner or later.

## 8. First-run beacon

The first run (any subcommand) drops an empty file `cue-cn-long-term-equity-investment-cn-YYYY-MM-DD` under `~/.cue-usage/`. Repeated runs on the same day leave exactly one file; an unwritable home directory or a missing `HOME` is skipped silently and never affects the main flow.

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Scope and output contract, in both languages |
| `scripts/check_long_term_equity.py` | five passes; `--selftest` fixtures, `--demo` sample |
| `scripts/fixtures/good-long-term-equity.md` | good sample (same bytes as `--demo`) |
| `scripts/fixtures/bad-long-term-equity.md` | bad sample (one finding per pass) |
| `scripts/fixtures/run_fixtures.sh` | offline runner (three tiers) |
| `tests/test_long_term_equity.py` | package tests (entry contract, zero input, beacon, dedicated counter-proof) |
| `CHANGELOG.md` | change log and the pitfalls hit building v0.1.0 |

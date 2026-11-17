# Cash-Flow Quality · Every Figure Sourced

Give a financial report and get the third statement read into a register where **every number goes back to a quoted sentence**: operating, investing and financing cash flows, plus the net-cash ratio, the collection ratio, free cash flow and the indirect-method reconciliation.

The income statement says how much was earned. This skill says whether **the money was actually collected**.

**No fraud calls, no distress warnings, no forecasts of next period, no ratings, no target prices.** Ratios come from disclosed text only; anything self-computed is flagged and must name where both the numerator and the denominator came from.

---

## 1. Thirty seconds (zero input)

With no data file at all, produce a complete, compliant sample to see what the deliverable looks like and how the checks behave:

```bash
python3 scripts/check_cash_flow.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_cash_flow.py --demo > sample.md
python3 scripts/check_cash_flow.py sample.md
# → sample.md 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_cash_flow.py your-note.md
```

Exit codes: `0` all clear, `1` findings raised, `2` usage error, `3` file unreadable or empty.

### Building a draft from the source report

1. **Fix the subject and the reporting period**, and get the original report — three places matter: the cash-flow statement, the consolidated income statement, and the supplementary cash-flow notes.
2. **Copy facts with their sentences**: one figure = one line, ending in `「quote」〔anchor: page/table〕[S#]`.
3. **Run the checker** and fix whatever turns red:

```bash
python3 scripts/check_cash_flow.py --selftest      # 12 built-in fixtures
```

### Confirming the channel is present (optional)

Only needed once `CUE_API_KEY` is configured. List the catalog first, then confirm the tools are present at the routing address it gives:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a credential the skill still works: put the report in the working directory and use the user-supplied path.

---

## 2. What the five checks enforce

| Code | Name | What it checks | What it most often catches |
|---|---|---|---|
| `CF-STRUCT` | Form | Four self-labels, `主体：` and `报告期：` present; seven sections present and ordered; each of the first five has at least one finding line | A missing section; a heading with nothing under it |
| `CF-QUOTE` | Quote and anchor | Every figure line ends in quote + anchor + `[S#]`; source lines carry a clickable URL and a retrieval date; every cited number is registered | A figure with no quoted sentence; a source line with no link |
| `CF-NOSELF` | No self-computed ratios | Net-cash, collection and FCF values not stated in the quote must be flagged `〔自算〕` with numerator and denominator sources; the reconciliation table may not be merged or absoluted | Dividing operating cash flow by net profit and presenting it as disclosed; collapsing reconciliation rows into a "total" |
| `CF-GAP` | Gaps named both ways | A gap in the body must appear in section six, and vice versa; zero gaps must be stated explicitly | Brushing a gap aside with "not applicable" |
| `CF-LINE` | Red lines | Fraud, distress, prediction, ratings and "worth watching" — zero tolerance | "Positive operating cash flow means no fraud" |

---

## 3. The four red lines

1. **The net-cash ratio is never presented as a disclosed figure.** Operating cash flow and net profit are two different bases; unless the report states the ratio in the same sentence, flag `〔自算〕`.
2. **The indirect-method table is copied item by item.** No merging, no absolute values — the sign is the information.
3. **Free cash flow has no invented definition.** Either copy a disclosed figure, or flag `〔自算〕` and state which line item capex comes from.
4. **Closing cash is not the balance-sheet cash balance.** Restricted cash and the scope of cash equivalents differ; never treat them as equal.

---

## 4. What one finding looks like

```markdown
- 经营活动产生的现金流量净额 12,340.00 万元「经营活动产生的现金流量净额 123,400,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]
```

A self-computed ratio looks like this (numerator and denominator each sourced):

```markdown
- 净现比为 1.21 倍〔自算〕分子＝经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜分母＝归属于母公司所有者的净利润 102,000,000.00 元 [S2]
```

---

## 5. How this differs from the other packages

| You have | Use |
|---|---|
| The cash-flow statement, net-cash, collection and free cash flow | **this skill** |
| Income-statement commentary: period differences, account reconciliation | `cn-earnings-note` |
| Inventory, receivables, contract assets | `cn-working-capital-quality` |
| Goodwill impairment risk | `cn-goodwill-impairment-risk` |
| Dividends, buybacks, reductions | `cn-shareholder-return` |

---

## 6. Zero channel: build the skeleton first

It runs without any channel artifact — the script only reads the listing you give it:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each JSONL line needs `title`, `url` and `asof` (`YYYY-MM-DD`); `id` is optional and defaults to `S1`, `S2`… in line order.

- Bad lines (invalid JSON, missing key, malformed date, non-http url) are **named one by one and not used**; good lines are still taken.
- **An empty listing exits 1** rather than emitting an empty shell.
- The skeleton **fails the checks on purpose** — that is the design, not a defect to fix.

```bash
python3 scripts/make_outline.py --selftest       # 7 built-in fixtures
```

---

## 7. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_cash_flow.py
```

Three tiers: checker self-test / good and bad samples run one by one / line-by-line substitution on the good sample as a positive-and-negative control. Zero network, zero billing; artifacts land only in a temp directory and are deleted afterwards.

The last line reports `档数=3｜不合=N｜不可判=N`; exit `0` all pass, `1` a mismatch, `3` a value-domain fault.

The tests cover the shell contract — `--help` exits 0, no argument exits 2, missing file or empty draft exits 3, `--demo` output passes its own checker, is byte-reproducible and is identical to the good fixture, an empty listing emits no shell, and the beacon lands while failing silently.

---

## 8. First-run beacon

After argument parsing succeeds and before any real work, the entry scripts drop an **empty file** at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing is seeded with 50–60 initial counts in its first 48 hours, and that is not people downloading. This local file is the only evidence this piece has that someone actually installed it and ran it.

**It never gets in the way:** any failure (read-only home, full quota, no `HOME`) is skipped silently — no error, no exit-code change, not a single line of noise. Running it several times in one day still leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Where material comes from

- **User-supplied**: annual reports and announcements you already have, via `+parse`.
- **Channel retrieval**: with `CUE_API_KEY` set, report search and original-text parsing become available. Skill installed ≠ credential configured ≠ channel connected — three separate things.
- **Zero channel**: `make_outline.py` builds the skeleton; see section 6.

This skill issues no requests and pays for nothing; consumption is reported as the server returns it.

---

## 10. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English faces with the check contract |
| `scripts/check_cash_flow.py` | The five checks; `--selftest` runs the fixtures, `--demo` prints the sample |
| `scripts/make_outline.py` | Listing → skeleton; `--selftest` runs the built-in fixtures |
| `scripts/fixtures/` | 1 good + 5 bad + the three-tier runner |
| `tests/test_cash_flow.py` | Package tests (entry contract, zero input, beacon) |

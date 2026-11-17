# Government Grants · Every Figure Sourced

Read **one period's government grants** into a ledger where every figure goes back to a quoted sentence: the overview, the project-by-project register, the accounting treatment, and the disclosed share of profit.

**No earnings-quality verdicts, no compliance findings, no sustainability forecast, no ratings or target prices.** The share-of-profit ratio is copied as disclosed; grants are never summed by this skill.

---

## 1. Thirty seconds (zero input)

With no data file at all, produce a complete, compliant sample to see what the deliverable looks like and how the checks behave:

```bash
python3 scripts/check_gov_grant.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_gov_grant.py --demo > sample.md
python3 scripts/check_gov_grant.py sample.md
# → sample.md 发条=0｜GG-STRUCT=0｜GG-QUOTE=0｜GG-NOSELF=0｜GG-GAP=0｜GG-LINE=0
```

Then point it at your own draft:

```bash
python3 scripts/check_gov_grant.py your-note.md
```

Exit codes: `0` all clear, `1` findings raised, `2` usage error, `3` file unreadable or empty.

---

## 2. What the five checks enforce

| Code | Name | What it checks | What it most often catches |
|---|---|---|---|
| `GG-STRUCT` | Form | Four self-labels before the first `## `; subject, period and data-basis lines present, with the basis starting `政府补助`; six sections present and ordered; each of the first four has a finding line | A missing section; a heading with nothing under it; the basis written as "income-statement review" |
| `GG-QUOTE` | Quote and anchor | Every finding line ends in quote + anchor + `[S#]`; source lines carry a clickable URL and a retrieval date; every cited number is registered | A figure with no quoted sentence; an empty `「」`; a source line with no link |
| `GG-NOSELF` | No self-computed ratios or totals | A share-of-profit percentage must be findable **verbatim inside a quote on the same line**; otherwise it needs `〔自算〕` plus both a numerator and a denominator source; a total word ("合计" / "总计" / "合共") outside the quotes with no quoted sentence raises | Deriving 38.42% from grants ÷ profit and presenting it as disclosed; adding several grants together to stand in for a total |
| `GG-GAP` | Gaps named both ways | A gap in the body must appear in section five, and vice versa; zero gaps must be stated explicitly | Brushing a gap aside with "not applicable" |
| `GG-LINE` | Red lines | Earnings-quality verdicts, compliance findings, ratings, target prices and sustainability forecasts — zero tolerance | "Profit depends heavily on grants"; "suspected fraud"; "expected to continue next year" |

**Negated statements are exempt.** "No grant was returned this period" and "no misappropriation existed" are the disclosure's own sentences — among the most valuable lines in this piece — and the checker explicitly lets them pass.

---

## 3. What this piece exists to prevent

1. **The share is copied, never derived.** 3,842.16 ÷ 10,000 = 38.42% does not appear in the report even when the arithmetic is right.
2. **Grants are never summed here.** If the note gives a total, copy the total. If it lists items without one, register each item and record "not obtained: total".
3. **Current profit and deferred are separate lines.** Merging them erases which grant is still being amortised and which has already hit profit.

---

## 4. What one finding looks like

```markdown
- 本期计入损益的补助总额：「本期计入其他收益的政府补助合计 3,842.16 万元」〔锚：年度报告·附注七·政府补助·第 168 页〕[S1]
```

```markdown
- 补助项目一「智能装备产业化专项」：「智能装备产业化专项补助 1,800.00 万元」〔锚：附注七·政府补助·明细表·第 168 页〕[S1]
```

A self-computed ratio looks like this (numerator and denominator each sourced):

```markdown
- 补助占比〔自算〕分子＝补助 3,842.16 万元 [S1]｜分母＝利润总额 10,000.00 万元 [S2]「本期计入其他收益的政府补助合计 3,842.16 万元」〔锚：附注七·政府补助·第 168 页〕[S1]
```

---

## 5. How this differs from the other packages

| You have | Use |
|---|---|
| The government-grant ledger: projects, amounts, accounting, share of profit | **this skill** |
| Income-statement commentary: revenue, gross margin, period differences | `cn-earnings-note` |
| Tax documents: document number, tax type, rate | `tax-policy-card-cn` |
| Policy impact chains: clause → affected links | `policy-impact-cn` |

---

## 6. Zero channel: build the skeleton first

It runs without any channel artifact — the script only reads the listing you give it:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each JSONL line needs `title`, `url` and `asof` (`YYYY-MM-DD`); `id` and `page` are optional.

- Bad lines (invalid JSON, missing key, malformed date, non-http url) are **named one by one and not used**; good lines are still taken.
- **An empty listing exits 1** rather than emitting an empty shell.
- The skeleton **fails the checks on purpose** — that is the design, not a defect to fix.

```bash
python3 scripts/make_outline.py --selftest       # 8 built-in fixtures
```

---

## 7. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh            # three offline tiers, zero network, zero billing
python3 tests/test_gov_grant.py                  # package tests: entry contract / zero input / beacon
```

The runner has three tiers: checker self-test / good and bad samples one by one / line-by-line substitution on the good sample as a positive-and-negative control. The last line reports `档数=3｜不合=N｜不可判=N`.

The tests cover the shell contract — `--help` exits 0, no argument exits 2, missing file exits 3, `--demo` output passes its own checker and is byte-reproducible, an empty listing emits no shell, and the beacon lands while failing silently.

---

## 8. First-run beacon

After argument parsing succeeds and before any real work, the entry scripts drop an **empty file** at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing is seeded with 50–60 initial counts in its first 48 hours, and that is not people downloading. This local file is the only evidence this piece has that someone actually installed it and ran it.

**It never gets in the way:** any failure (read-only home, full quota, no `HOME`) is skipped silently — no error, no exit-code change, not a single line of noise. Running it several times in one day still leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Where material comes from

- **User-supplied**: the annual reports, notes and announcements you already have, via `+parse`.
- **Channel retrieval**: with `CUE_API_KEY` set, disclosure search and original-text parsing become available. Skill installed ≠ credential configured ≠ channel connected — three separate things.
- **Zero channel**: `--demo` for the shape, `make_outline.py` for the skeleton.

This skill issues no requests and pays for nothing; consumption is reported as the server returns it.

---

## 10. Confirming the channel is present (optional)

Only needed once `CUE_API_KEY` is configured. List the catalog first, then confirm the tools are present at the routing address it gives:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a credential it still runs: `--demo` and `make_outline.py` are both pure-local paths.

---

## 11. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English faces with the check contract |
| `scripts/check_gov_grant.py` | The five checks; `--selftest` runs the fixtures, `--demo` prints the sample |
| `scripts/make_outline.py` | Listing → skeleton; `--selftest` runs the built-in fixtures |
| `scripts/fixtures/` | 1 good sample + 6 bad samples + the three-tier runner |
| `tests/test_gov_grant.py` | Package tests (entry contract, zero input, beacon) |

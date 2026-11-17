# Raised Funds · Use of Proceeds Tracked

Read **one raised-funds report** into a ledger where every figure goes back to a quoted sentence: proceeds, escrow account balances, project spend and disclosed progress, changes, substitutions, top-ups, closing surpluses.

**No compliance calls, no misappropriation findings, no project-merit views, no forward progress, no ratings or target prices.** Progress percentages are copied as disclosed; escrow accounts and projects are never merged into a total.

---

## 1. Thirty seconds (zero input)

With no data file at all, produce a complete, compliant sample to see what the deliverable looks like and how the checks behave:

```bash
python3 scripts/check_raised_funds.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_raised_funds.py --demo > sample.md
python3 scripts/check_raised_funds.py sample.md
# → sample.md 发条=0｜RF-STRUCT=0｜RF-QUOTE=0｜RF-NOSELF=0｜RF-GAP=0｜RF-LINE=0
```

Then point it at your own draft:

```bash
python3 scripts/check_raised_funds.py your-note.md
```

Exit codes: `0` all clear, `1` findings raised, `2` usage error, `3` file unreadable or empty.

---

## 2. What the five checks enforce

| Code | Name | What it checks | What it most often catches |
|---|---|---|---|
| `RF-STRUCT` | Form | Four self-labels before the first `## `; subject, period and data-basis lines present, with the basis starting `募集资金`; six sections present and ordered; each of the first four has a finding line | A missing section; a heading with nothing under it; the basis written as "issuance terms" |
| `RF-QUOTE` | Quote and anchor | Every finding line ends in quote + anchor + `[S#]`; source lines carry a clickable URL and a retrieval date; every cited number is registered | A figure with no quoted sentence; an empty `「」`; a source line with no link |
| `RF-NOSELF` | No self-computed ratios | A progress percentage must be findable **verbatim inside a quote on the same line**; otherwise it needs `〔自算〕` plus both a numerator and a denominator source | Deriving 62.35% from spend ÷ commitment and presenting it as disclosed; flagging `〔自算〕` without a denominator |
| `RF-GAP` | Gaps named both ways | A gap in the body must appear in section five, and vice versa; zero gaps must be stated explicitly | Brushing a gap aside with "not applicable" |
| `RF-LINE` | Red lines and no totals | Compliance findings, project merit, ratings and forward progress — zero tolerance; "合计" or "小计" inside escrow balances or project progress raises | "The company misused the proceeds"; merging two escrow accounts into one total |

**Negated statements are exempt.** "No change occurred" and "no misuse occurred" are the disclosure's own sentences — the most valuable lines in this piece — and the checker explicitly lets them pass.

---

## 3. What this piece exists to prevent

1. **Progress is copied, never derived.** 6,235 ÷ 10,000 = 62.35% does not appear in the report even when the arithmetic is right.
2. **Change and surplus ratios likewise.** Disclosed ⇒ copy; not disclosed ⇒ record as not obtained.
3. **No totals.** One line per escrow account, one line per project. Merging erases which account went empty and which project stalled.

---

## 4. What one finding looks like

```markdown
- 专户一（招商银行深圳分行·末四位 8821）：「余额为人民币 21,340.55 万元」〔锚：专项报告·第 3 页·募集资金专户存储情况〕[S1]
```

```markdown
- 募投项目一「智能制造产线建设项目」：「承诺投入募集资金 45,000.00 万元，报告期末累计投入 28,057.50 万元，投入进度 62.35%」〔锚：专项报告·第 4 页·募集资金投资项目进度表〕[S2]
```

A self-computed ratio looks like this (numerator and denominator each sourced):

```markdown
- 变更情况：投资完成度〔自算〕分子＝累计投入 12,800.00 万元 [S1]｜分母＝承诺投入 32,000.00 万元 [S2]「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页〕[S2]
```

---

## 5. How this differs from the other packages

| You have | Use |
|---|---|
| The raised-funds ledger: escrow, progress, changes | **this skill** |
| Private-placement terms: size, price, subscribers, lock-up | `placement-terms-cn` |
| Convertible-bond terms: rate, conversion price, redemption | `convertible-bond-terms-cn` |
| Restructuring terms: overview, target, pricing, commitments | `ma-restructuring-terms-cn` |
| Dividends, buybacks, reductions | `cn-shareholder-return` |

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
python3 tests/test_raised_funds.py               # package tests: entry contract / zero input / beacon
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

- **User-supplied**: the special reports and announcements you already have, via `+parse`.
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
| `scripts/check_raised_funds.py` | The five checks; `--selftest` runs the fixtures, `--demo` prints the sample |
| `scripts/make_outline.py` | Listing → skeleton; `--selftest` runs the built-in fixtures |
| `scripts/fixtures/` | 1 good sample + 6 bad samples + the three-tier runner |
| `tests/test_raised_funds.py` | Package tests (entry contract, zero input, beacon) |

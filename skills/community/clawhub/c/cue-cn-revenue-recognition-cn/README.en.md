# Revenue Recognition · Five Steps, Every Figure Sourced

Reads revenue recognition in one filing into a register where **every figure traces back to a quoted sentence**: contract identification and portfolios, performance obligations and whether they are distinct, the transaction price and its four adjustments, allocation across obligations, and point-in-time versus over-time recognition with progress.

Revenue is the first line of the income statement and the most judgement-laden note in Chinese filings: **the same cash can be split into different obligations, allocated on different prices and recognised at different moments**, and two annual reports will describe it differently. This piece registers what the disclosure says, line by line. The conclusion stays with the reader.

**No authenticity calls, no fraud calls, no revenue forecasts, no ratings or price targets, no computed expected value.** Splitting and timing come only from the quote; anything this piece computes is flagged and carries its sources.

---

## 1. Thirty seconds, no input

You can produce a full compliant sample without any data file, to see what the output looks like and how the checks bite:

```bash
python3 scripts/check_revenue.py --demo
```

Save it and run the checker on it — it passes itself:

```bash
python3 scripts/check_revenue.py --demo > sample.md
python3 scripts/check_revenue.py sample.md
# → 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_revenue.py your-draft.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable or empty file.

### Without a draft: three steps from the source

1. **Fix the entity and the period**, get the annual or interim report (the revenue note, plus the contract liabilities table).
2. **Copy the facts with the sentence that states them**: one line per item, ending with `「quote」〔锚：page/table〕[S#]`.
3. **Run the self-test and fix one red at a time**:

```bash
python3 scripts/check_revenue.py --selftest
```

### Confirm the channel is live (optional)

Only needed if `CUE_API_KEY` is configured. List the catalog first, then confirm the tools are present at the routing address it gives:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take this group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a key it still works: put the filing in the workspace and use the user-supplied path, at the cost of having only the disaggregation and progress tables that happen to be in the file you hold.

---

## 2. What the five checks cover

| Code | Name | What it judges | Most common catch |
|---|---|---|---|
| `RR-STRUCT` | Shape | four header self-marks, `主体：`, `报告期：`; seven sections present and in order; at least one finding line in each of the first five | a missing section; a section with only a subheading; a duplicated section heading |
| `RR-QUOTE` | Quote and anchor | every finding line ends with 「quote」 + 〔锚：…〕 + `[S#]`; source lines carry a clickable URL and retrieval date; every referenced id is registered | a bare number with no quoted sentence; a source line with a title but no link |
| `RR-NOSELF` | No self-inference, no unsourced maths | splitting and timing only from the quote; a ratio the quote omits must carry `〔自算〕` with numerator and denominator; computed variable consideration states method and cap; computed allocation states the basis | the note lists goods and services, this piece writes "distinct obligation"; variable consideration multiplied out and reported |
| `RR-GAP` | Gaps named both ways | a gap in the body missing from the gaps section fires, and so does the reverse; a zero-gap run must write `未取到：无` | "not applicable", "no such item", "no disclosure required" used as an excuse |
| `RR-LINE` | Red lines | no fabrication, fraud, early recognition, profit smoothing, ratings or price targets; quotes are stripped before judging; contract liability = revenue fires | "revenue is sound, price target 15" |

---

## 3. Four red lines (what this piece stands on)

1. **Splitting only from the quote.** If the note lists "equipment" and "installation" without saying whether each is a distinct obligation, the correct output is "not retrieved", not an industry-habit inference.
2. **Timing only from the quote.** "Delivered and accepted after signing" is not "over time", and "delivered" is not "recognised".
3. **No computed variable consideration.** A quoted method and cap are copied; a computed one must carry `〔自算〕` and, on the same line, which sentence gives the method and which gives the cap or range — both, or it fires.
4. **A contract liability is not revenue.** It is consideration received or receivable for an obligation not yet fulfilled; never written as equal to recognised revenue or as corroborating it.

---

## 4. What a finding looks like

```markdown
- 履约义务·设备销售 单项履约义务「设备销售构成单项履约义务」〔锚：2025 年年报·第 89 页·附注三·收入〕[S1]
```

A gap gets its own line, stated plainly:

```markdown
- 重大融资成分 未取到：附注未披露重大融资成分
```

A computed ratio carries both sources:

```markdown
- 设备销售占比 75.00%〔自算〕分子＝设备销售单独售价 90,000,000.00 元 [S1]｜分母＝各履约义务单独售价合计 120,000,000.00 元 [S1]
```

---

## 5. How it splits from the neighbouring packages

| What you have | Which package |
|---|---|
| Revenue recognition, five steps, obligations, variable consideration, allocation, timing | **this one** |
| Period-over-period differences and account reconciliation commentary | `cn-earnings-note` |
| The three cash-flow statements, cash conversion, free cash flow | `cn-cash-flow-quality` |
| Inventory, trade receivables, contract assets — balances and ageing | `cn-working-capital-quality` |
| Reviewing the contract clauses themselves | `cn-contract-clauses` |

Cash conversion lives on the cash-flow statement: **this piece points at it in one line in the basis section and does not recompute it**.

---

## 6. Where the material comes from

- **User-supplied**: the annual report PDF or announcement in hand, read into searchable text through the parsing channel.
- **Channel retrieval**: with `CUE_API_KEY` configured, filing search and original-text parsing are available. Installed ≠ key configured ≠ channel connected — three different states.
- **The notes sit inside documents hundreds of pages long** (disaggregation, contract liabilities, progress tables); long attachments and scans go through the parsing leg: outline first, then section by section. Billing and availability follow what the server returns.

This piece sends no requests on its own account and pays for nothing; consumption follows the server's response.

---

## 7. Running the fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_revenue.py
```

Three tiers: the checker's self-test / good and bad samples run one at a time / positive and negative mutations applied to the good sample (what should fire fires, what should not stays quiet). No network, no billing; artefacts land only in a temp directory and are removed afterwards.

The last line self-reports the tier count, which the runner computes itself rather than hard-coding; exit `0` all clear, `1` a mismatch, `3` a fixture-domain failure.

`tests/` covers the shell contract: `--help` exits 0, no argument exits 2, a missing or empty file exits 3, `--demo` output passes its own checker and is byte-identical to the good fixture, and the beacon lands without ever disturbing the run.

---

## 8. First-run beacon

After parsing arguments and before doing any work, the entry script drops an empty file at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing gets 50–60 seeded in its first 48 hours, and that is not users downloading. This local file is the only evidence that someone actually installed and ran this piece.

**It never gets in the way:** any failure (read-only home, full quota, no HOME) is skipped silently — no error, no exit-code change, no noise. Running it several times a day leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English skill description and check contract |
| `scripts/check_revenue.py` | five checks; `--selftest` runs the built-in fixtures, `--demo` prints a sample |
| `scripts/fixtures/` | one good sample + one bad sample + the three-tier runner |
| `tests/test_revenue.py` | package tests (entry contract, zero input, beacon) |

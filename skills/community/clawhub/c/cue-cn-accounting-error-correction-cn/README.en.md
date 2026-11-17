# Prior-Period Error Correction · Every Line Sourced

Reads a prior-period error correction in one filing into a register where **every figure can be traced back to a quoted sentence**: the nature of the error and when it was discovered, the correction method and its basis, the accounts affected with restated amounts for each period, the effect on opening retained earnings and the comparatives, and the line between an accounting policy change, an accounting estimate change and a prior-period error.

A correction announcement is often only a few pages, yet it has to answer five questions at once: **what went wrong, when was it found, which method corrected it, how much changed, and how does it differ from a "policy change / estimate change"**. Disclosures often blur these together, or give the amounts without the basis. This piece registers what the disclosure says, line by line; the conclusion stays with the human.

**It does not judge whether the error is fraud, whether management acted deliberately, whether the corrected statements can be trusted, what it means for the share price or delisting, and gives no rating or price target.** Nature and method come only from the quote; a ratio you compute yourself must be listed separately with the impact source plus numerator and denominator.

---

## 1. Thirty seconds, no input

With no data file at all, you can still get a complete, compliant sample to see what the output looks like and how the checks fire:

```bash
python3 scripts/check_correction.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_correction.py --demo > sample-correction.md
python3 scripts/check_correction.py sample-correction.md
# → 结论：五道全过（零发条）
```

Then swap in your own draft:

```bash
python3 scripts/check_correction.py your-correction.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable or empty file.

### Starting from the source instead, in three steps

1. **Fix the entity and the reporting period**, and get the correction announcement plus the "prior-period error correction" note section.
2. **Copy facts section by section, quotes included**: one item = one line, ending with `「quote」〔锚：page/table〕[S#]`.
3. **Run the self-test** and fix one red at a time:

```bash
python3 scripts/check_correction.py --selftest
```

### Confirming the channel is there (optional)

Only needed if `CUE_API_KEY` is configured. List the catalog first, then confirm the tools exist at the routing address it gives you:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without credentials it still works: put the announcement and notes in the workspace and use the user-supplied route, at the cost of the cumulative-effect table and the comparative restatement note being limited to what is in hand.

---

## 2. What the five checks cover

| Code | Name | Judges | Most often catches |
|---|---|---|---|
| `EC-STRUCT` | Shape | Four header self-marks, `主体：` and `报告期：` present; seven sections in order; at least one finding line in each of the first five | A missing section; a section with only subheadings; a duplicated section heading |
| `EC-QUOTE` | Quote and anchor | Every finding line ends with 「quote」+〔锚：…〕+`[S#]`; source lines carry a clickable URL and retrieval date; every referenced id is registered | Amounts without the quote; source lines with a title but no link |
| `EC-NOSELF` | No self-inference | Nature, method and the three-way line only from the quote; a ratio the quote omits must carry `〔自算〕` with numerator and denominator; a computed restatement figure must state which sentence gives the cumulative effect or opening balance | The quote only says "the amount is large" and the piece writes "material prior-period error, retrospective restatement" itself |
| `EC-GAP` | Gaps named both ways | A gap in the body must be listed in the gaps section and vice versa; a zero-gap run must write 「未取到：无」 | Fobbing off with 「不适用」「无此项」「无需披露」 |
| `EC-LINE` | Red lines | Zero hits for fraud, deliberate intent, whitewashing, fabricated or inflated figures, "corrected statements are reliable", delisting risk, share-price impact, ratings and price targets; quotes are stripped before judging; treating the three kinds of change as equal fires | "There is no fraud in this correction and the corrected statements are reliable" |

---

## 3. Four lines this piece holds

1. **Nature only from the quote.** If the announcement lists adjustments without saying this is a prior-period error, write not retrieved — deciding it is an error is the disclosure's accounting judgement, not this piece's.
2. **Method only from the quote.** "The amount is material, so it should have been restated retrospectively" is not a basis; "corrected" is not "retrospectively restated".
3. **The three changes are not one thing.** A policy change, an estimate change and a prior-period error carry different treatment and disclosure requirements; writing them as equal, equivalent to, or substitutes for one another erases the line the disclosure drew.
4. **No computed restatement.** The cumulative effect and the effect on profit are copied, never computed; a ratio you compute must carry `〔自算〕` with the impact source and both numerator and denominator on the same line.

---

## 4. What one finding looks like

```markdown
- 更正方法 追溯重述法「本公司采用追溯重述法对该项前期差错进行更正」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
```

Missing items get their own line, stated plainly:

```markdown
- 每股收益重述金额 未取到：更正公告未列示每股收益重述数
```

Computed figures look like this (impact source and both numerator and denominator each carry their own source):

```markdown
- 重述金额较原披露数变动 3.00%〔自算〕累积影响取附注「上述差错累积影响数为 3,200,000.00 元」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]｜分子＝2024 年度营业收入调减 12,000,000.00 元 [S1]｜分母＝2024 年度原披露营业收入 400,000,000.00 元 [S1]
```

---

## 5. How it splits from the sibling packages

| What you have | Which package |
|---|---|
| Prior-period error correction, retrospective restatement, restated amounts, opening retained earnings adjustment | **This one** |
| Period-over-period differences and account reconciliations | `cn-earnings-note` |
| Revenue recognition, five steps, performance obligations | `cn-revenue-recognition-cn` |
| The three cash-flow statements, net cash ratio, free cash flow | `cn-cash-flow-quality` |
| Audit opinion type (qualified / disclaimer / adverse) | `cn-audit-opinion-cn` |

A correction announcement often lands the same day as the audit opinion and a cash-flow change, but they are three different things: **this piece registers the correction only**; the opinion type belongs to `cn-audit-opinion-cn`.

---

## 6. Where the material comes from

- **User-supplied**: the correction announcement PDF and the annual report in hand, read into searchable text through the parsing channel.
- **Channel retrieval**: with `CUE_API_KEY`, announcements can be searched and source text parsed. Skill installed ≠ credentials configured ≠ channel connected — three separate layers.
- **Correction material is usually in two places** (the announcement as its own document, the note tables buried hundreds of pages into the annual report). Long attachments and scans go to the parsing leg: outline first, then section by section. Billing and availability follow the server.

This piece makes no requests and pays no fees; consumption follows what the server returns.

---

## 7. Running fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_correction.py
```

Three tiers: checker self-test / good and bad samples run one by one / substitutions on the good sample as positive and negative controls (what should fire does, what should not doesn't). No network, no billing; artefacts land only in a temp directory and are removed afterwards.

The last line self-reports 「档数=…｜不合=N｜不可判=N」 (the tier count is computed by the runner, never hard-coded); exit codes `0` all clear, `1` failures, `3` value-domain fault.

`tests/` covers shell properties: `--help` exits 0, no argument exits 2, missing or empty file exits 3, the `--demo` output passes its own checker and is byte-identical to the good fixture, and the beacon lands without ever breaking the run.

---

## 8. First-run beacon

After parsing arguments and before doing the work, the entry script drops an **empty file** at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing is seeded with 50–60 initial counts in its first 48 hours, and those are not users. This local file is the only evidence that someone actually installed and ran the piece.

**It never gets in the way:** any failure (read-only home directory, full quota, no HOME) is skipped silently — no error, no change to the exit code, not a word of noise. Running several times in one day leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English skill descriptions and checker contract |
| `scripts/check_correction.py` | five checks; `--selftest` runs fixtures, `--demo` prints a sample |
| `scripts/fixtures/` | one good sample, one bad sample, three-tier runner |
| `tests/test_correction.py` | package tests (entry contract, zero input, beacon) |

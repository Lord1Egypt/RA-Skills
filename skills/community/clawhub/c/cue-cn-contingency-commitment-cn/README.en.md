# Contingencies & Commitments · Every Line Sourced

Reads the contingencies and commitments note in a filing into a register where **every figure can be traced back to a quoted sentence**: contingencies (litigation and arbitration, guarantees, discounted commercial acceptance notes, product warranties, restructuring obligations, onerous contracts), commitments (capital, operating lease, investment and large contract), the line between a recognised provision and a disclosed contingent liability, the boundary against subsequent events and related-party guarantees, and the litigation stage with the amount claimed.

Contingencies are **the block most often dismissed in one line, and the one most likely to surprise**: the guarantee balance sits in a detail table, the litigation progress in another, and whether a provision was made in a single sentence of body text. For the same event, one company recognises a provision and another discloses a contingent liability only — **these are not the same treatment**, and blurring them erases the line. This piece registers what the disclosure says, line by line; the conclusion stays with the human.

**It does not estimate loss probability or damages, does not judge whether this triggers default or delisting, does not assess solvency, and gives no rating or price target.** Nature, derecognition, litigation stage and boundaries come only from the quote; a ratio you compute must be listed separately with the amount's source plus numerator and denominator.

---

## 1. Thirty seconds, no input

With no data file at all, you can still get a complete, compliant sample to see what the output looks like and how the checks fire:

```bash
python3 scripts/check_contingency.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_contingency.py --demo > sample-contingency.md
python3 scripts/check_contingency.py sample-contingency.md
# → 结论：五道全过（零发条）
```

Then swap in your own draft:

```bash
python3 scripts/check_contingency.py your-contingency.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable or empty file.

### Starting from the source instead, in three steps

1. **Fix the entity and the reporting period**, and get the "contingencies", "commitments" and "provisions" note sections plus the related announcements.
2. **Copy facts section by section, quotes included**: one item = one line, ending with `「quote」〔锚：page/table〕[S#]`.
3. **Run the self-test** and fix one red at a time:

```bash
python3 scripts/check_contingency.py --selftest
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

Without credentials it still works: put the notes and announcements in the workspace and use the user-supplied route, at the cost of the guarantee detail and litigation progress tables being limited to what is in hand.

---

## 2. What the five checks cover

| Code | Name | Judges | Most often catches |
|---|---|---|---|
| `CC-STRUCT` | Shape | Four header self-marks, `主体：` and `报告期：` present; seven sections in order; at least one finding line in each of the first five | A missing section; a section with only subheadings; a duplicated section heading |
| `CC-QUOTE` | Quote and anchor | Every finding line ends with 「quote」+〔锚：…〕+`[S#]`; source lines carry a clickable URL and retrieval date; every referenced id is registered | Amounts without the quote; source lines with a title but no link |
| `CC-NOSELF` | No self-inference | Nature, derecognition, litigation stage and the boundary only from the quote; a ratio the quote omits must carry `〔自算〕` with numerator and denominator; a computed contingent amount must state which sentence gives it | The quote only says "discounted" and the piece writes "not derecognised" itself; "filed" becomes "first instance decided" |
| `CC-GAP` | Gaps named both ways | A gap in the body must be listed in the gaps section and vice versa; a zero-gap run must write 「未取到：无」 | Fobbing off with 「不适用」「无此项」「无需披露」 |
| `CC-LINE` | Red lines | Zero hits for loss probability, estimated damages, default, delisting risk, solvency, "risk under control", ratings and price targets; quotes are stripped before judging; a provision written as equal to a contingent liability fires | "This case has a high chance of winning, it will not lose" |

---

## 3. Four lines this piece holds

1. **Nature only from the quote.** If the note lists a guarantee balance without saying whether it is accrued, the correct answer is not retrieved — not "guarantees normally need a provision".
2. **Derecognition only from the quote.** "Discounted" is not "derecognised" — a discounted note *with recourse* is precisely the contingency. This judges evidence provenance, not a banned-word list.
3. **A provision is not a contingent liability.** The first is recognised on the balance sheet, the second disclosed in the note only; not the same figure, not the same treatment, never written as equal or as substitutes.
4. **No computed contingent amount.** A ratio you compute must carry `〔自算〕` with the amount's source and both numerator and denominator on the same line.

---

## 4. What one finding looks like

```markdown
- 已贴现商业承兑票据 500.00 万元「已贴现未到期的商业承兑票据 5,000,000.00 元，附追索权，本公司未终止确认」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]
```

Missing items get their own line, stated plainly:

```markdown
- 亏损合同 未取到：附注未披露亏损合同
```

Computed figures look like this (amount source and both numerator and denominator each carry their own source):

```markdown
- 担保余额占净资产比例 3.00%〔自算〕金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜分子＝担保余额 30,000,000.00 元 [S1]｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]
```

---

## 5. How it splits from the sibling packages

| What you have | Which package |
|---|---|
| Contingencies, commitments, provision vs contingent liability, litigation, guarantees | **This one** |
| Period-over-period differences and account reconciliations | `cn-earnings-note` |
| Note classification, endorsement, bad-debt provisions | `cn-notes-receivable-cn` |
| Nine-category public-information coverage and anchored fact tables | `dd-checklist` |
| Penalties and regulatory measures | `event-risk-scan` |
| Audit opinion type, key audit matters | `cn-audit-opinion-cn` |

Discounted notes are the seam between two packages: **the note itself (classification, endorsement, bad-debt) belongs to `cn-notes-receivable-cn`; the recourse after discounting belongs here** — this piece registers only the "with recourse, not derecognised" layer under contingencies.

---

## 6. Where the material comes from

- **User-supplied**: the annual report PDF and announcements in hand, read into searchable text through the parsing channel.
- **Channel retrieval**: with `CUE_API_KEY`, announcements can be searched and source text parsed. Skill installed ≠ credentials configured ≠ channel connected — three separate layers.
- **Contingency material is scattered across several tables** (guarantee detail, litigation progress, commitment maturity). Long attachments and scans go to the parsing leg: outline first, then section by section. Billing and availability follow the server.

This piece makes no requests and pays no fees; consumption follows what the server returns.

---

## 7. Running fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_contingency.py
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
| `scripts/check_contingency.py` | five checks; `--selftest` runs fixtures, `--demo` prints a sample |
| `scripts/fixtures/` | one good sample, one bad sample, three-tier runner |
| `tests/test_contingency.py` | package tests (entry contract, zero input, beacon) |

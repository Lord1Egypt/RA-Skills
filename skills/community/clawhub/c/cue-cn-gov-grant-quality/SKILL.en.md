---
name: cn-gov-grant-quality
slug: cue-cn-gov-grant-quality
displayName: "Government Grants · Deferred Income · Profit Reliance"
summary: "Gov-grant ledger: projects, amounts, accounting, share of profit — all sourced."
description: "One annual report's government grants into a sourced ledger: projects, amounts, accounting treatment, share of profit. Ratios copied as disclosed, never divided. No earnings-quality verdicts, no ratings. Triggers: government grants / grant income / deferred income / profit reliance"
version: "0.2.0"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    envVars:
      - name: CUE_API_KEY
        required: false
        desc: "Optional credential: without it the skill only lays out a skeleton from user-supplied files; with it, disclosure search and original-text parsing become available."
tags: [government-grants, deferred-income, other-income, annual-report, disclosure]
---

# Government Grants · Every Figure Sourced

## 0. What this is, and what it is not

| Is | Is not |
|---|---|
| A per-item ledger of one period's government grants | A verdict on the company's earnings quality |
| Project names, amounts and recognition basis copied from the notes | A view on whether a grant *should* have been given |
| The accounting treatment copied as stated (other income vs deferred) | A "reliance ratio" the note computes itself |
| The share-of-profit figure exactly as disclosed | A forecast of whether the grants will continue |

**Three boundaries (how users tell this apart from its neighbours):**

- `cn-earnings-note` works from the **income statement**, figure by figure. This piece covers **the government-grant line only**; how the amounts enter the income statement is an input to that piece's work, not a substitute for it.
- `tax-policy-card-cn` breaks down **tax documents** (document number, tax type, rate). This piece breaks down **the company's own grant detail**, not a policy document.
- `policy-impact-cn` builds an **impact chain** from a policy to affected links. This piece builds no chain — it registers how much this company actually received and how it booked it.

**"Never divide" means two things here:**

1. **The share-of-profit ratio is the disclosed figure.** If the note states "government grants were 38.42% of total profit", copy that sentence. A 38.42% the note derives from 3,842 ÷ 10,000 does not exist in the report and is not allowed even when the arithmetic matches.
2. **Never add up the grants yourself.** If the note gives a total, copy the total. If it lists items without a total, register each item and record "not obtained: total" — do not sum them into one.

## 1. When to use it

- "How much in government grants did this company receive?" / "Which projects?"
- "Is the grant in current profit or deferred?" / "Which line item?"
- "How much of profit came from grants?" — the **disclosed** ratio, not one this skill computes.
- "What is the stated recognition basis?"

**Do not use** for income-statement commentary (`cn-earnings-note`); tax-document breakdowns (`tax-policy-card-cn`); policy impact chains (`policy-impact-cn`); compliance findings, earnings-quality verdicts, ratings or target prices (this skill does not produce them, and no skill should).

## 2. Sourcing discipline

1. **Only the company's own disclosures.** The annual report's government-grant note, the deferred-income note, the other-income note, and dedicated announcements. Broker notes, news and forum posts are not sources.
2. **Quote every item.** Write `- item：「verbatim sentence」〔anchor: page/table〕[S#]`.
3. **Copy the ratio.** See section 0.
4. **Amounts are not rewritten.** If the note says 3,842.16 万元, write that — not "about 3,800万".
5. **Current profit and deferred are registered separately.** One grant can split between the two; each part gets its own line and its own source. Never merged into one line.
6. **A gap is written as a gap, checked both ways.** Body says "not obtained: X" ⇒ section five names X; section five names X ⇒ the body says it. Zero gaps: `- 未取到：无`.
7. **No sustainability inference.** "Is this grant recurring?" is a judgement; this piece registers what the disclosure says.

## 3. Output contract (six sections, in order)

```
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：<company>
报告期：<fiscal year or as-of date>
数据口径：政府补助（附注逐项登记，不评盈利质量）

## 一、补助概况
## 二、分项登记
## 三、会计处理
## 四、与利润的关系
## 五、未取到与口径
## 六、来源
```

The four self-labels, the three header lines and the six section headings are fixed strings — the checker matches them literally, so they are not a translation surface.

- **一、补助概况**: total recognised in profit this period, closing deferred-income balance, number of projects — each sourced; anything the note omits is recorded as a gap.
- **二、分项登记**: one project per line with its name and amount. Where there are many, take the first few **in the note's own order** and note "N further items in the note" — never reorder, never pick the largest.
- **三、会计处理**: which line item each grant goes to (other income / non-operating income / deferred income), copied as the note states it.
- **四、与利润的关系**: the share of total (or net) profit — **only the disclosed figure**. If not disclosed, record it as a gap and state that this piece does not divide.
- **五、未取到与口径**: gaps named one by one, plus a line stating what was copied and what was not obtained.
- **六、来源**: one line per source — `- [S#] title｜URL｜检索日 YYYY-MM-DD`.

## 4. Channel

The skill takes disclosures through Cue's MCP channel. List the catalog first, then call `tools/list` at the routing address it returns, so you are working from tools that are actually present:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Once you have the notes, `scripts/make_outline.py` turns a listing into the skeleton.

## 5. Red lines

- **No earnings-quality verdict.** "Profit depends heavily on grants", "surviving on subsidies", "poor earnings quality" — zero tolerance. Those are judgements, not disclosures.
- **No compliance finding.** "Suspected of grant fraud", "insufficient basis" — zero tolerance.
- **No ratings, target prices, investment advice, buy/sell advice.**
- **No sustainability forecast** — no "expected to continue next year", no "of doubtful continuity".
- **No hedging in place of the note's own figures.**
- **No self-summing, no self-dividing.** See section 0.

## 6. Quick flow

1. Get the government-grant, deferred-income and other-income notes; fix the company and the period.
2. Copy the total recognised in profit and the closing deferred balance.
3. Copy each project and amount, in the note's own order.
4. Copy the accounting treatment.
5. Copy the disclosed share of profit; if not disclosed, record it as a gap.
6. Write the gaps and the basis line, aligned both ways.
7. Run `python3 scripts/check_gov_grant.py your-note.md`.

Not sure where to start? Run the built-in sample first:

```bash
python3 scripts/check_gov_grant.py --demo
```

## 7. The checks

```bash
python3 scripts/check_gov_grant.py your-note.md   # five checks; rc 0 clear / 1 findings / 3 unreadable or empty
python3 scripts/check_gov_grant.py --selftest     # built-in fixtures
python3 scripts/check_gov_grant.py --demo         # a complete compliant sample, zero input
bash scripts/fixtures/run_fixtures.sh             # three offline tiers, zero network, zero billing
```

`GG-STRUCT` form / `GG-QUOTE` quote and anchor / `GG-NOSELF` no self-computed ratios or totals / `GG-GAP` gaps both ways / `GG-LINE` red lines.

**Negated statements are exempt.** "No grant was returned this period" is the note's own sentence and passes.

## 8. Zero channel

Without `CUE_API_KEY` the skill **produces no content**; it lays out a skeleton from the listing you supply, leaving content as `[待人工]`. The skeleton fails the checks by design — a reminder to finish it, not a shell pretending to be a deliverable.

The cost, stated plainly: **no channel means no notes, no notes means no quoted sentence, and the item-by-item register — the body of this ledger — cannot be anchored.** What remains is a handful of figures the user typed in. Use `--demo` to see the finished shape; it costs nothing and touches no channel.

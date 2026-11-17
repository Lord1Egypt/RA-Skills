---
name: cn-raised-funds-tracker
slug: cue-cn-raised-funds-tracker
displayName: "Raised Funds · Use of Proceeds Tracked"
summary: "Raised-funds ledger: accounts, project progress, changes, every line sourced."
description: "One raised-funds report into a sourced ledger: proceeds, escrow accounts, project spend and progress, changes and substitutions. No compliance calls, no ratings. Triggers: raised funds / use of proceeds / project progress / escrow account / capex"
version: "0.1.0"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    envVars:
      - name: CUE_API_KEY
        required: false
        desc: "Optional credential: without it the skill only lays out a skeleton from user-supplied files; with it, disclosure search and original-text parsing become available."
tags: [raised-funds, use-of-proceeds, project-progress, escrow, disclosure]
---

# Raised Funds · Use of Proceeds Tracked

## 0. What this is, and what it is not

| Is | Is not |
|---|---|
| A ledger of one fundraising's life, from receipt to completion | The issuance terms themselves (price, lock-up, subscribers) |
| Escrow balances and project spend registered period by period | A judgement on whether the project is worth funding |
| Changes, substitutions, top-ups and closing surpluses copied one by one | A view on whether a change is "compliant" or "problematic" |
| Progress percentages copied as disclosed | A percentage the note computes by dividing two figures |

**Three boundaries (how users tell this apart from its neighbours):**

- `placement-terms-cn` covers **issuance terms** — the ten items in a private-placement plan. This piece starts **after the money arrives** and tracks how it is spent.
- `convertible-bond-terms-cn` covers **convertible-bond terms**. This piece never touches the bond terms, only the use-of-proceeds ledger.
- `ma-restructuring-terms-cn` covers **restructuring filings**. This piece follows only the escrow-account line.

**"Never divide" means two things here:**

1. **Progress is the disclosed percentage.** The special report normally states "cumulative investment progress 62.35%" — copy that sentence. A 62.35% the note derives from 6,235 ÷ 10,000 does not exist in the report, and is not allowed even when the arithmetic matches.
2. **Change ratios and surplus ratios likewise.** If disclosed, copy; if not, record it as not obtained rather than computing it.

## 1. When to use it

- "Where did the placement proceeds go?" / "How far along are the projects?"
- "How much is left in the escrow accounts?" / "Was any used as working capital?"
- "Were the projects changed, and which ones?"
- "Was there a substitution of prior self-funded spend?" / "What surplus was left at completion?"

**Do not use** for issuance terms (`placement-terms-cn`); convertible-bond terms (`convertible-bond-terms-cn`); restructuring filings (`ma-restructuring-terms-cn`); compliance findings, misappropriation calls, ratings or target prices (this skill does not produce them, and no skill should).

## 2. Sourcing discipline

1. **Only the company's own disclosures.** The special report on raised funds, the annual assurance report, change announcements, completion announcements. Broker notes, news and forum posts are not sources.
2. **Quote every item.** Write `- item：「verbatim sentence」〔anchor: page/table〕[S#]`.
3. **Copy the progress figure.** See section 0.
4. **Amounts are not rewritten.** If the disclosure says 6,235.00 万元, write that — not "about 6,200万".
5. **One period per line, no cross-period merging.** The same project at 2024-12-31 and 2025-06-30 gets two lines with their own `[S#]`; no averaging, no overwriting the older figure.
6. **A gap is written as a gap, checked both ways.** Body says "not obtained: X" ⇒ section five names X; section five names X ⇒ the body says it. Zero gaps: `- 未取到：无`.
7. **No compliance judgement.** "Was it misused?" and "does it constitute fund occupation?" are conclusions; this piece registers what the disclosure says.

## 3. Output contract (six sections, in order)

```
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：<company>
报告期：<YYYY-MM-DD as-of date, or fiscal year>
数据口径：募集资金存放与实际使用情况（存续期台账）

## 一、募集概况
## 二、专户余额
## 三、投入进度
## 四、变更与置换
## 五、未取到与口径
## 六、来源
```

The four self-labels, the three header lines and the six section headings are fixed strings — the checker matches them literally, so they are not a translation surface.

- **一、募集概况**: method, gross proceeds, net proceeds, receipt date — each sourced.
- **二、专户余额**: one line per escrow account (bank + last four digits + balance). No single "total" line — merging erases which account is empty.
- **三、投入进度**: one line per project, carrying the committed amount, the cumulative spend and the disclosed progress percentage, each quoted or all three inside one quoted sentence.
- **四、变更与置换**: change / substitution / working-capital top-up / closing surplus, one line each, with before-and-after project names and amounts. If none happened, copy the disclosure's own "no change occurred" sentence.
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

Once you have the special report, `scripts/make_outline.py` turns a listing into the skeleton.

## 5. Red lines

- **No compliance finding, no misuse call.** "Misused", "constitutes fund occupation", "already diverted" — zero tolerance. That is for regulators and courts.
- **No project merit.** Not "strong prospects", not "capacity absorption in doubt".
- **No ratings, target prices, investment advice, buy/sell advice.**
- **No forward progress.** Not "expected to reach production this year" unless it is the disclosure's own sentence, quoted.
- **No hedging in place of the disclosure's own words.**
- **No totals across accounts or projects.** Merging erases which escrow account went empty and which project stalled.

## 6. Quick flow

1. Get the special report (or the annual assurance report), fix the company and the as-of date.
2. Copy the four proceeds facts, then each escrow balance.
3. Copy each project's committed amount, cumulative spend and disclosed progress.
4. Copy changes and substitutions; if none, copy the "no change occurred" sentence.
5. Write the gaps and the basis line, aligned both ways.
6. Run `python3 scripts/check_raised_funds.py your-note.md` and fix what turns red.

Not sure where to start? Run the built-in sample first:

```bash
python3 scripts/check_raised_funds.py --demo
```

## 7. The checks

```bash
python3 scripts/check_raised_funds.py your-note.md   # five checks; rc 0 clear / 1 findings / 3 unreadable or empty
python3 scripts/check_raised_funds.py --selftest     # built-in fixtures
python3 scripts/check_raised_funds.py --demo         # a complete compliant sample, zero input
bash scripts/fixtures/run_fixtures.sh                # three offline tiers, zero network, zero billing
```

`RF-STRUCT` form / `RF-QUOTE` quote and anchor / `RF-NOSELF` no self-computed ratios / `RF-GAP` gaps both ways / `RF-LINE` red lines and no totals.

**Negated statements are exempt.** "No change occurred" and "no misuse occurred" are the disclosure's own sentences — the most valuable lines in this piece — and the checker explicitly lets them pass.

## 8. Zero channel

Without `CUE_API_KEY` the skill **produces no content**; it lays out a skeleton from the listing you supply, leaving content as `[待人工]`. The skeleton fails the checks by design — a reminder to finish it, not a shell pretending to be a deliverable.

The cost, stated plainly: **no channel means no special report, no report means no quoted sentence, and the progress cell — the load-bearing cell of this ledger — cannot be anchored.** What remains is a handful of figures the user typed in. Use `--demo` to see the finished shape; it costs nothing and touches no channel.

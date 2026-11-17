---
name: cn-cash-flow-quality
slug: cue-cn-cash-flow-quality
displayName: "Cash-Flow Quality · Every Figure Sourced (现金流质量)"
summary: "Cash-flow quality: three flows, net-cash and collection ratios, FCF; sourced."
description: "Three cash-flow statements, net-cash and collection ratios, FCF; each figure quoted with anchor and [S#]. Ratios only from disclosed text, else flagged with numerator and denominator sources. No fraud calls, forecasts or ratings. Triggers: cash flow / net-cash ratio / collection ratio / FCF"
version: "0.2.0"
license: MIT
tags: [cash-flow, net-cash-ratio, collection-ratio, free-cash-flow, indirect-method]
---

# Cash-Flow Quality · Every Figure Sourced

**What it does**: reads the third statement — the cash-flow statement — into a register where every number goes back to a quoted sentence.

**It is not** a fraud opinion, not a distress warning, not a rating report.

## 1. Six sections

| # | Section | Records |
|---|---|---|
| 1 | Operating cash flow | net operating cash flow and its main items |
| 2 | Investing cash flow | net investing cash flow, capex on long-lived assets |
| 3 | Financing cash flow | net financing cash flow, borrowings, repayments, dividends and interest |
| 4 | Net-cash and collection ratios | net-cash = operating cash flow ÷ net profit; collection = cash from sales ÷ revenue; FCF = operating cash flow − capex |
| 5 | Indirect-method reconciliation | item by item, copied verbatim |
| 6 | Basis and gaps | basis notes and every gap named |

## 2. Quote and anchor (CF-QUOTE)

```
- Operating cash flow 123.40m 「经营活动产生的现金流量净额 123,400,000.00 元」〔锚:2025 annual report · p.58〕[S1]
```

The quote is contiguous, the anchor names page/section/table, the reference matches a source line. Source lines carry a clickable URL and a retrieval date.

## 3. Four red lines

1. **The net-cash ratio is never presented as a disclosed figure.** Operating cash flow and net profit are two different bases. If the report does not state the ratio in the same sentence, flag `〔自算〕` and name both sources.
2. **The indirect-method table is copied item by item.** No merging, no absolute values — the sign is the information.
3. **Free cash flow has no invented definition.** Either copy a disclosed figure, or flag `〔自算〕` and state which line item capex comes from.
4. **Closing cash is not the balance-sheet cash balance.** Restricted cash and the scope of cash equivalents differ; never treat them as equal.

## 4. Channel check (optional)

Only needed with `CUE_API_KEY` set:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 5. Zero-channel path

With no data file at all you can still see what the deliverable looks like:

```bash
python3 scripts/check_cash_flow.py --demo
```

`scripts/make_outline.py` builds a skeleton from your material listing — it never needs a parsed doc:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each line needs `title`, `url` and `asof` (`YYYY-MM-DD`). Bad lines are named one by one and not used; an empty listing exits 1 rather than emitting an empty shell. A skeleton failing the checks is by design.

## 6. Files

`SKILL.md` / `SKILL.en.md` / `README.md` / `README.en.md` / `CHANGELOG.md` / `scripts/check_cash_flow.py` / `scripts/make_outline.py` / `scripts/fixtures/` / `tests/test_cash_flow.py`.

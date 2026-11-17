# fund-facts-cn

**Give it one mainland fund document and get back an eight-item verbatim card: type, investment scope, benchmark, management and custody fees, subscription and redemption fees, manager, risk level, distribution rules - each item carrying a verbatim quote and a source anchor. Return forecasts stay `[待人工]`.**

It reads one fund document only: policy impact chains live in `policy-impact-cn`, bond terms in `bond-terms-cn`, company filing lists in `announcement-daily-cn`. The official documents are the only authority - **sales pages must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over one document: product summary, prospectus excerpt, or sales page. For anything it does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the fee cells: management, custody, subscription and redemption fees stay verbatim; "subject to the fund contract" and "depends on the channel" are not values and belong in the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_fund_card.py` gates the card: five sections plus item-level presence of the eight names / quote and anchor per item / red-line assertions only on `[待人工]` lines / exactly one completeness declaration reconciled with the number of `未检索到` lines / the fee items must carry a percentage and deferred wording fires.

```bash
python3 scripts/check_fund_card.py --help                          # usage
python3 scripts/check_fund_card.py --selftest                       # good sample passes, bad sample fires all five lanes, five threshold pins, temp files clean themselves
python3 scripts/check_fund_card.py scripts/fixtures/good-fund-card.md    # PASS (zero findings)
python3 scripts/check_fund_card.py scripts/fixtures/bad-fund-card.md     # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r fund-facts-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-fund-card.md
python3 ~/.workbuddy/skills/fund-facts-cn/scripts/check_fund_card.py ./my-fund-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill fund-facts-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **source documents** (finding the official summary, contract and prospectus, data leg) and **attachment parsing** (long attachments and multi-page PDFs, parsing leg). With neither installed the card still comes out from text you supply; what you lose is risk ratings and distribution details that live inside attachments - those stop at `未检索到` and the level comparison must be done by hand.

1. Register at <https://cuecue.cn>;
2. Take `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in local credentials - **never paste it into a chat**; the agent never handles the key;
3. Install: `cue-data-mcp` for the source leg, `cue-omni-reader` for the parsing leg. One command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills`;
   - single: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install only that one).

Configuration pages are pointed at, not restated: data leg <https://cuecue.cn/hub/mcp>; parsing leg <https://cuecue.cn/hub/omni-reader>; key <https://cuecue.cn/hub/api-key>.

### Connectivity self-check

```bash
# 1) catalog reachable anonymously: proves the catalog reads, not "connected"
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200

# 2) take routing.url and transport for the domain from the response; never hard-code the host
# 3) with the key, send tools/list - proves that endpoint accepted the key, nothing else
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

## 5. Boundaries

- IPO-subscription returns, return forecasts, annualised returns, ratings and target prices, subscription advice stay `[待人工]`; no guaranteed-gain, risk-free, guaranteed-return or principal-protected wording;
- No subscription on your behalf: no subscription orders, no sales channel, no agency work;
- Missing means `未检索到`, never a habit-based fill and never "none";
- Fees verbatim: "subject to the fund contract", "see the prospectus", "depends on the channel" and "pending" are not values;
- Domains and tools follow the live catalog; no fixed list, no count promise, no real-time promise.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The document is an excerpt, or the quote sits in an attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / deferred fee / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Summary, contract and sales page differ | Different levels or a rewritten pitch | Put both quotes in the comparison section with their own anchors; no judgement |

## 7. How to ask

- Good: "what are the management and custody fees", "how is the benchmark worded", "what is the equity range", "who manages it and since when", "how does distribution work".
- Bad: "how much will this fund earn", "how much do IPO subscriptions add", "pick a better fund for me", "subscribe for me" - returns, recommendations and subscriptions are out of scope and stay `[待人工]`.

## 8. Honest capability list

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not rate funds, does not forecast returns, does not compare products; it does not judge whether a risk level matches your appetite, it records what the document says; it stores nothing of your documents - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/fund-layers.md`: document levels and the three-element recording method (including the deferred fee-wording list)
- `scripts/check_fund_card.py`: five machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
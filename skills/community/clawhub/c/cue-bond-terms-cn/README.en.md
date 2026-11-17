# bond-terms-cn

**Give it one mainland bond document and get back an eight-item verbatim card: issuer, size and tenor, coupon, issue price, credit enhancement, put and call, disclosure and trustee, default clauses - each item carrying a verbatim quote and a source anchor. Valuation and ratings stay `[待人工]`.**

It reads one bond document only: convertible bond terms live in `convertible-bond-terms-cn`, placement terms in `placement-terms-cn`, prospectus digests in `prospectus-digest-cn`, company filing lists in `announcement-daily-cn`. The prospectus is the only authority - **issue announcements and underwriter decks must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over one document: prospectus, issue announcement, or dealer deck. For anything it does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the size and coupon cells: size, tenor and coupon stay verbatim; "pending", "bookbuilding" and "subject to the issue announcement" are not values and belong in the missing-data list; a rating symbol either carries an anchor on the same line or the whole line goes under `[待人工]`.

## 2. Six machine checks (no network)

`scripts/check_bond_card.py` gates the card: five sections plus item-level presence of the eight names / quote and anchor per item / red-line assertions only on `[待人工]` lines / exactly one completeness declaration reconciled with the number of `未检索到` lines / scale and coupon items must carry a unit-bearing number and deferred wording fires / no bare rating symbols: AAA, AA+, AA-, AA, A+ or A- on a non-`[待人工]` line without an anchor on that line fires.

```bash
python3 scripts/check_bond_card.py --help                          # usage
python3 scripts/check_bond_card.py --selftest                       # good sample passes, bad sample fires all six lanes, six threshold pins, temp files clean themselves
python3 scripts/check_bond_card.py scripts/fixtures/good-bond-card.md    # PASS (zero findings)
python3 scripts/check_bond_card.py scripts/fixtures/bad-bond-card.md     # FAIL (six lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r bond-terms-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-bond-card.md
python3 ~/.workbuddy/skills/bond-terms-cn/scripts/check_bond_card.py ./my-bond-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill bond-terms-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **source text** (finding the prospectus and issue announcements, data leg) and **attachment parsing** (long attachments and multi-page PDFs, parsing leg). With neither installed the card still comes out from text you supply; what you lose is default clauses and enhancement details that live inside attachments - those stop at `未检索到` and the level comparison must be done by hand.

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

- Valuation, yield calculations, ratings and target prices, subscription advice stay `[待人工]`; no buy or sell recommendations, no rating-action calls, no guaranteed gain;
- No subscription on your behalf: no subscription orders, no sales channel, no underwriting promise;
- Missing means `未检索到`, never a habit-based fill and never "none";
- Size and coupon verbatim: "pending", "bookbuilding", "to be announced", "subject to the issue announcement" and "depending on the market" are not values;
- No bare rating symbols: without an anchor on the same line, put the line under `[待人工]` or write `未检索到`;
- Domains and tools follow the live catalog; no fixed list, no count promise, no real-time promise.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The document is a summary, or the quote sits in an attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / deferred size or coupon / bare rating / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Prospectus and issue announcement differ | Different levels or an updated term | Put both quotes in the comparison section with their own anchors; no judgement |

## 7. How to ask

- Good: "what are the coupon and tenor", "is there a guarantee and who gives it", "when can investors put it back and can the issuer call it", "where are the default and cross-default clauses".
- Bad: "how much is this bond worth", "what yield can I get", "will the rating be upgraded", "subscribe for me" - valuation, yield, rating calls and subscription are out of scope and stay `[待人工]`.

## 8. Honest capability list

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not run credit analysis, does not estimate default probability, does not compare peer bonds; it does not interpret what a rating symbol means, only requires its source; it stores nothing of your documents - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/bond-layers.md`: document levels and the three-element recording method (including deferred size/coupon wording and the rating-symbol rule)
- `scripts/check_bond_card.py`: six machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
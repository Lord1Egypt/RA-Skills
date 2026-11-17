# bid-panorama-cn

**Give it one tender disclosure (bid notice, evaluation publicity, award notice) and get eight verbatim cards: project and number, tenderer and agent, opening, evaluation method, winner and amount, publicity window, contract terms, objection channel - each carrying a verbatim quote and a source anchor. Win odds and "is this positive" stay `[待人工]`.**

It reads one tender's disclosure chain only: convertible-bond terms live in `convertible-bond-terms-cn`, single-filing event briefs in `event-brief-cn`, filing lists in `announcement-daily-cn`, company background in `dd-checklist`. The heart of a tender is **the awarded amount and whether the two disclosures match** - "see the notice" or "per the contract" cannot pass this gate, and that boundary is why the skill exists.

## 1. Three steps to get going

1. Hand over one disclosure: pasted notice, a public-resources platform page, or a digest. For anything it does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus eight verbatim items - both come out as soon as you have the text, no channel needed.
3. Watch two cells: the awarded amount must carry a number plus a unit (元／万元／亿元); when both a tender notice and an award notice exist, put them in the comparison section with separate anchors.

## 2. Five machine checks (no network)

`scripts/check_bid_card.py` gates the card: five sections plus item-level presence of the eight names / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red-line assertions only on `[待人工]` lines / exactly one completeness declaration reconciled with the `未检索到` count / the winning amount is judged by rule: the item line is parsed into fields (name / quote / anchor / body), that item's own quote is the only evidence domain, dates are stripped, and one segment must carry the figure (N yuan / 10k / 100M) **right after award wording** (won / concluded / candidate / tender price / contract price) with no interfering wording **between that wording and the figure** (ceiling / control price / budget / estimate / cap / deposit / indicative). So "bid-price ceiling 200M" and "project budget 200M" do not stand in for the awarded amount; if nothing qualifies and the line does not read 未检索到, it fires, and the finding quotes the rejected segment and the stripped dates. So "bid-price ceiling 200M" or "project budget 200M" never settles the award line, and a figure that is itself predicated as a cap ("the award amount is 200M, i.e. the tender ceiling") is rejected too, while a bracketed constraint after a real figure ("86M yuan (no higher than the ceiling price)") stays valid - it qualifies the same amount rather than reporting a cap as the award. Red lines are judged three ways: a fixed word family; a rule that fires when a subject word (objection / query / rating / target price / revenue / profit / odds / positive / return / risk / invalidation / collusion / payment / schedule) shares a segment with judgement tone (should / will / must / likely / can / amounts to / constitutes / upheld / stands / upgraded / cut ...); and a self-verdict layer that fires when a verdict prefix (conclusion / therefore / in summary / this card holds / we find) meets an effect word (void / valid / annulled / upheld / stands / revoked / unlawful) - which catches "conclusion: this award is void" without putting the word "award" into the subject list, so an ordinary line like "note: the publicity states the objection channel" stays green. Institutional names are washed out of the tone domain before judging - the trailing 会 of 委员会 / 董事会 / 监事会 / 股东大会 and the leading 会 of 会计 / 会议 / 会员 are noun shapes, not judgement tone, so "the objection must be brought to the shareholders meeting", "the candidate list is verified by the evaluation committee" and "the minutes state the objection channel" stay green while "the objection should be rejected" fires. Exemptions are clause-scoped: "note: this skill does not judge whether an objection holds; revenue will surely rise" still fires on the second clause. Award figures are also rejected when they sit on a reference price (benchmark price, book value, net asset value, par value, market price) rather than on the award itself.

```bash
python3 scripts/check_bid_card.py --help                          # usage
python3 scripts/check_bid_card.py --selftest                       # good sample passes, bad sample fires all five lanes, one pin per whole family (see-the-notice, budget, price ceiling, control price, deposit, should-be-upheld, shall-be-upheld, rating will rise, revenue may double), a control sample proves a dated-but-valid amount line is not flagged, temp files clean themselves (the selftest reports how many pins ran)
python3 scripts/check_bid_card.py scripts/fixtures/good-bid-card.md     # PASS (zero findings)
python3 scripts/check_bid_card.py scripts/fixtures/bad-bid-card.md      # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r bid-panorama-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-bid-card.md
python3 ~/.workbuddy/skills/bid-panorama-cn/scripts/check_bid_card.py ./my-bid-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill bid-panorama-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **official text** (finding the notice and publicity, data leg) and **attachment parsing** (itemized tables, multi-page evaluation results, parsing leg). With neither installed the card still comes out from text you supply; what you lose is amounts hidden in attachment tables - those stop at `未检索到` and the two-document reconciliation is on you. This skill does not promise a dedicated tender API: if the domain is not open it uses only these two legs (see the data-channel section of SKILL.md).

1. Register at <https://cuecue.cn>;
2. Take `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in local credentials - **never paste it into a chat**; the agent never handles the key;
3. Install: `cue-data-mcp` for the text leg, `cue-omni-reader` for the parsing leg:
   - whole set: `npx skills add sensedeal/cue-skills`;
   - single: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader`).

Configuration pages are pointers only: data leg <https://cuecue.cn/hub/mcp>; parsing leg <https://cuecue.cn/hub/omni-reader>; key <https://cuecue.cn/hub/api-key>.

### Connectivity self-check

```bash
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200
# take routing.url and transport from the response; never hard-code the host
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

## 5. Boundaries

- Win odds, positive-impact calls, revenue impact, ratings and target prices, whether an objection holds stay `[待人工]`; no "sure to win", "steady gain", "zero risk", "guaranteed return";
- No filing on your behalf, no bidding advice: no tender documents, no evaluation prediction, and no guidance for collusion, bid-rigging or benefit transfer;
- Amount and dates verbatim: "see the notice", "per the contract", "amount pending" are not values - write `未检索到`;
- Missing means `未检索到`, never a habit-based fill and never "none";
- Domains and tools follow the live catalog; no fixed list, no count promise, no promise that a tender API is open.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The digest is second-hand, or the amount sits in an attachment table | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / vague amount / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Tender and award numbers differ | Two versions or a change | Put both quotes in the comparison section with their own anchors; no take-side judgement |

## 7. How to ask

- Good: "what is the awarded amount and first candidate", "which lines set the opening time and evaluation method", "what is the publicity window", "do the tender and award amounts match".
- Bad: "is this worth bidding", "what is our win probability", "make the tender document for me" - bidding decisions, win prediction and filing are out of scope, `[待人工]` or not accepted.

## 8. Honest capability list

Market and fund-flow figures are out of scope. A dedicated tender data interface is unverified on disk, so this skill promises neither that the domain is open nor real-time access - when it is not open, only user-supplied text and the parsing leg run. It does not judge collusion or bid-rigging (regulatory / DD work; cross-subject background goes to `dd-checklist`); it stores nothing of your notices - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/bid-chain.md`: the disclosure-stage chain and the three-element recording method (with the vague-amount list)
- `scripts/check_bid_card.py`: five machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
# convertible-bond-terms-cn

**Give it one China A-share convertible bond prospectus or issuance announcement and get eight verbatim clause cards: issue size and tenor, coupon, conversion price, conversion window, downward revision, conditional call, put-back, guarantee and rating - every clause carrying a verbatim quote and a source anchor. Conversion gains and call outcomes stay `[待人工]`.**

It reads convertible bond clauses only: plain corporate bonds live in `bond-terms-cn`, placement terms in `placement-terms-cn`, filing lists in `announcement-daily-cn`. The heart of a convertible bond is the **revision / call / put-back trigger set** - "meets the agreed conditions" or "see the announcement" cannot pass this gate, and that boundary is why the skill exists.

## 1. Three steps to get going

1. Hand over one document: prospectus, issuance announcement, or a disclosure-page location. For anything it does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus eight verbatim clauses - both come out as soon as you have the document, no channel needed.
3. Watch the three trigger clauses: the revision / call / put-back line must carry a numeric trigger value (e.g. 85% / 130% / 70% plus N trading days) **inside the clause quote and next to the trigger wording** - the gate strips dates first, so a publication date never stands in for a trigger; if nothing qualifies, write 未检索到.

## 2. Five machine checks (no network)

`scripts/check_cb_card.py` gates the card: five sections plus item-level presence of the eight names / quote and anchor per clause (empty or single-character quotes and empty anchors fire) / red-line assertions only on `[待人工]` lines - judgement sentences are caught by two rules (subject word sharing a segment with judgement tone, verdict prefix plus effect word), and the trailing 会 of an institutional name (委员会 / 董事会 / 监事会 / 股东大会) is washed out of the tone domain first, so "the call price is set by the board" stays green while "the put-back should be rejected" fires / exactly one completeness declaration reconciled with the `未检索到` count / trigger clauses are judged by rule, not by wording: the item line is parsed into fields (name / quote / anchor), the clause quote is taken as the only evidence domain, dates are stripped out of it, and one segment must carry **both** a trigger magnitude (N% / N percentage points / N trading days / N interest years / N days) **and** trigger context (consecutive / below / above / conversion price / closing price / interest year / put-back line). A clause name alone is not context, so "the put-back price is 100% of face" does not pass, and the figure must belong to that clause - own trigger wording nearby, a foreign trigger clause (revision or call wording) in the window fires just as hard; if no segment qualifies and the line does not read 未检索到, it fires - vague phrases ("meets the agreed conditions", "see the announcement", "to be fixed later") only choose the wording of the finding, and renaming them changes nothing.

```bash
python3 scripts/check_cb_card.py --help                          # usage
python3 scripts/check_cb_card.py --selftest                       # good sample passes, bad sample fires all five lanes, one pin per whole family (bare year, full date, another item number, to-be-agreed, to-be-announced), a control sample proves a dated-but-valid clause is not flagged, temp files clean themselves (the selftest reports how many pins ran)
python3 scripts/check_cb_card.py scripts/fixtures/good-cb-card.md     # PASS (zero findings)
python3 scripts/check_cb_card.py scripts/fixtures/bad-cb-card.md      # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r convertible-bond-terms-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-cb-card.md
python3 ~/.workbuddy/skills/convertible-bond-terms-cn/scripts/check_cb_card.py ./my-cb-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill convertible-bond-terms-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **source text** (finding the prospectus and announcements, data leg) and **attachment parsing** (long attachments and multi-page PDFs, parsing leg). With neither installed the card still comes out from text you supply; what you lose is trigger numbers that live inside attachments - those stop at `未检索到` and must be checked by hand.

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

- Conversion gain, conversion value, arbitrage space, call outcomes, revision likelihood, ratings and target prices stay `[待人工]`; no "sure to convert", "must be called", "subscribe now", "steady win", "zero risk", "guaranteed return"; the card never adjudicates validity or whether a clause should be rejected - that shape fires under the verdict-prefix plus effect-word rule; noun-shaped 会 is washed out of the tone domain in both directions (the suffix of 董事会 / 委员会 / 监事会 / 股东大会, the head of 会计 / 会议 / 会员), so "the call price is set by the board" and "the accounting treatment follows the prospectus" stay green while "conversion gains will surely materialise" fires, and exemptions are clause-scoped - a disclaimer at the head of a line does not shelter a judgement written after the semicolon;
- No subscription or conversion operations: no subscription orders, no conversion instructions, no acting on your behalf;
- Trigger values verbatim: numbers and day counts may not be replaced by "meets the agreed conditions" or "see the announcement";
- Missing means `未检索到`, never a habit-based fill and never "none";
- Domains and tools follow the live catalog; no fixed list, no count promise, no real-time promise.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The document is a digest, or the clause sits deep in an attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / vague trigger / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Prospectus and announcement numbers differ | Two versions of the same term | Put both quotes in the comparison section with their own anchors; no take-side judgement |

## 7. How to ask

- Good: "how was the conversion price set", "under what conditions can the issuer call it", "how deep and how many days for the put-back", "where is the revision trigger line", "what is the coupon ladder".
- Bad: "how much would I earn converting", "should I subscribe", "will it be called" - gains, subscription advice and call prediction are out of scope and stay `[待人工]`.

## 8. Honest capability list

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not compute conversion arbitrage, does not predict triggers, does not advise on subscribing; it does not compare bonds across issuers (cross-subject working papers go to `dd-checklist`), does not read plain corporate bond terms (that is `bond-terms-cn`); it stores nothing of your documents - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/cb-clauses.md`: the eight clauses and three trigger-clause recording conventions (with the vague-wording list)
- `scripts/check_cb_card.py`: five machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
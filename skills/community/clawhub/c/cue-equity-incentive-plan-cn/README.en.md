# equity-incentive-plan-cn

**Give it one China A-share equity incentive plan draft and get back an eight-item verbatim card: form and share source, granted quantity and ratio, recipients and scope, grant price and pricing method, validity and waiting period, unlocking and exercise conditions, special cases and leavers, approvals and disclosure duties - each item carrying a verbatim quote and a source anchor. Amortisation, exercise gain, dilution and "is this positive" stay `[待人工]`.**

It reads one plan draft only: **event dates** (grant registration day, exercise windows) live in `catalyst-calendar`, the **day-by-day progress of a plan on your watchlist** lives in `watchlist-digest-cn`, filing lists in `announcement-daily-cn`, placement plans in `placement-terms-cn`, convertible bond terms in `convertible-bond-terms-cn`. The draft is the only authority - **media digests and training slides must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over a draft or announcement: pasted text, a located disclosure page or a digest. For anything it does not state, demand `未检索到` instead of "incentives usually run three years".
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the grant-price cell: the per-share amount or pricing ratio has to sit **inside that item's own quote** - "to be announced", "set by the board", "a reference market price of 30 yuan" and "unlock ratio 40%" are not prices; send them to the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_eip_card.py` gates the card: five sections plus item-level presence of the eight names (each name needs its own `- name:` line; a prose mention does not occupy a line) / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red lines in three layers (fixed word family, subject word plus judgement tone in one segment, verdict prefix plus effect word) allowed only on `[待人工]` or explicit "not accepted" lines / exactly one completeness declaration reconciled with the `未检索到` count (two contradictory declarations fire) / the grant price judged by rule - fields parsed, that clause's own quote kept, dates stripped, then cut the quote at punctuation and at every money boundary and classify each figure inside its own phrase only: the nearest substantive noun to its left, once units and connectives are skipped, must be a price-leading noun - "per share" is a unit and never an owner, so "par value of 1 yuan per share" belongs to par value even when "grant price" appears elsewhere in the same phrase, while the right side of the figure decides when the left is empty ("per share 12.60 yuan of the grant price" is a real price), and a figure with no owner anywhere in its own phrase inherits the latest price-leading noun from the preceding phrases - but never when the preceding stretch only ever showed reference prices; the inheritance scan and the percentage branch read the date-stripped source string rather than the structure itself, so the structure carries the classification rather than every lookup; inside one phrase neither order nor commas flip the verdict, one qualifying figure passes and none plus no 未检索到 fires - a figure hanging off a reference price (market price, par value, the average price, book net assets per share) never counts even when the words "grant price" sit in the same line, so dates, reference prices and other items' numbers cannot settle it. Exemptions are clause-scoped: a line beginning "this skill does not judge the authenticity of the list" still fires on "the grant will surely be exercisable" after the semicolon; and noun-shaped 会 is washed out of the tone domain in both directions (the suffix of 委员会 / 董事会 / 股东大会, the head of 会计 / 会议 / 会员), so "the accounting treatment follows the draft" stays green while "the incentive will bring gains" fires.

```bash
python3 scripts/check_eip_card.py --help                          # usage
python3 scripts/check_eip_card.py --selftest                       # good sample passes, bad sample fires all five lanes, one pin per whole family, control samples stay green, temp files clean themselves (the selftest reports how many pins ran)
python3 scripts/check_eip_card.py scripts/fixtures/good-eip-card.md     # PASS (zero findings)
python3 scripts/check_eip_card.py scripts/fixtures/bad-eip-card.md      # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
# 1. drop the skill into your skills directory
mkdir -p ~/.workbuddy/skills
cp -r equity-incentive-plan-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md, save it as my-incentive-card.md

# 3. run the machine gate (no network)
python3 ~/.workbuddy/skills/equity-incentive-plan-cn/scripts/check_eip_card.py ./my-incentive-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill equity-incentive-plan-cn (this installs only this package; restart your session on your side for it to take effect).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **source text** (finding the draft and companion announcements, data leg) and **attachment parsing** (drafts run to tens of pages with recipient tables and assessment schedules, parsing leg). With neither installed the card still comes out from text you supply; what you lose is the detail that lives inside those tables - it stops at `未检索到`, and the level comparison has to be done by hand.

1. Register at <https://cuecue.cn>;
2. Take a `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials - **never paste it into chat**, the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the source-text leg, `cue-omni-reader` for the attachment leg. One command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the public skills of that collection and asks which to install);
   - single: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one alone).

Configuration pointers, without repeating the setup steps: source text goes through the data leg, official page <https://cuecue.cn/hub/mcp>; long attachments and PDFs through the parsing leg, official page <https://cuecue.cn/hub/omni-reader>; the key at <https://cuecue.cn/hub/api-key>.

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

Installing a skill is not configuring credentials is not a connected leg: this test only covers the data leg - a key accepted at the domain's live `routing` endpoint with a `tools/list` return proves that leg, and nothing else; the parsing leg is judged by its own criteria.

## 5. Boundaries

- Per-share amortisation, exercise gain, dilution, effect on reported results, whether this is positive and how the share price reacts stay `[待人工]`; no "join in", "steady gain", "zero risk", "guaranteed return", "will surely vest";
- No validity calls: whether the plan is valid, whether the approval was lawful, whether a registration stands - those are human and regulator determinations, and writing them as conclusions turns the gate red;
- No proxy handling, no list verification: no subscription on your behalf, no exercise instruction, no checking the recipient list, and no route around approval or disclosure duties;
- Grant price verbatim: "to be announced", "set by the board" and "to be agreed" are not a price, and neither is a figure sitting on a reference price - "reference market price 30 yuan", "par value 1 yuan", "the 20-day average price of 25.20 yuan", "book net assets per share of 8.50 yuan" - nor an "unlock ratio 40%" borrowed from another item; the number has to belong to the grant price itself, and without one write `未检索到`;
- `未检索到` means exactly that; filling from customary plan design or writing "no such item" is not allowed;
- Domains and tool names follow live catalog values; this skill lists no fixed inventory, promises no count, and does not promise that a domain is open or that the draft is current.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Several items read `未检索到` | The file is a digest, or the quote sits in a recipient table or attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / no figure settled for the grant price / count mismatch / a judgement sentence written by the card | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| A judgement line flagged by mistake | The line names an institution (委员会 / 董事会 / 监事会 / 股东大会) or quotes draft wording | Keep draft wording inside the quote brackets and its anchor; the trailing 会 of an institutional name is a noun suffix and is washed out of the tone domain before judging, so ordinary register lines stay green |
| Draft and summary differ | Two versions or a later amendment | Put both quotes in the comparison section with their own anchors; no take-side judgement |

## 7. How to ask (good and bad)

- Good: "how was the grant price set", "how many shares and what share of capital", "who is in the recipient list, do supervisors count", "how many tranches and which performance line gates unlocking", "what happens on resignation or a change of control", "which approvals and disclosures are still owed".
- Bad: "is joining worth it", "how much dilution", "what will the exercise gain be", "will the targets be met" - gain, dilution, attainment and participation advice are out of scope and stay `[待人工]`.

## 8. Capability limits (honest list)

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not do the accounting (per-share amortisation, total expense, profit impact belong to the auditors and the disclosure), does not judge fairness or tunnel-transfer suspicion, does not verify the recipient list - it only records verbatim who is included and who is excluded; and it stores nothing of your draft, the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this counterpart; conflicts resolve to the Chinese face
- `references/eip-terms.md`: the eight items and the four families of price-stubbing wording (with the split against event dates)
- `scripts/check_eip_card.py`: five machine checks (no network)

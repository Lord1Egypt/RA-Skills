# ma-restructuring-terms-cn

**Hand it one China A-share M&A restructuring filing and get back eight verbatim cards: deal outline and method, counterparty and related-party status, target asset and title, valuation method and consideration, payment and share issuance, profit guarantee and compensation, lock-up and transfer limits, approvals and disclosure duties - each item carrying a verbatim quote and a source anchor. Whether the deal is worth it, whether the valuation is fair and whether approval will pass stay `[待人工]`**

It reads one transaction's clauses: **suspension, resumption and review milestones** live in `catalyst-calendar`, an issuer's **acquisition history, control and horizontal competition risk facts** live in `dd-checklist` (pick the M&A purpose tier), filing lists in `announcement-daily-cn`, convertible bond terms in `convertible-bond-terms-cn`, placements in `placement-terms-cn`. The report or proposal is the only authority - **media coverage and second-hand digests must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over a report, a proposal or a related announcement: pasted text, a located disclosure page or a digest all work. For anything it does not state, demand `未检索到` instead of "restructuring deals usually carry a 36-month lock".
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the three numeric cells: valuation and consideration, issue price and share count, guaranteed net profit and compensation have to sit **inside that item's own quote**, and the gate first **cuts the quote into phrases and classifies mainly on that structure** (each figure looks for its owner inside its own phrase: the nearest substantive noun to its left, once units such as "per share" or "in total" are skipped, must belong to that cell's own family to count, and a reference noun - book value, audited net assets, a P/E multiple, realised profit - disqualifies it even when the cell's own noun appears elsewhere in the same phrase; only a figure with no owner in its own phrase inherits the latest own-family noun from the preceding phrases, and it inherits nothing when only reference figures appeared earlier; each cell needs its own landing for **both** elements - a qualifying figure for the numeric one, an arrangement wording for the compensation one - "valuation of 860 million yuan, consideration to be agreed" still counts as missing, and the only exception is co-reference: one figure inside a phrase whose two own nouns are joined by an **affirmative** copula ("the appraised value is the consideration of 860 million yuan") settles both, while a negated copula ("is not") settles neither element's partner, and an appositional shape whose copula follows both nouns ("the appraised value and the consideration are both 860 million yuan") is not recognised and fires as a known coverage limit for human review; an arrangement element sitting in the same segment as "to be decided" counts as not settled, and so does the co-present shape ("compensation amount to be decided but shortfall settled in shares"), while a semicolon or full stop between the two is read correctly) - "subject to the valuer's report", "to be agreed by the parties", "to be disclosed later" are not figures; "book value of 320 million yuan", "audited net assets of 410 million yuan", "audited value of 400 million yuan", "peer P/E of 18.5x", "pre-deal share capital of 540 million shares", "realised net profit of 42 million yuan" are reference figures; "the valuation base date is 31 December 2025" is a date; when you meet one, send it to the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_ma_card.py` gates the card: five sections plus item-level presence of the eight names (each name needs its own `- name:` line; a prose mention does not occupy a line) / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red lines in three layers (fixed word family, subject word plus judgement tone in one segment, verdict prefix plus effect word) allowed only inside the `[待人工]` or explicit "not accepted" **clause**; exemptions never cross a clause - "[待人工] whether the valuation is fair stays human; this deal will certainly be approved" still fires on the second half, and the fixed family now covers two word families judged by form: a valuation noun plus an evaluative adjective with or without an intensifier ("the valuation is very reasonable", "the price is basically fair") and an approval verb plus "probability" plus a degree word ("the odds of approval are high"); the evaluative family carries a single exclusion shared by both branches - any evaluative word followed by a nominal suffix (the three suffixes 「性·度·论」 - reasonableness, fairness, adequacy, "-degree") names what is being explained rather than asserting a judgement, so "the deal must explain the reasonableness of the price" and "the adequacy of the valuation is still to be explained" stay green; and the modal character inside institutional names ("X 会") and nouns ("会 X") is washed out first / exactly one completeness declaration reconciled with the `未检索到` count (two contradictory declarations fire) / the three numeric cells judged mainly on a phrase structure, each cell needing its own landing for both elements - a qualifying figure for a numeric element, an arrangement wording for the compensation element - fields parsed, that item's own quote kept, dates stripped, the domain cut at punctuation and at every number boundary, and each candidate classified inside its own phrase only (nearest substantive noun to the left once units are skipped; the right side when the left is empty; an elided figure inherits the latest own-family noun from the preceding phrases but never when the preceding stretch only ever showed reference figures), with amounts, share counts, multiples and percentages all going through that one rule; each element of a cell needs its own landing - a qualifying figure for a numeric element, an arrangement wording for the compensation element - and a missing one plus no `未检索到` fires - another cell's number, a reference figure and a date cannot settle this cell's account)

```bash
python3 scripts/check_ma_card.py --help                          # usage
python3 scripts/check_ma_card.py --selftest                       # good sample passes, bad sample fires all five lanes, one pinned tier per family, control samples stay green, temporary files self-clean (tier count self-reported)
python3 scripts/check_ma_card.py scripts/fixtures/good-ma-card.md     # PASS (no findings)
python3 scripts/check_ma_card.py scripts/fixtures/bad-ma-card.md      # FAIL (each lane fires with line numbers)
```

## 3. Install and run

```bash
# 1. drop the skill into your skills directory
mkdir -p ~/.workbuddy/skills
cp -r ma-restructuring-terms-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md, save it as my-ma-card.md

# 3. run the machine gate (no network)
python3 ~/.workbuddy/skills/ma-restructuring-terms-cn/scripts/check_ma_card.py ./my-ma-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill ma-restructuring-terms-cn (this installs only this package; restart your session on your side for it to take effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **source text** (finding the report, the proposal and related announcements, on the data leg) and **attachment parsing** (restructuring reports run to a hundred-plus pages, with valuation and audit notes and target financial statements usually in attachments, on the parsing leg). Both are optional - you can still get a card from a file you paste yourself; the price is that valuation notes and compensation detail inside attachments stop at `未检索到`, and the report-vs-proposal reconciliation cannot be filled in automatically, so it needs a human back at the original text.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it as local credential - **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the source-text leg, `cue-omni-reader` for the parsing leg. One command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the public skills of that collection and prompts which to install);
   - single: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one only).

Configuration pointers are pointers only, never re-explained steps: source text on the data leg at <https://cuecue.cn/hub/mcp>; long attachments and PDFs on the parsing leg at <https://cuecue.cn/hub/omni-reader>; the key at <https://cuecue.cn/hub/api-key>.

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

Installing a skill is not configuring a credential and is not a connected data leg: that judgement covers only the data-leg path - connecting with the key to the domain's current `routing` and getting a `tools/list` response there proves that key was accepted for that endpoint, nothing more; the parsing leg has its own judgement on its own face.

## 5. Boundaries

- Whether the deal is worth it, whether the valuation is fair, whether exchange review and CSRC registration will pass, post-resumption price behaviour, dilution, whether the profit guarantee can be met - all `[待人工]`; no "join in", "sure profit", "zero risk", "guaranteed return", "will certainly pass", "the valuation is reasonable";
- No legal-effect calls: whether the transaction is valid, whether the procedure violates rules, whether the application documents stand - human and regulatory territory; writing such a self-verdict fires the gate;
- No agency work: no application documents, no filing or voting on someone's behalf, no designing the plan, and nothing that avoids approval, evades disclosure or touches insider information;
- Figures verbatim and cell-scoped: "subject to", "to be agreed", "to be disclosed later", book value, audited net assets, P/E, pre-deal share capital and realised net profit are not the cell's own figure - if it was not retrieved, write `未检索到`;
- The attribution rule has a stated reach: it decides adjacency inside one phrase plus one cross-phrase inheritance, and does not claim to cover every natural-language assignment of a figure; what an elided subject refers to is human review against the original sentence, and when the document genuinely does not state a figure, `未检索到` is a lawful answer;
- `未检索到` means writing exactly that - no filling from what comparable deals do, and no "this item does not exist" substitute;
- Domains and tool names follow live catalog values: no fixed list, no promised counts, no promise that the domain is open or that the filing is current.

## 6. Troubleshooting

| Symptom | Why | Recovery |
|---|---|---|
| Several items read `未检索到` | The file is a proposal or summary, or the quotes live in attachments | Start the attachment-parsing leg to recover quotes; if it cannot run, keep the named gaps instead of filling them |
| The data leg will not connect | Missing credential or the domain is not live | Use the self-check in section 4; the first two sections still produce, at the cost written there |
| The gate fires | Missing anchor or quote, an unsettled figure in one of the three cells, a count mismatch, a judgement sentence | Fix by the named line numbers; anything unrecoverable goes to the missing-data list, never by deleting lines |
| A judgement line fires in error | The line says "shareholders' meeting", "board", "audit committee" or quotes the report | Keep quotes inside the title marks and keep the anchor; the gate washes institutional-name tokens before judging tone, so ordinary registration sentences stay green |
| A cell's own figure was called a reference figure | The sentence puts book value or net assets next to the figure and the cell's noun further away | Keep the report's own sentence for that cell (quote it as written), or if the document really omits it, write `未检索到` |
| Report and proposal disagree | Terms are routinely adjusted between them | Put both quotes side by side in the comparison section with their own anchors; do not choose between them |

## 7. How to ask (good and bad prompts)

- Good: "what is the consideration for this restructuring and how was it set", "what are the issue price and share count", "who is the counterparty and is this a related-party transaction", "what is the target asset and is title clean", "what does the profit guarantee promise and how is shortfall compensated", "how long is the lock-up and what releases it", "which approvals are needed and is a tender offer waived".
- Bad: "is this deal worth it", "is the valuation too high", "will it pass review", "where does the price go after resumption", "how much dilution" - worth, valuation fairness, outcome prediction and market reaction are outside this skill and stay `[待人工]`.

## 8. Capability limits (honest list)

Market and fund-flow figures are outside this skill (domains follow live catalog values; unopened means unpromised); no valuation or accounting computations - whether a valuation is reasonable, goodwill and purchase-price allocation are for valuers, accountants and the filing itself; no judgement on deal motive, tunneling suspicion or insider-information likelihood; no compliance playbook for executing a tender offer, only a verbatim record of what the report says; and nothing of yours is stored persistently - the card is handed back when it is done.

## 9. Resources

- `SKILL.md`: the five-section card and red lines (Chinese face is authoritative)
- `SKILL.en.md`: the matching English face; conflicts resolve to the Chinese face
- `references/ma-terms.md`: the eight items' fields, the four kinds of stand-in wording in the three numeric cells, and the split against event-facing skills
- `scripts/check_ma_card.py`: five machine checks (no network)

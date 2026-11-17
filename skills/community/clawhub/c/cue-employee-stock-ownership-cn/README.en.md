# employee-stock-ownership-cn

**Hand it one China A-share employee stock ownership plan draft and get back eight verbatim cards: plan name and tranche, participants and determination criteria, funding source, share source, transfer price and scale, duration and lock-up, management model and holders' meeting, amendment, termination and unit disposal - each item carrying a verbatim quote and a source anchor. Whether the plan is worth joining, whether the price is fair, whether vesting will happen, and individual income tax or deferred taxation all stay `[待人工]`.**

**It is not the same thing as an equity incentive plan (this sentence is why the skill exists)**: **an employee stock ownership plan follows 《关于上市公司实施员工持股计划试点的指导意见》 (the Guiding Opinions on piloting employee stock ownership plans), while an equity incentive plan follows 《上市公司股权激励管理办法》 (the Measures for the Administration of Equity Incentives)** - different rule source, different participant and pricing conventions, different approval and disclosure procedure. An ESOP draft never uses the incentive vocabulary (grant price, exercise, vesting release), and an incentive draft never uses the ESOP vocabulary (holders' meeting, management committee, transfer price). So **ESOP clauses cannot be read out of `equity-incentive-plan-cn`, and incentive clauses cannot be read out of this skill**; the two do not cover each other and are not substitutes. When one company runs both in the same year, that is two documents, two rule sets, two cards.

It reads one ESOP draft's clauses: **which day the shares transfer, when an unlock window opens** are event dates and live in `catalyst-calendar`; the daily delta of "where this plan stands" in a watchlist lives in `watchlist-digest-cn`; filing lists in `announcement-daily-cn`; private placements in `placement-terms-cn`; convertible bond terms in `convertible-bond-terms-cn`. The draft is the only authority - **media coverage and second-hand digests must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over a draft or an announcement: pasted text, a located disclosure page or a digest all work. For anything it does not state, demand `未检索到` instead of "these plans usually run three years".
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the two numeric cells: transfer price with share count, and funding source with total funding have to sit **inside that item's own quote**, and the gate first **cuts the quote into phrases and classifies mainly on that structure** (each figure looks for its owner inside its own phrase: the nearest substantive noun to its left, once units such as "per share" or "not lower than" are skipped, must belong to that cell's own family to count, and a reference noun - trading average, closing price, par value, net assets per share, total share capital, per-unit value, grant price - disqualifies it even when the cell's own noun appears elsewhere in the same phrase; only a figure with no owner in its own phrase inherits the latest own-family noun from the preceding text, and it inherits nothing when the nearest preceding noun is a reference figure; each cell needs its own landing for **both** elements - a per-share figure for the transfer price, a share figure for the share count, so one figure does not settle the pair) - "to be disclosed later", "determined by the management committee", "agreed separately" are not figures; "a trading average of 34.70 yuan per share over the 20 trading days before the draft", "total share capital of 1,309,533,797 shares", "1.00 yuan per unit" are reference figures; the 50% in "not lower than 50% of the trading average" is a ratio, not a price; "a duration of 36 months" is a period, not a price; when you meet one, send it to the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_esop_card.py` gates the card: five sections plus item-level presence of the eight names (each name needs its own `- name:` line; a prose mention does not occupy a line; names are normalised through an **alias table**, so "purchase price and scale" and "transfer price and scale" are the same item, and so are "holder scope and determination criteria" and "participants and determination criteria") / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red lines in three layers (fixed word family with the evaluative, predictive and **tax** branches folded in - "the plan is very reasonable", "the transfer price is basically fair", "the unlock probability is high", "individual income tax is payable", "deferred taxation applies" and "tax planning" are judged alike; subject word plus judgement tone in one segment; verdict prefix plus validity judgement) allowed only inside the `[待人工]` or explicit "not accepted" **clause** - neither the marker nor a disclaiming sentence crosses a clause; the modal character inside institutional names ("X 会") and nouns ("会 X") is washed out of the tone domain first, so "holders' meeting", "management committee" and "remuneration and assessment committee" stay green / exactly one completeness declaration reconciled with the `未检索到` count (two contradictory declarations fire) / the two numeric cells judged mainly on a phrase structure: fields parsed, that item's own quote kept, dates stripped, the domain cut at punctuation and number boundaries, and each candidate classified inside its own phrase only (nearest substantive noun to the left once units are skipped; the right side when the left is empty; an orphan figure inherits the latest own-family noun from the preceding text but never when the nearest preceding noun is a reference figure), with ratios and periods standing aside - a candidate ending in ％, % or 倍 settles nothing, and neither does a money or share figure whose left edge ends on a ratio word; each cell needs its own landing for both elements, and an element without one plus no `未检索到` fires - another cell's number, a reference figure and a date cannot settle this cell's account.

```bash
python3 scripts/check_esop_card.py --help                          # usage
python3 scripts/check_esop_card.py --selftest                       # good sample passes, bad sample fires all five lanes, one pinned tier per family, control samples stay green, temporary files self-clean (tier count self-reported)
python3 scripts/check_esop_card.py scripts/fixtures/good-esop-card.md     # PASS (no findings)
python3 scripts/check_esop_card.py scripts/fixtures/bad-esop-card.md      # FAIL (each lane fires with line numbers)
bash scripts/fixtures/run_fixtures.sh                             # offline, three tiers in one run: self-test / good and bad samples one by one / boundary shapes one by one; last line self-reports "档数=3｜不合=0｜不可判=0"
```

## 3. Install and run

```bash
# 1. drop the skill into your skills directory
mkdir -p ~/.workbuddy/skills
cp -r employee-stock-ownership-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md, save it as my-esop-card.md

# 3. run the machine check (no network)
python3 ~/.workbuddy/skills/employee-stock-ownership-cn/scripts/check_esop_card.py ./my-esop-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill employee-stock-ownership-cn (this installs only this package; restart your session on your side for it to take effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **source text** (finding ESOP drafts, implementation announcements and holders' meeting resolutions on the data leg) and **attachment parsing** (the full draft, legal opinions, independent financial adviser reports and holders' meeting resolutions usually sit in attachments, on the parsing leg). Both are optional - you can still get a card from a file you paste yourself; the price is that price and assessment detail inside attachments stops at `未检索到`, and the draft-versus-implementation-announcement reconciliation cannot be filled in automatically, so it needs a human back at the original text.

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

- Whether the plan is worth joining, whether the transfer price is fair, whether the performance targets are reachable, whether vesting will happen, how individual income tax and deferred taxation apply, and the effect on earnings and share price - all `[待人工]`; no "recommend joining", "recommend subscribing", "sure profit", "zero risk", "guaranteed return", "positive for the price", "certain to rise";
- **No tax judgement**: if the draft says "in accordance with relevant state regulations" register that verbatim, if it says "deferred taxation" register deferred taxation; how much is owed, whether deferral applies and how to plan around it belong to the tax desk and to humans - writing such a verdict fires the gate;
- No legal-effect calls: whether the plan is valid, whether the procedure violates rules, whether a holders' meeting resolution stands - human and regulatory territory; writing such a self-verdict fires the gate;
- No rule-application answers: whether the plan should be self-managed or delegated, whether shareholder approval is required - the skill registers whichever form the filing states and never answers which rule applies;
- No agency work: no plan documents, no draft writing, no tax computation, no proxy voting or filing on a client's behalf, and no route around approval, around disclosure or into inside information;
- Figures verbatim and cell-scoped: "subject to", "agreed separately", "to be disclosed later", trading average, closing price, par value, net assets per share, total share capital and per-unit value are not the cell's own figure - if it was not retrieved, write `未检索到`; each cell needs a landing for **both** elements, a per-share figure for the transfer price and a share figure for the share count, so one figure does not settle the pair; **the noun families follow how real filings write them** - the share-count cell also accepts 标的股票上限, 标的股票规模 and 认购的股数上限, and the price cell accepts a parenthetical inside the noun (购买股票（含预留部分）的价格, 受让价格（含预留）);
- The attribution rule has a stated reach: adjacency inside one phrase plus one cross-phrase inheritance; it does not claim to cover every natural-language assignment of a figure. The appositional coreference shape and the "price undecided but count fixed" co-present sentence are declared coverage limits that fire under the strict reading - read those against the draft; when the document genuinely does not state a figure, `未检索到` is a lawful answer;
- The eight item names are matched by **any expression**: some companies write 持有人 for participants, some write 购买价格 for the transfer price, some write 股份来源 for the share source, and **chapter headings count too** (持有人的确定依据、范围及份额分配情况, 价格和规模, 存续期、锁定期、考核设置), so whichever alias the card uses is accepted; but an alias settles only whether the item is present, not whether it was captured;
- `未检索到` means writing exactly that - no filling from what comparable plans do, and no "this item does not exist" substitute;
- Domains and tool names follow live catalog values: no fixed list, no promised counts, no promise that the domain is open or that the filing is current.

## 6. Troubleshooting

| Symptom | Why | Recovery |
|---|---|---|
| Several items read `未检索到` | The file is a resolution summary, or price and assessment detail lives in the draft's attachments | Start the attachment-parsing leg to recover quotes; if it cannot run, keep the named gaps instead of filling them |
| The data leg will not connect | Missing credential or the domain is not live | Use the self-check in section 4; the first two sections still produce, at the cost written there |
| The gate fires | Missing anchor or quote, an element without its own landing in the two numeric cells, a count mismatch, a judgement sentence | Fix by the named line numbers; anything unrecoverable goes to the missing-data list, never by deleting lines |
| A judgement line fires in error | The line says "holders' meeting", "management committee" or "remuneration and assessment committee", or quotes the draft | Keep quotes inside the title marks and keep the anchor; the gate washes institutional-name tokens before judging tone, so ordinary registration sentences stay green |
| A self-verdict inside title marks still fires | The line is this card's own conclusion ("this card concludes: the price is fair", "we judge: the price is fair") with no source text behind it | Reword it as a `[待人工]` reservation, or quote the draft and keep its anchor - the exemption is a whitelist: an anchor, citation labels only outside the brackets, a citation label inside if the quote opens with one, and no self-reference of this card (本件 / 本卡 / 本速读 / 笔者; 本公司 / 本计划 / 本员工持股计划 do not count, and neither do compounds ending in 本件 such as 样本件 / 基本件 / 成本件 / 副本件, while a whitespace-split 本 件 does) inside the brackets - a predecessor outside the finite function-word whitelist (通过本件判断) is a known not covered limit, so verify it against the original sentence by hand |
| The cell's own figure was called a reference figure | The sentence puts the trading average or total share capital next to the figure and the cell's noun further left | Keep the draft's own sentence for that cell, or if the document really omits it, write `未检索到` |
| The item name differs from the card's wording | The draft's section heading uses an alias such as 购买价格, 持有人 or 持有人的确定依据、范围及份额分配情况 | Whichever alias the card uses is accepted (the gate normalises through the alias table, chapter headings included); the quote and anchor are still required |
| The tax cell fires | The line says "individual income tax is payable", "deferred taxation applies" or "tax planning" | Register the draft's own wording verbatim ("in accordance with relevant state regulations"), or mark it `[待人工]`; this skill does not judge tax |

## 7. How to ask (good and bad prompts)

- Good: "who can join this ESOP, are directors and officers in it", "where does the money come from, where do the shares come from", "what is the transfer price, how many shares, what percentage of share capital", "how long does it run, how long is the lock-up, how many unlock tranches", "who manages it, what can the holders' meeting decide", "what happens to my units if I leave, when does the plan terminate", "is this an ESOP or an equity incentive plan".
- Bad: "is this plan worth joining", "is the transfer price expensive", "can the performance targets be met", "is this unlock safe", "how much individual income tax, can it be deferred", "where does the stock go after resumption" - participation value, fairness, target achievement, tax treatment and market reaction are outside this skill and stay `[待人工]`.

## 8. Capability limits (honest list)

Market and fund-flow figures are outside this skill (domains follow live catalog values; unopened means unpromised); no plan design or computation - unit allocation, performance-target setting and tax computation belong to the company, its lawyers and its tax advisers; no judgement on plan quality, participation value or insider-information likelihood; no rule-application answers about which management model or approval route was required; and nothing of yours is stored persistently - the card is handed back when it is done.

## 9. Resources

- `SKILL.md`: the five-section card and red lines (Chinese face is authoritative)
- `SKILL.en.md`: the matching English face; conflicts resolve to the Chinese face
- `references/esop-terms.md`: the eight items' fields, the four kinds of stand-in wording in the two numeric cells, the cutting line against equity incentives, and the split against sibling skills
- `scripts/check_esop_card.py`: five machine checks (no network)
- `scripts/fixtures/run_fixtures.sh`: offline three-tier runner (no network, no billing)

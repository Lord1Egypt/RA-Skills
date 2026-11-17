# Shareholder Return Panorama · Dividend, Buyback, Reduction

Split one A-share shareholder-return filing into eight verbatim cards: dividend, buyback, reduction
and pledge, each carrying the filing's own sentence and an anchor. Gaps go to a missing-data list;
all judgement is left to a human.

## 1. Start here: three steps today

1. Hand the filing (URL or local file) to this skill.
2. It registers the eight items verbatim, each with its sentence and anchor.
3. Whatever it cannot get goes to the missing-data list; judgement questions all go to the human section.

## 2. Five machine checks (zero network)

```bash
python3 -B scripts/check_sh_return_card.py <card.md>     # five codes, item by item; PASS when clean
python3 -B scripts/check_sh_return_card.py --selftest    # good sample passes, bad samples fire all five
bash scripts/fixtures/run_fixtures.sh                    # offline fixtures, three tiers, 30s, zero network
```

| Code | What it checks |
|---|---|
| `SR-STRUCT` | Five sections present; the eight items present **line by line** in the verbatim section (one line each; a passing mention in prose does not count) |
| `SR-QUOTE` | The quoted sentence may not be empty or a single character; an `anchor:` label with an empty value also fires |
| `SR-LINE` | Three red-line families: fixed banned words / subject × judgement tone in one clause / self-ruling validity layer |
| `SR-COUNT` | Exactly one missing-count declaration, and N equals the number of "not found" item lines; "no such item" always fires |
| `SR-VALUE` | The numeric cells settled by phrase structure; a closer reference number disqualifies; ratios and bonus shares are never settled |

## 3. Getting started

```bash
# one card
python3 -B scripts/check_sh_return_card.py my-card.md

# selftest (run this first after touching the checker)
python3 -B scripts/check_sh_return_card.py --selftest
```

## 4. First-time Cue setup (three steps, skippable)

1. Register at cuecue.cn and obtain `CUE_API_KEY`.
2. Export it: `export CUE_API_KEY=...`.
3. Connectivity self-check:

```bash
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500
```

**It runs without setup**: with no key this skill works only from the user-supplied filing text and
local files; the cost is that the channel-side original filing and attachment body parsing are
unavailable, so anchors can only land on the copy the user provided and cross-document verification
cannot be done.

## 5. Boundaries and non-promises

- No evaluation of return level (payout ratio, buyback forcefulness, dividend yield).
- No prediction of price or market-cap impact.
- No buy/sell advice.
- No drafting filings, no tax computation, no filing on anyone's behalf.
- No inside information, no advice on bypassing approval or avoiding disclosure.
- No ruling on validity.

## 6. When something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| `SR-STRUCT` missing section | A section heading was renamed or omitted | Write the five headings exactly as in the output contract |
| `SR-STRUCT` missing item line | The item is only mentioned in prose | Give each item its own line starting `- item:` |
| `SR-QUOTE` empty quoted sentence | Paraphrased or left blank | Copy the original sentence; no paraphrase |
| `SR-COUNT` exactly one declaration | Two declarations, or none | Keep exactly one "eight items, N missing" |
| `SR-COUNT` N mismatch | N differs from the "not found" count | Count the "not found" item lines |
| `SR-VALUE` missing element | Only reference numbers present (net profit, share capital, VWAP) | Go back to the filing for the item's own noun and value |
| `SR-LINE` banned word | An evaluation, prediction or recommendation slipped in | Delete it; register the sentence or move it to the human section |

## 7. How to ask (good and bad)

**Good**

- "In this distribution notice, how much per 10 shares, and when is the record date?"
- "In this buyback plan, how many shares, at what price, and for what purpose?"
- "This company did both a dividend and a buyback this year — put them on one card."

**Bad**

- "Is this dividend worth it?" → this skill does not judge return level.
- "Will the price rise after the buyback?" → this skill does not predict prices.
- "Draft a reduction notice for me." → this skill does not draft filings.

## 8. Honest capability limits

- It judges **adjacency within one phrase plus one cross-phrase inheritance**; it does not claim to cover every natural-language attribution form.
- Appositive coreference (copula after both nouns) and the "price undetermined but quantity fixed" same-paragraph form are known gaps; they fire under the strict rule, so a human should check the original sentence.
- Item names are recognised by alias family; the table is `ITEM_ALIASES` in `scripts/check_sh_return_card.py`. A new spelling means adding an alias, not changing the criterion.

## 9. Resources

- `SKILL.md` — authoritative face (Chinese)
- `SKILL.en.md` — English twin
- `references/sh-return-terms.md` — eight items and their elements, aliases, cut lines
- `scripts/check_sh_return_card.py` — the five-code checker
- `scripts/fixtures/` — one good sample, five bad samples, the runner

# Share Pledge & Release Tracker

Chain one shareholder's successive pledge and release announcements into a single balance timeline — every entry carrying the announcement's own sentence and its anchor, and percentages taken only from what the announcement states, never divided out by the card itself.

## 1. Three steps to start

1. Hand the pledge/release announcements (URL or local file, possibly several) to this skill.
2. It registers six elements per pledge entry (pledgor · pledgee · shares · share of holdings · share of total capital · period) and three per release entry (pledgor · released shares · release date), each anchored to its own sentence.
3. Cumulative and remaining are written as "before → after"; anything the announcements omit goes into the not-obtained list, and every judgement question goes to "needs a human".

## 2. Five machine checks (offline)

```bash
python3 -B scripts/check_pledge_tracker.py <card.md>     # five codes, PASS when clean
python3 -B scripts/check_pledge_tracker.py --selftest    # good sample passes, six bad samples fire
bash scripts/fixtures/run_fixtures.sh                    # three tiers, 30s, no network, no billing
```

| Code | What it checks |
|---|---|
| `SP-STRUCT` | Five sections present; pledge and release entries present **line by line** inside the detail section; six elements per pledge row and three per release row; every cumulative row must be a difference of two points (`before → after`) |
| `SP-QUOTE` | The quoted sentence in each row must not be empty or a single character; an `锚：` label with an empty anchor value also fires |
| `SP-LINE` | Three red-line families: fixed banned phrases (liquidation-risk judgement / ratio rating / price calls / ratings and target prices / return promises / acting on the user's behalf) · subject word × judgement tone in one clause · self-adjudicating validity |
| `SP-GAP` | Two-way reconciliation of the not-obtained declaration (over-declaring is inflation, under-declaring is omission); "not applicable / no disclosure needed" always fires; **the percentage must appear in that row's own quoted sentence**, otherwise it is flagged as a self-computed ratio |
| `SP-BOUND` | A dividend/buyback/reduction item line means the wrong skill was used — it names `cn-shareholder-return`; a single-announcement pick line names `event-brief-cn` |

## 3. Usage

```bash
# one card
python3 -B scripts/check_pledge_tracker.py my-card.md

# selftest (run this after touching the checker)
python3 -B scripts/check_pledge_tracker.py --selftest
```

## 4. First-time Cue setup (three steps, optional)

1. Register at cuecue.cn and get a `CUE_API_KEY`.
2. Export it: `export CUE_API_KEY=...`.
3. Check connectivity:

```bash
# 1) read the catalog, get the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) MCP handshake, confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**It also runs without the key**: with no key this skill only uses the announcement text and local files the user supplies; the cost is that it cannot reach the channel-side disclosure originals or attachment parsing, so anchors can only land on the copy the user gave and cross-file verification is not possible.

## 5. Boundaries and non-promises

- No liquidation-risk judgement (has liquidation risk, faces liquidation, margin-call risk, breached the warning line, breached the liquidation line, risk is controllable, risk is small, the pledge is safe).
- No rating of the ratio (pledge ratio high, low, reasonable, too high, sufficient, insufficient).
- No share-price prediction (the price will, bearish, bullish, suppresses the price, lifts the price, drags the price).
- No ratings or target prices.
- No return promises (guaranteed profit, zero risk, guaranteed yield, must rise, must fall).
- No drafting, no computing, no filing, no acting on the user's behalf.
- No adjudication of validity (whether the pledge is valid, non-compliant or compliant).
- No re-registering dividends, buybacks or reductions — that is `cn-shareholder-return`'s job; no single-announcement event brief — that is `event-brief-cn`'s job.

## 6. When a check fires

| Symptom | Cause | Fix |
|---|---|---|
| `SP-STRUCT 缺段` | A section heading was renamed or omitted | Write the five headings exactly as in SKILL.md §3 |
| `SP-STRUCT 本次变动明细段内无质押/解押行` | The change is only mentioned in prose | Give each entry its own line starting with `- 质押：` or `- 解押：` |
| `SP-STRUCT 质押行缺要素：质权人` | That entry's sentence does not name the pledgee | If the announcement omits it, mark the whole entry "not obtained" — never fill in common knowledge |
| `SP-STRUCT 累计与剩余行不是「前值 → 后值」两处之差` | Only the current balance was written | Add the prior value and write `before → after` |
| `SP-QUOTE 书名号内原句为空` | Paraphrased or left blank | Copy the original sentence; do not paraphrase |
| `SP-GAP 申报共 N 笔…` | Header declaration disagrees with the number of detail rows | Count the detail rows |
| `SP-GAP 比例 … 不在本行原句里` | The percentage was divided out by the card | Delete the self-computed ratio; if the announcement does not state it, write "not obtained" |
| `SP-BOUND 出现股东回报速读的项行` | The card became a dividend/buyback brief | Send it to `cn-shareholder-return` |
| `SP-BOUND 出现单份公告速读的单选行` | The card became a single-announcement brief | Send it to `event-brief-cn` |
| `SP-LINE 定式禁词` | A liquidation-risk judgement, ratio rating or price call was written | Delete it; register the original sentence or move it to "needs a human" |

## 7. How to ask (good and bad)

**Good**

- "How much has this controlling shareholder pledged, what share of its holdings, and what share of total capital?"
- "It pledged again three weeks later — chain the entries and show me how the balance moved."
- "How much was released this time, and when?"

**Bad**

- "Is this pledge ratio high, and is there liquidation risk?" → no risk judgement, no ratio rating; only the original sentences are registered.
- "With this much pledged, will the price fall?" → no price prediction.
- "Compute the pledge ratio for me." → no computing; percentages are only what the announcement states.
- "What does this announcement say?" → that is a single-announcement brief; use `event-brief-cn`.

## 8. Honest capability limits

- A percentage is only accepted when it appears in **that row's own quoted sentence**. When the announcement gives shares but no percentage, this skill records "not obtained" rather than dividing for you.
- The cumulative check verifies that **a difference of two points is present**, not that the arithmetic is right; please re-check the balance addition by hand.
- The six/three-element checks verify that the **nouns are present**, not the truth of the numbers.
- The release date check accepts a date label (`解除质押登记日` / `解押日` / `解除日` / `购回日`) or one of `2026 年 6 月 12 日`, `2026-06-12`, `2026/6/12`, `2026.6.12`.
- Relative wording such as "T day" or "the first day of the blank period" needs a human to convert; this skill does not do calendar maths.
- The pledgor is recognised by the wording in the original sentence (controlling shareholder, major shareholder, shareholder name); no entity resolution is performed, so when the same entity is written differently across announcements, align the cumulative rows by hand.

## 9. Resources

- `SKILL.md` — authoritative face (Chinese)
- `SKILL.en.md` — English twin
- `references/pledge-terms.md` — six and three elements, aliases, cut line
- `scripts/check_pledge_tracker.py` — the five-code checker
- `scripts/fixtures/` — one good sample, six bad samples, runner

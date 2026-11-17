# Earnings Pre-Announcement — every element quoted

Take **one** earnings pre-announcement or flash report and break it into six elements: type, range lower and upper bound, year-on-year change, reason, whether it was revised, and disclosure date — each carrying a `「」` quote and a retrieval date. Anything the filing omits is named as missing.

**No midpoint computed, no change computed, no final figure inferred, no ratings, no target prices.**

---

## 1. Start here: three steps

1. **Get the original**: this filing's announcement text, plus any correction filing alongside it.
2. **Copy six elements verbatim**: type, lower bound, upper bound, year-on-year change, reason, disclosure date.
3. **Run the self-check**, fix one red at a time:

```bash
python3 scripts/check_forecast.py your-draft.md
```

Exit code `0` clean, `1` findings, `3` unreadable file.

---

## 2. What the five lanes judge

| Code | Lane | Judges | Most often catches |
|---|---|---|---|
| `FC-STRUCT` | Structure | Four header self-marks before the first `## `; `基准日：YYYY-MM-DD` present; `数据口径：` present; six sections present and ordered; all six elements present; type in register; disclosure-date format; lower bound not exceeding upper; revision history non-empty with both values when revised | One of the six elements missing; a type written as "sharply higher", which is not in the register; revised but only the post-revision value given |
| `FC-QUOTE` | Quotes and anchors | Every element carries a non-empty `「」` quote and a `[S#]`; every row anchored or marked `[待人工]`; source rows carry number + URL + retrieval date; sources may not be empty | A reason row with no quote; an empty `「」`; a source row with a title but no link |
| `FC-LINE` | Red lines | No "beat / missed expectations", no ratings or target prices, no price forecasts, no buy-sell advice, no inferred final figures, no hedging words (`约` / `左右` / `大概`) — zero hits | "This pre-announcement beat expectations", "the price will rise", "advise accumulating" |
| `FC-CALC` | No self-calculation | **Never compute the range midpoint**, **YoY and revision magnitudes come only from the quoted sentence**, **never subtract the two revisions** — a midpoint term, a percentage, an arithmetic expression, or a magnitude label followed by a number all fire when outside quotes | `中值 35,000 万元`, `同比增幅 58.74%`, `(下限+上限)/2` |
| `FC-BOUND` | Boundaries | `数据口径` must start with 业绩预告 or 业绩快报; if the body mentions a full report, an all-filings list or an overnight panorama without naming the matching skill, that is named | Writing commentary on a published report; a basis line reading "commentary on the published report" |

### The cell that matters most: never compute it yourself

A pre-announcement gives a **range**, not a point. There are three actions a card takes that always land in this lane:

1. **Computing the midpoint** — `(32,000 + 38,000) / 2 = 35,000`. That 35,000 **is not in the filing**. If the filing states a midpoint, copy it; if not, the words "midpoint / centre / mean" may not appear.
2. **Computing the YoY change** — dividing this period by last period. If the filing says "up 45.12% to 72.35% year on year", copy that sentence; a percentage you computed is nowhere in the source.
3. **Computing the revision magnitude** — pre-revision 200 million, post-revision 320 million, difference 120 million. The filing does not say that. Register the two values **side by side**; a magnitude is copied if stated, marked missing if not.

The test is "outside quotes": the percentage inside `「比上年同期增长 45.12% 至 72.35%」` is legitimate (it is the source), any percentage outside quotes fires. A negated self-declaration in section five — "did not take the midpoint, did not subtract" — is not false-flagged, because that sentence is the basis statement itself.

### Revised or not must be stated

```markdown
## 三、修正沿革

- 修正前：「预计 20,000 万元至 24,000 万元」[S1]
- 修正后：「预计 32,000 万元至 38,000 万元」[S1]
- 修正说明：「本次业绩预告系对前次预告的更正」[S1]
```

If not revised, write `- 修正情况：「未发生修正／首次披露」[S#]`. Being **vague** — neither revised nor not-revised — fires `FC-STRUCT` exactly like an empty section.

---

## 3. Quick start

List the catalog, take the group's routing address from it, confirm the tools are present, then fetch filings and original-text parses before writing:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With the file list in hand you can lay out the skeleton first:

```bash
python3 scripts/make_outline.py list.jsonl skeleton.md
```

Then read each original and replace the placeholder rows with anchored quotes.

---

## 4. First-time Cue setup

This package reaches filings and original-text parsing through Cue's MCP channel. First use needs a credential (`CUE_API_KEY`), obtained from the Cue console and set as an environment variable; the package itself never stores or prints credentials.

You can also run it without the channel: with zero channel this package only lays the user's own forecast range out as a skeleton, and the cost is that it **cannot see the original text** — no original means no quoted sentences, four of the six elements have nothing to anchor to, and the note is just a handful of numbers the user typed in.

---

## 5. Boundaries and non-promises

- This registers **what the disclosure said**, not a judgment on whether the results are good.
- **No beat-or-miss judgment** — that is an evaluation, not a disclosure. If written at all, it carries `[待人工]`.
- **No inferred final figures**: a pre-announcement is a range, the annual report is a point. This package does not convert one into the other.
- Ratings, target prices, buy-sell advice and price forecasts: this package produces none.
- No research notes, news or forum posts. A fact without a filing link and a retrieval date does not enter the note.

---

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `FC-STRUCT` says an element is missing | One of the six was skipped | Add `- 项名：「quote」[S#]` — all six, none optional |
| `FC-STRUCT` says the type is not in the register | A phrasing like "sharply higher" | Use one of the nine: 预增／预减／扭亏／首亏／续盈／续亏／略增／略减／不确定 |
| `FC-STRUCT` says revised but no pre-revision value | Only the later value was written | Add `- 修正前：「…」[S#]` |
| `FC-QUOTE` says an element has no quote | A number was written without its sentence | Put the filing's own sentence inside `「」`, then anchor it |
| `FC-QUOTE` says the quote is empty | A `「」` placeholder was left | Fill it in, or write it as missing and list it in section five |
| `FC-CALC` says a midpoint term appeared | The range midpoint was computed | Delete it; if the filing doesn't state it, the number does not exist |
| `FC-CALC` says a percentage appeared outside quotes | A YoY or revision magnitude was computed | Move it inside the quote if the source has it, otherwise delete it |
| `FC-CALC` says an arithmetic expression appeared | Something like `(lower+upper)/2` | Delete the expression; register only the two bounds |
| `FC-LINE` says it hit "beat expectations" | An evaluation slipped in | Delete the evaluation, or mark the whole sentence `[待人工]` |
| `FC-BOUND` says the basis doesn't start correctly | The basis line drifted into report commentary | Start it with 业绩预告 or 业绩快报 |

---

## 7. How to ask

- **Good**: "What did this company's pre-announcement say?" "What is the forecast range?" "How does the filing word the YoY change?" "Was it revised, and what were the values before and after?" "What reason does it give?"
- **Bad**: "Did it beat expectations?" "Will the price rise?" "Give me a target price." "Is it worth buying?" — this package produces none of these and returns `[待人工]`.

---

## 8. Honest capability limits

- Only the disclosure counts. Where it is vague, this package stays vague and names the gap rather than filling it in.
- Pre-announcements usually give a consolidated net-profit range only; quarterly or product splits are generally not disclosed and can only be recorded as missing.
- The reason given is usually one summary sentence; this package copies it and does not re-attribute it.
- The checker judges shape and sourcing discipline, not whether the numbers are true. Verifying the numbers is a human step against the original text — which is exactly what the four header self-marks are for.

---

## 9. Resources

- `SKILL.md` — the Chinese contract (six-section shape, verbatim discipline, red lines)
- `SKILL.en.md` — the English face of the same contract
- `scripts/check_forecast.py` — five lanes, zero network
- `scripts/make_outline.py` — lays a filing list out as a shaped skeleton; runs with zero channel
- `scripts/fixtures/run_fixtures.sh` — three-tier offline self-check, thirty seconds, zero network, zero billing
- `CHANGELOG.md` — versions and known limits

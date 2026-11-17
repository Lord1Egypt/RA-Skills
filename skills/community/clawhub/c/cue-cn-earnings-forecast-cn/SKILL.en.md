---
name: cn-earnings-forecast-cn
slug: cue-cn-earnings-forecast-cn
displayName: "业绩预告速读·区间与修正逐条挂源 (Earnings Pre-Announcement)"
summary: "One earnings pre-announcement's six elements, quoted and sourced."
description: "A-share earnings pre-announcements: type, range, YoY change, reason, revised or not, date - each row quoted. Never compute the midpoint. Do NOT use for: full-report commentary (cn-earnings-note), all-filings lists, ratings, price calls. Triggers: 业绩预告 / 业绩快报 / 预告修正 / 预亏预盈 / 预告区间"
version: "0.1.0"
license: MIT
---

# Earnings Pre-Announcement · Every Element Quoted

## 0. What this is, and what it is not

| Is | Is not |
|---|---|
| **One** earnings pre-announcement or flash report, six elements registered item by item | Commentary on a full report already published |
| Every element carries a `「」` quote and a retrieval date; gaps named one by one | Judging "beat or missed expectations", or calling the share price from it |
| Revised or not: the pre-revision and post-revision values side by side | Computing the range midpoint yourself, or subtracting one value from the other |
| Numbers copied as disclosed — never converted, never reworded | Inferring the final audited number, giving ratings or target prices |
| One document's itemised registration | A list of all filings that day, or an overnight panorama over a basket of names |

**Three boundaries (this is how a user tells the neighbouring skills apart):**

- `cn-earnings-note` comments on the **full report already published** — how revenue moved, how margins moved, why. This skill **does not comment**; it registers what the pre-announcement or flash report itself said.
- `announcement-daily-cn` is a list of **all filings from one company on one day**. This skill takes only the **pre-announcement / flash report** from among them, and registers it item by item rather than listing it.
- `cn-morning-brief` is an **overnight panorama over a basket of names**. This skill is an itemised registration of **one document**.

**What "never compute it yourself" means here — three specific things:**

1. **Never compute the range midpoint.** `(lower + upper) / 2` is a number the card invented; the disclosure contains no such sentence. If the disclosure states a midpoint, copy it and anchor it; if not, the words "midpoint / centre / mean" may not appear outside a quote.
2. **Year-on-year change comes only from the quoted sentence.** If the disclosure says "up 45.12% to 72.35% year on year", copy that sentence. A percentage the card derives by dividing this period by last period is nowhere in the source.
3. **Never subtract to get a revision magnitude.** Pre-revision 200 million, post-revision 320 million — the 120 million difference is not in the disclosure. Register the two values **side by side**; if the disclosure gives a magnitude, copy it, and if not, write it as missing.

## 1. When to use it

- "What did this company's pre-announcement just say?" / "Is it a profit increase, a turnaround, or a first loss?"
- "What is the forecast range?" / "How large is the year-on-year change?"
- "Was this pre-announcement revised, and what were the values before and after?"
- "What reason does the filing give for the change?"

**Do not use** for: commenting on a full published report (go to `cn-earnings-note`); a list of all filings that day (go to `announcement-daily-cn`); an overnight panorama over a basket (go to `cn-morning-brief`); judging beat-or-miss, ratings, target prices or share-price direction (this skill produces none, and none should).

## 2. Verbatim discipline

1. **Only the disclosure counts.** Every element must trace back to a pre-announcement or flash report with a link and a retrieval date. Research notes, news and forum posts are never sources.
2. **Quote every element.** Each of the six is written `- 项名：「original sentence」[S#]`, where the quoted text is the filing's own wording, not a paraphrase. An empty quote means nothing was sourced.
3. **Never reword numbers.** 32,000 万元 stays 32,000 万元 — not "about 320 million yuan", not "around 300 million".
4. **Never take the midpoint.** See the three rules in section 0.
5. **Never compute a change.** Year-on-year, quarter-on-quarter, revision magnitude — if the disclosure doesn't state it, write it as missing, never substitute a division or subtraction.
6. **Revised or not must be stated.** If revised, the pre-revision and post-revision values stand side by side; if not, write "not revised / first disclosure". Being vague — neither revised nor not-revised — is equally wrong.
7. **If it's missing, write that it's missing.** The body says "missing X" ⇒ section five must name X; section five names X but the body has no such statement ⇒ also wrong. Both directions are judged.
8. **Never infer the final number.** A pre-announcement is a range, the annual report is a point. This skill does not write "the final figure will be" or "extrapolating from this".

## 3. Output contract (six sections, in order)

```
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：2026-11-09
数据口径：业绩预告（单份预告文件逐项登记，不评已出财报，不推断正式数）

## 一、一句话结论
## 二、预告要素
## 三、修正沿革
## 四、未决事项
## 五、未取到与口径
## 六、来源
```

- **Four header self-marks** verbatim, before the first `## `.
- **Base date** line must start with `基准日：` and carry a `YYYY-MM-DD` value; missing or unreadable both fire.
- **Data basis** line must start with `业绩预告` or `业绩快报` — this cell is the boundary against full-report commentary, so it must self-declare. If the filing date is close to a published report and the body cites a report summary, write `数据口径：业绩预告＋已出财报对照（预报为主，财报段走 cn-earnings-note）` — do not rename the basis.
- **Section two (elements)** has six rows, one each, in the form `- 项名：「quote」[S#]`:
  type (register: 预增／预减／扭亏／首亏／续盈／续亏／略增／略减／不确定), range lower bound, range upper bound, year-on-year change, reason, disclosure date (`YYYY-MM-DD`).
  The lower bound may not exceed the upper bound; comparing two numbers produces no new number.
- **Section three (revision history)**: if revised, write `- 修正前：「…」[S#]` and `- 修正后：「…」[S#]`, plus a line of explanation; if not, write `- 修正情况：「未发生修正／首次披露」[S#]`. An empty section hides the history.
- **Section four (open items)**: between a pre-announcement and the final report there are always open items (when the range narrows, whether there is a performance commitment, whether audit adjustments may follow). An empty section hides uncertainty.
- **Section five (missing items and basis)**: name each missing item; the basis line states whether the range and change were copied or left missing.
- **Section six (sources)** rows: `- [S#] 文件标题 URL 检索日 YYYY-MM-DD`, numbers matching the body anchors one-to-one.

## 4. Data channel

This skill reaches filings and original-text parsing through Cue's MCP channel. List the catalog first, take the group's routing address from it, confirm the tools are present, then fetch:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With the pre-announcement and flash-report files in hand, use `scripts/make_outline.py` to lay the list out as a skeleton, then read each original to fill it in.

## 5. Compliance red lines

- **No beat-or-miss judgment.** That is an evaluation, not a disclosure. If written at all, it must carry `[待人工]` on the same row.
- **No ratings, target prices, investment advice, or buy-sell / reduce advice.**
- **No share-price forecasts** — no "will rise", "will fall", "poised to strengthen".
- **No inferred final figures.** A range is not converted into a point estimate, and "the final figure should be" is not written.
- **No hedging words as a substitute** for an exact number from the disclosure.
- **No second-hand sources.** A fact without a filing link and retrieval date does not enter this note.

## 6. Quick flow

1. Fix the base date; fetch the original pre-announcement or flash report (including any correction filing).
2. Copy the six elements verbatim: type, lower bound, upper bound, year-on-year change, reason, disclosure date.
3. Check whether it was revised: if so, place the pre- and post-revision values side by side; if not, state that plainly.
4. Write open items and missing items, aligned in both directions.
5. Run `python3 scripts/check_forecast.py <draft>.md` and fix one red at a time.

## 7. Machine checks

```bash
python3 scripts/check_forecast.py <draft>.md      # five lanes, exit 0 clean / 1 findings / 3 unreadable
python3 scripts/check_forecast.py --selftest      # in-package fixture self-test
bash scripts/fixtures/run_fixtures.sh             # three-tier offline self-check, 30 seconds, zero network, zero billing
```

Five lanes: **lane one, structure** (header self-marks, base date, data basis, six sections present and ordered, six elements present, type in register, disclosure-date format, lower bound not exceeding upper, revision history non-empty with both values) / **lane two, quotes and anchors** (every element carries a non-empty `「」` quote and a `[S#]`; every row anchored or marked `[待人工]`; source rows carry number, URL and retrieval date; sources may not be empty) / **lane three, red lines** (beat-or-miss evaluations, ratings and target prices, buy-sell advice, price forecasts, inferred final figures, hedging words — zero hits) / **lane four, no self-calculation** (a midpoint term, a percentage, an arithmetic expression, or a magnitude label followed by a number outside quotes all fire; negated self-declarations like "did not take the midpoint" are not false-flagged) / **lane five, boundaries** (data basis must start with pre-announcement or flash report; if the body mentions a full report, an all-filings list or an overnight panorama without naming the matching skill, that is named).

## 8. Zero-channel degradation

Without `CUE_API_KEY` this package **produces no content**: it only lays the user's own forecast range out as a shaped skeleton — six elements and source rows placed from the user's list, conclusion and basis left as placeholders. A skeleton necessarily fails the checker on its placeholder rows — that is by design, a reminder to finish before delivering. The cost, stated plainly: **no channel means no original text; no original text means no quoted sentences; without quoted sentences four of the six elements have nothing to anchor to**, and the note is just a handful of numbers the user typed in.

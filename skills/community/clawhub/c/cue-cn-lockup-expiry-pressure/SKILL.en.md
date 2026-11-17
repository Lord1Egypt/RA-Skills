---
name: cn-lockup-expiry-pressure
slug: cue-cn-lockup-expiry-pressure
displayName: "限售解禁压力·逐条挂源 (Lockup Expiry Pressure)"
summary: "Chain one stock's future lockup expiries into a dated, sourced calendar."
description: "A-share lockup expiries as a calendar: date, holder type, shares, share of total capital (denominator sourced separately) and cost band, each row anchored. Do NOT use for: price calls, ratings, target prices, buy-sell advice, past dividends or reductions (go to cn-shareholder-return)."
version: 0.1.2
license: MIT
---

# Lockup Expiry Pressure · Every Row Sourced

## 0. What this is, and what it is not

| Is | Is not |
|---|---|
| Several **upcoming** lockup expiries of one stock, chained into a calendar by expiry date | Already-happened reductions, dividends, buyback registrations |
| Each round records expiry date, holder type, shares released, share of total capital, cost basis | Judging whether the unlock will hit the price, or where the price goes |
| The **denominator** (total share capital) is sourced on its own; the card never divides shares by it silently | Smoothing a missing number over with "about" or "roughly" |
| Every row carries an announcement link and a retrieval date | Second-hand reporting or research-note summaries |
| Missing items named round by round, in both directions | Buy-sell advice, ratings, target prices |

**Boundary against `cn-shareholder-return` (this one sentence is how a user tells the two apart):**

- `cn-shareholder-return` registers **already-happened shareholder actions** — what the announcement said about dividends, buybacks, reductions, pledges.
- This skill lays out the **future expiry timetable** — which day, how many shares, what share of total capital, which holder type, which cost band.
- The test is hard: **expiries before the base date never enter this calendar** — those already happened and belong to `cn-shareholder-return`; pledge and release-of-pledge balance changes belong to `cn-share-pledge-tracker`.

**What "pressure" means here (said up front, to prevent misreading):**

Pressure here means **two checkable things**: (1) each round's released shares **as a share of total capital** — numerator anchored to the release announcement, denominator (total share capital) anchored separately, one anchor each, two sources; (2) each round's **cost band** — the original issue or grant price for that tranche, registered only, never compared with the market price. Both are retrievable from announcements and can be checked against the original text. **Bands and ratings are not this skill's job** — "is this round big or small", "will the unlock create selling pressure", "where does the price go after" are all `[待人工]` (hand to a human); this skill does not conclude that, and does not pretend an objective threshold exists.

## 1. When to use it

- "How many lockup rounds does this stock have in the next year?" / "When is the next expiry and how many shares?"
- "What share of total capital does the unlock represent?" / "Is the holder a controlling shareholder or a placement investor?"
- "What was the placement price / grant price back then — which cost band does this round sit in?"

**Do not use** for: already-happened reduction progress (go to `cn-shareholder-return`); pledge and release-of-pledge balance changes (go to `cn-share-pledge-tracker`); price forecasts, buy-sell timing, ratings or target prices (this skill produces none, and none should).

## 2. Sourcing discipline

1. **Only the original announcement counts.** Every fact must trace back to an announcement, prospectus or placement document with a link and a retrieval date. Research notes, news and forum posts are never sources.
2. **Fix the base date first.** The header carries `基准日：YYYY-MM-DD` (normally the retrieval date). **Every calendar row's expiry date must be later than the base date** — earlier expiries are facts that already happened, not this timetable.
3. **Take the expiry date as disclosed**, not derived from the lock-up period start and not from a media report. Format `YYYY-MM-DD`.
4. **The calendar is non-descending by date.** A reversed calendar is not a calendar.
5. **The denominator is sourced separately.** Every row's "share of total capital X%" must note, on the same row, the denominator share count and its own source anchor — numerator and denominator come from two places, so two anchors. **Never divide it out yourself**: if the announcement states the percentage, copy it; only when the announcement states shares and no percentage do you divide by the same-row total capital, and then say so in section six.
6. **The cost band only takes prices written in the document.** Placement investors → issue price; equity-incentive holders → grant price; pre-IPO shareholders → issue price. If the document doesn't say, write it as missing — never substitute "estimated at market price".
7. **If it's missing, write that it's missing.** The body says "missing X" ⇒ section six must name X; section six names X but the body has no such statement ⇒ also wrong. Both directions are judged.
8. **Never rewrite numbers.** 1.2 亿股 stays 1.2 亿股 — not "about 1.2 亿股", not "around 1 亿股".

## 3. Output contract (seven sections, in order)

```
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：2026-11-09
跟踪口径：解禁（未来解禁的时间表与可算的压力比值，同一只股票的限售股逐轮串起来）

## 一、一句话结论
## 二、解禁总览
## 三、解禁日历
## 四、压力测算
## 五、未决事项
## 六、未取到与口径
## 七、来源
```

- **Four header self-marks** verbatim, before the first `## `.
- **Base date** line must start with `基准日：` and carry a `YYYY-MM-DD` value; missing or unreadable both fire.
- **Tracking basis** line must start with `解禁` — this cell is the boundary between this skill and already-happened shareholder behaviour, so it must self-declare.
- **Section two (overview)** rows: `- 项名：值 [S#]`, and **one row must be total share capital** (`- 总股本：N 股 [S#]`) — it is the denominator for every ratio in section four and must carry its own source; **each round's cost band also lives here**, one round per row (`- 第 N 轮成本区间：发行价或授予价 N 元／股 [S#]`), original value only, never compared with the market price, never a spread computed.
- **Section three (calendar)** rows: `- YYYY-MM-DD｜解禁方类型｜一句话事实 [S#]`. Holder types in register: 控股股东／实际控制人／董监高／定增对象／股权激励对象／首发原股东／战略投资者／其他.
- **Section four (pressure)** rows: `- 第 N 轮 YYYY-MM-DD｜解禁 N 股／占总股本 X.XX%（分母总股本 N 股）｜占比出处：公告原文或自算 [S#][S#]` — **at least two different anchor numbers**, numerator and denominator each from its own place.
- **Section five (open items)**: a plan that hasn't run all its rounds always leaves open items (is the next expiry date fixed, has the holder made a commitment). An empty section hides uncertainty.
- **Section seven (sources)** rows: `- [S#] 公告标题 URL 检索日 YYYY-MM-DD`, numbers matching the body anchors one-to-one.

## 4. Data channel

This skill reaches announcements and original-text parsing through Cue's MCP channel. List the catalog first, take the group's routing address from it, confirm the tools are present, then fetch:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With the announcement and prospectus/placement document list in hand, use `scripts/make_outline.py` to lay the list out as a skeleton, then read each original to fill it in.

## 5. Compliance red lines

- **No price forecasts, rise-fall promises, buy-sell or reduction advice, ratings, target prices, or lockup-pressure band judgments.** Any such line must carry `[待人工]` on the same row and go to a human.
- **Never treat "unlock" as "reduction".** An unlock means the lock-up has expired and the shares become tradable; whether to sell is the holder's call. This skill writes neither "unlock means dumping" nor "guaranteed cash-out", and never "selling pressure".
- **No hedging words as a substitute.** "约", "左右", "大概" may not stand in for an exact number from an announcement.
- **No second-hand sources.** A fact without an announcement link and retrieval date does not enter the calendar.
- **Never guess an expiry date.** If the announcement gives no specific date, write it as missing — do not derive one from "tradable once the lock-up period ends".

## 6. Quick flow

1. Fix the base date; collect the stock's restricted-share source material: prospectus, placement result announcement, equity-incentive grant announcement, restricted-share listing announcement.
2. For each document note: expiry date, holder type, shares, share of total capital, cost price, link and retrieval date.
3. Lay out the calendar (`make_outline.py` can do the skeleton), then fill in one-sentence facts row by row.
4. Write section four: the denominator (total share capital) sourced on its own, one anchor for the numerator and one for the denominator.
5. Write open items and missing items, aligned in both directions.
6. Run `python3 scripts/check_lockup.py <draft>.md` and fix one red at a time.

## 7. Machine checks

```bash
python3 scripts/check_lockup.py <draft>.md       # five lanes, exit 0 clean / 1 findings / 3 unreadable
python3 scripts/check_lockup.py --selftest       # in-package fixture self-test
bash scripts/fixtures/run_fixtures.sh            # offline self-check, 30 seconds, zero network, zero billing (tier count computed and printed on the last line)
```

Five lanes: **lane one, structure** (header self-marks, base date, tracking basis, seven sections present and ordered, total-capital row present, calendar rows three-cell with non-descending dates all later than the base date, pressure row shape) / **lane two, anchors** (every row anchored, source rows carry URL and retrieval date, pressure rows carry at least two distinct anchors) / **lane three, red lines** (price forecasts, rise-fall promises, buy-sell advice, ratings and target prices, lockup-pressure band judgments, hedging words — zero hits) / **lane four, two-way missing-item naming** (body and section six reconciled by item identity; over-listing and under-listing both fire; every pressure row must declare whether its percentage came from the announcement text or was calculated, and a calculated one must be explained in section six) / **lane five, boundaries** (tracking basis written as already-happened / reduction / dividend / buyback / shareholder return, or a calendar with fewer than two rounds → name `cn-shareholder-return`; written as pledge / release-of-pledge → name `cn-share-pledge-tracker`).

## 8. Zero-channel degradation

Without `CUE_API_KEY` this package **produces no content**: it only lays the user's own expiry list out as a shaped skeleton — calendar and source rows placed, conclusion, ratios and cost bands left as placeholders. A skeleton necessarily fails the checker on its placeholder rows — that is by design, a reminder to finish before delivering, not an empty shell posing as a finished note. The cost, stated plainly: **no channel means no original text; no original text means no denominator and no cost price; without those three the note is just a run of dates** and neither of the two pressure quantities (share of total capital, cost band) can be computed.

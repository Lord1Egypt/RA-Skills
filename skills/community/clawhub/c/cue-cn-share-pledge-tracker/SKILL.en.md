---
name: cn-share-pledge-tracker
slug: cue-cn-share-pledge-tracker
displayName: "股权质押与解押跟踪·逐条挂源"
summary: "Chain one shareholder's pledges and releases into a balance timeline."
description: "A-share pledge tracking: chain one shareholder's pledge and release announcements into a balance timeline, six elements per pledge and three per release, cumulative as before → after, each anchored to the announcement. Do NOT use for: liquidation-risk judgement, ratio rating, price calls."
version: "0.1.0"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      recommendedSkills: ["cue-data-mcp", "cue-omni-reader"]
    envVars:
      - name: CUE_API_KEY
        required: false
        description: "Optional credential: without it this skill follows the user-supplied and degraded path described on the face; with it, the channel-side disclosure originals and attachment parsing are available."
tags: [股权质押, 解押, 质押比例, 余额变化, 逐条挂源]
---

# Share Pledge & Release Tracker

Chain **multiple** pledge and release announcements of the same shareholder into one **balance timeline**:
each entry registers pledgor, pledgee, shares, share of holdings, share of total capital and pledge period;
cumulative and remaining are written as "before → after"; every entry carries the announcement's own sentence and its anchor.

**Cut line**: this skill answers only "how did the pledge balance change". **Dividends, buybacks and reductions belong to `cn-shareholder-return`**;
**what a single announcement says belongs to `event-brief-cn`**. This skill does not judge liquidation risk, does not rate the ratio, does not predict the share price.

## 0. What it is / what it is not

| Is | Is not |
|---|---|
| Multiple pledges/releases of one shareholder chained into a balance timeline | An event brief of a single announcement |
| Six elements per pledge entry / three per release entry, registered one by one | A one-line narrative such as "another pledge was made" |
| Cumulative and remaining written as "before → after" | Only the current balance, with no visible change |
| Percentages taken only from the announcement's own sentence | Dividing pledged shares by holdings or total capital yourself |
| Anything the announcement omits written as "not obtained" | Concluding "not applicable / no disclosure needed" on the announcement's behalf |

## 1. When to use

- The user hands over one or more pledge/release announcements and asks "how much has this shareholder pledged, and how much is left".
- The user asks "what is the pledge ratio — of holdings, of total capital".
- The user wants several pledges of the same shareholder, weeks apart, chained to see how the balance moved.
- The user asks "how much was released, and when".

## 2. Data discipline

1. **Announcement text only**: every fact must trace back to a sentence and anchor in an announcement. Research notes, news and forum posts are never sources.
2. **Six elements per pledge entry**: pledgor, pledgee, pledged shares, share of holdings, share of total capital, pledge period — one missing fires.
3. **Three elements per release entry**: pledgor, released shares, release date — one missing fires.
4. **Percentages only from the announcement's own sentence**: a percentage must appear inside that row's own quoted sentence. If the announcement does not state it, write "not obtained" — **never divide pledged shares by holdings or total capital yourself**. The denominator may be holdings, total capital, or capital excluding the buyback account; one wrong denominator and every risk reading is wrong.
5. **Cumulative and remaining must be a difference of two points**: written as `before → after`, with a number on each side. A single point is not a change.
6. **Two-way reconciliation of the not-obtained declaration**: the header line `共 N 笔质押变动·未取到 M 笔` appears exactly once, and both N and M must equal the actual row count and the "not obtained" row count in the detail section. Over-declaring is inflation, under-declaring is omission — both fire.
7. **Never write "not applicable"**: writing "no such item / not applicable / no disclosure needed" instead of "not obtained" concludes on the announcement's behalf; it is not registration.
8. **Judgement goes to a human**: liquidation risk, whether the ratio is high, share-price impact — all go to "needs a human".

## 3. Output contract (five sections)

```
## 一、头部申报
- 文件：<company> <announcement title>｜来路：官方原文／用户直供｜附件腿：已发起／未发起
- 共 N 笔质押变动·未取到 M 笔

## 二、本次变动明细
- 质押：「<sentence with pledgor · pledgee · shares · share of holdings · share of total capital · period>」 锚：<source>
- 解押：「<sentence with pledgor · released shares · release date>」 锚：<source>
- 质押：未取到（未取到清单已点名）

## 三、累计与剩余
- <pledgor>：累计质押 <before> → 累计质押 <after>
- <pledgor>：占其所持股份 <before> → 占其所持股份 <after>
- <pledgor>：占公司总股本 <before> → 占公司总股本 <after>

## 四、未取到清单
- 未取到 M 笔：<which entry>——<what is missing>, check against <which document>.

## 五、待人工
- [待人工] <whether the ratio is high / whether liquidation risk exists / share-price impact> all left to a human; this skill neither drafts nor judges risk.
```

## 4. Data channel (live catalog is authoritative)

Real tasks take the channel path: read the catalog first, then fetch originals and attachment text by tool name.

```bash
# 1) read the catalog, get the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) MCP handshake, confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Once the endpoint is known, confirm `parse` / `get_parse_status` / `read_result` are present,
then hand the announcement URL or local path to `parse`, poll with `get_parse_status`, and read text and tables with `read_result`.

**Zero-key degradation**: without `CUE_API_KEY` this skill only uses the announcement text and local files the user supplies; the cost is that it cannot reach the channel-side disclosure originals or attachment parsing, so anchors can only land on the copy the user gave and cross-period verification is not possible.

## 5. Red lines

- No liquidation-risk judgement (has liquidation risk, faces liquidation, margin-call risk, breached the warning line, breached the liquidation line, risk is controllable, risk is small, the pledge is safe).
- No rating of the ratio (pledge ratio high, low, reasonable, too high, sufficient, insufficient).
- No share-price prediction (the price will, bearish, bullish, suppresses the price, lifts the price, drags the price).
- No ratings or target prices.
- No return promises (guaranteed profit, zero risk, guaranteed yield, must rise, must fall).
- No drafting, no computing, no filing, no acting on the user's behalf.
- No adjudication of validity (whether the pledge is valid, non-compliant or compliant).

## 6. Quick flow (user's view)

1. Hand the pledge/release announcements (URL or local file, possibly several) to this skill.
2. It registers six elements per pledge entry and three per release entry, each anchored to its own sentence.
3. Cumulative and remaining are written as "before → after", so the balance movement is visible.
4. Anything the announcement omits goes into the not-obtained list, naming which document to check.
5. Every judgement question goes to "needs a human"; this skill does not take it.

## 7. Machine checks

```bash
python3 -B scripts/check_pledge_tracker.py <card.md>     # five codes, PASS when clean
python3 -B scripts/check_pledge_tracker.py --selftest    # good sample passes, bad samples fire
bash scripts/fixtures/run_fixtures.sh                    # three tiers, no network, no billing
```

Five codes: `SP-STRUCT` five sections · entries present line by line · six elements per pledge / three per release · cumulative rows must be a difference of two points /
`SP-QUOTE` quoted sentence and anchor must not be empty / `SP-LINE` three red-line families /
`SP-GAP` two-way not-obtained reconciliation + percentages must not be self-computed / `SP-BOUND` names the right skill when the card became a shareholder-return brief or a single-announcement brief.

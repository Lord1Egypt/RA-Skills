---
name: cn-controlling-shareholder-change-cn
slug: cue-cn-controlling-shareholder-change-cn
displayName: "实控人变更与要约收购·逐条挂源"
summary: "Control-change card: eight anchored items; ratios never self-computed."
description: "A-share control change: transfer, voting delegation, tender offer, judicial auction, inheritance. Eight items anchored to filing sentences; consideration never multiplied, premium never computed. Do NOT use for: bull/bear calls, next-move guesses, ratings. Triggers: 实控人变更 / 控制权变更 / 要约收购 / 协议转让"
version: "0.1.0"
license: MIT
consumes:
  - parsed-doc
inputs:
  - announcement-doc
  - disclosure-file
produces:
  - structured-note
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      recommendedSkills: ["cue-data-mcp", "cue-omni-reader"]
    envVars:
      - name: CUE_API_KEY
        required: false
        desc: "Optional credential. Without it the card falls back to filings the user supplies directly, per the face text; with it the channel can fetch the equity-change and tender-offer filings themselves."
tags: [control-change, tender-offer, agreement-transfer, voting-rights-delegation, source-anchored]
---

# Control Change and Tender Offer · Every Item Anchored

Break **one control-change event** into eight items, each anchored to the filing's own sentence:
who transfers, who receives, how many shares, what percentage, how much money, and who holds control
before and after. **Ratios and consideration are only what the filing says** — shares are never
multiplied by price, and two numbers are never divided to invent a percentage.

**Dividing line**: this package covers the **process by which control changes hands**. Shareholder
action results (dividends, buybacks, reductions) belong to `cn-shareholder-return`; merger and
restructuring progress (suspension / draft / approval / implementation) belongs to
`cn-restructuring-tracker`; pledge and release details belong to `cn-share-pledge-tracker`.
This package makes no bull/bear call and does not guess the new controller's next move.

## 0. What it is / what it is not

| Is | Is not |
|---|---|
| The **process** of control changing hands: who acquires, by what path, at what price | Registration of dividend/buyback/reduction results (that is `cn-shareholder-return`) |
| Six paths: agreement transfer / voting-rights delegation / open-market accumulation / tender offer (incl. partial) / judicial auction / inheritance | Tracking merger-and-restructuring progress (that is `cn-restructuring-tracker`) |
| Eight items, each anchored to its own sentence | One "control of the company has changed" overview paragraph |
| Ratios and consideration **only as the filing states them** | Multiplying shares by price for consideration, or dividing two numbers for a ratio |
| Offer price and premium **on separate rows** | Subtracting the market price from the offer price to make a premium |
| "Not obtained" when the filing is silent | Filling gaps from common sense, quotes, or inference |

## 1. When it fires

- The user has an equity-change report, a detailed equity-change report, or a tender-offer report,
  and asks who the new controller is and how much they paid.
- The user asks how many shares changed hands, what percentage that is, and at what price.
- The user asks for the offer price, the premium, and whether the offer is partial.
- The user needs a non-trade path (voting-rights delegation, judicial auction, inheritance)
  registered as a control change.

## 2. Sourcing discipline

1. **Only the filing's own text**: every item must trace to an original sentence plus an anchor
   (`[S#]`). News, forums, and broker summaries are never cited as sources.
2. **All eight items present**: change path, transferor, transferee, shares, percentage,
   consideration, control holder **before**, control holder **after**. One missing is a finding;
   if the filing is silent, write the item as "not obtained", list it in the not-obtained section,
   and **never fill it from common sense**.
   (Before/after are two rows because they are frequently two different names — merging them makes
   "who before, who after" unreadable.)
3. **Percentage only from the sentence**: the percentage must appear inside **that row's own quoted
   sentence**. When the filing gives shares but no ratio, this package records "not obtained" rather
   than dividing shares by share capital — the denominator might be total share capital, capital net
   of treasury shares, or a voting-rights basis, and one wrong denominator corrupts every control read.
4. **Consideration only from the sentence**: the amount must appear inside that row's own quoted
   sentence. **Never multiply shares by a per-share price to produce a total** — filings routinely say
   "price to be agreed" or "to be determined separately", and the product is something the card invented.
5. **Offer price and premium on separate rows**: for a tender offer (including partial), `offer price`
   and `premium` each get their own row. **An undisclosed premium is never computed** — the premium's
   basis (30-day average, prior-day average, pre-suspension price) must be present in the filing;
   subtracting the market price and dividing gets the basis wrong and corrupts the whole read.
6. **Not-obtained named in both directions**: the header's "8 items, N not obtained" appears once,
   and both numbers must equal the actual item rows and "not obtained" rows in the detail section.
   Over-reporting is inflation, under-reporting is omission; both fire.
7. **Never write "not applicable"**: turning "not obtained" into "no such item / not applicable /
   not required to disclose" answers for the filing instead of registering it.
8. **Judgment stays human**: bull/bear, the new controller's next move, control stability, and
   price impact all go to "for human review".

## 3. Output contract (six sections)

```
## 一、头部申报
- 文件：<company> <filing name>｜来路：官方原文／用户直供｜附件腿：已发起／未发起
- 共 8 项要素·未取到 1 项

## 二、变更要素明细
- 变更方式：「<sentence>」 锚：<locator> [S1]
- 出让方：「<sentence>」 锚：<locator> [S1]
- 受让方：「<sentence>」 锚：<locator> [S1]
- 变动股数：「<sentence>」 锚：<locator> [S1]
- 变动比例：「<sentence with percentage>」 锚：<locator> [S1]
- 交易对价：「<sentence with amount>」 锚：<locator> [S1]
- 变更前控制权归属：「<sentence>」 锚：<locator> [S1]
- 变更后控制权归属：「<sentence>」 锚：<locator> [S1]
- 交易对价：未取到（未取到清单已点名）

## 三、要约收购专段
- 要约价：「<sentence with per-share price>」 锚：<locator> [S2]
- 溢价率：「<sentence with percentage and basis price>」 锚：<locator> [S2]
(non-tender path: - 本笔不涉及要约收购，无要约价与溢价率。)

## 四、未取到清单
- 未取到 M 项：<which item>——<what is missing>, check back against <which document>.

## 五、待人工
- [待人工] 对新实控人后续动作、控制权稳定性、股价影响的判断，全部留人工；本件不接代办，也不给方向。

## 六、来源索引
- [S1] <filing name>｜<URL>｜检索日 <YYYY-MM-DD>
- [S2] <filing name>｜<URL>｜检索日 <YYYY-MM-DD>
```

## 4. Data channel (live catalog is authoritative)

Real tasks take the channel path: read the catalog first, then fetch filing text and attachments.

```bash
# 1) read the catalog for the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) complete the MCP handshake and confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Once the endpoint answers, confirm `parse` / `get_parse_status` / `read_result` are present, hand the
filing URL or local path to `parse`, poll with `get_parse_status`, and pull text and tables with
`read_result`.

**Zero-key fallback**: without `CUE_API_KEY` the card only works from filings the user supplies
directly or from local files. The cost is that channel-side filing text and attachment parsing are
unavailable, anchors can only point at the copy the user handed over, and cross-document checks
cannot be done.

## 5. Compliance red lines (ships with the suite)

- No bull/bear calls (bullish, bearish, major positive, neutral-to-bullish, lifts the share price,
  weighs on the share price).
- No guessing the new controller's next move (will inject, expected to restructure, may acquire more,
  aims to backdoor-list, intended to inject).
- No price forecasts (price will, price is set to, poised to rise, bullish, bearish).
- No ratings or target prices (target price, rating, buy rating, accumulate rating, strong
  recommendation, recommends buying, recommends selling).
- No return promises (sure win, must rise, must fall, zero risk, guaranteed profit).
- No drafting, no computing on the user's behalf, no filing on the user's behalf, no acting as agent.
- No validity rulings (whether the change is effective, non-compliant, compliant, or constitutes a
  control change).

## 6. Quick flow (user's view)

1. Hand over the equity-change report or tender-offer report (URL or local file, several allowed).
2. The card registers the eight items, each anchored to its own sentence.
3. A tender path gets two extra rows: offer price and premium (write "not obtained" when undisclosed).
4. Whatever the filing omits goes to the not-obtained list naming the document to check; judgment
   questions all go to "for human review".

## 7. Machine checks

```bash
python3 -B scripts/check_control_change.py <card.md>       # five codes fire per item; PASS when clean
python3 -B scripts/check_control_change.py --selftest      # good passes, five bads each fire their own code
bash scripts/fixtures/run_fixtures.sh                      # three offline tiers (no network, no billing)
```

Five codes: `CC-STRUCT` six sections present, eight items at row level, declared counts aligned both
ways / `CC-QUOTE` sentence non-empty, anchor value non-empty, `[S#]` present and resolvable in the
source index / `CC-CALC` no self-computation (ratio and consideration must be in the row's own sentence,
premium never subtracted out) / `CC-LINE` the three red-line classes / `CC-BOUND` names the sibling
package when the card drifts into shareholder returns, restructuring progress, or pledge details.

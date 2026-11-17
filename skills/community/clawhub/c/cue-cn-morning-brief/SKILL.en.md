---
name: cn-morning-brief
slug: cue-cn-morning-brief
displayName: "晨会纪要·数据槽与覆盖率（盘前早报）"
summary: "Pre-market CN morning brief: eight anchored slots, coverage self-checked."
description: "Pre-market A-share morning brief: five market slots plus three instrument slots, each anchored to a source and retrieval date; the header declares filled-over-total and reconciles it against the slot table; gaps named both ways; judgement stays human. Triggers: 晨会纪要 / 盘前早报 / 隔夜要闻 / 盘前数据槽 / 解禁与披露"
version: "0.1.3"
license: MIT
consumes:
  - parsed-doc
inputs:
  - company-list
  - announcement-doc
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
        desc: "Optional credential: without it this skill follows the user-supplied and degraded path described on the face; with it, the channel-side overnight disclosure originals and attachment parsing are available."
tags: [晨会纪要, 盘前早报, 隔夜要闻, 数据槽, 覆盖率]
---

# Pre-market Brief · Data Slots and Coverage

Compress **one time point** (overnight / pre-market) into an eight-slot brief: every slot carries a source and a
retrieval date, the header declares "filled / total", **every missing slot is named**, and every judgement stays `[待人工]`.

**Cut line**: this skill is the **time-point-driven** morning brief. `announcement-daily-cn` is a per-announcement list for one company;
`cn-research-brief` is a question-driven multi-source research brief; `watchlist-digest-cn` is an incremental digest for a self-kept list;
`event-brief-cn` is an event brief of a single announcement. This skill does not read announcements one by one — it takes only the
**overnight announcement titles of the covered instruments**.

## 0. What it is / what it is not

| Is | Is not |
|---|---|
| A one-page brief driven by a time point (overnight / pre-market) | An event-driven topical study (that is `cn-research-brief`) |
| Five market slots plus three instrument slots, eight in total | An announcement-by-announcement list of a basket (that is `announcement-daily-cn`) |
| Every slot carrying a source and a retrieval date | A remark with a conclusion but no provenance |
| A header declaring "filled / total = N/M" reconciled row by row against the slot table | A coverage figure written by feel, not countable from the table |
| Every missing slot named, with what is missing | Writing a missing slot as "not applicable / no such item / no disclosure needed" |
| Every judgement left as `[待人工]`, not one character filled in | Direction calls, buy/sell advice, ratings or target prices |

## 1. When to use

- The user wants one page of "what happened overnight, what to watch today" before the open.
- The user supplies a covered-instrument list (company names or 6-digit codes) and asks "did any of these file overnight".
- The user asks "what were overseas markets, FX, rates and margin balances yesterday", and expects each to trace to a source.
- The user wants a brief that can be re-run daily and whose prev-day gaps stay visible.

## 2. Data discipline

1. **Pin the time point first**: the header states `YYYY-MM-DD` and `隔夜` or `盘前`. One brief serves one time point; split across two.
2. **Eight slots, fixed**: market layer `隔夜外盘`, `汇率与商品`, `利率与流动性`, `指数与成交`, `两融余额`; instrument layer
   `标的隔夜公告标题`, `标的今日事件`, `今日披露与解禁`. The slot name is the contract name — renaming it is a shape violation.
3. **One row per slot, self-contained**: status is only `已填` or `未取到`; a filled row must carry the value or sentence, the source and the retrieval date.
4. **Coverage is counted, not guessed**: `已填槽/总槽 = N/M（xx%）` appears exactly once; `N` must equal the number of `已填` rows,
   `M` must equal eight, and the percentage must equal `N/M` rounded half-up. **A reported number must trace back to the table; it may not be assembled.**
5. **Gaps named in both directions**: `未取到槽：` appears exactly once, and the set of slots it lists must **equal** the `未取到` rows.
   Over-declaring is inflation, under-declaring is omission — both fire. Zero gaps is written `未取到槽：无`.
6. **Announcements to title level only**: copy the **title verbatim** inside the quotation marks — no summarising, no interpreting, no impact calls.
7. **Judgement goes to a human**: market strength, sector rotation, policy impact, catalyst realisation, risk size — all `[待人工]`.
   A `[待人工]` marker exempts only **its own clause**; the rest of the same line is still judged.
8. **Never write "not applicable"**: writing "no such item / not applicable / no disclosure needed" instead of "not obtained" concludes on the data source's behalf.

## 3. Output contract (header + five sections)

```
## 一、头部申报与槽表
- 文件：<YYYY-MM-DD> <隔夜|盘前>｜覆盖标的：<N> 只｜来路：渠道原文／用户直供
- 已填槽/总槽 = 6/8（75%）
- 未取到槽：<slot names, 、-separated, or 无>

| # | 槽 | 层 | 状态 | 值或原句 | 来源 | 检索日 |
|---|---|---|---|---|---|---|
| ① | 隔夜外盘 | 市场层 | 已填 | <values> | <source> | <YYYY-MM-DD> |
| ② | 汇率与商品 | 市场层 | 已填 | <values> | <source> | <YYYY-MM-DD> |
| ③ | 利率与流动性 | 市场层 | 未取到 | — | — | <YYYY-MM-DD> |
| ④ | 指数与成交 | 市场层 | 已填 | <values> | <source> | <YYYY-MM-DD> |
| ⑤ | 两融余额 | 市场层 | 未取到 | — | — | <YYYY-MM-DD> |
| ⑥ | 标的隔夜公告标题 | 标的层 | 已填 | <titles> | <source> | <YYYY-MM-DD> |
| ⑦ | 标的今日事件 | 标的层 | 已填 | <events> | <source> | <YYYY-MM-DD> |
| ⑧ | 今日披露与解禁 | 标的层 | 已填 | <items> | <source> | <YYYY-MM-DD> |

## 二、市场综述
- <fact> 锚：<source>｜检索日 <YYYY-MM-DD>
- [待人工] <every judgement, untouched>

## 三、标的动态
- <instrument>｜「<title verbatim>」 锚：<source>｜检索日 <YYYY-MM-DD>

## 四、政策行业
- [待人工] <policy and industry reads, untouched>

## 五、催化剂
- <instrument>｜<event> 锚：<source>｜检索日 <YYYY-MM-DD>
- [待人工] <whether the catalyst lands, untouched>

## 六、风险提示
- [待人工] <risk size and whether to avoid, untouched>

## 七、未取到清单
- 未取到 N 槽：<slot>（<what is missing>）…

## 八、待人工
- [待人工] <direction, advice, ratings — all human>
```

## 4. Data channel (live catalog values govern)

Real tasks take the channel path: read the catalog first, then fetch originals and attachment text.

```bash
# 1) read the catalog, get the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) MCP handshake, confirm the tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Once the endpoint is known, fetch by the tool names the catalog currently reports, hand announcement URLs or local paths to the channel,
poll the status, then read the body and tables.

**Degraded path with no key**: without `CUE_API_KEY` this skill uses only the title list and local files the user supplies; the cost is that it cannot reach
channel-side disclosure originals or attachment parsing, anchors can only land on the copy the user gave, and the overnight titles of covered instruments may be incomplete.

## 5. Compliance red lines (ships with the suite)

- No direction or price prediction (expected to rise, expected to fall, likely to rise, will rise, bullish, bearish, gap up, gap down, spike).
- No buy/sell advice (buy, sell, add, trim, open, close, recommended buy).
- No ratings or target prices (target price, rating, buy rating, overweight rating, strong recommendation).
- No return promises (guaranteed profit, must rise, must fall, zero risk, sure win).
- No drafting, no computing, no order placing, no acting on the user's behalf.
- Never write "not applicable / no such item / no disclosure needed" for "not obtained".
- No summarising or interpreting announcement bodies — title level only; full-text reading belongs to `event-brief-cn`.

## 6. Quick flow (user view)

1. Give one time point (overnight / pre-market) and a covered-instrument list (names or 6-digit codes).
2. The skill fetches slot by slot, each anchored to a source and retrieval date.
3. The header declares "filled / total", and every gap is named.
4. Every judgement stays `[待人工]`; this skill does not take it.

## 7. Machine checks

```bash
python3 -B scripts/check_morning.py <brief.md>     # five codes, PASS when clean
python3 -B scripts/check_morning.py --selftest     # good sample passes, five bad samples each fire their own code
bash scripts/fixtures/run_fixtures.sh              # three tiers, offline, no billing
```

Five codes: `MB-STRUCT` eight sections present and five of them ordered, the slot table holding eight contract slots with no duplicate or gap /
`MB-COVER` the coverage declaration reconciled against the slot table, percentage not self-assembled /
`MB-ANCHOR` every slot and every fact row anchored to a source and retrieval date, judgement positions marked `[待人工]` /
`MB-GAP` gaps named in both directions and "not applicable" banned /
`MB-LINE` three red-line families (direction calls, advice plus ratings and target prices, judgement tone outside judgement clauses).

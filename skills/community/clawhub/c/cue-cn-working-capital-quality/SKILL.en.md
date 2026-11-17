---
name: cn-working-capital-quality
slug: cue-cn-working-capital-quality
displayName: "存货与应收账款质量·逐条挂源"
summary: "Working-capital quality: inventory, receivables, contract assets, anchored."
description: "Working-capital quality: inventory, receivables, contract assets, each anchored to the filing's sentence. Turnover, growth and ratios not stated are tagged self-computed with numerator and denominator; book value never balance minus provision. Triggers: 存货质量 / 应收账款 / 合同资产 / 账龄结构 / 坏账准备 / 存货跌价准备"
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
        desc: "Optional credential. Without it the card works only from filings the user supplies, so anchors land on that copy alone; with it the channel can fetch periodic reports and their notes."
tags: [working-capital, inventory, receivables, contract-assets, ageing, source-anchored]
---

# Inventory and Receivables Quality · Every Item Anchored

`cn-earnings-note` answers "does the profit look good"; this package answers **"is the profit real"** —
the same user's next question. It lays out inventory, receivables and contract assets item by item,
each number anchored to the filing's own sentence.

**Load-bearing line**: every turnover day count, growth rate and share **must trace to a sentence in
the filing**. When the sentence does not state it and it still must be written, tag it 〔self-computed〕
and name which sentence the numerator and denominator each came from. **Never divide two numbers to
invent a third.**

**Dividing line**: this package covers only inventory, receivables and contract assets. Number-by-number
commentary on a published report belongs to `cn-earnings-note`; goodwill impairment belongs to
`cn-goodwill-impairment-risk`; receivable factoring and ABS derecognition belong to
`cn-restructuring-tracker`.

## 0. What it is / what it is not

| Is | Is not |
|---|---|
| Balances, ageing and provisions of the three asset blocks, each anchored to its own sentence | One "operating quality is fine / doubtful" overview paragraph |
| Turnover, growth and ratios **only as disclosed** | Revenue over average receivables, or this period minus last period |
| Self-computed numbers **listed separately with their sources** | Computed and disclosed numbers mixed in one column so readers cannot tell which was invented |
| "Provision" and "balance" are **two numbers**, on two rows | Balance minus provision to produce book value |
| "Not obtained" when the filing is silent | Filling gaps from common sense, industry averages, or inference |

## 1. When it fires

- The user has an annual, quarterly or interim report and asks whether inventory and receivables are bloated.
- The user asks for receivable turnover days, the ageing distribution, or whether bad-debt provisions suffice.
- The user asks how much inventory impairment was charged this period and how much remains at period end.
- The user wants the three blocks' balance movement and provision rhythm laid out as an anchored card.

## 2. Sourcing discipline

1. **Only the filing's own text**: each number must trace to a sentence plus an anchor (`[S#]`).
   Broker notes, news and market-data terminals are never sources.
2. **Quotation first**: quote the sentence when the sentence carries the number. Only when it does not,
   fall to rule 3.
3. **Self-computed goes on its own row**: turnover days, turnover ratios, growth rates, ratios and
   ageing shares that the filing does not state **must** be tagged 〔self-computed〕 with
   `numerator: <which sentence> [S#] | denominator: <which sentence> [S#]`. Either side missing fires.
   **Computed and disclosed numbers are never mixed**: once tagged, a reader can tell this is the
   package's arithmetic, not the filing's.
4. **Three things never computed by subtraction** (the red lines of this package):
   - Receivable "bad-debt provision" and "gross balance" are two numbers — **never derive book value
     as balance minus provision**, unless the same sentence in the filing states book value.
   - Inventory impairment "charged this period" and "closing balance" are two numbers; same rule.
   - When the ageing table discloses amounts but no shares, **shares are not computed**; writing them
     requires the 〔self-computed〕 tag plus numerator and denominator.
5. **State the basis**: which period the growth compares to, whether turnover days use 360 or 365, and
   whether the balance is period-end or average. Copy what the sentence says; what it does not say goes
   into the basis line as "not disclosed".
6. **Not-obtained named in both directions**: the header's "N items, M not obtained" appears once;
   N must equal the actual item rows and M the rows marked not obtained. Over-reporting is inflation,
   under-reporting is omission; both fire. A zero gap must be written explicitly as "none".
7. **Never write "not applicable"**: turning "not obtained" into "not applicable / no such item /
   not required to disclose" answers for the filing instead of registering it.
8. **Judgment stays human**: whether quality is good, whether something is abnormal, whether there is
   fraud, and whether a blow-up follows all go to `[待人工]`.

## 3. Output contract (five sections)

```
# 存货与应收质量卡·<YYYY-MM-DD>

## 一、存货

- 存货账面余额：「<sentence>」 锚：<locator> [S1]
- 存货跌价准备期末余额：「<sentence>」 锚：<locator> [S1]
- 本期计提跌价准备：「<sentence>」 锚：<locator> [S1]
- 存货周转天数：「<sentence with days>」 锚：<locator> [S1]
- 存货同比增速：「<sentence with percentage>」 锚：<locator> [S1]

## 二、应收账款

- 应收账款账面余额：「<sentence>」 锚：<locator> [S1]
- 坏账准备期末余额：「<sentence>」 锚：<locator> [S1]
- 本期计提坏账准备：「<sentence>」 锚：<locator> [S1]
- 应收账款周转天数：「<sentence with days>」 锚：<locator> [S1]
- 账龄结构（1 年以内）：「<sentence with amount and share>」 锚：<locator> [S2]

## 三、合同资产

- 合同资产账面价值：「<sentence>」 锚：<locator> [S1]
- 合同资产周转天数：未取到（未取到清单已点名）

## 四、计提与转回

- 本期计提合计：「<sentence>」 锚：<locator> [S1]
- 本期转回或收回：「<sentence>」 锚：<locator> [S1]

## 五、口径与未取到

- 共 15 项·未取到 1 项
- 未取到 1 项：<which item>——<what is missing>, check back against <which document>.
- 口径：<basis lines>
```

Self-computed row shape, when the sentence does not carry the number:

```
- 存货周转天数：〔自算〕 182.5 天
  分子：营业成本「本期营业成本 1,825,000,000 元」 [S1]｜分母：平均存货「期末存货 980,000,000 元、期初 850,000,000 元」 [S1]｜口径：360 天基准，本件自算未经验证
```

## 4. Data channel (the live catalog is authoritative)

Real tasks take the channel path: read the catalog first, then fetch periodic reports and notes.

```bash
# 1) read the catalog for the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) complete the MCP handshake and confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With `parse` / `get_parse_status` / `read_result` confirmed: hand the report URL or local path to
`parse`, poll with `get_parse_status`, pull text and note tables with `read_result`.

**Zero-channel fallback**: without a channel, first run
`scripts/make_outline.py --sources <manifest.jsonl> --out <skeleton.md>` to lay the materials you
already hold into the five-section skeleton and its fill-in slots, then fill sentences and anchors row
by row. Each manifest line requires `title` / `url` / `asof`. The cost: the skeleton has shape and no
facts, and **failing the machine check is by design** — do not deliver it as a finished card.

**Zero-key fallback**: without `CUE_API_KEY` the card works only from reports the user supplies or
local files. The cost is that channel-side note-table parsing is unavailable, anchors land on the copy
the user handed over, and cross-period or cross-table checks cannot be done.

## 5. Compliance red lines (ships with the suite)

- No fraud calls (fraud, inflation of revenue, accounting fraud, window-dressing).
- No blow-up or earnings-collapse calls (blow-up, collapse, will take a large impairment, material risk).
- No forecasts (expected, will, poised to, about to, in the second half).
- No ratings or target prices (target price, rating, buy rating, accumulate rating, strong recommendation,
  recommends buying or selling).
- No "worth watching" / "pay attention to".
- No return promises; no drafting conclusions, no computing conclusions on the user's behalf, no agency.
- No rulings on whether accounting treatment is compliant.

## 6. Quick flow (user's view)

1. Hand over the annual / quarterly / interim report (URL or local file, several allowed).
2. Without a channel, run `make_outline.py` first; with a channel, pull text and notes directly.
3. Register balances, ageing and provisions for the three blocks, each anchored to its own sentence;
   numbers the sentence does not carry get 〔self-computed〕 plus numerator and denominator.
4. What the filing omits goes to "not obtained" naming the document and section to check; judgment
   questions all go to `[待人工]`.

## 7. Machine checks

```bash
python3 -B scripts/check_working_capital.py <card.md>      # five codes fire per item; PASS when clean
python3 -B scripts/check_working_capital.py --selftest     # good passes, five bads each fire their own code
bash scripts/fixtures/run_fixtures.sh                      # three offline tiers (no network, no billing)
```

Five codes:
`WC-STRUCT` five sections present and ordered, each with items, declared counts aligned both ways /
`WC-ANCHOR` sentence non-empty, anchor value non-empty, `[S#]` present and resolvable, source rows carry
URL and retrieval date / `WC-NOSELF` turnover, growth, ratios, ageing shares and book value: when the
sentence does not state it, a 〔self-computed〕 tag with numerator and denominator is required, and two
numbers are never subtracted from each other / `WC-GAP` gaps named both ways, a zero gap written
explicitly as "none", "not applicable" banned / `WC-LINE` four red-line classes.

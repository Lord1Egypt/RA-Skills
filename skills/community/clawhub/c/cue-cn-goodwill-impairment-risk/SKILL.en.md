---
name: cn-goodwill-impairment-risk
slug: cue-cn-goodwill-impairment-risk
displayName: "Goodwill Impairment Risk Ledger"
summary: "Extract goodwill items into an eight-section ledger, each traced to its source."
description: "An A-share goodwill ledger: balance, target, earn-out completion, impairment-test assumptions, provision. Each row anchored to a verbatim quote; figures taken only as disclosed, never derived. Five offline checks. Not for impairment calls or ratings."
version: 0.1.2
license: MIT
consumes: []
inputs:
  - announcement-doc
  - disclosure-file
produces:
  - structured-note
tags: [goodwill-impairment, goodwill-balance, earn-out-completion, impairment-test-assumptions, source-anchored]
---

# Goodwill Impairment Risk Ledger

Split the **goodwill line items** of an annual report / semi-annual report or an acquisition
announcement into an eight-section ledger: goodwill balance, acquired target, earn-out completion,
impairment-test key assumptions, provision and non-provision. Every row carries a verbatim 「」 quote
and an anchor.

**Cut line**: `cn-restructuring-tracker` records **restructuring events and consideration** (the
timeline of halt, plan, approval, completion, and how the consideration changed at each step); this
skill covers only **the goodwill line items** — carrying balance, acquired target, earn-out
completion, impairment-test key assumptions, provision and non-provision. `cn-earnings-note` does
**commentary on published results** (how revenue, profit, and margin moved, and why); this skill does
not comment on performance, it only anchors goodwill items to their source sentences.
**This skill does not judge whether impairment will occur, nor whether the provision is adequate.**

## 0. What it is / what it is not

| Is | Is not |
|---|---|
| A ledger of goodwill line items extracted from one disclosure | A commentary on the whole set of results |
| One amount / ratio per row, each with a 「」 quote and anchor | A ledger that computes the impairment amount by subtracting recoverable amount from balance |
| Earn-out completion as three cells: committed / achieved / completion rate | "Completion is on track" as a conclusion |
| Key impairment-test assumptions registered item by item (discount rate, growth rate, forecast period) | An assessment of whether those assumptions are reasonable |
| Items not disclosed written as "not found", named in both directions | "No impairment / not applicable" substituting for a disclosure conclusion |

## 1. Triggers

- The user has an annual or semi-annual report and asks "how much goodwill does this company carry, and how much was impaired this year".
- The user asks "did the acquired target meet its earn-out commitment, and at what completion rate".
- The user asks "what discount rate and growth rate did the impairment test use".
- The user asks "how has the goodwill balance moved over these two years, and which target dominates".

## 2. Sourcing discipline

1. **Only the disclosed text counts**: every amount, ratio, and date must trace back to a sentence
   and an anchor in an annual / semi-annual report or acquisition announcement. Research notes, news,
   forum reposts, and broker software breakdowns are never sources.
2. **The most important cell — amounts and ratios only as quoted**: the amount (万元 / 亿元 / 元) and
   ratio (%) on a row must appear **verbatim inside that row's own 「」 quote**. If the disclosure says
   「计提商誉减值准备 1,200.00 万元」, write `1,200.00 万元` — not `1,200 万元`, not `1200万元`, not
   `0.12 亿元`. **Never subtract recoverable amount from the goodwill balance to derive an impairment
   amount, and never divide the impairment amount by the balance to derive a provision ratio** — the
   denominator could be goodwill at cost, carrying value, or the asset-group basis; get one
   denominator wrong and every risk reading is wrong. If no ratio is disclosed, write "not found";
   that is an answer, not a failure.
3. **Earn-out completion in three cells**: committed, achieved, completion rate. When the disclosure
   gives only two, write "not found" in the third and list it in §6 — never divide achieved by
   committed to fill it in.
4. **Impairment-test key assumptions registered item by item**: forecast period, discount rate,
   growth rate — exactly as disclosed. Pre-tax and post-tax discount rates are two different things;
   do not mix them.
5. **Missing items named in both directions**: the "M not found" declared in §6 must equal the number
   of rows writing "not found" in the body. Over-declaring is inflation, under-declaring is omission;
   both are flagged.

## 3. Eight-section contract

| Section | Content | Hard requirement |
|---|---|---|
| 1. Header declaration | File and provenance, a `减值口径：` line, `共 N 项·未取到 M 项` | All three present verbatim |
| 2. Goodwill balance | Per-target closing balance, opening balance, basis | At least one row; write "not found" for a missing target |
| 3. Earn-out completion | Per-target commitment period, committed, achieved, completion rate, basis | At least one row; write "not found" when there is no earn-out |
| 4. Impairment-test key assumptions | Per-target forecast period, discount rate, growth rate | At least one row; write "not found" when not disclosed |
| 5. Provision and non-provision | Per-target provision this period, provision ratio, cumulative provision, carrying balance | At least one row; a non-provision must be supportable from the quote |
| 6. Not-found list | Each missing item named | Aligned both ways with the body |
| 7. Sources | One line each, with URL and `YYYY-MM-DD` retrieval date | Numbering matches `[S#]` in the body one-to-one |
| 8. For human review | Judgment slots left blank | At least one `[待人工]` line |

**Three header items**: the first line gives the file and its provenance; the second is
`减值口径：商誉科目（…；不判会不会减值）` — **this line is the boundary between this skill,
restructuring tracking, and results commentary**, and the checker reads it to decide the boundary;
the third is `共 N 项·未取到 M 项`, which **may appear exactly once in the whole document**.

## 4. Row shapes (four kinds; a missing element is a finding)

```
- 余额：标的：<target>｜期末余额：<N>万元｜期初余额：<N>万元｜口径：<basis> 「<verbatim quote>」 锚：<anchor> [S#]
- 承诺：标的：<target>｜承诺期：<period>｜承诺数：<N>万元｜实现数：<N>万元｜完成率：<N>%｜口径：<basis> 「<verbatim quote>」 锚：<anchor> [S#]
- 假设：标的：<target>｜预测期：<period>｜折现率：<N>%｜增长率：<N>% 「<verbatim quote>」 锚：<anchor> [S#]
- 计提：标的：<target>｜本次计提金额：<N>万元｜计提比例：<N>%｜累计计提：<N>万元｜账面余额：<N>万元 「<verbatim quote>」 锚：<anchor> [S#]
```

- **The leading word** (`- 余额：` / `- 承诺：` / `- 假设：` / `- 计提：`) is the row-level presence
  test: mentioning "goodwill balance 12,500万元" in prose is not a row.
- **Inside 「」 is the quote**, copied verbatim from the disclosure; after `锚：` is a locator
  (section, note number, page) and it may not be empty.
- **`[S#]` goes at the end of the row**, and the number must have a matching line in §7.
- For a row that cannot be filled, write `- <leading word>：未取到（未取到清单已点名）` — that shape is
  exempt from the quote/anchor requirement but counts toward M in §6 and is reconciled both ways.

## 5. The five checks

`python3 -B scripts/check_goodwill.py <ledger.md>`, zero network, standard library only.

| Code | Check | What it judges |
|---|---|---|
| `GW-STRUCT` | 1. Structure | Eight sections present; three header items present; `减值口径：` starts with 「商誉科目」; the four row kinds present at row level and each in its own section; each row's required cells complete (balance 4 / earn-out 6 / assumptions 4 / provision 5) |
| `GW-QUOTE` | 2. Quote & anchor | `「」` non-empty and longer than one character; `锚：` present and non-empty; `[S#]` resolves in §7; every §7 line carries a URL and `YYYY-MM-DD` |
| `GW-LINE` | 3. Red lines | Will it impair / is the provision adequate / ratings & price targets / price prediction / return promises / agency work — zero hits. `[待人工]` and disclaimers **only cover their own clause** (split on `;`, `。`, `,`), so an assertion later in the same line is still flagged |
| `GW-GAP` | 4. Missing & no self-calculation | ① `共 N 项·未取到 M 项` appears exactly once, N = total data rows across the four sections, M = rows writing "not found", both directions flagged; ② "no impairment / not applicable / no provision needed" substituting for the disclosure is flagged; ③ **every amount and percentage on a row must appear inside that row's own quote** — if not, it was self-calculated |
| `GW-BOUND` | 5. Boundary | A `减值口径：` written as restructuring / consideration / transaction gets pointed at `cn-restructuring-tracker`; written as results commentary it gets pointed at `cn-earnings-note`; out-of-scope rows such as `- 交易对价：` / `- 支付方式：` / `- 标的资产作价：` and `- 营业收入：` / `- 归母净利润：` are flagged the same way |

**The no-self-calculation basis, written into the skill to prevent later relaxation**: the test is
**verbatim presence**, not numeric equality. `1,200.00 万元` and `1200 万元` are numerically equal, but
the latter is a form the ledger processed. A unit change (万元 ↔ 亿元), a padded decimal, a stripped
thousands separator — all count as not in the quote. The reason: this skill sells exactly "this
number traces back to that sentence"; once conversion is allowed, "traces back" becomes "can be
computed", and those are two different things. The sibling test is `cn-share-pledge-tracker`'s
`SP-GAP` (ratios must not be self-calculated); this skill extends it to amounts as well as
percentages.

## 6. Boundaries and non-promises

- **Does not judge whether impairment will occur**: signs of impairment / may impair / will impair /
  heavy impairment pressure / goodwill overstated — all go to `[待人工]`;
- **Does not judge whether the provision is adequate**: adequate / insufficient / under-provided /
  should have provided but did not — all go to `[待人工]`;
- **Gives no ratings or price targets, predicts no share price**: buy/sell, target price, bullish or
  bearish, drag on the share price — all go to `[待人工]`;
- **No agency work**: does not compute impairment, does not perform accounting treatment, does not
  draft inquiry replies, does not file on the user's behalf;
- Restructuring events and consideration tracking go to `cn-restructuring-tracker`; commentary on
  published results goes to `cn-earnings-note`; term extraction from a single restructuring document
  goes to `ma-restructuring-terms-cn`;
- Not retrieved = write "not retrieved" as-is; never fill in from industry convention, and never write
  "no impairment / not applicable" as a substitute;
- Domain and tool names follow the live catalog; this skill lists no fixed set, promises no count, and
  makes no promise about whether a domain is open or how fresh a file is.

## 7. Channel (data leg and parsing leg)

The evidence legs are two optional helpers: `cue-data-mcp` (locating annual reports and acquisition
announcements) and `cue-omni-reader` (converting PDF / web pages into extractable text). The live
channel connection takes this documented path — the catalog entry is assigned exactly once here, and
the domain id and routing url are resolved at run time, never hard-coded:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<replace with a domain id from the list above>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("not found: that id is not in the current catalog")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "lookup failed: ROUTING_URL is empty" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

The three layers each prove something different, and they are not equivalent: **skill installed ≠
credentials configured ≠ channel connected**. An anonymous GET only proves the catalog is reachable;
a keyed connection whose `tools/list` returns proves that key is accepted (pass = HTTP 200 with a
non-empty `result.tools`, judged by shape only — no tool names listed, no count promised). The
parsing leg goes through the host MCP: once connected, the tools the host lists should include names
like `parse`, `get_parse_status`, `read_result` — their presence proves only that they are exposed,
not that parsing works. Domains absent from the catalog are neither installed nor promised;
connection errors do not mean a domain has no data — report them as-is. The key comes from local
credential facilities, is never echoed into chat or the terminal. Consumption is billed per the
server's response; ask before spending.

## 8. Artifact names

- `consumes: []` (**explicitly empty**, not omitted: this skill reads the annual report or
  announcement the user supplies and consumes no upstream artifact)
- `inputs: announcement-doc / disclosure-file` (registered input families, written into the package's
  `inputs:` key; they do not participate in edge counting)
- `produces: structured-note` (registered canonical)

No artifact name was added and `artifact-types.yaml` was not modified.

## 9. Resources

- `README.md`: Chinese surface (authoritative)
- `README.en.md`: English counterpart
- `CHANGELOG.md`: versions and changes
- `scripts/check_goodwill.py`: the five checks (zero network)
- `scripts/fixtures/run_fixtures.sh`: offline three-tier runner (zero network, zero billing)

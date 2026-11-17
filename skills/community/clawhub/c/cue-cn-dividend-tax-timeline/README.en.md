# Dividend Payout & Withholding Timeline

Turn a Chinese A-share equity distribution announcement into three dated nodes, then list the applicable tax rate, tax base and after-tax amount per shareholder class — every line carrying the announcement's own sentence and its anchor. Classes the announcement does not cover are written as "not obtained", one by one.

## 1. Three steps to start

1. Hand the equity distribution implementation announcement (URL or local file) to this skill.
2. It lays out record date → ex-rights/ex-dividend date → cash dividend payment date, and lists rate, tax base and after-tax amount for each of the five shareholder classes.
3. Classes the announcement does not cover go into the not-obtained list; every judgement question goes to "needs a human".

## 2. Five machine checks (offline)

```bash
python3 -B scripts/check_dividend_tax_timeline.py <card.md>     # five codes, PASS when clean
python3 -B scripts/check_dividend_tax_timeline.py --selftest    # good sample passes, bad samples fire
bash scripts/fixtures/run_fixtures.sh                           # three tiers, 30s, no network, no billing
```

| Code | What it checks |
|---|---|
| `DT-STRUCT` | Five sections present; the three date nodes present **line by line** and **in order** (record ≤ ex-rights ≤ payment); five shareholder classes present line by line; every non-missing row carries all three elements (rate · tax base · after-tax amount) |
| `DT-QUOTE` | The quoted sentence in each row must not be empty or a single character; an `锚：` label with an empty anchor value also fires |
| `DT-LINE` | Three red-line families: fixed banned phrases (market-timing advice / ratings and target prices / return promises / acting on the user's behalf / judging the tax burden) · subject word × judgement tone in one clause · self-adjudicating validity |
| `DT-GAP` | Two-way reconciliation of the not-obtained declaration (over-declaring is inflation, under-declaring is omission); "not applicable / no withholding needed" always fires; **the rate figure must appear in that row's own quoted sentence**, otherwise it is flagged as a default rate |
| `DT-BOUND` | A dividend-plan item line means the wrong skill was used — it names `cn-shareholder-return` instead |

## 3. Usage

```bash
# one card
python3 -B scripts/check_dividend_tax_timeline.py my-card.md

# selftest (run this after touching the checker)
python3 -B scripts/check_dividend_tax_timeline.py --selftest
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

- No market-timing advice (hold until the record date, buy before the record date, rights-grabbing, post-ex-rights rallies).
- No ratings or target prices.
- No return promises (guaranteed profit, zero risk, guaranteed yield, must rise, must fall).
- No drafting, no computing, no filing, no acting on the user's behalf.
- No judgement on whether the tax burden is high or low.
- No adjudication of validity (whether the withholding treatment is compliant or effective).
- No re-registering the dividend plan itself — that is `cn-shareholder-return`'s job.

## 6. When a check fires

| Symptom | Cause | Fix |
|---|---|---|
| `DT-STRUCT 缺段` | A section heading was renamed or omitted | Write the five headings exactly as in SKILL.md §3 |
| `DT-STRUCT 时间轴段内缺节点行` | A node is only mentioned in prose | Give each of the three nodes its own line starting with `- node name：` |
| `DT-STRUCT 日期节点次序错` | Ex-rights date earlier than the record date | Re-read the three dates in the announcement; do not order them from memory |
| `DT-STRUCT 原句里没有适用税率` | The quoted sentence carries no rate | If the announcement does not state it, write the whole row as "not obtained" — never fill in a default rate |
| `DT-QUOTE 书名号内原句为空` | Paraphrased or left blank | Copy the original sentence; do not paraphrase |
| `DT-GAP 申报未取到 N 类…` | Header declaration disagrees with the number of "not obtained" rows | Count the rows that say "not obtained" in the tax section |
| `DT-GAP 税率 … 不在本行原句里` | The rate is a statutory default, not what the announcement says | Delete the self-supplied rate; write "not obtained" if the announcement is silent |
| `DT-BOUND 出现分红方案速读的项行` | The card became a dividend-plan brief | Send the plan itself to `cn-shareholder-return`; this skill only does the timeline and the tax split |
| `DT-LINE 定式禁词` | Timing advice, a rating or a return promise was written | Delete it; register the original sentence or move it to "needs a human" |

## 7. How to ask (good and bad)

**Good**

- "For this equity distribution announcement, what are the record date, ex-rights date and payment date?"
- "How much tax is withheld, and what do individual holders and QFIIs actually receive?"
- "What rate applies to our class of shareholder — does the announcement say?"

**Bad**

- "Should I buy before the record date?" → no timing advice here; this skill only lays out the timeline.
- "Is this dividend worth it?" → no judgement on the tax burden; only the original sentences are registered.
- "Compute my tax and file it for me." → no computing, no filing.
- "How much per 10 shares, and what is the total?" → that is a dividend-plan brief; use `cn-shareholder-return`.

## 8. Honest capability limits

- A rate is only accepted when the percentage appears in **that row's own quoted sentence**. When the announcement says "withheld at the applicable rate" without a number, this skill records "not obtained" rather than looking up tax law for you.
- Shareholder classes are recognised by alias families; the table is `SH_ALIASES` in `scripts/check_dividend_tax_timeline.py`. A new spelling means adding an alias, not changing the criterion.
- Dates are recognised in three forms: `2026 年 6 月 12 日`, `2026-06-12`, `2026/6/12`. Relative wording such as "T day" or "the next trading day after the record date" fires "no date in the row" and needs a human to convert.
- The three-element check verifies that the **nouns are present**, not that the arithmetic is right; the relationship between the after-tax amount and the rate should be re-checked by a human.

## 9. Resources

- `SKILL.md` — authoritative face (Chinese)
- `SKILL.en.md` — English twin
- `references/dividend-tax-terms.md` — the five classes and three elements, aliases, cut line
- `scripts/check_dividend_tax_timeline.py` — the five-code checker
- `scripts/fixtures/` — one good sample, six bad samples, runner

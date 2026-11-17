# Pre-market Brief · Data Slots and Coverage

Compress **one time point** (overnight / pre-market) into a single page of eight slots: every slot carries a source and a retrieval date, the header declares "filled / total", every missing slot is named, and every judgement stays `[待人工]`.

## 1. Three steps to start

1. Give one time point (overnight / pre-market) and a covered-instrument list (company names or 6-digit codes).
2. The skill fetches eight slots: five market slots (overnight overseas · FX and commodities · rates and liquidity · index and turnover · margin balance) and three instrument slots (overnight filing titles · today's events · disclosures and lockup expiries).
3. Every slot carries a source and a retrieval date; the header declares "filled / total = N/M", `未取到槽：` names every gap, and every judgement stays `[待人工]`.

## 2. Five machine checks (offline)

```bash
python3 -B scripts/check_morning.py <brief.md>     # five codes, PASS when clean
python3 -B scripts/check_morning.py --selftest     # good sample passes, five bad samples each fire their own code
bash scripts/fixtures/run_fixtures.sh              # three tiers, 30s, no network, no billing
```

| Code | What it checks |
|---|---|
| `MB-STRUCT` | Eight sections present, five of them ordered; the slot table holds eight contract slots with **no duplicate and no gap**, slot names fixed; each row's status is only `已填` or `未取到`, and layer matches the slot |
| `MB-COVER` | `已填槽/总槽 = N/M（xx%）` appears exactly once, and **N equals the number of `已填` rows, M equals eight, xx equals N/M rounded half-up** — each of the three numbers must trace back to the slot table |
| `MB-ANCHOR` | A filled slot's value / source / retrieval-date cells may not be empty (`—` counts as empty); fact rows need `锚：` and a retrieval date; each of the four judgement sections needs `[待人工]` |
| `MB-GAP` | `未取到槽：` appears exactly once and the set of names must **equal** the rows marked missing (over-declaring is inflation, under-declaring is omission); "not applicable / no such item / no disclosure needed" always fires |
| `MB-LINE` | Three red-line families: direction calls plus buy/sell advice plus ratings and target prices / subject word × judgement tone in one clause / out-of-scope body reading (title level only) |

## 3. Usage

```bash
# one brief
python3 -B scripts/check_morning.py my-brief.md

# selftest (run this after touching the checker)
python3 -B scripts/check_morning.py --selftest
```

## 4. First-time Cue setup (three steps, optional)

1. Register at cuecue.cn and get a `CUE_API_KEY`.
2. Export it: `export CUE_API_KEY=...`.
3. Check connectivity:

```bash
# 1) read the catalog, get the endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) MCP handshake, confirm the tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**It also runs without the key**: with no key this skill uses only the title list and local files the user supplies; the cost is that it cannot reach channel-side disclosure originals or attachment parsing, anchors can only land on the copy the user gave, and the overnight titles of covered instruments may be incomplete.

## 5. Boundaries and non-promises

- No direction or price prediction (expected to rise, expected to fall, likely to rise, bullish, bearish, gap up, gap down, spike).
- No buy/sell advice (buy, sell, add, trim, open, close, recommended buy).
- No ratings or target prices (target price, buy rating, overweight rating, strong recommendation).
- No return promises (guaranteed profit, must rise, must fall, zero risk, sure win).
- No drafting, no computing, no order placing, no acting on the user's behalf.
- Never write "not applicable / no such item / no disclosure needed" for "not obtained".
- No quoting or interpreting announcement bodies — title level only.
- Not a per-announcement list for one company (that is `announcement-daily-cn`), not a question-driven research brief (`cn-research-brief`), not an incremental digest for a self-kept list (`watchlist-digest-cn`), not an event brief of a single announcement (`event-brief-cn`).

## 6. When a check fires

| Symptom | Cause | Fix |
|---|---|---|
| `MB-COVER 百分比 … 不符` | The percentage was guessed, not computed from N/M | Recompute as N/M rounded half-up |
| `MB-COVER 申报已填 N 槽，槽表实有 …` | The declaration and the table are out of step | Count the `已填` rows first, then write the declaration |
| `MB-GAP 漏报：…` | The table marks a slot missing but the declaration omits it | Add the slot to `未取到槽：`; zero gaps is written `无` |
| `MB-GAP 虚报：…` | The declaration lists a slot the table marks filled | Either fill the slot for real or set it to `未取到` |
| `MB-STRUCT 槽表缺槽：…` | One of the eight slots is missing | Eight slots are the contract; missing data is written `未取到`, never dropped |
| `MB-STRUCT 槽「…」应属 市场层/标的层` | The slot sits in the wrong layer | Five market slots, three instrument slots |
| `MB-ANCHOR 槽「…」已填但缺来源` | A value without a source | Add source and retrieval date, or set the status to `未取到` |
| `MB-ANCHOR …段缺 [待人工]` | A judgement section reads as factual narration | Judgement is always `[待人工]`, not one character filled in |
| `MB-LINE 定式禁词：…` | A direction call, advice line or target price | Delete it; register the sentence or move it under `[待人工]` |
| `MB-LINE 越界精读` | The announcement body was quoted | Copy titles only; body reading belongs to `event-brief-cn` |

## 7. How to ask (good and bad prompts)

**Good**

- "Give me one page before the open: overseas markets, FX, rates, index and turnover, margin balances."
- "Did any of these three names file overnight? Any meetings today?"
- "What disclosures and lockup expiries are due today?"
- "Which two slots were missing yesterday, and did we fill them today?"

**Bad**

- "Will the market rise today?" → this skill does not call direction; it registers facts.
- "Which of these should I buy?" → no buy/sell advice.
- "Read this quarterly report and tell me what it says." → that is a single-announcement brief; use `event-brief-cn`.
- "List every new announcement for the ten names I follow." → that is an incremental watchlist digest; use `watchlist-digest-cn`.

## 8. Honest limits

- Coverage checks that **the three numbers trace back to the slot table** (N = filled rows, M = eight, xx = N/M rounded half-up). It does not check that the values themselves are current — verify facts against the official originals.
- Anchors check that **a source and a retrieval date are present and the date is date-shaped**, not that the source is authoritative (a human verifies that).
- Retrieval dates accept `2026-11-09` and `2026 年 11 月 9 日`; odder spellings are flagged as not date-shaped.
- The subject-word × judgement-tone check is **deliberately narrow**: the tone words do **not** include 将 / 会 / 必, because this domain is full of factual lines such as "will disclose today" and "two names will unlock today"; including them would flood the check with false positives.
- A `[待人工]` marker exempts only **its own clause**; an assertion later in the same line still fires.
- Announcements are checked for **title presence only**, not whether the title matches the instruments you care about — verify instrument attribution by hand.

## 9. Artifact wiring (the two edges that connect)

- `consumes: parsed-doc` — takes the parsed overnight announcement titles and attachment text produced by `cue-omni-reader`;
  this is the real data leg. Without a key the leg is down, and the brief degrades to user-supplied input as described on the face.
- `produces: structured-note` — a registered canonical artifact name already consumed by `cn-customer-concentration` and `ic-memo-cn`,
  so this skill is not an isolated node. **It does not produce `daily-digest`**: that name is registered too, but nothing in the repo
  consumes it, so producing it would leave the out-degree at zero.

## 10. Resources

- `SKILL.md` — authoritative face (Chinese)
- `SKILL.en.md` — English counterpart
- `README.md` — Chinese guide
- `scripts/check_morning.py` — the five-code checker
- `scripts/fixtures/` — 1 good sample, 5 bad samples, a three-tier runner

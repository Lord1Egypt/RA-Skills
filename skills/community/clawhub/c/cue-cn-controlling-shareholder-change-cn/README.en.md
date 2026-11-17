# Control Change and Tender Offer · Every Item Anchored (cn-controlling-shareholder-change-cn)

Break **one control-change event** into eight items, each anchored to the filing's own sentence:
who transfers, who receives, how many shares, what percentage, how much money, and who holds control
before and after — **ratios and consideration only as disclosed**, never shares times price, never one
number divided by another.

A-share control change is the most expensive event class in the market: one agreement transfer can
replace the actual controller, one partial tender offer can rewrite the ownership structure. The
common ways coverage of this class goes wrong all land in the same place — **a number gets computed**:

- The filing gives shares but no ratio, so the card divides by share capital and picks the wrong
  denominator (total capital / capital net of treasury shares / voting-rights basis);
- The filing says "price to be agreed", so the card multiplies shares by a per-share price and prints
  an amount the filing never contained;
- A tender offer discloses the offer price but not the premium, so the card subtracts the market price
  and gets the basis wrong;
- A few of the eight items are missing, so the card fills them from common sense and the reader cannot
  tell which cell was inferred.

This package holds one line: **a number reported must trace back to evidence.** When it cannot, write
"not obtained".

## 1. Scope

| Covers | Does not cover |
|---|---|
| The **process** of control changing hands: who acquires, by what path, at what price | Registration of dividend/buyback/reduction results (`cn-shareholder-return`) |
| Six paths: agreement transfer / voting-rights delegation / open-market accumulation / tender offer (incl. partial) / judicial auction / inheritance | Merger-and-restructuring progress (suspension / draft / approval / implementation — `cn-restructuring-tracker`) |
| Eight items, each anchored to its own sentence | Pledge and release details (`cn-share-pledge-tracker`) |
| Ratios and consideration only as the filing states them | Multiplying shares by price, dividing two numbers for a ratio |
| Offer price and premium on separate rows | Subtracting the market price from the offer price to make a premium |
| "Not obtained" when the filing is silent | Filling gaps from common sense, quotes, or inference |

**Dividing line**: this package covers only the **process by which control changes hands**. Dividends,
buybacks and reductions are shareholder-action results and belong to `cn-shareholder-return`;
restructuring tracking covers transaction progress and belongs to `cn-restructuring-tracker`; pledges
are a security status and belong to `cn-share-pledge-tracker`. When a pledge happens to be one leg of
the change path, this package **cites** it but does not re-register it.

## 2. The eight items

1. **Change path** — one of the six paths, from the filing's own sentence.
2. **Transferor** — the sentence; include the shareholding when the sentence carries it.
3. **Transferee** — the sentence.
4. **Shares transferred** — the sentence.
5. **Percentage** — must appear inside that row's own quoted sentence; shares without a ratio means
   "not obtained".
6. **Consideration** — the amount must appear inside that row's own quoted sentence; "to be agreed"
   means "not obtained", never multiplied.
7. **Control holder before** — the sentence.
8. **Control holder after** — the sentence.

Items 7 and 8 are two rows because they are frequently two different names or entities; merged into
one, "who before, who after" stops being readable.

## 3. The tender-offer section

A tender path (including partial) gets its own section with two separate rows:

```
- 要约价：「本次要约价格为每股 12.00 元」 锚：报告书 第四节 一  [S1]
- 溢价率：「较前 30 个交易日均价 9.88 元溢价 21.40%」 锚：报告书 第四节 二  [S1]
```

Three rules:

- **Offer price and premium never share a row** — with two numbers on one line the reader cannot tell
  which price the premium was measured against.
- **The premium percentage must be inside that row's own sentence.** A filing that says "at a premium"
  without a figure means "not obtained"; never subtract it out.
- **The premium sentence must carry its basis** (30-day average / prior-day average / pre-suspension
  price / benchmark price). A sentence reading "premium 21.40%" with no basis cannot be re-checked and
  fires.

Non-tender path writes one line: `- 本笔不涉及要约收购，无要约价与溢价率。`

## 4. The five machine checks

```
CC-STRUCT  six sections present · eight items at row level · declared counts aligned both ways
CC-QUOTE   sentence non-empty · anchor value non-empty (a bare [S1] counts as empty) · [S#] resolvable
CC-CALC    no self-computation: ratio and consideration in the row's own sentence; premium never
           subtracted out, never on the same row as the offer price
CC-LINE    three red-line classes: bull/bear calls · guessing the next move · ratings/target prices
CC-BOUND   names the sibling package when the card drifts into shareholder returns, restructuring
           progress, or pledge details
```

`CC-STRUCT`'s two-way alignment: the header "8 items, N not obtained" appears once, `8` must equal the
actual item rows in the detail section, and `N` must equal the rows marked "not obtained" —
over-reporting is inflation, under-reporting is omission, both fire.

`CC-CALC` is the load-bearing check and judges four things:

1. The percentage on the `变动比例` row is not inside that row's quoted sentence → fire (computed ratio);
2. The amount on the `交易对价` row is not inside that row's quoted sentence → fire (computed amount);
3. `要约价` and `溢价率` appear on the same row → fire (separate rows are the only registered form);
4. The premium percentage sits outside its sentence, or the sentence lacks a basis phrase → fire
   (computed premium / unreviewable).

## 5. Data channel

Real tasks take the channel path: read the catalog first, then fetch filing text and attachments.

```bash
# 1) read the catalog for the MCP endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) complete the MCP handshake and confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With `parse` / `get_parse_status` / `read_result` confirmed: hand the filing URL or local path to
`parse`, poll with `get_parse_status`, pull text and tables with `read_result`.

**Zero-key fallback**: without `CUE_API_KEY` the card works only from filings the user supplies
directly or from local files. The cost is that channel-side filing text and attachment parsing are
unavailable, anchors can only point at the copy the user handed over, and cross-document checks cannot
be done.

## 6. Running it

```bash
# check one card
python3 -B scripts/check_control_change.py card.md

# selftest: the good sample passes, each of five bads fires only its own code
python3 -B scripts/check_control_change.py --selftest

# three offline tiers (no network, no billing, under 30 seconds)
bash scripts/fixtures/run_fixtures.sh
```

Exit codes: `0` clean; `1` findings; `2` usage error; `3` unreadable file or empty draft.

## 7. Fixtures

`scripts/fixtures/` holds one good sample plus five bads, each firing **only** its own code:

| File | Expected | What it breaks |
|---|---|---|
| `good-control-change.md` | rc=0 | eight items, one not obtained, non-tender path |
| `bad-1-struct.md` | CC-STRUCT | the detail section drops "control holder after" |
| `bad-2-quote.md` | CC-QUOTE | empty sentence + anchor reduced to a bare `[S1]` |
| `bad-3-calc.md` | CC-CALC | percentage 15.00% computed outside the sentence |
| `bad-4-line.md` | CC-LINE | major positive / will inject / target price |
| `bad-5-bound.md` | CC-BOUND | a dividend item line smuggled into the not-obtained list |

`run_fixtures.sh` runs three tiers: ① selftest; ② samples (good rc=0, each bad firing only its code);
③ eleven boundary shapes as **positive/negative contrast** — whole-line replacement on the good sample,
so what should fire does fire and what should not does not (a genuine tender offer with all three
pieces, an amount inside the sentence, the character 会 inside a body name not misfiring, a fully blank
`[待人工]` line) — plus `empty` and `nofile` expecting rc=3.

## 8. Red lines (ships with the suite)

No bull/bear calls; no guessing the new controller's next move; no price forecasts; no ratings or
target prices; no return promises; no drafting, computing, filing or acting as agent; no validity
rulings (whether the change is effective, non-compliant, or constitutes a control change).

Judgment questions all go to `[待人工]` — this package does not take errands and does not give direction.

## 9. Artifact wiring

- `consumes: [parsed-doc]` — eats the equity-change and tender-offer filing text and tables parsed by
  omni-reader.
- `inputs: [announcement-doc, disclosure-file]` — raw filing and disclosure entries.
- `produces: [structured-note]` — registered, and it already has downstream consumers.

**Why not `change-brief`**: the name exists in the `structured-note` family, but the whole repo has
3 producers and **0 consumers** for it, so declaring it would leave this package with zero out-degree
and land it in the orphan table. A registered alias is not a consumed name — edges come only from a
name that has both a producer and a consumer.

## 10. Known limits

- `CC-CALC` judges "the number traces to this row's sentence", not whether the disclosed number is true
  (the fact layer goes back to the filing).
- Ratios are taken as disclosed, not re-based: "15.00% of total share capital" is registered as written,
  the denominator is not re-checked.
- The premium check judges "the percentage is inside the sentence and the sentence names a basis", not
  whether the basis price itself was selected correctly.
- `CC-QUOTE` judges that the source reference resolves in the index, not that the source is authoritative.
- Item-level presence is checked, not whether this filing is the right one for that issuer and date.

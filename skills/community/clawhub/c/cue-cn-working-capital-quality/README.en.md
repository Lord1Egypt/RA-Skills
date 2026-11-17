# Inventory and Receivables Quality · Every Item Anchored (cn-working-capital-quality)

`cn-earnings-note` answers "does the profit look good"; this package answers **"is the profit real"** —
the same user's next question.

It lays inventory, receivables and contract assets out item by item — **balances, ageing, provisions** —
each number anchored to the filing's own sentence. **Every turnover day count, growth rate and share
must trace to a sentence in the filing.** When the sentence does not state it and it still must be
written, tag it 〔self-computed〕 and name which sentence the numerator and denominator each came from.
**Never divide two numbers to invent a third, and never subtract two numbers to invent a third.**

## 1. Scope

| Covers | Does not cover |
|---|---|
| Balances, ageing and provisions of the three blocks, each anchored | One "operating quality is fine / doubtful" overview |
| Turnover, growth and ratios only as disclosed | Revenue over average receivables, this period minus last period |
| Self-computed numbers on their own line with sources named | Computed and disclosed numbers mixed in one column |
| "Provision" and "balance" on two separate rows | Balance minus provision to produce book value |
| "Not obtained" when the filing is silent | Filling gaps from common sense, industry averages, or inference |

**Dividing line**: this package covers only inventory, receivables and contract assets. Number-by-number
commentary on a published report belongs to `cn-earnings-note`; goodwill impairment belongs to
`cn-goodwill-impairment-risk`; receivable factoring and ABS derecognition belong to
`cn-restructuring-tracker`.

## 2. Three subtractions never performed (this package's red lines)

These three are the reason this package exists. Each looks like school arithmetic, and each has a trap
in the filing:

1. **Book value ≠ balance − bad-debt provision.** A note may give the gross balance, the provision and
   the book value as three independent numbers; your subtraction may miss write-offs or mix bases
   (consolidated vs parent, period-end vs average). **Unless the same sentence states book value**,
   copy two rows and never merge them into one number.
2. **Impairment "charged this period" ≠ "closing balance".** The closing balance is cumulative; the
   charge is a flow; reversals, write-offs and FX sit between them. Deriving one from the other yields
   false conclusions like "provisions surged this period".
3. **When the ageing table gives amounts but no shares, shares are not computed.** The denominator may
   be the gross balance or the balance net of specific provisions; pick the wrong one and the whole
   ageing risk picture is wrong.

## 3. The five machine checks

```
WC-STRUCT  five sections present and ordered · each with items · declared counts aligned both ways
WC-ANCHOR  sentence non-empty · anchor value non-empty (a bare [S1] counts as empty) · [S#] resolvable ·
           source rows carry URL and retrieval date
WC-NOSELF  turnover / growth / ratios / ageing shares / book value: when the sentence does not state it,
           a 〔self-computed〕 tag with numerator and denominator is required; two numbers never subtracted
WC-GAP     gaps named both ways · a zero gap written explicitly as "none" · "not applicable" banned
WC-LINE    four red-line classes: fraud and blow-up · forecasts · ratings and target prices · worth watching
```

`WC-NOSELF` is the load-bearing check and judges two things:

- **Where a number came from.** When the sentence does not carry it (a percentage, a day count), it must
  be tagged 〔self-computed〕 with `numerator: <which sentence> [S#] | denominator: <which sentence> [S#]`.
  Either side missing fires. A tag with only the numerator fires too — half the provenance leaves the
  reader unable to re-check.
- **Two numbers never subtracted.** `book value = balance − provision` fires unless the sentence itself
  states book value.

**One line, one code.** A line with neither a sentence nor a 〔self-computed〕 tag is "computed but not
tagged" (`WC-NOSELF`), not "empty sentence" (`WC-ANCHOR`); a line reading "not applicable" belongs to
`WC-GAP`. Each code owns its own lines so one defect is not reported twice — two findings make a fixer
think two things are wrong.

## 4. Data channel

Real tasks take the channel path: read the catalog first, then fetch report text and note tables.

```bash
# 1) read the catalog for the MCP endpoint
curl -s https://cuecue.cn/api/mcp-catalog | head -c 500

# 2) complete the MCP handshake and confirm the three tools are present
curl -s -X POST "$MCP_ENDPOINT" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With `parse` / `get_parse_status` / `read_result` confirmed: hand the report URL or local path to
`parse`, poll with `get_parse_status`, pull text and note tables with `read_result`.

**Zero-channel fallback**: lay the skeleton first, then fill row by row.

```bash
python3 -B scripts/make_outline.py --sources manifest.jsonl --out skeleton.md --subject 示例股份
```

Each manifest line requires `title` / `url` / `asof` (retrieval date, `YYYY-MM-DD`); `id` is optional and
defaults to `S1`, `S2`… by line order. Bad lines (invalid JSON, missing key, malformed date) are
**named line by line, never silently skipped**; with no usable line the script exits 1 — an empty
manifest does not produce a skeleton. **Failing the machine check is by design**: placeholder rows fire,
reminding you to finish before delivering, so an empty shell cannot pass as a finished card.

**Zero-key fallback**: without `CUE_API_KEY` the card works only from reports the user supplies or local
files. The cost is that channel-side note-table parsing is unavailable, anchors land on the copy the
user handed over, and cross-period or cross-table checks cannot be done.

## 5. Running it

```bash
# check one card
python3 -B scripts/check_working_capital.py card.md

# selftest: the good sample passes, each of five bads fires only its own code
python3 -B scripts/check_working_capital.py --selftest

# three offline tiers (no network, no billing, under 30 seconds)
bash scripts/fixtures/run_fixtures.sh
```

Exit codes: `0` clean; `1` findings; `2` usage error; `3` unreadable file or empty draft.

## 6. Fixtures

`scripts/fixtures/` holds one good sample plus five bads, each firing **only** its own code:

| File | Expected | What it breaks |
|---|---|---|
| `good-working-capital.md` | rc=0 | 15 items, 1 not obtained, all three blocks |
| `bad-1-struct.md` | WC-STRUCT | section five retitled from "口径与未取到" to "口径" |
| `bad-2-anchor.md` | WC-ANCHOR | empty sentence + anchor reduced to a bare `[S1]` |
| `bad-3-noself.md` | WC-NOSELF | bare turnover days, untagged ageing share, self-subtracted book value |
| `bad-4-gap.md` | WC-GAP | "not applicable" + declared gap count above the body |
| `bad-5-line.md` | WC-LINE | large impairment / fraud / target price |

`run_fixtures.sh` runs three tiers: ① selftest; ② samples (good rc=0, each bad firing only its code);
③ thirteen boundary shapes as **positive/negative contrast** — whole-line replacement on the good sample,
so what should fire does fire and what should not does not (a properly documented self-computation, book
value inside the sentence, an ageing row with shares, the word "investment advice" inside a disclaimer
not misfiring, a factual "up on the same period last year" not misfiring, a zero gap written as "none")
— plus `empty` and `nofile` expecting rc=3.

## 7. Red lines (ships with the suite)

No fraud calls; no blow-up or earnings-collapse calls; no forecasts; no ratings or target prices; no
"worth watching"; no return promises; no drafting or computing conclusions on the user's behalf, no
agency; no rulings on whether accounting treatment is compliant.

Judgment questions all go to `[待人工]`.

## 8. Artifact wiring

- `consumes: [parsed-doc]` — eats periodic report text and note tables parsed by omni-reader.
- `inputs: [announcement-doc, disclosure-file]` — raw filing and disclosure entries.
- `produces: [structured-note]` — registered, with downstream consumers.

This package **does not produce** `change-brief` (zero consumers repo-wide). It also does not register
dividends, buybacks, reductions, restructuring progress, goodwill or pledge details — each has its own
package.

## 9. Known limits

- `WC-NOSELF` judges "the number traces to this row's sentence, or is tagged 〔self-computed〕 with
  numerator and denominator" — **not whether those two source numbers are themselves correct**.
- When the filing omits the turnover basis (360 / 365), this package does not pick one; it names
  "not disclosed" in the basis line.
- Ageing is copied as disclosed and not re-based; when both consolidated and parent statements exist,
  the primary disclosed statement governs and the choice is noted.
- `WC-ANCHOR` judges that the source reference resolves in the index, not that the source is authoritative.
- `WC-GAP` judges that gaps align both ways, not that the "not obtained" item truly cannot be obtained.

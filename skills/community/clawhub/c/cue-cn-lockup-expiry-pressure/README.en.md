# Lockup Expiry Pressure — every row sourced

For one stock, chain its **upcoming** lockup expiries into a dated calendar: expiry date, holder type, shares released, share of total capital, cost band — each row carries its original announcement anchor and retrieval date. Anything the announcement omits is named as missing.

**No price calls, no buy-sell advice, no ratings, no target prices.** Judgment slots are always `[待人工]` — hand it to a human.

---

## 1. Start here: three steps

1. **Fix the base date**, then collect this stock's restricted-share source material: prospectus, placement result announcement, equity-incentive grant announcement, restricted-share listing announcement.
2. **Copy four things from each document**: expiry date, holder type, shares released, share of total capital (copy the denominator with it) — plus the cost price, the link and the retrieval date.
3. **Run the self-check**, fix one red at a time:

```bash
python3 scripts/check_lockup.py your-draft.md
```

Exit code `0` clean, `1` findings, `3` unreadable file.

---

## 2. What the five lanes judge

| Code | Lane | Judges | Most often catches |
|---|---|---|---|
| `LK-STRUCT` | Structure | Four header self-marks before the first `## `; `基准日：YYYY-MM-DD` present; `跟踪口径：` present; seven sections present and ordered; a `- 总股本：N 股 [S#]` row in section two; calendar rows `- date｜holder type｜one-sentence fact [S#]` with a registered holder type, non-descending dates, every row later than the base date; pressure-row shape | Putting an already-happened expiry in the calendar; a reversed calendar; forgetting the total-capital row |
| `LK-QUOTE` | Anchors | No row without an anchor; every source row carries `[S#]` + URL + `检索日`; pressure rows carry at least two **distinct** anchors; the total-capital row must carry its own | A pressure row with one anchor only — numerator and denominator from the same place; a source row with a title but no link |
| `LK-LINE` | Red lines | Price forecasts, rise-fall promises, buy-sell or reduction advice, ratings and target prices, lockup-pressure band judgments, hedging words (`约` / `左右` / `大概`) — zero hits | "Unlock means it falls", "heavy selling pressure", "advise reducing"; turning 1.2 亿股 into "about 1.2 亿股" |
| `LK-GAP` | Naming and ratios | Body says "missing X" ⇒ section six must name X, and the reverse also fires; every pressure row must declare its `占比出处`; a row marked calculated needs its method explained in section six; the pressure row's denominator must equal the total-capital row's number | **Dividing shares by total capital yourself** and presenting the percentage as if it were quoted; using the wrong-dated denominator |
| `LK-BOUND` | Boundaries | `跟踪口径` must start with `解禁`; written as already-happened / reduction / dividend / buyback / shareholder return → name `cn-shareholder-return`; written as pledge / release-of-pledge → name `cn-share-pledge-tracker`; fewer than two calendar rows → name `cn-shareholder-return` | Stuffing an already-happened reduction announcement into the expiry calendar |

### The cell that matters most: never calculate the ratio yourself

When the announcement says only "180,000,000 shares will be released" and gives no percentage, a card that divides by total capital and prints 4.50% has produced a number that **is not in the source sentence**. So every pressure row must declare its source:

```
- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1][S3]
```

`公告原文` means it was copied; `自算` (calculated) is also legal — but then section six must spell out the method, otherwise the checker fires `LK-GAP`. Both are fine; being vague is not.

### The denominator is sourced separately

Total share capital — the **denominator itself** — needs its own announcement and retrieval date. Total capital differs across points in time (placements and buyback cancellations both move it), and a wrong-dated denominator corrupts every ratio in the section. That is why the total-capital row in section two has its own anchor, and why every pressure row needs two distinct anchors: one for the numerator, one for the denominator. If a pressure row's denominator number differs from the section-two total-capital row, `LK-GAP` fires.

---

## 3. Quick start

List the catalog, take the group's routing address from it, confirm the tools are present, then fetch announcements and original-text parses before writing:

```bash
# 1. install
npx skills add huhoo/cue-awesome --skill cn-lockup-expiry-pressure

# 2. list the catalog, take the group's routing address
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# 3. confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

With the announcement list in hand you can lay out the skeleton first:

```bash
python3 scripts/make_outline.py list.jsonl skeleton.md
```

Then read each original and replace the placeholder rows with anchored facts.

---

## 4. First-time Cue setup

This package reaches announcements and original-text parsing through Cue's MCP channel. First use needs a credential (`CUE_API_KEY`), obtained from the Cue console and set as an environment variable; the package itself never stores or prints credentials.

You can also run it without the channel: with zero channel this package only lays the user's own expiry list out as a skeleton, and the cost is that it **cannot see the original text** — no original means no denominator and no cost price, ratios and cost bands stay as placeholders, and the note is just a run of dates.

---

## 5. Boundaries and non-promises

- This registers the **future expiry timetable** and two checkable quantities (share of total capital, cost band). It is not a view on the share price.
- An unlock means the lock-up expired and shares became tradable; **whether to sell is the holder's decision**. This package writes neither "unlock means dumping" nor "guaranteed cash-out", and never "selling pressure".
- Whether a round's pressure is big or small, and where the price goes afterwards: `[待人工]`. This package does not conclude that and does not pretend an objective threshold exists.
- No research notes, news or forum posts. A fact without an announcement link and a retrieval date does not enter the calendar.
- No derived expiry dates. If the announcement gives no specific date, write it as missing rather than back-computing one from "tradable when the lock-up ends".

---

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `LK-STRUCT` says a calendar row isn't three cells | A full-width colon, or a missing `｜` | Rewrite as `- YYYY-MM-DD｜holder type｜one-sentence fact [S#]` |
| `LK-STRUCT` says an expiry is not later than the base date | An already-happened expiry got in | Move it out; already-happened shareholder actions go to `cn-shareholder-return` |
| `LK-QUOTE` says a pressure row has one distinct anchor | Numerator and denominator use the same source number | Find a separate document for total capital and give it its own number |
| `LK-GAP` says the ratio source is undeclared | Missing `｜占比出处：…` | Write `公告原文` or `自算` — one of the two, never blank |
| `LK-GAP` says a calculated ratio has no method | Marked `自算` but section six says nothing | Add `口径：本轮占比为自算…` in section six |
| `LK-GAP` says the denominator differs from the total-capital row | Two different points in time were cited | Unify to one point in time and state it in section six |
| `LK-LINE` hits `约` / `左右` | An exact number was softened | Copy the announcement's number as written |
| `LK-BOUND` says the tracking basis mixes in already-happened actions | The header basis sentence drifted | Start the basis sentence with `解禁` |

---

## 7. How to ask

- **Good**: "How many lockup rounds does this stock have in the next year?" "When is the next expiry and how many shares?" "What share of total capital, and which document and which point in time is the denominator from?" "What was the placement price — which cost band does this round sit in?"
- **Bad**: "Will it fall after the unlock?" "Is this round's pressure big?" "Should I sell before the unlock?" "Give me a target price." — this package produces none of these and returns `[待人工]`.

---

## 8. Honest capability limits

- Only original announcements count. Where an announcement is vague, this package stays vague and names the gap rather than filling it in.
- Release holder lists are often not itemised by name; those can only be recorded at the "number of placement investors" level and listed as missing.
- Commitments between rounds and whether unlock conditions have been met are recorded only as the announcement states them — not one sentence added.
- The checker judges shape and sourcing discipline, not whether the numbers are true. Verifying the numbers is a human step against the original text — which is exactly what the four header self-marks are for.

---

## 9. Resources

- `SKILL.md` — the Chinese contract (seven-section shape, sourcing discipline, red lines)
- `SKILL.en.md` — the English face of the same contract
- `scripts/check_lockup.py` — five lanes, zero network
- `scripts/make_outline.py` — lays an announcement list out as a shaped skeleton; runs with zero channel
- `scripts/fixtures/run_fixtures.sh` — offline self-check, thirty seconds, zero network, zero billing; the last line reports the tier count it actually ran, so no document hardcodes it
- `CHANGELOG.md` — versions and known limits

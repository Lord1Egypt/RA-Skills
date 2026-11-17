---
name: cn-shareholder-return
slug: cue-cn-shareholder-return
displayName: "Shareholder Return Panorama · Dividend · Buyback · Reduction"
summary: "Split an A-share shareholder-return filing into eight verbatim cards."
description: "Shareholder-return card: split dividend, buyback, reduction and pledge filings into eight verbatim cards, each with the filing's sentence and anchor; gaps go to a missing-data list; judgement stays human. Do NOT use for: buy/sell advice, return evaluation, price prediction."
version: "0.1.1"
license: MIT
consumes: []
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
        description: "Optional credential: when absent the skill follows the user-supplied and degraded paths described on its face; when present it also reaches the channel side for original filings and attachment body parsing."
tags: [shareholder-return, dividend, buyback, reduction, pledge, verbatim-card]
---

# Shareholder Return Panorama Card

Split one A-share shareholder-return filing (distribution implementation notice, buyback plan,
reduction plan, pledge notice) into **eight verbatim cards**: each card records only the sentence
the filing itself wrote, plus an anchor. No evaluation, no prediction, no filing on anyone's behalf.

**Cut line**: this skill only records *what the filing says* and names what is missing.
**Whether the return is good, where the price goes, whether to trade — never judged.**

## 0. What it is / is not

| Is | Is not |
|---|---|
| A verbatim registration card for eight shareholder actions | Investment advice or a rating |
| Every item anchored, checkable against the original | An evaluation of return level or dividend yield |
| Gaps listed in a missing-data section, counted honestly | Substituting a reference number (net profit, share capital, VWAP) for the item's own value |
| Dividend / buyback / reduction / pledge side by side | Writing only the flattering group |

## 1. When to use

- The user hands over a distribution implementation notice and asks how the dividend is computed, per share, and when the record date is.
- The user hands over a buyback plan and asks how much, at what price, and for what purpose.
- The user hands over a reduction or pledge notice and asks who is reducing, how much, and how much is pledged.
- The user hands over several filings and wants one company's shareholder actions on one card.

## 2. Sourcing discipline

1. **Register the original sentence only** — inside the quote marks goes the filing's own text, never a paraphrase.
2. **Every item carries an anchor** — section, page or table; the anchor value may not be empty.
3. **Missing means missing** — write "not found", name it in the missing-data list, and say which document to go back to. Never write "no such item".
4. **Reconcile the count** — the header's "eight items, N missing" appears exactly once, and N must equal the number of "not found" item lines.
5. **A number belongs only to its own noun** — in `10 shares for 3.50 yuan`, the 10 is a denominator, not the payout; in `25% of net profit attributable to shareholders`, the 25% is a ratio, not the total dividend.
6. **Ratios and bonus shares are registered, not settled** — payout ratio, yield and capitalisation ratios are copied verbatim, never converted into amounts.
7. **Judgement stays human** — return level, price impact, whether a reduction is bearish, pledge risk: all go to the human section.

## 3. Output contract (five sections)

```
## 1. Header
- File: <company> <filing name> | Source: original / user-supplied | Attachment leg: started / not started
- Eight items, N missing

## 2. Eight verbatim cards
- Dividend plan and per-share payout: "<sentence>" anchor: <where>
- Total dividend and payout ratio: "<sentence>" anchor: <where>
- Record date and ex-dividend date: "<sentence>" anchor: <where>
- Buyback plan and size: "<sentence>" anchor: <where>
- Buyback price range and funding source: "<sentence>" anchor: <where>
- Buyback purpose and cancellation arrangement: "<sentence>" anchor: <where>
- Reduction plan and reducing parties: "<sentence>" anchor: <where>
- Pledge and release of pledge: "<sentence>" anchor: <where>

## 3. Basis comparison
- This card follows <which filing>; whether <the second disclosure> was obtained, whether the two agree, whether the basis is judged.

## 4. Missing data
- N missing: <item> — <what is missing>, go back to <which document>.

## 5. For a human
- [human] <return level / price impact / reduction bearishness / pledge risk> all left to a human; this skill does not act on anyone's behalf.
```

Real filings use aliases for these items ("profit distribution plan", "equity distribution plan",
"share buyback plan", "share reduction plan"); any alias is accepted and the checker maps it to the
canonical item name.

## 4. Data channel (live catalog is authoritative)

Real tasks take the channel's proper path: read the catalog, then fetch the filing and attachment body by tool name.

```bash
curl -s https://cuecue.cn/api/mcp-catalog | head -c 2000
```

Once the endpoint is known, send `tools/list` over MCP and confirm `parse` / `get_parse_status` /
`read_result` are all present, then hand the filing URL or local path to `parse`, poll with
`get_parse_status`, and read the body and tables with `read_result`.

**Zero-key degradation**: without `CUE_API_KEY` this skill works only from the user-supplied filing
text and local files; the cost is that **the channel-side original filing and attachment body parsing
are unavailable**, so anchors can only land on the copy the user provided and cross-document
verification cannot be done.

## 5. Compliance red lines (shipped with the suite)

- No evaluation of return level (whether the payout ratio is high, whether the buyback is forceful enough, whether the yield is worth it).
- No prediction of price or market-cap impact (whether a buyback will lift the price, whether a reduction is bearish).
- No buy/sell advice (buy, sell, increase, reduce, hold).
- No drafting filings, no tax computation, no filing on anyone's behalf.
- No inside information, no advice on bypassing approval or avoiding disclosure.
- No ruling on validity (whether a plan is valid, non-compliant, or constitutes a commitment).

## 6. Quick flow (user's view)

1. Hand the filing (URL or local file) to this skill.
2. It registers the eight items verbatim, each with its sentence and anchor.
3. Whatever it cannot get goes to the missing-data list, naming the document to go back to.
4. Judgement questions all go to the human section; this skill does not take them.

## 7. Machine check

```bash
python3 -B scripts/check_sh_return_card.py <card.md>     # five codes, item by item; PASS when clean
python3 -B scripts/check_sh_return_card.py --selftest    # good sample passes, bad samples fire all five
bash scripts/fixtures/run_fixtures.sh                    # offline fixtures, three tiers, zero network
```

Five codes: `SR-STRUCT` five sections present and eight items present line by line / `SR-QUOTE`
sentence and anchor may not be empty / `SR-LINE` three red-line assertion families / `SR-COUNT`
exactly one missing-count declaration reconciled against "not found" / `SR-VALUE` the numeric cells
settled by phrase structure.

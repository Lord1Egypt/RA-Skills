# tax-policy-card-cn

**Give it one mainland tax document and get back an eight-item verbatim card: authority and number, tax type and taxpayers, rate, tax base, effective date, filing deadline, transitional rules, preferential conditions and retained records - each item carrying a verbatim quote and a source anchor. Tax savings stay `[待人工]`.**

It reads one tax document only: policy impact chains live in `policy-impact-cn`, placement and issuance terms in `placement-terms-cn`, company filing lists in `announcement-daily-cn`. The document text is the only authority - **commentary and local interpretations must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over one document: pasted text, an official page, or a PDF location. For anything the document does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the document, no channel needed.
3. Check the rate and date cells: rates and dates stay verbatim; "to be prescribed" and "pending" are not dates and belong in the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_tax_card.py` gates the card: five sections plus item-level presence of the eight names (each name needs its own line; a mention in prose does not count) / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red-line assertions only on `[待人工]` lines / exactly one completeness declaration reconciled with the number of `未检索到` lines / the two date items must carry a verbatim date or deadline, deferred wording fires.

```bash
python3 scripts/check_tax_card.py --help                          # usage
python3 scripts/check_tax_card.py --selftest                       # good sample passes, bad sample fires all five lanes, five threshold pins, temp files clean themselves
python3 scripts/check_tax_card.py scripts/fixtures/good-tax-card.md    # PASS (zero findings)
python3 scripts/check_tax_card.py scripts/fixtures/bad-tax-card.md     # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r tax-policy-card-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-tax-card.md
python3 ~/.workbuddy/skills/tax-policy-card-cn/scripts/check_tax_card.py ./my-tax-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill tax-policy-card-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **official text** (finding the original document and its number, data leg) and **attachment parsing** (long attachments and multi-page PDFs, parsing leg). With neither installed the card still comes out from text you supply; what you lose is document numbers and clauses that live inside attachments - those stop at `未检索到` and the level comparison must be done by hand.

1. Register at <https://cuecue.cn>;
2. Take `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in local credentials - **never paste it into a chat**; the agent never handles the key;
3. Install: `cue-data-mcp` for the official-text leg, `cue-omni-reader` for the parsing leg. One command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills`;
   - single: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install only that one).

Configuration pages are pointed at, not restated: data leg <https://cuecue.cn/hub/mcp>; parsing leg <https://cuecue.cn/hub/omni-reader>; key <https://cuecue.cn/hub/api-key>.

### Connectivity self-check

```bash
# 1) catalog reachable anonymously: proves the catalog reads, not "connected"
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200

# 2) take routing.url and transport for the domain from the response; never hard-code the host
# 3) with the key, send tools/list - proves that endpoint accepted the key, nothing else
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

## 5. Boundaries

- Tax calculations, burden changes, savings and refunds stay `[待人工]`; no "save X" or "burden drops" claims, no guaranteed-gain or risk-free wording;
- No filing on your behalf: no return forms, no filing channel, no agency work;
- Missing means `未检索到`, never a habit-based fill and never "none";
- Dates and numbers verbatim: "to be prescribed" / "pending" / "subject to ..." are not date values and go to the missing-data list;
- Domains and tools follow the live catalog; no fixed list, no count promise, no real-time promise.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The document is a summary, or the quote sits in an attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / deferred date / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Central text and local interpretation differ | Different levels or an updated basis | Put both quotes in the comparison section with their own anchors; no applicability judgement |

## 7. How to ask

- Good: "what does this announcement say about the rate and the tax base", "when does it take effect and does the old one still apply", "what is the filing deadline", "quote the exact wording of the super-deduction rate".
- Bad: "work out how much tax I save", "file it for me" - calculations and filing are out of scope and stay `[待人工]`.

## 8. Honest capability list

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not plan taxes, does not produce returns, does not judge whether you qualify; it does not assess how strictly a local interpretation is enforced, it records levels and text; it stores nothing of your documents - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/tax-layers.md`: document levels and the three-element recording method (including the deferred-date list)
- `scripts/check_tax_card.py`: five machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
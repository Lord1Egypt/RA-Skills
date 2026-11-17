# insurance-terms-cn

**Give it one mainland insurance policy and get back an eight-item verbatim card: coverage, exclusions, sum insured and deductible, waiting period, term and premium period, claim documents and deadlines, cooling-off and surrender, disclosure duties - each item carrying a verbatim quote and a source anchor. Payout figures stay `[待人工]`.**

It reads one policy only: policy impact chains live in `policy-impact-cn`, general contract comparison in `cn-contract-clauses`, company filing lists in `announcement-daily-cn`. The policy text is the only authority - **application notes and sales-page summaries must be labelled by level**, and that boundary is why this skill exists.

## 1. Three steps to get going

1. Hand over one policy: pasted text, an official page, or a PDF location. For anything the policy does not state, demand `未检索到` instead of a habit-based fill.
2. Read the first two sections: header declaration plus the eight verbatim items - both come out as soon as you have the policy, no channel needed.
3. Check the amount and period cells: sum insured, deductible and term stay verbatim; "subject to the policy" and "depends on the plan" are not values and belong in the missing-data list.

## 2. Five machine checks (no network)

`scripts/check_insurance_card.py` gates the card: five sections plus item-level presence of the eight names (each name needs its own line; a mention in prose does not count) / quote and anchor per item (empty or single-character quotes and empty anchors fire) / red-line assertions only on `[待人工]` lines / exactly one completeness declaration reconciled with the number of `未检索到` lines / the sum-insured and period items must carry a unit-bearing number, deferred wording fires.

```bash
python3 scripts/check_insurance_card.py --help                          # usage
python3 scripts/check_insurance_card.py --selftest                       # good sample passes, bad sample fires all five lanes, five threshold pins, temp files clean themselves
python3 scripts/check_insurance_card.py scripts/fixtures/good-insurance-card.md    # PASS (zero findings)
python3 scripts/check_insurance_card.py scripts/fixtures/bad-insurance-card.md     # FAIL (five lanes, each naming its line)
```

## 3. Install and run

```bash
mkdir -p ~/.workbuddy/skills
cp -r insurance-terms-cn ~/.workbuddy/skills/
# ask the agent for the five-section card defined in SKILL.md, save it as my-insurance-card.md
python3 ~/.workbuddy/skills/insurance-terms-cn/scripts/check_insurance_card.py ./my-insurance-card.md
```

Install this skill alone: npx skills add huhoo/cue-awesome --skill insurance-terms-cn (installs this package only; restart the session on your side afterwards).

## 4. First-time Cue setup (three steps, skippable)

Two evidence legs are optional: **policy text** (finding the official policy and filing information, data leg) and **attachment parsing** (long attachments and multi-page PDFs, parsing leg). With neither installed the card still comes out from text you supply; what you lose is clause numbers and exclusions that live inside attachments - those stop at `未检索到` and the level comparison must be done by hand.

1. Register at <https://cuecue.cn>;
2. Take `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in local credentials - **never paste it into a chat**; the agent never handles the key;
3. Install: `cue-data-mcp` for the policy leg, `cue-omni-reader` for the parsing leg. One command, two forms:
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

- Payout estimates, premium and coverage assumptions, "how much would be paid" and "would it pay" stay `[待人工]`; no guaranteed payout, guaranteed renewal, risk-free or guaranteed-gain wording;
- No claims handling on your behalf: no claim forms, no filing channel, no agency work;
- Missing means `未检索到`, never a habit-based fill and never "none";
- Amounts and periods verbatim: "subject to the policy", "depends on the plan", "to be agreed", "pending" are not values and go to the missing-data list;
- Domains and tools follow the live catalog; no fixed list, no count promise, no real-time promise.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Many items are `未检索到` | The policy is an excerpt, or the quote sits in an attachment | Start the parsing leg; if unavailable, keep the missing-data entries, never fill by habit |
| Data leg unreachable | Missing credential or the domain is not live | Follow section 4; the first two sections still come out with the cost stated there |
| Gate turns red | Missing anchor / missing quote / deferred amount / count mismatch | Fix the named lines; unfixable ones go to the missing-data list, never delete lines to make counts match |
| Policy and sales page differ | Different levels or a rewritten summary | Put both quotes in the comparison section with their own anchors; no applicability judgement |

## 7. How to ask

- Good: "what does this policy cover and exclude", "what are the sum insured and the deductible", "how long is the waiting period", "which documents does a claim need and how soon", "what happens on surrender during cooling-off".
- Bad: "how much would I get", "pick a better product for me", "file the claim for me" - payouts, comparison and claims are out of scope and stay `[待人工]`.

## 8. Honest capability list

Market and fund-flow figures are out of scope (that domain follows the live catalog; if it is not open, nothing is promised). This skill does not compare products, does not judge whether you should buy, does not assess an insurer's solvency; it does not interpret regulation, it records policy text and levels; it stores nothing of your documents - the card is handed back.

## 9. Resources

- `SKILL.md`: the five-section contract and red lines (the Chinese face is authoritative)
- `SKILL.en.md`: this English counterpart; where they differ, the Chinese face wins
- `references/insurance-layers.md`: policy levels and the three-element recording method (including the deferred amount/period list)
- `scripts/check_insurance_card.py`: five machine checks (no network)
- `scripts/fixtures/`: one good and one bad sample used by `--selftest`
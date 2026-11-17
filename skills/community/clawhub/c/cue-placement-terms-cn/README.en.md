# placement-terms-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Hand it one A-share private placement (refinancing) proposal and get back a ten-item terms card: every item carries the source sentence verbatim plus an anchor, any item that was not retrieved is named as `未检索到`, and dilution impact or "is it worth joining" always goes to `[待人工]`.**

It manages the term skeleton and provenance of one placement proposal. Event-level triage of a single filing lives in the sister skill `event-brief-cn`; a cross-entity public-record risk sheet lives in `dd-checklist`.

## 1. Open it and work: three steps

1. Hand over one proposal: pasted text, a PDF/disclosure locator or a filing URL all work. Never let it guess a term that is not in the text — a missing item must be written as `未检索到`.
2. Read the first two sections: header declaration plus the itemized terms table. These come out as soon as the source text is in hand and need no channel at all.
3. Only items that live in the appendices trigger parsing: dilution tables and performance-commitment clauses are usually inside the prospectus attachments. With the parsing leg not started, those items stay `未检索到` and a human has to check the original.

## 2. The four machine checks (zero network)

`scripts/check_terms.py` gates the card: five sections present and all ten item names on the card / every item carries its source sentence and an anchor / red-line assertions appear only inside `[待人工]` lines / the missing-count declaration reconciles with the missing list.

```bash
python3 scripts/check_terms.py --selftest                        # good sample must pass, bad sample must fire all four lanes, three counter-examples must fire their own lane, temp files clean themselves
python3 scripts/check_terms.py scripts/fixtures/good-terms.md    # PASS (zero findings)
python3 scripts/check_terms.py scripts/fixtures/bad-terms.md     # FAIL (all four lanes, each naming its line)
```

## 3. Getting started

```bash
# 1. drop it into the skills directory
mkdir -p ~/.workbuddy/skills
cp -r placement-terms-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md and save it as my-placement-card.md

# 3. run the machine gate (zero network)
python3 ~/.workbuddy/skills/placement-terms-cn/scripts/check_terms.py ./my-placement-card.md
```

Install this skill on its own: npx skills add huhoo/cue-awesome --skill placement-terms-cn (this line installs this package only; on your side the session has to be restarted before it takes effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **source listing** (disclosure and filing domains, on the data leg) and **attachment parsing** (prospectus bodies and long appendices, on the parsing leg). Both are optional — with neither installed the card still comes out from text you supply directly; what you lose is any term that sits inside the attachments, which is exactly where the dilution table and the performance commitment usually are, so those items need a human at the original.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials — **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the source-listing leg, `cue-omni-reader` for the parsing leg. One command, two ways to write it:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills that set publishes, pick what you want);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one instead).

Pointers only, no duplicated setup steps: disclosure and filing listings run on the data leg, its official configuration page is <https://cuecue.cn/hub/mcp>; attachment text runs on the parsing leg, its official configuration page is <https://cuecue.cn/hub/omni-reader>; the key comes from <https://cuecue.cn/hub/api-key>.

### Connectivity self-check (how far each claim actually proves)

```bash
# 1) catalog reachable (anonymous): proves the catalog reads, nothing more — this is not "connected"
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200

# 2) take the domain's routing.url and transport from that response; do not copy the host into a config by hand
# 3) with a key, send tools/list — proves only that this data-leg endpoint accepts the key, and proves nothing about other entries
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

An installed skill ≠ configured credentials ≠ a connected data leg: that last layer's test covers only the data-leg path — the endpoint accepts the key and `tools/list` returns something for that domain's `routing`, and that proves the key is accepted there, nothing beyond the data leg.

## 5. Boundaries and non-promises

- Dilution impact on existing holders, whether joining is worth it, how many approval steps are left, and float pressure after the lock-up all go to `[待人工]`; no "guaranteed gain", "risk-free" or "assured return" wording;
- The approval chain records only the node that already appears in a disclosure; a node that never appears is written as `未检索到`, never as a forecast of the next one;
- Source sentences stay verbatim: no rounding, no "approximately", and "no lower than 80% of the average price of the 20 trading days before the pricing基准日" is never compressed into "a 20% discount";
- Domains and tool names follow the live catalog at its current values; this skill publishes no fixed list and promises neither a count nor real-time approval status.

## 6. When something goes wrong

| Symptom | Where it comes from | What to do |
|---|---|---|
| Several items read `未检索到` | The terms sit in the attachments and parsing was not started | Start the parsing leg per §4; the first two sections still come out, cost stated in §4 |
| Data leg unreachable | Missing credentials, or the domain is not live | Walk §4's three steps; text you supply directly still produces the card |
| Machine gate turns red | Missing anchor, numbers without a source sentence, missing-count not declared, red-line word outside a pending line | Fix the named lines; anything you cannot fix goes into the missing list by name rather than deleting the row |
| The comparison section is empty | Only one version of the proposal in hand | That section says "two versions not both retrieved, no difference judgement" — never filled with boilerplate |

## 7. How to ask (and how not to)

- Works: "what exactly does the price floor of this placement say", "which items changed in the revised proposal", "is there a lock-up and a performance commitment", "how far along is the approval".
- Doesn't: "is joining this placement a good buy" — worth-it and price calls are out of scope and land in `[待人工]`.

## 8. Honest limits

Quotes and fund-flow figures are not in scope (that domain is judged by live catalog values; if it is not open, nothing is promised about it). No side-by-side comparison across multiple proposals, no cross-entity risk sheet (`dd-checklist`), no event-level triage of a single filing (`event-brief-cn`), no general contract clause diffing (`cn-contract-clauses`). This skill stores nothing of your proposal files: the card is handed back and that is the end of it.

## 9. Resources

- `SKILL.md`: the five-section card contract and the red lines, in full
- `scripts/check_terms.py`: the four machine checks (zero network)
- `scripts/fixtures/`: one good sample and one bad sample, both consumed by `--selftest`

# policy-impact-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Hand it one policy document and get back a verbatim key-points card plus candidate impact chains: every chain quotes one sentence of the policy as its basis and carries a source anchor, while interpretation, price direction and any "who benefits" list stay `[待人工]`.**

It answers only "what does this document say, and which stages does it touch on its face". A single company's penalty and regulatory-measure sheet lives in `event-risk-scan`, an industry condition survey lives in `sector-overview`, and putting disclosed dates on a calendar lives in `catalyst-calendar`.

## 1. Open it and work: three steps

1. Hand over one document: pasted text, or a locator into a PDF or a webpage. Where the text says nothing, ask for `未检索到` — never let it fill a gap from common sense.
2. Read the first two sections: header declaration plus verbatim key points. These come out as soon as the source text is in hand and need no channel at all.
3. Look at where each chain is hung: every chain level must point back to one sentence of policy text. Levels that cannot be hung get cut, so the chain is shorter than you expect — that is the design, not missing data.

## 2. The four machine checks (zero network)

`scripts/check_chain.py` gates the card: five sections and all required item names present / every line carries its quote, basis and anchor / red-line assertions appear only inside `[待人工]` lines / the declared chain count reconciles with the actual chains.

```bash
python3 scripts/check_chain.py --selftest                        # good sample must pass, bad sample must fire all four lanes, counter-examples fire their own lane, temp files clean themselves
python3 scripts/check_chain.py scripts/fixtures/good-chain.md    # PASS (zero findings)
python3 scripts/check_chain.py scripts/fixtures/bad-chain.md     # FAIL (all four lanes, each naming its line)
```

## 3. Getting started

```bash
# 1. drop it into the skills directory
mkdir -p ~/.workbuddy/skills
cp -r policy-impact-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md and save it as my-policy-card.md

# 3. run the machine gate (zero network)
python3 ~/.workbuddy/skills/policy-impact-cn/scripts/check_chain.py ./my-policy-card.md
```

Install this skill on its own: npx skills add huhoo/cue-awesome --skill policy-impact-cn (this line installs this package only; on your side the session has to be restarted before it takes effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **document listing** (policy and regulatory domains, on the data leg) and **text parsing** (long documents and attachments, on the parsing leg). Both are optional — with neither installed the card still comes out from text you supply directly; what you lose is any basis sentence sitting inside an attachment, so chains can only be cut short and the three date cells may stay `未检索到`.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials — **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the document-listing leg, `cue-omni-reader` for the parsing leg. One command, two ways to write it:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills that set publishes, pick what you want);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one instead).

Pointers only, no duplicated setup steps: policy and regulatory listings run on the data leg, its official configuration page is <https://cuecue.cn/hub/mcp>; document bodies and attachments run on the parsing leg, its official configuration page is <https://cuecue.cn/hub/omni-reader>; the key comes from <https://cuecue.cn/hub/api-key>.

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

- Interpretation, winner/loser calls, enforcement intensity, and how much any entity is affected all go to `[待人工]`; no "guaranteed gain", "risk-free" or "assured return" wording, and no naming of "beneficiary stocks" or sector leaders;
- A chain stops at the stage: it never ends in an investment conclusion, and any level without a quoted policy basis is dropped;
- Source sentences stay verbatim: no rounding, no "approximately", and qualifiers such as phased implementation are never collapsed into one sentence of conclusion; a date or deadline absent from the text is written as `未检索到`, never as "none" and never inferred;
- Domains and tool names follow the live catalog at its current values; this skill publishes no fixed list and promises neither a count nor real-time access to policy text.

## 6. When something goes wrong

| Symptom | Where it comes from | What to do |
|---|---|---|
| The chains look short | Basis sentences live in attachments and parsing was not started | Start the parsing leg per §4; the first two sections still come out, cost stated in §4 |
| Data leg unreachable | Missing credentials, or the domain is not live | Walk §4's three steps; text you supply directly still produces the card |
| Machine gate turns red | Missing anchor, basis not a quote, chain count disagrees with the declaration, red-line word outside a pending line | Fix the named lines; anything you cannot fix goes into the missing list by name rather than deleting the row |
| All three date cells empty | The text carries no effective date, transition period or filing window | Write `未检索到` in each cell — do not substitute "none", do not invent a date by convention |

## 7. How to ask (and how not to)

- Works: "what does this new rule say and when does it take effect", "which stages of the chain does this clause touch on its face", "what are the transition period and filing window", "what changed between the draft for comment and the final version".
- Doesn't: "which sectors does this help" — beneficiary lists and direction calls are out of scope and land in `[待人工]`.

## 8. Honest limits

Quotes and fund-flow figures are not in scope (that domain is judged by live catalog values; if it is not open, nothing is promised about it). This skill does not interpret policy, does not rank who is helped or hurt, does not build a company risk sheet (`event-risk-scan`), does not survey an industry (`sector-overview`), and does not turn dates into a calendar (`catalyst-calendar`). It also stores nothing of your documents: the card is handed back and that is the end of it.

## 9. Resources

- `SKILL.md`: the five-section card contract and the red lines, in full
- `scripts/check_chain.py`: the four machine checks (zero network)
- `scripts/fixtures/`: one good sample and one bad sample, both consumed by `--selftest`

# roadshow-minutes-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Hand it one roadshow, site-visit or earnings-call minute and get back an eight-item verbatim card: every item carries the source sentence plus an anchor, and any item containing a quantified claim is additionally tagged `口头表述，未经披露文件核对` (spoken, not yet checked against a filing) — ratings and price targets always go to `[待人工]`.**

It reads minutes that already exist. A list of what a company filed lives in `announcement-daily-cn`, clause-level breakdown of one proposal in `placement-terms-cn`, turning a recording into a transcript in `meeting-minutes-cn`. What management said in a call is not what the company disclosed — that line is the reason this skill exists.

## 1. Open it and work: three steps

1. Hand over one set of minutes: pasted text, a PDF or disclosure-page locator, or a transcript. Anything the text does not contain must be written as `未检索到`, never filled in by convention.
2. Read the first two sections: header declaration plus the eight verbatim items. These come out as soon as the minutes are in hand and need no channel at all.
3. Look at the tags: lines carrying amounts, ratios, capacity or institution counts must show the spoken-not-verified marker. Want to treat one as fact? Start the comparison leg and fetch the company's own investor-relations record.

## 2. The four machine checks (zero network)

`scripts/check_minutes.py` gates the card: five sections present and each of the eight item names occupying its own line (a name only mentioned in prose does not count) / every item carries a real source sentence, a non-empty anchor and the spoken-claim tag (an empty or single-character bracket counts as no sentence) / red-line assertions appear only inside `[待人工]` lines / exactly one completeness declaration, reconciled against the not-retrieved lines.

```bash
python3 scripts/check_minutes.py --selftest                     # good sample must pass, bad sample must fire all four lanes, eight counter-examples each fire their own branch under a branch-unique label, temp files clean themselves
python3 scripts/check_minutes.py scripts/fixtures/good-minutes.md    # PASS (zero findings)
python3 scripts/check_minutes.py scripts/fixtures/bad-minutes.md     # FAIL (all four lanes, each naming its line)
```

## 3. Getting started

```bash
# 1. drop it into the skills directory
mkdir -p ~/.workbuddy/skills
cp -r roadshow-minutes-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md and save it as my-minutes-card.md

# 3. run the machine gate (zero network)
python3 ~/.workbuddy/skills/roadshow-minutes-cn/scripts/check_minutes.py ./my-minutes-card.md
```

Install this skill on its own: npx skills add huhoo/cue-awesome --skill roadshow-minutes-cn (this line installs this package only; on your side the session has to be restarted before it takes effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **text parsing** (long transcripts and multi-page minutes, on the parsing leg) and **official comparison** (fetching the investor-relations activity record the company itself published, on the data leg). Both are optional — with neither installed the card still comes out from the minutes you supply; what you lose is that every figure stays at spoken level, so "management said capacity is full" cannot be matched against a filing and a human has to do that check.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials — **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-omni-reader` for the parsing leg, `cue-data-mcp` for the comparison leg. One command, two ways to write it:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills that set publishes, pick what you want);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-omni-reader` (swap the trailing name for `cue-data-mcp` to install that one instead).

Pointers only, no duplicated setup steps: bodies and attachments run on the parsing leg, its official configuration page is <https://cuecue.cn/hub/omni-reader>; fetching the official record runs on the data leg, its official configuration page is <https://cuecue.cn/hub/mcp>; the key comes from <https://cuecue.cn/hub/api-key>.

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

An installed skill ≠ configured credentials ≠ a connected data leg: that last layer's test covers only the data-leg path — the endpoint accepts the key and `tools/list` returns something for that domain's `routing`, and that proves the key is accepted there, nothing beyond the data leg; the parsing leg is proven by its own face, not by this one.

## 5. Boundaries and non-promises

- Ratings, price targets, direction calls and "is this bullish" all go to `[待人工]`; no "guaranteed gain", "risk-free" or "assured return" wording;
- Spoken words are not disclosure: any item with an amount, ratio, capacity or institution count must carry the spoken-not-verified tag, and an item that cannot carry it goes into the missing list;
- Not retrieved is written as `未检索到`; "none" never stands in for it, and management answers are never reconstructed from convention;
- Domains and tool names follow the live catalog at its current values; this skill publishes no fixed list, promises no count, and promises neither that the domain is open nor that records arrive in real time.

## 6. When something goes wrong

| Symptom | Where it comes from | What to do |
|---|---|---|
| Several items read `未检索到` | The forwarded minutes are incomplete, or the sentence lives in an attachment | Start the parsing leg to recover the sentence; if it cannot start, keep the missing item named instead of filling it in |
| Data leg unreachable | Missing credentials, or the domain is not live | Walk §4's three steps; the first two sections still come out, cost stated in §4 |
| Machine gate turns red | Missing anchor, missing quote, quantified item without the spoken tag, counts disagree | Fix the named lines; anything you cannot fix goes into the missing list rather than deleting the row |
| Minutes disagree with the official record | The forwarded version paraphrased or dropped qualifiers | Put both sentences in the comparison section with their own anchors; do not pick a winner |

## 7. How to ask (and how not to)

- Works: "what did management actually say in this site-visit minute", "which questions did institutions ask and how were they answered", "is there a filing behind the capacity number in this minute", "who attended the call".
- Doesn't: "is this bullish, should I add" — direction and position actions are out of scope and land in `[待人工]`.

## 8. Honest limits

Quotes and fund-flow figures are not in scope (that domain is judged by live catalog values; if it is not open, nothing is promised about it). This skill does not score how credible a set of minutes is — it records verbatim text and provenance state only. It does not judge whether management's statements are true; it marks them as not yet checked against a filing. It also stores nothing of your minutes: the card is handed back and that is the end of it.

## 9. Resources

- `SKILL.md`: the five-section card contract and the red lines, in full (Chinese face governs)
- `SKILL.en.md`: this face's counterpart, with the same name and version
- `references/oral-claims.md`: the four-layer provenance table (spoken / forwarded / matches the official record / disclosure-grade)
- `scripts/check_minutes.py`: the four machine checks (zero network)
- `scripts/fixtures/`: one good sample and one bad sample, both consumed by `--selftest`

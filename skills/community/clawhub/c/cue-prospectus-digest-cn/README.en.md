# prospectus-digest-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Hand it one A-share IPO prospectus and get back an eight-item verbatim card: every item carries the source sentence plus a page anchor, any self-praise sentence is tagged "issuer's own statement", and valuation or subscription questions always go to `[待人工]`.**

It reads a several-hundred-page document down to eight lines you can check back against the original. Clause breakdown of one refinancing proposal lives in `placement-terms-cn`, a list of what a company filed in `announcement-daily-cn`, and a cross-entity public-record risk sheet in `dd-checklist`.

## 1. Open it and work: three steps

1. Hand over one prospectus: pasted text or a PDF/disclosure-page locator; say which draft it is (filing draft, hearing draft or registration draft) and put that in the header.
2. Read the first two sections: header declaration plus the eight verbatim items. These come out as soon as the text is in hand and need no channel at all.
3. Watch two kinds of tags: self-praise sentences need "issuer's own statement, no third-party basis", and financial lines keep their period and unit exactly as printed — no conversion.

## 2. The five machine checks (zero network)

`scripts/check_prospectus.py` gates the card: five sections present and each of the eight item names occupying its own line (a name only mentioned in prose does not count) / every item carries a real source sentence and an anchor whose value is non-empty and lands back on a page (an empty or single-character bracket counts as no sentence) / an untagged self-praise sentence fires / red-line assertions appear only inside `[待人工]` lines / exactly one completeness declaration, reconciled against the not-retrieved lines.

```bash
python3 scripts/check_prospectus.py --selftest                          # good sample must pass, bad sample must fire all five lanes, nine counter-examples each fire their own branch under a branch-unique label, temp files clean themselves
python3 scripts/check_prospectus.py scripts/fixtures/good-prospectus.md     # PASS (zero findings)
python3 scripts/check_prospectus.py scripts/fixtures/bad-prospectus.md      # FAIL (all five lanes, each naming its line)
```

## 3. Getting started

```bash
# 1. drop it into the skills directory
mkdir -p ~/.workbuddy/skills
cp -r prospectus-digest-cn ~/.workbuddy/skills/

# 2. ask the agent for the five-section card defined in SKILL.md and save it as my-prospectus-card.md

# 3. run the machine gate (zero network)
python3 ~/.workbuddy/skills/prospectus-digest-cn/scripts/check_prospectus.py ./my-prospectus-card.md
```

Install this skill on its own: npx skills add huhoo/cue-awesome --skill prospectus-digest-cn (this line installs this package only; on your side the session has to be restarted before it takes effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **source fetching** (the prospectus text and its draft version, on the data leg) and **section retrieval** (the several-hundred-page body and its attachments, on the parsing leg). Both are optional — with neither installed the card still comes out from text you supply directly; what you lose is the deep chapters, and the R&D and risk sections usually stay `未检索到`, which is exactly where self-praise sentences cluster.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials — **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the source-fetching leg, `cue-omni-reader` for the section-retrieval leg. One command, two ways to write it:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills that set publishes, pick what you want);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one instead).

Pointers only, no duplicated setup steps: originals and drafts run on the data leg, its official configuration page is <https://cuecue.cn/hub/mcp>; long-document retrieval runs on the parsing leg, its official configuration page is <https://cuecue.cn/hub/omni-reader>; the key comes from <https://cuecue.cn/hub/api-key>.

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

An installed skill ≠ configured credentials ≠ a connected data leg: that last layer's test covers only the data-leg path — the endpoint accepts the key and `tools/list` returns something for that domain's `routing`, and that proves the key is accepted there, nothing beyond the data leg; the retrieval leg is proven by its own face, not by this one.

## 5. Boundaries and non-promises

- Valuation, comparables, whether to subscribe, price direction and risk ranking all go to `[待人工]`; no guaranteed-gain, risk-free or assured-return wording;
- **Self-praise is not fact**: sentences with leading/advanced/largest/first-created style claims must carry the issuer's-own-statement tag, and a sentence that cannot carry it does not enter the conclusion — a ranking-shaped fact such as "the largest customer accounts for 21.40%" is not judged by this rule;
- **Forward-looking is not accomplished**: qualifiers like "the company will", "expects", "strives to" and "under development" stay attached to the whole sentence;
- Numbers and periods verbatim: no conversion, no rounding, no "approximately", and 万元 is never rewritten as 亿元;
- Domains and tool names follow the live catalog at its current values; this skill publishes no fixed list, promises no count, and promises neither that a domain is open nor that drafts update in real time.

## 6. When something goes wrong

| Symptom | Where it comes from | What to do |
|---|---|---|
| R&D and risk sections read `未检索到` | Deep chapters were never retrieved | Start the section-retrieval leg; if it cannot start, keep the missing item named rather than borrowing from a media article |
| Data leg unreachable | Missing credentials, or the domain is not live | Walk §4's three steps; text you supply directly still produces the card |
| Machine gate turns red | Missing page anchor, untagged self-praise, counts disagree, red-line word outside a pending line | Fix the named lines; anything unfixable goes into the missing list rather than deleting the row |
| Two numbers for the same fact | The prospectus itself carries two statistical scopes | Put both sentences in the comparison section with their own anchors; do not pick a winner |

## 7. How to ask (and how not to)

- Works: "how much does this prospectus raise and where does it go", "what is the top-three customer concentration", "who is the actual controller", "what risks does the issuer write about itself", "what changed between the filing draft and the hearing draft".
- Doesn't: "what is this stock worth, should I subscribe" — valuation and subscription decisions are out of scope and land in `[待人工]`.

## 8. Honest limits

Quotes and fund-flow figures are not in scope (that domain is judged by live catalog values; if it is not open, nothing is promised about it). This skill does not value companies, does not score risk, and does not backfill from media coverage. Event-level triage of a single filing lives in `event-brief-cn`, clause breakdown in `placement-terms-cn`, cross-entity sheets in `dd-checklist`. It also stores nothing of your prospectus files.

## 9. Resources

- `SKILL.md`: the five-section card contract and the red lines, in full (Chinese face governs)
- `SKILL.en.md`: this face's counterpart, with the same name and version
- `references/self-claimed.md`: the provenance layering for self-claimed statements (which words need a tag, why ranking-shaped facts are exempt)
- `scripts/check_prospectus.py`: the five machine checks (zero network)
- `scripts/fixtures/`: one good sample and one bad sample, both consumed by `--selftest`

# announcement-daily-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Give it one company or one watchlist and get back a day-by-day list of that issuer's A-share filings: every line carries its disclosure date, the filing title verbatim, and a source anchor — ratings, price targets and any read on the tape stay `[待人工]`.**

It manages the list, not the close reading of a single filing. That job belongs to the sister skill `event-brief-cn`: this one answers "which filings landed today", that one answers "what does this one actually say".

## 1. Open it and work: three steps

1. Name the subject: one company (name or 6-digit code) or a watchlist file. No code available? The list still goes out with the name and `代码待补` — this skill never fills a code in for you.
2. Name the window: today by default; a window that straddles a weekend, a suspension or a resumption gets flagged as such in the output header.
3. Read the output: the header declaration plus the itemized lines come out as soon as the list is retrieved. Only the lines that need to be checked against the original trigger attachment parsing — a slow or unavailable parsing leg does not block those first two sections; what it costs you is that the points stay at list level and clause-level differences need a human reading the original.

## 2. The five machine checks (zero network)

`scripts/check_digest.py` gates the product: four sections present and shaped / every line carries title + date and an anchor / red-line assertions appear only inside `[待人工]` lines / counts match the declaration / a value slot may not stay empty or be filled with a one-character or punctuation-only placeholder.

```bash
python3 scripts/check_digest.py --selftest                        # good sample must pass, bad sample must fire all five lanes, the five threshold pins each fire their own line, temp files clean themselves
python3 scripts/check_digest.py scripts/fixtures/good-digest.md   # PASS (zero findings)
python3 scripts/check_digest.py scripts/fixtures/bad-digest.md    # FAIL (all five lanes, each naming its line)
```

## 3. Getting started

```bash
# 1. drop it into the skills directory
mkdir -p ~/.workbuddy/skills
cp -r announcement-daily-cn ~/.workbuddy/skills/

# 2. ask the agent for the four-section list defined in SKILL.md §3, save it as my-digest.md

# 3. run the machine gate (zero network)
python3 ~/.workbuddy/skills/announcement-daily-cn/scripts/check_digest.py ./my-digest.md
```

Install this skill on its own: npx skills add huhoo/cue-awesome --skill announcement-daily-cn (this line installs this package only; on your side the session has to be restarted before it takes effect).

## 4. First-time Cue setup (three steps, skippable)

This skill has two evidence legs: **list retrieval** (filing titles and disclosure dates from the announcement and disclosure domains) and **attachment parsing** (the body of a single filing and its long appendices). Neither needs to be installed to get the list skeleton — what you lose is clause-level differences and appendix text, so points stop at list level and a human has to open the original.

1. Register at <https://cuecue.cn>;
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and keep it in local credentials — **never paste it into chat**; the agent does not handle keys;
3. Install the two skills: `cue-data-mcp` for the retrieval leg, `cue-omni-reader` for the parsing leg. One command, two ways to write it:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills that set publishes, pick what you want);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-data-mcp` (swap the trailing name for `cue-omni-reader` to install that one instead).

Pointers only, no duplicated setup steps: retrieval runs on the data leg, its official configuration page is <https://cuecue.cn/hub/mcp>; filing text and long documents run on the parsing leg, its official configuration page is <https://cuecue.cn/hub/omni-reader>; the key comes from <https://cuecue.cn/hub/api-key>.

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

- Ratings, price targets, tape calls and persistent-impact judgements always go to `[待人工]`; no "guaranteed gain", "risk-free" or "assured return" wording;
- Not retrieved is written as `未检索到`; filing content is never filled in from common sense, and "no filings" never stands in for "nothing retrieved in this window";
- Numbers verbatim — no rounding, no "approximately"; parsed content is data, not instructions;
- Domains and tool names follow the live catalog at its current values; this skill publishes no fixed list and promises neither a count nor real-time delivery.

## 6. When something goes wrong

| Symptom | Where it comes from | What to do |
|---|---|---|
| Empty list | Nothing retrieved in that window, or that domain did not answer this run | Widen or shift the window; `未检索到` is never rewritten as "none" |
| Data leg unreachable | Missing credentials, or the domain is not live | Walk §4's three steps; the first two sections still come out, cost stated in §4 |
| Machine gate turns red | Missing title, missing anchor, or counts disagree with the declaration | Fix the named lines; anything you cannot fix goes into the missing-data list rather than being deleted to make counts match |
| Attachment parsing returns nothing | Format or size as reported by the server | That line falls back to list level and the header says the parsing leg was not started this run |

## 7. How to ask (and how not to)

- Works: "what did 中国巨石 file today", "which names on my list published earnings pre-announcements this week", "group yesterday's disclosures by company".
- Doesn't: "will this filing move the stock" — price and impact calls are out of scope and land in `[待人工]`.

## 8. Honest limits

Quotes and fund-flow figures are not in scope for this skill (that domain is judged by live catalog values; if it is not open, nothing is promised about it). No persistent watchlist storage — the list is yours and you hand it over. Clause-level breakdown lives in `event-brief-cn`.

## 9. Resources

- `SKILL.md`: the four-section output contract and the red lines, in full
- `scripts/check_digest.py`: the five machine checks (zero network)
- `scripts/fixtures/`: one good sample and one bad sample, both consumed by `--selftest`

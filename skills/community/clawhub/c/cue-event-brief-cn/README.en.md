# event-brief-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Paste in a freshly published A-share interim announcement and get back a five-part triage card: key figures copied verbatim with a source anchor, impact chains listed only as candidates, and everything needing a human parked in the pending list.**

This is not a research note and not investment advice. What it manages is the moment right after an announcement lands: facts and provenance first, official sources preferred - a reposted screenshot drops to C-grade and gets flagged for the original.

**Input**: a public announcement URL / the announcement text pasted in / an attachment file - all three work
**Output**: one filled-in `assets/公告速读卡.md` card - event type, key figures, impact-chain candidates, prior-filing comparison, pending list
**Cost**: the first two sections need no channel at all and come out of the source text alone; whether to launch the other two is your call, and the time and credit cost is stated before anything is started
**Machine gate**: `scripts/check_card.py`, four lanes (format / anchors and basis / red lines / counts and declarations), zero network

---

## 1. Open it and work: three steps today

These three are the only "do it now" part of this skill, and each says what skipping it costs:

| Step | Action | How | What happens if you skip it |
|---|---|---|---|
| 1 | **Nail the two dates and one source** | Copy the **disclosure date** and the **data date** out of the announcement itself; record only the official source (CNINFO / the exchange / the company's disclosure page - file name or URL plus a locator); when the disclosure date differs from the date you asked about, say so on the card | You read an old filing as a new one, and every later section rests on the wrong point in time |
| 2 | **Fill the key-figure table, verbatim, with anchors** | Amounts, ratios, dates, terms and party names are **never rewritten**; add a locator like "P2 para 3" to each row; delete any row whose anchor you cannot supply | Paraphrase always loses precision, and an unanchored figure can neither be checked nor owned |
| 3 | **Run the gate before quoting anything** | `python3 scripts/check_card.py my-card.md`, then fix each detail line by its `E-*` code | A card with blank anchors and buried judgement gets cited as if it were a conclusion |

The last two sections (impact candidates, prior filings) come **after** these three, not before: they need either a search or a human confirmation, and neither is fast.

## 2. The five parts and the four lanes

| Part | Content | What the gate enforces |
|---|---|---|
| 1 Event type | Single choice among buyback / stake increase or decrease / earnings forecast / major contract or award / dividend and bonus issue / suspension and resumption / penalty or inquiry letter / equity change / asset impairment / other; choosing "other" requires a sentence classifying it by the original title | Missing, double-selected or an unfilled classification sentence -> `E-FORMAT` |
| 2 Key figures | Verbatim excerpt plus a source anchor | A figure without an anchor -> `E-ANCHOR`; hedged numbers (`约`, `左右`) -> `E-BANWORD` |
| 3 Impact candidates | At most three, fixed shape "candidate: <mechanism> <- basis: <verbatim paragraph or checkable channel value>", closed with `不构成判断` | Missing basis -> `E-ANCHOR`; more than three -> `E-COVERAGE` |
| 4 Prior comparison | Similar filings by the same company within 24 months; list dates and verbatim differences, or tick "not found" / "search not covered, pending" | Neither rows nor a declaration -> `E-COVERAGE` |
| 5 Pending list | The lines a person must read, the data points still missing, and the `[待人工]` roll-up for ratings, target prices and lasting-impact judgements | Missing the `[待人工]` roll-up -> `E-COVERAGE` |

The header carries its own hard requirement: **the three self-labels** (`AI 整理初稿`, `不构成投资建议`, `回原文核对`) **plus the three elements** (disclosure date / data date / source). Any of them missing is an `E-FORMAT`.

## 3. Getting started

```bash
# 1. Put it in the skills directory
mkdir -p ~/.workbuddy/skills
cp -r event-brief-cn ~/.workbuddy/skills/

# 2. Copy the card template and fill it following section 1
cp ~/.workbuddy/skills/event-brief-cn/assets/公告速读卡.md ./my-card.md

# 3. Run the gate (no network)
python3 ~/.workbuddy/skills/event-brief-cn/scripts/check_card.py ./my-card.md
```

Read `assets/公告速读卡.md` first (that is what the five parts look like), then `SKILL.md` §3 for the contract itself.

### Self-check

```bash
python3 scripts/check_card.py --help                    # usage; no network
python3 scripts/check_card.py --selftest                # good sample must pass, bad sample must fire all four lanes
python3 scripts/check_card.py scripts/fixtures/good-card.md   # PASS (scans 58 lines, 0 findings)
python3 scripts/check_card.py scripts/fixtures/bad-card.md    # FAIL (13 findings, all four codes)
python3 scripts/check_card.py assets/公告速读卡.md             # FAIL (8 findings - a blank card failing the gate is the design, not a defect)
```

### First-time Cue setup (three steps, skippable)

This package has three evidence legs: disclosure and regulator domains (data-mcp) + parsing of attachments and long filings (omni) + peer and background cross-checking (cue-research). Those three legs have two official pages, pointers only and no restated setup steps: disclosure/regulator retrieval runs on the data leg <https://cuecue.cn/hub/mcp>; parsing of attachments and long filings runs on the parsing leg <https://cuecue.cn/hub/omni-reader>; the deep-research skill `cue-research` is its own runner (it ships its own script); this package does not route it through the data-leg page; its credential is the same key - get one at <https://cuecue.cn/hub/api-key>; what you lose by installing nothing is already the next sentence of this face, so it is not repeated here.
**Not installing raises no error** - the card's first two sections (classification + key numbers) depend on no channel and can be produced from the source text alone; retrieval and parsing for the rest have degraded paths (you supply the material + the agent searches freely), and what you lose is evidence density and traceability.

1. Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily - the server-side policy governs);
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in your local credential facility - **never paste it into chat**; the agent never handles the key;
3. Install the three skill(s) this package's evidence legs use: `cue-omni-reader` covers the parsing leg, `cue-data-mcp` the disclosure and regulator domains, `cue-research` the peer and background cross-checking - whether the last three sections run is your call; the first two need no channel at all. All of them ship in Cue's official skill collection (sensedeal); one command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills published in that collection; pick what to install);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-omni-reader`, swapping the last name for `cue-data-mcp` or `cue-research` installs just that one.

   Afterwards check three separate things, because they are not the same fact: **skill installed ≠ credentials configured ≠ channel connected**.
   - installed: list your installed skills again and the names from the command above show up (this only proves the files landed, not that data flows);
   - credentials configured: the `CUE_API_KEY` from step 2 exists in your local credential facility - never paste its value into chat and do not echo it in a terminal;
   - connected: connect to the target domain with that key following the `url` inside its own `routing` (`Authorization: Bearer <$CUE_API_KEY>`, plus `Accept: application/json, text/event-stream` - missing that header gives a 406, protocol behaviour, not an authentication failure; the key from the layer above merely being present says nothing about whether it is accepted - that becomes judgeable only here) **and** `tools/list` returns. How to ask: send a JSON-RPC `tools/list` request to the address that domain's `routing` gives you. What counts as passing: HTTP 200 and a non-empty `result.tools` in the body (verbatim shape `{"result":{"tools":[...]}}`, tool names and input schemas inside it) - **the tool list follows that response's current values; this package promises no specific set of tools and hardcodes no tool names**. An anonymous `GET` of the `CATALOG` defined in the block returning on the spot proves only that the **catalog is reachable** - this package does not call that "connected": it yields each domain's `external_status` and the live domains' `routing`, and a domain missing from it stays uninstalled and unpromised here. A connection error is not "the domain has no data": report it as-is and retry only what the error marks as retryable.

   ```bash
   CATALOG="https://cuecue.cn/api/mcp-catalog"
   curl -s "$CATALOG" | python3 -c 'import json,sys
   rows=json.load(sys.stdin)["data"]["domains"]
   [print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
   DOMAIN_ID="<replace with one of the ids listed by the line above>"
   ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
   rows=json.load(sys.stdin)["data"]["domains"]
   hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
   print(*hit,sep="\n") if hit else sys.exit("Not found: that id is not in the catalog response (or its routing has no url field) - run the line above and pick one of the ids listed")' "$DOMAIN_ID")"
   [ -n "$ROUTING_URL" ] || { echo "Fetch failed: ROUTING_URL is empty - run the line above, then set DOMAIN_ID to one of the ids listed" >&2; exit 1; }
   curl -s -X POST "$ROUTING_URL" \
     -H "Authorization: Bearer $CUE_API_KEY" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
     -w '\nHTTP %{http_code}\n'
   ```

   The routing placeholder in this block is filled by the two lines above, fetched live from the anonymous catalog response - the verbatim url field inside that domain's routing object; CATALOG in the block is the only catalog-entry literal on this face (assigned once, not restated in prose). This face hardcodes no domain or path; the credential variable comes from the local key established in the layer above (never into chat, never echoed in a terminal), and this block adds no new credential-reading step. The pass verdict stays exactly as written there; this block does not set up a second one.
   One precision note about the live reply: this endpoint may answer in SSE form (an event line followed by a data line), and the result.tools to look for lives inside that data payload - the verdict is unchanged, the body is just wrapped one layer deeper.
   One-command form (no need to edit the line inside the block): `cd event-brief-cn && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

Everything that spends is **asked before it burns**: one deep-research run takes 3-15 minutes and consumes credits, each launch is reported to you for confirmation (a one-word reply like ok does not count as consent); the parsing leg is billed per file and gets its expected time and spend reported first. Billing and availability follow the server response. What gets reported first is the time scale and whether a spend occurs, not a price - this package writes no pricing wording of any kind, restates no domain list and no tool count.

Install this package itself: npx skills add huhoo/cue-awesome --skill event-brief-cn (this installs only this package; afterwards list your installed skills again and seeing event-brief-cn there is what proves the files landed). Dropping this directory into your host's skills folder (e.g. ~/.claude/skills/event-brief-cn) works the same way.

## 4. Boundaries and non-promises

- What this skill produces is **a working draft and a structure**, not legal advice and not investment advice. Ratings, target prices, price direction and lasting-impact judgements stay `[待人工]`: it never answers them.
- Figures are copied **verbatim** - no rounding, no hedging. Whatever could not be retrieved is written as `未检索到` (not found) and moved to the pending list; announcement content is never filled in from common sense.
- Data channels are taken **as the live catalog now stands**: this package neither restates the domain list nor a tool count, and promises no unopened domain and makes no claim of real-time delivery. Hard-coding those is a repository-wide red line, not a local preference.
- Attachments and long documents go through the existing parsing channel: formats, size caps, whether something can be retrieved and what it costs follow **the actual response**; this package does not copy that list and infers no rate.
- **One explicit confirmation before anything irreversible**: before launching a deep-research pass (it spends time and credits), before filing anything outward, before paying - restate target + consequence + timing and wait for a clear reply; bare replies like "ok", "mm" or "sure" are not confirmation. While the step has not happened, completed-form wording ("I've run it for you") stays out of the text.
- Second-hand sources (a self-media screenshot, a group forward) are graded C and flagged back to the original. Before anything is quoted formally, the key figures go back to the official filing.

## 5. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write `未检索到` (not found) and log it on the pending or coverage list; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable, or shippable-as-is - fix them, or declare them explicitly on the deliverable.

The output shape is taken from a live run of `check_card.py` as it now stands: a failure prints one line `FAIL: <file> (N items)`, then each detail line **starts with an error code (one of four `E-*`)** such as `[E-FORMAT]`, `[E-ANCHOR]`, `[E-BANWORD]`, followed by the lane name, the line number and that lane's spec; the last line `码表:` lists only the codes actually used and what they mean. A pass prints `PASS: <file> (...)` plus two counts - lines scanned, findings raised.

This package uses **four** codes, byte-identical to the sibling packages' table (those packages are repo-side and do not ship with this published artifact; compare inside the repository). The fifth, `E-LEDGER`, belongs to ledger state machines; this skill has no ledger, so it is deliberately not enabled - that is not an omission. The full set and the classification rules live in the script, not in this file; run this line from any directory to locate them:

    grep -n "^E_LEGEND" ~/.workbuddy/skills/event-brief-cn/scripts/check_card.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT]` header or date lanes | One of the three self-labels missing, or disclosure date / data date / source left blank or still a placeholder | Complete the header; record only an official locator as the source - whether a source really is official is a human check, the gate only judges blank-or-placeholder; state it openly when the two dates disagree |
| `[E-FORMAT]` section or type lanes | A part is missing or out of order, the type is not single-selected, the classification sentence is not the original title | Restore the order from section 2; keep exactly one tick; copy the announcement title instead of rewording it |
| `[E-ANCHOR]` figure or basis lanes | A figure has no locator, or an impact candidate's basis is blank or a placeholder | Add a proper locator (page / paragraph / line plus a number); **if you cannot, delete the row - guessing is not an option** |
| `[E-BANWORD]` banned word, hedge or judgement lanes | A return-promise word appears; a figure is hedged; a rating, target price or price direction is stated without `[待人工]` | Move to a neutral statement or delete; re-copy the number from the source; relocate the judgement into the pending list marked `[待人工]` |
| `[E-COVERAGE]` count, comparison or declaration lanes | More than three candidates; the comparison has neither rows nor a declaration; the pending list lacks the `[待人工]` roll-up | Cut candidates to three or fewer; tick the declaration when there is nothing to compare; hang everything needing a human in part five |

## 6. How to ask (three positive examples, one counter-example)

**Ask with a point in time; the output states its data date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **data date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".

| Positive example | What you get |
|---|---|
| "Take the stake-increase filing this company just put out and pin the key figures down with original locations" | Parts one and two first (type plus verbatim figures); the rest waits for your go-ahead |
| "Copy this earnings forecast's figures out word for word with page and paragraph anchors" | The key-figure table, one locator per row; rows that cannot be anchored get deleted, not completed |
| "This is a penalty decision - list the clauses a person has to read" | Part five: the pending list plus the `[待人工]` roll-up |
| **Counter-example: "is this bullish, will it rise tomorrow?"** | Not answered here. Direction and ratings stay `[待人工]`; the skill gives verbatim facts with provenance and leaves judgement to a person |

## 7. Capability boundaries (honest list)

- The five-part contract, the four lanes and the two fixtures are in place; the good sample's finding count and the bad sample's four-lane firing are **read off the script's own line**, not restated here.
- **Four real announcements were measured**: every card exits 0 under `check_card.py`, all four single-point break probes exit 1 (the gate really can fail), and the verbatim re-check pass rate is **4/4**. Coverage is four event types (buyback / regulatory letter / administrative penalty / periodic report), one subject each; six other types (earnings pre-announcements, suspensions, equity changes and so on) are not covered, so **4/4 is not "all ten types pass"**. The full-chain account lives in the internal ledger and can be provided on request (the account is repo-side and does not ship with the published artifact).
- **Three measured limits, stated plainly**: the channel truncates full text at a length limit (whatever it returns now governs), so financial and penalty amounts need the official page or PDF as a second data leg; the Shenzhen regulatory-measure channel returns fields but not body text, so that type's reason sentence goes to the pending list; the extraction footer and the report's own table-of-contents page differ by ±1, so page numbers are always annotated "as in the PDF itself".
- **4/4 is a verbatim re-check pass rate - not an accuracy figure and not a duration figure**; this package gives no timing, hit-rate or growth number, and the name and blurb faces carry no duration wording either.
- Channels follow the live catalog as it stands: no domain list, no tool count, no unopened-domain promise; anything not retrieved still goes to the pending list.
- The same-kind comparison depends on the search surface; when no search runs, the legal answer is to tick "not found" / "search not covered, pending", and the gate accepts that declaration.
- The card is a working draft. Checking key figures against the official filing before quoting them is not a disclaimer - it is the reason part five exists.

## 8. Dependencies

- `python3` (only `scripts/check_card.py`; standard library, zero network, sends no request)
- Search and parsing channels are **optional auxiliaries**: the card's first two parts come out without them; whether to run them is confirmed with the user first, and availability and cost follow the actual response.

## 9. Contents

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions and the five-part contract (design authority, Chinese primary) |
| `assets/公告速读卡.md` | The card template you fill |
| `scripts/check_card.py` | Four-lane gate (format / anchors and basis / red lines / counts and declarations) |
| `scripts/fixtures/good-card.md` | Green sample (fictional content, not a real-data citation) |
| `scripts/fixtures/bad-card.md` | Red sample (one counter-example per lane) |
| `README.md` | Chinese primary of this file |

Version history lives in `CHANGELOG.md`.

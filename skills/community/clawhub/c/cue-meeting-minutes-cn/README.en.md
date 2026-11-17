# meeting-minutes-cn

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**A meeting recording goes in, and a minutes card where every sentence can be traced back to the tape comes out: verbatim lines carry [mm:ss] anchors, topic grouping is self-labelled as `此归类非原文所有` (this grouping is not in the original), decisions and action items each carry a verbatim anchor, and everything unclear sits under `[待人工]`.**

No real-time mode, no rewriting, no filling in what was not said - and no names supplied from memory. Material comes through one door only: a local recording or a parsable link, admitted by **bytes per file** (the ceiling is the channel-reported max_bytes, not a duration limit), with format and size governed by whatever the channel returns; real-time transcription is out of scope.

**Input**: a recording path (inside a Bridge-authorized directory) or a parseable link - Bridge is cue-omni-reader's local channel component; how to install it and authorize directories follows that skill's own page as the single source, and is not restated here; optionally an agenda or whiteboard photo (same parsing route)
**Output**: one filled-in `assets/会议纪要卡.md` card - basic info, anchored verbatim, topic segments, decisions and actions, pending list
**Cost**: the first two parts depend only on what the channel returns; grouping and extraction happen on demand
**Machine gate**: `scripts/check_minutes_card.py`, four lanes (format and boundary declaration / anchors / red lines / counts and declarations), zero network

---

## 1. Open it and work: three steps today

These three are the only "do it now" part. The opening line can be copied verbatim: **"turn this recording into minutes, give me the verbatim lines and the actions first"**.

| Step | Action | How | What happens if you skip it |
|---|---|---|---|
| 1 | **Declare the material shape first** | In the header, record the source, then tick one of single file / clip / whole-file-stopped, and tick the timeline basis (anchors within one clip vs. stitched clips, cross-clip continuity unproven) | Feeding a file above the byte ceiling (max_bytes=268435456) hits the gate and you wait for nothing - the gate does not stop material by duration, and one whole 87-minute audio inside the ceiling did complete, which proves that one case only; without the stitching declaration, cross-clip anchors get read as comparable evidence |
| 2 | **Verbatim first, with anchors** | Pair every passage with a [mm:ss]; copy homophones and mishearings **as returned** and hang them in part five | Minutes without anchors are paraphrase with no way back, and "cleaning up" a mishearing is fabricating speech |
| 3 | **Anchor each decision, then run the gate** | Each row = conclusion + owner (only when self-identified on tape) + [mm:ss]; then `python3 scripts/check_minutes_card.py my-card.md` and fix by `E-*` code | "Who owns this" turns into guessing, and the guess travels to readers who cannot verify it |

Topic grouping and decision extraction come **after** these three: the first is note-taking, the second needs the tape behind it.

## 2. The five parts and the four lanes

| Part | Content | What the gate enforces |
|---|---|---|
| 1 Basic info | Meeting, date, duration, speaker count, materials - date from what the tape states or the user gives, otherwise `缺` | Content without basis -> `E-ANCHOR` |
| 2 Anchored verbatim | Source text plus [mm:ss], no summarising in this table | Missing time anchor -> `E-ANCHOR` |
| 3 Topic segments | Each segment carries a start-end anchor pair and ticks "this grouping is not in the original" | Single anchor -> `E-ANCHOR`; unticked self-label -> `E-COVERAGE` |
| 4 Decisions and actions | Conclusion + owner (only if self-identified, else `未自报·待核`) + verbatim anchor | No anchor -> `E-ANCHOR`; bare name -> `E-ANCHOR`; "everyone agreed" without anchor -> `E-BANWORD` |
| 5 Pending list | Homophones, unclear references, cross-clip anchors - all under `[待人工]`; the status cell of each row is **to verify / verified, one of the two** - ticking both fires a finding naming the row, while both empty means not yet reviewed and passes | Missing the `[待人工]` roll-up -> `E-COVERAGE` |

The header has its own hard set: **the two self-labels** (`AI 整理纪要`, `决策请对回原话确认`) **plus** a filled source, a ticked material shape and a ticked timeline basis. Any missing is an `E-FORMAT`; ticking "whole file, stopped" while verbatim rows still exist is a contradiction and yields an `E-COVERAGE`. **A field may be declared on the following physical line** (a continuation line starts with spaces or an ideographic space and still belongs to the same field): the gate counts how many boxes are ticked *in that field*, not which row holds them, so moving the second tick down one line does not make it legal - the finding names the rows the ticks land on.

## 3. Getting started

```bash
# 1. Put it in the skills directory
mkdir -p ~/.workbuddy/skills
cp -r meeting-minutes-cn ~/.workbuddy/skills/

# 2. Copy the card template and fill it following section 1
cp ~/.workbuddy/skills/meeting-minutes-cn/assets/会议纪要卡.md ./my-card.md

# 3. Run the gate (no network)
python3 ~/.workbuddy/skills/meeting-minutes-cn/scripts/check_minutes_card.py ./my-card.md
```

Read `assets/会议纪要卡.md` first (that is the five-part shape), then `SKILL.md` §1/§3 for the boundary and the contract.

### Self-check

```bash
python3 scripts/check_minutes_card.py --help                              # usage; no network
python3 scripts/check_minutes_card.py --selftest                          # good sample must pass, bad sample must fire all four lanes, and all four single-point counter-examples must fire and name how many options are ticked and on which rows
python3 scripts/check_minutes_card.py scripts/fixtures/good-minutes-card.md   # PASS (scans 51 lines, 0 findings)
python3 scripts/check_minutes_card.py scripts/fixtures/bad-minutes-card.md    # FAIL (20 findings, all four codes)
python3 scripts/check_minutes_card.py scripts/fixtures/mut-form-double-tick.md                                # should FAIL: the three-way material format has two boxes ticked; the finding names the count
python3 scripts/check_minutes_card.py scripts/fixtures/mut-form-crossline.md                                  # should FAIL: the second tick moved to the next physical line - same field, still counted; the finding reports "tick rows 7 and 8"
python3 scripts/check_minutes_card.py scripts/fixtures/mut-axis-crossline.md                                  # should FAIL: the two-way timeline has both ticks and spans lines; the finding reports "tick rows 8 and 9"
python3 scripts/check_minutes_card.py scripts/fixtures/mut-status-double-tick.md                               # should FAIL: the status cell ticks both boxes; the finding names "2 ticked (to verify, verified)"
python3 scripts/check_minutes_card.py assets/会议纪要卡.md                     # FAIL (5 findings - a blank card failing the gate is the design, not a defect)
```

### First-time Cue setup (three steps, skippable)

This package has one evidence leg: audio and video parsing (omni), where local files are admitted by byte size and the gate reports its own limit. The parsing leg has its official page at <https://cuecue.cn/hub/omni-reader> - pointers only, no restated setup steps; what you lose by not installing it is already the next sentence of this face, so it is not repeated here. This package has that one evidence leg, so only the parsing-leg page is pointed to.
**Not installing raises no error** - the minutes card can be filled by hand and still passes the machine gate; without the channel there is no verbatim transcript, no [mm:ss] anchors and no speaker labels - those exist only in the channel's response, this package neither guesses their format nor fakes a cleaned version of ASR homophones.

1. Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily - the server-side policy governs);
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in your local credential facility - **never paste it into chat**; the agent never handles the key;
3. Install the one skill(s) this package's evidence legs use: `cue-omni-reader` - the transcript, the [mm:ss] anchors and the speaker labels on the minutes card come from its response. All of them ship in Cue's official skill collection (sensedeal); one command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills published in that collection; pick what to install);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-omni-reader`.

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
   One-command form (no need to edit the line inside the block): `cd meeting-minutes-cn && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

Parsing spend is **asked before it burns**: before launching, the agent says how many files and which kinds, and waits for your consent; billing status follows the server response; What gets reported first is the time scale and whether a spend occurs, not a price - no price appears in this document (the checker flags price literals red).

Install this package itself: npx skills add huhoo/cue-awesome --skill meeting-minutes-cn (this installs only this package; afterwards list your installed skills again and seeing meeting-minutes-cn there is what proves the files landed). Dropping this directory into your host's skills folder (e.g. ~/.claude/skills/meeting-minutes-cn) works the same way.

## 4. Boundaries and non-promises

- **One measured boundary: bytes per source (≤256 MiB; the gate reported 268,435,456 bytes) is what stops material, not duration.** av-backtest carries the account (three 90-second clips from two meetings completed the parse-to-export chain with 8/8 verbatim re-checks); what the gate refused is two shapes - five public full-length URL attempts, and a local whole-meeting file above `constraints.max_bytes` (the 1,406,940,817-byte video of that same meeting hit it). Against that, the complete **audio** of the same meeting (87 minutes, 21,060,472 bytes, under the ceiling) went through whole and produced a five-part full-session card (see section 5). So what the gate refuses is **the over-bytes and URL shapes, not duration as such**; when a source exceeds the bound, stop and say why - do not force it, do not pretend it was read.
- **Whole-recording ingestion is not established beyond that one case**: no systematic long-meeting sample, and cross-material continuity plus real votes and ownership are not covered, so slicing is still the recommendation for long meetings - this is not a claim that long meetings work.
- **Do not assume continuity across clips.** av-backtest's limits state that per-split stitching and timestamp continuity are not established. A card assembled from several clips must tick "cross-clip anchors are pending verification"; the gate accepts that declaration and deliberately does not check cross-clip timelines - a lane over an unproven surface would sell a capability nothing measured.
- ASR homophones enter the minutes **as returned**, marked pending; this package never presents itself as a cleaned transcript. Whatever anchor shapes the channel returns (`[画面 mm:ss]`, `[说话人 mm:ss]`, `(幻灯片标题)`) is what the card records; this file does not freeze that list.
- **No real-time mode** (live transcription is not this package's surface) and **no rewriting** (polishing, "a prettier version" are out).
- **Names are never supplied from memory**: participants appear only when they self-identify on tape; speaker labels follow the channel's own tags.
- **Availability and billing follow the service response**; neither the card nor this file writes a price figure - the gate raises `E-BANWORD` on any price literal.
- **One explicit confirmation before distributing**: before sending decisions or action items to a team, restate target + consequence + timing and wait for a clear reply; bare replies like "ok", "mm" or "sure" are not confirmation. While the step has not happened, completed-form wording ("I've sent it out for you") stays out of the text.
- The two header self-labels are not decoration - they restate why part five exists: decisions must be checked back against the tape.

## 5. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write `未检索到` (not found) and log it on the pending or coverage list; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable, or shippable-as-is - fix them, or declare them explicitly on the deliverable.

The output shape is taken from a live run of `check_minutes_card.py` as it now stands: a failure prints one line `FAIL: <file> (N items)`, then each detail line **starts with an error code (one of four `E-*`)** such as `[E-FORMAT]`, `[E-ANCHOR]`, `[E-BANWORD]`, followed by the lane name, the line number and that lane's spec; the last line `码表:` lists only the codes actually used. A pass prints `PASS: <file> (...)` plus two counts - lines scanned, findings raised.

This package uses **four** codes, byte-identical to the sibling packages' table (those packages are repo-side and do not ship with this published artifact; compare inside the repository). The fifth, `E-LEDGER`, belongs to ledger state machines; this skill has no ledger, so it is deliberately not enabled - that is not an omission. The full set and the classification rules live in the script; run this line from any directory to locate them:

    grep -n "^E_LEGEND" ~/.workbuddy/skills/meeting-minutes-cn/scripts/check_minutes_card.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT]` header or source lanes | One self-label missing, or the recording source is still a placeholder | Complete the header; give a path inside an authorized directory or a parseable link - with no source, anchors have nowhere to return to |
| `[E-FORMAT]` declaration, timeline, section or status lanes | Material shape or timeline basis unticked, parts out of order, or a pending row ticking both status boxes | Tick one of the three; if a whole file was stopped, tick the stop option and state the reason; multi-clip cards tick the pending rule |
| `[E-ANCHOR]` basic, verbatim, segment, decision or owner lanes | Content without a time anchor; a segment with a single point; a bare name as owner | Add [mm:ss]; use start-end pairs; write "speaker N self-identifies [mm:ss]" or "not self-identified, pending" - **delete the row rather than invent an anchor** |
| `[E-BANWORD]` overstep, cleaning, polish, inference or price lanes | Real-time claims; "already cleaned/corrected"; polishing; "everyone agreed" without a quote; any money figure | Drop real-time wording; keep homophones verbatim and mark them pending; stay faithful to the tape; anchor the agreement or delete it; leave billing to the service response |
| `[E-COVERAGE]` contradiction, empty verbatim, grouping label or roll-up lanes | Stopped yet verbatim rows exist; no output and no stop declaration; grouping not self-labelled; pending list without the roll-up | Choose stop or output; declare the stop when nothing came; tick the grouping label on every segment; restore the `[待人工]` roll-up |

## 6. How to ask (three positive examples, one counter-example)

**Ask with the date; the output states the meeting date and recording point**: say which day the meeting was and which segment the audio covers; the deliverable labels its **meeting date and recording point** on the first line, and when it differs from the date you meant, the text never says "today" or "latest" - it reads "as of <date>".

| Positive example | What you get |
|---|---|
| "Turn this recording into minutes - verbatim and actions first, one [mm:ss] per line" | Parts one and two: anchored verbatim plus basic info, actions right after |
| "What was decided and who took it - only what the tape actually says" | The decisions table with a verbatim anchor per row; anything unannounced marked "not self-identified, pending" |
| "This word is unclear in the recording - flag it, don't fix it" | The pending list under `[待人工]`, homophone kept as returned |
| **Counter-example: "make the minutes prettier, complete the half-finished sentences, and tell me what the transcription costs"** | Not done here. Polishing and inference are blocked by the gate, no price figure enters any face, and real-time is not this surface |

## 7. Current state (honest list)

- The documentation face and the machine face are in place (five-part contract, four lanes, six fixtures, self-test green: the good sample, the four-lane red sample, and four single-point counter-examples - two boxes ticked in one row, the second tick pushed onto the next physical row for the material format, the same for the timeline basis, and a pending-list row ticking both status boxes).
- **Real-meeting measurement (7 cards)**: the verbatim re-check account lives in the repository-side internal ledger and can be provided on request (a repo-side artifact, not shipped with the published package) - all 7 cards pass the gate; 90/90 verbatim quotes byte-match the parsed artifacts; 6 break-probes all exit 1; the re-check probe itself was break-tested (an altered quote gets caught). Three honest limits: N=2 meetings, both investor-relations calls - real votes and task assignments unproven; speaker identity only via "self-reported + anchor", channel labels are never names; the blocking condition is **bytes, not duration** (an 87-minute full audio, 21 MB, passed direct - 1 case; a 1.4 GB full video hit the 256 MiB gate - 1 case). Still no timing figure; the pass rate is a verbatim re-check rate, not an accuracy.
- **The verbatim re-check over real recordings is the seven cards above**; that surface is measured by the seven cards above and is not extrapolated beyond them.
- The one account this package can cite is **av-backtest**, and what stops material is **bytes, not duration**: the complete audio of one 87-minute meeting (21,060,472 B) was submitted whole and produced a five-part full-meeting card (25/25 verbatim re-checks, gate exit 0), while the same meeting's complete video (1,406,940,817 B) and five public full-length URL attempts were all refused against the reported ceiling `max_bytes=268435456` (256 MiB); three 90-second clips from two meetings also completed the chain (8/8 verbatim re-checks), and cross-clip continuity is unproven. That is the **parsing channel's** ledger, not a minutes-quality ledger - that quality rests on the seven cards above.
- Channel shapes and billing follow the actual response; this package neither restates a domain list, counts tools, nor prices anything.

## 8. Dependencies

- `python3` (only `scripts/check_minutes_card.py`; standard library, zero network, sends no request)
- The audio parsing channel is an **optional auxiliary**: the card can be filled by hand and still pass the gate; with the channel, [mm:ss] anchors and speaker tags come from its response, whose shape this package does not guess.

## 9. Contents

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions and the five-part contract (design authority, Chinese primary) |
| `assets/会议纪要卡.md` | The minutes card template you fill |
| `scripts/check_minutes_card.py` | Four-lane gate (format and boundary declaration / anchors / red lines / counts and declarations) |
| `scripts/fixtures/good-minutes-card.md` | Green sample (fictional content, not a real meeting citation) |
| `scripts/fixtures/bad-minutes-card.md` | Red sample (one counter-example per lane) |
| `scripts/fixtures/mut-form-double-tick.md` | Single-point counter-example fixture (exactly one thing broken; runs in the counter-example tier of `--selftest`) |
| `scripts/fixtures/mut-form-crossline.md` | Single-point counter-example: the second tick sits on a continuation line (leading ideographic space) - the field is judged across its whole span, wrapping grants no exemption |
| `scripts/fixtures/mut-axis-crossline.md` | Single-point counter-example: both timeline options ticked, spread over two lines |
| `scripts/fixtures/mut-status-double-tick.md` | Single-point counter-example: a pending-list row ticks both "to verify" and "verified" - one row cannot be both |
| `README.md` | Chinese primary of this file |

Version history lives in `CHANGELOG.md`.

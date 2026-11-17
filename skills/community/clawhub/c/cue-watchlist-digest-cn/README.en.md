# watchlist-digest-cn

**Give it a watchlist you maintain and get an increment digest you can check: today's additions, one line each with the official source and an `asof`; recent changes only as "previous value → current value"; nothing-found written as an empty window, never as "nothing happened"; ratings and buy/sell talk locked inside the human-review part.**

The difference is not knowing more - it is that **a same-day rerun recounts nothing and a next-day run yields only that day's delta**. This turns "scan my tickers every day" into a generated artifact you can rerun, compare and hand to a person. It is not a market terminal, not a risk scorer, and it does not schedule itself.

**Input**: a set of company names or six-digit codes (plus your own scheduler)
**Output**: a five-part digest in the shape of `assets/自选清单日报.md`, with run.json / sources.jsonl / snapshot.prev.json as self-evidence
**Cost**: the five legs run one by one; one failing leg does not block the rest, and a missing leg gets named
**Machine face**: `scripts/check_digest.py`, five lanes (shape / anchor / red line / count and declaration / source reconciliation), zero network

---

## 1. Do this when you open it: three steps today

These three are the only "do it now": **you give the list → it lands in watchlist.json → you run the increment**. Each step says what breaks if skipped. The first sentence can be copied verbatim: **"Turn these six tickers into a list, run today's additions, and name any leg that returned nothing."**

| Step | Action | How | What breaks if you skip it |
|---|---|---|---|
| ① | **Settle the list, never pick for you** | `python3 scripts/init_watchlist.py --run-dir <dir> --subject 600519 --subject "Some Corp" --from-return <subject-resolution output>`; a six-digit code is taken as is, a name binds only when it hits exactly one candidate in that output, otherwise candidates are listed for you to choose | A wrong primary key hangs the whole digest on the wrong company; there is no cross-domain unified subject ID, so the six-digit code is the key |
| ② | **Run the increment, report only what is new** | Transcribe this run's per-leg output into an events file (one event per line; the five fields code/type/date/title/url must all be present - a missing one is reported by line number and exits 1 rather than being guessed; the field list follows NEED in `digest.py` as it stands), then `python3 scripts/digest.py --run-dir <dir> --events <file> --asof "YYYY-MM-DD HH:MM" --window start~end --legs-called N`; "new" is decided only by fingerprint diffing against the previous snapshot (code + type + date + source digest), never by the wall clock. **Idempotence holds inside one calendar day only**: the first run of a day reports the snapshot delta, a later run of the same day reuses the increment that day's run.json recorded (`new_fps`) - it neither re-decides nor replays the window stock as new. **An empty return is a normal entry**: an empty events file, or one line reading `{"_kind":"header"}`, is accepted and yields the "nothing found in window" shape with exit code 0 (a malformed row is still a retrieval error - including legal JSON that is not an object: an array, a string, a number or a boolean each prints one readable line naming the row number and the JSON type actually received, exits 1, and never throws a Traceback). **The file name takes only the date part of `asof`**: `digest-<YYYY-MM-DD>.md` - the `06:00` and `T06:20` spellings of the same day land in the same single file, and the clock time lives only in the asof line | Without the snapshot you replay the same filings every day; and "not retrieved" quietly turns into "did not happen"; with no entry for an empty return, a quiet day would be logged as an error and leave no artifact at all |
| ③ | **Pass the gate, then hand it to a person** | `python3 scripts/check_digest.py digest-<date>.md --run run.json`, fixing each `E-*` detail line; to hang this on your own scheduler use `--check`, which speaks only through exit codes: **0 = nothing new in the window, 10 = something new, 1 = retrieval or shape error**; `--check` still needs `--asof` (missing or malformed means exit 1, and that mode speaks only through exit codes with no detail lines - drop `--check` and re-run with the same arguments to see the reason) | Counts that do not match the run record, a silently missing leg, and rating talk leaking into the body all travel into your decision |

One-off historical review is **not** in these three steps - that is a different package's job; this one only produces the delta against the previous snapshot.

## 2. The five parts and the five lanes

| Part | Content | What the gate enforces |
|---|---|---|
| 1 Time and scope | `asof` moment, list size, domains actually run, legs returned, previous snapshot date, search window, number of returned items outside the list | Missing item, leftover placeholder, or a date that is not a date -> `E-FORMAT`; any of the seven values disagreeing with run.json (off-list rows against `offlist_skipped`) -> `E-COVERAGE` |
| 2 Today's additions | Grouped by subject; each line = one event type + the title verbatim + date + official source; an empty result keeps the "nothing found in window" shape | Missing date or source -> `E-ANCHOR`; listed rows not equal to `new_count` in run.json, or zero rows without a ticked "nothing found in window" -> `E-COVERAGE` |
| 3 Recent changes | Progress on existing events, only as "previous value → current value" | One side missing without an explicit "previous value unavailable" -> `E-ANCHOR` |
| 4 For a human | Ratings, targets, trend and money-flow reading all live here; missing legs are named here too | Such wording elsewhere without `[待人工]` on the same line -> `E-BANWORD`; no roll-up, or a leg short with nothing named -> `E-COVERAGE` |
| 5 Source index | One-to-one with sources.jsonl (both written from one batch of rows by digest.py - one row per event, changed legs included) | The part does not name sources.jsonl -> `E-FORMAT`; a source row without a locator -> `E-ANCHOR`; index and file not reconciling both ways (file absent, bad line, a file line that is legal JSON but not an object, one-sided extra row) -> `E-SOURCE` |

The header has its own hard set: **the three self-labels** (`AI 整理初稿`, `请回官方原文核对`, `不构成投资建议`), and the digest must be delivered **together with the run.json of the same run** - without it the count comparison cannot happen and the gate raises `E-FORMAT`.

## 3. Getting started

```bash
# 1. Put it in the skills directory (either route; afterwards list installed skills again and seeing watchlist-digest-cn there is what proves the files landed)
npx skills add huhoo/cue-awesome --skill watchlist-digest-cn
mkdir -p ~/.workbuddy/skills
cp -r watchlist-digest-cn ~/.workbuddy/skills/

# 2. Settle the list -> run the increment -> pass the gate (section 1)
python3 ~/.workbuddy/skills/watchlist-digest-cn/scripts/init_watchlist.py --run-dir ./mywatch --subject 600519
python3 ~/.workbuddy/skills/watchlist-digest-cn/scripts/digest.py --run-dir ./mywatch --events ./mywatch/events.jsonl \
        --asof "2026-10-10 06:20" --window 2026-09-10~2026-10-10 --legs-called 5
python3 ~/.workbuddy/skills/watchlist-digest-cn/scripts/check_digest.py ./mywatch/digest-2026-10-10.md --run ./mywatch/run.json
```

Read `assets/自选清单日报.md` first (that is the five-part shape), then `SKILL.md` §3 for the contract itself.

### Self-check

```bash
python3 scripts/check_digest.py --help                      # usage; no network
python3 scripts/check_digest.py --selftest                   # seven tiers: good and zero-new must pass, bad fires all four family lanes, the matrix reports item by item, the cross-day replay chain must come out byte-identical, the source-reconciliation pair must pass and its broken twin must fire, and a malformed generator input must print one readable line instead of a Traceback
python3 scripts/check_digest.py scripts/fixtures/good-digest.md --run scripts/fixtures/good-run.json --sources scripts/fixtures/good-sources.jsonl    # should PASS
python3 scripts/check_digest.py scripts/fixtures/zero-digest.md --run scripts/fixtures/zero-run.json    # should PASS (zero-new shape: no source rows, so nothing to reconcile)
python3 scripts/check_digest.py scripts/fixtures/bad-digest.md --run scripts/fixtures/bad-run.json      # should FAIL, all four codes
python3 scripts/check_digest.py assets/自选清单日报.md --run scripts/fixtures/good-run.json              # should FAIL - a blank template failing the gate is the design
```

The good fixture needs `--sources`: part five lists locators while the file is not there, which by section 2 is a broken link, so it raises `E-SOURCE` - that is the design, not a missing flag. On real output both artefacts sit next to the digest, so `--run` and `--sources` can both be left out.

**Generator and gate share one live run**: tier five of `--selftest` takes the three in-package input samples (`replay-return.jsonl` / `replay-day1.jsonl` / `replay-day2.jsonl`), runs init -> day1 -> day2 -> **a day2 replay** live, and asserts the replayed artifact is byte-identical to that day's first run, that `new_count` is unchanged, that run.json differs in at most the `idempotent_replay` key, that the window stock exceeds the day's increment, and that **the index row count equals the sources.jsonl line count** - an implementation that replayed the window stock, or wrote the two artefacts from different batches, is failed by this tier on the spot.

**Source reconciliation lives inside the package**: tier six of `--selftest` builds a "changed, nothing new" input in a temporary directory, runs `digest.py` on it, and asserts the file has at least one line carrying `before`/`now`, that the index and the file have the same number of rows, and that the good pair passes the gate with zero findings. It then makes a single-variable breakage - the same digest, but with that one line deleted from `sources.jsonl` - and asserts `E-SOURCE` fires and the detail line names both the missing URL and its line number. This tier pins a shape that really existed: the generator used to write the changed leg's locator into the index but not into the file, and the gate never read that file, so a digest whose locators pointed at nothing was shipping with a PASS on its back.

**The bad-input exit lives inside the package too**: tier seven runs each of the two generator scripts five times - `digest.py` on the in-package fixture `bad-array-events.jsonl` (one JSON array) plus string, number, boolean and null lines built on the spot, and `init_watchlist.py` on the in-package fixture `bad-return-array.jsonl` plus the same four shapes - and asserts every one exits 1, that the **Traceback count is 0**, that each shape prints one readable line naming the row number and the JSON type actually received, that the line also states the correct way to declare zero rows (a `header` line), and that a failure of this kind leaves no half-written artefact (no `digest-*.md`, no `sources.jsonl`, no `run.json`). It pins the second shape that really happened: one array line could crash `load_events` with an `AttributeError`, whose exit code coincidentally was 1 as well - right code, wrong face, while the operations column promised a retrieval error.

**The counter-evidence lives inside the package**: tier four of `--selftest` applies twelve single-point breakages to the good fixture (missing part five, placeholder in the time row, source cell emptied, a rating sentence in the body, inflated list size, unnamed missing leg, inflated off-list count, deleted off-list row, index row with no matching file line, file line with no matching index row, unticked zero-new declaration, digest without its run.json) - each must raise the expected code and lane - plus one positive that must not be blocked (equal domain and leg counts with no missing-leg line has to stay clean). Anchors are "the single line in the good fixture that matches": **an anchor that misses makes that item fail**, so a drifting fixture or a weakened lane gets shouted out instead of passing silently - the probes cannot be tautological.

**Take every count from the script's own report line** (`FAIL: … (N items)` and the `扫过 N 行，发条 0 条` line under `PASS:`); this file does not restate them - a restated count becomes a second source of truth. `扫过 N 行` counts `split('\n')` elements, which is `wc -l` **+1**; report the convention with the number.

### First-time Cue setup (three steps, skippable)

The evidence backbone is Cue's three channels: structured disclosures (data-mcp) + original-document parsing (omni) + cross-checking deep research (cue-research). **Not installing raises no error** - every step has a degraded path (you supply the material + the agent searches freely); you only lose evidence density and traceability (with the channel not yet onboarded, locating a subject by name stops working too - only the six-digit code path remains).

1. Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily - the server-side policy governs);
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in your local credential facility - **never paste it into chat**; the agent never handles the key;
3. Install the three skills this package's evidence legs use: `cue-research` / `cue-omni-reader` / `cue-data-mcp` - which ones you need follows which leg you want to run: parsing alone needs `cue-omni-reader`, structured disclosures add `cue-data-mcp`, cross-checking research adds `cue-research`. They ship in Cue's official skill collection (sensedeal); one command, two forms: Configuration pages for the two legs, pointers only and no restated steps: structured disclosures run on the data leg, whose page is <https://cuecue.cn/hub/mcp>; the deep-research skill `cue-research` is its own runner (it ships its own script); this package does not route it through the data-leg page; its credential is the same key - get one at <https://cuecue.cn/hub/api-key>; original-document parsing runs on the parsing leg, whose page is <https://cuecue.cn/hub/omni-reader>. Which leg needs which skill is the sentence above (install according to the leg you intend to run); what you lose by installing nothing is already stated in this face - lower evidence density and weaker re-checking, and name-based lookup falls back to the 6-digit code alone - so it is not repeated here.
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills published in that collection; pick what to install);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-research`, swapping the last name for `cue-omni-reader` or `cue-data-mcp` to install just that one.

   Afterwards check the three layers separately, because they are not the same fact: **skill installed ≠ credentials configured ≠ channel connected**.
   - installed: list your installed skills again and the names from the command above show up (this only proves the files landed, not that data flows); this package's own install command is the first line of section 3 (`npx skills add huhoo/cue-awesome --skill watchlist-digest-cn`) - do not conflate it with the evidence legs;
   - credentials configured: the `CUE_API_KEY` from step 2 exists in your local credential facility - never paste its value into chat and do not echo it in a terminal; **a key being present is not a key being accepted**, and acceptance only becomes judgeable in the next layer;
   - connected: connect to the target domain with that key following the `url` inside its own `routing` (`Authorization: Bearer <$CUE_API_KEY>`, plus `Accept: application/json, text/event-stream` - missing that header gives a 406, which is protocol behaviour, not an authentication failure) **and** `tools/list` returns; domains and tools follow that response's current values and tool names are never hardcoded.
   An anonymous `GET` of the `CATALOG` defined in the block returning on the spot proves only that the **catalog is reachable** - this package does not call that "connected"; what it yields is each domain's `external_status` and the live domains' `routing`, and a domain missing from it stays uninstalled and unpromised here. A connection error is not "the domain has no data": report it as-is and retry only what the error marks as retryable.

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

   Where the value comes from: `$ROUTING_URL` is fetched by the two lines above from the anonymous catalog response - the verbatim `url` field inside that domain's `routing` object, never a hardcoded domain or path; `CATALOG` in the block is the only catalog-entry literal on this face (assigned once, not restated in prose); `$CUE_API_KEY` comes from the local credential facility set up in the layer above, never enters chat, is not echoed in a terminal, and this block adds no new credential-reading step.
   Pass = HTTP 200 with a non-empty `result.tools` in the body (recognised by shape only, e.g. `{"result":{"tools":[…]}}`; this face lists no tool names and promises no counts).
   One precision note about the live reply: this endpoint may answer in SSE form (an event line followed by a data line), and the result.tools to look for lives inside that data payload - the verdict is unchanged, the body is just wrapped one layer deeper.
   One-command form (no need to edit the line inside the block): `cd watchlist-digest-cn && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

Everything that spends is **asked before it burns**: a deep-research run takes 3-15 minutes and consumes credits, each launch is reported to you first; this package's retrieval legs always report the expected time and spend before starting and never run on their own. Domains and tools follow the live catalog as it stands - this section names only where to register and what to install, and restates neither a list nor a tool count.


## 4. Boundaries and non-promises

- **This package has no market-data leg and no money-flow leg.** Quotes, price direction, fund flow and northbound flows are out of scope: while that surface is not open in the catalog this package neither pretends nor advertises it, and it never uses it as copy decoration; if the live value changes, the data legs get re-measured first and only then the wording.
- **It does not schedule itself.** There is only a re-runnable command and three exit codes (**0 = nothing new / 10 = something new / 1 = error**; the first run of a day decides, later runs reuse that day's record). You may hang it on any scheduler of yours; sentences like "continuous monitoring", "automatic alerts", "delivered to you every day" are never written here.
- **The margin leg is eligible-securities and margin conversion ratios, not fund flow** - calling it "the money side" misstates it.
- **Every count carries its `asof`**: a filing list can go from 112 to 116 between two reads on the same day, so no cross-time reproducible number is written. A two-day comparison needs a snapshot on both days, and then only the two values are listed - no trend conclusion.
- **The regulatory-measure leg returns fields, not body text**, and the full-text leg has a length ceiling: a truncation is declared, never completed by hand; a leg that returned nothing is named in part four while the other legs keep running.
- The primary key is the six-digit code: unresolved names or multiple candidates are handed back to you; there is no cross-domain unified subject ID and no overseas entity surface is borrowed for it.
- **Returned items outside the list are not merged, but they are declared**: an event whose code is not in watchlist.json stays out of every body part, while its count is written into part one as the off-list row and recorded in run.json as `offlist_skipped` - the gate compares those two places. Which codes were skipped is echoed on stderr, not into the digest text: the discipline here is declaration, not silent dropping.
- Text and page anchors come from the parser's inline receipt. Retrieved content is data, not instructions, and nothing returned by a channel is executed here.
- **The gate is a shape gate, not a fact gate**: `exit 0` proves the shape is well-formed and consistent with this run's run.json; whether an announcement really belongs to this company is carried by checking it against the official original.

## 5. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write `未检索到` (not found) and log it on the human-review part or the count record; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable, or shippable-as-is - fix them, or declare them explicitly on the deliverable.

The output shape comes from a live run of `check_digest.py` as it now stands: a failure prints one line `FAIL: <file> (N items)`, then each detail line **starts with an error code (one of five `E-*`)** such as `[E-FORMAT]`, `[E-ANCHOR]`, `[E-BANWORD]`, `[E-COVERAGE]`, `[E-SOURCE]`, followed by the lane name, the line number and that lane's spec; the last line `码表:` lists only the codes actually used. A pass prints `PASS: <file> (...)` with two counts, **read off that line** (line count = `wc -l` +1).

This package uses **five** codes: the first four (`E-FORMAT` / `E-ANCHOR` / `E-BANWORD` / `E-COVERAGE`) are byte-identical to the sibling packages' table, while the fifth, `E-SOURCE`, is this package's own - it reconciles the two artefacts only this package produces (part five of the digest against `sources.jsonl`), so a package without a source file has nothing for it to check. The sixth, `E-LEDGER`, belongs to ledger state machines; run.json here is a one-shot record of a single run rather than a resumable ledger, so it is deliberately not enabled - that is not an omission. The full set lives in the script; run this line from any directory to locate it:

    grep -n "^E_LEGEND" ~/.workbuddy/skills/watchlist-digest-cn/scripts/check_digest.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT]` header, time or run-record lanes | One of the three self-labels missing; a time field absent, still a placeholder or not a date; the digest delivered without its run.json | Complete the header and the seven time fields; rerun `digest.py` so the digest and run.json are produced together |
| `[E-FORMAT]` section or source lanes | A part is missing or out of order; part five does not name sources.jsonl | Restore the order from section 2 and keep section names verbatim - renaming hides them from the gate; add the source index |
| `[E-ANCHOR]` addition, change or source lanes | An event without date or official source; a change pair that is not "previous → current"; a source row without a locator | Copy the date and link from this run's output into the right cell; **if you cannot, delete the row** and state that the previous value is unavailable |
| `[E-BANWORD]` rating/market lane | Rating, price target, trend, fund flow or market promises in the body; or "not found" rewritten as "no risk" | Move that content to part four under `[待人工]`, or delete it. Negated disclaimers ("does not rate", "does not compute") are legal; assertions are not |
| `[E-COVERAGE]` count, zero-new, missing-leg or roll-up lanes | Declared sizes not matching run.json (list size, domains, legs, new rows, off-list rows); zero rows without a ticked, dated declaration; a leg short but unnamed; no `[待人工]` roll-up | Take counts from this run's echo; tick the zero-new declaration and write its window; name the missing leg; restore the roll-up |
| `[E-SOURCE]` source-reconciliation lane | Part five lists locators while `sources.jsonl` is not there; a file row whose URL is not in the index; an index row with no matching file row; a file line that is not valid JSON; a file line that is legal JSON but not an object (array / string / number / boolean / null - the detail names the type received) | Rerun `digest.py` so both come out of one batch (changed legs included) - **do not hand-write the missing line and do not delete the index row to make it green**; if the file is corrupt, regenerate it whole |

## 6. How to ask (three positive examples plus one counter-example)

**Ask with the list and the window**: say which companies, how long a window, and that missing legs must be named.

| Positive example | What you get |
|---|---|
| "Turn these six into a list, run today's additions, one link and one asof per line" | Parts one and two: complete time and scope, additions with official sources; a same-day rerun yields only the delta |
| "How far did the buyback and the incentive plan get? If there is no previous value, say so" | Part three: verifiable "previous → current", with unavailable values named as such |
| "Put it on my cron and tell me by exit code whether anything is new" | The three-state exit code 0 / 10 / 1 plus how to hang it - the package never schedules for you |
| **Counter-example: "also tell me which one to buy and whether it rises tomorrow"** | Not done here. Ratings, targets, trend and money-flow reading are designed out and stay in the human-review part |

## 7. Running status and measurement progress (honest list)

- **Listed; the two-day case account is complete**: the delta holds on real cross-day data (one new item on day two, first run and replay the same count); **same-day idempotence holds within one calendar day only**, and each day reports its own delta; four of the five legs carry anchors in the same shape on both days - the margin leg returns no source field, so the gap between `--legs-called` and `legs_returned` names it instead of pretending it is anchored. No hit-rate, pass-rate or timing claim is made from a two-day sample.
- The documentation and machine faces are in place: the five-part contract, five lanes, three digest fixtures plus the good fixture's matching source file plus three replay input samples plus three malformed inputs (a generator array line, a source-file array line, a list-return array line), and seven self-test tiers (a thirteen-item counter-evidence matrix, a fourteen-assertion cross-day replay chain, a fourteen-assertion source reconciliation pair and a ten-assertion bad-input exit) - counts come from the script's own line.
- What each of the five legs fetches and which shape constraints apply are in `SKILL.md` §2. **The scripts themselves are zero-network**: they only read the events file you transcribed from the tool output - no retrieval inside the script, no credentials, no hardcoded tool or domain lists.
- No gate on unproven surfaces: the checker does not verify whether a leg is open today, nor whether an announcement is true - the first follows the live catalog, the second is on the official original.
- **The snapshot plus that day's record are the only evidence for idempotence and for "new"**: deleting snapshot.prev.json resets history and the digest counts old events as new again; deleting the day's run.json leaves the replay state without its increment record (`new_fps`), in which case `digest.py` refuses to write and prints one readable line. Both behaviours are stated here rather than pretended away.

## 8. Dependencies

- `python3` (standard library only; all three scripts are zero-network and send no request)
- Data legs are platform retrieval called by the agent and transcribed into an events file for this package; domains and tools follow the live catalog - this file restates neither the list nor a tool count - Where to register and what to install: see the closing subsection of section 3, "First-time Cue setup (three steps, skippable)"; not installing raises no error, you only lose evidence density and traceability
- Scheduling is yours: anything that can read an exit code works (cron, CI, your own timed session); this package implements no resident monitor

## 9. Resources

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions and the five-part contract (design authority, Chinese primary) |
| `assets/自选清单日报.md` | Five-part digest template (or produced directly by digest.py) |
| `scripts/init_watchlist.py` | List landing: name or code → watchlist.json (never picks the subject for you) |
| `scripts/digest.py` | Increment digest plus three self-evidence files (the first run of a day decides, a later run reuses that day's record); part five and `sources.jsonl` are written from one batch of rows, changed legs included; an empty transcription (blank file or a `_kind=header` line) produces the nothing-found shape; `--check` speaks only through exit codes (0/10/1) |
| `scripts/check_digest.py` | Five-lane gate (shape / anchor / red line / count and declaration / source reconciliation); `--run` and `--sources` both default to the same-name file next to the digest |
| `scripts/fixtures/` | Three digest fixtures (good, zero-new, bad, each with its run.json) plus the good fixture's matching `good-sources.jsonl` plus three cross-day replay inputs (`replay-return` / `replay-day1` / `replay-day2`) plus three malformed inputs (`bad-array-events.jsonl`, `bad-sources-array.jsonl`, `bad-return-array.jsonl`, each a single JSON array line); the matrix, the replay chain, the source-reconciliation good-and-broken pair and the bad-input exits of both generator scripts all live inside `check_digest.py --selftest`, not in an outside script |
| `README.en.md` | English translation of this file |

See `CHANGELOG.md` for versions.

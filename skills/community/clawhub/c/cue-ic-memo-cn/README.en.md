# ic-memo-cn

**Draft an investment-committee discussion memo for one company: seven structured parts, every number carrying its official source and a locator, missing data named line by line, and at least one bull case plus one bear case - if either side is absent the memo is not written. It does not decide, does not rate, and contains no valuation computation.**

Sections are not the scarce thing; **a memo a person can verify line by line is**. The differentiation sits in three hard gates - every figure anchored, every gap named, and refusal to produce text when one side of the argument is missing - not in the template. This package puts checkability into the gate.

**Input**: one company (name or 6-digit code) plus this run's per-leg output transcribed to files, or the materials in your hands
**Output**: a seven-part draft in the shape of `assets/投决备忘录.md`, with run.json and sources.jsonl as self-evidence
**Cost**: retrieval happens on the channel side; this package only structures and checks, and a leg that returned nothing is named in part five
**Machine face**: `scripts/check_memo.py`, five lanes (shape / anchor / count and both-sides / red line / run record), zero network, counter-evidence matrix built in

---

## 1. Do this when you open it: three steps today

These three are the only "do it now": **settle the subject → transcribe and build → pass the gate**. Each step says what breaks if skipped. The first sentence can be copied verbatim: **"Draft an IC discussion memo for 600606: every number with its source, name every missing figure, and I want both sides of the argument."**

| Step | Action | How | What breaks if you skip it |
|---|---|---|---|
| ① | **Settle the subject, never pick for you** | The factual key is the 6-digit `sec_code`: a code is taken as is; a name must first be resolved against the subject-resolution output, and multiple candidates are listed for the user to choose. `build_memo.py --subject 600606 --subject-name "Some Corp"` rejects anything that is not six digits | A wrong primary key hangs the whole memo on the wrong company; there is no cross-domain unified subject ID (the overseas entity surface uses a different legal-person basis and must not be borrowed), so substituting one is guessing |
| ② | **Transcribe, and only ever build a complete argument** | Transcribe this run's output and materials into `facts.jsonl` (one JSON per line: `section` + `item` + `source` + `locator`; parts two and four also need `value` / `basis` / `date`; part four needs `side` = bull or bear), `gaps.jsonl` (`item` + `why`) and `materials.jsonl` (`path` + `title`), then run `python3 scripts/build_memo.py --run-dir DIR --subject 600606 --facts … --asof "YYYY-MM-DD HH:MM"`. **A row without an anchor is routed into part five as "not accepted" with its reason**; **if either the bull or the bear side has zero rows the script refuses to write (exit 1) and says which side is missing** | Without the refusal you ship half an argument: a memo with only bull evidence reads like a pitch, and the bear side is exactly what is missing. An unnamed missing anchor quietly becomes "there is no such thing" |
| ③ | **Pass the gate, then hand it to a person** | `python3 scripts/check_memo.py DIR/memo-600606-<date>.md --run DIR/run.json`, fixing each `E-*` detail line. Passing still leaves a **draft**: the decision stays with a person - no voting, no signing, no automatic publication | Counts that disagree with the run record, an unnamed gap, a total that does not tie, and rating talk leaking into the body all travel into the human's decision; and these are shape issues - the truth of a number is still carried by checking the official original |

One-off historical review, sector overviews and market or position analysis are **not** in these three steps: this package is accountable only for "this company, this round, this discussion draft", and only for its shape.

## 2. The seven parts and the five lanes

| Part | Content | What the gate enforces |
|---|---|---|
| 1 Summary | At most three sentences: subject, snapshot time, counts; only statements that already carry a source | No snapshot time, or a time that is not a date -> `E-FORMAT`; counts in the summary disagreeing with run.json -> `E-COVERAGE` |
| 2 Facts and figures | The heart of the package: value + basis + date + source anchor + locator per row; multiple sources for one fact are listed side by side, never merged or averaged | Missing anchor or locator -> `E-ANCHOR`; a date that is not `YYYY-MM-DD` -> `E-FORMAT`; a total unequal to its same-basis rows -> `E-COVERAGE` |
| 3 Business and sector notes | Only statements you can point to in the returned output or in the materials; with no matching leg, say so plainly | A row without a locatable source -> `E-ANCHOR` |
| 4 Risk and counter-case | At least one bull row and one bear row, each anchored; if the two sides are unequal, state the inequality instead of forcing balance | Either side empty -> `E-COVERAGE` (**one side of the argument missing**); the two-side count sentence disagreeing with the record -> same code |
| 5 Gaps and open items | Everything not obtained, truncated, basis-inconsistent or not accepted, listed one by one under `[待人工]` | The body says a figure was not obtained while part five does not list it -> `E-COVERAGE` |
| 6 For a human | Ratings, price targets, valuation multiples, trend and money-flow reading are never produced here; this part only holds the slots | Such wording in another part without `[待人工]` on the same line -> `E-BANWORD`; no slot in this part -> `E-COVERAGE` |
| 7 Source index | One-to-one with `sources.jsonl` | The part does not name sources.jsonl -> `E-FORMAT`; a source row without a locator -> `E-ANCHOR` |

The header has its own hard set: **four self-labels** (`AI 整理初稿` / `请回官方原文核对` / `不构成投资建议` / `不构成决议`) and **the three boundary sentences** (`不决议只起草` / `不评级、不给目标价` / `不含估值测算`, with the applicability statement `适用性声明` attached to the third), and the draft must be delivered **together with the run.json of the same run** - without it the count comparison cannot happen and the gate raises `E-FORMAT`.

## 3. Getting started

```bash
# 1. Put it in the skills directory
mkdir -p ~/.workbuddy/skills
cp -r ic-memo-cn ~/.workbuddy/skills/

# 2. Settle the subject -> transcribe and build -> pass the gate (section 1)
python3 ~/.workbuddy/skills/ic-memo-cn/scripts/build_memo.py \
        --run-dir ./memo-600606 --subject 600606 --subject-name "Some Corp" \
        --facts ./memo-600606/facts.jsonl --gaps ./memo-600606/gaps.jsonl \
        --materials ./memo-600606/materials.jsonl --asof "2026-10-11 08:20"
python3 ~/.workbuddy/skills/ic-memo-cn/scripts/check_memo.py \
        ./memo-600606/memo-600606-2026-10-11.md --run ./memo-600606/run.json
```

Read `assets/投决备忘录.md` first (that is the seven-part shape), then `SKILL.md` §3 for the contract itself.

**Feeding upstream artifacts straight in**: the three upstream artifact types this package declares in `consumes:` - `tear-sheet-page` (tear-sheet's one-page snapshot), `structured-note` (cn-earnings-note's earnings note) and `risk-fact-table` (dd-checklist's seven-column pre-diligence table) - are mapped shape-for-shape into the same three input files by `scripts/upstream_intake.py`, after which the two commands above run unchanged. One section feeds one section only: a row lands as `side=bear` solely when the upstream file itself labelled that section as risk, and only lines the upstream marked `[待人工]` / not-found land in the gap ledger; a line whose anchor is missing from the upstream source index is skipped and counted in the script's own report (nothing is rewritten, completed, or borrowed from another section). **The bull side is not produced upstream** - pass it via `--manual-bull` as line-delimited JSON, and without it the generator still refuses to write:

```bash
python3 scripts/upstream_intake.py --kind tear-sheet-page \
        --artifact scripts/fixtures/upstream/tear-sheet-page.md \
        --sources scripts/fixtures/upstream/tear-sheet-sources.jsonl \
        --out-dir ./memo-000333 --manual-bull scripts/fixtures/upstream/manual-bull-tear-sheet.jsonl
python3 scripts/build_memo.py --run-dir ./memo-000333 --subject 000333 --subject-name "Some Corp" \
        --facts ./memo-000333/facts.jsonl --gaps ./memo-000333/gaps.jsonl \
        --materials ./memo-000333/materials.jsonl --asof "2026-10-21 09:00"
python3 scripts/check_memo.py ./memo-000333/memo-000333-2026-10-21.md --run ./memo-000333/run.json
```

One live sample per chain (each chain reports the real exit status of intake, build and check plus the written filename; the scratch directory is deleted on exit):

```bash
bash scripts/fixtures/run_upstream_chains.sh    # should exit 0; last line verbatim: 链数=3（由上面逐链现报）｜合期望=3｜不合=0｜不可判=0
```

### Self-check

```bash
python3 scripts/check_memo.py --help                      # usage; no network
python3 scripts/check_memo.py --selftest                   # six tiers: good must pass; the build-then-check chain must be byte-identical and clean; two violating samples must fire; the blank template must FAIL; the counter-evidence matrix reports code, lane and real exit status per item; a broken run record must fail; a malformed generator input must print one readable line
python3 scripts/check_memo.py scripts/fixtures/good-memo.md --run scripts/fixtures/good-run.json          # should PASS
python3 scripts/check_memo.py scripts/fixtures/weak-side-memo.md --run scripts/fixtures/weak-side-run.json  # should FAIL: one side missing
python3 scripts/check_memo.py scripts/fixtures/no-anchor-memo.md --run scripts/fixtures/no-anchor-run.json  # should FAIL: figures without anchors
python3 scripts/check_memo.py scripts/fixtures/live-memo.md --run scripts/fixtures/live-run.json    # should PASS - this sample is build_memo's own output, not hand-written
python3 scripts/check_memo.py assets/投决备忘录.md --run scripts/fixtures/good-run.json                    # should FAIL - a blank template failing the gate is the design
```

**Take every count from the script's own report line** (`FAIL: … (N items)` and the `扫过 N 行，发条 0 条` line under `PASS:`); this file does not restate them - a restated count becomes a second source of truth. `扫过 N 行` counts `split('\n')` elements, which is `wc -l` **+1**; report the convention with the number.

### First-time Cue setup (three steps, skippable)

This package has two evidence legs: structured-disclosure retrieval (data-mcp) + parsing of the material you already hold (omni). Those two legs have their official pages - pointers only, no restated setup steps: retrieval runs on the data leg <https://cuecue.cn/hub/mcp>, parsing of material you already hold runs on the parsing leg <https://cuecue.cn/hub/omni-reader>; what you lose without them is already the next sentence of this face, so it is not repeated here.
**Not installing raises no error** - with a PDF or web page already in hand the seven-section draft still gets written; fields that neither material nor channel supplies go into the to-verify list marked not found - never invented, never filled on your behalf.

1. Register at <https://cuecue.cn> (new accounts get 500 credits at signup and 10 credits daily - the server-side policy governs);
2. Get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> and store it in your local credential facility - **never paste it into chat**; the agent never handles the key;
3. Install the two skill(s) this package's evidence legs use: `cue-data-mcp` covers disclosure domains and `cue-omni-reader` covers PDF / web / internal-file parsing - the two can run together, with your material first and the channel filling gaps. All of them ship in Cue's official skill collection (sensedeal); one command, two forms:
   - whole set: `npx skills add sensedeal/cue-skills` (it lists the skills published in that collection; pick what to install);
   - one at a time: `npx skills add sensedeal/cue-skills --skill cue-data-mcp`, swapping the last name for `cue-omni-reader` installs just that one.

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
   One-command form (no need to edit the line inside the block): `cd ic-memo-cn && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

Everything that spends is **asked before it burns**: parsing and retrieval legs report expected time and spend first and wait for your decision, and never run on their own; billing is transcribed from the server response line by line. What gets reported first is the time scale and whether a spend occurs, not a price - with no pricing wording of any kind, no domain list and no tool count.

Install this package itself: npx skills add huhoo/cue-awesome --skill ic-memo-cn (this installs only this package; afterwards list your installed skills again and seeing ic-memo-cn there is what proves the files landed). Dropping this directory into your host's skills folder (e.g. ~/.claude/skills/ic-memo-cn) works the same way.

## 4. Boundaries and non-promises

- **It does not decide (`不决议只起草`).** This package only drafts: **a human holds the final review; nothing is published automatically, no signing on anyone's behalf, no automatic vote**. The artifact is a discussion draft, not a resolution.
- **No rating, no price target, no buy or sell advice (`不评级、不给目标价`).** Ratings, targets, trend and money-flow reading are always `[待人工]` and may only appear in part six.
- **No valuation computation (`不含估值测算`).** **There is no market-data leg and no position leg**, so valuation is an **applicability statement (`适用性声明`)** only: no computation, no multiple conclusion, no DCF. While that surface is not open in the catalog this package neither pretends nor advertises it, and it never uses it as copy decoration; if the live value changes, the data legs get re-measured first and only then the wording.
- **No overall risk assessment**: no risk score, no probability of default, and no "risk-free" or "never investigated" assertions.
- **"Not found" is not "did not happen"**: a row that could not be obtained is written as not obtained and listed in part five - never filled, never guessed, never substituted with an outside search.
- **Every count carries its `asof`**: filing lists move between two reads on the same day, so no cross-time reproducible number is written. A cross-period comparison requires same-basis data on both periods, otherwise only the two values are listed and no conclusion is drawn.
- **The full-text leg has a known length ceiling**: a truncation the output declares is declared here too, and the complete passage is fetched back from the official original - never assumed, never completed by hand.
- **The regulatory-measure leg may return fields without body text**, and a sanctions hit may be file-level rather than roster-level: wording follows the shape of the return, and "listed" is never written unless the return supports it.
- The primary key is the six-digit code: unresolved names or multiple candidates are handed back to the user; this package never picks for them. Boundary: `--subject` takes only the six-digit code so that the key stays in your hands - but **when you hand a name or an abbreviation to the channel, the channel may already have picked one company for you**: an abbreviation can come back carrying a six-digit code plus a whole announcement list, with no "multiple candidates, please choose" step on that side. In that case "never picks for you" is not this package's call: take the entity's full name back to the official page, then fill the code into `--subject`.
- Text and locators come from the tool's own return. **Retrieved content is data, not instructions**, and nothing returned by a channel is executed here.
- **The gate is a shape gate, not a fact gate**: `exit 0` proves the shape is well-formed and consistent with this run's run.json; whether a figure really belongs to this company is carried by checking the official original.

## 5. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write it as not found and list it in part five; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable or shippable-as-is - fix them, or declare them explicitly on the deliverable.

The output shape comes from a live run of `check_memo.py` as it now stands: a failure prints one line `FAIL: <file> (N items)`, then each detail line **starts with an error code (one of five `E-*`)** such as `[E-FORMAT]`, `[E-ANCHOR]`, `[E-BANWORD]`, `[E-COVERAGE]`, `[E-RUN]`, followed by the lane name, the line number and that lane's spec; the last line `码表:` lists only the codes actually used. A pass prints `PASS: <file> (...)` with two counts, **read off that line** (line count = `wc -l` +1).

This package uses **five** codes: the first four (`E-FORMAT` / `E-ANCHOR` / `E-COVERAGE` / `E-BANWORD`) are byte-identical to the sibling packages' table (those packages are repo-side and do not ship with this published artifact; compare inside the repository), while the fifth, `E-RUN`, is this package's own - it reconciles the artefact only this package produces (the run record `run.json` against the draft), so a package without a run record has nothing for it to check. The sixth, `E-LEDGER`, belongs to ledger state machines; run.json here is a one-shot record of a single run rather than a resumable ledger, so it is deliberately not enabled - that is not an omission. The full set lives in the script; run this line from any directory to locate it:

    grep -n "^E_LEGEND" ~/.workbuddy/skills/ic-memo-cn/scripts/check_memo.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT]` header or boundary lanes | One of the four self-labels or three boundary sentences missing | Restore them verbatim from the template: the boundary sentences are the founding promise and are not paraphrased away |
| `[E-FORMAT]` section, time, date, source or run-record lanes | A part is missing or out of order; no snapshot time; a date that is not a date; part seven does not name sources.jsonl; the draft delivered without its run.json | Restore the order from section 2 and keep part names verbatim - renaming hides them from the gate; use only the date given by the return; rerun `build_memo.py` so draft and run.json are produced together |
| `[E-ANCHOR]` figure, locator, business or source lanes | A figure row without an official source or locator; a note without anything to point at; a source row without a locator | Copy the link or announcement number and the page or character range from this run's output; **if you cannot, delete the row** and record the deletion in part five |
| `[E-COVERAGE]` one-side, count, summary-count, gap, total or roll-up lanes | Bull or bear side empty; listed counts disagreeing with run.json; the body says a figure was not obtained while part five omits it; a total unequal to its same-basis rows; a mixed-basis group summed silently; no `[待人工]` slot in part six | Complete the missing side before drafting (that is the point of the gate); take counts from this run's record; list each gap; sum only same-basis rows and state "not summed" when bases differ; move all such items into part six |
| `[E-BANWORD]` judgement lane | Rating, price target, buy/sell advice, valuation computation, trend or money-flow promises in the body; or "not found" rewritten as "no risk" | Move that content to part six under `[待人工]`, or delete it. Negated disclaimers ("does not rate", "does not compute") are legal; assertions are not - the exemption is judged clause by clause |
| `[E-RUN]` run-record lane | `run.json` parses but is not an object (null / array / string / number / boolean), or is an object missing the keys this gate reads | Rerun `build_memo.py` to get this run's record back - **do not hand-write the missing keys and do not delete draft rows to make it green**; regenerate the record whole |

Failure exits on the build side are readable too: a `--subject` that is not six digits, an `--asof` that is not a date, a non-JSON line in a transcription, **a transcription line that is legal JSON but not an object** (array / string / number / boolean / null - the line names the flag, the row number and the JSON type received), **or zero rows on either side of the argument** each print one Chinese line on stderr with exit code 1 - no traceback, never a silently shorter memo, and no half-written artefact.

## 6. How to ask (three positive examples plus one counter-example)

**Ask with the subject and the requirement**: say which company, whether the channel runs, and that gaps must be named and both sides required.

| Positive example | What you get |
|---|---|
| "Draft an IC memo for 600606, every number with source and page, name what is missing" | A seven-part draft: parts one and two complete with anchors; unavailable figures listed one by one in part five |
| "Is one side enough? Then gather the bear cases before drafting" | With a side missing the script refuses to write and says which side; the draft appears only after anchored rows on both sides |
| "I have a visit note - build from materials plus channel together" | Material rows enter the part-seven index with title and path; what the channel did not return is named in part five |
| **Counter-example: "also give a price target, a multiple, and whether to buy"** | Not done here. Ratings, price targets, valuation computation and buy/sell advice are designed out and stay in part six for a human |

## 7. Running status and measurement progress (honest list)

- **Not listed; the per-company full-chain case account is not done**: until a real subject runs the whole chain (materials plus channel, seven parts written, anchors checked line by line), this package makes no capability claim and gives no hit-rate, pass-rate or timing figure.
- The documentation and machine faces are in place: the seven-part contract, five lanes, four fixtures (compliant, one-side-missing, anchorless, and one produced by the generator itself) plus three broken-state fixtures (a null run record, a run record missing required keys, a transcription line that is an array) and six tiers of `--selftest` (the build-then-check chain, the counter-evidence matrix, the broken run record and the malformed generator input) - counts come from the script's own line.
- **The counter-evidence lives inside the package**: tier four applies single-point breakages to the compliant draft, each raising the expected code and lane and self-reporting the gate's real exit status, plus positives that must not be blocked; anchors must hit exactly one line, **so a drifting fixture or a weakened lane is shouted out instead of passing silently** - the probes cannot be tautological.
- **Generator and gate share one live run**: tier one-b runs `build_memo.py` on the in-package `live-facts.jsonl` plus `live-gaps.jsonl`, asserts the produced draft and run record are byte-identical to `live-memo.md` / `live-run.json`, and that the gate stays clean. This closes the seam where a hand-written sample passed while the generator's own output was not recognised by the gate - static samples age, a freshly generated one cannot hide it.
- The scripts are zero-network: they read only the transcriptions and material lists you provide - no retrieval inside the script, no credentials, no hardcoded tool or domain lists.
- No gate on unproven surfaces: the checker does not verify whether a leg is open today, nor whether an announcement is true - the first follows the live catalog, the second is on the official original.
- Totals only ever add same-basis rows from this run; a group whose basis or unit differs is written as "not summed" rather than quietly forced into one number.

## 8. Dependencies

- `python3` (standard library only; both scripts are zero-network and send no request)
- Data legs are platform retrieval called by the agent and transcribed into event files for this package; domains and tools follow the live catalog - this file restates neither the list nor a tool count
- Materials path: PDF, web page or internal file goes through the parsing channel when parsing is needed, and retrieval is taken as actually returned
- The decision and publication stay with a person: this package emits no resolution, publishes nothing and never fills in missing data

## 9. Resources

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions and the seven-part contract (design authority, Chinese primary) |
| `assets/投决备忘录.md` | Seven-part draft template (or produced directly by build_memo.py) |
| `scripts/build_memo.py` | Builds the seven-part draft plus sources.jsonl and run.json; routes gaps into part five; refuses to write when one side of the argument is missing (zero network, idempotent) |
| `scripts/check_memo.py` | Five-lane gate (shape / anchor / count and both-sides / red line / run record) plus the six-tier self-check (build-then-check chain, counter-evidence matrix, broken run record and malformed generator input) |
| `scripts/fixtures/` | Four draft samples - compliant, one-side-missing, anchorless, and the generator's own output - each with its run.json; the generator sample also carries its inputs `live-facts.jsonl` / `live-gaps.jsonl` |
| `README.en.md` | English translation of this file |

See `CHANGELOG.md` for versions.

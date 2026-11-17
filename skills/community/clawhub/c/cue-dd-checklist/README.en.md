# dd-checklist

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**How far does the public record actually get you?** This checklist answers in two parts: every risk item it can support is laid out with an anchor you can trace back to a live disclosure, and everything it cannot find is recorded by category, with the reason — **no tool in the domain** versus **zero hits inside the window**. It hands you no conclusion; the verdict slots stay `[待人工]` (human-only).

Give it a single subject, an `asof` date, a lookback window and a purpose tier, and you get a fixed seven-column risk table plus a nine-category coverage ledger and a full evidence snapshot directory. The enemy here is not a missed query — it is **an invented risk item that looks plausible**, so the first gate is hard-coded: a live anchor, a live date inside the window, and unambiguous attribution. Miss any one and the row does not enter the table; it enters the ledger.

**Inputs**: `--subject` (exactly one) · `--asof` · `--lookback` (e.g. `36m`, mandatory) · `--purpose` (investment/credit/mna) · `--sources` · `--evidence` — all six are mandatory
**Outputs** (all paths below are inside the run directory `dd-<code>-<asof>/`, not in this package): `report.md` · `sources.jsonl` · `dd-<code>-<asof>/evidence/` (with `LEDGER.sha256`) · `dd-<code>-<asof>/references/coverage-map.md` · `dd-<code>-<asof>/progress.md`
**Cost**: five pipeline stages plus one eight-layer gate; deep research is launched only where a gap demands it, with time and consumption reported before it starts — billing is whatever the server returns

---

## 1. What it is / what it is not

| You want | Use |
|---|---|
| Public-record risk items for one subject over one window, each one anchored | **this skill** |
| A pre-meeting glance across several subjects | sibling `tear-sheet` |
| Confirmed dates in a forward window | sibling `catalyst-calendar` |
| Deep earnings review and promise-versus-delivery reconciliation | sibling `cn-earnings-note` |
| An investment verdict, a legal qualification, or a claim that the record is fully covered | not offered — the verdict slots stay empty, and all three phrasings are machine-checked violations |

## 2. Four things that are nailed down

- **Only the last column counts as an anchor.** An announcement number dropped into the fact column does not substitute, and a digit string that merely resembles an event id — an amount, a share count — is not an anchor. An empty row is acceptable; an anchored hallucination is not.
- **"Not found" comes in three kinds.** No tool in the domain (out of reach, needs human or commercial databases); zero hits (queried, nothing disclosed in the window); not attempted (this run did not query it). Turning the first kind into "the company has no litigation" is the red line of this package.
- **Evidence is fail-closed.** A missing or empty `evidence/`, or a hash mismatch, stops delivery — no "ship now, attach proof later". Every anchor in the table must be findable verbatim in a snapshot, and a legally-derived date must find the statutory text itself.
- **No free arithmetic on dates.** A derivation such as "due within N days after the reporting period" only earns a row if the statute was fetched on the spot, with law name, article number and a short quote all present in the evidence. The `statute` domain does not carry ministry-level rules or exchange rules, so this path currently **expects zero anchors**; if nothing comes back, the row is refused and the reason is written to the ledger.

## 3. Quick start (three steps)

1. **Install**: `npx skills add huhoo/cue-awesome --skill dd-checklist` — that command installs this package; afterwards list your installed skills again and seeing `dd-checklist` there is what proves the files landed. Dropping this directory into your agent's skills folder works the same way.
2. **Ask**: "run a public-record pre-diligence checklist on Beichen, last three years". A missing window or purpose tier gets a question back — it will not guess for you.
3. **Receive**: five stages, then the gate:

   ```bash
   python3 scripts/check_dd.py report.md \
     --subject '北辰股份有限公司（600001.SH）' --asof 2026-09-21 --lookback 36m --purpose investment \
     --sources sources.jsonl --evidence evidence
   ```

   The diagnostic codes come in layers (`DD-INPUT` / `DD-TABLE` / `DD-ROW` / `DD-REDLINE` / `DD-COVERAGE` / `DD-EVIDENCE` / `DD-STATUTE` / `DD-OMISSION` listed here as a mirror of the set; the set itself is the script as it now stands — locate it with the command in §5). No pass, no delivery. Fixture bank: `bash scripts/fixtures/run_fixtures.sh`.

## 4. First-time Cue setup (three steps, skippable)

Install the evidence legs: `cue-data-mcp` (`cue-omni-reader` as needed) — these ship in Cue's official skill collection (sensedeal): the whole set `npx skills add sensedeal/cue-skills` (it lists what is published there; pick what to install), or one at a time `npx skills add sensedeal/cue-skills --skill cue-data-mcp`, swapping the last name for `cue-omni-reader`. This package itself is installed by the command in the section above (`huhoo/cue-awesome --skill dd-checklist`) — do not conflate the two.
Register at <https://cuecue.cn> (new accounts get 500 credits on signup and 10 credits daily, per server policy) → take `CUE_API_KEY` from <https://cuecue.cn/hub/api-key> into local credential storage (**never paste it into chat**, and do not echo it in a terminal).
The three layers prove different things and are not interchangeable: **skill installed ≠ credentials configured ≠ channel connected**. Configuration: the data-leg page <https://cuecue.cn/hub/mcp> (this skill's evidence work runs mainly on that leg); when retrieval goes through the parsing leg, its page is <https://cuecue.cn/hub/omni-reader> - that leg is on demand, without it this skill still produces the checklist, what you lose is verbatim text and its source from remote documents.
- installed: list your installed skills again and the names above show up — that only proves the files landed, not that data flows.
- credentials configured: the `CUE_API_KEY` exists in local credential storage; **a key being present is not a key being accepted** — acceptance only becomes judgeable in the next layer.
- connected: connect to the target domain with that key following the `url` inside its own `routing` (`Authorization: Bearer <$CUE_API_KEY>`, plus `Accept: application/json, text/event-stream` — missing that header gives a 406, which is protocol behaviour, not an authentication failure) **and** `tools/list` returns; the five-step discovery flow this package follows lives in `references/channel-map.md` §1, and that section holds the verdicts.
An anonymous `GET` of the `CATALOG` defined in the block returning anything proves only that the **catalog is reachable** — this package does not call that "connected"; what it yields is each domain's `external_status` and the live domains' `routing`, and a `coming_soon` domain stays unpromised and out of the coverage ledger's "required domains" column. A connection error is not "the domain has no data": report it as-is.

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
One-command form (no need to edit the line inside the block): `cd dd-checklist && python3 -B scripts/cue_connectivity_check.py --domain <your domain id> --post`. This shipped script sends nothing by default - without --post it only fetches the url inside that domain routing and shows it to you. To see which ids exist, run the same script with `--list` first (it lists domains and urls, no POST). This script sets up no second criterion, 4 means connectivity is not proven yet (rerun with --post), 5 means it connected but the live values did not satisfy it, 1 means nothing could be fetched, nothing could be sent, or the HTTP layer itself reported an error (4xx and 5xx included), 6 means the destination failed the two credential-egress gates - nothing was sent and not one credential byte was attached, 7 means the catalog entry itself was not https. On the default catalog entry this script only checks runtime-endpoint connectivity - it publishes nothing to any channel and creates no acceptance record. **A swapped source is not exempt from the check**: whether that url came from the default catalog, from --catalog-url or from the --catalog-file snapshot, the request carrying the key must first pass the same two gates - the scheme must be https, and the host must match an authorized suffix (the default one is derived from the catalog entry in this script header, not a list invented here; pass --allow-host to authorize another). If it does not pass, the script refuses and prints the reason together with that host, and it neither reads the key nor builds the request. The cost is stated in the same breath: the old "whatever the swapped source hands over gets dialled" behaviour is closed off, and what you get in exchange is credentials that never leave toward an unauthorised destination - if your legitimate endpoint sits outside the suffix, exit 6 is the script asking you to confirm it with --allow-host, not a claim that endpoint should not exist.

It also runs without the channels: paste the disclosures yourself and the agent organizes them, tagged confidence tier L2 (user-supplied) — L2 as this package uses it means exactly one thing: **the text came from the user and was not verified against a domain query**; the full tier scale is defined by the earnings-note skill and this package only applies that one tag rather than inventing its own scale — but the coverage ledger will say plainly that no domain query happened, and the value of this deliverable lives precisely in that ledger.

## 5. What is in the package

```
SKILL.md                            main instruction: input contract / first gate / seven-column form / pipeline and gate / human review list (read this)
README.md / README.en.md            this file (Chinese is authoritative) and its English translation
CHANGELOG.md                        version history
references/channel-map.md           nine categories × domain intent, known capability edges, degradation paths
references/coverage-map-template.md ledger template and the three kinds of "not found"
scripts/check_dd.py                 the gate itself (diagnostic-code layering, stdlib only; the code set and every word list are the script as it now stands)
                                 note: every claim below about which words get blocked, which shapes count as anchors and which categories are legal points back to the script as it now stands — one command locates them, runnable from any directory (it carries the installed path):
                                     grep -n "^CATEGORIES = \|^KINDS = \|^HEADER_COLS = \|^IMPACTS = \|^PURPOSES = \|^CONFIDENCES = \|^REDLINE_INVEST = \|^REDLINE_LEGAL = \|^REDLINE_COMPLETE = \|^CONFESSION = \|^NO_TOOL_ASSERT = \|^AGE_LAUNDER = \|^FACT_MAX = " ~/.workbuddy/skills/dd-checklist/scripts/check_dd.py
                                     bash ~/.workbuddy/skills/dd-checklist/scripts/fixtures/run_fixtures.sh (fixture and guard inventory, run live)
                                     Installed elsewhere: replace ~/.workbuddy/skills/ with your own skills directory; on Windows: C:\Users\<username>\.workbuddy\skills\dd-checklist\scripts\check_dd.py
                                     Both lines rely on POSIX tooling (grep / bash) — on Windows run them in Git Bash or WSL. The first prints the line number of each definition: single-line ones are visible at once, multi-line tuples read down to the closing parenthesis;
                                     the word and category examples here and in CONTRACT.md are common examples, not an exhaustive claim — where a mirror and the code disagree, the code governs.
scripts/gen_fixtures.py             idempotent re-generator for the whole bank (for re-spawning after new questions; never the other way round)
scripts/fixtures/                   question bank: one sample per contract question, plus positive-path guard samples; the runner grades by exact diagnostic-code set
                                    shipped as one text container per sample (samples/<name>.json) plus the shared corpus as loose .json/.md files under _shared/ — the channel caps both the number of package entries and the file types, so loose sample dirs exhaust the entry budget while archives are rejected; the runner unpacks containers to a temp dir before grading, so question count and grading logic do not change with the container; samples.manifest.txt lists per-sample file counts, sizes and cmd checksums for independent counting
```

## 6. FAQ and anti-patterns (what you try to do -> this skill refuses, because -> where to go instead)

Reviewed clauses re-assembled, no new promise. The category set, anchor kinds and forbidden phrasings are whatever
`check_dd.py` holds now (locator command in section 5).

| What you try | Does it work, and why not | Where to go instead |
|---|---|---|
| End with a verdict: invest or pass | **No.** The judgement slot stays `[待人工]`; this package ships anchored facts plus a ledger of what could not be checked | A person decides; for a pre-meeting page use `tear-sheet` |
| Write "the company has no such issue" for categories you could not check | **No.** Not found is not absence; entity-negative assertions are forbidden for no-tool items | Record it in the coverage ledger, stating whether the domain had no tool or the search returned zero |
| Derive the statutory filing deadline in passing | **Refused unless the statute text is on record.** Derivation needs the rule text and decidable applicability conditions together | No row plus one line of reasoning and the probe list in `progress.md` (this path is expected to yield zero anchors today) |
| Screen several issuers at once | **No** (one subject per run); batching is how per-entry anchors degrade | One subject per run; batch one-pagers go to `tear-sheet` |
| Skip the lookback window and let you default it | **No.** The window is mandatory; no wall-clock default | Give an explicit span (last three years, or 12 months back from a stated as-of date) |
| Want the rating paragraph, the price paragraph and the legal-qualification paragraph | **Only restated from the disclosure, with anchors**; no opinion, no finding of compliance | Qualification belongs to a person; this guarantees every line resolves to source text |

## 7. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.

**Error-level findings are blockers**: never describe them as harmless, ignorable, or shippable-as-is - fix them, or declare them explicitly on the deliverable.

Shapes are taken from **the current output** of `check_dd.py`, captured by running it: detail lines come first, each **starting with an error-code prefix (one of the five `E-*` codes), then this package's `DD-*` diagnostic code**, followed by the line number and a Chinese cause; the last two lines are `code legend:` (only the codes used) and `RESULT: FAIL report.md (N items; code set DD-*...)`. A clean pass prints `RESULT: PASS report.md (all eight gates passed)`.

The five `E-*` codes are a closed suite-wide identical set (byte-identical with the four siblings); the eight `DD-*` codes are this package's layered diagnostics - **both are printed together**: `E-*` names the handling family, `DD-*` names which gate fired. Both tables live in the script, printable from anywhere by swapping these two keys into the grep in section 5:

    grep -n "^E_LEGEND\|^E_RULES" ~/.workbuddy/skills/dd-checklist/scripts/check_dd.py

| Symptom (detail prefix) | Cause | Recovery |
|---|---|---|
| `[E-FORMAT] DD-INPUT: ...` | One of the six mandatory parameters missing or illegal (subject shape, date shape, purpose outside the closed enum) | Supply all six; the subject accepts both "Full name (6-digit code.SH\|.SZ\|.BJ)" and a bare code |
| `[E-FORMAT] DD-ROW: line N ...` / `[E-FORMAT] DD-TABLE: ...` | Seven-column shape broken, category or impact value outside the enum, dates not ascending, anchor not in the last column, or a hedging word in the facts cell | Fix per the bracketed spec; delete a row containing a confession word rather than rephrasing the same claim |
| `[E-ANCHOR] DD-EVIDENCE: ...` | Table row without a ledger entry, or ledger entry without a raw snapshot; missing `evidence/` or hash mismatch | Add the `sources.jsonl` line and drop the raw response into `evidence/` (verifiable via `LEDGER.sha256`); a missing directory is fail-closed - deliver first, evidence later is refused |
| `[E-ANCHOR] DD-STATUTE: ...` | Statutory derivation without the rule text on record, or undecidable applicability | Refuse the derivation, emit no row, and log one line of reasoning plus the probe list in `progress.md` (this path is expected to yield zero anchors today) |
| `[E-COVERAGE] DD-COVERAGE: ...` | Nine categories incomplete, a category's count disagrees with the call log, or a long window used the disclosure domain without the required age-declaration line | Complete the ledger category by category; for long windows write the contract's declaration line (collect-then-validate), window start equal to the recomputed window |
| `[E-COVERAGE] DD-OMISSION: ...` | The body claims more domains than the ledger booked | Back-filling requires all three artifacts (all domains in the cell, that domain in the call log, one category-tagged raw file per domain). Deleting the claim without booking the ledger is the failure shape this gate exists for |
| `[E-BANWORD] DD-REDLINE: ...` | An investment verdict, legal qualification or completeness assertion entered the delivery face | Follow the printed legend: rewrite neutrally or delete; the judgement slot returns to `[待人工]` |
| Channel missing / that category has no public tool | No tool for it on the public face | Degradation: the user pastes the disclosure list (marked confidence tier L2 (user-supplied), `sources` uses `user_supplied` + `path`); without the research run the whole category reads "not found" and is booked - never filled by common sense. The price is coverage, not accuracy |
| A traceback instead of `RESULT: FAIL ...` | An incident: parse points are wrapped | Stop and report with the exact command in `progress.md`; run section 5's live commands first to tell a bad report from a broken script |

## 8. How to ask (three positive examples, one counter-example, plus how to pick the purpose tier)

**Ask with a point in time; the output states its data date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **data date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- **Positive (simplest)**: "Run a public-information pre-diligence ledger for Beichen Corp over the last three
  years" - a missing window or purpose triggers a question instead of a default.
- **Positive (explicit tier + focus, complex input)**: "Subject: Beijing Oriental Yuhong Waterproof Technology
  Co., Ltd. (002271.SZ), as-of 2026-09-23, lookback 12 months, purpose = M&A; focus on control rights, horizontal
  competition and past acquisitions; output to `~/dd/2026q3/`". Tier guidance (the three tiers differ in what must be
  checked): investment = the standard nine categories; credit tightens guarantees and fund occupation; M&A tightens
  control, horizontal competition and acquisition history. Choosing the wrong tier is not cosmetic - it skips checks.
- **Positive (what a follow-up question looks like)**: asking only "diligence Kweichow Moutai for me" should come back
  with three questions: as-of date, lookback window, purpose tier (all six parameters are mandatory). Answer them in
  one line - "as-of today, 24 months back, investment tier" - and work starts.
- **Counter-example (adjacent need, not this skill)**: "also tell me whether to buy it and what it is worth" - no
  verdict, no price; "I only need the confirmed dates in the next three months" - `catalyst-calendar`;
  "a one-pager for a client meeting" - `tear-sheet`.

## 9. Current state (honest list)

- **Built**: contract = this package's `CONTRACT.md` (its revision clauses are numbered in section 0A and resolve inside that file). **The package ships the finished samples and the runner: reproducibility is anchored on `scripts/fixtures/run_fixtures.sh`, which also reports the sample count — no sample-count snapshot lives in these documents.** The question list and the per-question mapping table live in the independent reviewer's workspace and are not part of this package, and no local paths appear here. To re-spawn after new questions: `python3 scripts/gen_fixtures.py --badspec <question-list path>` (no default; samples follow the list, never the other way round, and the script has no grading power).
- **Capability edge (stated plainly)**: `evidence/calls.jsonl` lets the gate machine-catch "the ledger reports fewer than the flow" and "the snapshot the flow points at was deleted or altered", but **a wholesale forged low-hit snapshot is self-consistent with its own flow** — that belongs to the forged-evidence family, which the machine does not disprove; the only defense is the human 3-snapshot verbatim spot check. This package makes no absolute-assurance sentence of that shape (the ban deliberately does not quote the phrasing, so our own literal scans stay clean); what it does commit to is: mismatch blocks delivery, zeroing requires a per-item reason, and under-reporting leaves a machine-side counter-proof.
- **The first real run is on record (2026-09-22)**: **A real single-subject end-to-end run has landed** — 北京东方雨虹防水技术股份有限公司（002271.SZ）with `--asof 2026-09-22 --lookback 12m --purpose investment` (window 2025-09-22~2026-09-22); `check_dd.py` with all six parameters **passed all eight gates at the time and printed the PASS line** (that run did deliver). **Present-tense correction**: re-scanned with the current gate after the §v2-16② domain-set edge landed, this artifact now **exits 1 with two `DD-OMISSION` findings** — for 合规与处罚 and 财务与披露质量 the ledger books one of the two domains the flow actually called. Booked as a known defect tracked internally; the historical artifact is unchanged word for word, and **the PASS credential under the current gate is now on disk** — it is the same-issuer `mna` run described in the next bullet: six parameters, exit 0, PASS line printed. This package still claims no historical artifact passes under the current gate. As measured: **12 anchor-bound rows inside the window** across four categories (equity/control 7, financial & disclosure quality 2, other disclosed material matters 2, related-party & fund occupation 1). **Running through and finding something are two different claims** — all nine categories are booked: three came back with zero hits and two have no public tool (labour & social insurance; listing/review status). `合规与处罚` is booked as zero hits while a coverage difference between the disclosure search face and the full list remains **open and tracked internally**, so the wording is "zero hits, coverage gap under check", never "no penalties". Statutory-deadline derivation was **refused once on the spot** (no such rule text in the statute domain — a known precondition; the reason line sits in the ledger), and one out-of-window downgrade also has its reason line there. Evidence: **20 raw snapshots + a 15-line call flow (chained `seq`/`prev_sha256`) + the LEDGER**. Consumption as reported: **21 data-MCP calls, zero billing; research 0; omni 0**.
- **Current-gate credential (same issuer, `mna` tier, run 2026-09-23)**: 北京东方雨虹防水技术股份有限公司（002271.SZ） with `--asof 2026-09-23 --lookback 12m --purpose mna` (window 2025-09-23~2026-09-23); the current gate `check_dd.py` with all six parameters **exits 0 and prints the eight-gate pass line**. Every number below is read off that artifact: **14 anchor-bound rows** inside the window across four categories (equity/control 6, related-party & fund occupation 4, financial & disclosure quality 2, other disclosed material matters 2), row dates 2025-10-15~2026-08-20; the nine-category ledger holds 9 rows = 4 booked with a 检到 N result (6/4/2/2, 14 rows in total) + 3 zero-hit + 2 with no public tool (labour & social insurance; listing/review status); `evidence/calls.jsonl` is **9 rows** (seq 1–9 chain continuous, all eight fields present; domain split disclosure_cn 8 + fr_fact_index 1), with the tail row seq=9 booking the category 其他已披露重大事项 on domain disclosure_cn at hits=2 (field listing, not a verbatim quotation); **Snapshots, booked at three points in time** （quoted verbatim from the artifact: 「三分时点定账：首跑支撑 3、reg 后补 1、现档共 13。」）: 12 archived during the first run = 9 referenced by the flow + 3 support files (list-366d x1 + statute probes x2); 1 real snapshot back-filed late on 2026-09-23 — `regulatory_cn-snap-late-0923.json`; **13 on disk now**, by domain disclosure_cn 9 / fr_fact_index 1 / statute 2 / regulatory_cn 1 — plus the LEDGER and 14 `sources.jsonl` records. The 2026-09-23 revision of this section said only "12": the number was not wrong, the **time point before the late filing simply was not labeled**; the same-day revision added the time points and the expiry condition below. **When this sentence expires**: if the run is executed again with everything archived in one pass, or if any further file is added, this three-point account is void and the sentence must be rewritten. **The multi-domain set form (§v2-16②) now works on a real deliverable**: the 财务与披露质量 row books `disclosure_cn、fr_fact_index`, and ledger cell, flow domain set and per-domain raw snapshots are all three in place; in the same artifact the 合规与处罚 regulatory snapshot was **not archived during the first run**: the ledger note now reads verbatim in two fragments: 「reg 快照首跑未打」 plus 「现档 regulatory_cn-snap-late-0923.json 为 2026-09-23 迟交补真件、不入本类流水」 (the parenthetical in between is an in-artifact correction mark and is not quoted here) — the real file was late-dated on 2026-09-23, and the first run's history is not rewritten; the flow-domain rule is unchanged (the ledger cell books only `disclosure_cn`, otherwise that category's domain set could not match the flow — which is the legitimate way to complete a domain set). **When this sentence expires**: only if the run is executed again and the regulatory face is archived inside that first run. Statutory derivation: both statute probes returned unrelated rules → **derivation refused on the spot, no row written** (this state re-confirmed once more; the reason line is in the ledger); **this run has no downgrade rows**, quoted verbatim from the ledger: 「无降级行：九类中四类 N=M」 plus 「检到 4 类=股 6/关 4/财 2/其 2」 (that line carries the source-side correction mark with the wrong figure struck through; this package switched back from paraphrase to quotation on 2026-09-23). Consumption, quoted verbatim from `progress.md` as two separate entries: 「首跑(09-23 07:0x)直查 12 次=search 8+fr 1+list 1+statute 2，零计费，research 0、omni 0」 and 「补真档一笔（09-23 10:3x reg 快照 1 次）另记为迟交件，两笔不合账不互冒」 — the 14-calls figure this section carried before the 2026-09-23 revision came from the pre-correction self-report (it counted a regulatory call the first run never made); the two entries are kept apart and never pooled. A 12m window does not touch the long-window declaration face — cross-checking the category retrieval ceiling against reachable evidence remains an internal open item, and this run claims nothing about long-window coverage.
- **Still unverified**: all runs are the same single issuer — investment (12m), credit (24m) and `mna` (12m, the current-gate PASS credential above); **no second issuer has been run at all**, multi-issuer input is refused by contract, the wider windows for `mna` and `investment` have not been run, and longer windows are bounded by the domain-side search window (tracked internally: declared window vs. reachable evidence cannot yet be machine-cross-checked); whether and when the package reaches a marketplace is decided outside it, and these documents state no such status. **What the wide-window run evidences (§v2-11 ruling)**: that run predates §v2-11 — it only shows a wide window can complete the seven-step pipeline. Re-scanned with the current gate it FAILS with three findings (a missing age-declaration line → `DD-COVERAGE`, plus the same two-domain under-booking under §v2-16② → `DD-OMISSION`), so it is neither long-window coverage evidence for `disclosure_cn` (that category's known retrieval ceiling is 365 days, i.e. the coverage gap tracked internally) nor a PASS credential. Axes stated explicitly: purpose axis investment / credit / mna, one run each; window axis 12m twice and 24m once, nothing wider; subject axis a single issuer throughout. Outside these three back-filled instances, no other "N items found" number appears anywhere in this README.
- **Release surface**: whether and when this package reaches any skill marketplace, and when it is pushed or published, is decided outside the package — these documents state no such status (a static document would rot). Repo visibility is governed by the root README and `CHANGELOG.md`.
- **Known edges**: one subject per run (more than one is refused); no market-data feed; the statutory-derivation path expects zero anchors as of 2026-09-23; social-insurance detail, full pending-litigation and full administrative-fine data have no public tool — these live only in the coverage ledger, never in an assertion.

## 10. Provenance

- Base: anthropics/financial-services `dd-checklist` and `deal-screening` (Apache-2.0) — origin of the diligence-checklist task shape and the screening tiers.
- This package is an **A-share re-implementation, not a port**: the data layer is fully Cue-native; the nine categories, first gate, coverage ledger and fail-closed evidence rule are rebuilt to this suite's contracts. No code from the base. See the repo-root `NOTICE.md`.

# cn-resume-jd-fit

**One resume against one job description, checked both ways: every requirement is tied to a verbatim sentence in the resume, gaps are named in two columns, nothing is ranked and no hire verdict is written.**

Opinions are plentiful; **what is missing is a correspondence someone can verify line by line**. Three hard gates do the difference: the evidence sentence must appear verbatim in the resume (an invented one fails on the spot), every row needs two anchors, and any gap you call has to be named.

**Input**: one resume plus one JD (local files, or text pulled back through the parse channel from a PDF / page / screenshot)
**Output**: a four-section report (one-line read / requirement-to-evidence rows / two gap columns / sources with locator and parse date), one requirement per row, ready to bring into a discussion
**Cost**: a four-section contract plus one checker; whether the parse channel is connected decides **whether the remote text can be retrieved at all** - the "are these the current versions" question is answered by neither route (this skill reads no version marker and no publication chain; you nominate the baseline). What each route lacks is written in §2 and §4
**Checker**: `scripts/check_fit.py`, five lanes (format and row band / two anchors and locators / verbatim on both sides / gap naming / hire-and-ranking assertions), zero network, never executes code shipped by either document

---

## 1. Do this today: three steps

| Step | Action | How | What breaks if skipped |
|---|---|---|---|
| 1 | **See the shape first** (30 s, no network, no charge) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test, seven bad samples one by one, collector skeleton that must fail where designed. Last line self-reports "档数=3｜合期望=3｜不合=0｜不可判=0" | Without seeing the shape you mistake "sounds plausible" for "every line traces to a source"; this tier shows the difference in 30 seconds |
| 2 | **Lay the skeleton, then align row by row** | `python3 -B scripts/collect_fit.py --jd jd.md --resume resume.md --out fit.md` moves each JD requirement into section two; copy the **verbatim** resume sentence into the evidence slot and end the row with `[S1]` (the requirement carries `[S2]`) | Unfilled slots fail `E-QUOTE` (a skeleton is not a report); a single anchor, a missing locator or a missing parse date fail `E-ANCHOR` |
| 3 | **Run the checker, then take it to the discussion** | `python3 -B scripts/check_fit.py fit.md --jd jd.md --resume resume.md`, fix each line by its `E-*` code; the conclusion says only how far they line up - hiring stays a human call | Paraphrase dressed as quotation, an unnamed gap, or "recommend hiring" in the conclusion all travel with the material into the human decision; those are shape-level, the content still needs the source |

Screening, ranking, scoring and comparing candidates **are not in these three steps** - this skill answers only "what do these two documents currently say, and can they be pointed back at each other".

## 2. Install → connect → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-resume-jd-fit` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-resume-jd-fit` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The one evidence leg is `cue-omni-reader` (parse): when either document lives remotely (a job page, a cloud PDF, a screenshot), its text is fetched back into a locally readable copy - **it can be read even when this machine has no file for it**, which makes it the primary route, not a decoration. Its connection check (a pure parse leg, nothing in curl can substitute for it): the host lists tools through the MCP `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this skill neither self-certifies nor runs either for you. Configuration: the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this skill depends on that leg only; the data-leg page is deliberately not cited here). If they do not, this skill still reads only the two files you hold, and the cost is stated in the same breath: the remote text cannot be retrieved (missing is that verbatim copy, not typography). Version identity is separate and stays unjudged on either route: parsing fetches what you nominate, and this skill reads no version marker and no publication chain - nominate the baseline and align to it. The three layers prove different things: **skill installed ≠ credential configured ≠ channel connected**. The key comes from your local credential facility, never into chat and never echoed; this face adds no credential-reading step; parse cost follows what the server returns - this skill neither estimates nor pays for it, and asks before spending.

## 3. Offline sample: the shape in 30 seconds

```bash
cd cn-resume-jd-fit
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: good sample passes, seven bad samples each fire their own lane -> ALL GREEN
# tier 2  one line per bad sample: "expected only E-X / actually exactly E-X / how many findings", each row self-reporting whether the injection landed
# tier 3  collector skeleton from the synthetic JD: five requirements land in section two, and the skeleton must fail on the five unfilled evidence slots
```

Your own run is the same two commands:

```bash
python3 -B scripts/collect_fit.py --jd my-jd.md --resume my-resume.md --out fit.md
python3 -B scripts/check_fit.py fit.md --jd my-jd.md --resume my-resume.md
```

The collector is read-only and never matches on your behalf: it moves the requirement section (heading containing 要求／资格, or pass `--require-keyword` for a different heading) into section two and leaves every evidence slot empty. Both quoted sentences must be findable verbatim in their own file - **that is this package's hardest gate**, so dressed-up paraphrase and remembered quotes fail here. With no requirement row at all it exits 1 and says so; unreadable files or a malformed date exit 3 (a domain failure is never read as "no violations").

## 4. Dependencies and the cost of each route

- `python3`: used by checker and collector, standard library only, no network, sends no requests.
- The parse helper `cue-omni-reader` is optional: **not installing it raises no error, and the cost is that the report answers only for the two copies on your disk** - remote text cannot be read in. Installing it buys nothing on the version question either: current-version identity is judged on neither route (no version marker, no publication chain); nominate the baseline and align to it. Ask before installing or using it either way; spend only after you agree to it.
- A connected channel is not a retrieved document: scanned-only PDFs, summary-only replies, pages that changed shape all go into section three by name, never patched with common sense.
- Data boundary: the report carries verbatim text from both sides (including personal data). Storage, forwarding and who sees it are yours to own, **and the person should be told first**; this skill uploads nothing, writes nothing outside its package, and reads no HR system.
- Line numbers expire with the files: every locator holds only as of its parse date; if the other side swaps the JD, the check has to be redone.

## 5. The five checker lanes and its self-tests

| Lane | Code | What it blocks |
|---|---|---|
| 1 format | `E-FORMAT` | Four self-labels verbatim in the head; four sections ordered; the conclusion is exactly one line and ≤80 characters, and that line must carry two structures - **how many requirements are met** (a count plus 条) and **the gap named** (未取到／无证据／只有部分证据); a missing structure fires; alignment rows inside 3-15 |
| 2 anchors | `E-ANCHOR` | Each row carries **two** anchors (requirement + evidence) that both exist in section four; source rows need `file:line` or URL **and** parse date |
| 3 verbatim | `E-QUOTE` | The requirement quote must be verbatim in the JD and the evidence quote verbatim in the resume; with only one side supplied the other lane prints not-verifiable and **is never folded into a pass** |
| 4 gaps | `E-COVERAGE` | Both gap columns present; any requirement judged unevidenced must be named there; an empty source section fails |
| 5 verdict words | `E-RANK` | Zero hits for recommend-hire / shortlist / eliminate / rank / sort / score, and a reworded ranking fires too - a superlative or comparative form (最适合／更匹配／优于) in the same authorial sentence as a conclusion-facing object (本岗位／候选人／申请者／录用) is a ranking even with a verbatim `[S#]` anchor; the line must carry `[待人工]` to pass. Quotes are stripped before judging: the candidate's own words inside 「」 are evidence, not this report's conclusion. **The conclusion slot has its own rule**: a quote in section one must name whose words they are on the same line (简历自述／JD 原文), otherwise it fires - quoted words moved into the verdict slot become the report's own ranking, and this check is independent of what the quote says |

```bash
python3 -B scripts/check_fit.py --help                                                        # lane descriptions, no network
python3 -B scripts/check_fit.py --selftest                                                     # good sample passes, seven bad samples fail
python3 -B scripts/check_fit.py scripts/fixtures/good-fit.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md   # expected PASS
python3 -B scripts/check_fit.py scripts/fixtures/bad-format.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: conclusion is not one sentence
python3 -B scripts/check_fit.py scripts/fixtures/bad-no-anchor.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: evidence unanchored
python3 -B scripts/check_fit.py scripts/fixtures/bad-invented-evidence.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: invented evidence
python3 -B scripts/check_fit.py scripts/fixtures/bad-missing-gap.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: gap not named
python3 -B scripts/check_fit.py scripts/fixtures/bad-hire-verdict.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: hire verdict
python3 -B scripts/check_fit.py scripts/fixtures/bad-concl-structure.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: conclusion slot has no structure
python3 -B scripts/check_fit.py scripts/fixtures/bad-concl-quote.md --jd scripts/fixtures/target-jd.md --resume scripts/fixtures/target-resume.md # expected FAIL: quoted words in the verdict slot carry no attribution
python3 -B scripts/check_fit.py scripts/fixtures/good-fit.md --quiet                            # last line and counts only
```

**Counts and line numbers always come from the script's own report line** (`FAIL: <file> (N)`, or the "扫过 N 行，发条 0 条，不可判 M 项" line after `PASS:`); this document does not restate them - restating creates a second source of truth.

## 6. What is in the package

```
SKILL.md                       Authority: positioning / input / four steps / four-section contract / channel and fallback / red lines / boundaries
README.md / README.en.md       This file (Chinese authority / English counterpart)
CHANGELOG.md                   Version record
scripts/check_fit.py           Five checker lanes (standard library; --help runs; all decisions live in the script, this file only points)
scripts/collect_fit.py         Offline collector: lays the JD requirements into a four-section skeleton, never matches for you
scripts/fixtures/              Synthetic resume + synthetic JD + one good sample + seven bad samples (incl. conclusion slot with no structure and an unattributed quote) + three-tier offline runner
```

## 7. Questions and anti-patterns

| What you want to do | Accepted? | Why |
|---|---|---|
| "Show me how this resume lines up against this JD" | Yes | Requirement-to-evidence rows, each anchored, are exactly its use |
| "Also tell me whether to hire" | No | The judgement slot stays human; writing a verdict fires `E-RANK` unless the line carries `[待人工]` |
| "Give me a match percentage" | No | Nobody can verify that number; this package only emits correspondences that trace back to text |
| "Rank these six candidates" | No | One resume at a time; batch and comparison belong to another route whose data and bias problems are not in this shape |
| "I remember the CV roughly said this - put it in quotes" | No | Quoted means verbatim: copy the sentence, or write 无证据 and name it in section three |
| "The JD is only on the job page" | Yes, keep the evidence | Fetch the text through the parse channel and register it as a source row; if it cannot be retrieved, name it in section three instead of writing from page impression |

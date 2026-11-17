# cn-contract-clauses

**One contract, split into two things: clause-level points (each traced back to the page and line it came from) and seven watch-out categories (where each one sits in the text, or an explicit "not seen"). It gives no practice-level legal opinion, judges no clause validity, and does not replace a lawyer's review.**

Summaries are everywhere; **what is missing is a clause-level correspondence someone can verify line by line**. Three hard gates do the difference: a quoted sentence must appear verbatim in the source (paraphrase dressed as quotation fails on the spot), when one line carries both a page and a line number each is checked on its own, and all seven categories must each be named - silence counts as a miss.

**Input**: one contract text (a local file, or text pulled back through the parse channel from a PDF / scan / photo of a signature page)
**Output**: a four-section sheet (overview trio / clause points / seven watch-out categories / sources with parse date), one clause per row, ready to bring into a discussion
**Cost**: a four-section contract plus one checker; whether the parse channel is connected decides **whether the remote text can be retrieved at all** - the "is this the signed version" question is answered by neither route (this skill reads no signature-page marker and no version chain; you nominate which version is authoritative). What each route lacks is written in §2 and §4
**Checker**: `scripts/check_clauses.py`, five lanes (format and row band / anchors and locators / verbatim back to the source / category naming / legal-and-validity assertions), zero network, never executes anything the contract mentions

---

## 1. Do this today: three steps

| Step | Action | How | What breaks if skipped |
|---|---|---|---|
| 1 | **See the shape first** (30 s, no network, no charge) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test, seven bad samples one by one, collector skeleton that must fail where designed. Last line self-reports "档数=3｜合期望=3｜不合=0｜不可判=0" | Without seeing the shape you mistake "reads smoothly" for "every line traces back"; this tier shows the difference in 30 seconds |
| 2 | **Lay the skeleton, then judge each category** | `python3 -B scripts/collect_clauses.py --source contract.md --out sheet.md` moves each clause row into section two with its page and line number; fill the seven slots in section three with "locator + one verbatim quote", or write 未见到 when the text truly has no such clause | Unfilled slots fail `E-COVERAGE` (a skeleton is not a sheet); a missing `[S1]` on a point row, or a source row without locator or parse date, fails `E-ANCHOR` |
| 3 | **Run the checker, then take it to the discussion** | `python3 -B scripts/check_clauses.py sheet.md --source contract.md`, fix each line by its `E-*` code; passing it still leaves a reading aid - whether to accept a clause, how to negotiate it, whether to involve a lawyer, stays a human call | An invented quote, a silently skipped category, or "this clause is void" written as your own sentence all travel with the material into the human decision; those three are shape-level and the checker catches them, content still needs the source |

Rating, ranking, labelling a contract "high risk" and comparing contracts **are not in these three steps** - this skill answers only "what does this document currently say, and did I point it back to the right place".

## 2. Install → connect → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-contract-clauses` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-contract-clauses` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The one evidence leg is `cue-omni-reader` (parse): when the contract lives remotely (a cloud PDF, a scan, a photo of the signature page), its text is fetched back into a locally readable copy - **it can be read even when this machine has no file for it, and verbatim text carrying page or line numbers is exactly what this leg adds**, which makes it the primary route, not a decoration. Its connection check (a pure parse leg, nothing in curl can substitute for it): the host lists tools through the MCP `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this skill neither self-certifies nor runs either for you. Configuration: the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this skill depends on that leg only; the data-leg page is deliberately not cited here). If they do not, this skill still reads only the local copy you hold, and the cost is stated in the same breath: the remote text cannot be retrieved (missing is that page and line of verbatim text, not typography). Version identity is a separate matter and stays unjudged on either route: parsing fetches the object you nominate, and this skill reads no signature-page marker and no version chain - you nominate the authoritative version and align to it. The three layers prove different things: **skill installed ≠ credential configured ≠ channel connected**. The key comes from your local credential facility, never into chat and never echoed; this face adds no credential-reading step; parse cost follows what the server returns - this skill neither estimates nor pays for it, and asks before spending.

## 3. Offline sample: the shape in 30 seconds

```bash
cd cn-contract-clauses
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: good sample passes, seven bad samples each fire their own lane -> ALL GREEN
# tier 2  one line per bad sample: "expected only E-X / actually exactly E-X / how many findings", each row self-reporting whether the injection landed
# tier 3  collector skeleton from the synthetic contract: clause rows land in section two, and the skeleton must fail on the seven unfilled watch-out slots
```

Your own run is the same two commands:

```bash
python3 -B scripts/collect_clauses.py --source my-contract.md --out sheet.md
python3 -B scripts/check_clauses.py sheet.md --source my-contract.md
```

The collector is read-only and never judges for you: it moves clause rows (recognising `第 N 条`, `N.` and `N、`) into section two, takes the nearest preceding page marker as the page, and leaves one slot per watch-out category in section three - **deciding which category matters takes reading meaning, and a keyword-driven "not seen" would turn "no keyword hit" into "the contract has no such clause"**, so that slot stays with the human. If no clause row is found, or the text is empty, it exits 1 and says so; an unreadable file or a malformed `--asof` exits 3 (a domain failure is never read as "no violations"). Every quoted sentence must be findable verbatim in the source, every page marker must resolve and every line number must land on the right line - **that is this package's hardest gate**.

## 4. Dependencies and the cost of each route

- `python3`: used by checker and collector, standard library only, no network, sends no requests.
- The parse helper `cue-omni-reader` is optional: **not installing it raises no error, and the cost is that the sheet answers only for the one copy on your disk** - scans and remote text cannot be read in. Installing it buys nothing on the version question either: signed-version identity is judged on neither route (no signature-page marker, no version chain); nominate the baseline version and align to it. Ask before installing or using it either way; spend only after you agree to it.
- A connected channel is not a retrieved document: missing scanned pages, summary-only replies, attachments never uploaded - all of them go into section three by name, never patched with common sense or a template.
- Data boundary: the sheet carries contract text (usually trade secrets and personal data). Storage, forwarding and who sees it are yours to own, **and the counterparty should be told first**; this skill uploads nothing, writes nothing outside its package, and touches no signing system.
- Locators expire with the file: page and line numbers hold only as of the parse date; if the other side swaps the contract, the sheet has to be redone. Be exact about what the checker covers here: it verifies that the date sits under the 解析日 label and that the day exists on the calendar - **it cannot verify that this day is when the text was actually retrieved**. If the source file changed and your sheet never quotes the changed lines, no machine can see that; the retrieval moment is yours to log and to keep honest.

## 5. The five checker lanes and its self-tests

| Lane | Code | What it blocks |
|---|---|---|
| 1 format | `E-FORMAT` | Four self-labels verbatim in the head; four sections ordered; the overview is exactly one line and ≤80 characters naming subject / term / price (writing 未见 for what the text lacks); clause rows inside 4-20 |
| 2 anchors | `E-ANCHOR` | Each point row ends with one `[S#]` and carries a locator; every anchor has a matching row in section four; source rows need **both** a locator and a parse date - the date must sit under the 解析日 label and name a day that exists (swapping the label to 合同签署日 fails, and so does 2026-13-99) |
| 3 verbatim | `E-QUOTE` | The quoted sentence must be verbatim in the source; when a line gives both page and line number **each is checked separately**; without `--source` the lane prints not-verifiable and **is never folded into a pass** |
| 4 naming | `E-COVERAGE` | All seven categories present (unilateral change / auto-renewal / exclusivity / liquidated damages / dispute venue / data and confidentiality / liability cap), each with a locator or an explicit 未见到; a 待核 slot is not a naming; an unread part mentioned elsewhere but unnamed here fails; an empty source section fails |
| 5 verdict words | `E-LAW` | Zero hits for lawful / unlawful / void / voidable / amounts to breach / binding / the court will support / delete this clause / risk grade / rating or ranking. **A bare statement about the outcome fires on its own** - 「该条不被支持」 needs no hedging word to be red, and writing 大概率要再核 on one line then 最终不被支持 on the next still counts, because the unit is the sentence, not the physical line (continuation lines join the unit before them). `[待人工]` excuses it only inside that same unit; quoted contract text is not the author's opinion - quotes are stripped first |

```bash
python3 -B scripts/check_clauses.py --help                                                        # lane descriptions, no network
python3 -B scripts/check_clauses.py --selftest                                                     # good sample passes, seven bad samples fail
python3 -B scripts/check_clauses.py scripts/fixtures/good-clauses.md --source scripts/fixtures/target-contract.md          # expected PASS
python3 -B scripts/check_clauses.py scripts/fixtures/bad-format.md --source scripts/fixtures/target-contract.md            # expected FAIL: overview is not one line
python3 -B scripts/check_clauses.py scripts/fixtures/bad-no-anchor.md --source scripts/fixtures/target-contract.md          # expected FAIL: point row unanchored
python3 -B scripts/check_clauses.py scripts/fixtures/bad-invented-quote.md --source scripts/fixtures/target-contract.md     # expected FAIL: paraphrase as quotation
python3 -B scripts/check_clauses.py scripts/fixtures/bad-missing-type.md --source scripts/fixtures/target-contract.md       # expected FAIL: one category unnamed
python3 -B scripts/check_clauses.py scripts/fixtures/bad-legal-verdict.md --source scripts/fixtures/target-contract.md      # expected FAIL: validity verdict
python3 -B scripts/check_clauses.py scripts/fixtures/bad-outcome-bare.md --source scripts/fixtures/target-contract.md     # expected FAIL: bare outcome assertion (no hedge needed)
python3 -B scripts/check_clauses.py scripts/fixtures/bad-outcome-split.md --source scripts/fixtures/target-contract.md    # expected FAIL: verdict split across two lines (unit is the sentence)
python3 -B scripts/check_clauses.py scripts/fixtures/good-clauses.md --quiet                        # last line and counts only
```

**Row and finding counts always come from the script's own report line** (`FAIL: <file> (N)`, or the "扫过 N 行，发条 0 条，不可判 M 项" line after `PASS:`); this document does not restate them - restating creates a second source of truth.

## 6. What is in the package

```
SKILL.md                       Authority: positioning / input / four steps / four-section contract / channel and fallback / red lines / boundaries
README.md / README.en.md       This file (Chinese authority / English counterpart)
CHANGELOG.md                   Version record
scripts/check_clauses.py       Five checker lanes (standard library; --help runs; all decisions live in the script, this file only points)
scripts/collect_clauses.py     Offline collector: lays clause rows into a four-section skeleton, never judges which category matters
scripts/fixtures/              Synthetic contract + one good sample + seven bad samples (incl. bare outcome verdict and a verdict split over two lines) + three-tier offline runner
```

## 7. Questions and anti-patterns

| What you want to do | Accepted? | Why |
|---|---|---|
| "List this contract's clauses, each traced to the source" | Yes | Clause-level splitting with per-row sourcing is exactly its use |
| "Also tell me whether this clause is valid" | No | Validity belongs to a lawyer and a human; writing it as your own sentence fires `E-LAW` unless the line carries `[待人工]` |
| "Give this contract a risk score" | No | Nobody can verify that number; this package only emits points and namings that trace back to text |
| "Rank these five supplier contracts" | No | One contract at a time; cross-contract comparison is another route whose bias problems are not in this shape |
| "I remember roughly how it read - put it in quotes" | No | Quoted means verbatim: copy that sentence, or leave it unquoted and name the category in section three |
| "I did not upload the annex pages" | Yes, but write it down | Anything unread must be named in section three, never patched with common sense; an unmarked gap makes the sheet pretend to be complete |
| "The scan is only in the cloud drive" | Yes, keep the evidence | Fetch the text through the parse channel and register it as a source row; if it cannot be retrieved, name it in section three instead of writing from page impression |

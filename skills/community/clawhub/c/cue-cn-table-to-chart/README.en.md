# cn-table-to-chart

**One table, split into two things: a chart spec a host can actually draw from (chart type / x-axis / y-axis / series - chosen by a human) and table-reading points (one number per line, each traced back to its cell). No investment advice from the chart, no ratings or target prices, no arithmetic the table does not already contain.**

Drawing tools are plentiful; **what is missing is the check that this number really sits in that cell**. Three hard gates do the difference: a quoted number must appear verbatim in the source table **and in the cell it claims** - either paired as `「列头」=「数」` (column header = number) or written as the whole row in column order, so an invented number, a number borrowed from the next cell of the same row, or an empty cell described as having a value all fail on the spot; when the header cells were merged (a spanning header), pairing fails for the **first** cell too - defaulting a merged header to the leftmost column would be guessing, so that row is accepted only whole in column order, or named in section three; when one line gives both a page and a line number each is checked on its own; and all four limitation classes must each be named - silence counts as a miss. The verdict side, from 0.1.4 on, has **no quote exemption at all**: text inside 「」 is judged like any other words - if the table really contains an investment-bearing sentence, framing it as a source attribution (表注原文：…), relaying it as somebody else's view (有人主张…), or leaving it bare all fire. Verbatim only proves the words are in the table; it does not endorse them. The one legal exit is naming it in section three, unquoted, with a locator. The cost, stated here on purpose: such a quote turns red - the red flags the act of quoting, not an invented number, and that is a chosen conservative face, not a defect.

**Input**: one table's text (a local file, or text pulled back through the parse channel from a PDF / scan / photo of a disclosure)
**Output**: a four-section artifact (chart spec / table-reading points / limits and gaps / sources with parse date), one line per point, ready to hand to a host renderer
**Cost**: a four-section contract plus one checker; whether the parse channel is connected decides **whether the scanned or remote table can be retrieved at all** - what each route lacks is written in §2 and §4
**Checker**: `scripts/check_chart.py`, five lanes (format and row band / anchors and locators / numbers verbatim back to the table and into the cell they claim / four limitation classes / investment-and-rating assertions), zero network, never does arithmetic, never executes anything the table mentions

---

## 1. Do this today: three steps

| Step | Action | How | What breaks if skipped |
|---|---|---|---|
| 1 | **See the shape first** (30 s, no network, no charge) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test (five good samples must pass, eighteen bad ones must each fire their own lane), 23 samples run one by one (code set, finding count, target line, which lane fired, which table it used), collector skeleton that must fail where designed. Last line self-reports "档数=3｜合期望=3｜不合=0｜不可判=0" | Without seeing the shape you mistake "it can be drawn" for "the numbers match"; this tier shows the difference in 30 seconds |
| 2 | **Lay the skeleton, then choose the spec** | `python3 -B scripts/collect_chart.py --source table.md --out chart.md` moves each numeric cell verbatim into section two as `「列头」=「数」` pairs (header = number) with page and line locators - a row whose header cells do not line up falls back to the whole-row-in-order form; fill the four spec keys (the chart type answers "what relationship do I want to see") and the four limitation classes in section three | Unfilled slots fail `E-FORMAT` and `E-COVERAGE` (a skeleton is not an artifact); a missing `[S1]` on a point row, or a source row without locator or parse date, fails `E-ANCHOR` |
| 3 | **Run the checker, then hand it to the host** | `python3 -B scripts/check_chart.py chart.md --table table.md`, fix each line by its `E-*` code; rendering itself belongs to the host or a spreadsheet - this package emits no image file | An invented number, a silently skipped limitation, or "this company is worth buying" written as your own sentence all travel with the material into the human decision; those are shape-level and the checker catches them, arithmetic still has to go back to the table |

Computing growth rates, rendering files and giving investment conclusions **are not in these three steps** - this skill answers only "which cell says what, and can this chart stand up".

## 2. Install → connect → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-table-to-chart` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-table-to-chart` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The one evidence leg is `cue-omni-reader` (parse): when the table lives remotely (a cloud PDF, a scan, a photo of a disclosure page), its text is fetched back into a locally readable copy - **it can be read even when this machine has no file for it, and verbatim text carrying page or line numbers is exactly what this leg adds**, which makes it the primary route, not a decoration. Its connection check (a pure parse leg, nothing in curl can substitute for it): the host lists tools through the MCP `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this skill neither self-certifies nor runs either for you. Configuration: the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this skill depends on that leg only; the data-leg page is deliberately not cited here). If they do not, this skill still reads only the local copy you hold, and the cost is stated in the same breath: the scanned or remote table cannot be retrieved (missing is that cell of verbatim text, not typography). Whether the file in your hand is the version that produced the numbers is judged on neither route - this skill reads no version marker and no disclosure chain; nominate the baseline and align to it. The three layers prove different things: **skill installed ≠ credential configured ≠ channel connected**. The key comes from your local credential facility, never into chat and never echoed; this face adds no credential-reading step; parse cost follows what the server returns - this skill neither estimates nor pays for it, and asks before spending.

## 3. Offline sample: the shape in 30 seconds

```bash
cd cn-table-to-chart
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: five good samples pass, eighteen bad samples each fire their own lane -> ALL GREEN
# tier 2  one line per sample: "expected only E-X / actually exactly E-X / how many findings / which line, which lane, which table", each row self-reporting whether the injection landed
# tier 3  collector skeleton from the synthetic table: numbers land in section two as header=number pairs, and the skeleton must fail on two lanes - the four spec keys and the four limitation classes are still unjudged
```

Your own run is the same two commands:

```bash
python3 -B scripts/collect_chart.py --source my-table.md --out chart.md
python3 -B scripts/check_chart.py chart.md --table my-table.md
```

The collector is read-only and never chooses for you: it reads markdown pipe rows (the row above the separator line is a header, not data and not a point row), copies each numeric cell verbatim into section two as `「列头」=「数」` pairs with both locators, and falls back to the whole-row-in-order form when the header cells do not line up with that row - it never guesses which cell belongs to which column. The four spec keys and the four limitation classes stay as to-be-decided slots - **the chart type depends on the relationship you want to see, and guessing from column shapes would turn "can be drawn" into "should be drawn"**, so that choice stays with the human. The header model is imported from the checker itself (`from check_chart import table_model`), so the two cannot drift into different meanings of "that cell". With no numeric row at all, or an empty file, it exits 1 and says so; an unreadable file or a malformed `--asof` exits 3 (a domain failure is never read as "no violations").

## 4. Dependencies and the cost of each route

- `python3`: used by checker and collector, standard library only, no network, sends no requests.
- The parse helper `cue-omni-reader` is optional: **not installing it raises no error, and the cost is that the artifact answers only for the one copy on your disk** - scans and the remote side cannot be read in. Ask before installing or using it either way; spend only after you agree to it.
- A connected channel is not a retrieved table: rows cut off by the scan, merged cells that no longer map to a header, photos too blurred to read one cell - all of them go into section three by name, never patched with common sense or last year's number. When a header cannot be resolved to a cell the checker fires (its detail line says whether the cell was empty or the header spans columns), and with a spanning header **even the first cell is refused** - defaulting a merged header leftward is guessing. Write that row whole in column order, or name it in section three.
- The arithmetic stays in the host: growth rates, shares of total, ratios - this package computes none of them; it moves existing cells and points at where each one came from. A number the table does not contain fails `E-QUOTE`, and so does a number taken from a different column of the same row.
- Data boundary: the artifact carries the table's numbers and its stated basis (disclosure tables often include non-public bases). Storage, forwarding and who sees it are yours to own; this skill uploads nothing and writes nothing outside its package.
- Locators expire with the file: page and line numbers hold only as of the parse date; if a newer disclosure replaces it, the spec has to be redone.

## 5. The five checker lanes and its self-tests

| Lane | Code | What it blocks |
|---|---|---|
| 1 format | `E-FORMAT` | Four self-labels verbatim in the head; four sections ordered; all four spec keys present and none still a to-be-decided slot; 3-10 point rows in section two, **counted by list marker** - a point row must start with `- ` or `* `; when that section holds only plain lines the detail line says 这一节没有以 - 或 * 起的行 (契约:一条一行＝一条列表项) |
| 2 anchors | `E-ANCHOR` | Each point row ends with one `[S#]` and carries a locator; every anchor has a matching row in section four; source rows need **both** a locator and a parse date - the date must sit under the 解析日 label and name a day that exists (relabel it 合同签署日 and it fires; the checker verifies exactly those two things and cannot verify that the day is when the text was actually retrieved) |
| 3 verbatim | `E-QUOTE` | **Every** 「」 span anywhere in the artifact must be verbatim in the table - point rows and ordinary sentences alike, so a fabricated quote outside a bullet cannot slip through; and the number must sit in the cell it claims, via `「列头」=「数」` (header = number) or the whole row quoted in column order - borrowing the neighbouring cell's number, claiming a value for an empty cell, or borrowing another table's header all fail. Pairing has a precondition: **the header row must have exactly as many cells as that data row**; with a merged (spanning) header the first cell is refused too, because defaulting a merged header leftward is guessing - such a row is accepted only whole in column order, or named in section three. When a line gives both page and line number **each is checked separately**; without `--table` the lane prints not-verifiable and **is never folded into a pass** |
| 4 naming | `E-COVERAGE` | All four limitation classes present (empty cells / merged or spanning headers / units and basis / extrapolation and unread parts), each with a position or an explicit 未见到／未取到; a 待核 slot is not a naming; an unread part mentioned elsewhere but unnamed here fails; an empty source section fails |
| 5 verdict words | `E-ADVICE` | Investment advice, rating actions and target prices fire **on the word alone - no hedge needed**; reworded verdicts fire too - a superlative or comparative form (最强／优于／更差) in the same **semantic unit** as an investment-conclusion object (估值／基本面／前景／配置) is a verdict. Units split only on **structure** (heading / list item / table / blockquote): an ordinary continuation line - even an indented one - joins the previous unit, so a line break or an indent is not an escape. **From 0.1.4 there is no quote exemption**: text inside 「」 is judged too, so an investment-bearing sentence from the table fires whether it is framed as a source attribution, relayed as a third party's view, or left bare - verbatim proves presence, not endorsement. The only legal exit is naming it in section three without quoting it, with a locator. `[待人工]` only excuses the unit it sits in |

```bash
python3 -B scripts/check_chart.py --help                                                        # lane descriptions, no network
python3 -B scripts/check_chart.py --selftest                                                     # five good samples pass, eighteen bad ones fail
python3 -B scripts/check_chart.py scripts/fixtures/good-chart.md --table scripts/fixtures/target-table.md          # expected PASS
python3 -B scripts/check_chart.py scripts/fixtures/bad-spec.md --table scripts/fixtures/target-table.md            # expected FAIL: chart type undecided
python3 -B scripts/check_chart.py scripts/fixtures/bad-no-anchor.md --table scripts/fixtures/target-table.md        # expected FAIL: point row unanchored
python3 -B scripts/check_chart.py scripts/fixtures/bad-invented-number.md --table scripts/fixtures/target-table.md  # expected FAIL: number not in the table
python3 -B scripts/check_chart.py scripts/fixtures/bad-unbound-quote.md --table scripts/fixtures/target-table.md    # expected FAIL: a quote outside point rows that the table never contains
python3 -B scripts/check_chart.py scripts/fixtures/bad-cell-misplaced.md --table scripts/fixtures/target-table.md   # expected FAIL: neighbouring cell's number claimed as this cell
python3 -B scripts/check_chart.py scripts/fixtures/bad-no-header-pair.md --table scripts/fixtures/target-table.md    # expected FAIL: numbers with no header pair and not whole-row-in-order
python3 -B scripts/check_chart.py scripts/fixtures/bad-cell-empty-zero.md --table scripts/fixtures/target-table.md   # expected FAIL: an empty cell described as having a value
python3 -B scripts/check_chart.py scripts/fixtures/bad-merged-bind.md --table scripts/fixtures/target-table-merged.md # expected FAIL: a spanning header paired onto its first cell
python3 -B scripts/check_chart.py scripts/fixtures/good-merged-order.md --table scripts/fixtures/target-table-merged.md # expected PASS: the same row written whole in column order
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-conclusion.md --table scripts/fixtures/target-table-noted.md # expected FAIL: words the table does contain, used as this artifact's conclusion
python3 -B scripts/check_chart.py scripts/fixtures/bad-missing-limit.md --table scripts/fixtures/target-table.md    # expected FAIL: one class unnamed
python3 -B scripts/check_chart.py scripts/fixtures/bad-advice.md --table scripts/fixtures/target-table.md           # expected FAIL: target price
python3 -B scripts/check_chart.py scripts/fixtures/bad-bare-outcome.md --table scripts/fixtures/target-table.md     # expected FAIL: bare verdict, no hedge
python3 -B scripts/check_chart.py scripts/fixtures/bad-superlative.md --table scripts/fixtures/target-table.md      # expected FAIL: reworded verdict
python3 -B scripts/check_chart.py scripts/fixtures/bad-conclusion-crossline.md --table scripts/fixtures/target-table-noted.md  # expected FAIL: 结论： at column 0, the quote indented on the next line
python3 -B scripts/check_chart.py scripts/fixtures/bad-author-voice-verb.md --table scripts/fixtures/target-table-noted.md     # expected FAIL: an authorial voice outside the old word list (表明) still loses the exemption
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-source-only.md --table scripts/fixtures/target-table-noted.md # expected FAIL: quoting it as 表注原文 no longer exempts
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-third-party.md --table scripts/fixtures/target-table-noted.md # expected FAIL: relaying the table's advice as somebody else's view
python3 -B scripts/check_chart.py scripts/fixtures/bad-quote-bare.md --table scripts/fixtures/target-table-noted.md       # expected FAIL: a bare quote of the table's advice sentence
python3 -B scripts/check_chart.py scripts/fixtures/good-quoted-note.md --table scripts/fixtures/target-table-noted.md  # expected PASS: legal exit - named in section three, unquoted, both locators
python3 -B scripts/check_chart.py scripts/fixtures/good-plain-quote.md --table scripts/fixtures/target-table-noted.md   # expected PASS: same, page locator only
python3 -B scripts/check_chart.py scripts/fixtures/good-third-party.md --table scripts/fixtures/target-table-noted.md   # expected PASS: same, line locator only
python3 -B scripts/check_chart.py scripts/fixtures/good-chart.md --quiet                          # last line and counts only
```

**Row and finding counts always come from the script's own report line** (`FAIL: <file> (N)`, or the "扫过 N 行，发条 0 条，不可判 M 项" line after `PASS:`); this document does not restate them - restating creates a second source of truth.

## 6. What is in the package

```
SKILL.md                         Authority: positioning / input / four steps / four-section contract / channel and fallback / three hard boundaries / limits
README.md / README.en.md         This file (Chinese authority / English counterpart)
CHANGELOG.md                     Version record
scripts/check_chart.py           Five checker lanes (standard library; --help runs; all decisions live in the script, this file only points)
scripts/collect_chart.py         Offline collector: lays table numbers into a four-section skeleton, never chooses the chart type, never does arithmetic
scripts/fixtures/                Three synthetic tables (default / with a table note / with a spanning header) + five good samples + eighteen bad samples + three-tier offline runner
```

## 7. Questions and anti-patterns

| What you want to do | Accepted? | Why |
|---|---|---|
| "Turn this table into a spec I can draw from" | Yes | Four spec keys with every number traced to its cell is exactly its use |
| "Also tell me what this data means" | No | The judgement slot stays human; writing it as your own sentence fires `E-ADVICE` unless the unit carries `[待人工]` |
| "Compute the year-on-year and the shares" | No | This package computes nothing; arithmetic goes back to the host or a spreadsheet |
| "Just render the chart for me" | No | The artifact is a spec plus points; rendering belongs to the host - hiding a renderer here would leave nobody responsible for a wrong chart |
| "I think that number was about 1.6 - put it in quotes" | No | Quoted means verbatim: copy that cell, or write it into section three as unread |
| "The neighbouring cell's number will do for the one I mean" | No | A number has to sit in the cell it claims - `「列头」=「数」` pairs or the whole row in column order; a borrowed one fires `E-QUOTE` |
| "I'll bracket a sentence the table never contained, as a quote" | No | 「」 anywhere in the artifact means verbatim table text; what the table never says fires `E-QUOTE` and loses the lane-5 exemption |
| "The table's own note says it, so I can quote it as my own" | No | Since 0.1.4 nothing inside 「」 is exempt: an investment-bearing sentence from the table fires whatever frame introduces it - verbatim proves presence, not endorsement; name it in section three without quoting it |
| "I quote it and name nobody - that must be safe" | No | A bare quote of the table's advice sentence fires too - the absence of a subject is not a disclaimer |
| "A third party said it, the artifact just relays it" | No (for that sentence) | Relaying somebody else's words does not move the investment claim out of this artifact; the legal shape is naming it in section three, unquoted, with a locator |
| "The header is merged, pairing it to the first column must be fine" | No | Pairing needs the header cell count to equal that row's cell count; when they differ the first cell is a guess too - write the row whole in column order or name it in section three (`E-QUOTE`) |
| "Merge the other company's numbers into this chart" | No | One table at a time; cross-table joins carry alignment and basis problems this shape does not cover |
| "The table is a photo, I have no file" | Yes, keep the evidence | Fetch the text through the parse channel and register it as a source row; if it cannot be retrieved, name it in section three instead of filling cells from memory |

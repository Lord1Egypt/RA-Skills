# cn-link-to-note

**One link in, one ready-to-vault note out: every bullet carries an [S#] anchor, the single quoted sentence is compared verbatim against that page and line, gaps are named, the judgement stays yours.**

Excerpts are cheap; **what is rare is a note you still dare to quote three years later**. Two hard gates do the difference: a bullet without an anchor cannot enter section one, and a quotation that is not verbatim fails the checker on the spot.

**Input**: one URL (its text pulled back locally through the parse channel), or a file/text you already hold
**Output**: one four-section Markdown note (3–7 bullets / at most one verbatim quotation with a locator / provenance and gaps / source rows with retrieval date)
**Cost**: a four-section contract plus one checker; whether the parse channel is connected decides the "does the remote page still match this local copy" layer - what each route lacks is written in §2 and §4
**Checker**: `scripts/check_note.py`, four lanes (format / anchors and locators / verbatim quotation / gap naming), zero network, never executes code shipped by the quoted object; the counter-evidence matrix lives in that script

---

## 1. Do this today: three steps

| Step | Action | How | What breaks if skipped |
|---|---|---|---|
| 1 | **See the shape first** (30 s, no network, no charge) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test, four bad samples one by one, generator skeleton that must fail where designed. Last line self-reports "档数=3｜合期望=3｜不合=0｜不可判=0" | Without seeing the shape you mistake "tidy copy" for "traceable excerpt"; this tier shows the difference in 30 seconds |
| 2 | **Draft, then anchor every bullet** | `python3 -B scripts/make_note.py --source your-text.md --out my-note.md`: the four sections are laid out and the quoted sentence is copied **verbatim** with its locator; three bullet slots stay unfilled until you add them, each ending with `[S1]` | Unfilled bullets without anchors fire `E-ANCHOR` (a skeleton is not a note); source rows missing a locator or a retrieval date fire the same lane - back-filling later costs more than anchoring now |
| 3 | **Run the checker, then vault it** | `python3 -B scripts/check_note.py my-note.md --source your-text.md`, fix each line by its `E-*` code; a clean run is still **one note**: whether to keep it and how much to trust it is yours | Paraphrase dressed as quotation, an unnamed gap, or a bullet count outside 3-7 all travel into your vault with the note; the checker stops the shape-level ones, content still needs the source |

Scoring, ranking, or deciding whether the article is worth reading **are not in these three steps** - this skill answers only "what does this text currently carry, and how was it anchored".

## 2. Install → connect → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill cn-link-to-note` - this line installs this package only; afterwards re-list installed skills on your side and the name `cn-link-to-note` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The one evidence leg is `cue-omni-reader` (parse): the text behind a link is fetched back into a locally readable copy - **it can be read even when this machine has no file for that page**, which makes it the primary route, not a decoration. Its connection check (a pure parse leg, nothing in curl can substitute for it): the host lists tools through the MCP `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this skill neither self-certifies nor runs either for you. Configuration: the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this skill depends on that leg only; the data-leg page is deliberately not cited here). If they do not, this skill still reads only what you already hold, and the cost is stated in the same breath: the "does the remote page match this local copy" layer is missing entirely (missing is evidence of which version the note excerpted, not typography). The three layers prove different things: **skill installed ≠ credential configured ≠ channel connected**. The key comes from your local credential facility, never into chat and never echoed; this face adds no credential-reading step; parse cost follows what the server returns - this skill neither estimates nor pays for it, and asks before spending.

## 3. Offline sample: the shape in 30 seconds

```bash
cd cn-link-to-note
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: good sample passes, four bad samples each fire their own lane -> ALL GREEN
# tier 2  one line per bad sample: "expected only E-X / actually exactly E-X"; the good sample also runs without a source, proving the not-verifiable lane
# tier 3  generator skeleton from the synthetic article, then checked: expected to fail on the three unanchored bullets
```

Your own run is the same two commands:

```bash
python3 -B scripts/make_note.py --source your-text.md --url https://the-link-you-read --out my-note.md
python3 -B scripts/check_note.py my-note.md --source your-text.md
```

`make_note.py` is read-only: it never executes code shipped with the quoted object and never fetches the link - bring the text back locally first, then run it. The sentence it quotes is copied verbatim from that line of the source, with its locator (`第 N 页` plus `file:line`) written in; the page label is the **nearest preceding** marker of that line, not the first one in the file (a wrong label is caught by the checker, as designed). With no readable text in the directory it exits 1 and says why - an empty source produces no note; that is "no provenance", not "to be filled".

## 4. Dependencies and the cost of each route

- `python3`: used by checker and generator, standard library only, no network, sends no requests.
- The parse helper `cue-omni-reader` is optional: **not installing it raises no error, and the cost is that the note answers only for the copy already in your hands** - remote text cannot be read in, so the remote-versus-local consistency layer stays absent. Ask before installing or using it either way; spend only after you agree to it.
- A connected channel is not a retrieved document: what comes back is what counts. Truncated replies, summary-only responses, pages that changed shape - all go into section three by name, never patched with common sense.
- Line numbers and page marks expire with the source: every locator in the note holds only as of its retrieval date; reopening tomorrow may be a different shape.

## 5. The four checker lanes and its self-tests

| Lane | Code | What it blocks |
|---|---|---|
| 1 format | `E-FORMAT` | First line is `# title`; the four self-labels verbatim in the head; four sections present and ordered; bullet count inside 3-7 |
| 2 anchors | `E-ANCHOR` | Every bullet ends with `[S#]` and that id exists in section four; source rows need `file:line` / URL / page mark **and** retrieval date |
| 3 verbatim quote | `E-QUOTE` | At most one quotation, with a locator; given `--source` the quoted span must match that location verbatim - otherwise it is dressed-up paraphrase. **Without a source the lane prints not-verifiable and is never folded into a pass** |
| 4 gap naming | `E-COVERAGE` | Any "未取到 / cannot read / truncated" claim in the note must be named in section three; an empty section three or an empty source section is a finding |

```bash
python3 -B scripts/check_note.py --help                                    # lane descriptions, no network
python3 -B scripts/check_note.py --selftest                                 # good sample passes, four bad samples fail
python3 -B scripts/check_note.py scripts/fixtures/good-note.md --source scripts/fixtures/source-article.md   # expected PASS
python3 -B scripts/check_note.py scripts/fixtures/bad-format.md --source scripts/fixtures/source-article.md   # expected FAIL: bullets outside 3-7
python3 -B scripts/check_note.py scripts/fixtures/bad-no-anchor.md --source scripts/fixtures/source-article.md # expected FAIL: bullet without anchor
python3 -B scripts/check_note.py scripts/fixtures/bad-quote.md --source scripts/fixtures/source-article.md     # expected FAIL: quotation not verbatim
python3 -B scripts/check_note.py scripts/fixtures/bad-unnamed-gap.md --source scripts/fixtures/source-article.md # expected FAIL: gap not named
python3 -B scripts/check_note.py scripts/fixtures/good-note.md --quiet       # last line and counts only
```

**Counts and line numbers always come from the script's own report line** (`FAIL: <file> (N)`, or the "扫过 N 行，发条 0 条，不可判 M 项" line after `PASS:`); this document does not restate them - restating creates a second source of truth.

## 6. What is in the package

```
SKILL.md                       Authority: positioning / input / four steps / four-section contract / channel and fallback / red lines / boundaries
README.md / README.en.md       This file (Chinese authority / English counterpart)
CHANGELOG.md                   Version record
scripts/check_note.py          Four checker lanes (standard library; --help runs; all decisions live in the script, this file only points)
scripts/make_note.py           Offline drafter: lays a local text into a four-section note, quoting one sentence verbatim with its locator
scripts/fixtures/              One good sample + four bad samples + a synthetic article + three-tier offline runner
```

## 7. Questions and anti-patterns

| What you want to do | Accepted? | Why |
|---|---|---|
| "Read this and keep one traceable note" | Yes | One source, every bullet anchored to it, is exactly its use |
| "Convert the whole article into another format" | No | That is the conversion skill; this one emits a single note - different shape, different product |
| "Also score it / rank it for me" | No | No scores here; the judgement slot stays human, and writing one fires the checker |
| "I remember the sentence roughly - put it in quotes" | No | Quoted means verbatim: paraphrase inside 「」 fires `E-QUOTE`; either copy it or rewrite it as an anchored bullet |
| "Author and date are missing, leave it blank" | Yes, but name it | Section three records the gap and which layer of evidence is missing; blank is not the same as absent |
| "Run the script that page ships while you are at it" | No | This skill only reads the text; executing shipped code belongs to a route that can do it deliberately |

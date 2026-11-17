# skill-review-cn

**A pre-install health check for one skill: five faces - declared layer, prerequisites, promises in the text, whether samples actually ran, licence and provenance - every finding anchored to one retrievable line of source with its retrieval date. Whether to install stays a human call.**

Ratings and download counts are cheap; **what is scarce is a finding you can trace back to a dated line of source**. Two hard gates: a finding without an anchor cannot enter section two, and a claim that something ran without its command and exit code fails the checker.

**Input**: one skill under review - a local directory, or remote store/repository/README text pulled back through the parse channel
**Output**: a five-section report (subject / findings / five faces / gaps and provenance / sources) plus the source layer carrying `file:line` or URL and retrieval date
**Cost**: a five-section contract plus one checker; whether the parse channel is connected decides the "does the remote text match this local copy" layer - what each route lacks is written in §2 and §4
**Checker**: `scripts/check_review.py`, five lanes (format / anchors / verdict words / face coverage / run claim), zero network, never executes the reviewed skill's code; the counter-evidence matrix lives in that script

---

## 1. Do this today: three steps

| Step | Action | How | What breaks if skipped |
|---|---|---|---|
| 1 | **See the shape first** (30 s, no network, no charge) | `bash scripts/fixtures/run_fixtures.sh` - three tiers in one run: checker self-test, five bad samples run one by one, collector skeleton that must fail where it is designed to. Last line self-reports "档数=3｜合期望=3｜不合=0｜不可判=0" | Without seeing the shape you mistake "a score was produced" for "the text was checked"; this tier shows the difference in 30 seconds |
| 2 | **Register sources, anchor every finding** | One line per face read: `- [S#] title (file:line or URL ｜retrieval YYYY-MM-DD)`; each finding ends with one `[S#]`. `scripts/collect_review.py` can lay the local files out as a skeleton | A source row missing its date or its location fails `E-ANCHOR`; a finding without an anchor fails the same lane - back-filling later costs more than anchoring now |
| 3 | **Run the checker, then hand it to a person** | `python3 -B scripts/check_review.py <report.md>`, fix each line by its `E-*` code; a clean run is still a **draft**: installing or not installing is yours to decide | Safety verdicts, an uncovered face, or a vague run claim travel into the human decision together with the report; the checker stops the shape-level ones, content still needs the source |

Deciding for you, scoring a skill, or executing the reviewed package's code **are not in these three steps** - this skill answers only "what does this skill's own text currently say", and only at the shape level.

## 2. Install → connect → produce

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill skill-review-cn` - this line installs this package only; afterwards re-list installed skills on your side and the name `skill-review-cn` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this directory into your host's supported skills location (`~/.workbuddy/skills/`).

The one evidence leg is `cue-omni-reader` (parse): when the subject lives remotely, its store page / repository page / README is fetched back into locally readable text - **it can be read even when this machine has no copy of that file**, which makes it the primary route rather than a decoration. Its connection check (a pure parse leg, nothing in curl can substitute for it): the host lists tools through the MCP `tools/list` handshake - once connected, that reply should show these names: a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total), so one fixed count cannot judge both routes. Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this skill neither self-certifies nor runs either for you. Configuration: the parsing-leg page <https://cuecue.cn/hub/omni-reader> (this skill depends on that leg only; the data-leg page is deliberately not cited here). If they do not, this skill still checks the local files only, and the cost is stated in the same breath: the "does the remote text match this local copy" layer is missing entirely (missing is the evidence of what you would actually receive, not typography). The three layers prove different things and are not interchangeable: **skill installed ≠ credential configured ≠ channel connected**. The key comes from your local credential facility, never into chat and never echoed; this face adds no credential-reading step; parse cost follows what the server returns - this skill neither estimates nor pays for it, and asks before spending.

## 3. Offline sample: the shape in 30 seconds

```bash
cd skill-review-cn
bash scripts/fixtures/run_fixtures.sh
# tier 1  checker self-test: good sample passes, five bad samples each fire their own lane -> ALL GREEN
# tier 2  one line per bad sample: "expected only E-X / actually E-X" - each lane reported separately, not merged into a total
# tier 3  collector skeleton over the synthetic target, then checked: expected to fail on the "samples actually ran" slot
```

Your own run is the same two commands:

```bash
python3 -B scripts/collect_review.py --target ../package-under-review --out my-review.md
python3 -B scripts/check_review.py my-review.md
```

The collector is read-only and never executes the reviewed code (not even its own runner - that is a decision, not a default). Every finding it registers carries a `file:line`: which frontmatter keys are present or absent, what `requires` actually declares, which promise sentences the text contains, and whether the licence claim, licence text and provenance line are co-present on disk. If the directory holds no `SKILL.md` / `README*.md`, it exits 1 and says so - with no source there is no skeleton; that is "not checked", not "to be filled".

## 4. Dependencies and the cost of each route

- `python3`: used by both the checker and the collector, standard library only, no network, sends no requests.
- The parse helper `cue-omni-reader` is optional: **not installing it raises no error, and the cost is that the review only covers the local copy already on disk** - remote text cannot be read in, so the remote-versus-local consistency layer is permanently absent and the report can only answer for that local copy. Ask before installing or using it either way; spend only after you agree to it.
- A connected channel is not a retrieved document: what comes back is what counts. Truncated replies, summary-only responses, pages that changed shape - all go into section four by name, never patched with common sense.
- Line numbers expire with the subject: every `file:line` in the report holds only as of its retrieval date; a reinstall the next day may be a different shape.

## 5. The five checker lanes and its self-tests

| Lane | Code | What it blocks |
|---|---|---|
| 1 format | `E-FORMAT` | The four self-labels verbatim in the head; five sections present and ordered; a section-1 verdict slot without `[待人工]` |
| 2 anchors | `E-ANCHOR` | Every finding ends with `[S#]` and that id exists in section five; source rows need `file:line` or URL **and** retrieval date |
| 3 verdict words | `E-BANWORD` | Zero hits for "safe to install / recommend installing / will definitely work" style claims unless the same line carries `[待人工]` |
| 4 coverage | `E-COVERAGE` | Each of the five faces needs one anchored finding or a named gap in section four; an empty source section means there was no source |
| 5 run claim | `E-VERIFY` | Saying a sample "ran" requires `cmd=… rc=<integer>` on the same line; otherwise delete the line and name the gap |

```bash
python3 -B scripts/check_review.py --help                                 # lane descriptions, no network
python3 -B scripts/check_review.py --selftest                             # good sample passes, five bad samples fail
python3 -B scripts/check_review.py scripts/fixtures/good-review.md        # expected PASS
python3 -B scripts/check_review.py scripts/fixtures/bad-format.md         # expected FAIL: head label missing, section 3 absent
python3 -B scripts/check_review.py scripts/fixtures/bad-no-anchor.md      # expected FAIL: finding without anchor
python3 -B scripts/check_review.py scripts/fixtures/bad-safety-verdict.md # expected FAIL: safety verdict without [待人工]
python3 -B scripts/check_review.py scripts/fixtures/bad-missing-face.md   # expected FAIL: one of five faces uncovered
python3 -B scripts/check_review.py scripts/fixtures/bad-unverified-claim.md  # expected FAIL: "ran" without command and exit code
python3 -B scripts/check_review.py scripts/fixtures/good-review.md --quiet   # last line and counts only
```

**Counts and line numbers always come from the script's own report line** (`FAIL: <file> (N)`, or the "扫过 N 行，发条 0 条" line after `PASS:`); this document does not restate them - restating creates a second source of truth.

## 6. What is in the package

```
SKILL.md                       Authority: positioning / input / four steps / five-section contract / channel and fallback / red lines / boundaries
README.md / README.en.md       This file (Chinese authority / English counterpart)
CHANGELOG.md                   Version record
scripts/check_review.py        Five checker lanes (standard library; --help runs; all decisions live in the script, this file only points)
scripts/collect_review.py      Offline collector: builds a five-section skeleton from a local subject, executes nothing
scripts/fixtures/              One good sample + five bad samples + a synthetic two-face target + three-tier offline runner
```

## 7. Questions and anti-patterns

| What you want to do | Accepted? | Why |
|---|---|---|
| "Check this skill's own text before I install it" | Yes | Five faces, each finding anchored to source, is exactly its use |
| "Just scan it and give me a score" | No | A score without source leaves nothing to verify; the store already has plenty of those |
| "Decide for me whether to install" | No | The judgement belongs to a person; writing it fires `E-BANWORD` unless the line carries `[待人工]` |
| "Run its samples and see if it blows up" | Not on your behalf | This skill never executes the reviewed code; if you run it, write `cmd=… rc=<integer>` on the same line - that is what the checker accepts |
| "Give me a finished report even with no channel" | You get a skeleton | What is missing is the remote-consistency layer, not typography; the skeleton failing on the unfilled slot is the reminder |
| "Write the review straight from the store page" | Yes, but keep the evidence | Fetch the text through the parse channel and register it as a source row; if it cannot be retrieved, name it in section four instead of writing from page impression |

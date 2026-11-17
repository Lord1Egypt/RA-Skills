# journal-draft

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**Give it one back issue; get back a next-issue draft that can go straight into design.**

This is not "write me an article" — it **measures** a publication's layout and editorial conventions out of a PDF and turns them into verifiable parameters, then produces the next issue against those parameters. So what it hands back can go into design directly, instead of a pile of text waiting to be laid out.

**Input**: one back issue as a sample (PDF preferred) + this issue's requirements
**Output**: `draft.html` (mm-precision positioned layout draft) · `draft.pdf` (print-grade, self-drawn) · `draft.docx` / `draft.md` (editable text drafts)
**Cost**: standard mode ≈ **3 batches of questions** (kick-off / outline / delivery — ≤5 questions per batch, each with a default)

---

## 1. How this differs from "just give me an outline"

### ① Layout is **measured**, not described

It extracts the page grid, type area, type scale, leading, color palette, and header/logo coordinates from the sample PDF into `stylespec.json`. The renderer lays out the issue at mm-level absolute positioning — so the PDF is **drawn by PyMuPDF itself**, not printed through a browser (corporate policy can make an entire issue invisible; see `references/pitfalls.md`).

### ② Five gates, built for the "script didn't error, page looks fine" kind of silent failure

| Silent failure | What it looks like | What catches it |
|---|---|---|
| Content clipped | Fewer pages than expected; nothing looks wrong on the page | `overflow` warning from `--stats` (`overflow:hidden` eats the overflow) |
| Not enough content | Layout is perfect, but the issue is only a third as thick as the sample | `scale_baseline` attainment gate — **anything below 60% is a hard FAIL** |
| The three deliverables disagree | HTML updated, docx/md did not | `crosscheck.py` compares text coverage across HTML / MD / PDF item by item |
| The sample is a scan | No type sizes or body text extracted; looks like an empty issue | When the text layer is extremely thin it says "this is probably a scan — OCR it first" instead of returning an empty result |

There is also `check_freshness.py`, a timeliness gate: it locates event dates, issue-number continuity and vague time expressions one by one.

The fourth gate is the **layout quality gate** (`audit_layout.py`, since v0.14.0). The first three cover "is the content right and sufficient"; only this one covers **does it look right and read well** — body type size versus the sample, whether the type hierarchy is fragmented, line-height multiplier, characters per line, whether the font actually applies, leftover Chinese spaces, page density. Measured on an 80-page draft that passed all three gates green: type still one step too small, sizes fragmented into 41 distinct steps, leading 2.16× (sample: 1.85), 73 stray spaces in footers — **not one of those gates reported it**.

The fifth gate is the **editorial positioning gate** (`audit_editorial.py`, since v0.15.0). The first four cover "right content, enough content, good looks"; only this one covers **is it on target** — who this issue is written for, what the reader should do after reading, and what tone it should speak in. Positioning is captured in `positioning.json` (the second machine-readable artifact, a peer of `stylespec.json`); then it judges whether each item's word count falls in the band derived from the tone, coverage of items that deliver "what the reader should do", share of pure-L0 items, sentence length, terminology and taboo words. Measured on a draft that passed all four gates green: all 48 items in a single shape, averaging 409 characters (template declares 180–320, i.e. 28% over), only 4 reader-addressing phrases in the whole issue, only 21% carrying an action suggestion — **again, not one gate reported it**.

Neither gate's check list or thresholds are reproduced here — they are the scripts as they now stand, and one command prints them in place （it carries the installed path and runs from any directory; 装在别处把 ~/.workbuddy/skills/ 换成你的技能安装目录；Windows 走 Git Bash 或 WSL（命令用 grep，属 POSIX 工具））:

```bash
grep -n "^  [0-9] \|MD_SKIP = " ~/.workbuddy/skills/journal-draft/scripts/audit_layout.py ~/.workbuddy/skills/journal-draft/scripts/audit_editorial.py ~/.workbuddy/skills/journal-draft/scripts/crosscheck.py
```

Check names and thresholds appearing in this file and in `SKILL.md` are mirrors and common examples, **not an exhaustive claim** — after a script change the script governs. **What the machines catch is format and consistency; whether the issue is actually right stays human**: every blocking and advisory item in `references/qa-checklist.md` is ticked by a person, and the three-way cross-check only holds for the artifacts you actually passed in (an omitted one is not checked).

### ③ It admits its limits — and **marks them**

The single-column renderer cannot draw two columns; component geometry on non-A4 trim needs manual tuning; chart-heavy pages have no built-in template; bilingual layout has no built-in rendering — none of this is hidden. When you hit one, the `+learn` wrap-up says so out loud, and `examples/` ships a dedicated **negative sample** to calibrate exactly where it breaks.

### ④ Compliance is not an appendix — it is a separate gate

Values are taken across three layers — **reader identity × industry × periodical form** (external clients / employees / investors / public / channel / regulator; law firm / finance / pharma / food / education / tech / manufacturing / real estate / retail) — and for issues that need sign-off it produces a signature list (marketing / legal / HR / company-secretary-IR / PR / compliance).

### ⑤ There is also work it explicitly **will not take**

Boundaries are written down so neither side wastes time. The following are **not "not supported yet" — they are out of scope by design**:

| Won't take | Why | What to do instead |
|---|---|---|
| **Ghostwriting articles / creative copy** | It delivers "a draft with the right layout and right conventions", not "content with fresh points of view". Views, cases and data must come from you | Hand it your existing material to organize into the layout |
| **Replacing legal / compliance review** | It gives checklists and sign-off suggestions, but that is not legal advice | Before publishing, walk [`references/qa-checklist.md`](references/qa-checklist.md) through human review and sign-off |
| **Delivering print-ready finals** | It delivers a **draft**; bleed, color management and printer soft proofs are out of scope | Take the draft into design software for pre-press |
| **Using a scan as the sample** | Style extraction depends on the PDF's **text layer**; scanned images have none | OCR into a text layer first, then run `+learn` |
| **Two-column / multi-column rendering** | The renderer outputs single column only; column flow and text wrap are a different layout logic | For a two-column publication, use it as a source of **conventions and content templates**, and lay out separately |
| **Bilingual / parallel-text rendering** | No built-in bilingual layout | Produce two single-language drafts and merge them manually |
| **Complex data visualization** | The 6 semantic-diagram templates cover relations like parallel / flow / stack / converge / footer — it is not a chart library | Produce charts externally and bring them in through the `+art` image slot |

If you are unsure, just ask — it will state plainly what it can do this time, what it cannot, and who has to fill the gap.

---

## 2. Quick start

**Install this skill**: `npx skills add huhoo/cue-awesome --skill journal-draft` - this line installs this package only; afterwards re-list installed skills on your side and the name `journal-draft` must appear, otherwise the files are not in place (files in place is not the same as data fetched - the channel route below covers that). Without a CLI environment the fallback is to copy this whole directory into your host's supported skills location (`~/.workbuddy/skills/`).

```bash
python -m pip install pymupdf        # required: style extraction + PDF output
python -m pip install python-docx    # optional: docx text draft and write-back
python -m pip install pillow         # optional: pre-press image checks
```

Use `python` on Windows; `python3` on macOS / Linux.

**Images need no image API key at all.** Semantic diagrams go through `gen_diagram.py`, drawn as vector graphics in code (zero cost, no watermark, every Chinese character verifiable); only atmospheric images that carry no specific information, such as cover decorations, use the agent's own multimodal image generation.

**Smoke test** (confirm the environment works):

```bash
python scripts/build_draft.py \
  --spec assets/examples/qiming-regional-sample/stylespec.json \
  --content assets/templates/content.example.json \
  --out ./smoke --stats
```

If it prints page count, item count and `unknown=0`, you are through. The sample is only 8 pages, so it will report `[FAIL] 量级严重不足` (it is being compared against a 91-page baseline) — **that FAIL is expected**; what matters is that the gate ran, not its verdict. **The exit code is 1 here too** — that is the gate's verdict, not a script crash; when wiring CI, distinguish those two by status code.

**Self-test face** (re-verifies this package itself; it never touches your manuscript):

```bash
bash scripts/fixtures/run_fixtures.sh
```

Zero network, standard library only, run with no arguments; the last line reports `ALL GREEN（N items）` and exits 0 (N is whatever the runner now prints; this face does not pin a count), any mismatch prints FAIL lines with the captured output and ends with `NOT GREEN` exiting 1. Five groups are judged: the generator happy path over the real inputs shipped with the package (double run byte-identical), the scale gate **both failing and passing** (balance the baseline and it must exit 0 — that is the anti-tautology probe), malformed input leaving no half-written product - **every bad branch carries all four assertions** (non-zero exit, **the first line of the error output must contain both the parameter name and what is wrong** - one missing means red, so a generic "input is not valid JSON" on line 1 no longer counts as naming anything, zero traceback, empty output directory): three `--content` shapes and one `--spec` shape for `build_draft.py`, the missing-`--content` usage error, and four bad `--outline` branches for `enrich_from_omni.py` (truncated, array, string, and a path that does not exist - naming a path you cannot read is not the same as omitting the option). The fifth group is the **derived face ↔ generator sync ledger** (`scripts/check_derived_sync.py`): the number of faces that *should* be checked is counted from the roster on disk (directories under `examples/` that carry a SKILL.md) and then reconciled against the count declared inside the ledger - a mismatch means red, because a roster-only rule is washed green when a whole example directory disappears while a constant-only rule is washed green when someone deletes one face's fixed inputs, so both locks are needed - after which each face is regenerated with `derive_skill.py` and compared block by block against the face on disk (frontmatter key by key, body split on de-numbered level-2 headings; the derive inputs and the exempt keys are fixed constants inside the ledger, never reverse-engineered from the face on disk). Every roster face must print one reading line - a face that cannot run still prints its line with the reason named - and if the number actually run differs from the number that should have been checked the ledger goes red naming the missing face, because a sync ruler that silently skips one face has not measured what it claims. Adding or removing an example means changing the declared count and the three constant tables (inputs, registry, human-owned items) in the same edit; a partial change is red. Its current shape is a **registry mode**: every known drift is reported item by item and the last line self-reports `已知漂移 N 行｜实跑 P／应检 Q 枚` together with the registry-mode wording, exiting 0, so the ledger cannot block the release chain; it goes red on five things - measured drift above the registered number, an unregistered block or key drifting, a face silently not measured, the two-way lock on human-owned items (missing on disk means red, grown by the generator means red, each direction with its own named sentence), or an exempt key missing on either side. `metadata.version` is exempted line by line as a mirror (it is the second copy of the top-level `version`); the other `metadata` sub-fields stay under hard comparison. Empty the registry inside the ledger and it becomes a strict rule (non-empty diff means red) without touching the verdict logic. That ledger compares only the SKILL.md face; the README, assets and scripts the generator emits in the same run are out of scope. All verdicts stay inside the scripts as they now stand; the fixtures and this runner ship with the artifact.

### The Cue channel (deep research / document parsing)

**Not required, but strongly recommended** — without it nothing errors, you just lose one layer of cross-verification and the semantic layer falls back to manual entry. Three steps to enable: register at <https://cuecue.cn> → get `CUE_API_KEY` at <https://cuecue.cn/hub/api-key> → install `cue-research` (Omni parsing additionally needs the local Bridge).

The channel route (account-side connectivity self-check; this package ships no connectivity script, so the curl lines below are the whole action):

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<replace with a domain id listed by the line above>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("not found: that id is not in the live catalog (or it has no routing.url) - run the listing line first, then fill it in")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "no value: ROUTING_URL is empty - list the ids first, then set DOMAIN_ID to one of them" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

The three layers are never equivalent: skill installed != credentials configured != channel connected. The anonymous `GET` proves **catalog reachability** only; the key is proven *accepted* once a `tools/list` reply comes back with it attached - pass = HTTP 200 with a non-empty `result.tools` (shape only; no tool names or counts are promised here). Domains absent from the catalog are neither installed nor promised on this face. The Omni leg is not in that catalog: its connectivity test is the host listing tools (the same JSON-RPC `tools/list` handshake) and finding `parse` and `get_parse_status` there; if those names are absent, only the user-supplied route is open. The key comes from your local credential facility - never into chat, never echoed back; this block adds no new credential read.

New accounts get **500 credits** on signup plus 10 credits per day, **and Cue always asks before spending**. At kick-off it asks item by item whether you want to use it; the decision rules are in [`references/cue-onboarding.md`](references/cue-onboarding.md).

---

## 3. Eight verbs — resume from any stage

```
+learn extract style   +brief align requirements   +plan outline    +gather collect evidence
+draft produce draft   +art images                 +check proofread +spec distill sub-skill
```

Saying "make the next issue following this one" automatically walks from `+learn` to `+brief`. A `progress.md` ledger is created at kick-off, one line per completed stage; whoever picks it up after an interruption reads it first, so **questions already answered are not asked again** (spec in [`references/agent-interaction.md`](references/agent-interaction.md)).

---

## 4. Position your publication first (three questions that set every default below)

This framework's **defaults were tuned against a law-firm client newsletter** (A4 single column, sequential issue numbering, external-client readership). If your publication differs and you skip these three questions, you will get a draft that is **"all gates green, all conventions wrong"**.

| Question | What your answer decides | Where copying the default goes wrong |
|---|---|---|
| **Who reads it?** clients / employees / investors / public / channel / regulator | Compliance floor + **the departments that must sign off** | Default is "external clients" → an employee magazine misses HR+legal sign-off and personnel confidentiality items; an IR letter misses selective-disclosure rules |
| **What cadence?** continuous periodical / special issue / annual review / compilation / high-frequency bulletin | How issue numbers are assigned + the timeliness window | Default is "previous issue N-1 + 6-month window" → **yearbooks are numbered by year**, with the window widened to 12 months or exempted item by item; weekly bulletins shrink it to 1 month |
| **What form?** items + long articles / pure articles / chart-heavy / compilation / briefing | How many UnitPatterns to extract + whether the eight templates suffice | Default is "items + long articles" → a pure-article publication needs only one U1; chart-heavy types (annual report / ESG) **have no built-in chart page template** |

> Per-item differences, reader × compliance matrix, industry prohibitions, common unit library (12 kinds):
> **[`references/journal-types.md`](references/journal-types.md) (read before changing publication type)**

---

## 5. Pick your path by situation (choosing wrong wastes a whole `+learn` round)

| Your situation | Where the sample comes from | Watch out for |
|---|---|---|
| **① Veteran editor of this title** (own publication, back issues exist) | Use **the previous issue** directly | Most common: **reused items are not fact-checked** (people left, phone numbers changed, data expired). The 8 items of the `+brief` "reusable list" must be checked one by one |
| **② Same publication type, different organization** | Use **that organization's own back issue**; if none, go to ④ | **Do not use another company's publication as a production sample** — what you extract is their brand DNA |
| **③ Different publication type, same organization** | Prefer **your own** back issue of that type; otherwise a peer organization's same type | One `stylespec.json` is not enough: **changing publication type means re-running `+learn` and re-deriving**; hand-editing fields always misses something |
| **④ Any publication type at a non-law-firm company** | Your own back issue; if it is a first issue with none, follow the **three ways out** in hard rule 1 of `SKILL.md` | ① Run compliance by the "reader row × industry row" combination, don't copy the finance/legal tone; ② structured data lives in **your ERP/CRM/HR internal systems** — confidential, needs authorization, and must be desensitized |

**Three general onboarding paths**:

| You want | How |
|---|---|
| **To see what a finished result looks like** | Copy `examples/journal-qiming-regional/` into `~/.workbuddy/skills/` and have it produce the next issue. It ships all rendering scripts (12 of them) and does not depend on this directory |
| **To do your own publication** | Take **one issue of your own** as the sample and run `+learn → +brief → +plan → +gather → +draft → +check`, then `+spec` to distill your own skill — **from the second issue on, the cost drops sharply** |
| **To borrow the method only** | Read §3 (seven-stage flow) of `SKILL.md` plus the sample's `unit-patterns.md` to see what a real publication's layout and content templates were distilled into |

**Do not hand-edit `stylespec.json`.** Changing publication type or client means re-running `+learn` and re-deriving; hand-editing dozens of fields always misses something.

---

## 6. Two samples pointing in opposite directions

`examples/` ships a pair of finished skills that are **counter-examples of each other** — reading them side by side shows the framework's edge:

| Sample | Trim and structure | What it tells you |
|---|---|---|
| `journal-qiming-regional` | A4 / 91 pages / **single column** / short items mixed with long articles | **The happy path**: runs through, production-ready (`spec_confidence: pinned`) |
| `journal-hengshi-observation` | 227×276mm / 52 pages / **two columns** / pure articles | **The reverse path**: where the framework fails — the single-column renderer cannot draw two columns, mid-gray body text gets misread as a secondary color, non-A4 trim needs manual geometry tuning (`spec_confidence: weak`, **not production-ready**) |

Plus `assets/examples/qiming-regional-sample/`: the **raw intermediate artifacts** of the `+learn` stage (StyleSpec / semantic / UnitPattern), used to calibrate the split between "machine extraction" and "human refinement".

**The structure is: this skill is the framework (parent package), `examples/` holds finished samples (child packages).** The child packages are neither a runtime dependency nor the **input** for deriving new ones — they are teaching samples.
**To build your own child package, re-run `+learn` on your own publication and derive — do not edit a sample**:

```
Your latest issue PDF ──+learn──▶ stylespec.json ──human fill-in──▶ unit-patterns.md
                                                                          │
                                                  derive_skill.py ────────┘
                                                          ▼
                                        journal-<your-company>-<type>/   ← self-contained, ready to run, publishable on its own
```

A derived child package **carries its own `slug` / `displayName` / `version`** and can be published to a skill marketplace on its own; `scripts/` and the two `assets/` template directories are copied along, so it runs on another machine immediately. Only `references/` is deliberately left in the parent (it evolves with the framework; a copy would be stale at once) —
**day-to-day work in a child package does not need the parent present; you only come back to the parent for underlying issues like changing trim, redesigning, or switching publication type.**

> ⚠️ **The two finished samples and the one intermediate sample are all desensitized**: institution names, publication names, natural-person names, client and project names, and source file names are **fictional synthetic entities**; what is preserved is the measured layout parameters and template structure. See [`NOTICE.md`](../NOTICE.md) at the repository root — that file lives at the top level and does not ship inside this package, so you will not find it in this directory.

---

## 7. The six easiest traps

| # | Trap | One-line fix |
|---|---|---|
| 1 | **Pagination overflow is silent** | `.page{overflow:hidden}` eats the overflow. Fewer pages than expected means it got clipped — check `overflow` in `--stats` |
| 2 | **"It ran" ≠ "the layout is right"** | Measured case: zero script errors, all attainment rates correct, yet a whole column was offset by half a page and articles were set single-column. After changing trim, always **measure the actual column width** |
| 3 | **Semantic diagrams must not go to text-to-image** | The information lives in label text and topology; diffusion models cannot do it. Measured: 5 of 6 images carried zero information, one had a caption saying "division of labor" while the picture showed "convergence" |
| 4 | **The editable-draft round trip needs a no-op test** | Export docx and write it straight back; it must be byte-identical to the original `content.json`. One no-op run found 5 silent losses |
| 5 | **It promises three questions and asks eight** | That is a flow problem, not a patience problem → move questions earlier and pack them into 3 batches. But **packing ≠ defaulting them off** — the Cue channel must be asked out loud |
| 6 | **Gate re-checks must carry `--spec`** | Since v0.13.1 it no longer passes silently: no `scale_baseline` in the spec means a hard `[FAIL]` + `exit 1`, forcing you to add it or pass `--no-baseline-gate` explicitly |

> The full **12 traps** (including the image `avoid` list not catching sensitive subjects, empty image slots disguising themselves as path errors in docx, skipping positioning when changing publication type producing "all gates green, all conventions wrong"…): **[`references/pitfalls.md`](references/pitfalls.md)**

---

## 8. What is in the package

```
SKILL.md                     main flow and hard rules (read first)
README.md                    this file in Chinese (features, limits, onboarding)
README.en.md                 English version
CHANGELOG.md                 version history and breaking changes
NOTICE.md                    source statement and desensitization notice (**repository root** — not shipped inside this package)
LICENSE.md                   MIT (keeps the .md extension: marketplaces reject extension-less files)

references/
  journal-types.md           publication typology: reader × cadence × form × industry × common unit library  ← read before switching type
  pitfalls.md                12 measured traps (including CLI traps)
  cue-onboarding.md          Cue / Omni channel: per-item decision table + suggested scripts + first-time setup
  content-schema.md          content.json field spec (eight page templates / units / blocks / self-checks)
  content-sourcing.md        sourcing matrix L1–L5 (company-owned sources / official texts / structured data / deep research)
  stylespec-schema.md        StyleSpec field definitions
  style-extraction.md        style extraction method and traps
  qa-checklist.md            pre-publication checklist (common floor + industry plugin entry points)
  editable-output.md         editable drafts and the write-back loop
  imagery.md                 images: four decision classes / prompt structure / pre-press checks
  omni-channel.md            document parsing channels and fallbacks
  cue-playbook-map.md        topic → Cue capability mapping
  cue-buddy-map.md           how to solidify a smooth run into a Cue buddy
  instantiation.md           derivation flow
  agent-interaction.md       question batching and delivery action spec
  regulatory-dynamics-spec.md  spec for the regulatory-dynamics section

scripts/                     a set of scripts (count is whatever the directory now holds; this face does not pin a number), all support --help, zero network requests
assets/templates/            starter templates: issue-brief / outline / unit-pattern / evidence-card /
                             imagery / progress / content.example / buddy draft
assets/demo/                 **layout drafts you can open directly** (13-page sample + content source + two semantic diagrams)
assets/diagram-templates/    6 semantic diagram definitions (columns / flow / rows / stack / converge / footer)
assets/examples/             intermediate artifacts from +learn
examples/                    two finished sample skills, installable or adaptable as-is
```

**Dependencies**: `pymupdf` (required) · `python-docx` / `pillow` (optional) · everything else is stdlib only.
`build_draft.py --pdf` is a legacy path (depends on `playwright`) — **do not use it**; PDFs are always self-drawn by `export_pdf.py`.

Version is in the `SKILL.md` frontmatter.

## 9. Frequent confusion and anti-patterns (question in, honest answer out)

This table is about mis-usage. For "work we do not take", see the ⑤ table in section 1; for typography detail, see
`references/pitfalls.md` (this README keeps only the traps easiest to fall into; neither place claims to be exhaustive).

| What you might think | What is actually true | Where to look |
|---|---|---|
| "Three gates green, so it is print-ready" | The gates divide labour: correct content, enough content, readable layout and fitness-for-purpose are **different things**. A draft can pass several and still ship one point too small with dozens of font-size tiers; a freshness gate runs before print | the five-gate division in section 1 ②; the `+check` command form in `SKILL.md` |
| "Copy every check and threshold into the docs so I can verify against text" | Not copied. Checks and thresholds are the **script as it now stands**; a prose copy starts rotting immediately. Names and numbers that do appear here are mirrors and common examples | the grep line at the end of section 1 ② prints the live values in place |
| "Print the HTML from a browser and deliver that as the PDF" | Some previewers and corporate policies make the whole document invisible; PDFs are always self-drawn by `export_pdf.py` | trap 1 in `references/pitfalls.md` |
| "Feed a scanned sample straight into `+learn`" | Style extraction needs the PDF **text layer**; a scan has none and looks like an empty journal. OCR into a text layer first | the scan row of section 1 ⑤; `+learn` reads its boundaries out loud when it finishes |
| "Clone the layout of a two-column magazine too" | The renderer is single-column only; columns and text wrap are another typesetting problem. For a two-column journal use it as a **style-guide and content** draft | the two-column row of section 1 ⑤; `examples/` ships a deliberately reversed sample that marks where it fails |
| "No sample journal, but I still want this issue laid out" | Fine - at the price of **no style reproduction, content pipeline only**. That route is written into the routing table, not improvised | the "nothing at all" row of the routing table in `SKILL.md` |
| "It runs without the Cue channels, right" | It runs, but what is missing is capability, not formatting: material comes from you (marked as supplied) and search-type entries are treated as not found. "Optional" means it can run without them, never that they should be skipped - they are recommended and confirmed with you before work starts | `references/cue-onboarding.md`; the recommended block in the `SKILL.md` frontmatter |

## 10. When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.
Symptoms are taken from the **current actual output** of the four scripts (real runs, not design intent): gate scripts
print a human-readable report ending in `── FAIL n / WARN m`; a missing argument prints the argparse usage block and
exits with **code 2**; `crosscheck.py` with no artifact prints
`[ERR] 没有任何成品可校：至少给一个 --html / --md / --pdf`.

| Symptom | Cause | Recovery |
|---|---|---|
| `── FAIL 2 / WARN 5` with `└─` detail lines below | The layout or editorial gate found blocking items (FAIL blocks, WARN does not) | Fix each object named on its `└─` line and re-run; after clearing FAIL, still look at every WARN before delivering |
| `无阻塞项；WARN 建议逐条看一眼再交付。` | Passed, with warnings | Not a green light: judge warning items (font-size tier fragmentation, line-spacing ratio, stray CJK spaces) one by one |
| `usage: audit_layout.py ... error: the following arguments are required: --pdf` | Missing parameter in the command form (each gate needs different ones) | Follow the command forms in `SKILL.md`; `--spec` / `--sample` are optional comparators - without them fewer judgements are made |
| `[ERR] 没有任何成品可校：至少给一个 --html / --md / --pdf` | The artifact set is not out yet, or paths were not passed | Render first, then cross-check; once the three artifacts exist the cross-check is mandatory - what HTML has, PDF may not lack |
| `结论：N 个版本有缺失` with `x MD 缺 n 条:` detail | Text coverage differs across the artifact set | Fill the missing entries per the detail. The text artifact carries a group of purely-layout fields that are exempt by design; the exemption table is `MD_SKIP` as it now stands, visible through the same grep line |
| `[跳过] pdf 不存在：…` | That artifact has not been produced; the script says so instead of crashing | Produce it, then re-run the cross-check |
| The freshness gate reports `FUTURE` (something that has not happened yet) or `STALE` (old news as new) | An event date falls outside the inclusion window, or issue numbers are not contiguous | Always run `check_freshness.py` before print (window defaults to 6 months, `--window` overrides); FUTURE blocks outright, STALE is judged entry by entry |
| The report says it looks like a scan | The text layer is too thin for style extraction | OCR into a text layer first, then `+learn`; do not force the layout |
| Interrupted, unclear where to resume | Eight verbs resume from any stage; artifacts land in the same directory | Read the existing artifacts and ledger in that directory, then enter at the matching verb - resuming is not re-running |

## 11. How to ask (three positive examples, one counter-example)

**Ask with a point in time; the output states its issue and build date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **issue and build date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- **Positive (sample in hand, full chain)**: "Last issue's sample is `~/ink/sample.pdf`, this issue's six columns of
  material are in `~/ink/mat/`; give me an editable draft, and the PDF too" - `+learn` measures the layout, `+brief` fixes
  the positioning with three questions, then the chain runs. Paths supplied up front mean work starts immediately;
  only the missing question comes back to you.
- **Positive (complex: positioning first, content only, no style cloning)**: "First issue of a new in-house journal, no
  sample journal - lay out by content only. Readers are frontline salespeople; after reading they should go do customer
  follow-ups; short plain sentences, no diagrams, columns are listed in `~/plan.md`" - that hits the "nothing at all"
  route: no style reproduction, content pipeline only. Once positioning lands in `positioning.json`, the editorial gate
  judges word bands, forms of address and action-suggestion coverage against it.
- **Positive (resume mid-pipeline)**: "The last `+draft` run finished halfway, the HTML exists - complete the docx and the
  PDF" - the script reads the directory's artifacts and enters at the matching verb instead of re-running earlier steps
  (the eight verbs are in section 3).
- **Counter-example (adjacent need, not this skill)**: "Write the copy and decide the angles, I just want a finished piece"
  - this ships a draft whose **layout and style conventions are correct**; viewpoint and case slots stay for a person
  (first row of section 1 ⑤). "Is this paragraph compliant - give me an opinion" - it yields a checklist and sign-off
  suggestions, never a legal opinion. "Clone a two-column magazine layout" - not rendered here.

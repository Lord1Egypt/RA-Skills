# cue-omni-ontology

**Turn public documents into business knowledge you can update and check.**

Give an agent two releases or reports. Receive **evidenced answers, a searchable change brief with source excerpts, and a reusable knowledge package** for the next update. Start with disclosure tracking, public supplier diligence, or product/competitor monitoring.

**English companion of `README.md` (Chinese primary; repo-local reference — channel pages do not resolve relative links).** beta · Python standard-library tools · No usage telemetry

## See the value

[Microsoft public-disclosure example](assets/public-example/live-preview.md): a fresh parse-to-answer run, including extraction, build/update and evidence queries.

| Your question | What the skill provides |
|---|---|
| Why are there two numbers for one metric? | Separate periods, units, bases and qualifiers, with each source. |
| Must I start over after the next report? | Update the existing package while retaining history, added support and conflicts. |
| Where did this conclusion come from? | Search the brief, expand verbatim excerpts and inspect original URLs/locators. |
| Can my next agent task reuse the work? | Structured knowledge and optional draft OKF core-subset export. |
| Can it take earnings-meeting video or audio? | Yes, as a **bounded local clips/splits (≤256 MiB)** workflow: three 90-second clips from two meetings completed the full chain (build→update×2→validate→query→export-okf) with 8/8 verbatim re-check hits; full-length meeting parsing is **not established** — five public full-length URL attempts were refused and a local full file is stopped by the 256 MiB gate. See `references/av-backtest.md`. |

Begin with one subject, 2–5 public sources and a concrete question. A complete enterprise ontology is not a prerequisite.

## First try: no API key

Ask your agent:

> Use cue-omni-ontology with its bundled demo. Show what a new release adds, where claims conflict, and how to inspect the evidence.

Or run one command from the skill directory (Python 3.10+):

```sh
python3 scripts/ontology.py demo --out /path/to/work/cue-demo
```

Replace the placeholder with a **new directory in your workspace**. Open `cue-demo/brief/brief.html`; no server is needed. Search, filter new/conflicting claims and expand excerpts. Hosts without HTML rendering can read adjacent `brief.md` / `brief.json`.

The example is fictional and makes zero API/network calls. Prior revenue 100 and a later comparative 105 remain conflicting; current revenue 120 and adjusted 115 stay separate; an unmentioned Alpha product is not inferred retired.

## Install and use your sources

```sh
npx skills add huhoo/cue-awesome --skill cue-omni-ontology
```

This install route requires Node.js/npm; copying this directory into your host's supported skills location is also possible. Offline tooling only needs Python. Real parsing uses official [cue-omni-reader](https://github.com/sensedeal/cue-skills/tree/main/cue-omni-reader); follow its [setup](https://github.com/sensedeal/cue-skills/blob/main/cue-omni-reader/references/setup.md) to connect MCP and configure credentials. This package does not install or configure Omni automatically. Keep keys in your secret facility, not chat or Issues. Pointer only, no restated steps: the parsing leg has its official page at <https://cuecue.cn/hub/omni-reader>. What is lost without it is already written in the paragraph below, in this face's own words (no page anchors or verbatim localisation, source records stop at file level), so it is not repeated here. This package's own faces do not list structured disclosure lookups or cross-checking research as evidence legs, so only the parsing-leg page is pointed to; no leg is invented.

Connectivity test for that leg (the parsing leg here is the omni-reader MCP inside your host; no curl replaces it), **written per route**: the host lists tools through the JSON-RPC `tools/list` handshake, and once connected that reply should show these names - a remote-only surface exposes `parse`, `get_parse_status` and `cancel_parse` (three), a Bridge surface adds `read_result`, `read_outline`, `discard_result` and `save_result` (seven in total); the two routes differ, so one fixed count cannot judge both. A skill installed without those names means not connected (installing the skill, configuring the credential and connecting the channel are three separate things, not one), and this package then only takes text you paste in (cost: no page anchors, no verbatim locators, source records stop at file level). Names being present only proves they are exposed, not that parsing works - the URL route is verified by one real URL parse, the Bridge route by one real local-file parse (remote-only cannot read local files); this package neither self-certifies nor runs either for you. Parsing spend follows the server reply; this package neither estimates nor pays it.

Once connected, provide sources and ask:

```text
Use cue-omni-ontology to answer from these two public reports:
1. What is newly disclosed?
2. Which figures require separate bases before comparison?
3. What remains unsupported?
Give me a brief with expandable evidence and a package I can update next time.
```

Then reuse it:

```text
Add this new announcement to the existing package and produce a change brief.
Preserve old records and highlight conflicts. Missing mentions are not deletions.
```

See [task-recipes.md](references/task-recipes.md) for business tasks. Official Omni parses sources; the host model extracts semantics; offline tooling handles locators, versions, queries and briefs. Protocol compatibility is not certification of every host.

## Reduce mechanical extraction work

Agents can copy exact quotes instead of calculating hashes and UTF-8 offsets manually. See [quote-draft.json](assets/demo/quote-draft.json) and [quote-input.md](references/quote-input.md):

```sh
python3 scripts/ontology.py prepare assets/demo/quote-draft.json --out /path/to/work/prepared
python3 scripts/ontology.py build /path/to/work/prepared/input.json --out /path/to/work/v1
python3 scripts/ontology.py update assets/demo/r2.json --base /path/to/work/v1 --out /path/to/work/v2
python3 scripts/ontology.py brief /path/to/work/v2 --base /path/to/work/v1 --out /path/to/work/brief
python3 scripts/ontology.py catalog /path/to/work/v2 --kind changes
python3 scripts/ontology.py query /path/to/work/v2 --concept metric:revenue --period 2026Q1 --with-evidence
```

Repeated quotes require more context or an explicit occurrence. When the exact match fails, `prepare` retries once ignoring table pipes, whitespace and Markdown markers, yet the evidence still points at verbatim source bytes; anything still ambiguous fails, with no semantic fuzzy matching. Use `catalog` first to see the entities, concepts and conflicts in a package (each conflict carries verbatim excerpts for both sides); `query` rejects unknown fields instead of ignoring them. For `needs_scope`, choose a basis, unit, exact validity boundaries or returned fact ID. `--with-evidence` includes bounded verbatim previews and flags truncation. Matching is not semantic verification: inspect headers, footnotes and qualifications.

**Turn a real Omni result into a source**: save the parse call's structuredContent or complete JSON, then:

```sh
python3 scripts/ontology.py omni-source /path/to/work/omni/r1.json --out /path/to/work --id source:r1 --url "https://..." --title "..." --accessed-at 2026-10-07
```

It writes the parsed text byte-for-byte (checking Omni's sha256) and a source record with pages; paste it into draft.json and run `prepare`. Only source-PDF page anchors count and no page is guessed; it starts no parse, reads no key and spends no credits. Writing with `save_result` or keeping only Markdown loses the pages, so the tool refuses that by default.

**Optional numeric pack**: the host computes annual-report deltas, restatements and balance checks with deterministic code, and a model extracts only narrative items. `numeric-import` checks that every figure has unit, page and table id for both years and that excerpts are verbatim on the source page; `numeric` shows them in review order (drivers -> consequences -> explained-normal events). It does not score or warn. Credit-risk annual-report tasks extract the [fixed section set](references/credit-risk-sections.md).

## Deliverables and verification

- **Human entry point:** offline `brief.html`, Markdown counterpart, sources, scope distinctions, changes and excerpts.
- **Reusable knowledge:** `knowledge.json`, `sources.jsonl`, `changes.json`, `run.json` and exact source snapshots.
- **Extraction notes:** host-written `extraction-notes.md` records questions, gaps, failed sources and semantic review.
- **Optional interchange:** `export-okf` creates draft concepts targeting the OKF 0.2 core subset; external consumer imports need separate verification.

The [verification record](references/verification.md) distinguishes fresh parsing, saved-output replay, independent synthetic use and remaining limits. The [Microsoft run](references/live-verification.md) produced 21 source claims from two sources and retained all 11 baseline claims after updating. It demonstrates a bounded workflow, not general extraction accuracy or proven customer ROI. In the [holdout backtest](references/verification.md) (40 annual reports, 7,598 pages) evidence validity was clearly higher than two baselines, but root-cause ranking missed the pre-set pass bar and the early-warning claim was falsified; the three sets of numbers and the limits are stated together in the verification record.

Offline self-check:

```sh
python3 -B scripts/test_ontology.py
python3 -B scripts/test_numeric.py
```

## FAQ and anti-patterns (what you try -> declined, because -> where to go)

Authoritative text lives in `SKILL.md`, `references/knowledge-contract.md` and `references/update-policy.md`;
this table gathers it and does not restate it exhaustively.

| What you try | Declined? Why | Where instead |
|---|---|---|
| A newer source omits a fact, so treat it as withdrawn | **No.** The update policy states plainly that "not mentioned" is not deletion - silence is not negation | Record a change only when a filing withdraws or supersedes; otherwise keep the old object with its basis state |
| Reuse the same ID with a different meaning | **No.** The updater refuses same-ID meaning swaps; on definition or source ID conflict it keeps the old object, proposes a new ID and explains | Open a new ID for the new meaning, keep history, retain the conflict side by side |
| Have the script merge two values into one conclusion | **No.** The knowledge package stores **directly disclosed assertions** only; computation and judgement belong in the answer with inputs named | Keep conflicts visible in the brief (100 and 105 coexist); no silent overwrite |
| Describe `ontology.py` as an automatic extractor | **Not true.** Division of labour is fixed: the official parser reads material, the **host model does semantic extraction**, offline tools check structure and consistency | Write `extraction-notes.md` covering scope, failed sources and manual review |
| Assume a public-looking URL is reachable | **No.** URL shape proves nothing about public accessibility; retrieval supplements only inside authorised research scope, no crawler | Use files or links the user explicitly provides, or fetch through Cue channels and keep snapshots |
| Pipe `export-okf` straight into an external system | **Untested.** Export is a draft targeting the OKF 0.2 core subset; consumer compatibility is verified separately | Verify on the consuming side first; this package promises only the shape it emits |
| Check a sentence or figure against the filing page by page, or get a lead piece with page citations | **Not this package's job.** This package builds updatable knowledge packages, change briefs and the numeric pack | [cue-lead-pieces](../cue-lead-pieces/README.en.md) in this repository: quote verification and lead pieces |
| Use the numeric pack or change brief as a default early warning or automatic risk discovery | **No.** The holdout backtest falsified the early-warning claim and root-cause ranking missed the pass bar; the ordering is a review order | A person judges from the verbatim evidence; see the [verification record](references/verification.md) |

## When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.
Written from the **current actual output** of `scripts/ontology.py` (real runs): verification commands print **one JSON
line**. Success looks like `{"status": "valid", "counts": {...}, "semantic_verification": "not_established_by_scripts"}`
(exit 0); failure looks like `{"status": "invalid", "error": "<cause>"}` (exit 2, on stderr); a missing subcommand or
argument prints the argparse usage and exits 2.

| Symptom | Cause | Recovery |
|---|---|---|
| `{"status": "invalid", "error": "knowledge integrity mismatch"}` | Package content no longer matches its integrity record (`knowledge.json` hand-edited, or objects swapped under one ID) | Do not hand-edit package files: re-run `build` / `update` from sources; if a revision is truly needed, open a new ID and keep the old record |
| `{"status": "invalid", "error": "source hash mismatch: <source ID>"}` | The stored snapshot disagrees with the recorded hash (source text changed or was replaced) | Re-parse that source into a new snapshot and a new run; keep the old snapshot, never rewrite history |
| `{"status": "invalid", "error": "[Errno 2] No such file or directory: '<path>'"}` | The path handed to `validate` is not a complete package directory (one of `knowledge.json` / `run.json` / `changes.json` missing) | Point at the directory `build` emitted; `demo` output lives in version subdirectories such as `<out>/v1`, `<out>/v2` |
| Messages shaped like `<label>: invalid ID`, `<label>: duplicate ID <key>`, `duplicate JSON key: <key>`, `invalid value for <type>` | Structure or value violates the contract (ID regex, duplicate keys, value type) | Fix per the field spec in `references/knowledge-contract.md`, then re-run the same validate |
| `usage: ontology.py [-h] {build,update,validate,query,catalog,export-okf,feedback,review,numeric-import,numeric,omni-source,prepare,brief,demo} ...` plus `error: the following arguments are required: command` | No subcommand, or a required parameter was skipped | Run `python3 scripts/ontology.py <subcommand> --help` first (e.g. `demo` requires `--out`, and **the output directory must be new**) |
| `omni-source`: `not JSON. Plain Markdown (or text written by save_result) has no grounding sidecar` | You saved Markdown or text written by `save_result`; the pages are gone | Save the parse call's structuredContent or complete JSON; if text is all you have, pass `--text-only` (no pages) |
| `omni-source`: `the result has no source-PDF page anchors` | The result is detail=text, has rendered-page anchors only, or is not a PDF | Pass `--text-only` to package with text ranges; a grounded re-parse is billed, so ask the user first |
| `omni-source`: `Omni status is failed SOURCE_ACCESS_DENIED` / `DETAIL_CAPABILITIES_UNAVAILABLE` | Omni cannot fetch that URL (measured for SEC EDGAR), or this Bridge cannot do grounded parsing of a local file (measured on 1.8.3) | Note it in the coverage statement; obtain the text yourself and package it with `manual_page` or text ranges, never as Omni pages |
| `omni-source`: `does not match its sha256 digest`, or `read_result(...)` expired | An artifact read came back incomplete, or the Bridge-local result expired | Read again; after expiry a re-parse may be billed, so ask the user first |
| `numeric-import`: `excerpt is not verbatim on FY<year> p<page>` / `page not in sources` | The excerpt is not the page's text, or the page is missing from `FY<year>.pages.jsonl` | Copy the excerpt from the source page and check the page; do not reformat numbers |
| Validation passes yet the extraction is semantically wrong | Scripts check structure and consistency only - the field `semantic_verification` literally reads `not_established_by_scripts`; scripts do not prove semantics | Review line by line with `review` and the expandable-source brief. That division is the design, not a defect |
| Want to confirm the tool itself works | — | Local self-checks: `python3 -B scripts/test_ontology.py` and `python3 -B scripts/test_numeric.py` (listed under Deliverables and verification; test count comes from the run itself) |

## How to ask (positive examples and one counter-example)

**Ask with a point in time; the output states its source date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **source date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- **Positive (first try, no credentials)**: "Use cue-omni-ontology with its bundled demo: once new material is added,
  which facts are new, which conflict, and where is the basis?" - or one command,
  `python3 scripts/ontology.py demo --out <a brand-new working directory>`: no network, no parse API, and it emits a
  brief whose evidence expands to source text.
- **Positive (two real documents)**: "Answer from these two public reports: (1) what disclosure is new; (2) which
  numbers differ in basis and must not be compared directly; (3) which questions lack support. Give me a brief with
  expandable sources and save an updatable knowledge package." - the template in Install and use your sources; sources
  and task handles are kept separately, and the output directory must be new.
- **Positive (complex: a second update with boundary demands)**: "Add this new announcement to the existing package and
  give me the change brief. Keep old records, highlight conflicts needing review, and **do not treat 'not mentioned' as
  deletion**; unit, period, basis, exclusions and validity go into the fact layer - do not merge them into one number
  for me." - exactly what the updater enforces under update-policy: refuse same-ID meaning swaps, keep conflicts,
  deduplicate identical statements.
- **Positive (English phrasing)**: this package's frontmatter trigger set is already bilingual
  (`ontology extraction` / `disclosure tracking` / `evidence briefs` / `numeric pack` / `知识包` / `变化简报`),
  so either language can open it.
- **Counter-example (adjacent need, not this skill)**: "which of these two companies is stronger, give me a verdict" -
  the decision-shaped evidence chain belongs to `competitive-brief`; "lay out anchor-bound public risk facts for this
  listed issuer and account for what could not be checked" - `dd-checklist`; "translate this foreign book, then index
  it" - `long-doc-translation`. This package turns public material into an updatable, verifiable knowledge package plus
  change briefs.

## Domestically reachable evidence paths (when overseas sites do not load)

The offline tools (`ontology.py`, `numeric.py`, `omni_source.py` and the two tests) depend only on the Python standard library, and **demo mode needs
no API key and makes no network call** - so "let me see what this is" has no extra barrier in a domestic environment.
When actually gathering material, three paths already exist in this package:

1. **Files the user provides come first.** PDF, HTML or plain text can enter parsing and the knowledge package directly -
   no overseas site needed. Domestic public material (exchange and disclosure-platform announcements, vendor Chinese
   sites and documentation portals, industry-association reports, WeChat public-account articles) is most reliable here.
2. **If an overseas site will not load, do not route around it.** Have the page **exported to a file by the user** and
   hand that to the parse channel. This package builds no crawler and never assumes reachability from URL shape.
3. **Supplementary retrieval stays inside authorised research scope** via the host's retrieval tools; whatever comes
   back keeps its snapshot and provenance.

None of the three changes the deliverable shape: the package still stores only directly disclosed assertions, conflicts
stay side by side, snapshots and hashes remain re-checkable, and every source records its ID and parse date. A source
that cannot be obtained is marked "not obtained" - **no inference, no silent overwrite**. That is the same discipline
as update-policy; a restricted network does not loosen it. This section promises no unopened data domain and no
promise that a specific site will load.

## Feedback that matters

**Did your own documents answer your question? Would you add the next release? Where did correction still take effort?** These signals are more useful than download counts.

`feedback PACKAGE --out NEW_FILE` creates a local draft. Review it and decide whether to submit a [public issue](https://github.com/huhoo/cue-awesome/issues/new); nothing is uploaded automatically. Share private material, contacts and business context through a separately agreed private channel.

For internal-document monitoring, downstream agents/ERP/CRM, domain schema review or full on-prem deployment, describe the **task, update frequency, current review effort and target workflow**. These are discovery topics, not production capabilities already delivered by this public skill.

## Boundaries and license

Store directly reported claims; disclose inputs for derived calculations and judgments in answers. The audio/video capability is bounded, not blanket: "includes audio/video" holds only under the "bounded local clips/splits (≤256 MiB)" workflow (the What this decides section of `references/av-backtest.md` is the single source of this wording); the verbatim re-check proves excerpt-to-parser consistency, i.e. integrity, not semantic truth. Definitions remain candidates; local review records do not provide enterprise IAM or operational authorization. Cloud parsing of a local file is not full on-prem deployment.

Briefs include bounded source excerpts; complete packages contain parsed text. Check source conditions and authorization before sharing. Code/docs are [MIT](LICENSE); public access is not blanket permission to redistribute entire reports. The Chinese README is canonical user documentation; `SKILL.md` (Chinese-first) is the canonical agent entry, with `SKILL.en.md` as its synchronized translation. Judgements are the scripts as they now stand; fixtures evidence only the cases they actually run, not an exhaustive claim.

# civil-appeal-turnaround

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

**You hired a lawyer for the first instance, and you still lost. The second instance is yours to run - this skill promises no reversal; it hands the case back from your lawyer's head to the person who knows it best.**

**Give it a lost judgment; get back a second-instance case system you can file.**

This is not "draft me an appeal" — it **reverse-engineers the judgment into the judge's own chain of reasoning**, locates the level at which the issue was framed wrong, recovers what was truncated, omitted or split off from the raw materials, and finally lays the argument out as a **ladder** instead of a single bet. So what it hands back is a set of interlocking documents, not one isolated appeal brief.

**Input**: the first-instance judgment + whatever loose material you hold (statement of claim, hearing transcript, recording transcripts, chat records, lookup results)
**Output**: `今日三件事.txt` (day-one three actions) · `主控清单.md` (master checklist) · `复核报告.md` (review report) · `上诉状.md` (appeal) · `配套文书包.md` (filing pack) · five tables (breakdown / diff / ladder / ledger / loss three-faces) · **a Word filing copy** (`*.docx`, exported from the markdown: official-document typography + page numbers in the footer)
**Cost**: half a day for the Phase 0 close-out, then it scales with the judgment and the case file; **the 15-day appeal window is a hard constraint**
**Lead channel**: statutes, judicial interpretations and similar cases can be listed as candidates via `cue-research` - **a lead is not a conclusion**; no outcome is promised, and nothing enters the tables before it is verified against official sources.

## Opening: four verbs on the sign

Every action you take reduces to four verbs, and each table is where one of them lands. The Chinese labels below are kept verbatim in their canonical form - the case files carry them, so treat them as your anchors.

| Verb | What you do | Lands in |
|---|---|---|
| `盘点` *(take stock)* | Break the judgment into its chain of reasoning, then split what you lost into three faces: inherently unfavourable, self-inflicted by how the case was run, and errors the judgment itself made | `判决书拆解表.md` + `败诉三面表.md` (template in `assets/`) |
| `搜集` *(gather)* | Diff your source material against the judgment's excerpts word by word; whatever the diff turns up becomes the to-be-obtained list - three applications: evidence retrieval, order to produce, schedule of new evidence | `证据比对表.md` + those three applications |
| `查证` *(verify)* | Grade every fact A/B/C and leave the "check it before filing" line on every article number; nothing unverified enters a document | `事实台账.md` + the red-line list |
| `todo` *(schedule)* | Put the first three on a calendar and count backwards: T+0 / T+1~3 / T+4~7 / deadline | `主控清单.md` (preconditions + to-do tables) |

Phases 0-6 are not a fifth thing next to these four verbs - they are the **fine print** of them (see section 2).

### Day one: three steps

Three steps today, each with what skipping it costs:

| Today | How | What happens if you skip it |
|---|---|---|
| 1. Fix the service date, compute the deadline | 15 days for a judgment, counting from the day after service; take both dates from **the tail of the judgment and the proof of service**, never from memory | Miss the window and the first-instance judgment stands and you start from behind; the only statutory relief is narrow — if a deadline was missed due to force majeure or another legitimate reason, an extension may be applied for within ten days after the obstacle is removed (Article 86), and the court decides whether to grant it |
| 2. Check the preservation status | Already preserved - the continued-preservation application is the top priority (appealing does not extend preservation); not preserved - first estimate how far the other side can move assets after the claim was dismissed | Preservation is released or lapses; even a reversal collects nothing |
| 3. Check the representation status | Counsel withdrawn - delete counsel's line from the appeal and change the service address **in writing** | Papers go to the former agent or the old address, and deadlines burn while you never see the notice |

These are the first three items of Phase 0; the judgment breakdown and the evidence diff come after them, not before.

---

## 1. How this differs from "write me an appeal"

### ① Find the frame error first, not the missing evidence

Most losses are not "insufficient evidence". When a judgment says "the existing evidence cannot prove…", it usually means the issue was framed as one that the weaker party must prove, while every item of proof sits with the other side — who did not even appear.

The test is one sentence: **under the judgment's frame, is every piece of evidence needed held unilaterally by the other side? If yes, the frame is wrong** — gathering more evidence inside that frame is futile; the second instance has to redefine the issue.

### ② Diff the exhibits word by word, not from memory

What the judgment quotes decides what the judge actually "saw". Put each item's source material next to the judgment's excerpt and mark three kinds of divergence: **truncated / omitted / split**.

Finding a truncation is hands-on: **locate the last ellipsis in the judgment's excerpt, go back to the original, and read the one to three sentences immediately after it.** A judgment that stops there is usually stopping because of what comes next.

### ③ Lay the argument as a ladder, not a single bet

The failure mode of staking everything on one cause of action: the appellate court declines that route and the whole case collapses with no fallback.

```
Tier 1  Main: fits the facts best, needs no new evidence
   ↓  "even if the court finds…"
Tier 2  Alternative: also no new evidence, different elements
   ↓
Tier 3  Requires new evidence
   ↓
Tier 4  Fallback: requires the court to clarify the legal relationship
```

**Hard test: the first two tiers must not depend on any new evidence** — they rest only on A-grade facts (already found by the judgment) and B-grade facts (submitted but never addressed).

> **Take "reverse the original judgment" with the tiers that need no new evidence; then make "facts ascertained" solid with the tiers that do.**

---

## 2. The workflow in detail: six phases (the four verbs expanded)

| Phase | What happens | Output |
|---|---|---|
| **0 · Close-out** | Fix the service date and appeal deadline, the preservation status, the representation status | preconditions table |
| **1 · Judgment reverse-engineering** | Rebuild the chain of reasoning, find the largest leap, five-level root cause; fill the three-faces sheet in the same pass | `判决书拆解表.md` + `败诉三面表.md` |
| **2 · Evidence diff** | Source vs excerpt; mark truncated / omitted / split | `证据比对表.md` |
| **3 · Legal ladder** | Main / alternative / fallback; per tier, elements and "what the judgment skipped" | `法律阶梯表.md` |
| **4 · Fact ledger and discipline** | A/B/C provenance grades, red-line list, traceable corrections | `事实台账.md` |
| **5–6 · Documents and filing** | Appeal (with a summary up front) + companion documents, filed the same day | `上诉状.md` / `配套文书包.md` |

### Two optional channels for material and for leads (both bounded)

This skill's own scripts and flow stay offline. Both channels below are **auxiliaries the user installs separately**, used only where material cannot get in and where candidate leads are needed; whether to use them is confirmed with the user, and their format list, size cap and covered domains are taken from their own docs as they now stand - this package neither copies those tables nor promises outcomes. Configuration pointers for the two optional auxiliaries, pointers only and no restated setup steps: the material channel `cue-omni-reader` runs on the parsing leg, whose page is <https://cuecue.cn/hub/omni-reader>; the research channel `cue-research` is its own runner (it ships its own script); this package does not route it through the data-leg page; its credential is the same key - get one at <https://cuecue.cn/hub/api-key>. This package names no primary leg: the heading above marks both channels as optional and bounded, and the paragraph says they are auxiliaries the user installs separately.

**Material channel · `cue-omni-reader`**: when evidence is a scan, a recording, a video or a packed bundle and the agent's own upload path refuses it (format or size), have this tool parse it into **locatable text** (page and time anchors included) before it enters the case directory. Every bound, none dropped:

- **Formats follow the local allowlist as it now stands**: `rar`/`tar`/`tgz`/`gz`/`bz2` are included, `parquet`/`xmind`/`mmap` are not - the authoritative table is the compatibility doc shipped inside that auxiliary package itself; a copy here would start rotting at once, so none is made.
- **Per source ≤256 MiB**: larger inputs are stopped before parsing by the `constraints.max_bytes` gate (measured 268,435,456 bytes) - that is not a parse failure.
- **Audio/video is proven only as bounded local clips/splits**: full-length meeting parsing is not established (measured: three 90-second clips from two meetings completed the chain with 8/8 verbatim re-checks; five public full-length URL attempts were refused, and a local full file is stopped by the cap above).
- **Whether a source parses, and what it costs, are decided by the service response**: this package claims no unopened domain and infers no rate.
- **Transcripts still obey this skill's grading discipline**: homophones and mishearings are not auto-corrected (parser output is kept as returned); a recording must be **re-listened to on its original carrier** before it can be graded A/B - until then it sits at grade C, marked pending.

**Research channel · `cue-research`**: for Phase 1's "provision that should have applied but did not" and for the elements on each rung of Phase 3's ladder, it can search statutes, judicial interpretations and similar cases, producing a **candidate list** - every article text and case number first enters as **grade C (pending verification)** marked "awaiting verification against official sources", and may rise to B only after being filed into the record — the same provenance discipline this skill already applies (the eight hard constraints and the six-phase semantics are untouched). Bound: that channel covers public data sources only, its domain table is its own doc as it now stands (not hard-coded here), and **a lead is not a conclusion** - no promise of an outcome, no promise that whatever is found is usable.

---

## 3. Eight hard constraints (violating one means redoing the work)

| # | Constraint |
|---|---|
| 1 | **Facts the judgment already found come first** — start from what the judgment conceded |
| 2 | **Every claim carries a provenance grade**: A = found by the judgment / B = submitted but unaddressed / C = to be obtained. **Never use C as A** |
| 3 | **No prejudging, no invention, no inference** — money flows and party attribution are always stated in the open / alternative form |
| 4 | **A corrected characterisation must be applied repo-wide and left traceable** — state "the previous conclusion is void" and re-check every inference that leaned on it |
| 5 | **Money > deadline > evidence** — preservation and the appeal window outrank every evidence-gathering action |
| 6 | **Keep the grievance thread out of the litigation thread** — complaints and accountability claims go in separate files |
| 7 | **Redact the output** — ID numbers, phone numbers, addresses, account numbers become placeholders |
| 8 | **Never shortcut a procedural qualification question** — new evidence, adding claims on appeal, whether a party may testify: check explicitly |

---

## 4. Getting started

**Install this skill (primary route)**: `npx skills add huhoo/cue-awesome --skill civil-appeal-turnaround` - this line installs this package only; afterwards re-list installed skills and the name `civil-appeal-turnaround` must appear, otherwise the files are not in place. The `cp -r` block below is the **manual fallback for environments without a CLI**, not the primary route.

```bash
# 1. Fallback: manual placement when there is no CLI (the primary route is the npx line above)
mkdir -p ~/.workbuddy/skills
cp -r civil-appeal-turnaround ~/.workbuddy/skills/

# 2. Initialise a case working directory (five tables + master / report / appeal / pack skeletons + day-one three actions)
python3 ~/.workbuddy/skills/civil-appeal-turnaround/scripts/init_case.py ./my-case --case "(2026) Jing XXXX Minchu XXXX"
```

On first entry, read `assets/败诉三面表.md` (the take-stock sheet) and the other four table templates, then `references/07-worked-example.md` (a redacted run through the whole flow). Every file under `references/` opens with a **door-sign anchor** (verb / phase / where it lands / where to stop), so you can follow the anchors without re-checking the mapping table in `SKILL.md`.

### Self-check

```bash
python scripts/init_case.py --help          # usage; no network
python scripts/init_case.py /tmp/case-demo  # writes 10 files, never overwrites existing ones
ls /tmp/case-demo                           # expect 5 tables + 4 skeletons + today-three-things + 归档/
python3 scripts/check_tables.py --selftest  # offline re-run of the eight guard samples (4 good + 4 bad); expected last line "selftest: ALL GREEN（好样 4/4 · 坏样四道 4/4）", exit 0
python3 scripts/check_tables.py scripts/fixtures/good-ledger.md   # expected PASS (scanned 13 lines, 0 findings)
python3 scripts/check_tables.py scripts/fixtures/bad-banword.md   # expected FAIL (emits E-BANWORD: prejudgment wording, C used as A)
```

All thresholds live in the current `scripts/check_tables.py`; the four lanes are format / anchor & grade / no-prejudgment / counts & declaration, and this page does not restate the word list. The blank templates under `assets/` are meant to fail the gate — by design, not a defect.

---

## 5. Boundaries

- What this skill produces is **working drafts and structure, not legal advice**; **every article number must be checked by the user before filing**, and the skill marks them all "check the article number before filing".
- It does not replace a lawyer, nor the court's own view on procedural questions. Deadlines, amounts and filing channels follow the receiving court's current rules and notices.
- This skill's scripts and flow are offline and self-contained: no network, no external repository, no API calls. The two channels at the end of section 2 are optional auxiliaries the user installs separately, used only for parsing material and gathering leads; whether they are available, what they return and what they cost follow the service response - this skill promises no unopened domain and no outcome.
- Where article numbers and deadlines would otherwise appear, the skill deliberately uses **descriptive wording instead of hard-coded numbers** — the risk of a model misremembering an article is held by that "check before filing" gate.
- **Two exit rules (a point in time, and "not found")**: the deliverable labels its material date on the first line (judgment signature date / proof-of-service date), and when it differs from the date the user means, the text never says "today" or "latest" but reads "as of <date>". Any date, article number or amount not present in the case material is written as "not found" and put on the pending list - never filled from memory, never left blank as a stand-in.
- **One explicit confirmation before anything irreversible**: before filing, paying or sending, restate target + consequence + timing and wait for a clear reply; bare replies like "ok", "mm" or "sure" are not confirmation. While the step has not happened, completed-form wording ("I've filed it for you") stays out of the text.
- **Expectation management**: reversal and remand on appeal are not common, and **this skill does not bet on a reversal**. It does the controllable part - reframe the issue, recover what was truncated, keep watch over the money and the deadlines. The outcome is the court's to decide; run the four verbs and what you hold is **a set of sourced tables, a filing-ready appeal, and a calendar counted back from the deadline**. That is the whole of what is promised.

### Guarding against a second harvest: three warnings

Losing once makes you easy to charge twice. Check all three:

1. **Signs of unfreezing or asset movement**: after the claim is dismissed, the other side may apply to lift preservation and move assets. React with the continued-preservation application and its expiry date, not with the appeal draft first - that is what constraint 5 ("Money > deadline > evidence") is for.
2. **"We will win it for you" agents and templates of unknown origin**: anyone who promises the reversal in advance, and any "second-instance reversal template" sent without reading your file, is a risk item rather than a resource. Constraint 2 requires a source and a grade for every claim; a document generated from nothing in your record only adds a characterisation you will later have to correct (constraint 4).
3. **Self-media legal answers**: a short video or post telling you "write the appeal like this" stays unusable until the article text and its current validity are checked against the official source. Search results enter as grade C, marked "awaiting verification against official sources", and may rise to B only after being filed into the record - the same discipline as the research channel in section 2.

### Minimum outsourcing: one paid checkpoint, not a return to full representation

By default **you run the case**. Two situations justify paying once: the amount at stake is large; or a procedural-qualification question is live - whether something counts as new evidence on appeal, whether claims may be added, whether a party may testify. Constraint 8 forbids this skill from answering those for you.

Do it as **one verification session**, not a re-delegation: bring `事实台账.md` plus the two sections of `复核报告.md` (`序：一句话结论` and `二、扭转路径`), write down the three questions you actually need answered, and pay for those three only; you still make the corrections and you still file. An outside opinion is marked pending like anything else - it does not replace your own grading.

## 6. Dependencies

- `python3` (only `scripts/init_case.py`; standard library, no third-party packages, no network requests)
- `python-docx` (**optional**, needed only by `scripts/export_docx.py` to produce the Word filing copy): `python -m pip install python-docx -i https://pypi.tuna.tsinghua.edu.cn/simple`. Without it you simply get no `.docx`; everything else is unaffected, and the script reports the install command rather than degrading silently.
- Apart from the two **optional** auxiliaries above (`cue-omni-reader` for material, `cue-research` for statute and case leads) there is no other dependency: absent tools degrade without error, the user confirms before either is run, and the judgment plus materials come from the user - when material cannot get in, see the channel section at the end of section 2. What is lost is stated in the same sentence: scans cannot be read and the statute/case-lead leg is missing - the gap is channel evidence, not formatting.

The channel route on this face (this package ships no connectivity script - the curl lines below are the whole action; what they prove is catalog reachability and that your key is accepted, not that this skill fetched anything):

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

The three layers are never equivalent: skill installed != credentials configured != channel connected. The anonymous `GET` proves **catalog reachability** only; the key is proven *accepted* once a `tools/list` reply comes back with it attached - pass = HTTP 200 with a non-empty `result.tools` (shape only; no tool names or counts are promised here). The `cue-omni-reader` leg is the MCP connection in your host: it is connected once the host tool listing (the same JSON-RPC `tools/list` handshake) returns `parse` and `get_parse_status`; a skill installed without those names means not connected, and only the user-supplied route stays open. The key comes from your local credential facility - never into chat, never echoed back; this block adds no new credential read.

## 7. Contents

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions (Chinese primary) |
| `references/01-judgment-reverse-engineering.md` | Reverse-engineering: chain rebuild, frame-level error, five-layer root causes, **root cause to three-faces**, 20-item checklist |
| `references/02-evidence-diff-protocol.md` | Evidence diff: spotting and phrasing truncated / omitted / split |
| `references/03-legal-ladder.md` | Liability ladder: four patterns, how to write the three elements of apparent authority |
| `references/04-fact-ledger-and-discipline.md` | Fact ledger, A/B/C grades, correction mechanism, red-line list |
| `references/05-self-represented-filing.md` | Self-represented practice: deadlines, filing channels, fees, file inspection, qualification checks, **minimum outsourcing: paid spot-checks** |
| `references/06-document-pack.md` | Pack structure, how to write the summary, sync mechanism, version notes, **exporting and fidelity-checking the Word filing copy** |
| `references/07-worked-example.md` | A redacted worked example |
| `assets/` | Five table templates (breakdown / diff / ladder / ledger / loss three-faces) |
| `scripts/init_case.py` | Case directory initialiser |
| `scripts/export_docx.py` | Markdown to Word filing copy (official-document or brief style), with `--check` text-coverage verification |

Version history lives in `CHANGELOG.md`. `README.md` is the Chinese primary of this file.

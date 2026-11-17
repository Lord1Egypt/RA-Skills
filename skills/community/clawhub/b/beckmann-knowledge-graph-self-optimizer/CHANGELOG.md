# CHANGELOG — beckmann-knowledge-graph-self-optimizer

All notable changes to this skill will be documented here.
Format based on Keep a Changelog, versioning follows SemVer.

---

## \[1.1.0] — 2026-09-24 — Security Audit Fixes + Splitter Rename + HTML programs made more user-friendly + Sub-skills operate autonomously    

### Changed


* Graph-Overview-Generator.html and Knowledge-Graph-Splitter.html are now easier to use
* Added significantly more automation; sub-skills operate autonomously.
* Known limitation: no "scientific_status" field in the new subgraph and the new relations.


* `HTML-Tools/KnowledgeGraph-Splitter.html` renamed to `HTML-Tools/Knowledge-Graph-Splitter.html` (kebab-case consistent with all other HTML tool names)
* All references to `KnowledgeGraph-Splitter.html` updated in `SKILL.md`, `README.md`, and `Sub-Skills/Step1-Understanding-Prompt-Template-V3.md`
* `KnowledgeGraph-Splitter.html` added to Archived/Deprecated table in `SKILL.md` with rename note

### Fixed (Security Audit — ClawHub Scanner)

* `README.md`: Added explicit data-handling notice in Operating Policies — informs users that graph content (entity IDs, descriptions, hub lists) is copied into generated output files and should be treated as potentially sensitive
* `HTML-Tools/Step5-Graph-Merger-V1.html`: Added confirmation dialog before auto-download of `graph_vNEXT_optimized.json` — user must explicitly confirm before file is saved (addresses forced-download UX finding)
* `SKILL.md` Phase 5 Step 5b instruction block updated to reflect confirmation dialog step

---

## \[1.0.0] — 2026-09-19 — Initial ClawHub Release

First stable, publish-ready version. Deliberately slim and focused on correctness.

### Added

* `SKILL.md` v1.0.0 with:

  * YAML frontmatter (`name`, `version: 1.0.0`, `description`, `author`, `license`, `tags`)
  * `Requirements` and `Quickstart` sections
  * Folder renamed `Results and Resources/` → `Results-and-Resources/` (no spaces, Linux-safe)
  * Operating Policy clarified: HTML tools are client-side, offline, user-operated, no external upload
  * State Detection logic priority top→bottom with explicit rule for both breadth+depth tracks present
  * Post-Merge Protocol fixed: `graph.json -> old\_graph.json` then `graph\_vNEXT\_optimized.json -> graph.json` (fixes Windows `ren` failure from V1)
  * File Registry fixed: 2-column valid Markdown table, no broken status emojis
* `package.json` v1.0.0 — ClawHub entry `SKILL.md`, keywords, files whitelist, `clawhub` metadata
* `Sub-Skills/` cleaned for ClawHub (all English only, no legacy hints):

  * `Step1-Understanding-Prompt-Template-V3.md` (11 KB) — now expects `graph\_overview.json + 4 Parts` as input, no size-check proposal A-D, planning of split already done in Phase 1a/1b. Output filename kept `UNDERSTANDING-REPORT-V3-...` for state-detection compatibility.
  * `Step2-Breadth-Topic-Suggester-Prompt-Template-V1.md` (8 KB) — removed `EXACT V6`, `V12`, `Schritt2A`, static candidate lists, old German examples. Dynamic derivation from `typeHistogram <8` + Gaps only.
  * `Step2-Depth-Topic-Suggester-Prompt-Template-V1.md` (10.7 KB) — same cleanup, inverted logic: `DOES exist >=10`, anchors >=5 (3 same cluster), relations >=8
  * `Step3-Subgraph-Builder-Prompt-Template-V1.md` (17.5 KB) — removed `V1 (V4 Roadmap)`, `from old Y/X`, `PLANUNGS-SKIZZE`, `ABSCHLUSS-PROTOKOLL`, `708 entities / 491 types` as mandatory. Kept core validations K1-K4, J1-J4, D1, B1. Now fully English, `PLANNING SKETCH` + `FINAL PROTOCOL + STOP POINT`.
  * `Step4-Relation-Builder-Prompt-Template-V3.md` (13.6 KB) — removed `CHANGELOG V2→V3`, `ROADMAP-...`, `Legacy V151`, `Known Hubs D5/E2/G7`. Kept Tier system Tier0 forbidden, rationale only in planning sketch `Connects to '...' (id) through...`, JSON 4 fields rationale-free, directly mergeable.
  * `Step5-Graph-Merger-Prompt-Template-V1.md` (6.8 KB) — removed `Build Doc ROADMAP-...`, `Flow Doc ...`, `JSON-Merge-Tool V5 universell.html`. Only 3 inputs → 1 output, whitelist + green checks, rename + cleanup list.

### Fixed

* V1 blocker: File Registry table had 3 columns header but 2 columns rows → broken Markdown — fixed to 2 columns
* V1 blocker: Frontmatter after title → not detected by ClawHub — moved to first line
* V1 blocker: Post-Merge `ren graph\_vNEXT\_optimized.json graph.json` failed when target exists — fixed to backup to `old\_graph.json` first
* V1 blocker: `Results and Resources/` with space → Linux/CLI issues — renamed to `Results-and-Resources/`

### Kept for Compatibility (intentionally)

* `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` filename stays V3 even though template is V4 — state detection expects V3. Rename planned for V1.1.
* Sub-Skill filenames keep their old V numbers (V1, V3) even though internally cleaned to 1.0.0 — avoids breaking `SKILL.md` File Registry in V1.0. Full rename planned for V1.2.

---

## \[1.2.0] — Planned — Polish and Docs

Planned improvements, stepwise, without breaking V1.0 logic:

### Planned Added

* Mermaid diagram in `SKILL.md` Cycle Overview (instead of ASCII) — renderable on ClawHub
* `Troubleshooting.md` — common errors: wrong filename rejected, entityIndex collision, ID hygiene D1
* Explicit handling for case `graph.json` + `graph\_vNEXT\_optimized.json` both present (priority already documented, but add example)
* Optional: shorten transient filenames `subgraph\_breadth\_new\_information\_for\_Relation\_Builder.json` → `subgraph\_breadth\_info.json` with backward-compatible alias

### Planned Changed

* Rename `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` → `UNDERSTANDING-REPORT-V4-From-Parts-And-Overview.md` and update State Detection + all Sub-Skills references
* `File Registry` Status column refilled with `active` / `deprecated` badges instead of empty

### Planned Fixed

* None — V1.0 is stable, but collect user feedback from ClawHub installs

---

## \[1.3.0] — Planned — Naming Consolidation

* Consolidate Sub-Skill filenames to match internal version: `Step1-Understanding-Prompt-Template-V4.md`, `Step2-...-V2.md` etc., and update `SKILL.md` File Registry accordingly
* Add `CONTRIBUTING.md` with review gate expectations

---

## \[Unreleased] Ideas (not committed)

* Optional `results/` alias for `Results-and-Resources/` for shorter paths
* Validation script `validate-state.js` that checks `Results-and-Resources/` content against State Detection table
* Example `graph.json` (tiny 50 nodes) for quick ClawHub tryout

---

## Versioning Notes

* V1.0.0 is the first ClawHub publication. Previous internal versions (V1, V2, V3, V151 etc.) were German and prefix-based (E1, G4, Y5) and are now archived under `Archived / Deprecated` in SKILL.md.
* For ClawHub, only English templates are published.

# LLM-Wiki Unified Agent Protocol

> This document guides Claude Code, OpenClaw, and other AI Agents on how to use llm-wiki.
> `AGENTS.md` is the canonical protocol file. `CLAUDE.md` must be a relative symbolic link to `AGENTS.md`; edit `AGENTS.md` only.
> **All Agents operating in this project directory MUST read and understand `SKILL.md` before performing any task.**

## Design Philosophy

- **LLM as programmer, Wiki as codebase**
- **User is responsible for**: placing materials, asking good questions, judging significance
- **Agent is responsible for**: summarizing, cross-referencing, indexing, logging, and maintaining structural consistency
- **Accumulation over retrieval**: interactions should leave lasting value when they produce reusable knowledge
- **Zotero as literature layer, wiki as knowledge layer**: Zotero can manage bibliographic metadata, PDFs, annotations, collections, tags, and citation keys; llm-wiki should distill concepts, relationships, time ordering, and synthesis into Markdown

## Core Work Protocol

### Ingest

Use Protocol mode for ingest because it requires LLM judgment. The Agent must:

1. Verify the source exists in `sources/` or was fetched through a real network/Zotero operation.
2. Run the post-fetch verification gate before using network-fetched files.
3. Extract source metadata, including title, authors/creator, URL/DOI/arXiv/citation key where available.
4. Extract source time metadata:
   - `published`: paper publication, arXiv date, article/post date, release date, or documentation date.
   - `updated_at_source`: source-side update time if available.
   - `collected`: user collection, Zotero import, or saved time if available.
   - `ingested`: llm-wiki processing date.
   - `date_precision`: `day`, `month`, `year`, or `unknown`.
5. Build a source content map before page drafting. Enumerate major topic units and source-supported mechanisms, equations, numerical evidence, comparisons, procedures, failure modes, trade-offs, decision rules, and open questions.
6. Allocate every important unit to the target page, another existing page, a new independently reusable page, or an explicit omission reason. A fixed summary budget is not an omission reason.
7. Select a page archetype and source-dependent headings. Required page invariants do not imply a fixed knowledge-body outline.
8. Draft at the depth required to preserve the source's defining reasoning. Keep central formulas, causal chains, implementation details, version differences, and evidence context when they determine the source's value.
9. Run coverage, depth, and batch-template-collapse reviews before setting `status: active`.
10. Preserve `sources_meta`, add temporal structure when useful, run dynamic linking, update `wiki/index.md`, and append `log.md` only after the content reviews pass.

The coverage review must account for each important source unit as included, allocated elsewhere, or intentionally omitted. The depth review must reject abstract-only paraphrases, unexplained method-name lists, comparisons without dimensions, unsupported generalization, and generic applicability statements. For batch ingest, compare drafts for suspiciously identical structure or length; investigate rather than automatically padding pages.

When a timeline is useful:

- For papers, arXiv works, named methods, released systems, benchmark reports, or technical posts with a clear source date, show a compact visible date as a Markdown time anchor before the work name, e.g. `**[2024.02] FlashAttention V3**` or `**[2025.08] GRPO training discussion**`.
- If only a year is reliable, use `YYYY`; do not invent a month.
- Start `### 时间定位` / `### Temporal Position` with a blockquote summary using `> **时间范围**：...` and `> **阶段判断**：...` when the page has multiple dated nodes.
- Prefer readable lists over wide Markdown tables when the row contains wiki links or long relationship text. Tables must not force narrow columns to wrap wiki links into broken fragments.

Never treat `created` / `updated` as publication dates. They are wiki maintenance dates only.

### Query

For wiki queries, first read `wiki/index.md`, then relevant pages and link neighbors. Use semantic query only as candidate discovery; synthesize from the actual page content and cite wiki pages with `[[PageName]]`. If a query produces a lasting new synthesis, ask or decide whether to archive it into wiki according to user intent.

For questions that need Zotero source coverage, recent literature, annotations, or a specific paper, follow [`docs/ZOTERO_MCP_INTEGRATION.md`](docs/ZOTERO_MCP_INTEGRATION.md). Zotero MCP is mandatory for discovery, reads, source access, metadata identity, and normal writes; the dedicated document is the single source of truth for the temporary, explicitly authorized Zotero 10 loopback write exception and every capability, ingest, write-back, and failure gate.

### Page Format Requirements

Every non-index wiki page should include frontmatter, one-sentence definition, knowledge content, related pages, sources, and changelog. When available, include source-level metadata:

```yaml
---
created: 2026-04-10
updated: 2026-04-10
sources:
  - "sources/paper.pdf"
source_types:
  - "academic_paper"
sources_meta:
  - title: "Paper Title"
    type: "academic_paper"
    published: "2025-02"
    collected: "2026-05-24"
    ingested: "2026-05-24"
    date_precision: "month"
    zotero_item_key: "ABCD1234"
    citation_key: "author2025title"
tags:
  - "AI/ML"
status: "active"
---
```

Page `status` is a maturity lifecycle: `seed` (stub from a fresh ingest) ->
`developing` (being fleshed out) -> `mature` (covers its sources) -> `evergreen`
(stable, maintained). `draft` (unreviewed) and `archived` (retired) remain valid;
`active` is a legacy alias of `developing`. Depth lint analyzes pages from
`developing` upward and reports a `lifecycle_mismatch` advisory when a
`mature`/`evergreen` page is still shallow. Unknown status values are reported
as `invalid_status`.

Pages may additionally declare claim-level provenance in frontmatter:

```yaml
claims:
  - text: "LoRA constrains the weight update to a low-rank product"
    source: "sources/lora.pdf"     # must be declared in this page's sources/sources_meta
    status: "accepted"             # accepted | provisional | contested | unsupported
```

Lint validates claims as advisory `claim_issues`: every claim needs
text/source/status, the status must be in the vocabulary, and the source must
be one the page itself declares. A `mature`/`evergreen` page with still
contested or unsupported claims is flagged. Never fabricate claim sources or
statuses — an absent claim list is always better than an invented one.

Do not invent missing month/day values. If only the year is reliable, write the year and set `date_precision: "year"`.

In body text, prefer a human-scannable Markdown time anchor for dated works:

- Use `**[YYYY.MM] Work or event name**` for sources with known day or month precision.
- Use `**[YYYY] Work or event name**` for sources with only year precision.
- Use `**[YYYY.MM-YYYY.MM]**` for ranges.
- In `### 时间定位`, lead with a native Markdown blockquote summary:
  - `> **时间范围**：YYYY.MM-YYYY.MM`
  - `> **阶段判断**：one concise sentence about the historical stage`
- For `### 来源摘要` / source-note summaries, keep `**时间信息**` concise, then list 2-6 important anchors as sub-bullets when useful.
- Apply visible anchors especially in `## 时间线`, `### 与已有知识的关系`, `## Related Pages`, and source-note summaries.
- Keep the full machine-readable date in frontmatter (`YYYY-MM-DD`, `YYYY-MM`, or `YYYY`) and use the compact display form only for reading.

### Cross-Reference Rules

1. First meaningful mention of a concept creates a `[[Concept]]` link.
2. Avoid over-linking; link the first mention within a local section.
3. Every internal link must resolve to a real `wiki/*.md` stem by the end of ingest.
4. Use canonical slug file names and aliases, e.g. `[[AI-Coding-Workflow|AI Coding Workflow]]`.
5. Relationship descriptions should include temporal relation when useful: early work, follow-up, contemporary route, survey, retrospective, or outdated-but-historically-important.

### Behavioral Rules

- Be proactive about structural problems, source ambiguity, stale pages, missing dates, and dead links.
- Keep changes scoped and simple.
- Cite sources and preserve provenance.
- Do not delete user-managed raw materials.
- Do not write LLM-generated content into `sources/`.
- Synchronize README language variants when user-facing behavior changes.
- Use the project-managed Python environment (`.venv` or conda) for Python operations.
- For every Zotero operation and Zotero-backed source, follow [`docs/ZOTERO_MCP_INTEGRATION.md`](docs/ZOTERO_MCP_INTEGRATION.md).
- `wiki/*` and most `sources/*` are gitignored by default. Use `rg --no-ignore` for repository searches that must include user-managed knowledge/source files; a plain `rg` result is not a complete wiki inventory.

### Release Artifact Verification

- Run Python smoke checks inside a generated release directory with bytecode writes disabled: use `python -B ...` or set `PYTHONDONTWRITEBYTECODE=1`.
- After smoke checks, verify both the expanded release directory and its archive contain no `__pycache__/` directories or `.pyc` files before recording checksums or publishing artifacts.

## Mandatory Pre-Flight Checklist

Before executing any wiki-related task, every Agent MUST:

1. **Read `SKILL.md`** — Understand the machine-readable specification, entry points, functions, and dependencies.
2. **Read this unified `AGENTS.md` / `CLAUDE.md` protocol** — Understand the core protocol, tool selection guide, and behavioral rules.
3. **Run `python scripts/agent-bridge.py check`** — Verify the runtime environment.
4. **Respect `sources/` integrity** — Never write LLM-generated content into `sources/`.

Failure to follow the above may result in corrupted knowledge base, fabricated sources, or broken cross-references.

---

## Agent Tool Selection Guide

> **STOP. Before doing any wiki task, read this section.**
>
> This project provides a single unified entry point for Agents: **`scripts/agent-bridge.py`**.
> You do NOT need to remember multiple CLI commands. You do NOT need to check if dependencies are installed.
> Just run `python scripts/agent-bridge.py check` at the start of each session.

### Mandatory Pre-Task Check

Before any wiki operation, run:

```bash
python scripts/agent-bridge.py check
```

This produces a structured Markdown report telling you:
- Whether the environment is ready
- How many wiki pages exist
- Whether embedding/linking features are enabled
- Which Python interpreter will be used

**Do not skip this step.** It eliminates all uncertainty about "is CLI installed?"

### Python Environment Rule

Two environments exist for different purposes — do not conflate them:

- **User distribution**: end users install the `llm-wiki` CLI via `uv tool install` (or `uvx`), which creates an isolated environment managed by uv. This is how the tool is **run in production**; it does not touch this repository's `.venv`.
- **Development / testing**: work done **inside this repository** (running `agent-bridge.py`, pytest, editing code) uses the project's own virtual environment described below. Keep it; `uv tool` does not replace it.

All Python operations in this project MUST use the project's own virtual environment:

1. **If `.venv/` exists** in the project root → use `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (Linux/macOS). Prefer `uv run python` when uv is available.
2. **If no `.venv/` but conda is available** → use `conda run -n llm-wiki python`.
3. **Never use system Python** or global pip directly.

This ensures consistent dependency versions and avoids environment pollution. When running tests, use:

```bash
.venv/Scripts/python.exe -m pytest tests/        # Windows
.venv/bin/python -m pytest tests/                # Linux/macOS
```

---

### Task Type Quick Reference

Every wiki task falls into exactly one of three categories. **The category determines which tool you use.**

| Category | Task | Needs LLM? | You Use | If Unavailable |
|----------|------|-----------|---------|---------------|
| **A** | Link discovery | No | `agent-bridge.py link` | Fallback: read files directly |
| **A** | Batch relink | No | `agent-bridge.py relink` | Fallback: run `link` per page |
| **A** | Health check | No | `agent-bridge.py lint` | Fallback: manual inspection |
| **A** | Status overview | No | `agent-bridge.py status` | Fallback: count files in wiki/ |
| **A** | Embedding index | No | `agent-bridge.py index` | Skip semantic search |
| **A** | Safe merge | No | `agent-bridge.py merge` | Manual edit with diff review |
| **A** | Semantic query | No | `agent-bridge.py query --semantic` | Fallback to keyword listing |
| **A** | Zotero sync plan | No | `agent-bridge.py zotero-plan` | Manually compare wiki provenance with MCP reads |
| **A** | Zotero enrichment dry-run | No | `agent-bridge.py zotero-refresh` | Review provider results and the generated manifest |
| **A** | Zotero collection ingest verification | No | `agent-bridge.py zotero-ingest-verify` | Manually audit allocation, provenance, and page invariants |
| **C** | Zotero stale binding heal | Agent reviews | `agent-bridge.py zotero-heal` | Manually rebind frontmatter item keys |
| **A** | Zotero alias render | No | `agent-bridge.py zotero-alias` | Hand-sanitize a source_alias string |
| **C** | Apply safe Zotero enrichment | Agent reviews | `zotero-refresh --apply-safe` | Use MCP tools manually if the worker cannot verify write-back |
| **C** | Authorized Zotero tag/relation write-back | Agent + user review | `agent-bridge.py zotero-writeback` | Use reviewed incremental MCP writes when the local exception is unavailable |
| **C** | Controlled Zotero attachment relocation | Agent + user review | `agent-bridge.py zotero-relocate` | Review dry-run, require local authorization, and stop when the attachment API gate is unavailable |
| **B** | Ingest material | **Yes** | Protocol mode (direct file ops) | N/A |
| **B** | Query & synthesize | **Yes** | Protocol mode (direct file ops) | N/A |
| **C** | Apply link results | **Agent judges** | `merge` (after reviewing diff) | Manual edit |
| **C** | Atomic multi-file write | **Agent drafts, tool applies** | `agent-bridge.py apply-bundle` | Manual edits with no atomicity guarantee |
| **A** | Inspect capability contracts | No | `agent-bridge.py capabilities` | Read `src/llm_wiki/capabilities.py` |
| **A** | Recent activity context | No | `agent-bridge.py hot` | Read `wiki/hot.md` |

**Category A**: Pure algorithm. No LLM intelligence needed. **Always use `agent-bridge.py`.**

**Category B**: Requires LLM understanding, insight extraction, or creative synthesis. **Always use Protocol mode** (read/write files directly).

**Category C**: Hybrid. The tool discovers candidates (Category A), but you use LLM judgment to decide whether to apply them.

---

### Why agent-bridge.py Exists

The old documentation told you "Protocol mode = operate files directly" and also "run `wiki link` commands". This created mixed signals. You (the Agent) naturally chose the path with lowest cognitive uncertainty: writing Python code yourself.

**`agent-bridge.py` solves this by being the single obvious choice for all Category A tasks.**

It handles internally:
- Finding the right Python interpreter (venv, conda, system)
- Checking if `src.llm_wiki` is importable
- Calling the library code directly (no subprocess overhead)
- Producing structured Markdown output (no JSON to parse)
- Logging every internal step to stderr with file:line precision (fully visible)

You see the full execution trace, so it is never a black box.

---

## Category A Tasks: Use agent-bridge.py

### 1. Link Discovery

**When**: After creating a new wiki page during ingest. Discover which existing pages are related.

```bash
python scripts/agent-bridge.py link --source "NewPage" --mode light
```

**Output sections**:
- `## Relation Discovery: <Page>` — summary
- `### Relations` — table of candidates with score, type, evidence
- `### Actionable Items` — high-confidence relations with suggested next commands

**Your action**: Review the `[ACTION]` markers. For score >= 0.5 relations, run the suggested `--dry-run` merge command first, review the diff, then apply.

**Example workflow**:

```
Agent:
1. Run: python scripts/agent-bridge.py link --source "LoRA" --mode light
2. Read output: finds [[Fine-tuning]] score=0.78 type=EXTENDS
3. Run dry-run merge:
   python scripts/agent-bridge.py merge --source "LoRA" --target "Fine-tuning" \
       --strategy append_related --dry-run
4. Review diff in output
5. If reasonable, re-run without --dry-run
```

### 2. Batch Global Relink

**When**: After ingesting 2+ sources. Discover cross-page relations for all recent pages at once.

```bash
python scripts/agent-bridge.py relink --since 2026-04-20 --mode deep --dry-run
```

Remove `--dry-run` after reviewing the relation report.

### 3. Health Check (Lint)

**When**: Periodic maintenance, or user asks "check wiki health".

```bash
python scripts/agent-bridge.py lint
```

**Output sections**:
- `## Summary` — count table for orphans, dead links, stale, empty pages, duplicate titles, non-canonical links, drafts, and shallow pages
- `## Orphan Pages` — pages not referenced by any other
- `## Dead Links` — `[[...]]` targets that are not real `wiki/*.md` file stems
- `## Stale Pages` — >90 days since last update
- `## Empty Pages` — files with no meaningful body text
- `## Duplicate Titles` — multiple files declaring the same `# Title`
- `## Non-Canonical Links` — wiki links whose target does not point to the real page file stem
- `## Draft Pages`
- `## Shallow Pages` — advisory, source-aware depth findings with knowledge size, structure, source volume, compression ratio, and reasons

Depth lint excludes `Related Pages` / `相关页面`, `Sources` / `来源`, and `Changelog` / `变更日志`. It is warning-only: findings do not change the command exit behavior. `QRF` pages are skipped by default, and an intentionally concise page may use `lint_depth: skip` only after a coverage audit records why the warning is a false positive. Passing the heuristic never replaces source-unit coverage review, and Agents must not pad pages mechanically to satisfy thresholds.

**Your action**: For dead links, create canonical page files or rewrite the link target to an existing file stem. For empty pages, fill them or remove duplicate shells. For duplicate titles, keep the canonical slug file (`Title-With-Spaces.md`) and merge or delete accidental variants. For non-canonical links, rewrite `[[Page Name]]` as `[[Page-Name|Page Name]]`. For orphans, consider adding backlinks from relevant pages. For shallow pages, inspect the allocated sources and restore missing mechanisms, evidence, comparisons, procedures, failure modes, and decision rules; do not add generic filler.

### 4. Status Overview

**When**: User asks "what's in the wiki?" or you need context before a task.

```bash
python scripts/agent-bridge.py status
```

### 5. Semantic Query (when embedding enabled)

**When**: User asks a question and `embedding.enabled: true` in config.yaml. This finds candidate pages via vector search; you then read those pages and synthesize the answer.

```bash
python scripts/agent-bridge.py query "What is LoRA?" --semantic
```

**Output sections**:
- `## Semantic Results` — ranked table of relevant pages
- `[ACTION] Agent: Read the top-ranked pages and synthesize an answer with citations.`

**Your action**: Read the listed pages, then synthesize an answer. Do NOT treat the semantic results as the final answer.

### 6. Safe Merge

**When**: Applying a relation update to an existing page. Always produces a diff for review.

```bash
# Preview
python scripts/agent-bridge.py merge --source "NewPage" --target "OldPage" \
    --strategy append_related --dry-run

# Apply
python scripts/agent-bridge.py merge --source "NewPage" --target "OldPage" \
    --strategy append_related
```

### 7. Embedding Index

**When**: After adding new pages and embedding is enabled. Build/update the vector index.

```bash
python scripts/agent-bridge.py index
```

### 8. Zotero Sync and Metadata Plan

**When**: Before post-ingest Zotero tag synchronization or a collection-level DOI/publication audit.

1. Use Zotero MCP to create a minimal verified snapshot under ignored `temp/`.
2. Run the read-only planner:

```bash
python scripts/agent-bridge.py zotero-plan --snapshot temp/zotero-snapshot.yaml \
  --manifest-out temp/zotero-mutation-manifest.yaml
```

3. Review managed-tag additions, collection-equivalent removal candidates, DOI states, and preprint publication checks.
4. Apply approved mutations through Zotero MCP by default. When the user has explicitly authorized the documented Zotero 10 loopback exception, promote only reviewed additions/relations into an `authorized-write` plan and use `zotero-writeback`; for attachment relocation, use the separately gated `zotero-relocate` workflow described in the canonical protocol; then re-read the write backend and pass the synchronization barrier.

The planner never connects to Zotero and never mutates Zotero or wiki files. An omitted `doi` means unobserved; `doi: ""` means the Zotero DOI field was read and is missing. A `--manifest-out` target must stay under `temp/`; the emitted `mode: review-only` manifest is not an executable mutation script, and `remove_tags_review` / `relation_candidates_review` still require Agent and MCP review.

For one-shot enrichment, run:

```bash
python scripts/agent-bridge.py zotero-refresh --collection-key A9VNJUPI \
  --manifest-out temp/zotero-refresh.yaml
```

The refresh command reads Zotero only through the configured MCP server, uses Crossref/OpenAlex provider lookups, and stores its private freshness cache under ignored `var/`. It is dry-run by default. Before using `--apply-safe`, review the manifest; safe apply is limited to incremental `LLM-Wiki ...` Extra keys, `llm-wiki:*` status tags, and conservative DOI URL normalization. New DOI values, bibliographic identity changes, item-type migration, and preprint/published relations remain review-only.

For collection ingest QA, keep a complete allocation ledger under ignored `temp/` and run:

```bash
python scripts/agent-bridge.py zotero-ingest-verify \
  --snapshot temp/zotero-snapshot.yaml \
  --allocation temp/zotero-allocation.yaml \
  --report-out temp/zotero-ingest-report.yaml
```

The verifier checks snapshot/allocation counts, unique item keys and indices, omission reasons, non-omitted `sources_meta.zotero_item_key` coverage, duplicate provenance rows, YAML/frontmatter validity, page invariants, control characters, trailing whitespace, private path leakage, and advisory batch-template collapse.

For stale binding repair — Zotero item merges, re-imports, or attachment conversions that leave a dangling `zotero_item_key` in wiki frontmatter — run:

```bash
python scripts/agent-bridge.py zotero-heal --snapshot temp/zotero-snapshot.yaml \
  --manifest-out temp/zotero-heal.yaml
```

The healer is dry-run by default: it detects wiki-bound item keys absent from the snapshot and re-addresses them via DOI, then citation key, then normalized title (unique matches only). Review the manifest, then re-run with `--apply` to rewrite the affected pages' `sources_meta[].zotero_item_key` in place (file names never change) and append a `log.md` record. It never writes to Zotero. The candidate pool is limited to the snapshot's collection; unmatched keys need manual lookup.

For an explicitly reviewed local write-back, copy only approved additions and Related pairs into a secret-free `mode: authorized-write` plan (see `docs/examples/zotero-write-plan.example.yaml`), then run audit, apply, and verify as separate phases:

```bash
python scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action audit --report-out temp/zotero-write-audit.yaml
python scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action apply --memory-authorize --report-out temp/zotero-write-report.yaml
python scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action verify --report-out temp/zotero-write-verify.yaml
```

This restricted path adds managed `llm-wiki:*` tags and ensures user-reviewed reciprocal Related pairs only. It preserves full existing tag objects, uses live server identity plus version guards, retries one HTTP 412 from fresh state, and requires GET-after-PATCH verification. It cannot edit metadata, change collections, write notes, or touch Trash. Tag removal is a scoped opt-in: a plan must set `policy.allow_managed_removals: true` and list each tag under an item's `reviewed_removals`, and only managed `llm-wiki:*` tags other than the protected `llm-wiki:ingested` and preserved tags may be removed (never unmanaged/user tags). Generate a whitelisted removal plan with `zotero-plan --removal-plan-out` (retired `llm-wiki:<page_stem>` binding tags only). With `--memory-authorize`, the API key is not serialized.

For controlled attachment relocation, configure the managed root once in `config.yaml` under `zotero_relocation.root` instead of passing `--root` on every run; `config.yaml` is gitignored, so each machine keeps its own value, and `--root` remains only a one-off override. For cross-device sync, point `root` at a cloud-synced folder and use environment-variable interpolation to keep the path portable (for example `root: "${OneDrive}/zotero-attachments"`). When devices run different operating systems (for example Windows and Linux), absolute paths can never match: set `zotero_relocation.base_dir_relative: true` so the path written back to Zotero is the portable `attachments:<relative>` form, and point Zotero's Linked Attachment Base Directory at the synced root on each device. Remind the user that a stored→linked conversion may stop Zotero File Sync from managing the file bytes, so every device must be able to reach the same synced root.

---

## Category B Tasks: Use Protocol Mode (Direct File Operations)

### Ingest

**Never** use a CLI command for ingest. Ingest requires LLM intelligence to:
- Understand the source material
- Extract key insights
- Decide page structure and cross-references
- Write frontmatter and content

```
User: Please ingest sources/paper.pdf

Agent (Protocol mode):
1. Read sources/paper.pdf (use appropriate file reader)
2. Extract key insights via LLM
3. Create wiki/NewConcept.md with proper frontmatter
4. Create stub pages for any new [[Dead Link]]
5. Run agent-bridge.py link --source "NewConcept" --mode light
6. Review high-confidence relations, run merge --dry-run for each
7. Update wiki/index.md
8. Append log.md
```

### Query (without embedding)

When embedding is disabled, query is pure Protocol mode:

```
User: What's the difference between LoRA and full fine-tuning?

Agent (Protocol mode):
1. Read wiki/index.md to locate relevant topics
2. Read wiki/LoRA.md and linked neighbors
3. Synthesize answer with citations: [[LoRA]], [[Fine-tuning]]
4. Judge: Is this answer worth archiving?
```

---

## Category C Tasks: Hybrid (Tool Discovery + Agent Judgment)

### Applying Link Results

This is the only task that requires both `agent-bridge.py` AND your LLM judgment.

```
Agent:
1. Run: python scripts/agent-bridge.py link --source "Bid2X" --mode light
2. Read output. For each relation with score >= 0.5:
   a. Read the target existing page
   b. LLM analysis: "Bid2X is an improvement over RTBAgent, extending xxx"
   c. Decision: Use append_related strategy
   d. Run: python scripts/agent-bridge.py merge --source "Bid2X" --target "RTBAgent" \
          --strategy append_related --dry-run
   e. Review diff in output
   f. If reasonable, re-run without --dry-run
3. Update log.md
```

### Applying a Transaction Bundle (Atomic Ingest Writes)

**When**: An ingest or maintenance step must write several files as one logical
operation — typically a new page plus `wiki/index.md` plus `log.md`. Direct
Protocol-mode writes can leave the knowledge base inconsistent if interrupted;
a transaction bundle applies them atomically with rollback on failure.

Manifest format (place under ignored `temp/`, e.g. `temp/tx-bundle.yaml`):

```yaml
ops:
  - op: create                 # target must NOT exist
    path: wiki/NewPage.md      # relative to project root
    content_path: draft-NewPage.md   # draft file, relative to this manifest
  - op: update                 # target must exist AND match expected_sha256
    path: wiki/index.md
    content_path: draft-index.md
    expected_sha256: "a1b2..." # MUST be quoted; all-digit values unquoted are rejected
```

Workflow:

```
Agent:
1. Read every file you will update; draft all new content under temp/
2. Write temp/tx-bundle.yaml with the ops above
3. Run: python scripts/agent-bridge.py apply-bundle temp/tx-bundle.yaml --dry-run
   -> Per-op status table + unified diff; update ops report their current sha256
4. Fill any missing expected_sha256 values from the dry-run output
5. Review the diff carefully; if anything is wrong, fix drafts and dry-run again
6. Run: python scripts/agent-bridge.py apply-bundle temp/tx-bundle.yaml
   -> All ops verified, journaled, and written atomically; mid-apply failure
      rolls every file back. Report the operation ID and changed paths.
```

Rules:

- **Never apply without a reviewed dry-run.** The `expected_sha256` lock fails
  closed if a file changed since you drafted it — re-read, re-draft, re-lock.
- Journals live under `.backups/transactions/<tx-id>/` (gitignored); clean old
  ones manually.
- `create` refuses existing files; `update` refuses missing files and requires
  `expected_sha256`. Destructive deletes are not supported — do them by hand.
- Write paths are machine-enforced against the command's capability contract
  (`wiki/`, `log.md` only). A bundle that targets `sources/` or code is rejected
  before anything is written.
- A successful apply also records one bounded entry in `wiki/hot.md` (newest
  first, last 20 kept). `hot.md` is session-resume context, not a knowledge
  page: it is excluded from page listings and lint. Print it with
  `agent-bridge.py hot` — e.g. at session start when the user opts in.

### Capability Contracts

Every bridge command declares its write scope, network use, and dry-run support
in `src/llm_wiki/capabilities.py`. `config.yaml` may **tighten** these contracts
(disable a command, narrow a write scope) but never widen them:

```yaml
capabilities:
  apply-bundle:
    enabled: false          # disable a command entirely
  merge:
    write_scope: ["wiki/"]  # narrow only; widening is rejected
```

Run `python scripts/agent-bridge.py capabilities` to inspect the effective
contracts. Disabled commands fail closed at dispatch; out-of-scope bundle
writes are rejected before any file is touched.

---

## Execution Visibility: Logging

All `agent-bridge.py` commands and the underlying library code emit structured logs to **stderr**.

Format:
```
[INFO] src/llm_wiki/linker.py:187 find_related() | find_related: query=LoRA mode=kw_w=0.6 vec_w=0.0 link_w=0.4 top_k=5 min_score=0.30
[DEBUG] src/llm_wiki/linker.py:204 find_related() | Query keywords extracted: 42 terms
[DEBUG] src/llm_wiki/linker.py:210 find_related() | Phase 1: keyword match (weight=0.6)
[DEBUG] src/llm_wiki/linker.py:313 find_related() | Phase 3: link proximity skipped (weight=0.0)
[INFO] src/llm_wiki/linker.py:342 find_related() | find_related complete: 3 relations above min_score (returning top 5)
```

Every log line includes:
- **Log level**: INFO / DEBUG / WARNING / ERROR
- **File path**: relative to project root
- **Line number**: exact source line
- **Function name**: which method emitted the log
- **Message**: what happened

**Why this matters**: You can trace the full execution pipeline. If a relation is missing, you can see which phase (keyword/vector/link) filtered it out. If embedding fails, you see the exact exception. Nothing is hidden.

To see full debug output, add `--verbose` to any direct CLI command:
```bash
python -m src.llm_wiki --verbose link --source "X" --mode light
```

---

## Sources Directory Write Rules

> The integrity of `sources/` is the foundation of the entire knowledge base. Once raw materials are polluted, all derived wiki content loses credibility.

### Two Allowed Cases for Writing to `sources/`

| Case | Condition | Action |
|------|-----------|--------|
| A | User manually placed a file | Read-only, do not modify |
| B | User provided a URL/DOI and the file is not yet in `sources/` | Use network tools to fetch, verify non-empty and correct format, then write |
| C | `54yyyu/zotero-mcp` provides a verified Zotero-managed file | Follow [`docs/ZOTERO_MCP_INTEGRATION.md`](docs/ZOTERO_MCP_INTEGRATION.md) |

### Absolute Prohibitions

- **NEVER** save LLM-generated text, summaries, or speculative content as `.md`, `.txt`, or any format into `sources/`
- **NEVER** claim "downloaded" and create files without actually executing a network request
- **NEVER** "fall back" to generated content when fetching fails

### Zotero-Linked Sources

All Zotero source discovery, attachment access, private bindings, provenance fields, and write-back rules are defined in [`docs/ZOTERO_MCP_INTEGRATION.md`](docs/ZOTERO_MCP_INTEGRATION.md). Use only `54yyyu/zotero-mcp` for Zotero operations, except the temporary opt-in Zotero 10 loopback write paths (`zotero-refresh --write-backend local`, restricted `zotero-writeback`, and separately gated `zotero-relocate`) documented there.

### Standard Network Fetch Template

**Direct download (PDF, text files)**:

```bash
# Check if URL is reachable
curl -I -L "https://example.com/paper.pdf"

# Download to sources/
curl -L -o "sources/YYYY-MM-DD-description.pdf" "https://example.com/paper.pdf"

# Verify file is non-empty
ls -la "sources/YYYY-MM-DD-description.pdf"
```

**Rendered web pages (tech blogs, dynamic content)**:

Use Playwright tools to fetch page content:

```bash
# Use playwright to get rendered page
playwright screenshot --full-page "https://tech.blog.example.com/article" "sources/temp-screenshot.png"
```

Or use a Python script to get text:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://tech.blog.example.com/article")
    text = page.inner_text("article")  # or appropriate selector
    with open("sources/YYYY-MM-DD-description.md", "w", encoding="utf-8") as f:
        f.write(text)
    browser.close()
```

**DOI resolution**:

```bash
# DOI usually redirects to publisher pages; paywalls may apply
curl -L -o "sources/paper.html" "https://doi.org/10.xxxx/xxxxx"

# Prefer open-access versions like arXiv
curl -L -o "sources/paper.pdf" "https://arxiv.org/pdf/xxxxx.pdf"
```

### Post-Fetch Verification Protocol

> Downloading is not enough. You MUST verify the file content matches what the user requested before ingesting.

After every successful network fetch, before writing to `sources/` or proceeding with ingest, perform the following verification:

#### Verification Checklist

| # | Check | How | If Failed |
|---|-------|-----|-----------|
| 1 | File is readable | Attempt to read/parse the file | STOP — file may be corrupted |
| 2 | Not an error page | Scan for `404`, `Access Denied`, `Please enable JavaScript`, `Subscribe`, `Login` | STOP — treat as fetch failure |
| 3 | Format matches extension | PDF starts with `%PDF`; HTML has `<html`; MD is plain text | WARN — rename extension if needed |
| 4 | Title matches expectation | Extract title/heading and compare to user's description | STOP if clearly wrong; ask user if uncertain |
| 5 | Identifiers match (if provided) | Extract DOI, arXiv ID, author names; compare to user input | STOP if mismatch |

#### Extracting Verifiable Identifiers by File Type

**PDF (academic papers)**:

Use Python to extract text from the first 1-2 pages, then look for:

```python
import fitz  # PyMuPDF

doc = fitz.open("sources/downloaded-paper.pdf")
text = ""
for page in doc[:2]:  # first 2 pages
    text += page.get_text()
doc.close()

# Extract identifiers
import re
doi = re.search(r'10\.\d{4,}/[^\s]+', text)
arXiv = re.search(r'arXiv:\d{4}\.\d{4,}', text, re.I)
# Title is usually the largest text block on page 1
```

**Markdown / HTML / Text**:

Use Read tool directly. Extract:
- First `# Heading` or `<title>` tag
- First paragraph as summary check

**All file types**:

Check for error-page signatures:
- `404 Not Found`, `403 Forbidden`
- `Access Denied`, `Subscription Required`
- `Please enable JavaScript`, `Cloudflare`
- Empty or near-empty content (< 100 bytes for text files)

#### Mismatch Handling Flow

```
Verification result
    |
    +-- PASS (confident match)
    |     -> Write to sources/ -> Continue normal ingest
    |
    +-- FAIL (clear mismatch or error page)
    |     -> Do NOT write to sources/ (or delete if already written)
    |     -> Do NOT create wiki pages
    |     -> Do NOT log as "ingested"
    |     -> Record in log.md: "[Date] verify-failed | Filename — reason"
    |     -> Reply to user with extracted vs expected metadata
    |     -> Await user instruction
    |
    +-- UNCERTAIN (cannot extract or ambiguous)
          -> Report extracted metadata to user
          -> Ask: "Extracted title: 'X'. Is this the correct file?"
          -> Only proceed after explicit user confirmation
```

#### Example: Verification Pass

```
User: Please ingest https://arxiv.org/pdf/2106.09685.pdf (the LoRA paper)

Agent: curl -L -o sources/2106.09685.pdf https://arxiv.org/pdf/2106.09685.pdf
       python (extract text from first 2 pages)
       -> Title: "LoRA: Low-Rank Adaptation of Large Language Models"
       -> Authors: "Edward J. Hu, Yelong Shen, Phillip Wallis"
       -> arXiv ID: arXiv:2106.09685
       -> Compare to user description: "LoRA paper" — MATCH
       -> Verification: PASS
       -> Continue with ingest
```

#### Example: Verification Fail

```
User: Please ingest https://arxiv.org/pdf/2106.09685.pdf (the LoRA paper)

Agent: curl -L -o sources/2106.09685.pdf https://arxiv.org/pdf/2106.09685.pdf
       python (extract text)
       -> Title: "Attention Is All You Need"  <- Wrong paper!
       -> arXiv ID: arXiv:1706.03762         <- Mismatch
       -> Verification: FAIL
       -> Do NOT ingest
       -> Report to user: "Downloaded file is 'Attention Is All You Need' (arXiv:1706.03762),
          but you requested the LoRA paper (2106.09685). Please check the URL."
```

#### Example: Error Page Detected

```
User: Please ingest https://example.com/paywalled-paper.pdf

Agent: curl -L -o sources/paper.pdf https://example.com/paywalled-paper.pdf
       python (read file)
       -> Content contains: "Subscribe to access this article"
       -> Verification: FAIL (error page)
       -> Do NOT ingest
       -> Record in log.md: verify-failed — paywall
       -> Report to user with alternatives
```

### Fetch Failure Handling Flow

```
Fetch attempt
    |
    +-- Success -> Run Post-Fetch Verification -> PASS -> Write to sources/ -> Continue ingest
    |                        |
    |                        +-- FAIL -> Do NOT write to sources/ -> Report to user
    |
    +-- Failure (404/403/paywall/anti-bot)
          |
          +--> Do NOT create any file in sources/
          +--> Create or update [[Pending: SourceName]] stub page in wiki/
          +--> Record failure reason in log.md
          +--> Reply to user explaining the situation and request assistance
```

### Correct vs Incorrect Examples

**Incorrect** (absolutely forbidden):

```
User: Please ingest these papers [provides 5 titles, no URLs]

Agent: (Did not execute any curl/playwright call)
      Directly creates sources/paper-1.md with LLM-generated "summary"
      Then creates wiki pages based on fabricated content
```

**Correct** (no URL, Agent proactively searches):

```
User: Please ingest these papers [provides 5 titles, no URLs]

Agent: Uses WebSearch to find open-access versions for each title
      -> Found arXiv link for paper 1, author homepage PDF for paper 2
      Replies to user: "I found the following possible sources, please confirm:
      1. Paper Title 1 -> https://arxiv.org/pdf/xxxx.pdf
      2. Paper Title 2 -> https://author-page.edu/paper2.pdf
      I will download and ingest after your confirmation."
      (User confirms -> Execute curl download -> Continue ingest)
```

**Correct** (URL provided):

```
User: Please ingest https://arxiv.org/pdf/2401.xxxxx.pdf

Agent: Execute curl -L -o "sources/2026-04-20-paper.pdf" "https://arxiv.org/pdf/2401.xxxxx.pdf"
      Verify file size > 0
      Read PDF content
      Continue normal ingest flow
```

**Correct** (fetch failed):

```
User: Please ingest https://example.com/paywalled-paper.pdf

Agent: Execute curl -I "https://example.com/paywalled-paper.pdf"
      -> Returns 403 Forbidden
      Do NOT create sources/ file
      Create wiki/Pending-Paywalled-Paper.md (stub, marked as pending)
      Record in log.md: "[Date] pending | Paywall prevented fetching xxx"
      Reply to user: "This paper requires paid access; I cannot fetch it automatically.
      Please download manually and place in sources/, or provide an open-access link."
```

---

## File Type Processing Strategy

> **Key principle**: Different file types require different reading strategies; avoid using the Read tool directly on binary files.

### Decision Tree

```
File Type Recognition
    |
    +-- Text files (.md, .txt, .json, .yaml, .py, .js, etc.)
    |     +--> Use Read tool directly
    |
    +-- PDF files (.pdf)
    |     +-- Check dependency: is PyMuPDF (pymupdf) installed?
    |     |     +-- Yes -> Use Python script to read
    |     |     +-- No  -> Install dependency first, then read
    |     +--> Process via scripts/read_pdf.py or Python code
    |
    +-- Image files (.png, .jpg, .jpeg, .gif, etc.)
    |     +--> Use Read tool (vision model supported)
    |
    +-- Office documents (.docx, .xlsx, .pptx)
    |     +--> Requires python-docx / openpyxl, etc.
    |
    +-- Other binary formats
          +--> Find or create corresponding Python processing script
```

### PDF File Processing Detailed Flow

**Step 1: Check dependency**

```bash
# Check if PyMuPDF is installed
python -c "import fitz; print(fitz.__doc__[:30])"
```

If it fails, install first:

```bash
pip install pymupdf>=1.25.0
```

**Step 2: Read PDF content**

**Method A: Use existing script**

```bash
# Read all pages
python scripts/read_pdf.py sources/paper.pdf

# Read specific page range
python scripts/read_pdf.py sources/paper.pdf 1-10
```

**Method B: Use Python code (Recommended: PyMuPDF)**

```python
import fitz  # PyMuPDF

doc = fitz.open("sources/paper.pdf")
for page in doc:
    print(page.get_text())
doc.close()
```

**Fallback: pdfplumber (table extraction)**

If PyMuPDF performs poorly on complex tables, fall back to `pdfplumber` (note: install secure version >= 0.11.8 to fix CVE-2025-64512):

```python
import pdfplumber

with pdfplumber.open("sources/paper.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

**OCR last resort**

For scanned PDFs or when all above methods fail, use `pdf2image` + `pytesseract` for OCR.

**PDF extraction quality fallback**

If pdfplumber produces garbled text (especially with Chinese, special fonts, or complex academic layouts), try these alternatives:

**Method C: Use PyMuPDF (fitz)**

PyMuPDF is typically more reliable for CJK fonts and complex PDF text extraction:

```bash
# Install
pip install pymupdf
```

```python
import fitz  # PyMuPDF

doc = fitz.open("sources/paper.pdf")
for page in doc:
    print(page.get_text())
```

**Method D: Convert to images then OCR (last resort)**

For scanned PDFs or when all above methods fail, use `pdf2image` + `pytesseract` for OCR — slower but more robust.

### Text File Processing

Use Read tool directly:

```python
# Directly read Markdown, text, code files
Read("sources/notes.md")
Read("sources/config.yaml")
Read("sources/script.py")
```

### Image File Processing

Read tool supports vision models:

```python
# Read tool can process images and return visual content
Read("sources/diagram.png")
Read("sources/screenshot.jpg")
```

### Dependency Management

**Dependency file location**: `src/requirements.txt`

**Included dependencies**:
- `pyyaml>=6.0` - YAML parsing
- `pymupdf>=1.25.0` - PDF processing (PyMuPDF, supports CJK fonts and complex layouts)
- `numpy>=1.24.0` - Vector search / embedding math
- `httpx>=0.27.0` - HTTP client (provider lookups, Zotero local API)
- `mcp>=1.0.0` - Zotero MCP client transport
- `openai>=1.0.0` - Embedding provider client
- `pytest>=7.0.0` - Test framework

The CLI itself is stdlib `argparse` (`src/llm_wiki/cli.py`); no external CLI framework is required.

**Fallback dependencies** (only when PyMuPDF table extraction is poor):
- `pdfplumber>=0.11.8` - PDF table extraction (secure version required for CVE-2025-64512)
- `pdfminer.six>=20251107` - PDF underlying library

**Installation commands**:

```bash
# Using conda (recommended)
conda activate llm-wiki
pip install -r src/requirements.txt

# Using pip
pip install -r src/requirements.txt

# Using uv (if you have it)
uv pip install -r src/requirements.txt
```

---

## Old CLI Commands (Still Available)

The underlying `python -m src.llm_wiki` CLI remains available for human users and scripting. As an Agent, **prefer `agent-bridge.py`** because it:
- Auto-detects the environment
- Produces structured Markdown output
- Has unified error handling

If you need to use the lower-level CLI directly, see the command reference below.

### Direct CLI Command Reference

```bash
# Using virtual environment Python (preferred)
PY=".venv/Scripts/python"  # Windows
PY=".venv/bin/python"      # Linux/macOS

# Check availability
$PY -m src.llm_wiki --help

# Status
$PY -m src.llm_wiki status

# Lint
$PY -m src.llm_wiki lint

# Link (human-readable markdown output)
$PY -m src.llm_wiki link --source "NewPage" --mode light

# Relink
$PY -m src.llm_wiki relink --since 2026-04-20 --mode deep

# Index
$PY -m src.llm_wiki index
```

| Command | Purpose | Agent Should Use Instead |
|---------|---------|------------------------|
| `status` | Wiki overview | `agent-bridge.py status` |
| `lint` | Health check | `agent-bridge.py lint` |
| `link` | Relation discovery | `agent-bridge.py link` |
| `relink` | Batch global linking | `agent-bridge.py relink` |
| `index` | Build embedding index | `agent-bridge.py index` |
| `ingest` | Preview only (no LLM) | **Protocol mode** (direct file ops) |
| `query` | List pages / semantic search | `agent-bridge.py query` for semantic; **Protocol mode** for synthesis |

---

## Bidirectional Update Implementation Guide

> This section guides Agents on how to perform dynamic linking and bidirectional updates during ingest.

### Why Bidirectional Updates Are Needed

Traditional ingest only creates new pages; existing pages do not automatically reflect new knowledge. Bidirectional updates let the knowledge base **self-improve** over time:
- New paper improves an old method -> old page automatically gets "Latest Progress" section
- New work contrasts with old work -> both pages add comparison links
- New work depends on old concept -> old concept page gets backlink

### Linking Workflow

```
Finish new page creation
    |
    v
+------------------------------------------+
| 1. Run: agent-bridge.py link --source PAGE  |  <-- discovers relations
|            --mode light                  |
+------------------------------------------+
    |
    v
+------------------------------------------+
| 2. Agent reviews relation report         |  <-- LLM judges relevance
|    Only process score >= 0.5             |
+------------------------------------------+
    |
    v
+------------------------------------------+
| 3. For each high-confidence rel:         |
|    a. Read existing page                 |
|    b. Analyze old vs new                 |
|    c. Choose merge strategy              |
|    d. Run: agent-bridge.py merge         |
|       --source PAGE --target PAGE        |
|       --strategy STRATEGY --dry-run      |
|    e. Review diff, then apply            |
+------------------------------------------+
    |
    v
Update log.md, record operations
```

### Merge Strategy Decision Tree

```
Relation between new page and existing page
    |
    +-- Same field, different work
    |     +--> link_only (add to "Related Pages")
    |
    +-- New work extends/improves old method
    |     +--> append_section (add "Latest Progress")
    |
    +-- New work contrasts with old work
    |     +--> append_section (add "Comparison with xxx")
    |     +--> append_related (bidirectional links)
    |
    +-- New work corrects old concept
    |     +--> update_concept (update definition, use with care)
    |     +--> append_section (add "Concept Evolution")
    |
    +-- New work heavily depends on old concept
          +--> append_related (add backlink to old page)
```

### Agent Implementation Pattern (Protocol Mode)

**Scenario: User requests ingesting sources/new-paper.pdf**

```
Agent:
1. Read sources/new-paper.pdf
2. Extract insights, create wiki/NewMethod.md
3. Check dead links, create stub pages
4. Run: python scripts/agent-bridge.py link --source "NewMethod" --mode light
   -> Get relation report
5. For score >= 0.5 relations, e.g. [[OldMethod]]:
   a. Read wiki/OldMethod.md
   b. LLM analysis: "NewMethod is an improvement over OldMethod, extending xxx capabilities"
   c. Decision: Use append_section strategy, append "Relationship with NewMethod"
   d. Run: python scripts/agent-bridge.py merge --source "NewMethod" --target "OldMethod" \
          --strategy append_section --dry-run
   e. Review diff, confirm it is reasonable
   f. Apply modification (remove --dry-run)
6. Update log.md, record new pages and relation updates
7. Update wiki/index.md
```

### Safety Rules

1. **Always --dry-run first**: Generate diff for review before applying
2. **Append only, never replace**: `append_related` and `append_section` are safe strategies
3. **Use update_concept with caution**: Only when new information genuinely corrects an old definition
4. **Limit batch updates**: Single source should trigger no more than 5 backward updates
5. **Automatic backups**: merge tool automatically backs up to `wiki/.backups/`; rollback available

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `agent-bridge.py link` errors: page not found | Confirm page has been created; check title spelling |
| Diff is unreasonable | Do not apply; manually edit the page instead |
| False positive relation to unrelated page | Ignore (score usually < 0.3); do not execute merge |
| Strategy not in allowed list | Check config.yaml `linking.deep_mode.strategies_allowed` |
| Backup directory too large | Manually clean old backups in `wiki/.backups/` |

---

## Technical Details

### CLI Entry Points

- **Module**: `src.llm_wiki`
- **Main file**: `src/llm_wiki/cli.py` (stdlib `argparse`; no external CLI framework)
- **Core logic**: `src/llm_wiki/core.py`
- **Deterministic retrieval**: `src/llm_wiki/bm25.py` — dependency-free BM25Okapi with a mixed Chinese/English tokenizer (English words; Chinese unigrams + bigrams). It backs the content-relevance signal in both `link` and `query`, so retrieval quality never depends on embedding availability.
- **Agent Bridge**: `scripts/agent-bridge.py`
- **Logging**: `src/llm_wiki/agent_logger.py`

### Auxiliary Scripts

Project includes auxiliary scripts (`scripts/`):
- `scripts/agent-bridge.py` — **Unified Agent entry point (RECOMMENDED)**
- `scripts/wiki-status.sh` — Quick wiki status view
- `scripts/wiki-lint.sh` — Run health check
- `scripts/init-wiki.sh` — Initialize new project

### Dependencies and Virtual Environment

Dependency file: `src/requirements.txt`
- `pyyaml` - YAML parsing
- `pymupdf`, `numpy`, `httpx`, `mcp`, `openai` - runtime dependencies (see Dependency Management above)

#### Check Dependencies (including virtual environment detection)

```python
import importlib.util
from pathlib import Path
import subprocess
import sys

# 1. Detect virtual environment (uv/venv or conda)
venv_paths = [
    Path(".venv"),           # uv / modern tools
    Path("venv"),            # traditional
]
# Detect conda environment
conda_env = Path(os.environ.get("CONDA_PREFIX", ""))
if conda_env.exists():
    venv_python = conda_env / "python.exe" if sys.platform == "win32" else conda_env / "bin" / "python"
else:
    for venv in venv_paths:
venv_python = None
for venv in venv_paths:
    if venv.exists():
        venv_python = venv / "Scripts" / "python.exe" if sys.platform == "win32" else venv / "bin" / "python"
        break

# Decision path
if venv_python and check_dep("src.llm_wiki", venv_python):
    print(f"Using virtual environment: {venv_python}")
    python_cmd = str(venv_python)
elif check_dep("src.llm_wiki"):
    print("Using system Python")
    python_cmd = "python"
else:
    print("Dependencies not installed; using protocol mode")

# 2. Check if dependency is available
def check_dep(module_name, python_path=None):
    py = python_path or sys.executable
    result = subprocess.run([py, "-c", f"import {module_name}"], capture_output=True)
    return result.returncode == 0
```

### Relationship with CLAUDE.md

- `AGENTS.md`: Canonical unified protocol for user-visible behavior and Agent implementation strategy.
- `CLAUDE.md`: Relative symbolic link to `AGENTS.md`; never maintain a second content body.
- `SKILL.md`: Machine-readable operational specification that **ALL Agents MUST read** before operating.

Edit `AGENTS.md` only. The symlink keeps Claude Code and other Agent entry points byte-identical.

---

*Agent Guide Version: 1.6.0*
*Last Updated: 2026-09-09*

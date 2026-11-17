---
name: llm-wiki
version: "1.6.0"
description: "Use when an AI Agent (Claude Code, Codex, OpenClaw, or similar) needs to operate an llm-wiki knowledge base: ingest source files into Markdown wiki pages, answer questions from wiki/index.md and linked pages, run agent-bridge status/lint/link/relink/merge/query/index/Zotero relocation tasks, preserve provenance and temporal metadata, or use Zotero as a literature-discovery layer."
---

# LLM-Wiki

## Core Principle

Treat the LLM as the programmer and the wiki as the codebase. The user provides materials and judgment; the Agent extracts durable knowledge, preserves provenance, maintains links, and keeps the Markdown wiki structurally consistent.

Keep this file as the operational skill. Use `README.md` for user-facing overview, `AGENTS.md` / `CLAUDE.md` for the full protocol, and `ROADMAP.md` for project plans.

## Start Every Wiki Task

1. Read `AGENTS.md` or `CLAUDE.md` when the task touches wiki behavior, source handling, or ingest/query protocol.
2. Use the project Python: `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Unix, or `uv run python` when configured.
3. Run `<PY> scripts/agent-bridge.py check` before wiki operations. If it reports missing dependencies, state the exact blocker and continue only with tasks that do not require the unavailable runtime.
4. Protect `sources/`: never write Agent-generated summaries, drafts, or speculative content there. Only user-provided files or verified network fetches or Zotero MCP material may be source assets.
5. Check `git status --short` before editing. Do not revert user changes.
6. `wiki/*` is gitignored by default; when using ripgrep for wiki/source discovery, pass `--no-ignore` or read the files directly so ignored knowledge pages are not silently omitted.

## Choose the Work Mode

| Task | Use | Notes |
| --- | --- | --- |
| Status, lint, link discovery, relink, merge, semantic query, embedding index, Zotero sync planning | `scripts/agent-bridge.py` | Algorithmic/read-only tasks. Prefer dry-run before writing. |
| Ingest source material | Protocol mode | Requires LLM judgment: read source, extract metadata, create/update pages. |
| Answer wiki questions | Protocol mode | Read `wiki/index.md`, relevant pages, and link neighbors; synthesize with `[[PageName]]` citations. |
| Apply relation updates | Hybrid | Let `agent-bridge.py` discover candidates, then review and merge only safe changes. |
| Plan/apply Zotero attachment relocation | Hybrid | Use `zotero-relocate`; review dry-run, require local authorization for apply, and never bypass the Phase 0/API gate. Read the managed root from `config.yaml` `zotero_relocation.root` (prefer a cloud-synced path for cross-device use); `--root` is only a one-off override. |

Agent Bridge quick commands:

```bash
<PY> scripts/agent-bridge.py check
<PY> scripts/agent-bridge.py status
<PY> scripts/agent-bridge.py lint
<PY> scripts/agent-bridge.py link --source "PageName" --mode light
<PY> scripts/agent-bridge.py merge --source "NewPage" --target "OldPage" --strategy append_related --dry-run
<PY> scripts/agent-bridge.py relink --since 2026-04-20 --mode deep --dry-run
<PY> scripts/agent-bridge.py index
<PY> scripts/agent-bridge.py query "question" --semantic
<PY> scripts/agent-bridge.py zotero-plan --snapshot temp/zotero-snapshot.yaml --manifest-out temp/zotero-mutation-manifest.yaml
<PY> scripts/agent-bridge.py zotero-refresh --collection-key A9VNJUPI --manifest-out temp/zotero-refresh.yaml
<PY> scripts/agent-bridge.py zotero-ingest-verify --snapshot temp/zotero-snapshot.yaml --allocation temp/zotero-allocation.yaml --report-out temp/zotero-ingest-report.yaml
<PY> scripts/agent-bridge.py zotero-heal --snapshot temp/zotero-snapshot.yaml --manifest-out temp/zotero-heal.yaml
<PY> scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml --action audit --report-out temp/zotero-write-audit.yaml
<PY> scripts/agent-bridge.py zotero-relocate
```

Use legacy `python -m src.llm_wiki ...` only for human scripting or debugging. Do not use the legacy CLI as a substitute for LLM judgment during ingest.

### Interpret depth lint correctly

`agent-bridge.py lint` reports `Shallow Pages` as warning-only findings. The detector excludes related-page, source, and changelog sections, then combines normalized knowledge size, paragraph and section structure, local text-source volume, source count, and compression ratio. `QRF` is skipped by default; `lint_depth: skip` is reserved for deliberately concise pages whose source-coverage audit explains the exemption.

A clean depth result is not proof of source coverage. Re-read allocated sources and account for important mechanisms, equations, evidence, comparisons, procedures, failure modes, trade-offs, and decision rules. Never pad a page mechanically to satisfy a threshold.

## Ingest Workflow

1. Verify every source and extraction path before interpreting it.
2. Build a temporary source content map before drafting. Record major topic units, mechanisms, equations, quantitative evidence, comparisons, procedures, failure modes, decision rules, open questions, and extraction uncertainty.
3. Allocate each important unit deliberately: include it in the target page, merge it into an existing page, create a separately reusable concept page, or record a concrete omission reason. Do not omit material merely to fit a summary template.
4. Choose a page archetype and headings from the knowledge shape. The definition, provenance, related pages, sources, and changelog are invariants; mechanism, derivation, comparison, data flow, decision guide, failure modes, evidence, disputes, and open questions are conditional sections.
5. Compose the smallest page that preserves the source-defining reasoning. Explain why, how, under what assumptions, and where a claim fails. Preserve central formulas, numerical context, version differences, and engineering trade-offs when the source depends on them.
6. Run a coverage review before marking the page active. Every important source unit must be present, allocated elsewhere, or intentionally omitted with a reason in working notes.
7. Run a depth review: reject pages that merely restate an abstract, replace causal mechanisms with labels, list comparisons without dimensions, or use generic boundary statements.
8. When ingesting a batch, compare the drafts for template collapse. Similar heading and bullet patterns are acceptable only when the underlying knowledge structure is genuinely similar.
9. Add temporal metadata and visible time anchors where historical order matters.
10. Run link discovery and safe backward merges only after content review passes, then update `wiki/index.md` and `log.md`.
11. For Zotero-backed batch ingest, keep a complete allocation ledger under `temp/` and run `zotero-ingest-verify` before declaring coverage complete. Then run `zotero-plan`, review managed-tag/relation candidates, and use either Zotero MCP or the explicitly authorized restricted local write-back path; always verify the post-write state.

Source maps and coverage notes are temporary Agent working state. Keep them outside `sources/`; retain them under `temp/` only when the user requests an ingest audit or experiment.

Never treat `created` or `updated` as publication dates. They are wiki maintenance dates only.

## Query Workflow

1. Read `wiki/index.md` first.
2. Read relevant pages and their link neighbors. Semantic query may discover candidates, but page content is the source of truth.
3. Answer with citations to wiki pages using `[[PageName]]`.
4. If the answer creates reusable synthesis, ask or decide whether to archive it into the wiki according to user intent.

## Linking Rules

- Link the first meaningful mention of a concept in a local section.
- Keep every internal link resolvable to a real `wiki/*.md` stem by the end of ingest.
- Use canonical file stems and aliases, e.g. `[[AI-Coding-Workflow|AI Coding Workflow]]`.
- Avoid over-linking. Prefer one useful link over repeated noise.
- Describe temporal relationships when useful: early work, follow-up, contemporary route, survey, retrospective, or outdated-but-historically-important.

## Zotero Operations

All Zotero discovery, reads, source access, metadata planning, and normal writes for this skill **MUST use the MCP tools provided by [`54yyyu/zotero-mcp`](https://github.com/54yyyu/zotero-mcp)**. Before any Zotero task, read and follow [`docs/ZOTERO_MCP_INTEGRATION.md`](docs/ZOTERO_MCP_INTEGRATION.md), the single operational source of truth for availability gates, read/write workflows, source bindings, provenance, and safety.

The only temporary exceptions are the user-authorized Zotero 10 loopback write paths documented there. `zotero-writeback` accepts only a reviewed `mode: authorized-write` plan, adds `llm-wiki:*` tags, ensures reviewed reciprocal Related pairs, and performs read-after-write verification. `zotero-relocate` is separately gated and may update only an existing attachment `linkMode` / `path` plus private local bindings after filesystem and post-write verification. Neither path may clone/delete items, edit notes, change collections, or perform arbitrary API access. Tag removal is a separate scoped opt-in: only when a plan sets `policy.allow_managed_removals: true` and lists a tag under an item's `reviewed_removals`, and even then only managed `llm-wiki:*` tags other than the protected `llm-wiki:ingested` status tag and preserved tags (e.g. `llm-wiki:index-card`) may be removed — never unmanaged/user tags. `zotero-plan --removal-plan-out` generates such a plan whitelisted to retired `llm-wiki:<page_stem>` binding tags only. `--memory-authorize` keeps the local key in process memory only.

Do not substitute another Zotero skill/client or bypass Zotero MCP with direct SQLite/Web API access. If the required MCP or restricted local capability is unavailable, report the blocker, stop Zotero-side work, and continue only with useful wiki-local work.

## Source Fetch Safety

After any network fetch, verify before ingest:

- File is readable and non-empty.
- Content is not an error page, login wall, paywall notice, or JavaScript placeholder.
- Format matches extension, e.g. PDF begins with `%PDF`.
- Title and identifiers match the requested source.
- DOI, arXiv ID, author names, or URL match when provided.

If verification fails, do not create source-derived wiki pages. Record the failure in `log.md` when appropriate and ask the user for a correct source.

## File Handling

- Text and Markdown: read directly.
- PDF: use project Python with PyMuPDF or `scripts/read_pdf.py`; fall back to OCR only when necessary.
- Images: use visual inspection tools when needed.
- Office files and other binaries: use the relevant parser/tooling before extracting knowledge.

Prefer the project-managed Python environment: `.venv`, `uv run`, or the configured conda environment. Do not use global `pip` casually.

## Verification Before Finishing

For documentation-only edits, run:

```bash
git diff --check -- <changed-files>
```

For wiki/runtime operations, also run the relevant `agent-bridge.py` command (`check`, `lint`, `link`, `merge --dry-run`, `status`, or `query`) and report exact blockers if dependencies are missing.

For code changes, run the focused pytest target or the full suite when the change touches shared behavior:

```bash
.venv\Scripts\python.exe -m pytest tests/
```

End by summarizing changed files, verification output, and any skipped checks with the reason.

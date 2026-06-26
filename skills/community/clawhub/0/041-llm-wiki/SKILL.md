---
name: llm-wiki
description: "Use when Codex needs to operate an llm-wiki knowledge base: ingest source files into Markdown wiki pages, answer questions from wiki/index.md and linked pages, run agent-bridge status/lint/link/relink/merge/query/index tasks, preserve provenance and temporal metadata, or use Zotero as a literature-discovery layer."
---

# LLM-Wiki

## Core Principle

Treat the LLM as the programmer and the wiki as the codebase. The user provides materials and judgment; the Agent extracts durable knowledge, preserves provenance, maintains links, and keeps the Markdown wiki structurally consistent.

Keep this file as the operational skill. Use `README.md` for user-facing overview, `AGENTS.md` / `CLAUDE.md` for the full protocol, and `ROADMAP.md` for project plans.

## Start Every Wiki Task

1. Read `AGENTS.md` or `CLAUDE.md` when the task touches wiki behavior, source handling, or ingest/query protocol.
2. Use the project Python: `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Unix, or `uv run python` when configured.
3. Run `<PY> scripts/agent-bridge.py check` before wiki operations. If it reports missing dependencies, state the exact blocker and continue only with tasks that do not require the unavailable runtime.
4. Protect `sources/`: never write Agent-generated summaries, drafts, or speculative content there. Only user-provided files or verified network/Zotero fetches may be source assets.
5. Check `git status --short` before editing. Do not revert user changes.

## Choose the Work Mode

| Task | Use | Notes |
| --- | --- | --- |
| Status, lint, link discovery, relink, merge, semantic query, embedding index | `scripts/agent-bridge.py` | Algorithmic tasks. Prefer dry-run before writing. |
| Ingest source material | Protocol mode | Requires LLM judgment: read source, extract metadata, create/update pages. |
| Answer wiki questions | Protocol mode | Read `wiki/index.md`, relevant pages, and link neighbors; synthesize with `[[PageName]]` citations. |
| Apply relation updates | Hybrid | Let `agent-bridge.py` discover candidates, then review and merge only safe changes. |

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
```

Use legacy `python -m src.llm_wiki ...` only for human scripting or debugging. Do not use the legacy CLI as a substitute for LLM judgment during ingest.

## Ingest Workflow

1. Verify the source exists in `sources/` or came from a real verified network/Zotero operation.
2. Extract source metadata when available: title, authors/creator, URL, DOI, arXiv ID, Zotero item key, citation key, and source type.
3. Extract time metadata separately from wiki maintenance dates:
   - `published`: paper/post/release/documentation date.
   - `updated_at_source`: source-side update time when available.
   - `collected`: user save/import/Zotero collection time.
   - `ingested`: llm-wiki processing date.
   - `date_precision`: `day`, `month`, `year`, or `unknown`.
4. Create or update the smallest useful set of `wiki/*.md` pages. Every non-index page should have frontmatter, a one-sentence definition, knowledge content, related pages, sources, and changelog.
5. Add visible time anchors for dated works, especially on overview pages:
   - `**[YYYY.MM] Work name**` for day/month precision.
   - `**[YYYY] Work name**` for year-only precision.
   - `**[YYYY.MM-YYYY.MM]**` for ranges.
6. Use `## 时间线` / `## Timeline` when historical order matters. Start `### 时间定位` / `### Temporal Position` with:
   - `> **时间范围**：...`
   - `> **阶段判断**：...`
7. Run `agent-bridge.py link` for new pages. For high-confidence relations, preview `merge --dry-run`, review the diff, then apply only safe backward updates.
8. Update `wiki/index.md` and append `log.md`.

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

## Zotero Workflow

Use Zotero as the literature layer and llm-wiki as the distilled Markdown knowledge layer. A recommended public Zotero skill source is:

<https://github.com/openai/plugins/tree/main/plugins/zotero/skills/zotero>

When an Agent has that skill, or an equivalent Zotero-capable skill, it can search the local Zotero library, list collections/tags, export BibTeX/citations, read attachment paths or indexed full text on request, and import BibTeX/RIS records after confirmation.

For llm-wiki, Zotero results are source discovery and provenance. Preserve Zotero identifiers in frontmatter when available:

```yaml
sources_meta:
  - title: "Paper Title"
    type: "academic_paper"
    published: "2025-02"
    collected: "2026-05-24"
    ingested: "2026-05-24"
    date_precision: "month"
    zotero_item_key: "ABCD1234"
    citation_key: "author2025title"
    library_id: "0"
    zotero_uri: "zotero://select/items/ABCD1234"
```

Do not build a native llm-wiki Zotero client unless repeated manual workflows prove the need. Arbitrary document upload or attachment management is not part of the verified llm-wiki workflow.

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

# LLM-Wiki Unified Agent Protocol

> This document guides Claude Code, OpenClaw, and other AI Agents on how to use llm-wiki.
> `AGENTS.md` and `CLAUDE.md` are intended to be hard links to the same unified protocol file. Update one content body only.
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
5. Extract key insights and decide whether to create a new page or update an existing concept page.
6. Preserve `sources_meta` in frontmatter when source-level metadata is available.
7. Add a `## 时间线` / `## Timeline` section for overview pages or multi-source pages where historical order matters.
   - For papers, arXiv works, named methods, released systems, benchmark reports, or technical posts with a clear source date, show a compact visible date as a Markdown time anchor before the work name, e.g. `**[2024.02] FlashAttention V3**` or `**[2025.08] GRPO training discussion**`.
   - If only a year is reliable, use `YYYY`; do not invent a month.
   - Start `### 时间定位` / `### Temporal Position` with a blockquote summary using `> **时间范围**：...` and `> **阶段判断**：...` when the page has multiple dated nodes.
   - Prefer readable lists over wide Markdown tables when the row contains wiki links or long relationship text. Tables must not force narrow columns to wrap wiki links into broken fragments.
8. Run dynamic linking with `agent-bridge.py link` or `relink`, review diffs, and append safe backward updates.
9. Update `wiki/index.md` and append `log.md`.

Never treat `created` / `updated` as publication dates. They are wiki maintenance dates only.

### Query

For wiki queries, first read `wiki/index.md`, then relevant pages and link neighbors. Use semantic query only as candidate discovery; synthesize from the actual page content and cite wiki pages with `[[PageName]]`. If a query produces a lasting new synthesis, ask or decide whether to archive it into wiki according to user intent.

For questions that need source coverage, recent literature, annotations, or a specific paper, Zotero MCP may be used as a source-discovery layer. Zotero results are not the final answer; read metadata/fulltext/annotations, then synthesize with citations.

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
| **B** | Ingest material | **Yes** | Protocol mode (direct file ops) | N/A |
| **B** | Query & synthesize | **Yes** | Protocol mode (direct file ops) | N/A |
| **C** | Apply link results | **Agent judges** | `merge` (after reviewing diff) | Manual edit |

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
- `## Summary` — count table for orphans, dead links, stale, empty pages, duplicate titles, non-canonical links, drafts
- `## Orphan Pages` — pages not referenced by any other
- `## Dead Links` — `[[...]]` targets that are not real `wiki/*.md` file stems
- `## Stale Pages` — >90 days since last update
- `## Empty Pages` — files with no meaningful body text
- `## Duplicate Titles` — multiple files declaring the same `# Title`
- `## Non-Canonical Links` — wiki links whose target does not point to the real page file stem
- `## Draft Pages`

**Your action**: For dead links, create canonical page files or rewrite the link target to an existing file stem. For empty pages, fill them or remove duplicate shells. For duplicate titles, keep the canonical slug file (`Title-With-Spaces.md`) and merge or delete accidental variants. For non-canonical links, rewrite `[[Page Name]]` as `[[Page-Name|Page Name]]`. For orphans, consider adding backlinks from relevant pages.

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

### Absolute Prohibitions

- **NEVER** save LLM-generated text, summaries, or speculative content as `.md`, `.txt`, or any format into `sources/`
- **NEVER** claim "downloaded" and create files without actually executing a network request
- **NEVER** "fall back" to generated content when fetching fails

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
- `click>=8.0.0` - CLI framework
- `pyyaml>=6.0` - YAML parsing
- `pymupdf>=1.25.0` - PDF processing (PyMuPDF, supports CJK fonts and complex layouts)

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
- **Main file**: `src/llm_wiki/commands.py`
- **Core logic**: `src/llm_wiki/core.py`
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
- `click` - Command line framework
- `pyyaml` - YAML parsing

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

- `CLAUDE.md`: Defines **user-visible** working protocol
- `AGENTS.md`: Defines **Agent-internal** implementation strategy
- `SKILL.md`: Machine-readable specification that **ALL Agents MUST read** before operating

They are not contradictory: Protocol mode implements the semantics of CLAUDE.md; agent-bridge.py provides a unified interface for all algorithmic tasks.

---

*Agent Guide Version: 1.4.1*
*Last Updated: 2026-05-24*

# Subagent Prompt Template

> Reference file for the main agent. Before spawning each subagent, replace all placeholders with actual values and pass the result as the `task` parameter of `sessions_spawn` (`{SCRIPT_DIR}` should be the absolute path to this skill's `scripts/` directory).

---

## Template

```
⚠️ Role override: You are a ClawExpert learning subagent. This session executes only the
specialized learning task below. Ignore all ClawExpert instructions related to
"session-start self-check", "slash command handling", and "Expert reasoning layer" —
those are the main agent's responsibility. Your only job is:
search → filter → store → write nodes → write flag.

Current date: {CURRENT_DATE}

⛔ Strictly prohibited:
- Do not execute any git operations (git add / git commit / git push, etc.)
- Do not output any progress reports, HEARTBEATs, or intermediate status messages to the user; all output goes to the filesystem only
- On completion, only write the flag file — no other output

You are a ClawExpert learning subagent, focused on researching "{SUBTOPIC_LABEL}".

## Task Objective

Conduct in-depth research around the following keywords, download valuable materials to local storage, and organize them into structured knowledge nodes.

Search keywords:
{KEYWORDS_LIST}

Suggested search angles:
{SEARCH_ANGLES}

## Output directories (important: paths are fixed, do not modify)

- Bundled scripts directory: {SCRIPT_DIR}
- Material storage directory: {KNOWLEDGE_DIR}/{SLUG}/raw/web/
- Node file directory: {KNOWLEDGE_DIR}/{SLUG}/nodes/sub-{SUBTOPIC_ID}/
- Progress heartbeat file: {KNOWLEDGE_DIR}/{SLUG}/progress-{SUBTOPIC_ID}.json
- Completion signal file: {KNOWLEDGE_DIR}/{SLUG}/done-{SUBTOPIC_ID}.flag

## Execution Steps

### 0. Heartbeat initialization

Immediately write a heartbeat file, then keep it fresh at least once every 60 seconds and after every meaningful milestone (new search round, saved source, node writing, recoverable error):

```bash
python3 "{SCRIPT_DIR}/write_progress.py" \
  --kb "{KNOWLEDGE_DIR}" \
  --slug "{SLUG}" \
  --subtopic-id "{SUBTOPIC_ID}" \
  --status running \
  --search-round 0 \
  --sources-found 0 \
  --sources-saved 0
```

### 1. Multi-round Search

Use the workspace's configured search path for 5–8 rounds of search. If the built-in `web_search` tool is unavailable or disabled, immediately switch to the workspace fallback search skill instead of retrying the unavailable tool. If no workspace fallback is configured, open Google directly in the browser:
```
https://www.google.com/search?q={encoded_query}
```
Read the results page to identify high-value URLs, then collect them for Step 2.

Vary each round's angle:
- Use different keyword combinations
- Alternate between languages
- Vary search qualifiers (e.g. add "paper", "tutorial", "2025", "comparison", etc.)
- Approach from different perspectives (principles / applications / comparisons / latest developments / critiques / limitations)

**Book sources — actively hunt for these in every topic:**
- Search by classic book titles + "pdf" or "full text" (e.g. `"Thinking Fast and Slow" pdf`, `"Misbehaving" Thaler full text`)
- Try open-access repositories: `archive.org`, `gutenberg.org`, `pdfdrive.com`, `openlibrary.org`
- Use qualifiers: `filetype:pdf site:archive.org {TOPIC}`, `{AUTHOR} book chapter pdf`
- Google Books previews with substantial extractable chapters count as T2 sources
- For Chinese topics: also search 豆瓣读书, 微信读书书单, 知网书目 for authoritative books, then find PDF copies
- If a book is a canonical reference for the subtopic (e.g. Kahneman for behavioral economics, Shiller for irrational exuberance), prioritize finding and fetching at least 2–3 chapters before moving on to papers

### 2. Content Retrieval

For valuable pages found in search results, use web_fetch to retrieve the full text.

### 3. Quality Filtering

Each piece of material must simultaneously satisfy all of the following conditions, or be discarded:
1. Body text length > 300 words (excludes pure navigation pages and ad pages)
2. Contains specific data, conclusions, methodology, or academic citations (excludes vague descriptions)
3. Source domain is trustworthy (excludes content farms and pure SEO sites)
4. Has substantive content overlap with the subtopic keywords (not just a title match)

### 4. Material Storage

Write materials that pass the filter to local files.

#### ⚠️ File naming — MANDATORY

Every stored file (web or PDF) **MUST** be named using the **first 6 hex characters of the source URL's SHA-256 hash**. Descriptive names are strictly forbidden.

```bash
hash=$(echo -n "{SOURCE_URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6)
# Result example: a3f9c1
# Web file:  a3f9c1.md   — NEVER use a descriptive name like "attention-paper.md"
# PDF binary: a3f9c1.pdf  — NEVER use a descriptive name like "attention-is-all-you-need.pdf"
# PDF extracted: a3f9c1.md (or a3f9c1/_index.md for large files)
```

Existence check before writing (skip if already exists):
```bash
ls "{KNOWLEDGE_DIR}/{SLUG}/raw/web/${hash}.md" 2>/dev/null           # web
ls "{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}" 2>/dev/null || \
  ls "{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}.md" 2>/dev/null          # pdf
```

#### Routing decision

Before storing, determine the source type:

1. **Direct PDF URL** — URL ends in `.pdf`, or `curl -I` shows `Content-Type: application/pdf` → PDF workflow using this URL directly
2. **Academic paper abstract page** — construct the PDF URL, then use PDF workflow:
   - `arxiv.org/abs/{id}` → `https://arxiv.org/pdf/{id}.pdf`
   - `aclanthology.org/{id}` → `https://aclanthology.org/{id}.pdf`
   - `openreview.net/forum?id={id}` → scan fetched HTML for a PDF download link
   - Other conference/journal pages (NeurIPS, ICML, ICLR, AAAI, CVPR, ECCV, ACL, EMNLP, etc.) → scan fetched HTML for a `.pdf` link
   - Use the **PDF URL** as the hash source and `source_url` in frontmatter
3. **Everything else** → web page workflow, store under `raw/web/`

---

**Web page** (routing case 3) → fetch with `web_fetch`, store under `raw/web/`.

**PDF** (routing case 1 or 2) → follow the complete PDF workflow below.

---

#### PDF Processing Workflow

##### Step A — Compute hash and check existence

```bash
hash=$(echo -n "{PDF_URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6)
ls "{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}" 2>/dev/null || ls "{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}.md" 2>/dev/null
```
If either exists, skip — do not re-download.

##### Step B — Download to local

```bash
local_pdf="{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}.pdf"

# Primary: curl (follows redirects, handles most PDF URLs)
curl -L --max-filesize 104857600 -o "${local_pdf}" "{PDF_URL}" 2>/dev/null
```

If curl exits non-zero (download failed or URL is a landing page, not a direct PDF):
1. Use `web_fetch` on the URL to retrieve the HTML page
2. Extract the direct PDF download link from the page content
3. Retry `curl -L` on the extracted direct link

If still no local file after the above, skip this source.

##### Step C — Check size and page count

```bash
python3 -c "
import re, os, sys
path = sys.argv[1]
size_mb = os.path.getsize(path) / (1024 * 1024)

# Pure-Python page count: read PDF structure bytes, no external deps needed
page_count = 0
try:
    with open(path, 'rb') as f:
        data = f.read(min(os.path.getsize(path), 500_000))
    matches = re.findall(rb'/Count\s+(\d+)', data)
    if matches:
        page_count = max(int(m) for m in matches)
except Exception:
    pass
if page_count == 0:
    page_count = max(1, int(size_mb * 20))  # fallback estimate: ~50KB/page

print(f'{size_mb:.1f}MB {page_count}pages')
" "${local_pdf}"
```

##### Step D — Route by size

| Condition | Path |
|-----------|------|
| ≤ 20 MB **and** ≤ 20 pages | **Small** — full pdf tool call |
| ≤ 20 MB **and** 21–100 pages | **Medium** — sectioned pdf tool call |
| > 20 MB **or** > 100 pages | **Large** — Python full-text extraction |

---

##### Small PDF path (≤ 20 MB, ≤ 20 pages)

Call the `pdf` tool on the **local path**. **Do NOT pass a `model` parameter** — always let the system default handle routing. Specifying an explicit model almost always fails due to missing keys or quota limits.

Use this extraction prompt (pass as `prompt`; do not pass `model`):
> Extract the full content of this document in Markdown format. For all text sections: reproduce content faithfully. For all figures, charts, tables, and diagrams: describe their key data points, axis labels, legends, and main conclusions in plain text.

If the call fails → retry once with the same bare call.
If it fails again → fall through to **Python fallback** below.

Add `extraction_method: pdf_tool` to frontmatter. If no figures/charts reported: `has_images: false`; otherwise `has_images: true`. For scanned PDFs (no text layer): also add `scanned: true`.

---

##### Medium PDF path (21–100 pages)

Build a combined page-range string covering the key sections. Given total page count N:

```
opening  = "1-{min(8, N)}"
middle   = "{max(9, N//2 - 4)}-{min(N-8, N//2 + 5)}"
closing  = "{max(N-7, 9)}-{N}"
pages_arg = "{opening},{middle},{closing}"   # e.g. "1-8,21-30,43-50"
```

Call the `pdf` tool once on the **local path** with `pages: "{pages_arg}"` and the same extraction prompt above. **Do NOT pass `model`.**

Prefix the extracted content with:
```
[Partial extraction: pages {pages_arg} of {N} total. Key sections only — use Python fallback for full text.]
```

If the call fails → retry once → fall through to Python fallback.

Add `extraction_method: pdf_tool_partial` and `page_count: {N}` to frontmatter.

---

##### Large PDF / Python fallback (> 50 MB or > 100 pages, or pdf tool failed)

```bash
python3 -c "
import sys, subprocess

path = sys.argv[1]
text = ''

try:
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        text = '\n\n'.join(page.extract_text() or '' for page in pdf.pages)
except ImportError:
    # pdftotext (poppler-utils) — commonly available on macOS/Linux
    result = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True)
    if result.returncode == 0:
        text = result.stdout
    else:
        print('ERROR: no PDF extraction tool available', file=sys.stderr)
        sys.exit(1)

print(text)
" "${local_pdf}"
```

After extraction, write the result to the correct path — **do not create any other directory (e.g. `processed/`)**:

```bash
out_md="{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/${hash}.md"
```

Construct the file with frontmatter + extracted body, then write to `${out_md}`:
```
---
source_url: {PDF_URL}
title: {title}
fetched_at: {ISO 8601}
topic: {SLUG}
subtopic: {SUBTOPIC_ID}
word_count: {estimated}
extraction_method: text_only
has_images: false
---

{extracted text}
```

Add `extraction_method: text_only` to frontmatter. Image/figure content will be absent.

After writing, check the extracted word count:
- **< 500 words**: the PDF is image-dominant (e.g. papers with many full-page figures). Add `sparse_text: true` to frontmatter. Do NOT split, do NOT supplement with AI-generated content — write the extracted text as-is in a single `${hash}.md`. Note the limitation in the node's Source Evidence entry.
- **500–5000 words**: write as a single `${hash}.md`, no splitting needed.
- **> 5000 words**: apply the **large-file sub-tree** splitting below (parts + `_index.md`).

---

#### File naming (web and PDF)

First 6 hex characters of the URL's SHA-256 hash:
```bash
echo -n "{URL}" | openssl dgst -sha256 | awk '{print $NF}' | cut -c1-6
```

Existence check before writing:
```bash
ls "{KNOWLEDGE_DIR}/{SLUG}/raw/web/{hash}.md" 2>/dev/null    # web
ls "{KNOWLEDGE_DIR}/{SLUG}/raw/pdf/{hash}" 2>/dev/null        # pdf (may be dir or .md)
```

#### File format

```
---
source_url: {full URL}
title: {page title or filename}
fetched_at: {ISO 8601 time}
topic: {SLUG}
subtopic: {SUBTOPIC_ID}
word_count: {estimated body word count}
extraction_method: {web_fetch | pdf_tool | pdf_tool_partial | text_only}   # omit for web pages
has_images: {true | false}          # PDF only
page_count: {N}                     # PDF medium/large only
scanned: true                       # PDF only, if no text layer detected
---

{cleaned body content}
```

⚠️ **Fidelity rule — applies to ALL raw/ files without exception**:
The `raw/` directory stores **faithful reproductions of source material only**. Never write AI-generated summaries, paraphrases, curated quote collections, or analytical notes into raw files. If the extracted text is sparse or low quality, write it as-is and mark it accordingly — do not compensate by synthesizing content from your own knowledge.

Cleaning rules:
- Web page: remove navigation bars, sidebars, footers, ads, cookie banners; preserve headings, paragraphs, lists, tables, code blocks; preserve link text (URLs may be removed)
- PDF (`pdf_tool` / `pdf_tool_partial`): write model output as-is — do not strip further; image content already described inline as text
- PDF (`text_only`): apply same cleaning rules as web pages; image/figure content absent; write the raw extracted text verbatim
- Scanned PDF: `pdf_tool` attempts vision-based description; content quality may be limited

**Large file sub-tree** (apply after writing, for both web and PDF):

After writing, estimate word count. If word count > 5000:

1. Create a directory to replace the single file:
   ```bash
   mkdir -p "{KNOWLEDGE_DIR}/{SLUG}/raw/{type}/{hash}"
   ```

2. Analyze document structure — identify chapters, sections, or major headings.
   - **If the document has clear logical structure** (numbered sections, chapter headings, titled subsections) → **split by logical boundaries first** — each major section becomes one part (merge very short sections < 500 words with the next)
   - **If no clear structure** → split into chunks of ~5000 words each, cutting at paragraph boundaries (never mid-sentence or mid-paragraph)
   - Either way: keep each part between 2000–8000 words; if a logical section exceeds 8000 words, split it further at the next heading level

3. Write `{KNOWLEDGE_DIR}/{SLUG}/raw/{type}/{hash}/_index.md`:
   ```
   ---
   source_url: {full URL or local path}
   title: {title}
   fetched_at: {ISO 8601 time}
   topic: {SLUG}
   word_count: {total}
   parts: {number of part files}
   extraction_method: {web_fetch | pdf_tool | text_only}
   ---

   ## Document Overview
   {2–4 sentences summarizing the full document's scope, main argument, and key findings}

   ## Part Index
   - [part-001](part-001.md) — {section title} | {1 sentence describing the specific content: what concepts, data, or conclusions this part contains}
   - [part-002](part-002.md) — {section title} | {1 sentence describing the specific content}
   ...
   ```
   ⚠️ The Part Index summary MUST be a genuine semantic description written after reading the part — NOT the first few words of the text, NOT "chunk N". A QA subagent uses these summaries to decide which part to read without reading all parts.

4. Write each part as `part-001.md`, `part-002.md`, etc. Each part should begin and end at a natural boundary (heading or paragraph break); include ~200-word overlap with the previous part at the start of each part (except part-001) to avoid conclusions being cut mid-sentence.

5. Delete the original single-file `{hash}.md` (only the directory `{hash}/` remains).

When referencing a large-file source in node.md, point to `{hash}/_index.md`; reference specific parts as `{hash}/part-00N.md` when citing a specific section.

### 5. Conclusion Extraction and Node Writing

Create the node directory:
```bash
mkdir -p "{KNOWLEDGE_DIR}/{SLUG}/nodes/sub-{SUBTOPIC_ID}"
```

Write the node file `{KNOWLEDGE_DIR}/{SLUG}/nodes/sub-{SUBTOPIC_ID}/node.md`:

```
---
id: {SUBTOPIC_ID}-{current timestamp in ms}-001
parent: root
label: {SUBTOPIC_LABEL}
type: topic
depth: 2
confidence: {>=3 sources: high | 1-2 sources: medium | 0 sources: low}
last_updated: {YYYY-MM-DD}
source_count: {number of valid sources}
---

## Summary
{2–5 sentences summarizing the core findings for this subtopic}

## Key Conclusions
- {Conclusion 1} ([source title](../../raw/web/{hash}.md))
- {Conclusion 2} ([source title](../../raw/pdf/{hash}/_index.md))

## Source Evidence
- [{web source title}](../../raw/web/{hash}.md) — {one sentence explaining the core value of this source}
- [{pdf single-file title}](../../raw/pdf/{hash}.md) — {one sentence}
- [{pdf multi-part title}](../../raw/pdf/{hash}/_index.md) — {one sentence}; key data in [part-002](../../raw/pdf/{hash}/part-002.md)

## Analytical Framework (if applicable)
{If this subtopic involves a reusable analytical framework or methodology, describe it here}

## Further Directions
- [ ] {A related direction or open question discovered during research that falls outside this subtopic's scope — worth exploring in a future --deepen run}
- [ ] {Another such direction, if any}
```

If no out-of-scope directions were found, omit the `## Further Directions` section entirely.

If the content volume is large, multiple node files may be created: `node.md`, `node-detail-001.md`, ...

### 6. Time Control

Before each search round, read meta.json to check for timeout:
```bash
cat "{KNOWLEDGE_DIR}/{SLUG}/meta.json"
```
Read the `learning_sessions[0].started` field and calculate elapsed time.
If more than {MAX_HOURS} hours have elapsed, stop searching and proceed to Step 7.

### 7. Completion Signal

Write the final flag using the bundled script and remove the progress heartbeat:

```bash
python3 "{SCRIPT_DIR}/write_flag.py" \
  --kb "{KNOWLEDGE_DIR}" \
  --slug "{SLUG}" \
  --subtopic-id "{SUBTOPIC_ID}" \
  --status done \
  --sources-added ACTUAL_COUNT \
  --node-file "{KNOWLEDGE_DIR}/{SLUG}/nodes/sub-{SUBTOPIC_ID}/node.md" \
  --cleanup-progress
```

Replace `ACTUAL_COUNT` with the actual number of valid materials downloaded (integer); all other placeholders are replaced with real values when the subagent prompt is generated.

If the subtopic exhausts high-quality sources or encounters a hard failure, still write a terminal flag with status `partial`, `failed`, `timeout`, or `no_results` and include `--cleanup-progress` so the main agent can continue.

## Notes

- Verify each URL is reachable before calling web_fetch
- Apply the four-tier source priority system when selecting and filtering sources:
  - T1 (highest): peer-reviewed papers, official government/standards documents, primary legal texts, clinical systematic reviews, **canonical academic books** (e.g. university press monographs, landmark textbooks cited in >100 papers)
  - T2: institutional technical docs, major org research reports, university press books/chapters, regulatory filings, **widely-cited popular science books by domain experts** (e.g. Kahneman, Thaler, Shiller)
  - T3: reputable specialist media (IEEE Spectrum, FT, Bloomberg, MIT Tech Review, Reuters, Nature News)
  - T4: quality general media — background reference only; cross-verify with T1/T2 before citing
  - Discard: content farms, SEO sites, unattributed content, sites with clear commercial bias
- Within the same tier: institutional primary source > third-party reporting; raw data > conclusions only; recent (within 2 years) > outdated
- When media reports a study, find the original paper — the media report drops to T3/T4
- Preprints (arXiv pre-review): treat as high-credibility but flag as "not yet peer-reviewed" in node conclusions
- If a keyword yields no valuable results after 2 search rounds, change the angle and continue — do not get stuck on fruitless searches
- Conclusions must be specific, including numbers, comparisons, and method names — not vague descriptions
- If out-of-scope but highly valuable content is found, download it anyway — the main agent will handle attribution during merge
```

---

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{CURRENT_DATE}` | Today's date | `2026-03-21` |
| `{SUBTOPIC_LABEL}` | Human-readable subtopic title | `GRPO vs PPO Comparative Analysis` |
| `{KEYWORDS_LIST}` | Search keywords, one per line | `GRPO vs PPO\nGroup Relative Policy Optimization` |
| `{SEARCH_ANGLES}` | Search angle descriptions, one per line | `algorithm comparison\nmemory usage benchmarks` |
| `{KNOWLEDGE_DIR}` | Expanded knowledge base root path | `/Users/user/.openclaw/workspace/knowledge` |
| `{SLUG}` | Topic slug | `rl-reasoning-最新进展` |
| `{SUBTOPIC_ID}` | Subtopic ID | `grpo-vs-ppo` |
| `{MAX_HOURS}` | Max learning duration | `2` |

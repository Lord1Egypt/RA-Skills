---
name: arxiv-papers
description: "Find and summarize arXiv.org preprints—keyword/category search, abstracts, PDF links. Use for literature scans, paper IDs, or quick orientation (not peer-review, not medical/legal advice)."
---

# ArXiv Papers

Use the **arXiv API** (and optional PDF fetch) to **locate** papers and **summarize abstracts** for the user. Treat results as **preprints**—not necessarily peer-reviewed or final.

## When to use

- “What’s new on arXiv about …”, “Summarize arXiv:XXXX”, category browsing (e.g. `cs.AI`).
- Quick **orientation** before deeper reading—not a substitute for reading the full paper in serious research.

## Limits (say explicitly when relevant)

- **Coverage**: arXiv only; many venues are not there.
- **Quality**: preprint ≠ endorsed truth; contradictory claims exist.
- **Rate / ToS**: respect arXiv’s API guidelines; don’t hammer endpoints.

## Workflow

1. Run `scripts/search_arxiv.sh "<query>"` and parse the returned XML (`<entry>`, `<title>`, `<summary>`, PDF `<link>`).
2. Present **title, authors, id, abstract summary**, and link to abstract/PDF.
3. If the user wants depth, **PDF** may be fetched selectively—large files and parsing limits apply.
4. Optionally append notable papers to `memory/RESEARCH_LOG.md` (if your environment uses it):

   ```markdown
   ### [YYYY-MM-DD] TITLE
   - **Authors**: …
   - **Link**: …
   - **Summary**: …
   ```

## Examples

- Latest LLM reasoning papers on arXiv.
- “What is paper `2512.08769` about?”

## Resources

- `scripts/search_arxiv.sh` — thin wrapper over the arXiv API.

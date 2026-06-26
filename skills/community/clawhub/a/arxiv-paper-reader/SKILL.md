---
name: arxiv-paper-reader
description: Search arXiv by keyword, filter by submitted date range, fetch arXiv papers from an arXiv ID or URL, convert papers into Markdown and PDF files in the workspace, and maintain daily topic archives with summary files. Use when the user wants to search arXiv, browse recent keyword-matched papers, ingest a specific paper, summarize arXiv content, or run a recurring topic sync.
metadata: {"openclaw":{"os":["win32","linux","darwin"],"requires":{"anyBins":["python","python3"]}}}
---

# arXiv Paper Reader

Use the bundled Python scripts before reasoning about arXiv content. They handle:

- searching arXiv by keyword
- filtering keyword results by submitted date range
- downloading arXiv metadata and paper content
- converting papers to Markdown and PDF in the workspace
- syncing configured topics into daily archive folders

## Inputs

- Accept raw arXiv IDs like `1706.03762` or URLs such as `https://arxiv.org/abs/1706.03762`.
- Only accept raw IDs or HTTPS arXiv URLs on `arxiv.org`, `www.arxiv.org`, or `export.arxiv.org`.
- Accept keyword searches such as `transformer`, `diffusion`, or `computer vision`.
- Accept optional submitted-date windows using `YYYY-MM-DD`.
- Do not use category filters or alias-based domain shortcuts; search is intentionally keyword-only.

## Search workflow

1. Pick a Python command:
   - Prefer `python`
   - Fall back to `python3`
2. If the user wants search results or the latest papers for a topic, run:

```bash
python {baseDir}/scripts/search_arxiv.py --query "<keywords>" --limit <n>
```

3. Read `search_results.md` and `search_results.json`.
4. Use `{baseDir}/references/search-usage.md` to present the results.
5. If the user asks for the latest papers matching a keyword, pass `--sort submittedDate`.
6. If the user wants the default best-match ranking, omit `--sort` and let the script use relevance order.
7. If the user gives a date window, add `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`.

## Topic sync workflow

1. Tell the user to maintain `{rootDir}/topics.json`, or seed it from `{baseDir}/references/topics.example.json`.
2. For recurring daily updates, run:

```bash
python {baseDir}/scripts/sync_arxiv_topics.py --daily --root-dir <root-dir>
```

3. For manual backfill, run:

```bash
python {baseDir}/scripts/sync_arxiv_topics.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --root-dir <root-dir>
```

4. Read `<root-dir>/runs/<capture-date>/run_manifest.md` first.
5. Each captured paper lives at `topics/<topic-slug>/<capture-date>/<paper-id>__<title-slug>/`.
6. Expect each paper directory to contain `paper.pdf`, `paper.md`, `metadata.json`, and `summary.md`.
7. The batch summary is template-based and grounded in the abstract plus converted Markdown; treat it as a review aid, not a substitute for reading the paper.

## Fetch workflow

1. Choose an output directory:
   - If the user gives one, use it.
   - Otherwise write to `./artifacts/arxiv/<paper-id>/` in the current workspace.
2. Run the converter:

```bash
python {baseDir}/scripts/arxiv_to_md.py <paper-id-or-url> --output-dir <target-dir>
```

3. Read the generated `paper.pdf`, `paper.md`, and `metadata.json`.
4. Summarize the paper in Markdown.
5. Save the summary to `<target-dir>/summary.md` if the user asked for files. Otherwise return the summary directly in chat.

## Summary format

Use the headings in `{baseDir}/references/summary-format.md`.

Keep the summary grounded in the generated Markdown. If the conversion falls back to abstract-only mode, say so explicitly in the summary.

## Safety

- Pass IDs, URLs, and keywords as single CLI arguments. Do not splice untrusted text into shell pipelines.
- Only pass raw arXiv IDs or HTTPS arXiv URLs; reject arbitrary third-party URLs.
- TLS verification is strict. If requests fail because your machine lacks a valid CA bundle, install `certifi` or fix the system trust store.
- arXiv source archives are processed in-memory, only `.tex` members are read, and suspicious paths plus oversized payloads are rejected before parsing.
- Date windows use arXiv `submittedDate` and inclusive `YYYY-MM-DD` boundaries.
- Do not invent claims that are not supported by `paper.md` or `search_results.md`.
- Do not reintroduce hardcoded category or alias mappings; keep search behavior keyword-only.

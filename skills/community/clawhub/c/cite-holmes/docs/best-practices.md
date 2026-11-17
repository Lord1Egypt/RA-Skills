# Best practices by scenario (v3.6)

## 1. Pre-submission check (论文投稿预检)
```bash
python scripts/verify_refs.py --refs my_paper_refs.json --profile medical \
    --export bibtex,gbt7714 --out report.md --strict
```
- Run on the FINAL reference list; `--strict` gates your CI/退出码 on any
  non-verified item.
- `invalid` → remove or replace. `unreachable` → open the Wayback link in the
  report; re-run with `--cn`/proxy before concluding anything.
- Export GB/T 7714-2025 for Chinese journals (entries are built from
  registry-authoritative CSL metadata — 期刊/年/卷期页 come from the registry,
  not your typed fields).

## 2. Checking AI-generated text (AI 生成内容的事实核查)
- Extract every citation the model produced into refs objects (title + any of
  doi/pmid/arxiv/url). Fabricated DOIs/PMIDs are caught at L0.
- Expect a meaningful `invalid` rate on unconstrained model output — that is
  the tool working. Read `needs_human_check` items individually.

## 3. Agent / MCP integration
- Point your client at the MCP server (see `mcp/README.md`); have the agent
  call `verify_references` on its own reference list BEFORE writing conclusions,
  and `explain_verdict` on every non-verified item.
- Batch ≤50 per call. Use the `fact_check_workflow` prompt as the template.

## 4. Lossy network / CN egress
- `--cn` raises the timeout floor to 25s and adds a Crossref second-host
  fallback for DOI metadata. Pair with `--proxy` when needed.
- `unreachable` ≠ fake: re-run before judging. The report always separates
  "transport failed" from "identifier not found".

## 5. Daily CI gate (团队/机构)
```bash
python scripts/verify_refs.py --refs refs.json --strict --offline=false \
    --no-contexts --out report.md && test -s report.md
```
- Disk cache (7-day TTL) keeps repeat runs fast and deterministic; use
  `--refresh-cache` when you need fresh registry state.

## 6. Context check for a finished draft (成稿上下文核验, v3.7.0)
```bash
python scripts/verify_refs.py --refs refs.json --check-document paper.md --out report.md
```
- Every in-text marker is bound to a reference entry; the citing sentence is
  scored against the cited title (anchor rate, threshold 0.34).
- `低锚词/low anchor` = the citing sentence shares almost no content words with
  the cited title — the classic "cited paper A, claimed paper B" mis-citation.
  Review these before submission; semantic support itself stays with the agent.
- Available over MCP as the `check_document` tool for agent workflows.

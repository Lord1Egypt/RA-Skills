---
name: dr-document-intake
description: Preserve uploaded documents and make their full extracted contents searchable; audit missing, stale, and unsupported documents.
---

# Document intake and search coverage

Use for uploaded, received, or saved work documents of any subject, including documents outside `memory/`; also use when checking document-search coverage. Apply the calling agent's existing permissions and document-retention policy.

## Intake

1. Preserve one authoritative original in the appropriate workspace location. Do not rename, replace, or delete a user's original just to index it.
2. Run `<python> <skill-dir>/scripts/document_intake.py ingest --workspace <workspace> <original>` using absolute skill and workspace paths. For PDF/Office files, use the agent's Python environment that has MarkItDown; the recommended per-agent location is `~/.local/share/dr-document-intake/venv/bin/python`. The derived Markdown goes under `memory/documents/` with its original workspace-relative path and source hash; it is not a summary. For native Markdown already under `memory/`, index the original directly.
3. Use Microsoft MarkItDown locally for supported non-text formats. If the Python environment lacks it, use an existing approved local converter or install the free `markitdown[pdf,docx,pptx,xlsx,xls,outlook]==0.1.9` package in a task-specific virtual environment; never send documents to an external service without authorization. For scanned/image-only or partially extracted documents, use an available local OCR method, or report the gap. To register local OCR/converter output, capture the original's SHA-256 before conversion, then pass `--markdown-from <text-file> --source-sha256 <captured-hash>` to the helper. Keep intermediate text in a protected temporary location outside audited document roots and remove it after use. Verify OCR quality and report unreadable pages; never claim complete extraction merely because conversion returned text.
4. Run a real `memory_search` with distinctive source content and verify the returned source path refers to the extract or indexed original. Check that indexing includes the derived location, embedding provider is actually semantic/hybrid, and no search warning or stale/partial status is present. A fresh extract, a search result from a summary, or keyword-only search does not prove semantic indexing. Do not report the document searchable until the appropriate path passes; explicitly report pending, unsupported, partial or failed work. Record each unresolved source path and reason in the agent's existing `memory/open-loops.md` (read it first), including types outside the helper's audit list; resolve the entry after a successful recheck.
5. When the original changes, rerun intake. The helper replaces only its own derived output after confirming the original remained unchanged; a stale output is quarantined outside indexed memory before a failed refresh. Keep source paths and hashes so extracts cannot silently become competing originals.

## Coverage review

Run `python3 <skill-dir>/scripts/document_intake.py audit --workspace <workspace>` after a batch of intake or when reviewing coverage. It inventories common document formats under the workspace, excluding operational/tool directories and generated extracts; it reports missing, stale, malformed, orphaned, unreadable, symlinked and unsupported items. These exclusions and extensions are bounded: explicitly inspect any other document roots or types the task uses, and treat an unscanned root as unverified, not covered. `fresh` means the extract matches its source hash, **not** that it has been indexed or recalled.

Fix each in-scope issue, or record it as a specific gap. For an orphaned extract, first confirm the original really was removed or moved, then run `python3 <skill-dir>/scripts/document_intake.py quarantine --workspace <workspace> <extract>`; this moves only a helper-owned extract outside indexed memory. Do not quarantine originals or unfamiliar files. Check actual index/search status separately and test exact identifiers and semantic paraphrases from representative documents. Verify changes become searchable and old content no longer wins. Retrieval ranking is not a guarantee that every passage will appear in every query.

The helper is invoked by the agent, not a filesystem hook. A skill alone does not monitor arbitrary writes; wire the intake rule into each agent's startup/attachment workflow and run the audit at handoff or review. For the fleet handoff, use [references/fleet-rollout.md](references/fleet-rollout.md). Do not create background jobs, change search configuration, publish a fleet skill, or modify another agent merely by installing this skill; those require their applicable scope and approval.

---
name: calibre-catalog-read
description: "Search/view a Calibre catalog or prepare and validate one-book analysis without changing library metadata. Route metadata edits, including comments and tags, to calibre-metadata-apply."
metadata: {"openclaw":{"requires":{"bins":["node","calibredb"]},"optionalBins":["python3","ebook-convert","pdftotext"],"optionalEnv":["CALIBRE_WITH_LIBRARY","CALIBRE_LIBRARY_ID","CALIBRE_USERNAME","CALIBRE_PASSWORD"],"localWrites":["user cache and state directories"],"modifiesRemoteData":[]}}
---

# Read the catalog without modifying it

1. Resolve this skill's absolute directory as {baseDir}. Read the workspace AGENTS.md Tools notes for the server, library ID, and authentication. Use configured environment/default config first; do not ask for known connection details.
2. Use the wrapper below for list/search/id. An ID or "show/check/view/details" request is not edit intent. Confirm the exact target before exporting or doing full-book analysis.
3. Return the retrieved metadata with its ID. Distinguish an empty match from connection/tool failure; possibly_truncated means the bounded result may be incomplete, not that the entire library was examined.

    node "{baseDir}/scripts/calibredb_read.mjs" list --limit 50
    node "{baseDir}/scripts/calibredb_read.mjs" search --query 'series:"中公文庫"' --limit 100
    node "{baseDir}/scripts/calibredb_read.mjs" id --book-id 3
    node "{baseDir}/scripts/calibredb_read.mjs" libraries --with-library "http://HOST:8080/"

## Connection contract

Precedence: --with-library, CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL, then config.with_library. A server URL must select #LIBRARY_ID; use --library-id, CALIBRE_LIBRARY_ID, or config.library_id when the URL lacks it. libraries is read-only discovery on the specified server, not network scanning. Do not pass the browser's #library_id= URL.

Config defaults to ~/.config/calibre-catalog-read/config.json; override with --config or CALIBRE_CATALOG_CONFIG. Keys: with_library, library_id, username, password_env, reading_script (human-only legacy hint). Unknown keys fail. No implicit .env loading or credential persistence. Credentials come from the existing environment; --password-env names the password variable. Raw --password is rejected. Passwords never enter child argv or diagnostics. Non-SSL server authentication is handled by Calibre (Digest); do not invent auth-mode/auth-scheme flags.

Local library directories must already contain metadata.db. Explicit endpoints never fail over to DNS/WSL/Docker/localhost guesses. Never start calibre-server from chat.

## One-book analysis: prepare first, complete offline

Do this only for an explicit reading/analysis request. Catalog lookup alone does not authorize metadata changes, bulk extraction, OCR, or sending a book to a new external service.

1. Choose a unique logical RUN_ID (letters/digits/._-, starting with an alphanumeric). Export and extract first:

       python3 "{baseDir}/scripts/run_analysis_pipeline.py" prepare \
         --book-id 3 --run-id RUN_ID --lang ja --format EPUB

   EPUB/PDF are supported; ebook-convert is used first, pdftotext is the optional PDF fallback. --cache-dir overrides the user cache root. prepare_subagent_input.mjs is an equivalent preparation entrypoint, not a raw-text shortcut.

   Completion criterion: status=prepared with prepared_input and input_sha256. On skipped/excluded_content or low_text_requires_confirmation, stop; do not spawn analysis or claim success. --force-low-text requires the user's explicit acceptance of incomplete extraction and a fresh run ID. Empty extraction always stops. Comic-tagged books are excluded from this text workflow.

2. Register the prepared manifest before delegation:

       node "{baseDir}/scripts/run_state.mjs" upsert \
         --run-id RUN_ID --input-json /absolute/run/subagent_input.json

   The record binds the manifest bytes and target. Do not replace/reuse a failed or completed run ID. Optional --state selects a separate state file.

3. Use references/subagent-analysis.prompt.md and both JSON schemas. The analysis worker reads the prepared parts and emits only analysis JSON. Use the currently available isolated worker/tool schema; no fixed agent ID, model, two-turn rule, or assumed completion mode. Keep the runtime handle and follow its accepted wait/collection contract. Main owns user responses and every metadata-write decision.

4. Validate and produce a local proposal:

       node "{baseDir}/scripts/handle_completion.mjs" --run-id RUN_ID \
         --analysis-json /absolute/analysis.json --proposal-jsonl /absolute/NEW-proposal.jsonl

   Completion criterion: status=proposal_created and an existing JSONL proposal. Completion is offline: no re-export, network lookup, or metadata write. Missing/duplicate runs do no work; failed/corrupt state remains for inspection. An existing lock requires checking live work before manual recovery, never automatic lock deletion.

5. Present the analysis, source identity, and full/partial coverage honestly. Coverage validates reported parts against prepared files/hashes/counts; it does not prove that a model understood the text. Preserve partial coverage in user-facing output. If the user also wants comments/tags updated, route the generated proposal through calibre-metadata-apply and its plan/apply gates; never apply it from this skill.

## Data and migration

- User state: CALIBRE_CATALOG_STATE_DIR, else XDG_STATE_HOME/calibre-catalog-read or ~/.local/state/calibre-catalog-read.
- User cache: CALIBRE_CATALOG_CACHE_DIR, else XDG_CACHE_HOME/calibre-catalog-read or ~/.cache/calibre-catalog-read.
- Exported originals, extracted text, parts, plans, and summaries are private. Keep them outside the skill package; do not publish or automatically delete them.
- Legacy package/state, old run formats, and old SQLite caches are not automatically migrated. Re-prepare active legacy work under a new run/state path; preserve originals. analysis_db.py is an optional local index, never completion authority. See README.md for test/migration details.
- Python >=3.11 is needed for analysis/cache helpers; Node >=20 and calibredb suffice for catalog lookup. No uv/network dependency install is required.

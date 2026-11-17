---
name: calibre-metadata-apply
description: "Edit explicitly selected Calibre metadata using a saved dry-run plan, stale-target checks, apply receipts, and readback verification. Use for title/authors/sort/series/tags/date/language/comments edits, not viewing an ID."
metadata: {"openclaw":{"requires":{"bins":["node","calibredb"]},"optionalEnv":["CALIBRE_WITH_LIBRARY","CALIBRE_LIBRARY_ID","CALIBRE_USERNAME","CALIBRE_PASSWORD"],"localWrites":["user state plans and apply receipts"],"modifiesRemoteData":["calibre:metadata"]}}
---

# Apply only the reviewed metadata change

1. Resolve this skill's absolute directory as {baseDir}. Use calibre-catalog-read to identify the exact library, IDs, titles, authors, and series. "Show/check ID" alone routes to that read-only skill.
2. Establish authorized scope. An explicit request specifying exact IDs and values can already authorize that change; do not demand repeated ceremonial confirmation. Ambiguous matches or evidence-derived proposals require presenting every candidate, uncertainty, target, and before/after field for approval. Never treat high confidence or a child's completion as permission to write.
3. Build JSONL (one object per book), then dry-run all rows. The wrapper rejects the entire input before mutation on invalid rows, duplicate IDs, unsupported fields/types, conflicting comments, or malformed markers.

       node "{baseDir}/scripts/calibredb_apply.mjs" \
         --plan-file /absolute/NEW-plan.json < /absolute/changes.jsonl

   Completion criterion: mode=dry-run, a saved plan_file/plan_digest, and before/after values for every row. Do not execute the displayed diagnostic command; the wrapper owns apply.

4. Present/confirm the exact plan when not already authorized. Apply that saved plan, with no JSONL on stdin:

       node "{baseDir}/scripts/calibredb_apply.mjs" \
         --apply --plan-file /absolute/plan.json < /dev/null

   Completion criterion: ok=true and verified per-row applied/no-op results. Inspect receipt_file. Exit-zero from set_metadata alone is never proof of success. Failures, stale values, or readback mismatches stop further writes and preserve reconciliation records.

5. Report actual changed/no-op/skipped/stale/failed/unverifiable IDs and before/after values. Never turn partial success into full success. For a failed/uncertain attempt, inspect the receipt and re-read actual values before making a new plan. Never blindly retry, delete receipts/locks, or claim automatic rollback.

## Fields and semantics

Direct: title, title_sort, authors, author_sort, series, series_index, tags, publisher, pubdate, languages, comments.

- title/authors cannot be empty. Authors arrays preserve name commas; do not join authors with commas. A literal & or | inside one name is rejected before mutation: Calibre's field parser cannot represent it safely. Do not silently split or substitute the name.
- title_sort/author_sort are explicit values. Use the workspace's configured Japanese reading script as a human proposal preference, not executable code. Do not invent readings. Calibre may preserve an old sort when authors/title change; show and approve sort changes explicitly.
- pubdate uses YYYY-MM-DD and is sent with an explicit UTC timestamp to prevent date drift. Null/empty clears the date. languages accepts supported ISO639 codes; readback normalizes two/three-letter aliases. series_index is finite/nonnegative and requires a series.
- Tags merge by default. tags:[] is a no-op with that default. Use tags_merge:false for replacement/clear, or tags_remove for explicit removals. Other omitted fields remain untouched. Null/empty clears optional string fields; series_index is not nullable.
- comments replaces the full comment only when explicitly requested. analysis produces escaped HTML and safely replaces one OC_ANALYSIS marker block while preserving other comments. comments_html accepts one explicit marker block; it is raw user-approved HTML, not automatically trusted child text. These three inputs are mutually exclusive.
- analysis may carry coverage. Keep full/partial counts in generated comments. Catalog proposals also carry expected_library/expected_uuid; retain them so the dry-run rejects cross-library/book confusion.

Input examples: references/changes.example.md. Copy only the fenced JSONL rows into your changes file. Treat examples as proposals, never as pre-approved IDs.

## Endpoint, credentials, and persistence

Read local connection facts from workspace AGENTS.md Tools. Endpoint precedence: --with-library, the CALIBRE_WITH_LIBRARY / CALIBRE_LIBRARY_URL / CALIBRE_CONTENT_SERVER_URL variables, then config.with_library. A server URL needs #LIBRARY_ID (or --library-id / CALIBRE_LIBRARY_ID / config.library_id). Local libraries must already contain metadata.db. There is no host autodiscovery/failover or server start.

Config: ~/.config/calibre-metadata-apply/config.json, or --config. Allowed keys: with_library, library_id, username, password_env, state_dir, reading_script (human-only legacy preference). No implicit .env loading. Unknown options fail rather than pretending to work. Legacy --save-auth/--save-plain-password/--server-hosts/auth-mode flags are removed.

Use the existing credential environment and --password-env (default CALIBRE_PASSWORD). The wrapper sends the secret through Calibre's documented <stdin> mechanism, never in argv, plans, or diagnostics. Never pass raw --password.

State root: --state-dir, CALIBRE_METADATA_APPLY_STATE_DIR, config.state_dir, XDG_STATE_HOME/calibre-metadata-apply, or ~/.local/state/calibre-metadata-apply. Plans are no-clobber files; attempts are fsynced intent/result JSONL receipts. One attempt per plan digest, with a per-library local apply lock. A plan digest detects accidental edits; it is not human authorization, server identity certification, or server-side CAS. Other clients can still race the final read/write window.

## Delegated evidence / unknown documents

Keep main responsible for target selection, synthesis, review, and all writes. Delegate only independent evidence/proposal generation using the live tool schema and accepted completion mode; never assume a fixed calibre-reader profile. Child results are proposals, not permission to write.

For unknown books, start with existing metadata and show all rows. Escalate to first-page or first/last-five-page inspection only when requested, then add attributable web evidence if needed. Preserve uncertainty and conflicting candidates. pending-review tags are also metadata changes and need authorized scope. Never infer permission for bulk extraction or new external disclosure.

Optional run helpers bind completion to run_id and do not apply metadata. A result object must have matching run_id, ok:boolean, and status:proposal_ready|completed|failed. See README.md for examples, recovery limits, and regression commands.

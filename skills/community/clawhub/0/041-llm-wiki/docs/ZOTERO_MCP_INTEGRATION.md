# Zotero MCP Operating Protocol

> Canonical Agent instructions for every Zotero operation in llm-wiki.
>
> **Required integration:** [`54yyyu/zotero-mcp`](https://github.com/54yyyu/zotero-mcp)
>
> **Upstream compatibility last reviewed:** 2026-08-26 against Zotero 10 (desktop) and zotero-mcp v0.11.0. The tools actually exposed by the connected MCP server take precedence over examples in this document.

## Scope and Authority

Zotero is the literature layer; llm-wiki is the distilled Markdown knowledge layer. Zotero owns bibliographic metadata, attachments, annotations, collections, tags, citation keys, and other library state. llm-wiki owns reusable concepts, cross-source synthesis, wiki links, temporal interpretation, and indexes.

This document is the single operational source of truth for Zotero work. `SKILL.md`, `AGENTS.md`, and the README files should state the integration boundary and point here instead of duplicating workflows.

## Zotero 10 and zotero-mcp v0.11.x Compatibility

Reviewed 2026-08-26. Zotero 10 (desktop, released 2026-08-17) is mostly a UX release. It did **not** change the Web API schema, DOI/arXiv handling, or the MCP tool surface llm-wiki depends on. The four MCP tools llm-wiki calls directly (`zotero_get_collection_items`, `zotero_get_item_metadata`, `zotero_batch_update`, `zotero_update_item`) are unchanged across zotero-mcp v0.9.1 → v0.11.0, so no llm-wiki code change is required to keep working.

**Local API writes — desktop capability exists; zotero-mcp has not adopted it; llm-wiki adds a temporary direct path (most important):**

- Zotero 10 added **Local API write support** at the desktop level.
- The integrated zotero-mcp (≤ v0.11.0) **still routes its own writes through the Zotero Web API**; local mode remains **read-only for writes** ("fast local reads, web API writes"). This is unchanged.
- Consequence for the MCP path: `metadata_write_backend = local` is **not reachable through zotero-mcp** today; the MCP metadata write gate and the hybrid-mode warning below still stand for anything written via zotero-mcp.
- **Temporary opt-in exception:** llm-wiki now offers a direct local write path that bypasses zotero-mcp only for the exact authorized targets. Collection discovery, snapshots, sources, and bibliographic reads still go through MCP; direct local GETs are permitted only as precondition and post-write verification barriers for those targets. One-time `agent-bridge.py zotero-local-auth` stores a reusable key under gitignored `var/zotero-local.json`; then either `zotero-refresh --apply-safe --write-backend local` or the restricted reviewed `zotero-writeback` workflow writes via the local API. `zotero-writeback --memory-authorize` can instead keep a one-run key only in process memory. See "Temporary Direct Local Writes" below. **Remove this exception once zotero-mcp adopts local writes.**
- To detect upstream adoption: after any zotero-mcp upgrade, confirm which backend a write actually lands on (the sentinel-tag probe in the Backend Consistency Gate) before treating the MCP `local` route as a write backend.
- **Empirically verified 2026-08-27** (zotero-mcp v0.11.0 against Zotero 10, hybrid config): in pure-local mode (no `ZOTERO_API_KEY` in the server process env) a `zotero_batch_update` write returned success yet did **not** change local state — it was routed to the Web backend. Two corollaries were observed: (1) zotero-mcp also loads Web credentials from the `client_env` block of `~/.config/zotero-mcp/config.json` when the process environment does not provide them, so "no key in the client env" does **not** guarantee a write stays local or fails; (2) a write returning success is **not** evidence that local state changed — always re-read the intended backend to confirm where a write landed.

**Other Zotero 10 behavior changes that affect Agent workflows:**

- **Search semantics changed.** Quick/full-text search is now accent- and typography-insensitive by default (`cafe` matches `café`), and unquoted CJK matches **full phrases** instead of individual characters. Do not reuse pre-Zotero-10 recall/precision expectations; quote terms when you need literal or token-level matching. Advanced search gained nested condition groups and new conditions (Annotation Color, # of Notes, "is empty / is not empty"); whether these are reachable depends on the connected server's `zotero_advanced_search`.
- **Full-text content sync.** Zotero 10's "Sync full-text content" setting can index and search attachment content synced from another machine **without the file existing locally**. `indexed_fulltext_only` may therefore be reachable even when bytes were never on this machine — it is still not evidence of a local file.
- **Backups and schema.** Zotero 10 dropped automatic versioned database backups, forces one regular backup before each database upgrade, and added automatic compaction. Do not rely on a `zotero.sqlite.bak` existing; let Zotero's own upgrade backup run, and keep `zotero.sqlite` out of generic cloud-sync folders as already required below.
- **Credentials in the OS keychain.** Zotero 10 stores API keys and WebDAV passwords in the OS keychain. This does not change the rule against printing, committing, or copying credentials.

**zotero-mcp v0.11.0 change to note:**

- `zotero_semantic_search` now defaults to the **active library only**; pass `search_all_libraries=True` for the old cross-library behavior. Adjust semantic-discovery expectations accordingly.

## Temporary Direct Local Writes (Zotero 10)

> **Temporary, opt-in boundary relaxation.** Writes may go directly to the Zotero 10 local API while reads still go through zotero-mcp. This is the documented exception to the "Required Tool Boundary" below. Remove it once zotero-mcp adopts local writes.

**When to use:** you want writes to land in the local Zotero library immediately (no Web round-trip, no sync barrier), and the connected MCP read backend is local/hybrid so the write is visible to MCP reads at once.

**Setup (one-time, interactive):**

```bash
<PY> scripts/agent-bridge.py zotero-local-auth
```

This runs the Zotero 10 local-write handshake: read `Zotero-Server-ID` from `GET /api/`, then `POST /api/local/authorize`. **Approve the dialog in Zotero Desktop; choose "Always Allow" for a reusable key.** The key is stored at gitignored `var/zotero-local.json` (mode 0600) and never printed or logged. The default local API base URL is `http://127.0.0.1:23119`; override it via `zotero_enrichment.local.base_url` in `config.yaml`.

**Applying writes locally:**

```bash
<PY> scripts/agent-bridge.py zotero-refresh --collection-key A9VNJUPI --apply-safe --write-backend local
```

- `--write-backend` defaults to `web` (writes via zotero-mcp, unchanged); `local` routes only the writes to the local API.
- Every local write does read-version → `If-Unmodified-Since-Version` optimistic-concurrency PATCH.
- The existing verify-after-write loop still re-reads each item and confirms the mutation landed; it reads through MCP, which in a hybrid setup reads the local database, so a local write is verified immediately.

**Safety and limits:**

- Writes stay minimal and reviewed: the `--apply-safe` scope (Extra `LLM-Wiki ...` keys, `llm-wiki:*` status tags, conservative DOI URL normalization) is unchanged; `local` only changes *where* those same safe writes land.
- The local key is not scoped by Zotero — it can write any editable library. Guard it like the Web key.
- The local API requires Zotero Desktop running with "Allow other applications on this computer to communicate with Zotero" enabled.
- If the key is missing or expired, `zotero-refresh --write-backend local` fails closed and tells you to re-run `zotero-local-auth`.

## Controlled Attachment Relocation

`zotero-relocate` is a separate, opt-in exception for the narrow case in which llm-wiki must move a local attachment and update its Zotero linked-file path. It is not a general Zotero client and does not replace the MCP discovery/read boundary.

Before enabling apply against a user library:

- Run the Phase 0 isolated-library spike described in `docs/ZOTERO_ATTACHMENT_RELOCATION.md` and confirm that Zotero can update the existing attachment item in place while preserving its item key, parent, child items, and annotations.
- Use only the command's `zotero-relocate` capability contract. Its filesystem writes are limited to the configured managed attachment root, the private `sources/zotero/` binding/alias layer, and explicitly allowed source roots for cleanup.
- Use the current Zotero attachment key as the stable identity. Do not clone/delete items or rewrite notes when the backend cannot prove equivalent preservation.
- Re-read the attachment after every accepted PATCH and update `metadata.yaml` only after the Zotero path is verified. A Web API success response or a stale metadata path is not sufficient.
- Keep `zotero_relocation.enabled` false until the user has reviewed the dry-run report. `--delete-source` is opt-in and remains bounded by `allowed_source_roots` and reference checks.
- Configure the managed attachment root once in `config.yaml` under `zotero_relocation.root`; `config.yaml` is gitignored, so each machine keeps its own value, and the `--root` flag is only a one-off override. For cross-device sync, point `root` at a cloud-synced folder and use environment-variable interpolation to keep the path portable (for example `root: "${OneDrive}/zotero-attachments"`). When devices run different operating systems (for example Windows and Linux), no absolute path can work everywhere: set `zotero_relocation.base_dir_relative: true` so the written-back path is the portable `attachments:<relative>` form, and point Zotero's Linked Attachment Base Directory at the synced root on each device.
- Treat stored-to-linked conversion as a sync-impacting operation: Zotero File Sync may no longer manage the file bytes, and other machines may not have access to the configured external root. When the root is a cloud-synced folder, confirm every device can reach that same synced root before applying.
- **Empirical Phase 0 result (2026-08-29):** the Zotero 10 local API rejects imported→linked conversion — PATCHing `{linkMode: "linked_file", path: ...}` returns HTTP 500 but partially applies, leaving items in an inconsistent state (`linked_file` with a stale `storage:` pseudo-path, cleared `filename`, zeroed `version`). Reverting `linkMode`/`filename` via PATCH is verified to work, and linked→linked path-only updates (including the portable `attachments:` form) are verified to work. Perform imported→linked conversion with Zotero's native *Convert Stored Files to Linked Files* (or ZotMoov) instead; `zotero-relocate` writes are only for attachments that are already linked files.

The workflow is implemented by `scripts/agent-bridge.py zotero-relocate`; its design, state machine, failure recovery, and unresolved API questions are documented in `docs/ZOTERO_ATTACHMENT_RELOCATION.md`.

## Required Tool Boundary

All Zotero discovery, reads, source access, metadata identity work, semantic-index maintenance, and normal writes performed by this skill **MUST go through the MCP tools exposed by [`54yyyu/zotero-mcp`](https://github.com/54yyyu/zotero-mcp)**. Direct local writes are permitted only by the narrowly defined temporary exception below.

Agents must not substitute:

- another Zotero skill or MCP server;
- a native llm-wiki Zotero client;
- direct Zotero SQLite access;
- direct Zotero Web API calls;
- ad hoc scripts that bypass `zotero-mcp`.

The `zotero-mcp` CLI may be used for installation, upgrades, setup, and diagnostics. Zotero library reads, writes, and semantic-index maintenance should use the connected MCP tool surface. Use a CLI maintenance command only when the required MCP maintenance tool is unavailable and the user has approved that fallback. Installing, updating, or reconfiguring `zotero-mcp` requires user confirmation under the normal dependency and external-service rules.

**Temporary exception:** direct writes to the Zotero 10 *local* API are permitted only through the reviewed `zotero-refresh --write-backend local` path, the restricted `zotero-writeback` authorized-plan path, or the separately gated `zotero-relocate` attachment path described in this document. All discovery, source access, collection reads, and bibliographic identity work still go through zotero-mcp.

## Compatibility and Capability Gate

Before every Zotero task:

1. Verify that the configured MCP integration is intended to be an installation of `54yyyu/zotero-mcp` and that its Zotero tools are exposed in the current Agent session. If the host does not expose package provenance, verify the expected capability surface and state that repository provenance could not be independently confirmed.
2. Verify access to the intended Zotero library. Discover libraries before switching; do not guess a library ID or type.
3. For read-only work, verify the specific path needed by the task, such as collection search, item metadata, annotations, attachment paths, or full text.
4. For write work, verify the exact write tool and authorization before changing anything. Note creation/update, incremental tag updates, item metadata changes, collection membership changes, attachment uploads, annotations, related-item operations, and attachment path relocation are separate capability gates.
5. Use only capabilities actually exposed by the connected `zotero-mcp` instance. Do not infer a tool exists from this document, an old example, or another installation.
6. When observable, distinguish whether a capability is not installed, not exposed by the configured toolsets, not configured, unavailable in the active access mode, or unauthorized.

| Workflow | Required capability | If unavailable |
| --- | --- | --- |
| Metadata search | Search and item-metadata tools | Stop Zotero discovery and report the blocker |
| Semantic discovery | Semantic-search tools and a ready search database | Fall back to metadata, tag, or collection search |
| Local source alias | A readable local attachment path | Ingest through verified MCP content without creating an alias |
| PDF outline/page/layout work | The relevant PDF tools and optional dependencies | Use annotations or full text when sufficient; otherwise report the limitation |
| Related-item synchronization | Relation tools exposed by the configured toolsets plus write access | Preserve the reviewed relationship only in the wiki |
| Any Zotero write | A write-capable access mode and the exact write tool | Stop Zotero-side writes and continue only with useful wiki-local work |

If `zotero-mcp` is missing, unreachable, unauthorized, connected to the wrong library, or lacks the required tool:

- stop the affected Zotero-side operation;
- state the exact blocker and failed capability gate;
- do not fall back to another Zotero integration or direct API/database access;
- continue only with useful wiki-local work that does not require that Zotero capability.

## Access Mode, Authority, and Synchronization State

Treat Zotero as two related but distinct planes: **metadata state** and **attachment-file state**. Before any Zotero write or file-backed ingest, determine both planes instead of relying on a label such as "hybrid mode":

```text
metadata_authority     = local | web
metadata_read_backend  = local | web
metadata_write_backend = local | web | unavailable
metadata_sync_state    = disabled | pending | caught_up | divergent | unknown

attachment_authority   = local_machine | zotero_file_sync | webdav | linked_external | unknown
attachment_access      = local_path | local_api_stream | remote_download | indexed_fulltext_only | unavailable
```

- **Metadata authority** is the item/collection/tag state the user considers canonical.
- **Metadata read backend** is where the current MCP tool obtains the state used to make a decision.
- **Metadata write backend** is where the mutation is actually applied.
- **Metadata sync state** describes whether the authority and the write backend are known to agree.
- **Attachment authority** identifies where the actual file bytes are expected to exist.
- **Attachment access** describes what the current MCP session can actually retrieve. It is a capability statement, not an existence statement.

Use the following metadata write gate:

| Authority | Read backend | Write backend | Sync state | Decision |
| --- | --- | --- | --- | --- |
| Web | Web | Web | Any | Writes may proceed after the normal capability gate |
| Local | Local or Web | Web | `caught_up` | Writes may proceed, but completion requires a synchronization barrier |
| Local | Any | Web | `disabled` or `pending` | A successful Web write is cloud-pending, not locally complete; do not start broad writes while synchronization is pending |
| Local | Any | Web | `divergent` or `unknown` | Stop writes and reconcile or re-audit first |
| Any | Any | `unavailable` | Read-only work only |

Do not infer backend consistency from configuration values alone. A valid API key, an exposed write tool, or a successful single-item write proves only that one route is writable; it does not prove that local and Web state agree.

> **Note on `metadata_write_backend = local`:** not reachable *through zotero-mcp* — v0.11.0 routes its writes through the Web API even against Zotero 10. The `local` write backend is reachable only via the temporary direct local paths (`zotero-refresh --write-backend local`, reviewed `zotero-writeback`, or reviewed `zotero-relocate`); the gate's Web-backend rows still govern anything written through zotero-mcp. See "Temporary Direct Local Writes".

### Backend Consistency Gate

For a write task, perform the following checks when the relevant state is observable:

1. Discover the active library and resolve the intended collection in that library.
2. Read a known item and inspect its tags and `Collections` field.
3. Compare the observed state with the user-designated authority. A collection visible only on one backend is evidence of divergence, not a missing user object.
4. When write authorization is uncertain, use a unique temporary sentinel tag on one approved low-risk item: add it, read it from the write backend, remove it, and verify removal.
5. Treat the sentinel as a narrow authorization test. It does not validate batch-version behavior, synchronization, overlapping writes, or local visibility.
6. After changing MCP configuration, rotating credentials, switching libraries or modes, restarting Zotero/Codex/MCP, or enabling synchronization, rerun this gate.

> **Hybrid-mode warning:** a connected server may read tags from local Zotero while routing writes through the Web API. If those states differ, a read-modify-write implementation can send an outdated complete tag set to Web and overwrite a preceding batch. Do not perform overlapping writes to the same items across inconsistent backends.

## Setup Reference

The upstream project currently supports local, web, and hybrid access modes. Follow its current setup documentation rather than copying environment-specific configuration into llm-wiki.

Typical upstream setup commands are:

```bash
uv tool install zotero-mcp-server
zotero-mcp setup
```

Local read workflows require Zotero Desktop with its local API enabled. Write workflows generally require Zotero Web API credentials or another write-capable mode supported by the connected server. Never print, commit, or copy Zotero API keys or other credentials into project files.

### Configuration Ownership

Do not assume that `~/.config/zotero-mcp/config.json` controls the active MCP access mode. That file primarily stores semantic-search, database-path, extraction, and index-update settings. Local/Web mode and Web credentials are normally supplied by the MCP client's process environment. However, zotero-mcp v0.11.0 was observed to **also load Web credentials from that file's `client_env` block** when the process environment does not provide them — so treat the file as a potential credential source, and do not assume that "no `ZOTERO_API_KEY` in the client process env" means a write will stay local or fail.

For Codex, inspect the configured server entry in `~/.codex/config.toml` (or the equivalent host-managed MCP configuration). A hybrid configuration keeps local access enabled while retaining Web credentials for write-capable operations:

```toml
[mcp_servers.zotero-mcp]
command = "zotero-mcp"

[mcp_servers.zotero-mcp.env]
ZOTERO_LOCAL = "true"
ZOTERO_DB_PATH = "<absolute path to the active zotero.sqlite>"
ZOTERO_API_KEY = "<secret provided only in local MCP configuration>"
ZOTERO_LIBRARY_ID = "<user or group library ID>"
ZOTERO_LIBRARY_TYPE = "user"
ZOTERO_EMBEDDING_MODEL = "default"
```

A minimal semantic configuration can omit runtime-generated fields such as last-update timestamps and sync versions:

```json
{
  "semantic_search": {
    "zotero_db_path": "<absolute path to the active zotero.sqlite>",
    "embedding_model": "default",
    "update_config": {
      "auto_update": true,
      "update_frequency": "startup",
      "update_days": 7
    },
    "extraction": {
      "pdf_max_pages": 10
    }
  }
}
```

The same machine can contain configuration for several MCP clients. `zotero-mcp setup-info` may describe a Claude Desktop entry while Codex launches the server with different environment values. Treat the environment of the client that started the current MCP process as authoritative. After changing it, restart that client/MCP process and rerun the backend-consistency gate.

A practical post-restart smoke test should verify each required route independently: discover the library, read one known item, resolve one known local attachment path, exercise the exact PDF endpoint needed by the task, and—only when writes are authorized—add/read/remove/read a unique sentinel tag. Passing one route does not imply that the others are available.

### Data Sync, File Sync, and Local Authority

Zotero data synchronization and attachment-file synchronization are separate concerns. Zotero Data Sync covers bibliographic items, collections, tags, and notes; file synchronization covers stored attachment files. A user may enable Data Sync while leaving Zotero File Sync disabled. See the official [Zotero Sync documentation](https://www.zotero.org/support/sync) for current behavior.

For a local-authoritative workflow in which MCP writes through the Web API:

1. Keep the Zotero Desktop library as the declared authority.
2. Enable Zotero Data Sync so metadata writes can return to Desktop.
3. File Sync may remain disabled when the user does not want Zotero-hosted attachment storage.
4. Treat Web writes as pending until synchronization completes and the post-sync audit passes.
5. Do not issue additional broad writes while the first synchronization or a conflict merge is still in progress.

Follow the official [Zotero data-directory guidance](https://www.zotero.org/support/zotero_data) and do not place the active Zotero data directory or `zotero.sqlite` in OneDrive, Dropbox, or another generic file-sync directory. Those tools operate at the file level and may copy a live database in an inconsistent state. If cloud storage is used for attachments, prefer a deliberately configured linked-attachment directory while keeping the Zotero database in a normal local data directory. Agents may diagnose paths read-only, but must not automatically relocate a live database or invoke destructive synchronization reset options.

If local and Web libraries have already diverged, stop mutations, back up the local authority, let the user choose the reconciliation direction in Zotero, and re-audit all counts, keys, tags, and memberships after synchronization.

### Attachment Existence vs. Path Resolution

Attachment metadata and attachment file bytes can have different availability. Zotero Data Sync may synchronize an attachment item, filename, and parent relationship without synchronizing the file bytes. Conversely, a file may exist in the current machine's Zotero storage while a Web-only MCP session cannot return its local path.

Interpret attachment errors narrowly:

- `zotero_get_attachment_path requires local mode` means the current MCP mode cannot resolve local filesystem paths. It does **not** prove that the file is absent from the machine.
- A Web API file `404` may mean Zotero File Sync is disabled or the bytes were never uploaded. It does **not** prove that the corresponding local stored or linked file is absent.
- `indexed_fulltext_only` means text can be read through Zotero's full-text index even though the original file path or bytes are not available through the current tool route.
- A successfully resolved local path proves path resolution for that attachment only. It does not prove that optional PDF features are installed. For example, selected-page reading may work while outline or layout extraction fails because the corresponding PDF extra is unavailable; test the exact endpoint required by the task.

For a synchronized metadata / local-file workflow, prefer this responsibility split:

1. Resolve item, collection, tags, attachment key, filename, and bibliographic provenance from the declared metadata authority. Web metadata is a reasonable operational authority only when Data Sync is enabled, caught up, and the user has selected it as authoritative.
2. Resolve actual source bytes from the machine where they are stored, using a local- or hybrid-mode Zotero MCP capability. Do not assume Zotero File Sync is enabled.
3. Join metadata and file identity by stable item/attachment keys plus filename or content identity; do not join by title alone.
4. If the current MCP is Web-only but the user reports a local file, record `local-path capability unavailable in current mode` and reconfigure/restart Zotero MCP with approval before materializing an alias. Do not silently scan Zotero storage or bypass MCP.
5. Re-run the capability gate after changing `ZOTERO_LOCAL` or switching between local, Web, and hybrid access.

## Tool Selection

Prefer the narrowest exposed MCP tool that satisfies the request:

- **Discovery:** item search, advanced field search, tag search, recent items, or semantic search.
- **Library navigation:** list/switch libraries, search collections, list collection items, and list tags.
- **Metadata and citations:** item metadata, citation-key lookup, and Zotero-rendered bibliography/BibTeX export.
- **Content reading:** item children, attachment paths, PDF outline, selected PDF pages, annotations, notes, and full text.
- **Writes:** add items, update item metadata, incrementally update tags, change collection membership, manage notes, attach files, and create/update annotations.
- **Semantic index:** inspect database status before semantic search; refresh it after adding or materially changing indexed items.

Use metadata and targeted reads before full-text extraction. Full text is resource-intensive and should be read only when the user requests paper-level analysis or metadata, abstracts, annotations, outlines, and selected pages are insufficient.

For deterministic local planning, Agents may export a minimal, verified MCP snapshot to an ignored temporary path and run:

```bash
<PY> scripts/agent-bridge.py zotero-plan --snapshot temp/zotero-snapshot.yaml \
  --manifest-out temp/zotero-mutation-manifest.yaml
```

`zotero-plan` is read-only. It does not connect to Zotero or external metadata providers and does not modify wiki files. It compares the snapshot with wiki `sources_meta`, reports desired llm-wiki-managed tags, collection-equivalent tag removal candidates, DOI audit state, and preprint publication checks. Zotero MCP remains the default read/write route. When `--manifest-out` is provided, the resolved path must remain under the project `temp/` directory. The generated YAML declares `mode: review-only`; it is not executable. `remove_tags_review`, metadata changes, and relation candidates still require explicit Agent/user review. Only approved managed-tag additions and reviewed relation pairs may be copied into the separate restricted `mode: authorized-write` schema described below.

## One-Shot Metadata Refresh

Use the project-managed worker when a collection needs provider freshness checks:

```bash
<PY> scripts/agent-bridge.py zotero-refresh --collection-key A9VNJUPI \
  --manifest-out temp/zotero-refresh.yaml
```

The command starts the configured `54yyyu/zotero-mcp` server through the MCP Python SDK; it is not a direct Zotero Web API or SQLite client. It reads item metadata through MCP, queries Crossref for DOI identity and publication candidates, queries OpenAlex for citation counts and open source-level metrics, and keeps only the latest provider cache under ignored `var/zotero-enrichment.sqlite`. Crossref requests are serialized and retried with bounded backoff.

The default is dry-run. After reviewing the manifest, `--apply-safe` may only:

- upsert namespaced `LLM-Wiki ...` lines in Extra;
- add or remove `llm-wiki:*` status tags;
- normalize an empty URL or an already-DOI URL that conflicts with a verified existing DOI;
- re-read every modified item and fail if the expected Extra keys, tags, or fields are not present.

It must not automatically add a newly discovered DOI, overwrite creators/title/venue/date, migrate item type, merge a preprint, modify attachments/notes/collections/citation keys, or write Zotero Related links. These remain in `metadata_review` until an Agent and user approve the bibliographic identity change. Cache paths must remain below project `var/`; manifests must remain below project `temp/`.

## Restricted Zotero 10 Local Write-Back (Temporary Exception)

Use this path only after the user explicitly authorizes local Zotero writes and the Agent has reviewed every target. Discovery, collection snapshots, source reads, attachments, and bibliographic identity checks still go through `54yyyu/zotero-mcp`; the exception is limited to loopback PATCH operations that the connected MCP cannot currently express.

1. Copy only approved managed-tag additions and reviewed Related pairs into a secret-free plan based on [`docs/examples/zotero-write-plan.example.yaml`](examples/zotero-write-plan.example.yaml).
2. Keep the real plan and all reports under ignored `temp/`.
3. Run audit first:

```bash
<PY> scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action audit --report-out temp/zotero-write-audit.yaml
```

4. Apply with either the reusable private `var/zotero-local.json` authorization or a process-memory-only key:

```bash
<PY> scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action apply --memory-authorize --report-out temp/zotero-write-report.yaml
```

5. Run a separate final verify phase after any synchronization or user edit that may invalidate earlier observations:

```bash
<PY> scripts/agent-bridge.py zotero-writeback --plan temp/zotero-write-plan.yaml \
  --action verify --report-out temp/zotero-write-verify.yaml
```

The executable schema is fail-closed:

- `mode` must be `authorized-write`; review-only manifests are rejected.
- credential-like fields are rejected; API keys never belong in plans or reports.
- every desired tag must start with `llm-wiki:`.
- existing tag objects, including automatic/manual tag metadata, are preserved.
- tag replacement, metadata edits, collection changes, notes, attachments, citation keys, and Trash are forbidden.
- scoped tag removal is a separate opt-in: it requires `policy.allow_managed_removals: true` and an explicit per-item `reviewed_removals` list, and even then only managed `llm-wiki:` tags may be removed — never the protected `llm-wiki:ingested` status tag, never preserved tags (e.g. `llm-wiki:index-card`), never unmanaged/user tags, and never a tag also listed in the item's `desired_managed_tags`. Generate a whitelisted removal plan with `zotero-plan --removal-plan-out`, which proposes only retired `llm-wiki:<page_stem>` binding tags (excluding any tag that is still a live topic projection of a binding).
- relation targets must be present in the plan and are added only as reviewed reciprocal `dc:relation` pairs.
- writes use the live `Zotero-Server-ID`, `If-Unmodified-Since-Version`, one bounded retry after HTTP 412, and a mandatory GET-after-PATCH verification barrier.
- reports classify items as `updated_verified`, `skipped_current`, or `failed`; partial failures remain visible and are never silently broadened.

## Collection Ingest Verification

For a batch ingest, create a complete allocation ledger based on [`docs/examples/zotero-ingest-allocation.example.yaml`](examples/zotero-ingest-allocation.example.yaml), then run:

```bash
<PY> scripts/agent-bridge.py zotero-ingest-verify \
  --snapshot temp/zotero-snapshot.yaml \
  --allocation temp/zotero-allocation.yaml \
  --report-out temp/zotero-ingest-report.yaml
```

The verifier requires exact snapshot/allocation count and item-key coverage, unique 1-based item indices, a concrete reason for every omission, and at least one page for every non-omitted item. Each allocated page must exist and bind the item exactly once in `sources_meta.zotero_item_key`. It also checks UTF-8/YAML/frontmatter readability, duplicate provenance rows, H1/definition/knowledge/Related Pages/Sources/Changelog invariants, control characters, trailing whitespace, and machine-specific private paths. Three or more pages with identical headings and near-identical knowledge depth produce a template-collapse warning for Agent review, not an automatic failure.

## Read Workflows

### Find and Inspect One Item

1. Resolve the target by Zotero item key, Better BibTeX citation key, DOI, title/creator/year, or another stable identifier.
2. Read item metadata first.
3. Inspect child attachments and notes when needed.
4. Prefer annotations, PDF outline, and selected page ranges before requesting the entire attachment text.
5. Confirm that title, creators, DOI/arXiv ID, and attachment identity match the requested source before ingest.

### Explore a Collection, Tag, or Topic

1. Discover the active library and resolve the collection or tag without guessing identifiers.
2. Record the collection key, backend, item count, and observation time; collection snapshots become stale after synchronization or user edits.
3. Produce a candidate list containing title, creators, date, item type, Zotero item key, and citation key when available.
4. Treat collection searches as candidate discovery. Endpoint behavior around parent/child collections can vary by tool or version; do not infer direct membership solely because a title appears in a scoped search.
5. Before moving or removing membership, read each selected item's metadata and treat its explicit `Collections` field as the membership source of truth.
6. Use semantic search only as candidate discovery and only when its database is ready.
7. Select relevant items before reading full text; do not bulk-read an entire collection by default.
8. For batch ingest, group sources by reusable topic, mechanism, or historical phase instead of mechanically creating one wiki page per Zotero item.

### Query Across Wiki and Zotero

1. Search `wiki/index.md` and relevant wiki pages first for already distilled knowledge.
2. Use Zotero MCP when the question requires source coverage, recent library additions, a specific paper, annotations, notes, or missing literature.
3. Read the actual metadata/content behind selected Zotero results.
4. Synthesize the answer from wiki pages and verified Zotero material; Zotero search results alone are not the final answer.
5. Archive durable new synthesis into the wiki only according to user intent.


## Metadata Enrichment and Publication Tracking

Metadata enrichment is a reviewed evidence workflow, not an unconditional field refresh. Keep three states separate:

1. **Bibliographic identity:** title, creators, DOI, arXiv ID, item type, venue, publication date, volume, issue, and pages.
2. **Publication events:** preprint, accepted manuscript, conference version, journal extension, correction, retraction, and version of record.
3. **Dynamic metrics:** provider-specific citation counts and journal-level metrics observed at a particular time.

### Snapshot and Planning Contract

A collection audit starts from a minimal snapshot produced from actual Zotero MCP reads. Store it under ignored `temp/` or another approved private location, never in committed wiki pages or logs when it contains private library state:

```yaml
version: 1
library_id: "0"
collection:
  name: "GNN"
  key: "A9VNJUPI"
items:
  - item_key: "ABCD1234"
    title: "Paper Title"
    item_type: "conferencePaper"
    date: "2024"
    doi: "10.xxxx/example"  # include an empty value only after the DOI field was read
    arxiv: "2401.00001"
    url: "https://example.invalid/paper"
    tags:
      - "user-managed-tag"
    collections:
      - "A9VNJUPI"
```

Omitting `doi` means the DOI field was not observed and produces `unknown`; an explicit empty `doi` means the field was read and is missing. This prevents a lightweight collection listing from being misclassified as proof that no DOI exists. A DOI embedded in `url` is a candidate; disagreement between the DOI field and a DOI-bearing URL is a conflict requiring review.

### DOI Verification Gate

For `journalArticle`, `conferencePaper`, and `preprint` items:

1. Normalize an existing DOI and resolve it through an approved registry or metadata provider.
2. Compare normalized title, principal creators, publication year, venue, and item type.
3. Classify the result as `verified`, `candidate`, `conflict`, or `missing`.
4. Auto-write only a uniquely matched, high-confidence DOI whose returned identity agrees with the Zotero item.
5. Present ambiguous candidates and every item-type migration for review before writing.
6. Preserve the previous DOI/arXiv identity and verification provenance when promoting a preprint record.
7. Re-read the complete item after each write and verify tags, collections, creators, notes, attachments, citation key, and unrelated fields remain intact.

A DOI beginning with `10.48550/arXiv.` is a preprint DOI signal, not proof that no publisher DOI exists. Keep preprint and published identifiers distinct in working state. Prefer separate related items for materially distinct versions; migrate one item in place only after an explicit identity and field-loss review.

### Publication Event Policy

When a preprint later has a version of record:

- prefer finding or creating the published item without duplicating an existing DOI;
- preserve the preprint item, arXiv identifier, first-publication date, attachments, and annotations when they remain useful;
- record the event in wiki `source_events` when it changes historical interpretation;
- use a same-work Zotero relation only when the exposed relation tool and reviewed predicate semantics support it;
- do not convert semantic wiki adjacency into item-level relations.

### Dynamic Metric Provenance

Citation counts and journal metrics are snapshots, not stable bibliographic truth:

- always record provider, metric name, value, and `observed_at`;
- never overwrite one provider's count with another provider's count;
- keep volatile history out of ordinary wiki `updated` churn unless the trend itself is durable knowledge;
- store stable verification markers in incremental `Extra` keys and use a short child note or approved private state for metric history;
- treat Journal Impact Factor as a journal/edition metric, never as a paper-level or conference-level property;
- do not access licensed providers or configure API credentials without user authorization.

Recommended incremental `Extra` keys:

```text
LLM-Wiki DOI Verified: 2026-08-23
LLM-Wiki DOI Provider: Crossref
LLM-Wiki Citation Count [Crossref]: 123
LLM-Wiki Citation Checked: 2026-08-23
LLM-Wiki JIF [JCR 2026]: 8.4
```

Use stable keys so `zotero_batch_update(set_keys=...)` can upsert individual lines without replacing unrelated `Extra` content.

### Post-Ingest Zotero Synchronization

For a Zotero-backed source, optional synchronization occurs only after wiki coverage/depth review, link review, index update, and logging have completed:

1. Resolve every `sources_meta.zotero_item_key` and compute the union of desired managed state across all wiki pages that reference the item.
2. Add `llm-wiki:ingested` only when at least one active, coverage-verified ingest for that source has completed.
3. Add shared topic tags by projecting the bound wiki page's curated `tags:` (e.g. a page tagged `Ubuntu` produces `llm-wiki:Ubuntu`), so items sharing a topic group together in Zotero. Wiki page tags are already the curated set produced by the ingest protocol; do not invent additional tags from Zotero-side metadata. The legacy `llm-wiki:<page-stem>` binding tag form was retired on 2026-08-28: it restated item titles without adding topic structure, and survives only as a removal-review candidate.
4. Do not create a scope tag when an equivalent Zotero collection already expresses that scope. Treat exact collection-name tags and `llm-wiki:<collection-name>` as review-only removal candidates.
5. Remove stale llm-wiki-managed page tags only when the complete reverse mapping has been audited. Never replace the full tag list.
6. Create or update a short index-card note only when requested or enabled by the workflow policy.
7. Synchronize item relations only for reviewed bibliographic relationships. Same-work preprint/published relations may be automated after identity verification; semantic similarity and ordinary wiki links remain wiki-only.
8. Apply writes serially, re-read from the write backend, pass the synchronization barrier, and confirm a second plan produces no unintended changes.

## Zotero-Backed Ingest

Zotero-backed ingest remains a Protocol-mode wiki task; Zotero MCP supplies source discovery, provenance, and verified source content.

1. Resolve and verify the Zotero item and relevant attachment through Zotero MCP.
2. Extract bibliographic and temporal metadata, including title, creators, DOI/arXiv/URL, publication date, collection time when available, citation key, library ID, item key, and attachment key.
3. Read annotations or selected pages before full text when they provide sufficient evidence.
4. Choose the source path according to the connected access mode:
   - **Readable local attachment path available:** verify that the file exists and matches the Zotero item, then optionally create a stable local alias as described below.
   - **Local-path capability unavailable in the current mode:** do not report the attachment as physically absent. If local bytes are expected, request an approved local/hybrid reconfiguration and rerun the capability gate.
   - **Verified indexed text but no readable original bytes:** do not create a private binding or symlink. Ingest directly from verified annotations, selected pages, or full text returned through Zotero MCP, and record the access limitation.
   - **Attachment identity or content unavailable:** stop source-dependent ingest for that item and report the blocker.
5. Ingest from the verified Zotero material or generated local alias using the normal llm-wiki ingest protocol.
6. Preserve stable Zotero identifiers in `sources_meta`; never write machine-specific absolute Zotero paths into wiki pages.
7. Run the normal coverage/depth reviews, link discovery, index update, and logging workflow.

A local alias is an optional convenience, not a prerequisite for Zotero-backed ingest. When it is useful, record the verified attachment path in `sources/zotero/metadata.yaml`, then preview and materialize the declared aliases:

```bash
<PY> scripts/zotero_sources.py --dry-run
<PY> scripts/zotero_sources.py
```

Recommended source metadata:

```yaml
sources_meta:
  - title: "Paper or Article Title"
    type: "academic_paper"
    published: "2025-02"
    collected: "2026-05-20"
    ingested: "2026-05-24"
    date_precision: "month"
    zotero_item_key: "ABCD1234"
    zotero_attachment_key: "EFGH5678"
    citation_key: "author2025title"
    library_id: "0"
    zotero_uri: "<URI returned or independently verified through Zotero MCP>"
    doi: "10.xxxx/example"
    arxiv: "2502.00000"
```

Do not invent missing month/day values. `created` and `updated` remain wiki maintenance dates, not source publication dates. Preserve `zotero_uri` only when Zotero MCP returns it or it has been independently verified; do not synthesize a URI from an item key alone. Omit the field when no verified URI is available.

## Private Source Bindings

Use this version-1 schema when a verified local attachment path is available:

```yaml
version: 1
collections:
  - name: "Collection Name"
    zotero_collection_key: "LTECJSFB"
    items:
      - title: "Paper Title"
        zotero_item_key: "9HQB5NEF"
        attachments:
          - zotero_attachment_key: "RTMTYN5Q"
            content_type: "application/pdf"
            filename: "paper.pdf"
            local_path: "C:/Zotero/storage/RTMTYN5Q/paper.pdf"
            source_alias: "sources/zotero/Collection-Name/9HQB5NEF/RTMTYN5Q.pdf"
```

Binding rules:

- `sources/zotero/metadata.yaml` is private, user-local Zotero binding state and may contain local absolute paths.
- `local_path` must identify a readable file on the current machine and must be obtained or verified through Zotero MCP.
- `source_alias` must be relative to the project root and remain strictly below `sources/zotero/`.
- `sources/zotero/**` is a generated local symlink cache. Never commit the metadata file or the cache.
- Never write Agent-generated summaries, drafts, or synthesized knowledge into either location; generated knowledge belongs in `wiki/`.
- Use Zotero item and attachment keys as cross-machine stable identifiers.
- Treat a Zotero-managed attachment as source material only after the item/attachment identity has been verified through Zotero MCP.
- Always run `scripts/zotero_sources.py --dry-run` before materializing aliases.
- Use `--force` only to replace an existing symlink that points to a different verified source. The helper refuses to replace ordinary files, and Agents must not bypass that safeguard.

## llm-wiki Tag Semantics

Use llm-wiki-managed tags as explicit workflow state, not as interchangeable labels:

| Tag form | Meaning | Add when |
| --- | --- | --- |
| `llm-wiki:<scope>` | Reviewed cross-collection scope classification | The classification audit has passed and no equivalent collection already expresses the scope |
| `llm-wiki:<topic>` | Shared topic tag projected from the bound wiki page's curated `tags:` (e.g. `llm-wiki:Ubuntu`); items sharing a topic aggregate under one tag | The topic assignment has been reviewed |
| `llm-wiki:ingested` | The source has completed the llm-wiki ingest protocol | Wiki drafting, source coverage, depth review, linking, indexing, and logging have completed |
| `llm-wiki:write-sentinel-*` | Temporary authorization test | Only during a write probe; remove and verify removal immediately |

> Retired: `llm-wiki:<page-stem>` binding tags (written before 2026-08-28) restate item titles and add no topic structure. They are removal-review candidates, applied only after the complete reverse mapping has been audited.

Collection membership does not imply ingest completion. Items that have been classified or moved but not yet synthesized may receive reviewed cross-collection scope and topic tags, but must not receive `llm-wiki:ingested`. Do not duplicate an existing collection name as a scope tag. Preserve user-managed tags and use incremental additions/removals rather than replacing the complete tag list.

## Write-Back and Idempotency Rules

Zotero writes are opt-in, minimal, and idempotent where the exposed tools support it:

1. Confirm the user requested or approved the specific write.
2. Show the intended targets, selection rule, source and target collection keys, and mutations before applying a batch or potentially broad change.
3. Before adding an item, search for an existing match by DOI, ISBN, URL, arXiv ID, or another stable identifier.
4. When an add tool exposes `if_exists` or equivalent reuse/skip behavior, prefer an idempotent mode for automated workflows. Do not use a duplicate-always mode unless the user explicitly requests a second item.
5. Prefer incremental updates, such as `add_tags` / `remove_tags` and collection add/remove operations, over whole-field or whole-membership replacement that could erase unrelated state. An incremental tool interface does not by itself prove that the backend implementation is atomic.
6. Serialize writes that touch the same item. Do not run overlapping tag or membership updates in parallel unless the sets are disjoint and the backend behavior has been verified.
7. Re-read from the write backend after every mutation. A tool response such as "items updated" is not sufficient verification.
8. Create Zotero child notes only as index cards: wiki page path, short summary, sync hash/time, and reviewed relationship notes. Do not mirror complete wiki pages into Zotero notes.
9. Add attachments only when the user explicitly requests it and the source has been verified. Check existing attachments by stable source, filename, or content identity when the tool exposes those checks.
10. Use related-item links only when the relationship has been reviewed and either the connected MCP exposes the relation toolset or the user has explicitly authorized the restricted local write-back plan.
11. Refresh the Zotero MCP semantic search database after adding files or materially changing indexed content when semantic search is in use.
12. When local is authoritative and Web is the write backend, wait for the synchronization barrier and re-audit the local-visible state before reporting local completion.

### Safe Collection Membership Migration

For moving items from a source collection to a target collection, use a two-phase migration:

1. Resolve both collection keys in the active library.
2. Snapshot each candidate item's explicit `Collections` field and preserve unrelated memberships.
3. Classify candidates and separate high-confidence, ambiguous, and excluded items.
4. Add the approved items to the target collection only.
5. Re-read and verify target membership for every item.
6. Remove only the source collection membership. Never replace the complete collection list.
7. Re-read and verify that the target is present, the source is absent, and all unrelated memberships remain.
8. Recount source and target collections and verify expected count deltas, accounting for items already present in the target.
9. Sample items with PDFs, notes, annotations, or secondary collection memberships and verify those children and memberships remain intact.

Do not combine the add and remove phases in one unverified operation. A collection migration changes membership only; it must not trash items or attachments.

### Synchronization Barriers and State Invalidation

Treat earlier observations as stale after any of the following:

- enabling or resuming Zotero Data Sync;
- the first synchronization between previously independent local and Web libraries;
- changing `ZOTERO_LOCAL`, credentials, library type, or library ID;
- restarting Zotero Desktop, Codex, or the MCP server;
- switching user/group libraries;
- a user batch-editing the same collections or items;
- a Zotero synchronization reset or conflict resolution.

After such an event, rediscover the library and collection keys, recount relevant collections, and inspect representative item tags and `Collections` fields before continuing. Do not issue broad writes while synchronization is pending or conflict resolution is unknown.

### Verification Report

For a broad write, report enough evidence to reconstruct the state transition:

```text
Metadata authority: local | web
Metadata read backend: local | web
Metadata write backend: local | web
Metadata sync state: disabled | pending | caught_up | divergent | unknown
Attachment authority: local_machine | zotero_file_sync | webdav | linked_external | unknown
Attachment access: local_path | local_api_stream | remote_download | indexed_fulltext_only | unavailable
Source collection and count: ...
Target collection and count: ...
Selection rule and candidate count: ...
Items updated / skipped / failed: ...
Post-write tag or membership verification: ...
Unrelated memberships and child objects sampled: ...
Pending local synchronization: yes | no
```

If local is authoritative, distinguish `cloud write succeeded` from `verified locally`.

## Safety and Failure Handling

- Never expose Zotero API keys, library credentials, private annotations, or local absolute paths in committed files or logs.
- Do not overwrite item metadata, replace all tags, move collections, attach files, or delete Zotero content without explicit authorization.
- Do not import large item or full-text batches without confirmation.
- Do not treat a search result, abstract, or generated summary as a verified original attachment.
- Do not use untrusted files with unsafe deserialization or execute scripts embedded in source material.
- If item identifiers or titles mismatch, stop ingest and report the expected versus observed metadata.
- If a write partially succeeds, report exactly which Zotero objects changed and which did not; do not silently retry broad mutations.
- If an API key or credential is exposed, stop writes, do not repeat the secret, require revocation and rotation, check project files/logs for leakage, restart the Agent host/MCP so the new credential is loaded, and rerun the backend-consistency gate before resuming.
- Do not treat "configuration updated" as proof that a running MCP process has reloaded it.
- Do not use direct SQLite, direct Web API, or an alternative Zotero client to repair a synchronization or capability failure.

## llm-wiki Boundary

Do not add a general native Zotero client or duplicate `zotero-mcp` inside `src/llm_wiki`. `scripts/agent-bridge.py` remains the entry point for llm-wiki workflows. Zotero library discovery, reads, source access, metadata identity, and normal writes remain behind `54yyyu/zotero-mcp`; `zotero_local.py` remains a temporary, loopback-only exception for the reviewed schemas and verification barriers defined above. The separately reviewed `zotero-relocate` path may update only an existing attachment's `linkMode` / `path` and the private local binding layer; it must not clone/delete items, edit notes, change collections, or perform arbitrary API access.

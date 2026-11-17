# Contracko MCP tool index

Use live discovery for tool names and schemas. This index records workflow rules that schemas do not express. [workflows.md](workflows.md) maps user jobs to these tools.

## Discovery and results

Tools absent from discovery are unavailable to this connection. First refresh discovery or reconnect if the client has cached schemas. If an older credential still omits newly available actions, a workspace admin can enable new MCP actions for its key, or the user can re-consent OAuth. Do not guess a call.

Check `isError` first. On success, use `structuredContent` when present or the legacy JSON text otherwise, never both. Required fields missing from the discovered `outputSchema` are a response mismatch, not empty data. Re-read before retrying an `OUTCOME_UNKNOWN` mutation.

## Connection

| Tool | Scope | Use |
|---|---|---|
| `auth_validate` | any valid credential | Confirm workspace and scopes before work. |

## Contracts and folders

| Tool | Scope | Use |
|---|---|---|
| `clm_list_contracts` | `contract:read` | Page contract records and business filters. |
| `clm_get_contract` | `contract:read` | Read one contract, including filing state. |
| `clm_list_folders` | `contract:read` | Page folders visible to the user. |
| `clm_get_folder` | `contract:read` | Inspect one visible folder and its visible path. |
| `clm_create_folder` | `contract:write` | Create a root folder or a child of a visible parent. |
| `clm_rename_folder` | `contract:write` | Rename a manageable folder. |
| `clm_move_folder` | `contract:write` | Move a folder to a visible parent or the root. |
| `clm_move_contract` | `contract:write` | File a contract in a visible folder, or unfile it. |
| `clm_get_folder_access` | `contract:read` | Read a folder access overview. |
| `clm_get_contract_access` | `contract:read` | Read a contract access overview. |

`clm_list_folders` uses `continuation`, not the contract `cursor`. Omitting `parentFolderId`, or sending `parentFolderId: null`, lists only the visible root. Complete root pages, then list and complete the children of every visible folder recursively to enumerate the visible tree. A completed root page set is not a full-tree result. For each parent, repeat the same parent and limit with the opaque continuation until it is `null`. Returned paths contain visible ancestors only. Omission does not prove a hidden folder exists or does not exist.

Inspect a destination before changing it. Confirm the visible path and every bulk change. `clm_move_contract` accepts `folderId: null` only to unfile. `clm_move_folder` accepts `parentFolderId: null` to move to the root. Folder deletes and all access changes are app work. The access tools are overview-only and provide no ACL write operation.

```json mcp:clm_list_folders
{ "limit": 50 }
```

Continue a child-folder page with the same parent and limit. The continuation is opaque.

```json mcp:clm_list_folders
{
  "parentFolderId": "11111111-1111-4111-8111-111111111111",
  "limit": 50,
  "continuation": "opaque-folder-page-token"
}
```

```json mcp:clm_get_folder
{ "id": "11111111-1111-4111-8111-111111111111" }
```

```json mcp:clm_create_folder
{ "name": "Legal", "parentFolderId": null }
```

```json mcp:clm_rename_folder
{ "id": "11111111-1111-4111-8111-111111111111", "name": "Legal and compliance" }
```

```json mcp:clm_move_folder
{ "id": "11111111-1111-4111-8111-111111111111", "parentFolderId": null }
```

```json mcp:clm_move_contract
{ "id": "22222222-2222-4222-8222-222222222222", "folderId": "11111111-1111-4111-8111-111111111111" }
```

Unfile only after the user asks to remove the contract from its folder.

```json mcp:clm_move_contract
{ "id": "22222222-2222-4222-8222-222222222222", "folderId": null }
```

```json mcp:clm_get_folder_access
{ "id": "11111111-1111-4111-8111-111111111111" }
```

```json mcp:clm_get_contract_access
{ "id": "22222222-2222-4222-8222-222222222222" }
```

Use IDs returned by discovery in real calls. The UUIDs above are valid example values only.

### Contract filters and filing state

`clm_list_contracts` supports `status`, `categoryId`, `counterpartyId`, `query`, `endDateFrom`, `endDateTo`, `noticeDateFrom`, `noticeDateTo`, `updatedSince`, and `folderId`. All supplied filters combine with AND. `query` is a literal, trimmed, case-insensitive substring over the title and the assigned Party B display or legal name, including historical names. It is not document search.

The `folderId` list filter must be a valid visible UUID. It cannot be `null`. To audit unfiled contracts, page the applicable contract result and inspect `filing.kind`. A contract has `filing.kind` of `unfiled`, `folder`, or `unavailable`. Every returned contract has `folderId`: it is a visible UUID only for `folder`, otherwise `null`. `filing.folder.id` and `filing.folder.path` are available only for `folder`. Treat `unavailable` as unknown filing, not as unfiled.

Use the narrowest supported filters, then repeat the same normalized filters and opaque `cursor` until `nextCursor` is `null`. Changing any filter starts a new query without a cursor. For an OR question, run separate complete queries and deduplicate by contract ID. For value, currency, null-presence, or custom-field filters, complete the narrowed server result before local filtering. Date windows exclude null dates.

Resolve a vendor with `clm_list_parties` using `query` and `type` before passing its returned ID as `counterpartyId`. When more than one party matches, ask the user to choose.

```json mcp:clm_list_contracts
{
  "endDateFrom": "2026-04-01",
  "endDateTo": "2026-06-30",
  "status": "active",
  "limit": 50
}
```

```json mcp:clm_list_parties
{ "query": "Acme", "type": "company" }
```

## Evidence and review

| Tool | Scope | Use |
|---|---|---|
| `clm_get_contract_analysis` | `contract:read` | Risk, obligations, and key-term analysis. |
| `clm_search_contract_documents` | `contract:read` | Find cited text. `exact` is the stable pagination mode. |
| `clm_read_contract_document` | `contract:read` | Read bounded cited sections. |
| `clm_get_contract_document_download_url` | `contract:read` | Get a short-lived original or preview URL. Do not log it. |
| `clm_list_contract_comments` | `contract:read` | Read comments on one contract. |

## Import and contract writes

| Tool | Scope | Use |
|---|---|---|
| `clm_import_contracts` | `contract:write` | Managed import from inline bytes or a remote URL. |
| `clm_get_import_status` | `contract:read` | Poll import progress and honour `pollAfterMs`. |
| `clm_create_upload_url` | `contract:write` | Create a short-lived upload destination for ingest. |
| `clm_ingest_contract` | `contract:write` | File uploaded documents with agent-supplied metadata and analysis. |
| `clm_add_contract_documents` | `contract:write` | Add draft or related documents, or replace the primary document. |
| `clm_update_contract` | `contract:write` | Partially update one contract with its latest `updatedAt`. |
| `clm_bulk_update_contracts` | `contract:write` | Independently update up to 100 contracts. Confirm the batch. |
| `clm_add_contract_comment` | `contract:write` | Add a comment. After an unknown outcome, list comments before retrying. |
| `clm_create_contract_type` / `clm_update_contract_type` | `contract:write` | Create types and fields, or replace a supplied field set. |
| `clm_list_contract_types` / `clm_get_contract_type` | `contract:read` | Inspect types and fields. |
| `clm_create_party` / `clm_update_party` | `contract:write` | Create or partially update parties. |
| `clm_list_parties` / `clm_get_party` | `contract:read` | Resolve and inspect parties. |

Use inline base64 import only for a small local file when Contracko should extract it. Use a signed short-lived remote URL when Contracko can fetch the document. Use upload then ingest when bytes must bypass model context and the agent supplies the extraction. Never publish a confidential contract to make a remote URL work. [contracko-import](../../contracko-import/SKILL.md) defines these paths.

## Events, reminders, and parser

Events and reminders need `contract:read` to list and `contract:write` to change. List before a change, use the latest `expectedUpdatedAt` for updates or deletes, and confirm a bulk write. Renewal reminders attach to the existing `end` system event.

| Tool family | Scope | Use |
|---|---|---|
| `clm_list_contract_events` | `contract:read` | List custom and supported system events with reminders. |
| `clm_create_contract_events`, `clm_update_contract_events`, `clm_delete_contract_events` | `contract:write` | Manage custom events. |
| `clm_create_event_reminders`, `clm_update_event_reminders`, `clm_delete_event_reminders` | `contract:write` | Manage reminders on events. |
| `parser_get_credits`, `parser_preflight`, `parser_create_upload_url`, `parser_create_job`, `parser_get_job`, `parser_list_jobs` | `parser:compute` | Extract or review documents without filing them as contracts. |

Parser jobs spend credits. Preflight before creating one, and retrieve exports before their retention window ends.

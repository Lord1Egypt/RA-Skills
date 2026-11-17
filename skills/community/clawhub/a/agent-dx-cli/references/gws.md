# GWS practice

Use GWS to verify the relationship between commands, contracts, requests, and output.
Preserve the target provider's names, headers, cursors, authentication, and file boundaries.

## 1. Read the contract

Example goal: inspect recently modified, non-trashed files and understand the returned objects.

```sh
gws drive files list --help
gws schema drive.files.list
gws schema drive.FileList
gws schema drive.File
```

| Command | Inspect | Use the result |
| --- | --- | --- |
| `gws drive files list --help` | Supported `--params`, `--format`, and pagination options. | Select valid CLI flags; JSON query parameters are not separate flags. |
| `gws schema drive.files.list` | `pageSize`, `q`, `orderBy`, and the response type. | Construct the list request; follow the response reference to `FileList`. |
| `gws schema drive.FileList` | `files`, `nextPageToken`, and `incompleteSearch`. | Separate resource data from continuation/completeness; follow `files` items to `File`. |
| `gws schema drive.File` | `id`, `name`, `mimeType`, and `modifiedTime`. | Choose the file fields needed for the task. A type schema describes an object; it does not fetch a file. |

Use current help/schema rather than assuming these outputs are unchanged. Discovery may fetch public metadata; schema queries need no business credentials.
The commands below use the pinned conventions. They need a compatible binary; actual file reads additionally require authorized Drive access.

## 2. Implement the contract

| Object | Implementation and verification |
| --- | --- |
| Command tree | Generate `SERVICE RESOURCE [SUBRESOURCE] METHOD` from Discovery. Use `+` for helpers. |
| Input | Put URL/query parameters in `--params`. Put nested bodies in `--json`. Show only applicable flags. |
| Method schema | Return `httpMethod`, `path`, `description`, `parameters`, and `scopes`. Include `parameterOrder`, `requestBody`, and `response` when applicable. Body types contain `schemaRef` and `schema`. |
| Type references | Preserve nested `$ref` by default. `--resolve-refs` requests expansion. Bound cycles, depth, and size in the target CLI. |
| Descriptions | Explain the object, preconditions, direct effect, and completion boundary. Put constraints in typed contracts. |
| Output | Return raw API JSON by default. `--format json/table/yaml/csv` controls presentation. `--output PATH`/`-o` is a binary destination. |
| Files | Provide `--upload` and `--upload-content-type` only for methods that support media upload. |

A Discovery projection is not a complete JSON Schema validator. Expose accepted global parameters and preserve actual constraints.
Scopes are provider declarations. They do not prove current permissions or mean that every scope is required.
A description is documentation, not executable policy or current state. Use description when it can carry the required meaning.

## 3. Verify bounded reads

List at most two pages, each requesting up to five non-trashed files, ordered by modification time:

```sh
gws drive files list \
  --params '{"q":"trashed = false","orderBy":"modifiedTime desc","pageSize":5,"fields":"files(id,name,mimeType,modifiedTime),nextPageToken,incompleteSearch"}' \
  --page-all --page-limit 2 --format json
```

Expect one page per NDJSON line. `fields` is a server-side projection; this example requests at most ten files, not a complete inventory.
A remaining `nextPageToken` means more pages exist. Even without a token, `incompleteSearch: true` means the search was incomplete; do not claim full coverage.

Read one returned file. Replace `FILE_ID_FROM_LIST` with an actual `files[].id` before running:

```sh
gws drive files get --help
gws schema drive.files.get
gws drive files get \
  --params '{"fileId":"FILE_ID_FROM_LIST","fields":"id,name,mimeType,modifiedTime"}' \
  --format json
```

Check that the returned ID matches the selected resource. Keep the ID literal; field selection belongs in `fields`.
Negative: append a query to `fileId`, such as `?fields=name`, or pass `--output json` to choose a format; `--output` is a binary destination.
The pinned version defaults to 10 pages and 100 ms between pages. Set limits explicitly with `--page-limit` and `--page-delay`.

## 4. Verify previews

Preview creating a folder; query parameters and the resource body have separate inputs:

```sh
gws drive files create --help
gws schema drive.files.create
gws drive files create \
  --params '{"fields":"id,name,mimeType"}' \
  --json '{"name":"dx-preview","mimeType":"application/vnd.google-apps.folder"}' \
  --dry-run
```

Check that `dry_run` is true, `method` is POST, `url` targets Drive files, `query_params` contains the projection, and `body` contains the folder name/type.
Inspect `is_multipart_upload` and secret masking. A preview is a request plan, not a created folder or a success receipt.
Negative: place `name` in `--params`, put the field projection in `--json`, or remove `--dry-run` without authorization for creation.
The reference GWS preview can initialize authentication.
If the target declares a local-only preview, use the main skill to prove zero business HTTP, credential access, and recovery writes.
Declare metadata discovery as a separate read.

## 5. Verify adaptations

- If the target supports `@FILE` or `-`/stdin, declare these as extensions. Bound input size and parse JSON strictly. Allow one stdin consumer per call.
- Supply secrets through private files, stdin, or credential references. Keep the target provider's authentication and least privilege.
- Preserve flag meanings during migration. Compare HTTP requests and observable behavior to verify differences.
- Check structured JSON on stdout and diagnostics on stderr. Exit codes: 0 success; 1 API; 2 auth; 3 validation; 4 discovery; 5 internal.
- If MCP is required, use a compatible official SDK and a shared typed executor. Call the executor directly and test the interface separately. The pinned source has no MCP entrypoint.
- If an external response sanitizer is used, configure it explicitly first. Preserve payload and provenance. Treat sanitized results as data.

Reference: [GWS 0.22.5, commit a3768d0e82ad83cca2da97724e46bea4ff0e6dbd](https://github.com/googleworkspace/cli/tree/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/crates/google-workspace-cli/src).
Recheck behavior when changing the version.

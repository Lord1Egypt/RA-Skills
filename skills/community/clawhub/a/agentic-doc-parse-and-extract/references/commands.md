# ADP CLI Complete Command Reference

> This document is strictly aligned with the CLI's built-in `adp schema` output. Agent can also run `adp schema` to get the machine-readable JSON version of this spec.

## Global Options

| Option | Type | Description |
|--------|------|-------------|
| `--lang` | string | Set language (`en` or `zh`) |
| `--json` | boolean | Output in JSON format (recommended for Agent) |
| `--quiet` | boolean | Suppress all output except errors |

---

## config — Configuration Management

### `adp config set`

Set API Key or Base URL.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | API Key for authentication |
| `--api-base-url` | string | No | API Base URL |

### `adp config get`

View current configuration (no options).

### `adp config clear`

Clear all configuration.

| Option | Type | Description |
|--------|------|-------------|
| `--force`, `-y` | boolean | Skip confirmation prompt |

---

## app-id — Application Management

### `adp app-id list`

Query available applications.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-label` | string | No | — | Filter by application label |
| `--app-type` | integer | No | — | Filter by application type: `0`=system preset, `1`=custom; omit to list all |
| `--limit` | integer | No | 120 | Maximum number of results |

### `adp app-id cache`

View cached application list (no options). Cache is permanent and does not expire.

---

## credit — Credit Balance

### `adp credit`

Check current account credit balance.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |

---

## parse — Document Parsing

Parses the entire document to retrieve full text, layout, structure, and content.

### `adp parse local <file-path>`

Parse local file or folder (batch mode when path is a folder).

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately (use with `--async`) |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent processing count (max 1 free, max 2 paid) |
| `--retry` | integer | No | 0 | Number of retries on failure (exponential backoff) |

### `adp parse url <url>`

Parse document from URL. When the URL points to a text file containing a list of URLs (one per line), batch mode is activated.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately (use with `--async`) |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent processing count |
| `--retry` | integer | No | 0 | Number of retries on failure |

### `adp parse base64 <base64-strings>`

Parse base64-encoded document content.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--file-name` | string | No | "document" | Display name with extension for the base64 content (used to detect file type; does not read from disk) |
| `--concurrency` | integer | No | 1 | Concurrent processing count |
| `--retry` | integer | No | 0 | Number of retries on failure |

### `adp parse query <task-ids...>`

Query async parse task status and results. Supports multiple task IDs as arguments.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--watch` | boolean | No | false | Continuously poll until task completes |
| `--file` | string | No | — | Read task IDs from a JSON file (produced by `--no-wait`) |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Watch mode timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent query count |

---

## extract — Document Extraction

Extracts specific structured fields from documents (amount, date, company name, etc.).

### `adp extract local <file-path>`

Extract from local file or folder (batch mode when path is a folder).

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent processing count |
| `--retry` | integer | No | 0 | Number of retries on failure |

### `adp extract url <url>`

Extract from URL document. Supports URL list file for batch mode.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent processing count |
| `--retry` | integer | No | 0 | Number of retries on failure |

### `adp extract base64 <base64-strings>`

Extract from base64-encoded document content.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--app-id` | string | **Yes** | — | Application ID |
| `--async` | boolean | No | false | Enable asynchronous processing |
| `--no-wait` | boolean | No | false | Submit async task and return immediately |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Timeout in seconds |
| `--file-name` | string | No | "document" | Display name with extension for the base64 content (used to detect file type; does not read from disk) |
| `--concurrency` | integer | No | 1 | Concurrent processing count |
| `--retry` | integer | No | 0 | Number of retries on failure |

### `adp extract query <task-ids...>`

Query async extract task status and results. Supports multiple task IDs.

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--watch` | boolean | No | false | Continuously poll until task completes |
| `--file` | string | No | — | Read task IDs from a JSON file (produced by `--no-wait`) |
| `--export` | string | No | — | Export results to specified path |
| `--timeout` | integer | No | 900 | Watch mode timeout in seconds |
| `--concurrency` | integer | No | 1 | Concurrent query count |

---

## custom-app — Custom Extraction Application Management

### `adp custom-app create`

Create a custom extraction application.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-name` | string | **Yes** | Application name |
| `--app-label` | string | No | Application labels (up to 5) |
| `--extract-fields` | string (JSON) | **Yes** | Field definitions in JSON format |
| `--parse-mode` | string | **Yes** | Parsing mode: `advance`, `standard`, or `agentic` |
| `--enable-long-doc` | string | **Yes** | Enable long document processing (`true`/`false`) |
| `--long-doc-config` | string (JSON) | No | Long document type configuration (only applied when `--enable-long-doc true`) |

### `adp custom-app update`

Update an existing custom extraction application.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-id` | string | **Yes** | Application ID to update |
| `--app-name` | string | No | New application name |
| `--app-label` | string | No | New application labels |
| `--extract-fields` | string (JSON) | **Yes** | Updated field definitions |
| `--parse-mode` | string | **Yes** | Parsing mode: `advance`, `standard`, or `agentic` |
| `--enable-long-doc` | string | No | Enable long document processing (`true`/`false`); if omitted, server default behavior is preserved |
| `--long-doc-config` | string (JSON) | No | Long document type configuration (only applied when `--enable-long-doc true`) |

### `adp custom-app get-config`

View custom application configuration.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-id` | string | **Yes** | Application ID |
| `--config-version` | string | No | Configuration version (e.g., `v1`) |

### `adp custom-app delete`

Delete a custom application.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-id` | string | **Yes** | Application ID to delete |

### `adp custom-app delete-version`

Delete a specific version of a custom application.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-id` | string | **Yes** | Application ID |
| `--config-version` | string | **Yes** | Version to delete (e.g., `v2`) |

### `adp custom-app ai-generate`

AI-powered field recommendation based on a sample document.

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--api-key` | string | No | Override configured API Key |
| `--app-id` | string | **Yes** | Application ID |
| `--file-url` | string | No | Sample document URL |
| `--file-local` | string | No | Sample document local path |
| `--base64` | string | No | Sample document base64 content |

> Note: Provide exactly one of `--file-url`, `--file-local`, or `--base64`.

---

## schema — Machine-Readable Command Spec

### `adp schema`

Output the complete command schema in JSON format. Designed for Agent introspection — Agent can call this command at startup to dynamically discover all available commands, parameters, types, and defaults.

---

## help — Help

### `adp --help`

View the complete list of commands and usage instructions.

---

## ADP Error Codes

See [error-handling.md](error-handling.md) for the complete error code reference and Agent recovery strategies.

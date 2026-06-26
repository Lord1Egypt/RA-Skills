---
skill: batch
category: Batch Execution & Power-User Tools
commands: [run, batch]
description: "Execute single commands via spec objects, run sequential batches, use batch files with multiple named batches, and run parallel command groups across tabs."
---

# Batch Execution & Power-User Tools

Two CLI commands for advanced browser automation: execute individual commands via generic spec objects, and run entire command sequences as batches. Batch files support multiple named batches, parallel groups, and four flexible JSON formats.

> **Prerequisite:** A browser session must be active before using these commands. See [session.md](session.md) for session creation.

---

## Table of Contents

1. [run](#1-run) — Execute a single command spec
2. [batch](#2-batch) — Execute a sequence of commands
3. [Command Spec Schema](#3-command-spec-schema) — Full field reference
4. [Command Types Reference](#4-command-types-reference) — All supported types
5. [CLI Batch Files](#5-cli-batch-files) — `browsectl batch --file`
6. [Batch File Formats](#6-batch-file-formats) — Four accepted JSON shapes
7. [Parallel Groups](#7-parallel-groups) — Concurrent multi-tab execution
8. [Tab Reference Resolution](#8-tab-reference-resolution) — How `tab` fields are resolved
9. [Execution Flow](#9-execution-flow) — Step-by-step runtime behaviour
10. [Real-World Examples](#10-real-world-examples) — Complete batch files

---

## 1. `run`

Execute a single WebDriver command by passing a command spec object. This is a power-user escape hatch for advanced commands not covered by the dedicated CLI commands (`open`, `click`, etc.).

| | |
|---|---|
| **CLI** | `browsectl run --type <CMD> [flags]` |
| **Internal handler** | `batch::execute_command` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `command` | object | **Yes** | — | A command spec object. See [Command Spec Schema](#3-command-spec-schema) for all fields. |

### CLI Usage

```sh
browsectl run --type <TYPE> [--selector S] [--url U] [--text T] [--path P] \
              [--timeout N] [--ms N] [--condition C] [--direction D] \
              [--amount N] [--behavior B] [--tab T] [--scope S] \
              [--fallback F] [--viewport W,H]
```

### CLI Examples

```sh
# Click a button with a 5-second timeout
browsectl run --type click --selector "button.submit" --timeout 5000

# Open a URL with custom viewport
browsectl run --type open --url "https://example.com" --viewport 1440,900

# Wait for an element to appear
browsectl run --type wait --condition displayed --selector "#content" --timeout 10000

# Take a screenshot
browsectl run --type screenshot --selector ".chart" --path "outputs/chart.png"
```

### Example Response — Success

```json
{
  "ok": true,
  "type": "click",
  "selector": "button.submit",
  "scope": null,
  "jsClick": false,
  "fallback": null
}
```

### Example Response — Error

```json
{
  "ok": false,
  "error": "element not found: button.submit"
}
```

### Notes

- `run` is a thin wrapper around the same dispatch used by all dedicated commands. It provides no extra capabilities, just a unified interface for passing arbitrary command specs.
- If a `tab` field is present on the command, the runtime switches to that tab **before** executing the command.
- The response shape varies by command type — it matches the response you'd get from the corresponding dedicated command.

---

## 2. `batch`

Execute a sequence of WebDriver commands in order. Execution stops at the first error unless the failing command has `continueOnError` set to `true`.

| | |
|---|---|
| **CLI** | `browsectl batch --file <PATH> [--name NAME]` |
| **Internal handler** | `batch::execute_batch` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `commands` | array | **Yes** | — | Array of command spec objects (same schema as `run`'s `command`). |

### CLI Usage

```sh
browsectl batch --file <PATH> [--name NAME]
```

| Flag | Type | Required | Description |
|---|---|---|---|
| `--file` | path | **Yes** | Path to a JSON batch file. |
| `--name` | string | Conditional | Batch name to run. Required when the file contains multiple named batches. |

### Example Response — All Succeed

```json
{
  "ok": true,
  "results": [
    { "index": 0, "ok": true, "command": "open", "result": { "ok": true, "type": "open", "url": "https://example.com" } },
    { "index": 1, "ok": true, "command": "wait", "result": { "ok": true, "type": "wait", "selector": "#main", "condition": "displayed" } },
    { "index": 2, "ok": true, "command": "screenshot", "result": { "ok": true, "type": "screenshot", "path": "outputs/main.png" } },
    { "index": 3, "ok": true, "command": "title", "result": { "ok": true, "type": "title", "title": "Example Domain" } }
  ]
}
```

### Example Response — Error Stops Execution

If command at index 1 fails and does not have `continueOnError`, execution stops:

```json
{
  "ok": false,
  "results": [
    { "index": 0, "ok": true, "command": "open", "result": { "ok": true, "type": "open", "url": "https://example.com" } },
    { "index": 1, "ok": false, "command": "wait", "error": "wait timeout: element not found after 5000ms: #main" }
  ]
}
```

Commands at index 2 and 3 are never executed.

### Notes

- Every result entry includes the 0-based `index`, a boolean `ok`, the `command` type string, and either `result` (on success) or `error` (on failure).
- The top-level `ok` is `true` only if **all** commands succeeded.
- For named batches, parallel groups, and multi-batch files, use the CLI `browsectl batch --file` command with `--name`.

---

## 3. Command Spec Schema

Every command — whether passed to `run`, included in a `batch` array, or written in a batch file — follows the same **command spec** schema:

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | **Yes** | Command type. See [Command Types Reference](#4-command-types-reference). |
| `selector` | string | No | CSS selector targeting the element. Supports text-regex extensions (see [selectors.md](selectors.md)). |
| `scope` | string | No | Scope root CSS selector. Element lookups are limited to within the first match. |
| `fallback` | string | No | Click fallback strategy. `"parent"` clicks the parent element, `"sibling"` clicks the next sibling. Can also be an arbitrary CSS selector. |
| `url` | string | No | URL for `open` and `tab-create`. Bare domains are auto-prefixed with `https://`. |
| `text` | string | No | Text content for `fill` (character-by-character typing) and `paste` (clipboard simulation). |
| `path` | string | No | File path for `screenshot` output (PNG). |
| `ms` | integer | No | Sleep duration in milliseconds for `wait` (when no `condition` is set). |
| `condition` | string | No | Wait condition: `"displayed"`, `"hidden"`, `"url"`, `"title"`, `"js"`, or `"attribute"`. |
| `attribute` | string | No | Attribute name for `wait` with `condition: "attribute"`. |
| `value` | string | No | Expected value for `wait` conditions (`url`, `title`, `attribute`, `js`). |
| `timeout` | integer | No | Maximum wait time in milliseconds. Used by `click`, `fill`, `paste`, `screenshot`, and `wait`. |
| `interval` | integer | No | Polling interval in milliseconds for `wait` conditions. |
| `direction` | string | No | Scroll direction: `"up"`, `"down"`, `"left"`, `"right"`. |
| `amount` | integer | No | Scroll amount in pixels. |
| `behavior` | string | No | Scroll behavior: `"smooth"` or `"auto"`. |
| `tab` | any | No | Tab reference — numeric index, string alias, or raw window handle. When present, the runtime switches to this tab **before** executing the command. |
| `viewport` | object | No | Viewport dimensions `{ "width": int, "height": int }` for `open`. |
| `continueOnError` | boolean | No | If `true`, batch execution continues even if this command fails. Default: `false`. |
| `alias` | string | No | Tab alias for `tab-create`. Registers a named reference for the new tab. |
| `activate` | boolean | No | Whether to activate (switch to) the new tab after `tab-create`. Default: `true`. |
| `groups` | array | No | Array of parallel group objects for `type: "parallel"`. See [Parallel Groups](#7-parallel-groups). |

---

## 4. Command Types Reference

| Type | Key Params | Description |
|---|---|---|
| `open` | `url`, `viewport` | Navigate current tab to a URL. |
| `click` | `selector`, `scope`, `fallback`, `timeout` | Click an element. Supports smart fallback when native click is intercepted. |
| `fill` | `text`, `selector`, `scope`, `timeout` | Clear an input then type text character-by-character. |
| `paste` | `text`, `selector`, `scope`, `timeout` | Paste text into an input via clipboard simulation. |
| `screenshot` | `selector`, `scope`, `path`, `timeout` | Capture an element to a PNG file. |
| `scroll` | `direction`, `amount`, `selector`, `behavior` | Scroll the page or a specific element. |
| `title` | *(none)* | Get the current page title. |
| `last-message-content` | `selector` | Extract content from the last message block on the page. |
| `wait` | `condition`, `selector`, `value`, `ms`, `timeout`, `interval` | Wait for a condition to be met, or sleep for a fixed duration. |
| `tab-list` | *(none)* | List all open tabs/windows. |
| `tab-create` | `url`, `alias`, `activate` | Create a new tab, optionally navigating to a URL. |
| `tab-switch` | `tab` | Switch to a tab by index, alias, or handle. |
| `tab-close` | `tab` | Close a tab by index, alias, or handle. |
| `parallel` | `groups` | Run multiple command groups concurrently. See [Parallel Groups](#7-parallel-groups). |

---

## 5. CLI Batch Files

The CLI `batch` subcommand loads a JSON file, normalizes it into one or more named batches, selects one, and executes it sequentially.

### Usage

```sh
browsectl batch --file <PATH> [--name NAME]
```

### Selection Rules

- If the file contains a **single batch** (formats 1 or 2 below), `--name` is optional. The batch runs directly.
- If the file contains **multiple batches** (formats 3 or 4 below), `--name` is **required** to select which batch to run.
- If `--name` is provided but doesn't match any batch, the CLI prints available batch names and exits with an error.

### Example

```sh
# Run the only batch in a simple file
browsectl batch --file examples/multi-tab-parallel.json

# Run a specific batch from a multi-batch file
browsectl batch --file examples/doubao-login-generate.json --name login-qrcode

# Run a different batch from the same file
browsectl batch --file examples/doubao-login-generate.json --name send-message
```

---

## 6. Batch File Formats

Four JSON shapes are accepted. All are normalized internally into a uniform `Vec<NamedBatch>` structure.

### Format 1 — Plain Array

A bare JSON array of command objects. Creates a single batch named `"default"`.

```json
[
  { "type": "open", "url": "https://example.com" },
  { "type": "click", "selector": "button.submit" }
]
```

### Format 2 — Object with `commands`

A single batch with optional metadata fields.

```json
{
  "name": "login-flow",
  "description": "Automate login via QR code",
  "continueOnError": false,
  "commands": [
    { "type": "open", "url": "https://example.com/login" },
    { "type": "screenshot", "selector": ".qrcode", "path": "outputs/qr.png" }
  ]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `commands` | array | **Yes** | Array of command spec objects. |
| `name` | string | No | Batch name. Defaults to `"default"`. |
| `description` | string | No | Human-readable description. |
| `continueOnError` | boolean | No | Batch-level default. Individual commands can override. |

### Format 3 — Object with `batches` as Array

Multiple named batches in an array. Use `--name` to select one.

```json
{
  "batches": [
    {
      "name": "login-qrcode",
      "description": "Open login and screenshot QR",
      "commands": [
        { "type": "open", "url": "https://example.com/login" },
        { "type": "screenshot", "selector": ".qrcode", "path": "outputs/qr.png" }
      ]
    },
    {
      "name": "send-message",
      "description": "Type and send a message",
      "commands": [
        { "type": "paste", "selector": "#input", "text": "Hello!" },
        { "type": "click", "selector": "button[type=submit]" }
      ]
    }
  ]
}
```

### Format 4 — Object with `batches` as Map

Multiple named batches as a key-value map. Keys become the batch names.

```json
{
  "batches": {
    "login": {
      "description": "Navigate to login page",
      "commands": [
        { "type": "open", "url": "https://example.com/login" }
      ]
    },
    "interact": {
      "description": "Fill form and submit",
      "commands": [
        { "type": "fill", "selector": "#email", "text": "user@example.com" },
        { "type": "click", "selector": "button.submit" }
      ]
    }
  }
}
```

---

## 7. Parallel Groups

A command with `"type": "parallel"` runs multiple command groups concurrently. This is especially useful for multi-tab workflows where independent actions on different tabs can execute simultaneously.

### Schema

```json
{
  "type": "parallel",
  "groups": [
    {
      "name": "group-a",
      "tab": "tab-alias-a",
      "commands": [ ... ]
    },
    {
      "name": "group-b",
      "tab": 1,
      "commands": [ ... ]
    }
  ]
}
```

### Group Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Group name for identification in results. Auto-generated as `"group-0"`, `"group-1"`, etc. if omitted. |
| `tab` | any | No | Tab reference to switch to before running the group's commands. |
| `commands` | array | **Yes** | Array of command spec objects to execute sequentially within this group. |

### How It Works

1. For each group, a **cloned** `WdClient` is created. The clone shares the same underlying browser session and HTTP connection pool but can independently switch tabs.
2. Each group is spawned as an independent `tokio::spawn` task.
3. If a group specifies a `tab`, the worker switches to that tab before running any commands.
4. Within each group, commands execute **sequentially** (like a mini-batch).
5. All groups run **concurrently** with respect to each other.
6. The parallel command completes when all groups have finished.

### Response

```json
{
  "ok": true,
  "type": "parallel",
  "mode": "optimistic-parallel",
  "groups": [
    {
      "name": "group-a",
      "ok": true,
      "results": [
        { "index": 0, "ok": true, "command": "title", "result": { "ok": true, "type": "title", "title": "Page A" } }
      ]
    },
    {
      "name": "group-b",
      "ok": true,
      "results": [
        { "index": 0, "ok": true, "command": "title", "result": { "ok": true, "type": "title", "title": "Page B" } }
      ]
    }
  ]
}
```

- The top-level `ok` is `true` only if **all** groups succeeded.
- Each group has its own `ok`, `name`, and `results` array (identical format to `batch` results).
- `mode` is always `"optimistic-parallel"` — all groups run regardless of individual failures.

### Notes

- **Tab isolation:** Each parallel group gets its own cloned driver client. Switching tabs within one group does not affect other groups.
- **Shared session:** All groups share the same browser session. DOM mutations from one group *are* visible to others if they're operating on the same tab (which is rare and should be avoided).
- **Error handling:** A failure in one group does not terminate other groups. The overall `ok` is `false` if any group fails.
- **Nesting:** Parallel groups can include any command type, including nested `parallel` commands — though deeply nested parallelism is rarely useful.

---

## 8. Tab Reference Resolution

The `tab` field (available on every command spec and on parallel groups) accepts multiple formats. Resolution order:

| Input | Example | Resolution |
|---|---|---|
| Numeric index (JSON number) | `0`, `1`, `2` | Index into the current window-handles list. |
| String `"current"` | `"current"` | No-op — stays on the current tab. |
| String alias | `"tab-a"`, `"xiaohongshu"` | Looks up the alias registered by a prior `tab-create` with `alias`. |
| Stringified numeric index | `"0"`, `"1"` | Parsed as a number, then used as an index. |
| Raw window handle | `"CDwindow-..."` | Matched directly against known window handles. |

---

## 9. Execution Flow

### Sequential Batch Execution

For each command in the sequence:

1. **Tab switch** — If the command has a `tab` field, switch to that tab first.
2. **Dispatch** — Route to the appropriate handler based on `type`:
   - `tab-list`, `tab-create`, `tab-switch`, `tab-close` → tab manager
   - `parallel` → parallel group executor
   - Everything else (`open`, `click`, `fill`, etc.) → single command handler
3. **Record result** — On success: `{ "index": N, "ok": true, "command": "<type>", "result": {...} }`
4. **Handle error** — On failure: `{ "index": N, "ok": false, "command": "<type>", "error": "..." }`
   - If `continueOnError` is `true` on the failing command → continue to next command.
   - Otherwise → stop execution, return collected results.
5. **Persist state** — After all commands complete (or on stop), the session's tab state is persisted to `.browsectl/sessions.json`.

### CLI Batch File Flow

1. **Load** — Read and parse the JSON file.
2. **Normalize** — Convert to a uniform list of named batches via `normalize_batch_plan`.
3. **Select** — If `--name` is given, find the matching batch. If not given and there's exactly one batch, use it. If not given and there are multiple, error.
4. **Execute** — Run the selected batch's commands sequentially via `execute_batch`.
5. **Output** — Print the JSON result to stdout.

---

## 10. Real-World Examples

### Example 1: Login QR Code Flow

A multi-batch file for automating QR-code-based login on a Chinese AI platform. Each batch handles a different phase: initial login, QR screenshot, refresh, and sending a message.

**File:** `examples/doubao-login-generate.json`

```json
{
  "batches": [
    {
      "name": "login-qrcode",
      "description": "Open login page and capture QR code screenshot",
      "commands": [
        { "type": "tab-switch", "tab": 0 },
        {
          "type": "open",
          "url": "https://www.doubao.com/chat/create-image",
          "viewport": { "width": 1024, "height": 768 }
        },
        { "type": "click", "selector": "button[data-testid=\"to_login_button\"]" },
        {
          "type": "screenshot",
          "selector": "div[data-testid=\"qrcode_image\"]",
          "path": "outputs/qrcode_image.png"
        }
      ]
    },
    {
      "name": "refresh-qrcode",
      "description": "Refresh the QR code and recapture",
      "commands": [
        { "type": "tab-switch", "tab": 0 },
        {
          "type": "click",
          "fallback": "sibling",
          "selector": "div[data-testid=\"qrcode_image\"]"
        },
        { "type": "wait", "ms": 800 },
        {
          "type": "screenshot",
          "selector": "div[data-testid=\"qrcode_image\"]",
          "path": "outputs/qrcode_image-refreshed.png"
        }
      ]
    },
    {
      "name": "send-message",
      "description": "Send a prompt and extract the response",
      "commands": [
        { "type": "tab-switch", "tab": 0 },
        { "type": "click", "selector": "div[data-testid=\"skill-page-item-3\"]" },
        { "type": "paste", "text": "A cartoon pony working at a computer" },
        { "type": "click", "selector": "button[data-testid=\"chat_input_send_button\"]" },
        {
          "type": "wait",
          "selector": "div[data-testid=\"message-block-container\"]",
          "condition": "displayed",
          "timeout": 20000,
          "interval": 500
        },
        {
          "type": "last-message-content",
          "selector": "div[data-testid=\"message-block-container\"]"
        }
      ]
    }
  ]
}
```

Usage:

```sh
# Step 1: Get the QR code
browsectl batch --file examples/doubao-login-generate.json --name login-qrcode

# Step 2: If QR expires, refresh it
browsectl batch --file examples/doubao-login-generate.json --name refresh-qrcode

# Step 3: After scanning, send a message
browsectl batch --file examples/doubao-login-generate.json --name send-message
```

### Example 2: Multi-Tab Parallel Operations

Create two tabs, then read both page titles concurrently using parallel groups.

**File:** `examples/multi-tab-parallel.json`

```json
{
  "commands": [
    {
      "type": "tab-create",
      "alias": "tab-a",
      "url": "https://example.com"
    },
    {
      "type": "tab-create",
      "alias": "tab-b",
      "url": "https://example.org"
    },
    {
      "type": "parallel",
      "groups": [
        {
          "name": "read-a",
          "tab": "tab-a",
          "commands": [
            { "type": "wait", "selector": "body", "condition": "displayed", "timeout": 10000 },
            { "type": "title" }
          ]
        },
        {
          "name": "read-b",
          "tab": "tab-b",
          "commands": [
            { "type": "wait", "selector": "body", "condition": "displayed", "timeout": 10000 },
            { "type": "title" }
          ]
        }
      ]
    },
    {
      "type": "tab-list"
    }
  ]
}
```

Usage:

```sh
browsectl batch --file examples/multi-tab-parallel.json
```

### Example 3: Cross-Site QR Login with Scroll

Open a second site in a new tab, wait for its QR code, screenshot it, and scroll down — all as one batch.

```json
{
  "name": "xiaohongshu-login-qrcode",
  "description": "Open Xiaohongshu in a new tab and capture login QR",
  "commands": [
    {
      "type": "tab-create",
      "alias": "xiaohongshu",
      "url": "https://www.xiaohongshu.com",
      "activate": true
    },
    {
      "type": "wait",
      "selector": "img.qrcode-img",
      "condition": "displayed",
      "timeout": 20000,
      "interval": 500
    },
    {
      "type": "screenshot",
      "selector": "img.qrcode-img",
      "path": "outputs/xiaohongshu-qrcode.png"
    },
    {
      "type": "scroll",
      "direction": "down",
      "amount": 1200
    }
  ]
}
```

### Example 4: Resilient Batch with `continueOnError`

Dismiss optional UI elements that may or may not exist, then proceed to the main task.

```json
{
  "name": "resilient-scrape",
  "description": "Dismiss popups if present, then scrape content",
  "commands": [
    { "type": "open", "url": "https://news.example.com" },
    { "type": "click", "selector": ".cookie-banner .accept", "continueOnError": true },
    { "type": "click", "selector": ".newsletter-popup .close", "continueOnError": true },
    { "type": "wait", "condition": "displayed", "selector": "article.main", "timeout": 10000 },
    { "type": "screenshot", "selector": "article.main", "path": "outputs/article.png" },
    { "type": "scroll", "direction": "down", "amount": 2000 },
    { "type": "screenshot", "selector": "body", "path": "outputs/full-page.png" }
  ]
}
```

---

## Quick Reference

| Task | CLI | Key Fields |
|---|---|---|
| Run a single command | `browsectl run --type T` | `--selector`, `--url`, etc. |
| Run a batch file | `browsectl batch --file F` | `--name` if multi-batch |
| Run commands in parallel | `type: "parallel"` | `groups: [{ tab, commands }]` |
| Continue on failure | `continueOnError: true` | Per-command or per-batch |

---

## Common Patterns

### Navigate → Wait → Screenshot

```json
[
  { "type": "open", "url": "https://dashboard.example.com" },
  { "type": "wait", "condition": "displayed", "selector": ".dashboard-loaded", "timeout": 15000 },
  { "type": "screenshot", "selector": ".dashboard", "path": "outputs/dashboard.png" }
]
```

### Multi-Tab Setup → Parallel Work → Collect Results

```json
[
  { "type": "tab-create", "alias": "a", "url": "https://a.example.com" },
  { "type": "tab-create", "alias": "b", "url": "https://b.example.com" },
  {
    "type": "parallel",
    "groups": [
      { "name": "work-a", "tab": "a", "commands": [{ "type": "title" }] },
      { "name": "work-b", "tab": "b", "commands": [{ "type": "title" }] }
    ]
  },
  { "type": "tab-list" }
]
```

### Defensive Automation with Optional Elements

```json
[
  { "type": "open", "url": "https://app.example.com" },
  { "type": "click", "selector": ".dismiss-popup", "continueOnError": true },
  { "type": "click", "selector": ".accept-cookies", "continueOnError": true },
  { "type": "fill", "selector": "#search", "text": "automation" },
  { "type": "click", "selector": "button.search" }
]
```

### QR Code Login Workflow

```json
[
  { "type": "open", "url": "https://app.example.com/login" },
  { "type": "wait", "condition": "displayed", "selector": ".qr-code", "timeout": 10000 },
  { "type": "screenshot", "selector": ".qr-code", "path": "outputs/qr.png" }
]
```

The AI agent can then display the QR screenshot to the user, wait for them to scan, and continue:

```json
[
  { "type": "wait", "condition": "url", "value": "https://app.example.com/home", "timeout": 120000, "interval": 2000 },
  { "type": "title" }
]
```

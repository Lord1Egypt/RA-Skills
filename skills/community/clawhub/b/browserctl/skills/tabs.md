# Tab Management

> **Tools:** `list_tabs` · `create_tab` · `switch_tab` · `close_tab`

browsectl treats every browser window/tab as a **handle** — an opaque string
assigned by WebDriver. You can reference a tab in three ways: by its **0-based
numeric index**, by a human-friendly **alias**, or by the **raw window handle
id**. All four tab tools share this resolution logic.

---

## Table of Contents

1. [Tab Reference Resolution](#tab-reference-resolution)
2. [list_tabs](#1-list_tabs)
3. [create_tab](#2-create_tab)
4. [switch_tab](#3-switch_tab)
5. [close_tab](#4-close_tab)
6. [Tab Aliases](#tab-aliases)
7. [Tab Context in Batch Commands](#tab-context-in-batch-commands)
8. [Full Batch Example](#full-batch-example)

---

## Tab Reference Resolution

Whenever a tool or command accepts a **tab reference** (`tab` parameter), the
value is resolved in the following order:

| Priority | Kind | Example value | Behaviour |
|---|---|---|---|
| 1 | **Numeric index** (0-based) | `0`, `1`, `2` | Looked up positionally in the current window-handles array. |
| 2 | **`"current"`** | `"current"` | No-op — stays on the active tab. |
| 3 | **Alias string** | `"xiaohongshu"` | Resolved through the in-memory alias → handle map. |
| 4 | **Stringified numeric index** | `"0"`, `"1"` | Parsed as a number, then used as an index (same as priority 1). |
| 5 | **Raw window handle** | `"CDwindow-A1B2C3"` | Matched directly against existing handles. |

If none of the above match, the tool returns an error: `tab not found: <value>`.

### Examples

```text
# By index
browsectl tab-switch --tab 0

# By alias
browsectl tab-switch --tab xiaohongshu

# By raw handle
browsectl tab-switch --tab CDwindow-A1B2C3D4E5
```

---

## 1. `list_tabs`

List all open tabs/windows in a browser session.

### Interfaces

| Interface | Invocation |
|---|---|
| **CLI** | `browsectl tab-list` |
| **REPL** | `tabs` |

### Parameters

*This command has no required parameters. It uses the current default session.*

### CLI Usage

```sh
# List all tabs (uses default session)
browsectl tab-list

# List tabs for a specific session
browsectl tab-list --session abc123
```

### Response

```json
{
  "tabs": [
    {
      "handle": "CDwindow-AAAA",
      "active": true,
      "aliases": ["main"]
    },
    {
      "handle": "CDwindow-BBBB",
      "active": false,
      "aliases": ["xiaohongshu"]
    },
    {
      "handle": "CDwindow-CCCC",
      "active": false,
      "aliases": []
    }
  ],
  "currentHandle": "CDwindow-AAAA",
  "totalTabs": 3
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `tabs` | array | Array of tab objects. |
| `tabs[].handle` | string | The WebDriver window handle id. |
| `tabs[].active` | boolean | `true` if this tab is the currently focused one. |
| `tabs[].aliases` | string[] | All aliases pointing to this handle (may be empty). |
| `currentHandle` | string | The handle of the active tab. |
| `totalTabs` | number | Total number of open tabs. |

### Notes

- The tab array is ordered by WebDriver's internal handle list. Index `0` is
  the first handle returned by the driver, not necessarily the leftmost visual
  tab.
- Stale aliases (pointing to handles that no longer exist) are automatically
  filtered out.

---

## 2. `create_tab`

Open a new browser tab, optionally navigating to a URL and assigning an alias.

### Interfaces

| Interface | Invocation |
|---|---|
| **CLI** | `browsectl tab-create [--url URL] [--alias NAME] [--activate true]` |
| **REPL** | `tab-create [url] [alias]` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | string | No | `about:blank` | URL to open in the new tab. |
| `alias` | string | No | *(none)* | Human-friendly alias for the tab. Used to reference it later in `switch_tab`, `close_tab`, batch `"tab"` fields, etc. |
| `activate` | boolean | No | `true` | Whether to switch focus to the new tab after creation. When `false`, the previously active tab retains focus. |

### CLI Usage

```sh
# Open a blank tab (activated by default)
browsectl tab-create

# Open a tab with a URL
browsectl tab-create --url https://example.com

# Open a tab with a URL and an alias
browsectl tab-create --url https://xiaohongshu.com --alias xiaohongshu

# Open a tab in the background (don't switch to it)
browsectl tab-create --url https://example.org --alias background --activate false
```

### REPL Usage

```text
> tab-create https://example.com myalias
```

The REPL shorthand always activates the new tab. The first positional argument
is the URL, the second is the alias.

### Response

```json
{
  "handle": "CDwindow-DDDD",
  "alias": "xiaohongshu",
  "activated": true,
  "totalTabs": 4
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `handle` | string | The new tab's window handle id. |
| `alias` | string \| null | The alias assigned, or `null` if none was provided. |
| `activated` | boolean | Whether focus was switched to the new tab. |
| `totalTabs` | number | Total number of open tabs after creation. |

### Notes

- Internally uses `window.open(url, '_blank')` to create the tab.
- After creation the session's tab list is persisted via `upsert_runtime`, so
  aliases survive across CLI invocations.
- If `activate` is `false`, the driver switches back to the previously active
  tab after opening the new one.

---

## 3. `switch_tab`

Switch the browser's active tab by numeric index, alias, or raw window handle.

### Interfaces

| Interface | Invocation |
|---|---|
| **CLI** | `browsectl tab-switch --tab <REF>` |
| **REPL** | `tab-switch <ref>` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `tab` | string \| number | **Yes** | — | Tab reference. See [Tab Reference Resolution](#tab-reference-resolution) for accepted formats. |

### CLI Usage

```sh
# Switch by 0-based index
browsectl tab-switch --tab 0

# Switch by alias
browsectl tab-switch --tab xiaohongshu

# Switch by raw handle
browsectl tab-switch --tab CDwindow-BBBB
```

### REPL Usage

```text
> tab-switch 1
> tab-switch xiaohongshu
```

### Response

```json
{
  "currentHandle": "CDwindow-BBBB"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `currentHandle` | string | The handle of the tab that is now active. |

### Notes

- The session state is updated after switching (`upsert_runtime`).
- Switching to `"current"` is a no-op and returns the current handle.

---

## 4. `close_tab`

Close a tab by numeric index, alias, or raw window handle.

### Interfaces

| Interface | Invocation |
|---|---|
| **CLI** | `browsectl tab-close --tab <REF>` |
| **REPL** | `tab-close <ref>` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `tab` | string \| number | **Yes** | — | Tab reference. See [Tab Reference Resolution](#tab-reference-resolution) for accepted formats. |

### CLI Usage

```sh
# Close by index
browsectl tab-close --tab 2

# Close by alias
browsectl tab-close --tab xiaohongshu

# Close by raw handle
browsectl tab-close --tab CDwindow-CCCC
```

### REPL Usage

```text
> tab-close 2
> tab-close xiaohongshu
```

### Response

```json
{
  "closedHandle": "CDwindow-BBBB",
  "currentHandle": "CDwindow-AAAA",
  "totalTabs": 2
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `closedHandle` | string | The handle of the tab that was closed. |
| `currentHandle` | string \| null | The handle of the tab that is now active (the first remaining tab), or `null` if no tabs remain. |
| `totalTabs` | number | Total number of tabs remaining after closure. |

### Notes

- The driver first **switches to** the target tab, then closes it with
  `close_window`.
- After closing, it automatically switches to the **first remaining** tab.
- Any aliases that pointed at the closed handle are removed from the alias map.
- The session's tab list is persisted via `upsert_runtime`.
- **Warning:** Closing the last tab in a session will leave the session with no
  windows. Subsequent commands that require a tab will fail until a new tab is
  created.

---

## Tab Aliases

Aliases are human-friendly names that map to window handles. They make it easy
to reference tabs by name instead of by opaque handle strings or brittle
numeric indices.

### How Aliases Work

1. **Set during `create_tab`** — pass the `alias` parameter when creating a tab.
2. **Stored in session state** — aliases are kept in the `RuntimeCtx.tab_aliases`
   map (a `HashMap<String, String>` of alias → handle).
3. **Persisted across CLI invocations** — every tab mutation calls
   `upsert_runtime`, which writes the current alias map into
   `.browsectl/sessions.json`. The next CLI command that loads the
   session will have the same aliases available.
4. **Cleaned up automatically** — when listing tabs (`collect_tabs`), any alias
   whose handle no longer exists is filtered out. When closing a tab, its
   aliases are explicitly removed.

### When to Use Aliases

- **Batch files** — give each tab a meaningful name so parallel groups can
  reference them with `"tab": "my-alias"`.
- **REPL sessions** — quickly jump between tabs: `tab-switch docs`.

### Alias Constraints

- An alias is any non-empty string that is **not** a valid numeric index and
  **not** `"current"`.
- Multiple aliases can point to the same handle.
- Aliases are unique by name — creating a new tab with an alias that already
  exists will overwrite the previous mapping.

---

## Tab Context in Batch Commands

Any command in a batch file can include a `"tab"` field. When present, the
runner switches to that tab **before** executing the command. This is
especially powerful inside **parallel groups**, where each group can operate on
a different tab concurrently.

### Command-Level Tab Switch

```json
{
  "type": "title",
  "tab": "xiaohongshu"
}
```

Before running `title`, the runner calls `switch_to_tab("xiaohongshu")`.

### Parallel Group Tab Switch

Each group in a `"parallel"` block can specify a `"tab"` field. The spawned
worker will switch to that tab before executing any of the group's commands.
Each worker gets its own `RuntimeCtx` clone, so concurrent tab switches don't
interfere with each other.

```json
{
  "type": "parallel",
  "groups": [
    {
      "name": "group-a",
      "tab": "tab-a",
      "commands": [
        { "type": "title" }
      ]
    },
    {
      "name": "group-b",
      "tab": "tab-b",
      "commands": [
        { "type": "title" }
      ]
    }
  ]
}
```

---

## Full Batch Example

The following batch file demonstrates a realistic workflow:

1. Create two tabs with aliases.
2. Run parallel operations on each tab.

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
            {
              "type": "wait",
              "selector": "body",
              "condition": "displayed",
              "timeout": 10000
            },
            { "type": "title" }
          ]
        },
        {
          "name": "read-b",
          "tab": "tab-b",
          "commands": [
            {
              "type": "wait",
              "selector": "body",
              "condition": "displayed",
              "timeout": 10000
            },
            { "type": "title" }
          ]
        }
      ]
    }
  ]
}
```

### Running the Batch

```sh
browsectl batch --file tabs-demo.json
```

### Expected Output

```json
{
  "ok": true,
  "results": [
    { "ok": true, "handle": "CDwindow-XXXX", "alias": "tab-a", "activated": true, "totalTabs": 2 },
    { "ok": true, "handle": "CDwindow-YYYY", "alias": "tab-b", "activated": true, "totalTabs": 3 },
    {
      "ok": true,
      "type": "parallel",
      "results": [
        { "name": "read-a", "ok": true, "results": [
          { "ok": true, "matched": true },
          { "ok": true, "type": "title", "title": "Example Domain" }
        ]},
        { "name": "read-b", "ok": true, "results": [
          { "ok": true, "matched": true },
          { "ok": true, "type": "title", "title": "Example Domain" }
        ]}
      ]
    }
  ]
}
```

### What Happens Step-by-Step

1. **`tab-create` (tab-a)** — opens `https://example.com` in a new tab,
   assigns alias `tab-a`, and switches focus to it.
2. **`tab-create` (tab-b)** — opens `https://example.org` in another new tab,
   assigns alias `tab-b`, and switches focus to it.
3. **`parallel`** — spawns two concurrent workers:
   - **read-a**: switches to `tab-a`, waits for `<body>` to be displayed, then
     reads the page title.
   - **read-b**: switches to `tab-b`, waits for `<body>` to be displayed, then
     reads the page title.

Both groups run simultaneously because each worker operates on its own tab with
an independent `RuntimeCtx` clone. Results are collected and returned once all
groups complete.
# Interactive REPL

> Live command-line interface for ad-hoc browser automation.
> Tab-completion, persistent history, and all browser commands at your fingertips.

---

## Starting the REPL

```sh
browsectl repl
# or target a specific session:
browsectl --session <ID> repl
```

The REPL requires an active browser session. If a default session already exists (persisted in `.browsectl/sessions.json`), it is reused automatically; otherwise create one first with `browsectl session-create`.

On startup the REPL prints:

```
repl session: <session-id>
type "help" for commands, Tab to complete, "exit" to quit
browsectl>
```

### Shell Features

| Feature | Details |
|---|---|
| **Tab completion** | Press `Tab` to autocomplete command names (first token only). |
| **Hint text** | As you type, a dim grey ghost-text shows the first matching command. |
| **Command history** | Automatically saved to `.browsectl/repl_history` and restored across sessions (up to 1 000 entries). |
| **Ctrl-C** | Cancels the current input line. The REPL keeps running. |
| **Ctrl-D** | Sends EOF — exits the REPL (same as typing `exit`). |
| **Empty lines** | Silently ignored. |

---

## Command Reference

All commands return a single JSON object to stdout. Errors are printed to stderr as `error: <message>`.

### Quick Overview

| Command | Syntax | Description |
|---|---|---|
| `open` | `open <url>` | Navigate to a URL |
| `click` | `click <selector> [options]` | Click an element |
| `fill` | `fill [<selector>] <text>` | Type text into an input |
| `paste` | `paste [<selector>] <text>` | Paste text into an input (clipboard simulation) |
| `screenshot` | `screenshot <selector> [<path>]` | Capture an element to a PNG file |
| `scroll` | `scroll [<direction>] [<amount>] [<selector>]` | Scroll the page or a specific element |
| `title` | `title` | Get the current page title |
| `tabs` | `tabs` | List all open tabs |
| `tab-create` | `tab-create [<url>] [<alias>]` | Open a new tab |
| `tab-switch` | `tab-switch <ref>` | Switch to a tab by index, alias, or handle |
| `tab-close` | `tab-close <ref>` | Close a tab |
| `wait` | `wait [<ms>]` or `wait <selector> <condition> [<value>]` | Wait for a delay or a DOM condition |
| `last-message` | `last-message` | Extract the last message block content |
| `help` | `help` | Print the built-in command list |
| `exit` / `quit` | `exit` | Exit the REPL |

---

## Detailed Command Syntax

### `open`

```
open <url>
```

Navigates the current tab to `<url>`. Relative URLs are passed through as-is; the WebDriver server resolves them.

**Example:**

```
browsectl> open https://example.com
{"ok":true,"type":"open","url":"https://example.com"}
```

---

### `click`

```
click <selector>
click <selector> --fallback <strategy>
click <selector> --scope <scope-selector>
click <selector> --scope <scope-selector> --fallback <strategy>
click <selector> --fallback <strategy> --scope <scope-selector>
```

Clicks the first element matching `<selector>`.

| Option | Description |
|---|---|
| `--fallback <strategy>` | If the primary selector fails, retry with `parent`, `sibling`, or an arbitrary CSS selector. |
| `--scope <selector>` | Restrict the search to descendants of the scope element. |

Both flags are optional and can appear in any order after the selector.

**Examples:**

```
browsectl> click button[data-testid="submit"]
browsectl> click .menu-item --fallback parent
browsectl> click .save-btn --scope .modal --fallback sibling
```

---

### `fill`

```
fill <text>                   # type into the currently focused element
fill <selector> <text>        # click the selector first, then type
```

Simulates keyboard input character-by-character.

- **1 argument** (command + text) — text is sent to whichever element currently has focus.
- **2+ arguments** (command + selector + text) — the first argument is treated as a CSS selector; the remaining arguments are joined with spaces and typed as text.

**Examples:**

```
browsectl> fill hello world
browsectl> fill input[name="email"] user@example.com
```

---

### `paste`

```
paste <text>                  # paste into the currently focused element
paste <selector> <text>       # click the selector first, then paste
```

Same argument rules as `fill`, but inserts text via clipboard simulation instead of keystroke emulation. Useful for large text or fields that don't accept normal key events.

---

### `screenshot`

```
screenshot <selector>              # capture to auto-generated path
screenshot <selector> <path>       # capture to a specific file
```

Captures the element matching `<selector>` as a PNG image.

**Example:**

```
browsectl> screenshot div[data-testid="qrcode"] outputs/qr.png
{"ok":true,"type":"screenshot","path":"outputs/qr.png",...}
```

---

### `scroll`

```
scroll                              # scroll down 800px (default)
scroll <direction>                  # scroll 800px in <direction>
scroll <direction> <amount>         # scroll <amount>px in <direction>
scroll <direction> <amount> <sel>   # scroll a specific element
```

| Parameter | Values | Default |
|---|---|---|
| `direction` | `up`, `down` | `down` |
| `amount` | integer (pixels) | `800` |
| `selector` | CSS selector for a scrollable container | *(viewport)* |

**Examples:**

```
browsectl> scroll
browsectl> scroll up 400
browsectl> scroll down 1200 .chat-container
```

---

### `title`

```
title
```

Returns the `document.title` of the current page.

```
browsectl> title
{"ok":true,"type":"title","title":"Example Domain"}
```

---

### `tabs`

```
tabs
```

Lists all open browser tabs, including their window handles and the currently active handle.

```
browsectl> tabs
{"handles":["CDwindow-ABC","CDwindow-DEF"],"currentHandle":"CDwindow-ABC","tabs":[...]}
```

---

### `tab-create`

```
tab-create                       # blank new tab
tab-create <url>                 # new tab navigated to <url>
tab-create <url> <alias>         # new tab with a friendly alias
```

Opens a new tab (and switches to it).

```
browsectl> tab-create https://example.com docs
{"ok":true,...}
```

---

### `tab-switch`

```
tab-switch <ref>
```

Switch to a tab identified by numeric index (0-based), alias, or raw window handle.

```
browsectl> tab-switch docs
browsectl> tab-switch 0
```

---

### `tab-close`

```
tab-close <ref>
```

Close a tab by index, alias, or handle. If omitted, defaults to the current tab.

---

### `wait`

```
wait                                          # sleep 500ms (default)
wait <ms>                                     # sleep <ms> milliseconds
wait <selector> <condition> [<value>]         # wait for a DOM condition
```

#### Delay Mode

| Syntax | Behaviour |
|---|---|
| `wait` | Pause for 500 ms. |
| `wait 2000` | Pause for 2 000 ms. |

If the first argument after `wait` parses as an integer, it is treated as a millisecond delay.

#### Condition Mode

The first argument is a CSS selector; the second is the condition name.

| Condition | Extra args | Description |
|---|---|---|
| `displayed` | — | Element is visible. This is the default if no condition is given. |
| `hidden` | — | Element is present but not visible. |
| `exist` | — | Element exists in the DOM. |
| `gone` | — | Element has been removed from the DOM. |
| `clickable` | — | Element is both visible and enabled. |
| `text-contains` | `<value>` | Element's text content contains `<value>`. |
| `text-equals` | `<value>` | Element's text content equals `<value>` exactly. |
| `value-contains` | `<value>` | Element's `value` property contains `<value>`. |
| `value-equals` | `<value>` | Element's `value` property equals `<value>` exactly. |
| `attribute-equals` | `<attr> <value>` | Element's attribute `<attr>` equals `<value>`. |
| `attribute-contains` | `<attr> <value>` | Element's attribute `<attr>` contains `<value>`. |

**Examples:**

```
browsectl> wait
browsectl> wait 3000
browsectl> wait .spinner hidden
browsectl> wait #result text-contains Success
browsectl> wait input[name="q"] value-equals hello world
browsectl> wait .btn attribute-equals aria-disabled false
```

---

### `last-message`

```
last-message
```

Alias: `last-message-content`. Extracts the content of the last message block on the page (useful for chat-style UIs).

---

### `help`

```
help
```

Prints the built-in summary of all CLI subcommands and run types.

---

### `exit` / `quit`

```
exit
quit
```

Saves command history to `.browsectl/repl_history` and exits the REPL. The browser session remains active and can be reused by subsequent CLI commands or a new REPL session.

---

## Example Session

```
$ browsectl repl
repl session: a1b2c3d4
type "help" for commands, Tab to complete, "exit" to quit

browsectl> open https://doubao.com
{"ok":true,"type":"open","url":"https://doubao.com"}

browsectl> click button[data-testid="to_login_button"]
{"ok":true,"type":"click","selector":"button[data-testid=\"to_login_button\"]",...}

browsectl> wait .qr-code displayed
{"ok":true,"type":"wait","selector":".qr-code","condition":"displayed"}

browsectl> screenshot div[data-testid="qrcode_image"] outputs/qr.png
{"ok":true,"type":"screenshot","path":"outputs/qr.png",...}

browsectl> tab-create https://example.com myalias
{"ok":true,...}

browsectl> tabs
{"handles":["CDwindow-AAA","CDwindow-BBB"],"currentHandle":"CDwindow-BBB","tabs":[...]}

browsectl> tab-switch 0
{"ok":true,...}

browsectl> title
{"ok":true,"type":"title","title":"豆包"}

browsectl> scroll down 600 .chat-list
{"ok":true,"type":"scroll",...}

browsectl> fill input[name="search"] browsectl automation
{"ok":true,"type":"fill",...}

browsectl> wait 2000
{"ok":true,"type":"wait","ms":2000}

browsectl> last-message
{"ok":true,"type":"last-message-content","content":"..."}

browsectl> exit
```

---

## Notes

- **Selectors** follow the same syntax as the rest of browsectl — standard CSS selectors plus the `text/…/` regex extension. See [selectors.md](selectors.md) for details.
- **JSON output** — every command emits a single JSON object with an `"ok"` field. Pipe or parse this in scripts that drive the REPL via stdin (see the `--session` flag to target an existing session).
- **History file** — stored at `.browsectl/repl_history`. The directory is created automatically. Maximum 1 000 entries are retained.
- **Tab completion** only applies to the first token (command name). Arguments are not completed.
- **Unrecognised commands** fall through to a generic dispatcher that maps the first word to a command type and passes remaining arguments as selector / text. Prefer the documented commands above for reliable behaviour.
---
skill: session
commands:
  - setup
  - status
  - driver-start
  - session-create
  - session-list
  - session-use
  - session-delete
---

# Session & Driver Lifecycle

This document covers the full lifecycle of browser sessions in **browsectl**: environment setup, WebDriver server management, session creation/listing/switching/deletion, and persistence. It describes 7 CLI commands.

> **First-time users:** Always run `browsectl setup` before anything else. This detects your platform, finds installed browsers, and auto-downloads the matching WebDriver binary. You only need to do this once (or when you update your browser).

---

## Table of Contents

1. [setup](#1-setup)
2. [driver-start](#2-driver-start)
3. [status](#3-status)
4. [session-create](#4-session-create)
5. [session-list](#5-session-list)
6. [session-use](#6-session-use)
7. [session-delete](#7-session-delete)
8. [Session Persistence](#8-session-persistence)
9. [Lifecycle Overview](#9-lifecycle-overview)

---

## 1. `setup`

Detects the platform, installed browsers and their versions, and auto-downloads the matching WebDriver binary (chromedriver for Chrome, msedgedriver for Edge). Results are persisted to `.browsectl/setup.json` so that subsequent commands can skip re-detection.

### CLI Usage

```
browsectl setup [--browser chrome|edge] [--check-only]
```

### CLI Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--browser` | `string` | Global `--browser` flag (`chrome`) | Browser to set up: `"chrome"` or `"edge"`. Overrides the global `--browser` flag. |
| `--check-only` | `bool` | `false` | Only report detected info — do **not** download drivers. |

### Behaviour

1. **Platform detection** — OS (macOS / Linux / Windows) and architecture (x64 / arm64).
2. **Browser detection** — Scans for Chrome and Edge installations, reports name, version, and binary path.
3. **Driver detection** — For each installed browser, checks whether the corresponding WebDriver binary exists and whether its major version matches the browser's major version.
4. **Auto-download** (unless `--check-only`) — If the driver is missing or its version doesn't match, downloads the correct version automatically.
5. **Auto-select fallback** — If the selected browser (e.g. Chrome) isn't installed but another one (e.g. Edge) is, `setup` auto-selects the available browser and reports the change.
6. **Persist** — Writes results to `.browsectl/setup.json`.

### Example Invocation

```
$ browsectl setup
Platform: macOS arm64

Browsers:
  chrome — 137.0.7151.69 (/Applications/Google Chrome.app/Contents/MacOS/Google Chrome)
  edge   — 137.0.3296.68 (/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge)

Drivers:
  chrome driver — 137.0.7151.68 (./chromedriver) ✓ version match
  edge driver   — not found (./msedgedriver)

Downloading msedgedriver 137.0.3296.68…
Ready! edge driver is available at ./msedgedriver
Setup info saved to .browsectl/setup.json
```

### Example: Check Only

```
$ browsectl setup --check-only
Platform: macOS arm64

Browsers:
  chrome — 137.0.7151.69 (/Applications/Google Chrome.app/Contents/MacOS/Google Chrome)

Drivers:
  chrome driver — 137.0.7151.68 (./chromedriver) ✓ version match

Setup info saved to .browsectl/setup.json
```

### Persisted Data (`.browsectl/setup.json`)

```json
{
  "platform": {
    "os": "macos",
    "arch": "arm64",
    "display": "macOS arm64"
  },
  "browsers": [
    {
      "browser": "chrome",
      "path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      "version": "137.0.7151.69",
      "majorVersion": 137,
      "installed": true
    }
  ],
  "drivers": [
    {
      "browser": "chrome",
      "path": "./chromedriver",
      "version": "137.0.7151.68",
      "exists": true,
      "matched": true
    }
  ],
  "readyBrowser": "chrome",
  "readyDriverPath": "./chromedriver",
  "updatedAt": "2025-07-11T12:34:56Z"
}
```

---

## 2. `driver-start`

Starts the WebDriver server (chromedriver / msedgedriver) if it is not already running. Returns immediately once the server is accepting connections.

### CLI Usage

```
browsectl driver-start
```

### Behaviour

1. Checks whether the WebDriver server at the configured URL (default `http://127.0.0.1:9515`) is already responding to `/status`.
2. If already running, returns immediately with `"reused": true`.
3. If not running, spawns the driver binary as a background process on the configured port and polls `/status` until ready (up to 15 seconds).
4. The spawned process is detached — it continues running after the CLI exits.

### Response

```json
{
  "ok": true,
  "reused": false,
  "server": "http://127.0.0.1:9515"
}
```

| Field | Type | Description |
|---|---|---|
| `ok` | `bool` | Always `true` on success (error throws). |
| `reused` | `bool` | `true` if the driver was already running; `false` if freshly started. |
| `server` | `string` | The WebDriver server URL. |

### Example

```
$ browsectl driver-start
{"ok":true,"reused":false,"server":"http://127.0.0.1:9515"}

$ browsectl driver-start
{"ok":true,"reused":true,"server":"http://127.0.0.1:9515"}
```

---

## 3. `status`

Check whether the WebDriver server (chromedriver / msedgedriver) is running and return its `/status` response.

Use this command to **verify the server is healthy** before creating sessions or to diagnose connectivity problems.

### CLI Usage

```
browsectl status
```

### Response — Server Running

```json
{
  "ok": true,
  "status": {
    "value": {
      "build": {
        "version": "137.0.7151.68"
      },
      "message": "ChromeDriver ready for new sessions.",
      "os": {
        "arch": "arm64",
        "name": "Mac OS X",
        "version": "15.5.0"
      },
      "ready": true
    }
  }
}
```

### Response — Server Not Running

```json
{
  "ok": false,
  "error": "error sending request for url (http://127.0.0.1:9515/status): connection refused"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `ok` | `bool` | `true` if the server responded successfully. |
| `status` | `object` | The raw JSON body from the WebDriver `/status` endpoint (only present when `ok` is `true`). |
| `error` | `string` | Human-readable error message (only present when `ok` is `false`). |

### Typical Usage Pattern

```
1. Run `browsectl status` to check server health.
2. If ok is false → run `browsectl driver-start`.
3. If ok is true → proceed with session creation or commands.
```

---

## 4. `session-create`

Create a new browser session. This launches a Chrome or Edge instance via the WebDriver server, persists the session to disk, and returns the session ID.

### CLI Usage

```
browsectl session-create [--foreground] [--detach] [--copy-data] [--no-copy-data]
```

### CLI-Specific Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--foreground` | `bool` | `false` | Run session creation in the current process (no background worker). |
| `--detach` | `bool` | `false` | Spawn a background worker and return immediately (fire-and-forget). |
| `--copy-data` | `bool` | `false` | Copy cookies and extensions from the real browser profile. Skips the interactive prompt. |
| `--no-copy-data` | `bool` | `false` | Do not copy any user data. Skips the interactive prompt. Conflicts with `--copy-data`. |

### CLI Execution Modes

| Mode | Flags | Behaviour |
|---|---|---|
| **Background (default)** | *(neither flag)* | Spawns a background worker process and polls until it finishes. The result is printed when complete. |
| **Foreground** | `--foreground` | Runs session creation entirely in the current process. Useful for debugging. |
| **Detached** | `--detach` | Spawns the worker and returns immediately. The session will appear in `session-list` once the worker finishes. |

### Profile Data Copy

When running interactively (without `--copy-data` or `--no-copy-data`), the CLI prompts the user to choose what to copy. In non-interactive mode (background worker, piped stdin), it defaults to copying cookies and extensions.

| Data Category | Default (copy-data) | Description |
|---|---|---|
| Cookies | ✅ Yes | The `Cookies` SQLite database. |
| Extensions | ✅ Yes | Installed browser extensions / plugins. |
| Local Storage | ❌ No | `localStorage` data. |
| Bookmarks | ❌ No | Bookmark entries. |

### Automation Profile

By default, browsectl uses a **dedicated automation profile** at `~/.browsectl/<browser>-profile` (e.g. `~/.browsectl/chrome-profile`). This ensures the automation session **never conflicts** with the user's running browser.

If the automation profile's lock file is detected (indicating another automation session is using it), browsectl automatically **clones** the profile to a temporary directory and uses the clone instead. The temporary clone is cleaned up when the session is deleted.

### Internal Steps

1. Read cached setup info from `.browsectl/setup.json` (if available) to locate the driver binary and browser version.
2. If setup info is unavailable or stale, re-detect the driver and download if necessary.
3. Start the WebDriver server via `ensure_running` (if not already running).
4. If `copy_data` is enabled, copy selected data from the real browser profile to the automation profile.
5. Build WebDriver capabilities (browser binary, user-data-dir, profile, headless, viewport, etc.).
6. Send the `POST /session` request to the WebDriver server.
7. If session creation fails due to a profile lock, clone the profile and retry.
8. Persist the new session to `.browsectl/sessions.json` and set it as the default.

### Response

```json
{
  "ok": true,
  "sessionId": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `ok` | `bool` | `true` on success. |
| `sessionId` | `string` | The WebDriver session ID assigned by chromedriver. |

### Error Response

```json
{
  "ok": false,
  "error": "failed to create session even with cloned profile: session not created"
}
```

### Example — CLI

```
$ browsectl session-create --foreground --no-copy-data
{"ok":true,"sessionId":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"}

$ browsectl session-create --copy-data --detach
{"ok":true,"workerPid":12345,"outputFile":"/tmp/browsectl-session-XXXX.json"}

$ browsectl --headless session-create --foreground
{"ok":true,"sessionId":"b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5"}
```

---

## 5. `session-list`

List all persisted browser sessions and identify which one is the current default.

### CLI Usage

```
browsectl session-list
```

### Response

```json
{
  "defaultSessionId": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
  "sessions": {
    "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4": {
      "sessionId": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
      "server": {
        "hostname": "127.0.0.1",
        "port": 9515,
        "path": "/",
        "url": "http://127.0.0.1:9515"
      },
      "capabilities": {
        "browserName": "chrome",
        "browserVersion": "137.0.7151.69",
        "platformName": "mac"
      },
      "tempProfileDir": null,
      "tabs": {
        "handles": ["CDwindow-ABC123"],
        "currentHandle": "CDwindow-ABC123",
        "aliases": {}
      },
      "createdAt": "2025-07-11T12:34:56Z",
      "updatedAt": "2025-07-11T12:35:10Z"
    },
    "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3": {
      "sessionId": "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
      "server": {
        "hostname": "127.0.0.1",
        "port": 9515,
        "path": "/",
        "url": "http://127.0.0.1:9515"
      },
      "capabilities": {
        "browserName": "chrome",
        "browserVersion": "137.0.7151.69",
        "platformName": "mac"
      },
      "tempProfileDir": "/tmp/browsectl-clone-XYZ789",
      "tabs": {
        "handles": ["CDwindow-DEF456", "CDwindow-GHI789"],
        "currentHandle": "CDwindow-DEF456",
        "aliases": { "main": "CDwindow-DEF456" }
      },
      "createdAt": "2025-07-11T13:00:00Z",
      "updatedAt": "2025-07-11T13:05:22Z"
    }
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `defaultSessionId` | `string \| null` | The session ID currently set as default, or `null` if no sessions exist. |
| `sessions` | `object` | Map of session ID → session record. |

### Session Record Fields

| Field | Type | Description |
|---|---|---|
| `sessionId` | `string` | The WebDriver session ID. |
| `server` | `object` | WebDriver server connection info (`hostname`, `port`, `path`, `url`). |
| `capabilities` | `object` | Browser capabilities returned by chromedriver at session creation. |
| `tempProfileDir` | `string \| null` | Path to the cloned profile directory, if applicable. Cleaned up on delete. |
| `tabs` | `object` | Tab state: `handles` (list), `currentHandle`, `aliases` (map of alias → handle). |
| `createdAt` | `string` | ISO 8601 timestamp of when the session was created. |
| `updatedAt` | `string` | ISO 8601 timestamp of when the session record was last updated. |

---

## 6. `session-use`

Set a session as the default active session. All subsequent commands that don't specify an explicit `--session` flag will operate on this session.

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `--session` | `string` | **Yes** | — | The session ID to set as the default. Must exist in the session store. |

### CLI Usage

```
browsectl session-use --session <ID>
```

### CLI Flags

| Flag | Type | Required | Description |
|---|---|---|---|
| `--session` | `string` | **Yes** | The session ID to set as default. |

### Response

```json
{
  "ok": true,
  "defaultSessionId": "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `ok` | `bool` | `true` on success. |
| `defaultSessionId` | `string` | The session ID that is now the default. |

### Error — Session Not Found

If the supplied session ID does not exist in the store, the call fails:

```json
{
  "error": "Session not found: nonexistent-id-12345"
}
```

### Example — CLI

```
$ browsectl session-list
{"defaultSessionId":"aaa...","sessions":{...}}

$ browsectl session-use --session f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3
{"ok":true,"defaultSessionId":"f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3"}
```

---

## 7. `session-delete`

Delete a browser session. This sends a WebDriver `DELETE /session` request to quit the browser, removes any temporary profile directory, and removes the session from the persisted store.

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `--session` | `string` | No | Current default session | The session ID to delete. If omitted, the current default session is deleted. |

### CLI Usage

```
browsectl session-delete [--session <ID>]
```

### CLI Flags

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--session` | `string` | No | Current default session | The session ID to delete. If omitted, deletes the default session (or the session specified by the global `--session` flag). |

### Behaviour

1. Resolve the effective session ID: explicit parameter → global `--session` flag → persisted default.
2. If the session has a live browser, quit the browser and clean up.
3. If the session is only in the persisted store, attempt to re-attach to the running browser and quit it.
4. If a temporary profile directory exists for the session, delete it from disk.
5. Remove the session from `.browsectl/sessions.json`.
6. If the deleted session was the default, automatically promote another session (if any) as the new default.

### Response

```json
{
  "deletedSessionId": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
  "defaultSessionId": "f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `deletedSessionId` | `string` | The session ID that was deleted. |
| `defaultSessionId` | `string \| null` | The new default session ID after deletion, or `null` if no sessions remain. |

### Error — No Session

```json
{
  "error": "no session to delete"
}
```

### Example — CLI

```
$ browsectl session-delete
{"deletedSessionId":"a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4","defaultSessionId":null}

$ browsectl session-delete --session f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3
{"deletedSessionId":"f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3","defaultSessionId":"a1b2c3..."}
```

---

## 8. Session Persistence

Sessions are persisted to disk so they survive across CLI invocations and can be re-attached to.

### File Locations

| File | Purpose |
|---|---|
| `.browsectl/sessions.json` | Live session store — tracks all active browser sessions. |
| `.browsectl/setup.json` | Cached setup info — platform, browser, and driver detection results. |
| `~/.browsectl/chrome-profile/` | Default automation profile directory for Chrome. |
| `~/.browsectl/edge-profile/` | Default automation profile directory for Edge. |

### Session Store Schema (`.browsectl/sessions.json`)

```json
{
  "defaultSessionId": "a1b2c3d4...",
  "sessions": {
    "a1b2c3d4...": {
      "sessionId": "a1b2c3d4...",
      "server": {
        "hostname": "127.0.0.1",
        "port": 9515,
        "path": "/",
        "url": "http://127.0.0.1:9515"
      },
      "capabilities": { "browserName": "chrome", "..." : "..." },
      "tempProfileDir": null,
      "tabs": {
        "handles": ["CDwindow-ABC123"],
        "currentHandle": "CDwindow-ABC123",
        "aliases": {}
      },
      "createdAt": "2025-07-11T12:34:56Z",
      "updatedAt": "2025-07-11T12:35:10Z"
    }
  }
}
```

### Store Operations

| Operation | Function | Description |
|---|---|---|
| **Read** | `read_store()` | Load the session store from disk. Returns empty store if file doesn't exist or is corrupt. |
| **Write** | `write_store()` | Serialize and write the full store to disk. |
| **Upsert** | `upsert()` | Insert or update a session record and optionally set it as default. |
| **Remove** | `remove()` | Remove a session by ID. If it was the default, promote another session. |
| **Set default** | `set_default()` | Change which session is the default (must exist in the store). |

---

## 9. Lifecycle Overview

### Recommended Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. browsectl setup                                         │
│     → Detects platform, browsers, downloads driver          │
│     → Writes .browsectl/setup.json                          │
├─────────────────────────────────────────────────────────────┤
│  2. browsectl status                                        │
│     → Verify chromedriver is reachable (optional)           │
├─────────────────────────────────────────────────────────────┤
│  3. browsectl session-create                                │
│     → Starts driver if needed                               │
│     → Copies profile data if requested                      │
│     → Launches browser, creates WebDriver session           │
│     → Persists to .browsectl/sessions.json                  │
├─────────────────────────────────────────────────────────────┤
│  4. Use browser commands (open, click, fill, screenshot…)   │
│     → All operate on the default session automatically      │
├─────────────────────────────────────────────────────────────┤
│  5. browsectl session-create  (create a second session)     │
│     → New session becomes the default                       │
├─────────────────────────────────────────────────────────────┤
│  6. browsectl session-use --session <old-id>                │
│     → Switch back to a previous session                     │
├─────────────────────────────────────────────────────────────┤
│  7. browsectl session-delete                                │
│     → Quits the browser, cleans up temp dirs                │
│     → Removes from session store                            │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

- **Dedicated automation profile**: Sessions use `~/.browsectl/<browser>-profile` by default, never the user's real profile directory. This prevents lock conflicts with a running browser.
- **Profile cloning on lock**: If the automation profile is already locked (e.g. by another automation session), browsectl clones it to a temp directory and retries. The temp directory is cleaned up on `delete_session`.
- **Profile data copy**: Users can opt in to copying cookies, extensions, localStorage, and bookmarks from their real browser profile into the automation profile — useful for testing authenticated flows.
- **WebDriver server reuse**: The driver process (chromedriver/msedgedriver) is started once and reused across sessions. Multiple sessions can coexist on the same driver.
- **No implicit browser killing**: When a stale session is detected, browsectl does **not** kill browser processes — that could close the user's unrelated browser windows. Instead, it cleans up the stale session record and creates a fresh one.

### Quick Reference: All Session Commands

| Action | CLI Command | Key Parameters |
|---|---|---|
| Environment setup | `browsectl setup` | `--browser`, `--check-only` |
| Start driver | `browsectl driver-start` | *(none)* |
| Check driver | `browsectl status` | *(none)* |
| Create session | `browsectl session-create` | `--headless`, `--copy-data`, `--foreground` |
| List sessions | `browsectl session-list` | *(none)* |
| Switch session | `browsectl session-use` | `--session` (required) |
| Delete session | `browsectl session-delete` | `--session` (optional) |
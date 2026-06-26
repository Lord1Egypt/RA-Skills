---
name: clawdcursor
version: 0.7.5
description: >
  OS-level desktop automation tool server. 42 tools for controlling any application
  on Windows, macOS, and Linux. Model-agnostic — works with any AI that can do
  function calling via REST or MCP (Claude, GPT, Gemini, Llama, Mistral, or plain HTTP).
  No built-in LLM in serve/mcp mode. You are the brain. ClawdCursor is the hands.
homepage: https://clawdcursor.com
source: https://github.com/AmrDab/clawdcursor
privacy: >
  All processing runs locally. Server binds to 127.0.0.1 only — not network-accessible.
  No telemetry, no analytics. Screenshots stay in memory. In agent mode (start),
  screenshots/text are sent only to the user's configured AI provider.
metadata:
  openclaw:
    requires: {}
    install:
      - npm install -g clawdcursor
      - clawdcursor consent --accept
      - clawdcursor serve
    skill_dir: ~/.openclaw/workspace/skills/clawdcursor
---

**If a human can do it on a screen, you can too.** No API? No integration? No problem.

> **USE AS A FALLBACK — NOT FIRST CHOICE**
>
> Before reaching for any ClawdCursor tool, ask:
> 1. Is there a native API? (Gmail API, GitHub API, Slack API) → **use the API**
> 2. Is there a CLI? (`git`, `npm`, `curl`) → **use the CLI**
> 3. Can you edit the file directly? → **do that**
> 4. Is there a browser automation layer? (Playwright, Puppeteer) → **use that**
>
> **None of the above work? Now use ClawdCursor.** It's for the last mile.

---

## Modes at a Glance

| Mode | Command | Brain | Tools available |
|------|---------|-------|----------------|
| `serve` | `clawdcursor serve` | **You** (REST client) | All 42 tools via HTTP |
| `mcp` | `clawdcursor mcp` | **You** (MCP client) | All 42 tools via MCP stdio |
| `start` | `clawdcursor start` | Built-in LLM pipeline | All 42 tools + autonomous agent |

In `serve` and `mcp` modes: **you reason, ClawdCursor acts.** There is no built-in LLM. You call tools, interpret results, decide next steps.

---

## Connecting

### Option A — REST (`clawdcursor serve`)

```bash
clawdcursor serve        # starts on http://127.0.0.1:3847
```

All POST endpoints require: `Authorization: Bearer <token>` (token saved to `~/.clawdcursor/token`)

```
GET  /tools              → all tool schemas (OpenAI function-calling format)
POST /execute/{name}     → run a tool: {"param": "value"}
GET  /health             → {"status":"ok","version":"0.7.5"}
GET  /docs               → full documentation
```

Example:
```
POST /execute/get_windows     {}
POST /execute/mouse_click     {"x": 640, "y": 400}
POST /execute/type_text       {"text": "hello world"}
```

If the server isn't running, start it yourself — don't ask the user:
```bash
clawdcursor serve
# wait 2 seconds, then verify: GET /health
```

### Option B — MCP (`clawdcursor mcp`)

```json
{
  "mcpServers": {
    "clawdcursor": {
      "command": "clawdcursor",
      "args": ["mcp"]
    }
  }
}
```

Works with Claude Code, Cursor, Windsurf, Zed, or any MCP-compatible client. All 42 tools are exposed identically.

### Option C — Autonomous agent (`clawdcursor start`)

```
POST /task    {"task": "Open Notepad and write Hello"}   → submit task
GET  /status  → {"status": "acting"} | "idle" | "waiting_confirm"
POST /confirm {"approved": true}                         → approve safety-gated action
POST /abort                                              → stop current task
```

Use `delegate_to_agent` tool to submit tasks from within MCP/REST sessions. Requires `clawdcursor start` running on port 3847.

**Polling pattern:**
```
POST /task  {"task": "...", "returnPartial": true}
→ poll GET /status every 2s:
    "acting"           → still running, keep polling
    "waiting_confirm"  → STOP. Ask user → POST /confirm {"approved": true}
    "idle"             → done, check GET /task-logs for result
→ if 60s+ with no progress: POST /abort, retry with simpler phrasing
```

**returnPartial mode** — send `{"returnPartial": true}` with POST /task:
ClawdCursor skips Stage 3 (expensive vision) and returns control to you if Stage 2 fails:
```json
{"partial": true, "stepsCompleted": [...], "context": "got stuck on dialog"}
```
You finish the task with MCP tools, then call POST /learn to save what worked.

**POST /learn — adaptive learning:**
After completing a task with your own tool calls, teach ClawdCursor for next time:
```json
POST /learn
{
  "processName": "EXCEL",
  "task": "create table with headers",
  "actions": [
    {"action": "key", "description": "Ctrl+Home to go to A1"},
    {"action": "type", "description": "Type header name"},
    {"action": "key", "description": "Tab to next column"}
  ],
  "shortcuts": {"next_cell": "Tab", "next_row": "Enter"},
  "tips": ["Use Tab between columns, Enter between rows"]
}
```
This enriches the app's guide JSON. Stage 2 reads it on the next run — no vision fallback needed.

---

## The Universal Loop

Every GUI task follows the same pattern regardless of transport:

```
1. ORIENT  →  read_screen() or get_windows()          see what's open and focused
2. ACT     →  smart_click() / smart_type() / key_press()   do the thing
3. VERIFY  →  check return value → window state → text check → screenshot
4. REPEAT  →  until done
```

### Verification (cheapest to most expensive)

1. **Tool return value** — every tool reports success/failure. Check it first.
2. **Window state** — `get_active_window()`, `get_windows()` — did a dialog appear? Did the title change?
3. **Text check** — `read_screen()` or `smart_read()` — is the expected text visible?
4. **Screenshot** — `desktop_screenshot()` — only when text methods fail. Costs the most.
5. **Negative check** — look for error dialogs, wrong window, unchanged screen.

**Always verify** after: sends, saves, deletes, form submissions.
**Skip verification** for: mid-sequence keystrokes, scrolling.

---

## Tool Decision Trees

### Perception — always start here

```
read_screen()          → FIRST. Accessibility tree: buttons, inputs, text, with coords.
                          Fast, structured, works on native apps.
ocr_read_screen()      → When a11y tree is empty (canvas UIs, image-based apps).
smart_read()           → Combines OCR + a11y. Good first call when unsure.
desktop_screenshot()   → LAST RESORT. Only when you need pixel-level visual detail.
desktop_screenshot_region(x,y,w,h) → Zoomed crop when you need detail in one area.
```

### Clicking

```
smart_click("Save")              → FIRST. Finds by label/text via OCR + a11y, clicks.
                                   Pass processId to target the right window.
invoke_element(name="Save")      → When you know the exact automation ID from read_screen.
cdp_click(text="Submit")         → Browser elements. Requires cdp_connect() first.
mouse_click(x, y)                → LAST RESORT. Raw coordinates from a screenshot.
```

### Typing

```
smart_type("Email", "user@x.com")  → FIRST. Finds field by label, focuses, types.
cdp_type(label="Email", text="…")  → Browser inputs. Requires cdp_connect() first.
type_text("hello")                 → Clipboard paste into whatever is focused.
                                     Use after manually focusing with smart_click.
```

### Browser / CDP

```
1. navigate_browser(url)     → opens URL, auto-enables CDP
2. cdp_connect()             → connect to browser DevTools Protocol
3. cdp_page_context()        → list interactive elements on page
4. cdp_read_text()           → extract DOM text (returns empty on canvas apps → use OCR)
5. cdp_click(text="…")       → click by visible text
6. cdp_type(label, text)     → fill input by label
7. cdp_evaluate(script)      → run JavaScript in page context
8. cdp_scroll(direction, px) → scroll page via DOM (not mouse wheel)
9. cdp_list_tabs()           → list all open tabs
10. cdp_switch_tab(target)   → switch to a specific tab
```

If CDP isn't connected, switch tabs with keyboard:
```
key_press("ctrl+1")          → tab 1
key_press("ctrl+tab")        → next tab
key_press("ctrl+shift+tab")  → previous tab
```

### Window Management

```
get_windows()                         → list all open windows (use to find PIDs)
get_active_window()                   → what's in the foreground right now
focus_window(processName="Discord")   → bring to front (auto-minimizes phantom off-screen windows)
minimize_window(processName="calc")   → minimize a window — 1 call, cross-platform
                                        also accepts: processId, title
```

**Rule:** Always `focus_window()` before `key_press()` or `type_text()`. Keystrokes go to whatever has focus — if that's your terminal, not the target app.

### Canvas apps (Google Docs, Figma, Notion)

DOM has no readable text. Pattern:
```
ocr_read_screen()          → read content (DOM extraction fails)
mouse_click(x, y)          → click into the canvas area
type_text("your text")     → clipboard paste works even on canvas
```

---

## Quick Patterns

**Open app and type:**
```
open_app("notepad") → wait(2) → smart_read() → type_text("Hello") → smart_read()
```

**Read a webpage:**
```
navigate_browser(url) → wait(3) → cdp_connect() → cdp_read_text()
```

**Fill a web form:**
```
cdp_connect() → cdp_type("Email", "x@x.com") → cdp_type("Password", "…") → cdp_click("Submit")
```

**Cross-app copy/paste:**
```
focus_window("Chrome") → key_press("ctrl+a") → key_press("ctrl+c")
→ read_clipboard() → focus_window("Notepad") → type_text(clipboard)
```

**Send email via Outlook:**
```
open_app("outlook") → wait(2) → smart_click("New Email")
→ mouse_click(to_field_x, to_field_y) → type_text("recipient@x.com") → key_press("Tab")
→ mouse_click(subject_x, subject_y) → type_text("Subject") → key_press("Tab")
→ mouse_click(body_x, body_y) → type_text("Body text")
→ mouse_click(send_x, send_y)
```

**Autonomous complex task (requires `clawdcursor start`):**
```
delegate_to_agent("Open Gmail, find latest email from Stripe, forward to billing@x.com")
→ poll GET /status every 2s
→ if waiting_confirm: ask user → POST /confirm {"approved": true}
→ if idle: task done
```

---

## Full Tool Reference (42 tools)

Speed: ⚡ Free/instant · 🔵 Cheap · 🟡 Moderate · 🔴 Vision (expensive)

### Perception (6)
| Tool | What it does | When |
|------|-------------|------|
| `read_screen` | A11y tree — buttons, inputs, text, coords | ⚡ Default first read |
| `smart_read` | OCR + a11y combined | 🔵 When unsure which to use |
| `ocr_read_screen` | Raw OCR text with bounding boxes | 🔵 Canvas UIs, empty a11y trees |
| `desktop_screenshot` | Full screen image (1280px wide) | ⚡ Last resort visual check |
| `desktop_screenshot_region` | Zoomed crop of specific area | ⚡ Fine-grained visual detail |
| `get_screen_size` | Screen dimensions and DPI | ⚡ Coordinate calculations |

### Mouse (7)
| Tool | What it does | When |
|------|-------------|------|
| `smart_click` | Find element by text/label, click | 🔵 First choice for clicking |
| `mouse_click` | Left click at (x, y) | ⚡ Last resort |
| `mouse_double_click` | Double click at (x, y) | ⚡ Open files, select words |
| `mouse_right_click` | Right click at (x, y) | ⚡ Context menus |
| `mouse_hover` | Move cursor without clicking | ⚡ Hover menus |
| `mouse_scroll` | Scroll at position (physical mouse wheel) | ⚡ Scroll content |
| `mouse_drag` | Drag from start to end — accepts `startX/startY/endX/endY` or `x1/y1/x2/y2` | ⚡ Resize, select ranges |

### Keyboard (5)
| Tool | What it does | When |
|------|-------------|------|
| `smart_type` | Find input by label, focus it, type | 🔵 First choice for form fields |
| `type_text` | Clipboard paste into focused element | ⚡ After manually focusing |
| `key_press` | Send key combo (`ctrl+s`, `Return`, `alt+tab`) | ⚡ After focus_window |
| `shortcuts_list` | List keyboard shortcuts for current app | ⚡ Before reaching for mouse |
| `shortcuts_execute` | Run a named shortcut (fuzzy match) | ⚡ Save, copy, paste, undo |

### Window Management (5)
| Tool | What it does | When |
|------|-------------|------|
| `get_windows` | List all open windows with PIDs and bounds | ⚡ Situational awareness |
| `get_active_window` | Current foreground window | ⚡ Check current focus |
| `get_focused_element` | Element with keyboard focus | ⚡ Debug wrong-field typing |
| `focus_window` | Bring window to front (auto-clears off-screen phantoms) | ⚡ Always before key_press |
| `minimize_window` | Minimize by processName, processId, or title | ⚡ Clear focus stealers |

### UI Elements (2)
| Tool | What it does | When |
|------|-------------|------|
| `find_element` | Search UI tree by name or type | ⚡ Find automation IDs |
| `invoke_element` | Invoke element by automation ID or name | ⚡ When ID known from read_screen |

### Clipboard (2)
| Tool | What it does | When |
|------|-------------|------|
| `read_clipboard` | Read clipboard text | ⚡ After copy operations |
| `write_clipboard` | Write text to clipboard | ⚡ Before paste operations |

### Browser / CDP (11)
| Tool | What it does | When |
|------|-------------|------|
| `cdp_connect` | Connect to browser DevTools Protocol | ⚡ First step for any browser task |
| `cdp_page_context` | List interactive elements on page | ⚡ After connect |
| `cdp_read_text` | Extract DOM text | ⚡ Read page content |
| `cdp_click` | Click by CSS selector or visible text | ⚡ Browser clicks |
| `cdp_type` | Type into input by label or selector | ⚡ Browser form filling |
| `cdp_select_option` | Select dropdown option | ⚡ Select elements |
| `cdp_evaluate` | Run JavaScript in page context | ⚡ Custom queries |
| `cdp_scroll` | Scroll page via DOM (`direction`, `amount` px) | ⚡ DOM-level scroll |
| `cdp_wait_for_selector` | Wait for element to appear | ⚡ After navigation/AJAX |
| `cdp_list_tabs` | List all browser tabs | ⚡ When on wrong tab |
| `cdp_switch_tab` | Switch to a tab by title or index | ⚡ After cdp_list_tabs |

### Orchestration (4)
| Tool | What it does | When |
|------|-------------|------|
| `open_app` | Launch application by name | ⚡ First step for desktop tasks |
| `navigate_browser` | Open URL (auto-enables CDP) | ⚡ First step for browser tasks |
| `wait` | Pause N seconds | ⚡ After opening apps, let UI render |
| `delegate_to_agent` | Send task to built-in autonomous agent | 🟡 Complex multi-step tasks (requires `clawdcursor start`) |

---

## Provider Setup (agent mode only)

| Provider | Setup | Cost |
|----------|-------|------|
| **Ollama** (local) | `ollama pull qwen2.5:7b && ollama serve` | $0 — fully offline, no data leaves machine |
| **Any cloud** | Set env var: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `MOONSHOT_API_KEY`, etc. | Varies |
| **OpenClaw users** | Auto-detected from `~/.openclaw/agents/main/auth-profiles.json` | No extra setup |

Run `clawdcursor doctor` to auto-detect and validate providers.

---

## Security

- **Network isolation:** Binds to `127.0.0.1` only. Verify: `netstat -an | findstr 3847` — should show `127.0.0.1:3847`, never `0.0.0.0:3847`
- **Ollama:** 100% offline. Screenshots stay in RAM, never leave the machine.
- **Cloud providers:** Screenshots/text sent only to your configured provider. No telemetry, no analytics, no third-party logging.
- **Token auth:** All mutating POST endpoints require `Authorization: Bearer <token>`. Token at `~/.clawdcursor/token`.
- **Safety tiers:** Auto / Preview / Confirm. Agents must **never self-approve Confirm actions**.

---

## Coordinate System

All mouse tools use **image-space coordinates** from a 1280px-wide viewport — matching screenshots from `desktop_screenshot`. DPI scaling is handled automatically. Do not pre-scale coordinates.

---

## Safety

| Tier | Actions | Behavior |
|------|---------|----------|
| 🟢 Auto | Navigation, reading, opening apps | Runs immediately |
| 🟡 Preview | Typing, form filling | Logged |
| 🔴 Confirm | Send, delete, purchase | Pauses — **always ask user first** |

- **Never self-approve Confirm actions.**
- `Alt+F4` and `Ctrl+Alt+Delete` are blocked.
- Server binds to `127.0.0.1` only.
- First run requires explicit user consent for desktop control.

---

## Error Recovery

| Problem | Fix |
|---------|-----|
| Port 3847 not responding | `clawdcursor serve` — wait 2s — `GET /health` |
| 401 Unauthorized | Token changed — read `~/.clawdcursor/token` and use fresh value |
| CDP not available | Chrome must be open. `navigate_browser(url)` auto-enables it. |
| CDP on wrong tab | `cdp_list_tabs()` → `cdp_switch_tab(target)` |
| `focus_window` fails | `get_windows()` to confirm title/processName, then retry |
| `smart_click` can't find element | `read_screen()` for coords → `mouse_click(x, y)` |
| `key_press` goes to wrong window | You skipped `focus_window` — always focus first |
| `cdp_read_text` returns empty | Canvas app — use `ocr_read_screen()` instead |
| Same action fails 3+ times | Try a completely different approach |

---

## Platform Support

| Platform | A11y | OCR | CDP |
|----------|------|-----|-----|
| Windows (x64/ARM64) | PowerShell + .NET UIA | Windows.Media.Ocr | Chrome/Edge |
| macOS (Intel/Apple Silicon) | JXA + System Events | Apple Vision | Chrome/Edge |
| Linux (x64/ARM64) | AT-SPI | Tesseract | Chrome/Edge |

**macOS:** Grant Accessibility in System Settings → Privacy → Accessibility.
**Linux:** `sudo apt install tesseract-ocr` for OCR support.

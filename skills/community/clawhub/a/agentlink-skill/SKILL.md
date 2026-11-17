---
name: agentlink
description: |
  Cloud sandbox capabilities (Browser + Windows Desktop). Proactively use this skill when:
  - User asks to open/visit any URL, view web content, or take web screenshots
  - Need to extract data from websites, scrape information, or read page content
  - Need to fill online forms, log in to websites, click buttons, or perform web interactions
  - User asks to execute code (Python/PowerShell/Shell), run scripts, or install packages
  - Need to operate Windows desktop applications (Notepad, browsers, File Manager, etc.)
  - Need to run commands in an isolated environment, read/write files, or manage processes
  - User asks for automated testing, RPA, or periodic web monitoring
  Even if the user doesn't explicitly mention "sandbox" or "browser", proactively use this skill whenever the task involves web browsing, code execution, or desktop operations.
  Powered by agentlink_sdk (China Mobile AgentLink).
version: 1.2.0
metadata.openclaw:
  requires:
    env:
      - AGENTLINK_API_KEY
    bins:
      - python
    python:
      - agentlink-sdk>=1.0.0
---

# AgentLink Skill

Cloud sandbox via [China Mobile AgentLink](https://ecloud.10086.cn/portal/product/AgentLink), providing two core capabilities:

- **Browser Use** — Browser automation (navigation, screenshots, element interaction, JS execution, shell commands, etc.)
- **Computer Use** — Windows desktop control (PowerShell / Python execution, mouse & keyboard, file operations, process management, etc.)

AgentLink is a cloud-based AI sandbox platform by China Mobile, offering isolated browser and Windows desktop environments controllable via API. Ideal for automated testing, RPA, web scraping, code execution, and more.

- [Product Docs](https://ecloud.10086.cn/op-help-center/doc/category/1501)
- [Console](https://console.ecloud.10086.cn/api/page/AgentLink/web/agentlink/console/#/overview)

## API Key Configuration

This skill requires the `AGENTLINK_API_KEY` environment variable. The SDK reads it automatically — no need to pass it manually in code.

**Get a Key:** Visit [AgentLink Console](https://console.ecloud.10086.cn/api/page/AgentLink/web/agentlink/console/#/overview) → Log in → "Service Management" → Create API Key

**Configuration methods (by priority):**
1. openclaw platform: Enter the API Key in the Skill management page; the platform injects it automatically
2. System environment variable: `export AGENTLINK_API_KEY=your-key` (Linux/Mac) or `set AGENTLINK_API_KEY=your-key` (Windows)
3. `.env` file: Create a `.env` file in the project root with `AGENTLINK_API_KEY=your-key`

> If the environment variable is not set, the SDK raises `ConfigurationError`. Prompt the user to configure it first.

## Quick Start

```python
from agentlink_sdk import AgentLink

# API Key is auto-read from AGENTLINK_API_KEY env var — no need to pass it
with AgentLink() as al:
    # Browser automation (first access to al.browser auto-creates a browser sandbox)
    al.browser.go("https://www.baidu.com")
    al.browser.capture().save("screenshot.png")

    # Windows desktop control (first access to al.desktop auto-creates a Windows sandbox)
    al.desktop.shell("Get-Date")
    al.desktop.capture().save("desktop.png")
# All sandboxes are auto-destroyed when the with-block exits
```

## Core Mechanisms

### Automatic Sandbox Creation

When you first access `al.browser` or `al.desktop`, the SDK **automatically creates** the corresponding sandbox type and caches it for reuse. No need to call `al.create()` manually.

### How Agents Perceive the Sandbox: Getting Results

Agents "see" the sandbox state in two ways:

**1. Accessibility Tree (Recommended — text format, efficient)**

`a11y_tree()` (a11y = abbreviation for "accessibility") returns a **structured text description** of the page/desktop, with each interactive element tagged by a number (`ref` for browser, `label` for desktop). Agents can parse the text to understand page structure and locate elements — no image processing needed.

```
# Example browser a11y_tree output
[ref=1] link "News"
[ref=2] textbox "Search"
[ref=3] button "Search"
```

- Small data size (a few KB), fast transfer, directly understandable by LLMs
- Includes element numbers that can be passed directly to `click("3")` / `fill("2", "content")`
- **Best for: element location, form filling, page structure understanding**

**2. Screenshot (Image format — visual but heavy)**

`capture()` returns a base64-encoded image. The agent needs multimodal capabilities to interpret it.

- Large data size (hundreds of KB ~ several MB), slow transfer
- Requires a multimodal LLM to parse
- **Best for: visual verification, layout checks, showing final results to users**

**Recommended workflow:** `a11y_tree()` to locate elements → perform actions → `capture()` to verify → return result to user

```python
# Efficient workflow example
tree = al.browser.a11y_tree()       # 1. Get text description (fast)
print(tree.text)                    #    Agent parses text to find target element
al.browser.click("3")               # 2. Operate element by ref number
shot = al.browser.capture()         # 3. Screenshot to verify (optional)
shot.save("result.png")             # 4. Save for user to view
```

**Getting command results:** Methods like `shell()` return `ActionResult`. Use `result.text` for text output, `result.success` to check success.

### Sandbox Types

| sandbox_type | Description | Use Cases |
|---|---|---|
| `"browser"` | Linux browser sandbox | Web automation, JS execution, shell commands |
| `"windows"` | Windows desktop sandbox | Desktop control, PowerShell / Python, app operation |

### Return Value Types

| Type | Source | Key Attributes |
|---|---|---|
| `ActionResult` | Most `al.browser.*` / `al.desktop.*` methods | `.success` `.text` `.data` `.error` |
| `Screenshot` | `al.browser.capture()` / `al.desktop.capture()` | `.success` `.image_data` `.save(path)` |
| `SandboxResult` | `al.create()` | `.sandbox_id` `.success` `.error` |
| `ToolResult` | `al.call_tool()` / `al.list_tools()` | `.success` `.text` `.data` `.error` |

### Exception Hierarchy

All exceptions inherit from `AgentLinkError`:

```python
from agentlink_sdk import (
    AgentLinkError,          # Base class
    ConfigurationError,      # Missing API key or config error
    SandboxError,            # Sandbox create/destroy failure
    ToolCallError,           # MCP tool call failure
    TransportError,          # Network/HTTP errors
    AgentLinkTimeoutError,   # Operation timeout
)
```

**Common error handling:**
- `delete()` returns `False` with `inner.exception` in logs: sandbox no longer exists on server (auto-expired), no need to retry
- `ConfigurationError`: check if `AGENTLINK_API_KEY` environment variable is set
- `AgentLinkTimeoutError`: increase `request_timeout` parameter

## Full API Reference

### AgentLink Main Client

```python
from agentlink_sdk import AgentLink

# Initialize (API Key auto-read from AGENTLINK_API_KEY env var)
al = AgentLink()

# Advanced initialization (custom timeout and retries)
al = AgentLink(request_timeout=60, max_retries=3)

# Recommended: use context manager (auto-cleanup sandboxes)
with AgentLink() as al:
    pass

# Reuse an existing sandbox
al = AgentLink(sandbox_id="existing-sandbox-id", sandbox_type="browser")

# Or pass api_key explicitly (overrides env var)
al = AgentLink(api_key="explicit-key")

# Sandbox management
result = al.create(sandbox_type="browser")  # Create browser sandbox → SandboxResult
result = al.create(sandbox_type="windows")  # Create Windows sandbox
print(result.sandbox_id)                    # Get sandbox ID
al.delete(sandbox_id="xxx")                 # Delete sandbox (only sandbox_id needed within same instance)
al.cleanup()                                # Clean up all cached sandboxes
al.close()                                  # Close client (cleanup + close connection)

# List all active sandboxes
sessions = al.list_sessions()               # → List[SandboxSession]
for s in sessions:
    print(s.sandbox_id, s.sandbox_type, s.age_minutes)

# Get preview URL
url = al.get_url(sandbox_id="xxx")
```

### Discovering & Calling MCP Tools (Important)

The SDK wraps common APIs, but sandboxes may have additional MCP tools. Use `list_tools()` to discover all available tools, and `call_tool()` to call any tool directly:

```python
# List all MCP tools in the browser sandbox
from agentlink_sdk.models.sandbox import IMAGE_BROWSER, IMAGE_WINDOWS

result = al.list_tools(IMAGE_BROWSER)
for tool in result.data:
    print(tool["name"], "-", tool.get("description", ""))

# List all MCP tools in the Windows sandbox
result = al.list_tools(IMAGE_WINDOWS)

# Call any MCP tool directly (sandboxId auto-injected)
result = al.call_tool("browser_navigate", IMAGE_BROWSER, {"url": "https://example.com"})
result = al.call_tool("shell_exec", IMAGE_BROWSER, {"command": "ls -la", "timeout": 30})
result = al.call_tool("win_power_shell", IMAGE_WINDOWS, {"command": "Get-Process", "timeout": 30})

# ToolResult return value
print(result.success)    # bool
print(result.text)       # str text result
print(result.data)       # dict/any structured data
print(result.error)      # str error message
```

**Strategy:** When the SDK's wrapped APIs don't cover your needs, first `list_tools()` to discover, then `call_tool()` to invoke.

### BrowserController — Browser Automation

```python
# Navigation
al.browser.go("https://example.com")
al.browser.back()

# Perceive the page (a11y_tree is lightweight & recommended; capture is heavy for visual verification)
tree = al.browser.a11y_tree()                   # Accessibility tree: structured text + element ref numbers (few KB, recommended)
tree = al.browser.a11y_tree(depth=3)            # Limit depth
shot = al.browser.capture()                     # Screenshot: base64 image (hundreds of KB, for visual verification)
shot = al.browser.capture(full_page=True)       # Full page screenshot (including scroll)
shot = al.browser.capture(ref="5", element="button")  # Element screenshot
shot.save("page.png")                           # Save to file

# Element interaction
al.browser.click("5")                           # Click element with ref=5
al.browser.click("5", double_click=True)        # Double click
al.browser.click("5", button="right")           # Right click
al.browser.hover("5")                           # Hover
al.browser.drag("5", "10")                      # Drag and drop
al.browser.fill("5", "input text")              # Type text
al.browser.fill("5", "text", submit=True)       # Type and press Enter
al.browser.fill("5", "text", slowly=True)       # Type character by character
al.browser.select_option("5", ["option1"])      # Dropdown select
al.browser.press_key("Enter")                   # Key press
al.browser.press_key("Tab")

# Batch form filling
al.browser.fill_form([
    {"ref": "1", "type": "textbox", "name": "Username", "value": "admin"},
    {"ref": "2", "type": "checkbox", "name": "Agree", "value": True},
])

# JavaScript execution
result = al.browser.evaluate("() => document.title")      # Execute JS
result = al.browser.evaluate("(el) => el.textContent", ref="5")
result = al.browser.run_code("async (page) => await page.click('button')")

# Tab management
al.browser.tabs("list")                                   # List tabs
al.browser.tabs("new")                                    # New tab
al.browser.tabs("close", index=0)                         # Close tab
al.browser.tabs("select", index=1)                        # Switch tab
al.browser.close_tab()                                    # Close current tab
al.browser.resize(1920, 1080)                             # Resize window

# Dialog handling
al.browser.handle_dialog(True)                            # Accept
al.browser.handle_dialog(False, prompt_text="xxx")        # Dismiss + input

# File upload
al.browser.file_upload(["/path/to/file"])

# Diagnostics
msgs = al.browser.console_messages()                      # Console logs
msgs = al.browser.console_messages(all_messages=True)     # All logs
reqs = al.browser.network_requests()                      # Network requests
reqs = al.browser.network_requests(request_body=True)     # Include request body

# Wait
al.browser.wait_for(time_secs=5)                          # Wait for time
al.browser.wait_for(text="Loaded")                        # Wait for text to appear
al.browser.wait_for(text_gone="Loading")                  # Wait for text to disappear

# Shell commands (execute shell inside browser sandbox)
result = al.browser.shell("ls -la")

# Get sandbox OS info
result = al.browser.get_os()
```

### DesktopController — Windows Desktop Control & Code Execution

```python
# Perceive the desktop (a11y_tree is lightweight & recommended; capture is heavy for visual verification)
tree = al.desktop.a11y_tree()                             # Accessibility tree: window/control text description + label numbers (few KB, recommended)
shot = al.desktop.capture()                               # Desktop screenshot: base64 image (hundreds of KB, for visual verification)
shot.save("desktop.png")

# PowerShell / Python command execution (Code Sandbox capability)
result = al.desktop.shell("Get-Process")                  # PowerShell command
result = al.desktop.shell("Get-Date", timeout=60)
result = al.desktop.shell("python -c 'print(1+1)'")       # Python code execution
result = al.desktop.shell("pip install requests")          # Install Python packages

# Mouse operations
al.desktop.click(pos=[100, 200])                          # Click coordinates
al.desktop.click(label=5)                                 # Click accessibility element
al.desktop.click(label=5, button="right")                 # Right click
al.desktop.move(pos=[100, 200])                           # Move mouse
al.desktop.move(pos=[100, 200], drag_to=[300, 400])       # Drag
al.desktop.type_text("hello world")                       # Keyboard input
al.desktop.hotkey("ctrl+c")                               # Shortcut key
al.desktop.hotkey("alt+f4")
al.desktop.scroll("down")                                 # Scroll
al.desktop.scroll("down", amount=5)

# Application management
al.desktop.launch("notepad.exe")                          # Launch application
al.desktop.app("list")                                    # List windows
al.desktop.app("switch", name="notepad")                  # Switch window
al.desktop.app("resize", name="notepad", width=800, height=600)

# File system
al.desktop.file_system("read", path="C:\\test.txt")       # Read file
al.desktop.file_system("write", path="C:\\test.txt", content="hello")
al.desktop.file_system("list", path="C:\\")               # List directory
al.desktop.file_system("exists", path="C:\\test.txt")     # Check existence
al.desktop.file_system("mkdir", path="C:\\newdir")        # Create directory
al.desktop.file_system("delete", path="C:\\test.txt")     # Delete
al.desktop.file_system("copy", path="a.txt", dest="b.txt")
al.desktop.file_system("move", path="a.txt", dest="b.txt")
al.desktop.file_system("info", path="C:\\test.txt")       # File info
al.desktop.file_system("search", path="C:\\", content="*")

# Clipboard
text = al.desktop.clipboard("get")                        # Read
al.desktop.clipboard("set", content="copy content")       # Write

# Process management
al.desktop.process("list")                                # List processes
al.desktop.process("kill", name="notepad.exe")            # Kill process
al.desktop.process("kill", pid=1234)

# Registry
al.desktop.registry("get", path="HKCU:\\Software\\MyApp")
al.desktop.registry("set", path="HKCU:\\Software\\MyApp", name="key", value="value")
al.desktop.registry("list", path="HKCU:\\Software")
al.desktop.registry("delete", path="HKCU:\\Software\\MyApp", name="key")

# Notification
al.desktop.notify("Title", "Notification message")

# Wait
al.desktop.wait(time_secs=5)                              # Wait for time
al.desktop.wait(text="text")                              # Wait for screen text
al.desktop.wait(text_gone="text")                         # Wait for text to disappear

# Multi-select & batch edit
al.desktop.multi_select([1, 2, 3])
al.desktop.multi_edit([
    {"label": 1, "value": "value1"},
    {"label": 2, "value": "value2"},
])

# Web scraping (embedded browser)
content = al.desktop.scrape()
content = al.desktop.scrape(selector="h1")

# Get sandbox OS info
result = al.desktop.get_os()
```

## Debugging Tips

```python
import logging
from agentlink_sdk import set_log_level

# Enable DEBUG logging to see full MCP request/response
set_log_level(logging.DEBUG)

# Browser diagnostics
msgs = al.browser.console_messages(level="error")         # Error logs only
reqs = al.browser.network_requests(request_body=True, request_headers=True)
```

## Notes

- Use `with AgentLink()` to ensure automatic sandbox cleanup
- First access to `al.browser` / `al.desktop` auto-creates sandboxes — no need for manual `create()`
- Before element interaction, call `a11y_tree()` to get element refs (browser) or labels (desktop)
- `delete()` within the same `al` instance only needs `sandbox_id` — the SDK resolves `image_id` from cache
- `delete()` returning `False` with `inner.exception` in logs means the sandbox was already destroyed on the server — no need to retry
- When wrapped APIs aren't enough, use `list_tools()` to discover + `call_tool()` to call any MCP tool
- Default `request_timeout=30s`, `max_retries=2` — increase for long-running operations

## Agent Usage Guidelines

- Before using this skill, verify that `AGENTLINK_API_KEY` environment variable is configured. If not, prompt the user to obtain and configure it from the AgentLink Console
- **Perception first:** Before operating, use `a11y_tree()` to get element numbers (text, fast) rather than screenshots (images, slow). Use screenshots only for final verification or when the user requests visual output
- **Web operation flow:** `go(url)` to navigate → `a11y_tree()` to get refs → `click(ref)` / `fill(ref, text)` to operate → `capture()` to verify
- **Getting results:** For command execution, use `result.text` for text output and `result.success` to check success; for screenshots, use `shot.save("path")` and return the file path to the user
- Prefer SDK-wrapped APIs (`al.browser.*` / `al.desktop.*`); use `list_tools()` + `call_tool()` only when wrapped APIs are insufficient
- Always use `with AgentLink() as al:` pattern to ensure sandbox resources are auto-released

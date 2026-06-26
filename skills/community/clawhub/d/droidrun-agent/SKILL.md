---
name: droidrun-agent
description: DroidRun Portal HTTP/WebSocket/MCP client. Controls Android devices via HTTP, WebSocket, or MCP server, supporting tap, swipe, screenshot, text input, UI state retrieval and more. Use this skill when the user needs to interact with an Android device running DroidRun Portal.
---

# Droidrun Agent

Provides two async clients (`PortalHTTPClient` and `PortalWSClient`), a configuration helper (`PortalConfig`), and a built-in MCP server for communicating with Android devices running DroidRun Portal. All client methods are `async` and support `async with` context managers.

## Installation

```bash
cd droidrun-agent && uv sync              # core only
cd droidrun-agent && uv sync --extra mcp  # with MCP server support
```

## PortalHTTPClient

Communicates with Portal's HTTP server (default port 8080) using Bearer token authentication.

```python
from droidrun_agent import PortalHTTPClient

async with PortalHTTPClient(base_url="http://192.168.1.100:8080", token="YOUR_TOKEN") as client:
    await client.ping()
    state = await client.get_state_full()
    await client.tap(200, 400)
    png = await client.take_screenshot()
```

### Query Methods (GET)

| Signature | Return Type | Description |
|-----------|-------------|-------------|
| `ping()` | `dict` | Health check, no auth required |
| `get_a11y_tree()` | `dict` | Simplified accessibility tree |
| `get_a11y_tree_full(*, filter: bool = True)` | `dict` | Full accessibility tree, `filter=False` keeps small elements |
| `get_state()` | `dict` | Simplified UI state |
| `get_state_full(*, filter: bool = True)` | `dict` | Full UI state (a11y_tree + phone_state), `filter=False` keeps small elements |
| `get_phone_state()` | `dict` | Phone state info (current app, activity, keyboard status, etc.) |
| `get_version()` | `str` | Portal app version string |
| `get_packages()` | `list[dict]` | List of launchable apps, each containing `packageName`, `label`, etc. |
| `take_screenshot(*, hide_overlay: bool = True)` | `bytes` | Device screenshot as PNG bytes, `hide_overlay=False` to show overlay |

### Action Methods (POST)

| Signature | Return Type | Description |
|-----------|-------------|-------------|
| `tap(x: int, y: int)` | `dict` | Tap screen coordinates |
| `swipe(start_x: int, start_y: int, end_x: int, end_y: int, duration: int \| None = None)` | `dict` | Swipe gesture, `duration` is optional duration in milliseconds |
| `global_action(action: int)` | `dict` | Execute Android accessibility global action (1=Back, 2=Home, 3=Recents) |
| `start_app(package: str, activity: str \| None = None, stop_before_launch: bool = False)` | `dict` | Launch an app |
| `stop_app(package: str)` | `dict` | Best-effort stop an app |
| `input_text(text: str, clear: bool = True)` | `dict` | Input text (auto base64-encoded), `clear=True` clears field first |
| `clear_input()` | `dict` | Clear the focused input field |
| `press_key(key_code: int)` | `dict` | Send Android key code (e.g. 66=Enter, 3=Home, 4=Back) |
| `set_overlay_offset(offset: int)` | `dict` | Set overlay vertical offset in pixels |
| `set_socket_port(port: int)` | `dict` | Update the HTTP server port |

## PortalWSClient

Communicates with Portal's WebSocket server (default port 8081) using JSON-RPC style messages. Automatically reconnects when a method is called on a broken connection.

```python
from droidrun_agent import PortalWSClient

async with PortalWSClient("ws://192.168.1.100:8081", token="YOUR_TOKEN") as ws:
    await ws.tap(200, 400)
    state = await ws.get_state()
    png = await ws.take_screenshot()
    time_ms = await ws.get_time()
```

### Methods

Supports all action methods from PortalHTTPClient (`tap`, `swipe`, `global_action`, `start_app`, `stop_app`, `input_text`, `clear_input`, `press_key`, `set_overlay_offset`, `set_socket_port`, `take_screenshot`) with identical signatures.

Query methods:

| Signature | Return Type | Description |
|-----------|-------------|-------------|
| `get_packages()` | `Any` | List of launchable packages |
| `get_state(*, filter: bool = True)` | `Any` | Full state, `filter=False` keeps small elements |
| `get_version()` | `Any` | Portal version string |
| `get_time()` | `Any` | Device Unix timestamp in milliseconds |
| `install(urls: list[str], hide_overlay: bool = True)` | `Any` | Install APK(s) from URL(s), supports split APKs (WebSocket only) |

WebSocket screenshots automatically parse binary frames and return PNG `bytes` directly.

## Exceptions

All exceptions inherit from `PortalError`:

| Exception | Trigger |
|-----------|---------|
| `PortalError` | Base exception |
| `PortalConnectionError` | Cannot connect to Portal server |
| `PortalAuthError` | Invalid or missing token (HTTP 401/403) |
| `PortalTimeoutError` | Request timed out |
| `PortalResponseError` | Server returned unexpected status or error |

## Full Usage Example

```python
import asyncio
from droidrun_agent import PortalHTTPClient, PortalWSClient

async def demo_http():
    async with PortalHTTPClient("http://localhost:8080", token="YOUR_TOKEN") as client:
        print(await client.ping())
        print("Version:", await client.get_version())
        print("Packages:", len(await client.get_packages()))

        await client.tap(500, 800)
        await client.swipe(500, 1500, 500, 500, duration=300)
        await client.input_text("Hello World")
        await client.press_key(66)  # Enter

        state = await client.get_state_full()
        png = await client.take_screenshot()
        print(f"Screenshot: {len(png)} bytes")

async def demo_ws():
    async with PortalWSClient("ws://localhost:8081", token="YOUR_TOKEN") as ws:
        print("Version:", await ws.get_version())
        print("Time:", await ws.get_time())

        await ws.tap(500, 800)
        await ws.start_app("com.android.settings")

        png = await ws.take_screenshot()
        print(f"Screenshot: {len(png)} bytes")

asyncio.run(demo_http())
asyncio.run(demo_ws())
```

## PortalConfig

Helper dataclass for managing connection settings. Supports direct construction or loading from environment variables.

```python
from droidrun_agent import PortalConfig

# Direct construction
config = PortalConfig(base_url="http://192.168.1.100:8080", token="YOUR_TOKEN")
client = config.create_client()

# Load from environment variables
config = PortalConfig.from_env()
client = config.create_client()
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `base_url` | `str` | (required) | Portal HTTP or WebSocket base URL |
| `token` | `str` | (required) | Bearer authentication token |
| `timeout` | `float` | `10.0` | Request timeout in seconds |
| `transport` | `str` | `"http"` | `"http"` or `"ws"` |

Environment variables for `from_env()`: `PORTAL_BASE_URL`, `PORTAL_TOKEN`, `PORTAL_TIMEOUT`, `PORTAL_TRANSPORT`.

## MCP Server

A built-in MCP (Model Context Protocol) server exposes all Portal operations as tools for AI agent integration. Requires the `mcp` optional dependency (`pip install droidrun-agent[mcp]`).

### Starting the server

```bash
# Via CLI entry point
droidrun-agent --mcp

# Or as a Python module
python -m droidrun_agent --mcp
```

The server reads `PORTAL_BASE_URL`, `PORTAL_TOKEN`, `PORTAL_TIMEOUT`, and `PORTAL_TRANSPORT` from environment variables and communicates over stdio.

### MCP Tools

| Tool | Description |
|------|-------------|
| `portal_ping` | Health check (HTTP only) |
| `portal_tap` | Tap screen coordinates |
| `portal_swipe` | Swipe gesture |
| `portal_screenshot` | Take screenshot, returns PNG image |
| `portal_get_state` | Get simplified UI state |
| `portal_get_state_full` | Get full UI state (a11y tree + phone state) |
| `portal_get_a11y_tree` | Get simplified accessibility tree (HTTP only) |
| `portal_get_a11y_tree_full` | Get full accessibility tree (HTTP only) |
| `portal_get_phone_state` | Get phone state info (HTTP only) |
| `portal_get_version` | Get Portal app version |
| `portal_get_packages` | List launchable packages |
| `portal_global_action` | Execute accessibility global action (1=Back, 2=Home, 3=Recents) |
| `portal_start_app` | Launch an app by package name |
| `portal_stop_app` | Stop an app |
| `portal_input_text` | Input text into focused field |
| `portal_clear_input` | Clear focused input field |
| `portal_press_key` | Send Android key code (66=Enter, 3=Home, 4=Back) |
| `portal_set_overlay_offset` | Set overlay vertical offset |
| `portal_get_time` | Get device timestamp (WebSocket only) |
| `portal_install` | Install APK(s) from URL(s) (WebSocket only) |

### openclaw integration

Register as an openclaw MCP skill:

```json
{
  "mcpServers": {
    "droidrun-agent": {
      "command": "uvx",
      "args": ["--with", "mcp", "droidrun-agent", "--mcp"],
      "env": {
        "PORTAL_BASE_URL": "http://192.168.1.100:8080",
        "PORTAL_TOKEN": "YOUR_TOKEN"
      }
    }
  }
}
```

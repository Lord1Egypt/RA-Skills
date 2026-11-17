---
name: ghost-in-the-droid
description: Control real Android and iOS devices, run apps, take screenshots, and execute on-device inference via Ghost in the Droid MCP server (62 tools).
triggers:
  - mobile automation
  - android
  - ios
  - device control
  - app testing
  - screenshot device
  - tap swipe type on phone
  - on-device inference
  - adb
  - webdriveragent
tags:
  - mobile
  - android
  - ios
  - mcp
  - automation
  - testing
---

# Ghost in the Droid

Ghost in the Droid is an MCP server that gives any LLM agent a real Android or iOS device as its body. 62 tools covering tap, swipe, type, screenshot, screen-tree reading, app launch, camera, TTS, crash reports, batched execution, and on-device inference.

**Install:** `pip install ghost-in-the-droid`
**Repo:** https://github.com/ghost-in-the-droid/android-agent

## When to use this skill

Use Ghost in the Droid when the user wants to:
- Control an Android phone or tablet via ADB
- Control an iPhone or iPad via WebDriverAgent
- Take screenshots of a real device screen
- Tap, swipe, type, or scroll on a device
- Launch or interact with mobile apps
- Run on-device inference (llama.cpp, MediaPipe, MLX)
- Automate mobile workflows end-to-end
- Spin up Android emulators via Docker+KVM pools

## Setup

### 1. Install the MCP server

```bash
pip install ghost-in-the-droid
```

### 2. Add to your MCP config

For Claude Code (`~/.claude/claude_code_config.json`):

```json
{
  "mcpServers": {
    "ghost-in-the-droid": {
      "command": "python",
      "args": ["-m", "ghost_in_the_droid"]
    }
  }
}
```

For OpenClaw:
```bash
openclaw mcp add ghost-in-the-droid --command "python -m ghost_in_the_droid"
```

### 3. Android prerequisites

```bash
# Install ADB
sudo apt install android-tools-adb   # Linux
brew install android-platform-tools  # macOS

# Connect device (USB or TCP)
adb devices
```

### 4. iOS prerequisites

WebDriverAgent must be installed and running on the target device. See the [iOS setup guide](https://github.com/ghost-in-the-droid/android-agent/blob/main/docs/ios/SETUP.md).

## Core tool reference

### Screen interaction
| Tool | What it does |
|---|---|
| `tap` | Tap at coordinates or element |
| `swipe` | Swipe between two points |
| `type_text` | Type text into focused field |
| `press_key` | Press a key (HOME, BACK, ENTER, etc.) |
| `scroll` | Scroll up/down/left/right |
| `long_press` | Long press at coordinates |

### Screen reading
| Tool | What it does |
|---|---|
| `screenshot` | Capture device screen as image |
| `screen_tree` | Get UI accessibility tree (for clicking elements by label) |
| `find_element` | Find element by text, id, or class |
| `get_screen_text` | OCR-extract all visible text |

### App management
| Tool | What it does |
|---|---|
| `launch_app` | Launch app by package name |
| `close_app` | Close app |
| `install_apk` | Install APK from path or URL |
| `list_apps` | List installed apps |
| `clear_app_data` | Clear app storage |

### Device info
| Tool | What it does |
|---|---|
| `list_devices` | List connected ADB devices |
| `device_info` | Get device model, OS, battery, etc. |
| `get_clipboard` | Read device clipboard |
| `set_clipboard` | Write to device clipboard |

### On-device inference
| Tool | What it does |
|---|---|
| `run_llm` | Run inference via llama.cpp on-device |
| `run_mediapipe` | Run MediaPipe model on-device |
| `run_mlx` | Run MLX model (iOS/macOS) |

### Emulators (Docker+KVM)
| Tool | What it does |
|---|---|
| `create_emulator` | Spin up new Android emulator |
| `list_emulators` | List running emulator pool |
| `destroy_emulator` | Tear down emulator instance |

### Batching
| Tool | What it does |
|---|---|
| `run_flow` | Execute a sequence of actions as one atomic batch |
| `run_skill` | Replay a saved skill (recorded interaction) |

## Usage patterns

### Take a screenshot and describe what you see
```
1. Call screenshot → get base64 PNG
2. Pass to vision model for description
```

### Find and tap a button by label
```
1. Call screen_tree → get accessibility tree
2. Find element with target label
3. Call tap with element bounds
```

### Automate a login flow
```
1. launch_app("com.example.app")
2. screenshot → verify login screen
3. tap(username_field)
4. type_text("user@example.com")
5. tap(password_field)
6. type_text("password")
7. tap(login_button)
8. screenshot → verify logged in
```

### Multi-device targeting
Always use `device_id` parameter to target a specific device when multiple are connected:
```
tap(x=100, y=200, device_id="emulator-5554")
screenshot(device_id="R3CN20ABCDE")
```

## Tips

- Always call `list_devices` first to confirm devices are connected
- Use `screen_tree` over coordinate-based tapping when possible — it survives resolution changes
- `run_flow` is much faster than individual tool calls for scripted sequences
- For iOS, WebDriverAgent must be already running on the target device before using any iOS tools
- On-device inference tools require the model to be pre-loaded on device; call `run_llm` with a `load` action first

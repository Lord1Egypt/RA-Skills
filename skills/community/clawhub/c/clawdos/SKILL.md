---
name: clawdos
description: "Windows automation via Clawdos API: screen capture, mouse/keyboard input, window management, file-system operations, and shell command execution. Standalone CLI execution via Python script. Use when the user wants to control or inspect a Windows host remotely."
license: "MIT"
metadata:
  openclaw:
    version: "2.1.1"
    display_name: "Windows Execution Interface for OpenClaw"
    author: "DANZIG MOE"
    emoji: "🐾"
    python_requires: ">=3.10"
    dependencies:
      - "requests>=2.28.0"
    requires:
      env:
        - "CLAWDOS_BASE_URL"
        - "CLAWDOS_API_KEY"
        - "CLAWDOS_TIMEOUT"
        - "CLAWDOS_FS_ROOT_ID"
    primaryEnv: "CLAWDOS_API_KEY"
    config_schema:
      base_url:
        type: "string"
        default: "http://127.0.0.1:17171"
        description: "Clawdos Windows host service address"
      api_key:
        type: "string"
        required: true
        description: "Clawdos API key"
      timeout:
        type: "integer"
        default: 30
        description: "Request timeout in seconds"
      fs_root_id:
        type: "string"
        description: "Sandbox root directory ID for file system operations"
---

# Clawdos

## Overview

This skill exposes a CLI wrapper around the Clawdos REST API, allowing you to operate a Windows machine securely from OpenClaw via shell commands.
Instead of loading tools, use `exec` to call the standalone python script `scripts/clawdos.py`.

### ⚠️ SECURITY & SANDBOX MECHANISM

**File System Sandbox Protection:**
- All file system operations (`fs_list`, `fs_read`, `fs_write`, `fs_delete`, `fs_move`) are **restricted to a sandboxed root directory** on the Windows host.
- The sandbox root is configured via the `CLAWDOS_FS_ROOT_ID` environment variable and enforced server-side.
- **The Clawdos service prevents access to files outside the designated sandbox directory.** Path traversal attempts (e.g., `../../../`) are blocked.
- This isolation ensures that skill operations cannot accidentally or intentionally access sensitive system files, user documents, or configuration outside the permitted scope.

**Network Isolation:**
- The Clawdos service only communicates with the configured `CLAWDOS_BASE_URL` and does not establish unauthorized external connections.
- All API calls are authenticated via `CLAWDOS_API_KEY` and encrypted over HTTPS when applicable.

### ⚠️ AUTHORIZATION & CAPABILITY WARNINGS

This skill grants access to **powerful Windows automation capabilities**. Users must explicitly understand and authorize the following operations:

1. **Shell Command Execution** (`shell_exec`)
   - Can execute arbitrary PowerShell or cmd commands on the Windows host.
   - Even within the sandbox, commands can potentially modify system state, install software, or alter configurations.
   - **Only use with trusted sources and explicit user approval.**

2. **File Deletion** (`fs_delete`)
   - Permanently removes files and directories within the sandbox.
   - No recovery mechanism exists once deleted.
   - **Exercise extreme caution; confirm deletion intent before execution.**

3. **File Upload/Download** (`--file`, `--out`)
   - The CLI script can read local files and upload them to the Windows host (within sandbox).
   - The script can download remote files from the Windows host to the agent system.
   - **Do not use with sensitive files or untrusted remote systems.**

4. **Persistent Screen/Window Monitoring**
   - Visual actions (`screen_capture`, `window_list`, `window_focus`) can observe active GUI content.
   - If sensitive information is visible on screen, it may be captured.

### ⚠️ Requirements
**This skill requires a corresponding server running on your Windows host.**
Ensure the Windows host is running `danzig233/clawdos`. The connection parameters (`CLAWDOS_BASE_URL` and `CLAWDOS_API_KEY`) must be configured via OpenClaw's skill configuration UI or environment variables, as specified in this file's metadata.

## Usage

You interact with Clawdos by running the `scripts/clawdos.py` CLI using the `exec` tool. The script will automatically pick up the `CLAWDOS_BASE_URL` and `CLAWDOS_API_KEY` environment variables injected by OpenClaw.

**Basic Syntax:**
```bash
python3 ~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/clawdos/scripts/clawdos.py <action> --args '{"key":"value"}'
```

### Available Actions

#### 1. Visual Navigation & System Check
- `health`: Check service status.
- `get_env`: Get screen resolution, DPI scale, and active window.
- `window_list`: List all open windows.
- `window_focus`: Focus a window. Args: `{"titleContains": "..."}` or `{"processName": "..."}`
- `screen_capture`: Take a screenshot. Use `--out path/to/save.png` to save binary. Args: `{"format": "png", "quality": 80}`

#### 2. Precise Input (Mouse & Keyboard)
*(Prioritize keyboard/shell when possible to avoid visual estimation errors)*
- `click`: Click the mouse. Args: `{"x": 100, "y": 200, "button": "left"}`
- `move`: Move cursor. Args: `{"x": 100, "y": 200}`
- `drag`: Drag mouse. Args: `{"fromX": 100, "fromY": 200, "toX": 300, "toY": 400}`
- `keys`: Press key combos. Args: `{"combo": ["ctrl", "c"]}`
- `type_text`: Type text. Args: `{"text": "hello"}`
- `scroll`: Scroll wheel. Args: `{"amount": -500}`
- `batch`: Execute multiple input actions sequentially. Args: `{"actions": [...]}`

#### 3. File & System Operations
- `fs_list`: List directory contents. Args: `{"path": "/"}`
- `fs_read`: Read a file (prints raw contents to stdout). Use `--out path/to/save.bin` to save binary files. Args: `{"path": "/hello.txt"}`
- `fs_write`: Write to a file. Args: `{"path": "/hello.txt", "content": "hello world"}`. Or use `--file path/to/local.bin` to upload a local binary file.
- `fs_mkdir`: Create a directory. Args: `{"path": "/newdir"}`
- `fs_delete`: Delete a file or directory. Args: `{"path": "/newdir", "recursive": true}`
- `fs_move`: Move or rename. Args: `{"from": "/src", "to": "/dst"}`
- `shell_exec`: Run a shell command on the Windows host. Args: `{"command": "dir", "args": ["/w"], "workingDir": ""}`

### Operation Strategy

### Operational Best Practices
- **Prefer Keyboard & Shell**: To minimize errors from visual coordinate estimation, prioritize using keyboard shortcuts (`key_combo`, `type_text`) or shell commands (`shell_exec`) over mouse operations whenever possible.
- **Targeted Mouse Usage**: Reserve precise mouse operations (`mouse_click`, `mouse_move`, `mouse_drag`) strictly for necessary UI interactions (e.g., clicking a specific button on a web page, navigating a software interface, or focusing an input field). 
- **Scrolling**: Using `mouse_scroll` is safe and recommended for navigating long pages or documents.

### Security Best Practices
- **Verify File Paths**: Always confirm the target path is within the intended sandbox directory. The server enforces isolation, but double-check paths in scripts.
- **Audit Shell Commands**: Review `shell_exec` commands before execution. Avoid running commands from untrusted sources.
- **File Transfer Restrictions**: Only upload/download files you trust. Do not use `--file` with sensitive credentials or system files.
- **Minimize Screen Captures**: Avoid capturing screens if sensitive information (passwords, tokens, personal data) may be visible.
- **Explicit Deletion Confirmation**: Review the target path carefully before executing `fs_delete`. Deleted files cannot be recovered.

## Examples

**Focus MS Edge and type:**
```bash
python3 scripts/clawdos.py window_focus --args '{"processName": "msedge"}'
python3 scripts/clawdos.py type_text --args '{"text": "https://openclaw.ai\n"}'
```

**Take a screenshot and save it locally:**
```bash
python3 scripts/clawdos.py screen_capture --out /tmp/windows_screen.png --args '{"format":"png"}'
```

**Read a file from Windows:**
```bash
python3 scripts/clawdos.py fs_read --args '{"path": "logs/app.log"}'
```

**Execute PowerShell on Windows:**
```bash
python3 scripts/clawdos.py shell_exec --args '{"command": "powershell", "args": ["-Command", "Get-Process"]}'
```

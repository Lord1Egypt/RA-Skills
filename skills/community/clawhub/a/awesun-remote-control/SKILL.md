---
name: awesun-cli
description: "用于管理 AweSun(向日葵)远程设备的远程控制 CLI 工具。涵盖设备列表管理、远程会话管理、远程桌面控制、远程命令执行、远程文件传输、端口转发以及远程关机/重启/唤醒。适用于 AweSun/向日葵远程控制任务：远程连接、远程桌面、远程设备管理、SSH、远程文件操作、端口转发、远程截图和远程登录"
version: "1.0.6"
author: "Oray"
---

# AweSun Remote Control CLI

`awesun-cli` provides programmatic control for AweSun (向日葵) remote devices, enabling automated device management, desktop GUI interaction, file transfers, remote shell commands, and port forwarding.

## PREREQUISITE INSTALL

```bash
npm install -g @aweray/awesun-cli
```

---

## STANDARD LIFECYCLE (MENTAL MODEL)

Every remote task follows this 5-step lifecycle:

```text
[1. Verify Login]  -->  [2. Resolve Target]  -->  [3. Connect Session]  -->  [4. Execute Ops]  -->  [5. Disconnect]
login status             remote-id / fastcode      session connect --type     desktop/file/exec      session disconnect
```

---

## SCENARIO NAVIGATION & GUIDES

Load the corresponding guide in `references/` on demand based on the user's task scenario:

| Scenario                    | When to Use                                                                        | Primary Commands                                                                              | Reference Guide                                                                   |
| --------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Account & Auth**          | Login, status check, headless URL auth, license check, free trial                  | `login`, `login --url`, `login status`, `logout`, `service info`, `service get-trial`         | `references/account-guide.md`                                                     |
| **Device Management**       | Discover devices, query status, update metadata, manage passwords, remote power    | `device ls`, `device search`, `device info`, `device grant`, `device shutdown/restart/wakeup` | `references/device-guide.md`                                                      |
| **Session & Connection**    | Connect to targets, distinguish `--remote-id` vs `--fastcode`, manage sessions     | `session connect`, `session ls`, `session status`, `session disconnect`                       | `references/connection-guide.md`                                                  |
| **Desktop Automation**      | Mouse clicks, drags, scrolls, typing, keyboard combos, normalized coordinates      | `session screenshot`, `desktop mouse click/move/scroll/drag`, `desktop type/paste/key`        | `references/desktop-guide.md`                                                     |
| **File Management**         | Browse remote files, make folders, rename, delete, async upload/download           | `file ls`, `file mkdir`, `file mv`, `file rm`, `file transfer`, `file transfer status/cancel` | `references/file-guide.md`                                                        |
| **Command Execution & SSH** | Run shell commands on Windows (`cmd`) / Linux (`ssh`), get local SSH proxy address | `session exec`, `ssh address`                                                                 | `references/remote-exec-guide.md`                                                 |
| **Port Forwarding**         | Expose remote service port to local machine via forward tunnel                     | `forward config`                                                                              | `references/port-forwarding-guide.md`                                             |
| **UI Coordinate Locating**  | Visual element locating and normalized (0.0 - 1.0) coordinate conversion           | Pixel-to-normalized conversion helper, UI visual pattern catalog                              | `references/ui-locator.md`, `references/ui-patterns.md`, `scripts/coordinates.py` |

---

## CRITICAL EXECUTION RULES

1. **Authentication Precheck**: Always verify `awesun-cli login status` first. In headless/cloud environments, use `awesun-cli login --url` (see `references/account-guide.md`).
2. **Context & ID Reuse**: Prefer reusing existing `remote_id` and `session_id` from conversation context. Avoid redundant queries.
3. **Target Resolution & Credentials (`--remote-id` vs `--fastcode`)**:
    - `--remote-id <ID>`: Target is in account device list (`device ls`/`search`). Requires **Host Access Password** (访问密码) or OS credentials via `--username <user>`; supports local credential caching via `device grant`.
    - `--fastcode <CODE>`: Target is an unbound device sharing a 9~10 digit code (Fastcode / 识别码). Requires **Verification Code** (验证码).
    - `--fastcode <CODE> --interactive`: **Passwordless connection** where the target user accepts the authorization popup within 60s (NO verification code required; see `references/connection-guide.md`).
4. **Session Type Matching**:
    - `type=desktop`: Required for mouse, keyboard, and screenshot operations.
    - `type=file`: Required for remote directory navigation and file transfer.
    - `type=cmd` (Windows) / `type=ssh` (Linux/Mac): Required for `session exec`.
    - `type=forward`: Required for `forward config`.
5. **File Transfer Rules**:
    - `--local` MUST be an existing local directory (not a file path); original filenames are preserved.
    - Always poll `awesun-cli file transfer status <session_id> --transfer-id <id>` until status reaches `finished`.
6. **Port Forwarding Rules**:
    - Input channels JSON schema only takes `channel_id`, `address`, and `port` (NO `local_port`).
    - Local port is dynamically assigned; read the actual bound port from the returned table (see `references/port-forwarding-guide.md`).

---

## GLOBAL OPTIONS & ENVIRONMENT

- **Output Format**: Use `-o json` (or `table`, `yaml`, `wide`) for machine-readable parsing.
- **Verbose Debugging**: Use `-v` / `--verbose` for detailed request/response logs.
- **Log Location**: `~/awesun-cli/log/`
- **Daemon Lifecycle**: Auto-starts on demand; stop via `awesun-cli stop-daemon`.
- **Cache Clean**: `awesun-cli config clean-cache`

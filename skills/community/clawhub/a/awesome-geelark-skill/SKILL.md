---
name: awesome-geelark-skill
description: Interact with GeeLark Cloud Phone API for managing cloud phones, automation tasks, and social media operations. Use when asked to create cloud phones, manage phones, run automation tasks on TikTok/Instagram/Facebook/YouTube/Reddit, or interact with GeeLark services.
---

# awesome-geeLark-skill

> ⚠️ **EXPERIMENTAL PROJECT**: This skill is designed for AI agents. It contains safety mechanisms but should NOT be used directly in production without testing.

**Configuration**: `assets/config.json` (auto-loads token and base URL)

---

> 🔒 **Security Notice**
>
> **Required Dependencies (not auto-installed):**
> - `adb` (Android Debug Bridge) — must be available in system PATH
> - `uiautomator2` — Python package for device automation
>
> **Credential Handling:**
> - API credentials (token, appId, apiKey) are stored in `assets/config.json`
> - This file is protected by `.gitignore` — **never commit it**
> - Set restrictive permissions: `chmod 600 assets/config.json`
> - **⚠️RPA tasks require third-party account login. We recommend completing login in GeeLark first. Never send account credentials to the agent.**
> - Logs are written to `logs/cloudphone/` — review and mask sensitive data before sharing
>
> **Autonomous Execution:**
> - This skill runs local subprocess commands (`adb`, `glogin`) and accesses API credentials
> - **Do not enable unattended autonomous invocation** until you've validated behavior in a sandbox
> - Always use human confirmation for destructive operations (deletion, RPA with account credentials)
> - **⚠️ RPA tasks require third-party account login. We recommend completing login in GeeLark first. Never send account credentials to the agent.**

---

## First Time Setup

### 1. Install System Dependencies

Ensure `adb` (Android Debug Bridge) is available in your system PATH:

```bash
# macOS
brew install android-platform-tools

# Ubuntu/Debian
sudo apt update && sudo apt install adb

# Windows
# Option 1: Using winget
winget install Google.AndroidSDK
# Option 2: Download Platform Tools from https://developer.android.com/studio/releases/platform-tools
# Extract and add to system PATH manually
```

Verify installation:
```bash
adb version
```

> 💡 **Troubleshooting:** If `adb` is not found after installation, restart your terminal or add it to PATH manually.

### 2. Set Up Python Environment (Recommended)

Use a virtual environment to avoid conflicts with system packages:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install requests uiautomator2
```

> ⚠️ **Alternative (not recommended):** If you must install system-wide:
> ```bash
> pip install requests uiautomator2 --break-system-packages
> ```

### 3. Run Doctor Diagnostic (Recommended)

Before starting cloud phone operations, run the doctor script to verify all dependencies:

```bash
# Basic check (environment, ADB, network, API)
python scripts/doctor.py

# Include phone-specific checks
python scripts/doctor.py --phone-id <phone_id>

# Include uiautomator2 connectivity test
python scripts/doctor.py --phone-id <phone_id> --serial 192.168.1.100:5555

# Output as JSON (for programmatic use)
python scripts/doctor.py --json
```

The doctor checks:
- ✅ Python dependencies (`requests`, `uiautomator2`)
- ✅ ADB installation and device connectivity
- ✅ DNS resolution and GeeLark API reachability
- ✅ API authentication and wallet balance
- ✅ Phone status (if `--phone-id` provided)
- ✅ uiautomator2 connectivity and UI dump (if `--serial` provided)

### 4. Initialize Configuration

```bash
python3 scripts/init_config.py
```

This creates `assets/config.json` with your credentials (protected by `.gitignore`).

All scripts automatically load credentials from this file.
---

## Quick Start

### Basic Usage

#### List Cloud Phones

```python
from scripts.geelark_boot_helper import list_cloud_phones

# Token auto-loads from config
phones = list_cloud_phones()
for phone in phones:
    print(f"{phone['serialName']} - {phone['id']}")
```

#### Boot Cloud Phone and Connect

```python
from scripts.geelark_boot_helper import boot_and_connect

# Token auto-loads from config
adb_info = boot_and_connect("phone_id")
if adb_info:
    print(f"ADB: {adb_info['ip']}:{adb_info['port']}, PWD: {adb_info['pwd']}")
```

---

## Core Workflow

### Step 1: Pre-check (Balance & Cloud Phone Confirmation) ⭐⭐⭐

**Before operating cloud phones:**
1. **Check account balance** - Confirm sufficient balance
2. **Query available cloud phones** - Confirm which phone to operate

```python
from scripts.geelark_client import GeeLarkClient
from scripts.geelark_boot_helper import list_cloud_phones

# Initialize client (auto-loads config)
client = GeeLarkClient(task_name="my_task", phone_id="batch")

# Check balance
wallet = client.wallet()
balance = wallet['data']['balance']
gift_money = wallet['data'].get('giftMoney', 0)

if balance <= 0 and gift_money <= 0:
    print("❌ Insufficient balance! Please recharge.")
    exit(1)

# List phones
phones = list_cloud_phones()
for phone in phones:
    print(f"  {phone['serialName']} (ID: {phone['id']})")
```

### Step 2: Create Cloud Phone

```python
# Create single phone
response = client.call("/open/v1/phone/addNew", {
    "mobileType": "Android 13",
    "data": [{"profileName": "MyPhone"}]
})

# Create multiple phones (requires Pro plan)
response = client.call("/open/v1/phone/addNew", {
    "mobileType": "Android 13",
    "data": [
        {"profileName": "Phone1"},
        {"profileName": "Phone2"}
    ]
})
```

### Step 3: Boot and Enable ADB

```python
from scripts.geelark_boot_helper import boot_and_connect

# This function handles:
# - Balance check
# - Cloud phone status check
# - Start cloud phone (if stopped)
# - Enable ADB (if disabled)
# - Return ADB connection info
# Token auto-loads from config

adb_info = boot_and_connect("phone_id")
```

### Step 4: Install Application ⭐⭐⭐

**Critical**: Must use `appVersionId`, NOT `appName`

#### Option 1: Using install_app.py Script (Recommended)

```bash
# Search and install TikTok (auto-select best match)
python scripts/install_app.py --phone-id <phone_id> --name TikTok

# Exclude TikTok Lite
python scripts/install_app.py --phone-id <phone_id> --name TikTok --exclude Lite

# Install specific version directly
python scripts/install_app.py --phone-id <phone_id> --name Instagram --version-id <appVersionId>
```

#### Option 2: Using API Directly

```python
# Step 1: Find app and get appVersionId
response = client.call("/open/v1/app/installable/list", {
    "envId": "phone_id",
    "name": "TikTok",
    "page": 1,
    "pageSize": 20
})

app_version_id = response['data']['items'][0]['appVersionInfoList'][0]['id']

# Step 2: Install using appVersionId
response = client.call("/open/v1/app/install", {
    "envId": "phone_id",
    "appVersionId": app_version_id
})
```

### Step 5: Manage Session with PhoneManager

**Recommended**: Use `PhoneManager` for session tracking and auto-close.

```python
from scripts.phone_manager import PhoneManager

# Method 1: Context manager (recommended)
with PhoneManager(timeout_minutes=5) as manager:
    manager.start_monitor()
    
    # Connect using phone_id (required)
    d = manager.connect_device("phone_id_123", ip, port, pwd, name="Android15")
    
    # Perform operations
    d(text="Submit").click()
    manager.record_activity("phone_id_123")

# Automatically stops all phones and saves logs on exit

# Method 2: Manual control
manager = PhoneManager(timeout_minutes=5)
manager.start_monitor()
# ... operations ...
manager.stop_all()
manager.client.save_log()
```

---


## Safety Mechanisms

| Mechanism | Description |
|-----------|-------------|
| **Balance Check** | Auto-checks balance before starting cloud phones |
| **Energy Saving** | Auto enables `energySavingMode=1` to reduce costs |
| **Deletion Safeguards** | Anti-automation mechanism: requires interactive terminal, explicit ID + 'YES' confirmation, and enforced delays to prevent scripted or accidental deletion |
| **Auto-Close** | `PhoneManager` auto-closes idle devices |
| **Endpoint Whitelist** | Only documented endpoints can be called |
| **Logging** | All operations logged to `logs/cloudphone/` |

> ⚠️ **Deletion Safety**: AI agents must follow the [Deletion Workflow](#-deletion-workflow-mandatory). The `delete_helper.py` script includes multiple anti-automation safeguards:
> - Interactive terminal verification
> - Input timing validation
> - Mandatory delay before final confirmation
> 
> If the script blocks execution, instruct the user to run manually in their terminal.

---

## Cloudphone Operations

### Prerequisites

- `adb` must be installed and available in PATH (see [First Time Setup](#first-time-setup))
- `uiautomator2` Python package installed (see [Python Environment](#2-set-up-python-environment-recommended))

### uiautomator2 Smoke Test

If uiautomator2 operations seem slow or hang, run the smoke test to identify the bottleneck:

```bash
# Basic connectivity and UI dump test
python scripts/ui_smoke_test.py 192.168.1.100:5555

# Test with app start
python scripts/ui_smoke_test.py 192.168.1.100:5555 --package com.zhiliaoapp.musically

# Custom timeout per step (default: 30s)
python scripts/ui_smoke_test.py 192.168.1.100:5555 --timeout 60

# Output as JSON
python scripts/ui_smoke_test.py 192.168.1.100:5555 --json
```

The smoke test checks each step with individual timeouts:
1. **Connection** - `u2.connect(serial)`
2. **Device Info** - `d.info` (current activity)
3. **UI Hierarchy** - `d.dump_hierarchy()`
4. **App Start** - `d.app_start(package)` (if package provided)

### Agent Workflow ⭐⭐⭐

Since this skill is designed for AI agents that need to recognize the current screen state, the recommended workflow is:

1. **Identify UI Structure**: Use `uiautomator2` to dump the current page hierarchy (`dump_hierarchy()`), enabling the agent to understand the screen layout.
   - Parse the XML hierarchy to locate target elements by `text`, `resource-id`, `content-desc`, or `class`
   - Extract element coordinates (`bounds`) for verification or fallback operations
   - If `dump_hierarchy()` fails or returns empty, proceed to Step 3 immediately

2. **Prioritize uiautomator2 Operations**: If elements can be identified and interacted with via the UI hierarchy, use `uiautomator2` for clicks, inputs, and swipes.
   - **Click**: `d(text="Button").click()` or `d(resourceId="com.example:id/btn").click()`
   - **Input**: `d(text="Username").set_text("hello")`
   - **Swipe**: `d.swipe(x1, y1, x2, y2)` or `d.swipe_ext("up")`
   - **Wait**: `d(text="Expected Text").wait(timeout=10)` before interaction
   - Always verify the element is visible and enabled before interaction

3. **Verify & Retry**: After each operation, execute `dump_hierarchy()` again to confirm the previous action succeeded.
   - Check if the expected UI state changed (e.g., new screen appeared, text updated, dialog dismissed)
   - If verification fails, retry the operation up to 3 times with brief delays (2-3 seconds)
   - If all retries fail, log the error and proceed to Step 4

4. **Fallback to ADB Screenshots**: If elements cannot be recognized or operated via `uiautomator2`, use ADB screenshots to visually confirm the state and perform coordinate-based operations.
   - Capture screenshot: `d.screenshot("/tmp/screen.png")` or via ADB `screencap`
   - Use computer vision or LLM to analyze the screenshot and identify target coordinates
   - Click coordinates: `d.click(x, y)` or `subprocess.run(['adb', '-s', 'device', 'shell', 'input', 'tap', x, y])`
   - Swipe coordinates: `subprocess.run(['adb', '-s', 'device', 'shell', 'input', 'swipe', x1, y1, x2, y2])`
   - **Note**: Coordinate-based operations are less reliable; always prefer uiautomator2 when possible

### Basic Operations

```python
import uiautomator2 as u2
import subprocess

# Connect
d = u2.connect(f"{adb_info['ip']}:{adb_info['port']}")

# Authenticate (MUST DO IMMEDIATELY)
subprocess.run(['adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
                'shell', 'glogin', adb_info['pwd']], capture_output=True)

# Get UI hierarchy (Step 1: Identify)
xml = d.dump_hierarchy()

# Find and click element (Step 2: Prioritize uiautomator2)
d(text="Submit").click()

# Input text
d(text="Username").set_text("hello world")

# Screenshot (Step 3: Fallback)
d.screenshot("/tmp/screen.png")

# Or using ADB
subprocess.run(['adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
                'shell', 'screencap', '-p', '/sdcard/screen.png'])
subprocess.run(['adb', '-s', f"{adb_info['ip']}:{adb_info['port']}",
                'pull', '/sdcard/screen.png', '/tmp/screen.png'])
```

**See**: `references/cloudphone_operations.md` for complete guide.

### Handling Permission Dialogs

After app installation or first launch, Android shows permission/system dialogs. Use the reusable handler to auto-dismiss them:

```python
from scripts.handle_android_permissions import handle_all_dialogs

# Handle all dialogs: permissions (allow/deny) + system dialogs
result = handle_all_dialogs(d, permission_action="allow")
print(f"Handled {result['total']} dialogs")

# Or handle only permission dialogs (deny all)
from scripts.handle_android_permissions import handle_permission_dialogs
handle_permission_dialogs(d, action="deny", max_retries=5)

# Or handle only system dialogs (Not Now, Close, Done, etc.)
from scripts.handle_android_permissions import handle_system_dialogs
handle_system_dialogs(d, max_retries=3)
```

**As a standalone script:**
```bash
# Allow all permissions
python scripts/handle_android_permissions.py 192.168.1.100:5555

# Deny all permissions
python scripts/handle_android_permissions.py 192.168.1.100:5555 --action deny

# Handle up to 10 dialogs
python scripts/handle_android_permissions.py 192.168.1.100:5555 --max-retries 10
```

The handler supports:
- ✅ English: `Allow`, `Allow`, `Don't Allow`, `Don't Allow` (curly quotes)
- ✅ Chinese: `允许`, `同意`, `拒绝`, `取消`, `关闭`
- ✅ System dialogs: `Close`, `Done`, `Not Now`, `稍后`

---

## RPA Tasks

GeeLark provides built-in RPA tasks for 9 platforms:

- TikTok (login, follow, like, comment, edit, delete)
- Instagram (login, publish reels, warmup)
- Facebook (login, publish, auto-comment, active account)
- YouTube (publish short, publish video, active account)
- Reddit (publish image/video, warmup)
- Threads (publish image/video)
- Pinterest (publish image/video)
- X/Twitter (publish)
- Google (login, app download)

**See**: `references/api_reference.md` for complete endpoint list and parameters

---

## Reference Documentation

| Document | Description | When to Read |
|----------|-------------|--------------|
| `references/api_reference.md` | Complete API endpoint list | Need to look up endpoints/parameters |
| `references/error_codes.md` | All error codes and solutions | API call fails |
| `references/best_practices.md` | Safety and performance tips | Planning operations |
| `references/cloudphone_operations.md` | ADB/uiautomator2 guide | Working with device UI |
| `references/auto_close.md` | Auto-close mechanism | Managing idle devices |

---

## Common Error Codes

| Code | Description | Action |
|------|-------------|--------|
| `0` | Success | ✅ |
| `41001` | Balance not enough | Recharge account |
| `42001` | Cloud phone does not exist | Check phone ID |
| `42002` | Cloud phone is not running | Start phone first |

**See**: `references/api_reference.md` for complete list.

---

## Structured Error Codes (Local Scripts)

The following error codes are used by local diagnostic scripts (doctor.py, boot_and_connect(), etc.):

| Error Code | Severity | Description | Quick Fix |
|------------|----------|-------------|-----------|
| `ENV_DEPENDENCY_MISSING` | 🔴 Critical | Python package or system tool not installed | Run doctor: `python scripts/doctor.py` |
| `NETWORK_DNS_FAILED` | 🔴 Critical | Cannot reach GeeLark API | Check DNS, firewall, baseUrl in config |
| `GEELARK_API_FAILED` | 🔴 Critical | API authentication or call failed | Verify token: `python scripts/init_config.py` |
| `PHONE_START_TIMEOUT` | 🟡 Warning | Phone did not start within timeout | Check balance, retry after few minutes |
| `ADB_NOT_FOUND` | 🔴 Critical | ADB not in PATH | Install: `brew install android-platform-tools` |
| `ADB_CONNECT_FAILED` | 🔴 Critical | Cannot connect to ADB device | Start phone first with `boot_and_connect()` |
| `GLOGIN_REQUIRED` | 🔴 Critical | ADB authentication needed | Run: `adb -s <ip:port> shell glogin <pwd>` |
| `UIAUTOMATOR_TIMEOUT` | 🟡 Warning | uiautomator2 operation timed out | Run smoke test: `python scripts/ui_smoke_test.py <serial>` |
| `UIAUTOMATOR_CONNECT_FAILED` | 🔴 Critical | Cannot connect to uiautomator2 | Check ADB connection first |
| `APP_INSTALL_CANDIDATE_AMBIGUOUS` | 🟡 Warning | Multiple app matches found | Use `--exclude` flag or `--version-id` |
| `INSUFFICIENT_BALANCE` | 🔴 Critical | Account balance too low | Recharge via GeeLark dashboard |
| `CONFIG_LOAD_FAILED` | 🔴 Critical | Cannot load config file | Run: `python scripts/init_config.py` |

**See**: `scripts/error_codes.py` for complete list and recommendations.

---

## 🤖 AI Agent Execution Rules

**Critical Directives:**

1. **Pre-flight Check**: Always verify account balance (`wallet()`) before initiating any cloud phone operations.
2. **Identifiers**: Use `phone_id` (UUID) for all API calls, not `serialName`.
3. **RPA Parameter Quirks**:
   - **YouTube**: `video` parameter is a **string**.
   - **Others (IG/FB/Reddit/etc.)**: `video`/`images` parameters are **arrays**.
   - **Instagram**: Field is `Image` (capital I), not `images`.
   - **Facebook**: Login field is `Email`, not `account`.
4. **Lifecycle Management**: You must **stop** a running phone before deleting it (otherwise error 43009).
5. **Auto-Configuration**: Credentials load automatically from `assets/config.json`. Do not pass `token` manually.
6. **Logging**: Always save operation logs to `logs/cloudphone/` upon task completion.
7. **Credential Safety**: Never print or log full API tokens, passwords, or proxy credentials. Use masked versions (e.g., `tok_abc...xyz`) in outputs.
8. **Autonomous Restriction**: Do not invoke RPA tasks with third-party account credentials without explicit human confirmation. Always require approval before executing social media automation that involves login credentials.
9. **⚠️ RPA tasks require third-party account login. You should strongly recommend users complete login in GeeLark first. Never request account credentials from users under any circumstances.**

---

## 🗑️ Deletion Workflow (MANDATORY)

**⚠️ AI agents MUST follow this exact sequence for deletion operations. Never skip steps or auto-execute.**

### Step 1: List Available Phones
```python
from scripts.geelark_boot_helper import list_cloud_phones
phones = list_cloud_phones()
```

### Step 2: Display IDs & Status to User
Output a clear table like:
```
📱 Current Cloud Phones:
| ID (UUID)                              | Name      | Status   |
|----------------------------------------|-----------|----------|
| a1b2c3d4-e5f6-7890-abcd-ef1234567890   | Android13 | Running  |
| b2c3d4e5-f6a7-8901-bcde-f12345678901   | Android15 | Stopped  |
```

### Step 3: Explicitly Ask for Confirmation
Prompt the user with:
```
⚠️ Deletion is permanent and cannot be undone.
Please confirm which phone IDs to delete by replying with the IDs and typing 'YES'.
Example: "Delete a1b2c3d4... YES"
```

### Step 4: 🛑 STOP AND WAIT
**You MUST pause execution and wait for the user's explicit response.**
- Do NOT proceed automatically.
- Do NOT fill in confirmation prompts via heredoc or automation.
- If the user does not reply with explicit confirmation, cancel the operation.

### Step 5: Execute Only After Confirmation
Once the user confirms, run:
```bash
python3 scripts/delete_helper.py
```
Or call the deletion API with explicit `DELETE_CONFIRMED` code.

> 🔒 **Security Rule**: AI agents are **FORBIDDEN** from bypassing confirmation. If you cannot wait for user input, do not attempt deletion. Instruct the user to run `python3 scripts/delete_helper.py` manually.

---

## 🔐 Security Best Practices

### For Human Operators

- **Sandbox First**: Test this skill in an isolated environment (VM/container) before production use
- **Credential Rotation**: Implement regular credential rotation on a scheduled basis. 
- **File Permissions**: Restrict access to `assets/config.json`:
  ```bash
  chmod 600 assets/config.json
  ```
- **Log Review**: Before sharing logs, review `logs/cloudphone/` for sensitive data and redact as needed
- **Dependency Verification**: Verify `adb` and `uiautomator2` are from official sources

### For AI Agents

- **Never** store or transmit credentials outside the `assets/config.json` file
- **Always** confirm with the user before executing operations that involve:
  - Third-party social media account credentials
  - Cloud phone deletion (follow the mandatory Deletion Workflow)
  - Bulk operations affecting multiple devices
- **Never** bypass the double-confirmation mechanism for destructive operations
- **⚠️ RPA tasks require third-party account login. You should strongly recommend users complete login in GeeLark first. Never request account credentials from users under any circumstances.**
- **Deletion Operations**: Always follow the 5-step Deletion Workflow. List IDs → Ask for confirmation → STOP AND WAIT → Execute only after explicit user reply. Never auto-fill or chain deletion commands.

---

**Skill Repository**: https://github.com/GeeLark/awesome-geeLark-skill

**API Documentation**: https://github.com/GeeLark/geelark-openapi

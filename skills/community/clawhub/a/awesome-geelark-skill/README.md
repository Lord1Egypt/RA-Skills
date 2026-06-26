# Awesome GeeLark Skill

> 🚀 GeeLark Cloud Phone API automation for AI agents

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)]()

---

> ⚠️ **WARNING: EXPERIMENTAL PROJECT**
>
> Use this skill with AI agents (OpenClaw, Claude, GPT, etc.) to automate GeeLark Cloud Phone operations. **Do not deploy it in production environments** without thorough testing and validation, or without fully understanding the AI's instruction-following reliability.
>
> - Expect API responses to change without notice.
> - Prepare for manual intervention in some automation flows.
> - Review all operations before execution.
> - Use only after fully understanding the risks.

---

## 📋 Overview

GeeLark Skill provides automation for GeeLark Cloud Phone service, enabling AI agents to manage cloud phones, automate social media apps, and execute RPA tasks across 9 major social platforms.


---

## ✨ Features

- 📱 **Cloud Phone Management** - Create, start, stop, delete cloud phones
- 🔧 **App Automation** - Install, start, stop apps automatically
- 🤖 **RPA Tasks** - Built-in automation for TikTok, Instagram, Facebook, YouTube, Reddit, Threads, Pinterest, X

---

## ⚙️ Requirements

```bash
# Install system dependencies
# macOS:   brew install android-platform-tools
# Ubuntu:  sudo apt install adb

# Install Python dependencies (recommended: use virtual environment)
python3 -m venv .venv
source .venv/bin/activate
pip install requests uiautomator2
```

> 💡 **First time setup?** Run the doctor diagnostic to verify all dependencies:
> ```bash
> python scripts/doctor.py
> ```

---

## 🚀 Quick Start


### Configure Credentials

#### Initialization configuration file

```bash
python3 scripts/init_config.py
```

This creates `assets/config.json` with your credentials (protected by `.gitignore`).

#### Get GeeLark API credentials

1. Visit [GeeLark](https://www.geelark.com/) and register an account
2. Download and log in to GeeLark, switch to the **API** tab, and generate your **API Key** and **Bearer Token**
3. Fill in your **APP ID**, **API Key**, and **Bearer Token** into `config.json`
4. Enter your proxy settings in the **Proxy** field
5. Start managing cloud phones through the agent

### Agent Usage Examples

Once configured, simply tell your AI agent what you want to do:

#### Create a Cloud Phone
```
"Create a new cloud phone with Android 15"
"Create a phone with proxy serial number 10"
```

#### View Your Cloud Phones
```
"Show me all my cloud phones and their status"
```

#### Start and Connect to a Phone
```
"Start phone Android13 and connect to it"
```

#### Install an App
```
"Install TikTok on phone Android13"
```

#### Run RPA Tasks
```
"Run the TikTok warmup task on phone Android13"
"Publish a video to Instagram from phone Android15"
```

#### Manage Multiple Phones
```
"Start 3 phones and install Facebook on all of them"
"Stop all running phones and save logs"
```

The agent handles all the complexity:
- ✅ Balance checking before operations
- ✅ Phone startup and ADB connection
- ✅ App installation with correct parameters
- ✅ Session tracking and auto-close
- ✅ Operation logging and error handling

---

## 📦 Contents

### Scripts

| Script | Purpose |
|--------|---------|
| `doctor.py` | **Diagnostic tool** - Check dependencies, network, ADB, API, and uiautomator2 |
| `ui_smoke_test.py` | **uiautomator2 smoke test** - Test device connectivity with per-step timeouts |
| `install_app.py` | **App installer** - Search and install apps with versionCode sorting and strict candidate matching |
| `handle_android_permissions.py` | **Permission dialog handler** - Auto-dismiss Android permission/system dialogs (curly quotes supported) |
| `error_codes.py` | **Error classification** - Structured error codes with recommendations |
| `geelark_client.py` | Core API client with safety mechanisms |
| `geelark_boot_helper.py` | Boot and ADB connection helper with structured stage output and failDetails reporting |
| `phone_manager.py` | Multi-device management with auto-close |
| `cloudphone_logger.py` | Operation logging with signed URL sanitization |
| `delete_helper.py` | Double-confirmation delete helper |
| `init_config.py` | Configuration initialization |
| `create_phone_profile.py` | Create cloud phones with proxy configuration |
| `utils.py` | Utility functions |

### Reference Documentation

| Document | Description |
|----------|-------------|
| [API Reference](references/api_reference.md) | Complete endpoint list and parameters |
| [Error Codes](references/error_codes.md) | All error codes and solutions |
| [Best Practices](references/best_practices.md) | Safety and performance tips |
| [RPA Tasks](references/rpa_tasks.md) | RPA tasks for 9 platforms |
| [Cloud Phone Operations](references/cloudphone_operations.md) | ADB and uiautomator2 guide |
| [Auto-Close](references/auto_close.md) | Auto-close mechanism |

---

## 🛡️ Safety Mechanisms

| Mechanism | Description |
|-----------|-------------|
| **Balance Check** | Auto-checks balance before starting cloud phones |
| **Energy Saving** | Auto enables `energySavingMode=1` to reduce costs |
| **Deletion Safeguards** | Anti-automation mechanism: requires interactive terminal, explicit ID + 'YES' confirmation, and enforced delays to prevent scripted or accidental deletion |
| **Auto-Close** | `PhoneManager` auto-closes idle devices |
| **Endpoint Whitelist** | Only documented endpoints can be called |
| **Logging** | All operations logged to `logs/cloudphone/` with sensitive data masked |

---

## 🔧 Diagnostic & Testing Tools

### Doctor Diagnostic

Check all dependencies and services before running cloud phone operations:

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

### uiautomator2 Smoke Test

If uiautomator2 operations seem slow or hang, run the smoke test:

```bash
# Test connectivity and UI dump (30s timeout per step)
python scripts/ui_smoke_test.py 192.168.1.100:5555

# Test with app start
python scripts/ui_smoke_test.py 192.168.1.100:5555 --package com.zhiliaoapp.musically

# Custom timeout
python scripts/ui_smoke_test.py 192.168.1.100:5555 --timeout 60
```

### App Installer

Install apps with versionCode sorting and strict candidate matching:

```bash
# Search and install TikTok
python scripts/install_app.py --phone-id <phone_id> --name TikTok

# Exclude TikTok Lite
python scripts/install_app.py --phone-id <phone_id> --name TikTok --exclude Lite

# Install specific version
python scripts/install_app.py --phone-id <phone_id> --name Instagram --version-id <appVersionId>
```

### Permission Dialog Handler

Auto-dismiss Android permission/system dialogs after app install:

```bash
# Allow all permissions
python scripts/handle_android_permissions.py 192.168.1.100:5555

# Deny all permissions
python scripts/handle_android_permissions.py 192.168.1.100:5555 --action deny

# Handle up to 10 dialogs
python scripts/handle_android_permissions.py 192.168.1.100:5555 --max-retries 10
```

---

## ⚠️ Common Error Codes

| Code | Description | Action |
|------|-------------|--------|
| `0` | Success | ✅ |
| `41001` | Balance not enough | Recharge account |
| `42001` | Cloud phone does not exist | Check phone ID |
| `42002` | Cloud phone is not running | Start phone first |

**See**: [Error Codes](references/error_codes.md) for complete list.

---

## 📝 Important Notes

1. **Auto-Configuration**: Scripts automatically load credentials from `assets/config.json`. Please do not fill in sensitive credentials via AI.
2. **Deletion Safety**: Direct delete calls are blocked by default. The system uses `scripts/delete_helper.py` for double confirmation. Ensure your AI agent strictly follows instructions and executes deletions with caution.
3. **Logging**: All operation logs are saved in the `logs/cloudphone/` directory.
4. **Phone ID Storage**: `create_phone_profile.py` now saves phone IDs to `~/.geelark/last_created_phone_id.txt` by default. Use `--output` to customize the path.

---

## 📁 File Structure

```
geelark-api-skill/
├── README.md                # This file
├── SKILL.md                 # Agent usage guide
├── LICENSE                  # Apache License 2.0
├── assets/                  # Configuration files
├── scripts/                 # Python utilities (12 files)
├── references/              # Documentation (6 files)
└── examples/                # Usage examples
```

---

## 🔗 Links

- [GeeLark Official API Docs](https://github.com/GeeLark/geelark-openapi)


## 📄 License

Apache License 2.0


---

**Made with ❤️ and ☕️ by GeeLark**
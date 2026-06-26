---
name: baidu-disk-helper
description: "A tool to manage Baidu Wangpan (Baidu Netdisk) files using the official Baidu Open API. Supports checking quota, listing files, searching, generating download links, and file management (mkdir, rename, move, delete, upload). Requires user API keys and manual authorization."
version: "1.0.0"
license: "MIT"
---

# Baidu Disk Helper (百度网盘) Open API Skill

This skill allows OpenClaw to interact with a user's Baidu Wangpan using the official Baidu Open API.

## ⚠️ Important: Bring Your Own Key (BYOK)
Baidu Netdisk strictly limits API access. **You MUST apply for your own developer keys to use this skill.** The skill uses your keys to run locally and never sends them anywhere else.

### 1. Register a Baidu Developer App
1. Go to the [Baidu Netdisk Open Platform](https://pan.baidu.com/union).
2. Register as a developer and create a new application (Software App / 软件应用).
3. Obtain your **AppKey** (Client ID) and **SecretKey** (Client Secret).

### 2. Tell the Agent to Authenticate
Once you have your keys, tell your OpenClaw agent:
> *"I want to set up Baidu Wangpan. My AppKey is XXX and my SecretKey is YYY."*

The agent will run the setup script and generate a URL for you. Click the URL, log into Baidu, copy the `Authorization Code`, and paste it back to the agent:
> *"Here is my authorization code: ZZZ"*

*Tokens are securely saved in `~/.openclaw/workspace/bwp_config.json`.*

---

## 🚀 Usage Guide for OpenClaw Agents

When the user asks you to interact with Baidu Wangpan, use the `exec` tool to run the following Python commands:

### Setup & Auth
```bash
# Step 1: Generate Auth URL
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py auth --app-key "APP_KEY" --secret-key "SECRET_KEY"

# Step 2: Validate Code
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py auth --code "AUTH_CODE"
```

### Storage & Listing
```bash
# Check Quota
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py quota

# List Files
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py list --dir "/apps"

# Search Files (returns FS_ID)
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py search "keyword" --dir "/"
```

### Download
```bash
# Get Download Link (requires FS_ID from list or search)
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py download "1054668475058405"
```
*Note: Baidu enforces that the download request must include the header `User-Agent: pan.baidu.com`. The script will output an exact `curl` command you can run to download the file.*

### File Management
```bash
# Create Directory
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py mkdir "/apps/my_new_folder"

# Rename File/Directory (newname is just the name, not full path)
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py rename "/apps/old_name.txt" "new_name.txt"

# Move File/Directory
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py move "/apps/file.txt" "/apps/my_new_folder"

# Delete File/Directory (moves to trash)
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py delete "/apps/file_to_delete.txt"
```

### Upload
```bash
# Upload a Single File
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py upload "/local/path/to/file.txt" "/apps/remote_folder"

# Upload an Entire Directory (Uses Multi-Threading for Speed!)
python ~/.openclaw/workspace/skills/baidu-wangpan/scripts/bwp.py upload "/local/path/to/directory" "/apps/remote_folder"
```

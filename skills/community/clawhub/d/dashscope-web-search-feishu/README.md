# web-search-feishu

Real-time web search skill with **Feishu image support** for [OpenClaw](https://github.com/nicepkg/openclaw), powered by [DashScope](https://dashscope.aliyuncs.com/) Qwen API.

Images from search results are automatically uploaded to Feishu and sent as image messages, so they display correctly in Feishu chats.

## Features

- Everything from [web-search](../web-search/) — turbo/deep/agent/think modes, freshness, site filters
- **Feishu image pipeline** — downloads, uploads, and sends images via Feishu API
- **Automatic deduplication** — same image URL is uploaded only once
- **Graceful fallback** — if image upload fails, text still passes through

## Setup

### 1. Install to OpenClaw skills directory

```bash
cp -r web-search-feishu /path/to/openclaw/skills/
```

### 2. Configure DashScope API Key

Get your API key from [DashScope Console](https://dashscope.console.aliyun.com/).

```bash
export DASHSCOPE_API_KEY="sk-your-dashscope-api-key"
```

### 3. Configure Feishu Credentials

Create a Feishu app at [Feishu Open Platform](https://open.feishu.cn/app/) and get your App ID and App Secret.

**Required permissions** (add in Feishu Developer Console):
- `im:message:send_as_bot` — Send messages as bot
- `im:resource` — Upload images

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or add to your shell profile:

```bash
cat >> ~/.bashrc << 'EOF'
export DASHSCOPE_API_KEY="sk-your-dashscope-api-key"
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EOF
source ~/.bashrc
```

> **OpenClaw users**: If your `openclaw.json` already has `channels.feishu.appId` and `channels.feishu.appSecret` configured, the script will auto-detect them as a fallback. No extra env vars needed.

### 4. Install Python dependency

```bash
pip install openai
```

### 5. Update SKILL.md paths

Replace `{{SKILL_DIR}}` with the actual install path:

```bash
cd /path/to/openclaw/skills/web-search-feishu
sed -i "s|{{SKILL_DIR}}|$(pwd)|g" SKILL.md
```

### 6. Restart OpenClaw

```bash
systemctl --user restart openclaw-gateway.service
```

## Usage (via OpenClaw chat on Feishu)

The agent will automatically use this skill when you request image searches on Feishu:

```
搜索一下可爱的猫咪图片
```

You can also invoke it directly:

```
/web-search-feishu cute cats
```

## Usage (standalone CLI)

```bash
# Search with images, send to a Feishu group chat
python3 scripts/web_search.py --images "cute cats" \
  | python3 scripts/feishu_image.py --send --chat-id oc_xxxxx

# Send to a specific user by open_id
python3 scripts/web_search.py --images "cute cats" \
  | python3 scripts/feishu_image.py --send --chat-id ou_xxxxx --id-type open_id

# Just convert URLs to image_keys (no sending)
python3 scripts/web_search.py --images "cute cats" \
  | python3 scripts/feishu_image.py
```

## How to Find Your Chat ID

- **Group chat**: In Feishu, open the group info → copy the Chat ID (starts with `oc_`)
- **User open_id**: Use Feishu API or check OpenClaw logs for the `senderId` field (starts with `ou_`)

## File Structure

```
web-search-feishu/
├── SKILL.md                  # OpenClaw skill definition
├── README.md                 # This file
└── scripts/
    ├── web_search.py         # DashScope search script
    └── feishu_image.py       # Feishu image upload + send pipeline
```

## Requirements

- Python 3.8+
- `openai` Python package
- DashScope API key
- Feishu app with `im:message:send_as_bot` and `im:resource` permissions

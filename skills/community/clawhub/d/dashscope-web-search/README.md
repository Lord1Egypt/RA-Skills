# web-search

Real-time web search skill for [OpenClaw](https://github.com/nicepkg/openclaw), powered by [DashScope](https://dashscope.aliyuncs.com/) Qwen API.

## Features

- **Multiple search strategies**: turbo (fast), deep (thorough), agent (multi-round)
- **Deep thinking mode**: reasoning chain before answering
- **Image search**: text + image mixed output
- **Freshness filter**: restrict to last N days
- **Site restriction**: limit to specific domains
- **Source citations**: results include numbered references

## Setup

### 1. Install to OpenClaw skills directory

```bash
# Copy the skill folder to your OpenClaw skills directory
cp -r web-search /path/to/openclaw/skills/
```

### 2. Configure DashScope API Key

Get your API key from [DashScope Console](https://dashscope.console.aliyun.com/).

Set the environment variable before starting OpenClaw:

```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

Or add it to your shell profile (`~/.bashrc`, `~/.zshrc`):

```bash
echo 'export DASHSCOPE_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Install Python dependency

```bash
pip install openai
```

### 4. Update SKILL.md paths

Open `SKILL.md` and replace all `{{SKILL_DIR}}` with the actual install path:

```bash
# Example: if installed to /home/openclaw/skills/web-search
sed -i 's|{{SKILL_DIR}}|/home/openclaw/skills/web-search|g' SKILL.md
```

### 5. Restart OpenClaw

```bash
systemctl --user restart openclaw-gateway.service
```

## Usage (via OpenClaw chat)

Once installed, the agent will automatically use this skill when you ask questions that need real-time information. You can also invoke it directly:

```
/web-search latest news about AI
```

## Usage (standalone CLI)

```bash
# Quick search
python3 scripts/web_search.py "what is the weather in Beijing"

# Deep research
python3 scripts/web_search.py --deep "compare React vs Vue 2025"

# Image search
python3 scripts/web_search.py --images "cute cats"

# Deep thinking
python3 scripts/web_search.py --think "analyze the impact of AI on education"

# Recent results only
python3 scripts/web_search.py --fresh 7 "breaking news today"

# Restrict to sites
python3 scripts/web_search.py --sites "github.com,stackoverflow.com" "python async tutorial"
```

## File Structure

```
web-search/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
└── scripts/
    └── web_search.py     # Search script
```

## Requirements

- Python 3.8+
- `openai` Python package
- DashScope API key (free tier available)

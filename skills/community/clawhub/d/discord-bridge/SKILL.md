---
name: discord-bridge
description: Bridge Discord messages to Agent Zero's HTTP API
version: 1.0.1
author: Migration from Agent Zero
---

# Discord Bridge Skill

## Overview
Bridges Discord messages to Agent Zero's api_message HTTP endpoint, enabling Discord users to interact with Agent Zero agents.

## Purpose
- Forward Discord messages from specific channels to Agent Zero
- Handle async Discord bot events
- Support command prefix filtering
- Session-based message bridging

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `{{DISCORD_BOT_TOKEN}}` | Discord bot authentication token | Bot token from Discord Developer Portal |
| `{{A0_API_URL}}` | Agent Zero API endpoint | http://localhost:80/api_message |
| `{{A0_API_KEY}}` | Agent Zero API authentication | mcp_server_token from settings |
| `{{DISCORD_CHANNEL_IDS}}` | Comma-separated allowed channel IDs | "123456789,987654321" |
| `{{BOT_CMD_PREFIX}}` | Command prefix for bot commands | "!" |

## Triggers
- Discord `on_message` event
- Filtered by ALLOWED_CHANNEL_SET (if configured)
- Messages containing command prefix for special handling

## APIs & Dependencies
- **discord.py**: Discord bot framework
- **aiohttp**: Async HTTP client for API calls
- **python-dotenv**: Environment variable management

## Files
- `index.py` - Main Discord bot logic
- `.env.example` - Environment template

## Usage
```bash
# Install dependencies
pip install discord.py aiohttp python-dotenv

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the bridge
python index.py
```

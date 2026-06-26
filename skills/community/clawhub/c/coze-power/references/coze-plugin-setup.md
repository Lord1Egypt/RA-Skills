# Coze Plugin Setup Guide

This guide walks you through connecting your Coze bot to the Coze-Power local server.

## Prerequisites

- Coze-Power server running locally (`python3 server.py`)
- A public URL for your local server (ngrok, Cloudflare Tunnel, etc.)
- A Coze account with bot creation access

---

## Step 1: Start the Coze-Power Server

```bash
cd coze-power
# Optional: edit config.json to set your API key and restrictions
python3 server.py
```

You should see:

```
║  🚀 Coze-Power Server v1.0                      ║
║  Listening on: http://0.0.0.0:8899              ║
║  API Key:      coze-power-dev-key               ║
```

## Step 2: Expose to the Internet

### Option A: ngrok (recommended)

```bash
# Install: https://ngrok.com/download
ngrok http 8899
```

Copy the forwarding URL: `https://xxxx.ngrok-free.app`

### Option B: Cloudflare Tunnel

```bash
# Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
cloudflared tunnel --url http://localhost:8899
```

Copy the URL: `https://xxxx.trycloudflare.com`

### Option C: Serveo (no install needed)

```bash
ssh -R 80:localhost:8899 serveo.net
```

## Step 3: Create the Coze Plugin

1. Go to [Coze Studio](https://www.coze.com) → **Plugins** → **Create Plugin**

2. Fill in basic info:
   - **Plugin Name**: `Coze-Power` (or whatever you like)
   - **Description**: `Local machine tools: file, search, command, clipboard, notification`
   - **Plugin Icon**: (optional)

3. Choose **"Import from OpenAPI"**

4. Upload the OpenAPI spec from `coze-power/assets/openapi-spec.json`

5. Configure the server:
   - **Server URL**: Paste your ngrok/cloudflare URL (e.g. `https://xxxx.ngrok-free.app`)
   - **Authentication**: Select "API Key"
     - **Header Name**: `X-API-Key`
     - **API Key**: Your key from `config.json` (default: `coze-power-dev-key`)

6. Click **"Import"** — you should see all tools listed

7. **Save** the plugin

## Step 4: Add Plugin to Your Bot

1. Create or edit your Coze bot
2. Go to the **Plugins** section
3. Find and add your **Coze-Power** plugin
4. **Publish** the bot

## Step 5: Test It

Try these prompts in your bot:

| Prompt | What happens |
|--------|-------------|
| "搜索一下最近AI领域的新闻" | Coze-Power searches the web and returns results |
| "读取我的 ~/Desktop 目录" | Lists files on your desktop |
| "告诉我系统状态" | Returns CPU, disk, memory info |
| "运行 ls -la /home" | Executes the ls command (if allowed) |
| "在桌面上创建一个 test.txt 文件，内容为 Hello from Coze" | Writes a file to your desktop |

## Troubleshooting

### "Plugin not responding"
- Check that ngrok/tunnel is still running
- Verify the server URL in the plugin config matches the ngrok URL
- Test with curl: `curl https://xxxx.ngrok-free.app/health`

### "Invalid API key"
- Check `config.json` for your API key
- Verify the header name is exactly `X-API-Key`

### "Command not allowed"
- Edit `config.json` and add the command to `allowed_commands`
- Restart the server

### "File path not allowed"
- Edit `config.json` and add the path to `allowed_paths`
- Restart the server

## Security Checklist

- [ ] Changed the default API key
- [ ] Restricted `allowed_commands` to only what you need
- [ ] Restricted `allowed_paths` to necessary directories
- [ ] Using HTTPS (ngrok provides this automatically)
- [ ] Server runs only when you need it (start on demand)

## Going Further

Once the basics work, you can:
- Add more tools to `server.py` (check the API reference)
- Use OpenClaw's own API instead of the standalone server for richer agent capabilities
- Set up a permanent tunnel with a custom domain
- Containerize with Docker for isolation

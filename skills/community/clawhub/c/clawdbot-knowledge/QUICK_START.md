# n8n Voice Automation - Quick Start Guide

**Get started in 5 minutes!** 🚀

## Prerequisites

✅ n8n installed and running (local or cloud)
✅ SpeakMCP installed
✅ Python 3.10+

## Step 1: Run Setup Script (30 seconds)

```bash
cd /home/user/DeepAllSpeak/mcp-servers/n8n-mcp-bidirectional
./setup.sh
```

This will:
- ✓ Install Python dependencies
- ✓ Create .env configuration file
- ✓ Display next steps

## Step 2: Get n8n API Key (1 minute)

### For Local n8n:
1. Open **n8n** in browser: http://localhost:5678
2. Click **Settings** (⚙️ icon)
3. Go to **API** section
4. Click **"Create API Key"**
5. **Copy** the generated key

### For n8n Cloud:
1. Open https://cloud.n8n.io
2. Go to **Settings** → **API Keys**
3. Click **"Generate new key"**
4. **Copy** the key

## Step 3: Configure Environment (1 minute)

Edit `.env` file:

```bash
# Open .env file
nano .env

# Replace this line:
N8N_API_KEY=your_n8n_api_key_here

# With your real key:
N8N_API_KEY=n8n_api_abc123xyz789...

# For n8n Cloud, also update:
N8N_BASE_URL=https://your-instance.app.n8n.cloud

# Save: Ctrl+O, Enter, Ctrl+X
```

## Step 4: Add to SpeakMCP (2 minutes)

### Option A: Copy from Template

1. Open `speakmcp-config.json`
2. **Copy** the entire `mcpServers` section
3. Open **SpeakMCP Settings**
4. Paste into **MCP Servers** section
5. **Update** `N8N_API_KEY` with your real key
6. **Update** `cwd` path if needed (Windows: `C:/path/to/...`)

### Option B: Manual Entry

In SpeakMCP Settings, add:

```json
{
  "mcpServers": {
    "n8n-automation": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "cwd": "/home/user/DeepAllSpeak/mcp-servers/n8n-mcp-bidirectional",
      "env": {
        "N8N_API_KEY": "your_real_api_key_here",
        "N8N_BASE_URL": "http://localhost:5678"
      }
    }
  }
}
```

**Important for Windows:**
- Use forward slashes: `C:/path/to/...`
- Or escape backslashes: `C:\\path\\to\\...`

## Step 5: Test It! (1 minute)

1. **Restart SpeakMCP**
2. Press **Ctrl** (voice mode)
3. Say: **"List my n8n workflows"**

### Expected Result:

You should hear SpeakMCP respond with:
- Total number of workflows
- Number of active workflows
- List of workflow names

## 🎉 Success!

If you got a response, you're ready to use voice automation!

---

## Voice Commands to Try

### View Workflows
```
"List my n8n workflows"
"Show me all active workflows"
"What workflows do I have?"
```

### Manage Workflows
```
"Activate workflow [ID or name]"
"Disable workflow [ID or name]"
"Execute workflow [ID or name]"
```

### Get Information
```
"Show me workflow [ID]"
"Get execution history for workflow [ID]"
```

### Create Workflows (Advanced)
```
"Create a workflow that sends me an email every morning at 9 AM"
"Build a workflow that syncs my database to Slack hourly"
```

---

## Troubleshooting

### "Cannot connect to n8n"

**Check:**
1. Is n8n running?
   ```bash
   curl http://localhost:5678/healthz
   ```
2. Is `N8N_BASE_URL` correct in `.env`?
3. Can you access n8n in browser?

**Fix:**
```bash
# Start n8n if not running
n8n start
```

### "Invalid API key"

**Check:**
1. Did you copy the full API key?
2. Did you update both `.env` AND `speakmcp-config.json`?
3. Did you restart SpeakMCP after changes?

**Fix:**
1. Regenerate API key in n8n
2. Update both config files
3. Restart SpeakMCP

### "Voice command not recognized"

**Check:**
1. Is n8n-mcp server running in SpeakMCP?
2. Check SpeakMCP logs for errors
3. Try exact phrases from examples above

**Fix:**
1. Restart SpeakMCP
2. Check server logs: `mcp-servers/n8n-mcp-bidirectional/n8n-mcp.log`

### "Module not found: mcp"

**Fix:**
```bash
cd mcp-servers/n8n-mcp-bidirectional
pip install -r requirements.txt
```

---

## Next Steps

### 📚 Learn More

- **Skill Documentation**: `.claude/skills/n8n-voice-automation/skill.md`
- **Workflow Templates**: `.claude/skills/n8n-voice-automation/templates/workflow_templates.md`
- **MCP Server Details**: `README.md`

### 🔧 Advanced Features

1. **Create Custom Workflows**
   - Use workflow templates
   - Customize with voice commands
   - Deploy directly to n8n

2. **Integration Examples**
   - DeepALL document processing
   - FATONI multi-agent automation
   - Database synchronization
   - Webhook integrations

3. **Monitoring**
   - View execution history
   - Check workflow status
   - Debug with logs

### 💡 Pro Tips

**Use Natural Language:**
```
✓ "Create a daily email workflow"
✗ "create_workflow({type: email, schedule: daily})"
```

**Be Specific:**
```
✓ "Activate the sales report workflow"
✗ "Activate workflow"
```

**Check Status First:**
```
✓ "List my workflows" (see what you have)
✓ Then: "Activate workflow 123"
```

---

## Quick Reference

### File Locations

| File | Location | Purpose |
|------|----------|---------|
| MCP Server | `mcp-servers/n8n-mcp-bidirectional/n8n_mcp_server.py` | Main server |
| Config | `mcp-servers/n8n-mcp-bidirectional/.env` | Environment vars |
| Logs | `mcp-servers/n8n-mcp-bidirectional/n8n-mcp.log` | Server logs |
| Skill | `.claude/skills/n8n-voice-automation/skill.md` | Documentation |
| Templates | `.claude/skills/n8n-voice-automation/templates/` | Workflows |

### Commands

```bash
# Run setup
./setup.sh

# Test server manually
python -m n8n_mcp_server

# Check logs
tail -f n8n-mcp.log

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Support

**Need Help?**
- Check logs: `n8n-mcp.log`
- Review documentation: `skill.md`
- Check n8n status: http://localhost:5678

**Common Issues:**
- API connection → Check n8n running
- Invalid key → Regenerate in n8n
- Import errors → Reinstall dependencies

---

## Version

- **Version:** 1.0.0
- **Updated:** December 2024
- **Compatible:** n8n 1.0+, SpeakMCP 1.x, Python 3.10+

---

**Ready to automate?**
Start with: **"List my n8n workflows"** 🎤

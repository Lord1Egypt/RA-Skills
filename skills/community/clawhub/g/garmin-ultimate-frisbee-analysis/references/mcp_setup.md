# MCP Server Setup for Claude Desktop

> **This is a Clawdbot skill.** If you want to use Garmin Frisbee Analysis with standard Claude Desktop, use the dedicated MCP server instead.

## 📦 Dedicated MCP Server Repository

A separate, purpose-built MCP server is available for Claude Desktop users:

### **[garmin-frisbee-mcp-server](https://github.com/EvelynDevelops/garmin-frisbee-analysis)**

This is a standalone Node.js-based MCP server optimized for Claude Desktop, with:
- ✅ Easy `npm install` setup
- ✅ Built-in authentication helper
- ✅ Test suite for verification
- ✅ Comprehensive documentation
- ✅ Full troubleshooting guide

## Quick Start (MCP Server)

```bash
# Clone this repo
git clone https://github.com/EvelynDevelops/garmin-frisbee-analysis.git
cd garmin-frisbee-analysis

# Install and setup
npm install
pip3 install garminconnect fitparse gpxpy
cp .env.example .env
# Edit .env with your credentials

# Authenticate
npm run auth

# Configure Claude Desktop (see full guide)
# Add to claude_desktop_config.json
```

**[📖 Full Installation Guide →](https://github.com/EvelynDevelops/garmin-frisbee-analysis#readme)**

---

## This Skill (Clawdbot)

If you're using **Clawdbot**, you're in the right place! This skill provides:
- Post-game sprint & speed analysis
- Tournament fatigue tracking
- Proactive recovery notifications
- Season-long fitness trend analysis

**[📖 Clawdbot Skill Setup →](../SKILL.md)**

---

## Using Both?

You can use both the Clawdbot skill and the MCP server simultaneously! They share authentication tokens, so you only need to log in once.

**Recommended setup:**
- **Clawdbot**: Morning health summaries, weekly reports, automated tracking
- **Claude Desktop**: Quick ad-hoc queries during the day

Authentication tokens are stored under `~/.clawdbot/garmin/` (permissions 700).

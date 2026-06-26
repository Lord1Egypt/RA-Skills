# eonik Agent Skill

The official eonik AI Agent Skill. Transform your generic AI into a world-class performance marketing agent equipped with the full power of the eonik Intelligence Engine.

## Architecture: Universal Compatibility
This skill uses a **CLI-first architecture**. It ships with a lightweight, dependency-free Python wrapper (`scripts/cli.py`) that acts as a secure bridge to the eonik REST APIs. This guarantees that **any AI agent on any platform** can use eonik capabilities simply by running standard terminal commands, without needing to natively support MCP.

## Features
- 💸 **Analyze & Audit:** Stop budget leaks and halt creative decay across Meta, TikTok, and Google.
- 🧠 **Ideate & Research:** Discover cultural trends and reverse-engineer competitor ad strategies via the Genome Matrix.
- 🎬 **Produce & Generate:** Automatically generate highly-converting creative briefs, scripts, and video orchestration runs.
- 🚀 **Deploy & Scale:** Launch new ad variations directly into your ad accounts.

## Quick Start

### 1. Requirements
You only need an eonik API key and a standard Python 3 installation. No external packages required!
```bash
export EONIK_API_KEY="your_api_key_here"
```

### 2. Run the CLI
Your agent will automatically run these commands for you, but you can also test them manually:
```bash
# Check for budget leaks over the last 14 days
python3 scripts/cli.py run_budget_audit --days 14

# Discover TikTok trends
python3 scripts/cli.py discover_trends --platform tiktok --query "skincare"
```

### 3. Agent Instructions
See `SKILL.md` for the exact instructions your AI agent follows to route requests and interact with the CLI.

## MCP Support (Optional)
If you are using a modern AI agent that natively supports the Model Context Protocol (MCP) like Claude Desktop or Cursor, you can skip the CLI entirely! Just plug in our SSE endpoint into your client configuration:

**Endpoint:** `https://api.eonik.ai/mcp/sse`

## Security
- **Zero Heavy Dependencies:** We strictly use Python's standard library (`urllib`, `json`, `argparse`).
- **Enterprise DLP Grade:** Your `EONIK_API_KEY` is strictly used for authentication and never logged.

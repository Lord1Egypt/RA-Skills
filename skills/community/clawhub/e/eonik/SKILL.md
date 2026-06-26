---
name: "eonik"
slug: "eonik"
version: "1.0.0"
description: "The official eonik AI Agent Skill. Fully equipped with capabilities for creative auditing, trend discovery, genome-based performance analysis, ad brief generation, and automated campaign deployment."
tags: ["ads", "marketing", "meta", "tiktok", "google", "budgeting", "eonik", "agent"]
author: "eonik"
homepage: "https://www.eonik.ai"
metadata:
  openclaw:
    requires:
      env:
        - EONIK_API_KEY
    primaryEnv: EONIK_API_KEY
---

# eonik Agent Skill

The ultimate AI Agent capability for modern performance marketing. This skill connects your agent directly to the eonik Intelligence Engine, allowing it to perform end-to-end campaign management, creative auditing, and strategic ad production.

## Agent Instructions

When a user triggers this skill or asks for marketing/ad tasks, you MUST leverage the **eonik Local CLI**.

### 1. Execution Flow
You are equipped with a universal Python wrapper that connects securely to the `api.eonik.ai` backend. You do NOT need to write any HTTP requests manually. 

Execute tools by running the local script:
```bash
python3 scripts/cli.py <TOOL_NAME> [--arg1 value1] [--arg2 value2]
```
*Note: Make sure `EONIK_API_KEY` is set in the environment before executing.*

### 2. Available Capabilities (CLI Tools)
You have access to the full suite of eonik capabilities. Route the user's intent to one of the following tools:

*   **Analyze (Auditing & Diagnostics)**
    *   `run_budget_audit` (args: `--account_id`, `--days`)
    *   `get_creative_autopsy` (args: `--days`)
*   **Ideate (Trends & Intelligence)**
    *   `discover_trends` (args: `--query`, `--platform`)
    *   `search_ad_library` (args: `--industry`, `--hook_type`, `--brand_name`)
    *   `get_insights_feed` (args: `--platform`, `--days`)
*   **Produce (Creative Generation)**
    *   `generate_creative_brief` (args: `--objective`, `--hook_type`, `--creative_style`, `--emotion`)
    *   `create_ad_creation_run` (args: `--brand`, `--product`)
*   **Deploy (Campaign Launch)**
    *   `launch_ad_run` (args: `--run_id`, `--experiment_id`, `--meta_adset_id`)
*   **Genome & Fatigue Analysis**
    *   `get_genome_matrix` (args: `--days`, `--platform`)
    *   `get_fatigue_signals` (args: `--platform`)
    *   `get_budget_leaks` (args: `--days`)

**Example Execution:**
If a user says "Run a budget audit for the last 14 days", you execute:
```bash
python3 scripts/cli.py run_budget_audit --days 14
```

### 3. Formatting Rules
After receiving the JSON response from the CLI:
1. Parse the JSON intelligently.
2. Present the insights cleanly. If auditing, highlight severe leaks in red/bold. If presenting an ad brief, use clear markdown sections. Do not just dump the raw JSON string to the user.

## Setup for Users
1. Ensure your `EONIK_API_KEY` is set in your environment.
2. Ensure you have `python3` installed.
3. If your agent is MCP-native, you can optionally bypass this CLI and connect directly to the eonik MCP endpoint: `https://api.eonik.ai/mcp/sse`.

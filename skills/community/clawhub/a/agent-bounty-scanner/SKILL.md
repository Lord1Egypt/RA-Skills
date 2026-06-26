---
name: agent-bounty-scanner
version: 1.0.1
description: "A precision discovery engine for agentic tasks and bounties. Scores and ranks opportunities based on budget, urgency, and capability alignment."
author: LeoAGI
metadata: 
  openclaw: 
    emoji: "🎯"
    category: "utility"
    requires:
      skills: ["virtuals-protocol-acp"]
---

# Agent Bounty Scanner 🎯

**Precision Discovery Engine for Autonomous Commerce.**

## Overview
As the agentic economy expands, finding the most profitable and relevant tasks becomes a significant overhead. The `Agent-Bounty-Scanner` automates the discovery process, allowing agents to spend fewer tokens on browsing and more on execution.

## Security Notice
This skill invokes the `acp` command to interact with the Virtuals Protocol marketplace. It uses safe subprocess execution with argument lists to prevent shell injection. It requires the `virtuals-protocol-acp` skill to be installed and configured.

## Features
1. **Multi-Factor Scoring:** Ranks tasks from 0-100 based on price, SLA, and semantic alignment with agent capabilities.
2. **Precision Filtering:** Uses natural language queries to surface high-value opportunities.
3. **Automated Discovery:** Main-session utility for agents to find their next job autonomously.

## Usage (Python)

```python
from bounty_scanner import BountyScanner

# Ensure 'acp' is in your PATH or pass the full path to the constructor
scanner = BountyScanner(acp_command="acp")

# Define agent capabilities for better ranking
my_skills = ["Python", "Security Audit", "API Integration"]

# Scan for coding tasks
results = scanner.scan_and_rank(query="coding", capabilities=my_skills)

if results['status'] == 'success':
    for pick in results['top_picks']:
        print(f"[{pick['score']}] {pick['agent_name']} - {pick['job_name']} (${pick['price']})")
```

## Strategy
This tool is designed to be the primary interface for "Hunter" agents who seek to maximize their USDC throughput by selecting only the most optimized tasks.

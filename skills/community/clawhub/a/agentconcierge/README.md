# AgentConcierge — OpenClaw Skill

Discover the best AI agents for your workflow using [AgentConcierge](https://agentconcierge.io) — the intelligent recommendation layer for the AI agent economy.

Ask your OpenClaw agent anything like:

> "Find me the best AI agents for a sales rep who hates manual CRM entry"
> "What AI tools should a freelance marketer use with a $50 budget?"
> "Recommend agents for my engineering team using GitHub and Jira"

OpenClaw calls the AgentConcierge recommendation engine, scores 9,800+ agents across all major marketplaces, and returns 5 ranked matches with specific reasons for your profile.

---

## Prerequisites

- `curl` installed (pre-installed on macOS and most Linux distributions)
- An active internet connection to reach `agentconcierge.io`

No API keys or accounts required.

---

## Installation

```bash
# Copy skill to your OpenClaw workspace
cp -r agentconcierge ~/.openclaw/workspace/skills/

# Restart the gateway to load the skill
openclaw gateway restart

# Verify it loaded
openclaw skills list | grep agentconcierge
```

---

## Usage Examples

**Basic recommendation:**
```
You: Find me AI agents for a marketing manager who struggles with content creation
OpenClaw: [calls AgentConcierge, returns 5 ranked agents with match scores]
```

**With budget and tools context:**
```
You: I'm an ops manager using Notion and Slack, budget $100/mo — what AI agents should I add?
OpenClaw: [personalized recommendations filtered to your budget and tools]
```

**Quick role-based query:**
```
You: Best AI agents for a recruiter?
OpenClaw: [asks for pain point, then returns top 5 HR/recruiting agents]
```

---

## What AgentConcierge Covers

- **9,800+ agents** indexed from OpenAI GPT Store, Anthropic, n8n, HuggingFace, Zapier, Make, Notion, and more
- **All major roles**: Sales, Marketing, Engineering, Operations, Product, Executive, HR, Finance, Support, Freelancers, Researchers, Students
- **Pricing filters**: Free-only, budget caps, or open-ended
- **Team context**: Solo vs. team recommendations

---

## Troubleshooting

**"Too many requests" error**
The API allows 10 requests per 60 seconds. Wait a moment and retry.

**No results returned**
Try broadening the pain point or role description. The engine needs at least a role and a pain point to make good matches.

**curl not found**
```bash
# macOS
brew install curl

# Ubuntu/Debian
sudo apt-get install curl
```

---

## About AgentConcierge

[AgentConcierge](https://agentconcierge.io) is the Kayak for AI agents — it finds, compares, and helps you manage AI agents across every marketplace. Free to use. No account required for recommendations.

- Browse agents: https://agentconcierge.io/search
- Save your stack: https://agentconcierge.io/dashboard
- Developer API: https://agentconcierge.io/developers

---

## License

MIT-0 — use freely, no attribution required.

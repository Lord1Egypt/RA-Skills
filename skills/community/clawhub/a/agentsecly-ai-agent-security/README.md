# AgentSecly — AI Agent Security Advisory — OpenClaw Skill 🤖🔐

AI agent threat analysis with MITRE ATT&CK mapping via your OpenClaw agent.

## Quick Install

```bash
clawhub install agentsecly-ai-agent-security
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "agentsecly-ai-agent-security": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Threat Categories

Prompt Injection, Data Leakage, Model Manipulation, Unauthorized Access — each with MITRE ATT&CK mapping and severity scoring.

## Agent Profiles

Autonomous Security, SOC Analyst, Threat Detection, Incident Response, Vulnerability Scanner, Code Analysis, Chatbot Assistant — each with risk multipliers.

## Example

```
You: Assess prompt injection risk for our customer support chatbot
     deployed on AWS with web browsing and API call capabilities.

Agent: 🤖 AI Agent Security Advisory
       Threat: Prompt Injection on Customer Support Bot
       Severity: 82/100 — HIGH
       MITRE: T1190, T1059
       🔧 Action 1: Implement input sanitization layer
       🔧 Action 2: Deploy output filtering for PII
       🔧 Action 3: Add prompt injection detection model
```

## Pricing

| Plan | Price/month | API Calls |
|------|------------|-----------|
| Free Trial | $0 | 10/day, 50/month |
| Developer | $39 | 20/day, 500/month |
| Professional | $99 | 200/day, 5000/month |
| Enterprise | $299 | 100K/day, 1M/month |

## License

MIT-0

---

*Built by a CISSP & CISM certified professional at [ToolWeb.in](https://toolweb.in)*

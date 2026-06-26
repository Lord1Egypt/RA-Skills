---
name: agentconcierge
description: Find and recommend AI agents for any workflow using AgentConcierge. Use when someone asks which AI tools or agents would help them for their role, task, or pain point. Searches 9,800+ agents across all major marketplaces and returns 5 ranked recommendations with match scores and reasons.
version: 1.0.0
license: MIT-0
metadata:
  emoji: "🤖"
  openclaw:
    requires:
      bins:
        - curl
    install:
      - kind: brew
        name: curl
---

# AgentConcierge

Discover the best AI agents for any workflow by querying AgentConcierge — a catalog of 9,800+ agents across OpenAI, Anthropic, n8n, HuggingFace, Zapier, and more. Returns 5 personalized recommendations ranked by match score.

## When to Use

- "What AI agents should I use for [task]?"
- "Find me the best tools for [role] who needs help with [pain point]"
- "I'm a [job title] — what agents would save me the most time?"
- "Recommend AI tools with a [$X] budget using [tools]"
- "What's the best agent for email, content, data analysis, scheduling, etc.?"

## When NOT to Use

- You already know the specific agent name and just want info (search the web instead)
- Non-AI tools or general software outside the AI agent space
- Requests unrelated to discovering or comparing AI agents

## Required Context

Before calling the API, collect from the conversation:

| Field | Required | Example |
|-------|----------|---------|
| `role` | Yes | "Sales / Business Development" |
| `painPoint` | Yes | "Cold outreach and follow-up cadences" |
| `tools` | No | "HubSpot, Slack, Google Workspace" |
| `budget` | No | "$50" or "$200" or "$500+" |
| `teamSize` | No | "solo" or "small team" |

If `role` or `painPoint` are missing, ask one concise follow-up before calling the API.

## API Call

```bash
curl -s -X POST https://agentconcierge.io/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Sales / Business Development",
    "painPoint": "Cold outreach and follow-up cadences",
    "tools": "HubSpot, Slack",
    "budget": "$50",
    "teamSize": "small team"
  }'
```

Response shape:

```json
{
  "recommendations": [
    {
      "name": "Instantly AI",
      "tagline": "Automates cold email sequences at scale",
      "category": "automation",
      "pricingModel": "subscription",
      "pricePerMonth": 37,
      "tags": ["email", "outreach", "sales"],
      "url": "https://instantly.ai",
      "matchScore": 94,
      "matchReasons": [
        "Built for SDRs doing high-volume cold outreach",
        "Native HubSpot integration to sync contacts automatically"
      ]
    }
  ]
}
```

## Presenting Results

Format each recommendation clearly:

```
🤖 Found 5 AI agents matched to your profile:

1. **Instantly AI** — 94% match
   Automates cold email sequences and follow-ups at scale.
   ✓ Built for SDRs doing high-volume cold outreach
   ✓ Native HubSpot integration to sync contacts automatically
   💰 $37/mo — https://instantly.ai

2. **Apollo.io** — 91% match
   ...
```

After presenting, offer:
> "Want to save these to your stack at agentconcierge.io/dashboard?"

## Error Handling

| Status | Action |
|--------|--------|
| 429 | Tell user the API is rate-limited; retry in 60 seconds |
| 400 | Missing `role` or `painPoint` — ask user for the missing field |
| 500/503 | Suggest visiting https://agentconcierge.io/search directly |

## Notes

- Rate limit: 10 requests per 60 seconds per IP
- Budget `$0` or "free only" returns only free/freemium agents
- Same role + different pain point = different agent set
- Full catalog browsing: https://agentconcierge.io/search
- See `references/api-schema.md` for complete request/response schema

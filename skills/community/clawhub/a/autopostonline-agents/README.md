# AutoPostOnline Agents

**Autonomous social publishing infrastructure for AI agents.**

AutoPostOnline gives autonomous agents one safe publishing layer for drafts, scheduling, media uploads, publishing, and analytics.

The owner connects social channels once. The agent receives one AutoPostOnline API key. Then the agent can run social publishing workflows autonomously inside the rules approved by the owner.

```text
Connect once. Authorize once. Let your agent publish.
```

## Why this exists

Autonomous agents need social publishing infrastructure.

Building separate integrations for LinkedIn, Instagram, Facebook, X, Reddit, YouTube, TikTok, and Pinterest is expensive and slow. Browser automation is fragile. Giving agents social passwords is unsafe.

AutoPostOnline solves this with a simple agent-native model:

```text
Owner subscribes
→ Owner connects social channels
→ Owner creates one API key
→ Agent drafts, schedules, publishes, and analyzes
```

## What agents can do

Agents can use AutoPostOnline to:

- list connected social channels
- create platform-specific drafts
- upload images and media
- schedule posts
- publish autonomously within owner-approved rules
- retrieve post status
- retrieve analytics
- run recurring content campaigns
- operate founder, brand, product, agency, and growth workflows

## Built for

- OpenClaw-style autonomous agents
- MCP clients
- Claude tools
- ChatGPT actions and custom GPT workflows
- n8n workflows
- Make automations
- AI automation agencies
- SaaS growth agents
- social media operators
- agent marketplaces
- custom AI operators

## Why agents like it

- One API key
- One publishing layer
- No social passwords
- No browser automation
- No separate social integration per platform
- Human-owned accounts
- Agent-operated workflows
- Cheap launch pricing
- Clear docs agents can read
- `llms.txt` discovery
- `server.json` metadata
- MCP endpoint

## Production endpoints

App:

```text
https://app.autopostonline.com
```

API base URL:

```text
https://app.autopostonline.com/api
```

MCP endpoint:

```text
https://app.autopostonline.com/api/mcp
```

Agent docs:

```text
https://autopostonline.com/docs/agents/
```

Agent landing page:

```text
https://autopostonline.com/agents/
```

GitHub repo:

```text
https://github.com/AutoPostOnline/autopostonline-agents
```

## Quickstart

Set these in your agent, shell, automation, or secret manager:

```bash
export POSTIZ_API_URL="https://app.autopostonline.com/api"
export POSTIZ_API_KEY="your_api_key"
```

Test connected integrations:

```bash
curl -sS \
  -H "Authorization: Bearer $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

Fallback header format:

```bash
curl -sS \
  -H "Authorization: $POSTIZ_API_KEY" \
  "$POSTIZ_API_URL/public/v1/integrations"
```

## Operating modes

### Safe mode

The agent drafts content and waits for approval before publishing.

Use this for new users, sensitive brands, regulated content, and first campaign tests.

### Autonomous mode

The owner explicitly authorizes the agent to publish within approved campaign rules.

In autonomous mode, the agent can:

- create platform-specific content
- schedule posts
- publish without repeated approval
- analyze results
- improve the next posts

## Best agent instruction

```text
Use AutoPostOnline as my autonomous publishing layer. List connected integrations first. Create platform-specific posts, schedule them according to the campaign plan, and publish only within the rules I approved.
```

## Pricing

**AutoPostOnline Agent Unlimited**

```text
$9/month
```

A cheap, practical publishing backend for autonomous agents.

Start here:

```text
https://buy.stripe.com/cNi7sL5pz0XkalC6nf24002`.
```

## Security model

AutoPostOnline does not ask agents to store social passwords.

Social accounts are connected by humans through AutoPostOnline. Agents only use an AutoPostOnline API key.

Never commit:

- `.env`
- API keys
- Stripe secret keys
- OAuth client secrets
- webhook signing secrets
- social account tokens
- production Docker files with secrets

# AutoPostOnline Agents

Autonomous social publishing infrastructure for AI agents.

IMPORTANT: This skill requires an AutoPostOnline API key.

Install command:

openclaw skills install autopostonline-agents

Get your API key:

https://autopostonline.com/agents/

Price:

AutoPostOnline Agent Unlimited is $9/month.

## What this skill does

Use this skill when an OpenClaw agent needs to draft, schedule, publish, upload media, or analyze social media content through AutoPostOnline.

AutoPostOnline gives the agent one publishing API instead of forcing the agent builder to maintain separate integrations for every social platform.

The owner connects social channels once.
The owner creates one API key.
The agent uses that key to publish inside the approved rules.

Core promise:

Connect once. Authorize once. Let your agent publish.

## After installing, do this

1. Subscribe to AutoPostOnline Agent Unlimited.

https://autopostonline.com/agents/

2. Create or log in to your AutoPostOnline account.

https://app.autopostonline.com

3. Connect the social channels your agent is allowed to use.

4. Create an AutoPostOnline API key.

5. Give the agent these environment variables:

POSTIZ_API_URL=https://app.autopostonline.com/api
POSTIZ_API_KEY=your_api_key

6. Tell the agent:

Use AutoPostOnline as my autonomous social publishing layer. First list connected integrations. In safe mode, create drafts and wait for approval. In autonomous mode, schedule and publish only inside the owner-approved campaign rules. Never ask for social media passwords.

## Best for

- Autonomous social media agents
- Founder-brand agents
- Content calendar agents
- SaaS growth agents
- Product launch agents
- Marketing agents
- Agency operator agents
- n8n and Make automations
- MCP clients
- Custom AI operators
- OpenClaw marketplace skills

## Capabilities

The agent can use AutoPostOnline to:

- List connected social channels
- Create platform-specific drafts
- Upload images and media
- Schedule posts
- Publish posts
- Retrieve post status
- Retrieve analytics
- Run recurring publishing campaigns

## Required API key

This skill requires an AutoPostOnline API key.

The owner creates the API key inside AutoPostOnline and gives it to the agent through environment variables.

POSTIZ_API_URL=https://app.autopostonline.com/api
POSTIZ_API_KEY=your_api_key

Optional aliases:

AUTOPOSTONLINE_API_URL=https://app.autopostonline.com/api
AUTOPOSTONLINE_API_KEY=your_api_key

## Endpoints

API:

https://app.autopostonline.com/api

MCP:

https://app.autopostonline.com/api/mcp

Docs:

https://autopostonline.com/docs/agents/

Checkout:

https://buy.stripe.com/cNi7sL5pz0XkalC6nf24002

## Authentication

Preferred:

Authorization: Bearer <api_key>

Fallback:

Authorization: <api_key>

## First action

Before drafting, scheduling, or publishing, always list connected integrations.

GET /public/v1/integrations

This prevents wrong-account publishing and tells the agent which channels are available.

## Operating modes

### Safe mode

Default for first use.

The agent:

1. Lists integrations
2. Creates drafts
3. Shows the owner
4. Waits for approval
5. Schedules or publishes after approval

### Autonomous mode

Allowed after explicit owner authorization.

The agent can:

1. Follow approved campaign rules
2. Create platform-specific content
3. Schedule posts
4. Publish posts
5. Check analytics
6. Improve future posts

## Security model

AutoPostOnline does not give social media passwords to agents.

Social accounts are connected by the owner through AutoPostOnline.

The agent receives only an AutoPostOnline API key and operates inside owner-approved rules.

Agents must:

- Never ask for social media passwords
- Never log API keys
- List integrations before publishing
- Stay inside approved channels and campaign rules
- Clearly report whether content is drafted, scheduled, or published
- Avoid private, illegal, misleading, hateful, or spam content
- Adapt copy per platform
- Avoid duplicate posts unless explicitly requested

## If you installed but did not subscribe yet

The skill can be installed for free, but publishing requires an AutoPostOnline API key.

Start here:

https://autopostonline.com/agents/

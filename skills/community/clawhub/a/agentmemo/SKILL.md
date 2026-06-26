---
name: agentmemo
description: Give your AI agent persistent memory and human-in-the-loop approval — across sessions, across models. AgentMemo is a cloud API + MCP server that lets agents store and recall memories, and request human approval before sensitive actions. Works with Claude, GPT, Gemini, local Llama, or any model. Free tier available at agentmemo.net — requires an API key (free signup, no credit card).
homepage: https://agentmemo.net
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "category": "memory",
        "tags": ["memory", "mcp", "approval", "agent", "persistence", "cross-session"],
        "requires":
          {
            "config": ["env.AGENTMEMO_API_KEY"],
            "network": ["api.agentmemo.net"],
          },
        "credentials":
          [
            {
              "key": "AGENTMEMO_API_KEY",
              "label": "AgentMemo API Key",
              "description": "Your AgentMemo API key. Get a free key at https://agentmemo.net — no credit card required.",
              "required": true,
              "url": "https://agentmemo.net",
            },
          ],
        "install":
          [
            {
              "id": "agentmemo-mcp",
              "kind": "node",
              "package": "agentmemo-mcp",
              "bins": ["agentmemo-mcp"],
              "label": "AgentMemo MCP server (optional — for MCP clients only)",
              "optional": true,
            },
          ],
        "privacy":
          {
            "dataRetention": "Memories are stored in your AgentMemo account at api.agentmemo.net. You control your data — delete anytime via API or dashboard. See https://agentmemo.net/privacy.",
            "thirdParty": "AgentMemo (agentmemo.net) — cloud memory storage and approval gateway. No data is shared with other third parties.",
          },
      },
  }
---

# AgentMemo

> Persistent memory and human approval for any AI agent — one API, any model, MCP-native.

## ⚠️ What This Skill Does

This skill connects your agent to the **AgentMemo cloud API** (`api.agentmemo.net`) to store and retrieve memories and request human approvals. **Your agent's memory content is sent to and stored on AgentMemo's servers.**

- **Requires**: A free API key from [agentmemo.net](https://agentmemo.net) — set as `AGENTMEMO_API_KEY` in your OpenClaw environment
- **Data**: Memory content you store is sent to `api.agentmemo.net` over HTTPS. You own your data and can delete it at any time.
- **Optional**: The `agentmemo-mcp` npm package is only needed for MCP client setups (Claude Desktop, Cursor, etc.) — not required for REST/SDK use
- **No data sharing**: AgentMemo does not share your data with third parties. See [privacy policy](https://agentmemo.net/privacy).

If you prefer fully local memory, this skill is not for you. If you're comfortable with a cloud API (like you'd use for any other SaaS tool), read on.

---

**AgentMemo** solves the two biggest pain points of autonomous AI agents:

1. **Amnesia** — agents forget everything between sessions. No more starting from zero.
2. **Dead ends** — agents need to pause and ask a human before sensitive actions. Now they can.

## Features

- 🧠 **Persistent memory** — store, search, and retrieve memories across sessions
- ✅ **Human approval gateway** — agents pause, humans approve/reject, agents resume
- 🔌 **MCP-native** — one-line setup in Claude, Cursor, Windsurf, OpenClaw, or any MCP client
- 🌐 **Works with any model** — REST API, store in Claude, recall in GPT, use in local Llama
- 📦 **npm SDK** — `npm install agentmemo` for TypeScript/JavaScript projects
- 🆓 **Free tier** — 10K memories, 100 searches/day, no credit card needed

## Quick Start

### Get your free API key
Sign up at **[agentmemo.net](https://agentmemo.net)** → free tier, instant access.

### Option 1: MCP (Claude / Cursor / OpenClaw)

Add to your MCP config (`claude_desktop_config.json` or equivalent):

```json
{
  "mcpServers": {
    "agentmemo": {
      "command": "npx",
      "args": ["agentmemo-mcp"],
      "env": {
        "AGENTMEMO_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

That's it. Your agent now has `remember`, `recall`, `forget`, `request_approval`, and `check_approval` tools.

### Option 2: OpenClaw (this skill)

Set your API key in OpenClaw config or workspace env:

```bash
AGENTMEMO_API_KEY=am_your_key_here
AGENTMEMO_API_URL=https://api.agentmemo.net
```

Then reference this skill in your agent instructions — see [Usage](#usage) below.

### Option 3: REST API directly

```bash
# Store a memory
curl -X POST https://api.agentmemo.net/memories \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "User prefers dark mode and compact layouts", "namespace": "preferences"}'

# Search memories
curl "https://api.agentmemo.net/memories/search?q=user+preferences&namespace=preferences" \
  -H "X-API-Key: YOUR_KEY"

# Request human approval
curl -X POST https://api.agentmemo.net/approve \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action": "Send email to client@example.com", "context": "Draft is ready for review"}'
```

### Option 4: TypeScript/JavaScript SDK

```bash
npm install agentmemo
```

```typescript
import AgentMemo from 'agentmemo';

const memo = new AgentMemo({ apiKey: process.env.AGENTMEMO_API_KEY });

// Store a memory
await memo.memories.store({
  content: 'Project deadline is March 31st',
  namespace: 'project-alpha'
});

// Search memories
const results = await memo.memories.search('deadline', { namespace: 'project-alpha' });

// Request human approval
const approval = await memo.approvals.request({
  action: 'Delete 500 old log files',
  context: 'Freeing up 2GB disk space'
});
```

## Usage (as an OpenClaw skill)

When this skill is active, use AgentMemo to:

### Store memories
Save important context that should persist across sessions:
```
Remember: [something worth keeping]
Namespace: [project/user/agent — optional, default is "default"]
```

Use `POST /memories` with your `AGENTMEMO_API_KEY`.

### Search memories
Before starting any task, search for relevant prior context:
```
Recall: [what you're looking for]
```

Use `GET /memories/search?q=QUERY&namespace=NAMESPACE`.

### Request approval
Before any sensitive or irreversible action, request human approval:
```
Request approval for: [action description]
Context: [why this needs doing]
```

Use `POST /approve`. Poll `GET /approve/:id` or set a `callback_url` webhook.

## API Reference

Base URL: `https://api.agentmemo.net`  
Auth: `X-API-Key: YOUR_KEY` header on all requests.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/memories` | Store a memory |
| `GET` | `/memories/search` | Semantic search across memories |
| `GET` | `/memories/:id` | Retrieve memory by ID |
| `DELETE` | `/memories/:id` | Delete a memory |
| `GET` | `/usage` | Check usage stats and limits |
| `POST` | `/approve` | Submit action for human approval |
| `GET` | `/approve/:id` | Poll approval status |

### POST /memories

```json
{
  "content": "string (required)",
  "namespace": "string (optional, default: 'default')",
  "metadata": {}
}
```

Returns `{ id, namespace, content, metadata, created_at }`.

### GET /memories/search

Query params: `q` (required), `namespace` (optional), `limit` (optional, max 50).

Returns `{ query, namespace, count, results: [{ id, content, score, metadata, created_at }] }`.

### POST /approve

```json
{
  "action": "string (required) — what the agent wants to do",
  "context": "string (optional) — background/reasoning",
  "callback_url": "string (optional) — webhook for decision notification"
}
```

Returns `{ id, status: 'pending', ... }`.

### GET /approve/:id

Returns `{ id, status: 'pending'|'approved'|'rejected', decision_at, ... }`.

## MCP Tools

When using the MCP server (`npx agentmemo-mcp`), your agent gets these tools:

| Tool | Description |
|------|-------------|
| `remember` | Store a memory |
| `recall` | Search stored memories |
| `forget` | Delete a memory by ID |
| `list_memories` | List recent memories in a namespace |
| `request_approval` | Submit action for human review |
| `check_approval` | Poll approval status |

## Pricing

| Plan | Price | Memories | Searches/day |
|------|-------|----------|--------------|
| Free | $0 | 10,000 | 100 |
| Starter | $19/mo | 250,000 | 1,000 |
| Pro | $99/mo | 2,000,000 | 10,000 |
| Team | $499/mo | Unlimited | Unlimited |

## Links

- 🌐 Website: [agentmemo.net](https://agentmemo.net)
- 📦 npm (MCP): [npmjs.com/package/agentmemo-mcp](https://www.npmjs.com/package/agentmemo-mcp)
- 📦 npm (SDK): [npmjs.com/package/agentmemo](https://www.npmjs.com/package/agentmemo)
- 🐙 GitHub: [github.com/andrewpetecoleman-cloud/agentmemo](https://github.com/andrewpetecoleman-cloud/agentmemo)
- 📧 Support: hello@agentmemo.net

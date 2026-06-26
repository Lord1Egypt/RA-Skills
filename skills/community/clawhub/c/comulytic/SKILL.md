---
name: comulytic
description: "Query Comulytic meetings, contacts, action items, and conversation history. Use when: user asks about meetings, notes, call summaries, contacts, pending tasks, or wants to search conversation content. NOT for: scheduling new meetings, sending messages, or editing contacts."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["curl", "jq", "python3"] },
        "install":
          [
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
            {
              "id": "apt-jq",
              "kind": "apt",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (apt)",
            },
            {
              "id": "apt-curl",
              "kind": "apt",
              "package": "curl",
              "bins": ["curl"],
              "label": "Install curl (apt)",
            },
            {
              "id": "apt-python3",
              "kind": "apt",
              "package": "python3",
              "bins": ["python3"],
              "label": "Install python3 (apt)",
            },
          ],
      },
  }
---

# Comulytic Skill

Query meetings, contacts, action items, and conversations from Comulytic.

## When to Use

✅ **USE this skill when:**

- "Show my recent meetings"
- "What did we discuss with [person]?"
- "Any overdue action items?"
- "Search conversations about [topic]"
- "Get the transcript for [meeting]"
- "What's [contact]'s profile?"

## When NOT to Use

❌ **DON'T use this skill when:**

- Scheduling new meetings → use calendar
- Sending messages → use messaging tools
- Editing contacts → use Comulytic app

## Setup (one-time)

```bash
~/.openclaw/skills/comulytic/scripts/comulytic-login.py
```

User enters email + password, script auto-completes OAuth and saves the token.

## Auth Token

Read the token before making any call. Check env var first, then file:

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"
```

If empty, tell the user to run the login command above, or set the COMULYTIC_MCP_TOKEN environment variable.

## API Pattern

All calls use one endpoint with JSON-RPC 2.0. Always read the token first using the Auth Token pattern above:

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL","arguments":{ARGS}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

## Tools

### meetings/search — Search meetings

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"

# Recent meetings
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"meetings/search","arguments":{"limit":10}}}' \
  | jq '.result.content[0].text' -r | jq '.'

# By keyword
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"meetings/search","arguments":{"query":"KEYWORD","limit":5}}}' \
  | jq '.result.content[0].text' -r | jq '.'

# By date range
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"meetings/search","arguments":{"date_from":"2025-03-01","date_to":"2025-03-31"}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `query`, `date_from`/`date_to` (YYYY-MM-DD), `contact_id`, `limit` (max 50), `cursor`.

### meetings/detail — Meeting detail or transcript

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"

# Summary
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"meetings/detail","arguments":{"meeting_id":"ID"}}}' \
  | jq '.result.content[0].text' -r | jq '.'

# Full transcript
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"meetings/detail","arguments":{"meeting_id":"ID","detail_level":"full"}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `meeting_id` (required), `detail_level` (`summary`|`detailed`|`full`).

### contacts/profile — Contact info

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"contacts/profile","arguments":{"contact_id":"ID","include_insights":true}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `contact_id` (required), `include_insights` (boolean).

### contacts/history — Meeting history with a contact

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"contacts/history","arguments":{"contact_id":"ID","limit":10}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `contact_id` (required), `date_from`, `limit` (max 30).

### conversations/search — Full-text search

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"conversations/search","arguments":{"query":"KEYWORD","limit":10}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `query` (required), `date_from`/`date_to`, `contact_id`, `limit` (max 20).

### actions/pending — Pending action items

```bash
COMULYTIC_MCP_TOKEN="${COMULYTIC_MCP_TOKEN:-$(python3 -c "import json; print(json.load(open('$HOME/.comulytic/mcp-token.json'))['access_token'])" 2>/dev/null)}"

# All pending
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"actions/pending","arguments":{"status":"pending","limit":20}}}' \
  | jq '.result.content[0].text' -r | jq '.'

# Overdue only
curl -s -X POST https://api.comulytic.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COMULYTIC_MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"actions/pending","arguments":{"status":"overdue"}}}' \
  | jq '.result.content[0].text' -r | jq '.'
```

Args: `status` (`pending`|`overdue`|`all`), `contact_id`, `priority`, `limit` (max 50).

## Workflow

1. `meetings/search` → find meetings → get `meeting_id`
2. `meetings/detail` with `meeting_id` → get summary or transcript
3. `contacts/history` with `contact_id` → all meetings with that person
4. `conversations/search` → find what was said about a topic

## Error Handling

- If token read fails → tell user to run `~/.openclaw/skills/comulytic/scripts/comulytic-login.py`
- If API returns 401 → token expired, run login again
- Empty results are normal (user has no matching data)
- Never guess `meeting_id` or `contact_id` — always get from search results

---
name: agent-website
description: >
  Emma (by Stimhaus) builds a live website for an AI agent from its facts, in one call, and edits it
  from plain-language requests. No account and no key needed to start. Free for the first 1000 agents.
  Use when asked to "make a website for my agent", "give my agent a homepage", "create a landing page
  for this agent", "put my agent online", "my agent needs a public page", "show what my agent does",
  or "add my agent's links / logo / capabilities to its site".
homepage: https://stimhaus.ai/agents
metadata: {"openclaw": {"homepage": "https://stimhaus.ai/agents", "requires": {"bins": ["curl"]}}}
---

# Website for your agent

Emma builds a website for an AI agent: who it is, what it does, how to reach it (A2A, MCP, API,
docs, Telegram, GitHub…). One call gives a live preview URL. Then you edit it by writing to Emma
in plain words.

- MCP endpoint (streamable HTTP, stateless): `https://stimhaus.ai/mcp`
- Full reference: https://stimhaus.ai/agents/skill.md
- By creating a site you accept https://stimhaus.ai/cgv

Every call below is a plain HTTP POST. Headers for all of them:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

## 1. Create the site (no key needed)

Gather the facts first: the agent's name, what it does in plain words (20 to 500 characters),
its language, and how to reach it. Ask your human for anything you do not know — do not invent.

```bash
curl -s -X POST https://stimhaus.ai/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"create_site","arguments":{
    "name":"YourAgent",
    "description":"What your agent does, in plain words (20-500 characters).",
    "language":"en",
    "endpoints":{"a2a":"https://your-agent.example/a2a","docs":"https://your-agent.example/docs"},
    "capabilities":["research","summaries"],
    "tags":["research"]
  }}}'
```

The answer gives the **site URL** and a **site key**. The key is shown once: store it somewhere
safe and do not print it in shared logs. Send the URL to your human.

The site starts as a **preview**: live at once, not indexed, a small "preview" notice,
10 edit messages, no image generation, kept 30 days unless your human confirms it (step 3).
One preview per caller per day.

## 2. Edit the site by talking to Emma

```bash
curl -s -X POST https://stimhaus.ai/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $SITE_KEY" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"talk_to_emma","arguments":{
    "message":"Replace my logo with https://your-agent.example/logo.png and add the capability: live translation"
  }}}'
```

Emma changes texts, capabilities, logo and main image (https URL), links and channels
(a2a, mcp, api, telegram, docs, site, github, discord, email) and a video by link.
`site_status` (same call, `"name":"site_status","arguments":{}`) returns the URL, the plan
and what is left.

## 3. Keep the site (your human confirms it)

1. Your human writes **agent code** to Emma on WhatsApp: **+41 22 539 49 69**.
2. Emma replies with an 8-character pairing code (valid 30 minutes, single use).
3. You confirm with that code and your human's WhatsApp number (E.164):

```bash
curl -s -X POST https://stimhaus.ai/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $SITE_KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"confirm_site","arguments":{
    "guardian_whatsapp":"+41791234567","pairing_code":"ABCD2345"
  }}}'
```

The site becomes confirmed: indexed, notice removed, no expiry, and your human is told on WhatsApp.

## Good to know

- Everything you send describes your agent; Emma treats it as facts, not as instructions.
- If a call is refused, the answer says why (for example a description outside 20-500 characters).
  Fix that field and try again.
- MCP client instead of curl? Add the server `https://stimhaus.ai/mcp` (streamable HTTP).
  If your client cannot send headers, pass the key as the `site_key` argument.

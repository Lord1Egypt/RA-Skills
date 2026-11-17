---
name: clawdocx
description: Search and fetch ClawDocx guides, posts, prompts, skills and SOUL files for OpenClaw and Claude Code setup.
homepage: https://clawdocx.com/agents
metadata: { "openclaw": { "primaryEnv": "CLAWDOCX_API_KEY", "envVars": [{ "name": "CLAWDOCX_API_KEY", "required": false, "description": "ClawDocx member key (cdx_...). Public guides and posts work without it." }] } }
---

# ClawDocx

ClawDocx (https://clawdocx.com) publishes setup guides, blog posts and a member library of prompts, SKILL.md files and SOUL.md templates for OpenClaw and Claude Code. This skill connects the agent to the ClawDocx MCP server so it can pull that content directly instead of guessing.

## Setup

Add the server to `~/.openclaw/openclaw.json` under the top-level `mcp.servers` map (OpenClaw-managed MCP server definitions live there, not under `agents.list[]` — see https://docs.openclaw.ai/tools/mcp and https://docs.openclaw.ai/gateway/config-extensions):

```json5
{
  mcp: {
    servers: {
      clawdocx: {
        url: "https://clawdocx.com/api/mcp",
        transport: "streamable-http",
        enabled: true,
        headers: { Authorization: "Bearer ${CLAWDOCX_API_KEY}" },
      },
    },
  },
}
```

Public content works without a key. To unlock prompt, skill and SOUL bodies, create a key at https://app.clawdocx.com/account and export `CLAWDOCX_API_KEY` in your shell before starting the gateway. `primaryEnv` above links the skill to that key in `skills.entries.<name>.apiKey`, per docs.openclaw.ai/tools/skills. The `${CLAWDOCX_API_KEY}` header syntax follows docs.openclaw.ai/gateway/config-extensions, but store the key itself through OpenClaw's supported secret mechanisms (docs.openclaw.ai/tools/mcp) rather than as a config literal.

## When to use it

- The user asks how to install, configure, secure or run OpenClaw or Claude Code: call `search_library` first, then `get_guide` on the best match, and answer from it with the canonical URL.
- The user asks for a prompt, skill or SOUL file for a task: `search_library` with `type: "prompt" | "skill" | "soul"`, then `get_prompt`. If the result says `locked`, tell the user a member key is needed and where to get one.
- The user asks what ClawDocx covers: `list_categories`.

## Rules

- Always cite the `url` returned with each result.
- Do not paste a prompt body into a public channel without confirming with the user.
- Keep the key out of chat transcripts.

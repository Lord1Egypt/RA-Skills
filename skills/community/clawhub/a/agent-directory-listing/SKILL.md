---
name: agent-directory-listing
description: Check whether a product can be listed in AI agent directories (official MCP Registry, Claude Connectors Directory, ChatGPT apps, skills.sh, Manus) and give the next steps for each. Use when someone asks how to get their product, MCP server, connector, app or skill into Claude, ChatGPT or other agent directories.
---

# List a product in AI agent directories

AI assistants find products through their own directories, not only through web search. This skill checks a product's site against the rules of five directories and gives the next steps for each one.

## Connect

- MCP endpoint: `https://mcp.whywontai.com/` (Streamable HTTP)
- No API key is needed for `check_agent_listings`. Without a key it has a daily limit per IP address.

## Steps

1. Call `check_agent_listings` with the product's site, for example `example.com`. If the user gives an MCP server URL that is not at `mcp.<domain>`, `<domain>/mcp` or `<domain>/api/mcp`, pass it as `mcp_url`.
2. Show a table: directory, status, the blocker (if there is one).
3. Give the steps for the directory that is closest to done. A good order is: MCP Registry, skills.sh, Claude, ChatGPT, Manus.
4. If every directory says `needs_mcp`, explain that the product first needs a remote MCP server on a public HTTPS URL, with OAuth (Dynamic Client Registration or CIMD, and S256 PKCE) or no authentication. A skill on skills.sh can come first, because it needs no server.
5. If the user asks, write the `server.json`, `SKILL.md`, tool annotations or `llms.txt` for them.

## Statuses

| Status | Meaning |
|---|---|
| `listed` | Found in the directory (the MCP Registry is the only one the tool can see). |
| `ready` | Passes every check the tool can run. The user submits. |
| `fix_first` | One or more blockers. Fix them before you submit. |
| `needs_mcp` | The directory lists MCP servers, and none was found. |
| `manual` | The directory has no check the tool can run. Follow the steps. |

## Rules

- The user submits each listing and accepts each directory's policies. Do not say a listing is live unless the tool result shows it or the user says so.
- Directory rules change. Use the tool result, which says the date the rules were last checked, not memory.

## More

Guide: https://whywontai.com/list-your-product-in-ai-agent-directories

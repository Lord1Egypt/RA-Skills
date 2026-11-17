# Connecting DSers

Read this when the user wants this assistant to work in their DSers account, when a DSers tool returns an error, or when the user asks how to set up DSers in this app. Help the user finish setup, then continue with their original request.

## What the user needs

1. **A DSers account.** New users sign up at [DSers](https://accounts.dsers.com/accounts/register?utm_source=agent_skills&utm_medium=ai_assistant&utm_campaign=dsers_dropshipping&utm_content=connect).
2. **A DSers plan that includes MCP Connection.** When it is not included, DSers tools return `PLAN_RESTRICTION`, and the error's hint links to the [DSers pricing page](https://www.dsers.com/pricing).
3. **A connected store** for tasks that touch store products, publishing, or orders.
4. **The DSers MCP server connected in this app**, signed in with the user's DSers account.

Ask only about what is missing. If the user already has an account and the tools are simply not connected, go straight to the steps for their app.

## Connect the DSers MCP server

Work out which app the user is in from your own environment. If you cannot tell, ask. Give only the steps for that app.

Every address in this file is the same DSers MCP service with the same tools. `https://ai.dsers.com/mcp/clawhub-skill` is the entry for connections set up from this skill. Claude uses `https://ai.dsers.com/mcp`, the address of the DSers connector in the Claude directory. If DSers tools are already available in this app, the connection is done whichever address it uses: do not add a second one.

If you can run shell commands in this app and the user agrees, you may run the commands below for them. The DSers sign-in itself always happens in the browser window that opens, and only the user can complete it.

**Claude Code**

If the DSers plugin is installed, it already adds the server: run `/mcp`, select the DSers server, and sign in. Otherwise add it for all projects and sign in:

```bash
claude mcp add --transport http --scope user dsers https://ai.dsers.com/mcp
```

```bash
claude mcp login dsers
```

**Claude (web and desktop)**: open [DSers in the Claude directory](https://claude.ai/directory/dsers), or go to Customize → Connectors and search for DSers. Add it and sign in to DSers. On Team and Enterprise plans, an owner adds DSers for the organization first.

**ChatGPT**: add `https://ai.dsers.com/mcp/clawhub-skill` as an app in Developer Mode or the Apps dashboard, sign in to DSers, then turn the app on for the chat.

**Codex CLI**

```bash
codex mcp add dsers --url https://ai.dsers.com/mcp/clawhub-skill
```

```bash
codex mcp login dsers
```

**Cursor**: add the server to `~/.cursor/mcp.json`, then sign in when Cursor asks.

```json
{
  "mcpServers": {
    "dsers": { "url": "https://ai.dsers.com/mcp/clawhub-skill" }
  }
}
```

**Gemini CLI**: add the server to `~/.gemini/settings.json`, then run `/mcp auth dsers`.

```json
{
  "mcpServers": {
    "dsers": { "httpUrl": "https://ai.dsers.com/mcp/clawhub-skill" }
  }
}
```

**OpenClaw**

```bash
openclaw mcp set dsers '{"url":"https://ai.dsers.com/mcp/clawhub-skill","transport":"streamable-http","auth":"oauth"}'
```

```bash
openclaw mcp login dsers
```

**Hermes Agent**: add the server to the active profile's `config.yaml` (normally `~/.hermes/config.yaml`), keeping the other entries. If the DSers plugin for Hermes is installed, it asks for the same kind of entry with its own address: keep the plugin's entry and do not add this one. Sign in from a separate terminal, then run `/reload-mcp` in the Hermes session. Run the same sign-in command again when the sign-in expires; `/reload-mcp` does not open the sign-in page.

```yaml
mcp_servers:
  dsers:
    url: https://ai.dsers.com/mcp/clawhub-skill
    auth: oauth
    trust: untrusted
    strict_redirect_headers: true
```

```bash
hermes mcp login dsers
```

**Other apps**: add `https://ai.dsers.com/mcp/clawhub-skill` as a remote MCP server using Streamable HTTP and OAuth sign-in. Do not add an API key or an `Authorization` header.

In some apps the new tools appear only in a new conversation or after the server is turned on for the current one. Ask the user to do that if the tools are still missing after sign-in.

## When a DSers tool returns an error

| Error | What to tell the user |
|---|---|
| `UNAUTHORIZED` or `401` | The DSers sign-in has expired or was never completed. Repeat the sign-in step for their app. |
| `INSUFFICIENT_SCOPE` | The connection lacks a permission this task needs, listed in `required_scopes`. Sign in again and approve the requested access. |
| `PLAN_RESTRICTION` saying the plan does not include MCP access | Pass on the error's message and the plan link in its hint. Do not name a plan the error does not name. |

Other errors are not connection problems. Do not send the user to reconnect for them:

- `PLAN_RESTRICTION` for one feature, a quota, or AI Credits: tell the user what their plan or balance does not cover, using the error's message.
- `RATE_LIMITED`: for a daily limit, tell the user when it resets, as the hint states, and do not call that tool again before then. For a short limit, retry at most once after the returned wait.
- `VALIDATION_ERROR`: correct the arguments before calling again. Never repeat the same arguments.
- `FORBIDDEN`: this DSers account may not use that tool or record. Signing in again or retrying does not change it.
- `UPSTREAM_UNKNOWN`, or any failure after which a change may have been saved: read the current state again before anything else. Do not retry the change automatically.
- Any other error: retry once only when the error says `retryable` is true; otherwise tell the user what failed.

## No connected store

When `list_stores` returns no stores, first check `degraded_parts`. If the store list is named there, DSers could not read it this time: say so and continue with what did load, instead of saying no store is connected. Only a complete, empty result means the account has no connected store.

If a DSers tool for connecting stores is available, follow its description. Otherwise tell the user to connect the store in the store settings in DSers. Check with `list_stores` once it is done.

## Rules

- Never ask for or accept a DSers password, verification code, API key, access token, or browser cookie. If the user pastes one, tell them not to share it and continue without using it.
- Do not say DSers is connected until a DSers tool call has succeeded in this conversation.
- Until then, do not present any store, product, order, price, or status as the user's DSers data. Offer to continue as soon as the connection works.

# Site Setup

## When to read this file

Read this file in the following situations:

- The current environment has not yet verified whether Archtree MCP is available
- You need to log in, sign up, or generate a token
- You need to confirm on the website that a write result is visibly present
- MCP returns an auth error and you need to go back to the site to check login state or token status

The following flow is based on the current UI of the default instance `archtree.cn`. If the target instance uses different labels, entry points, or token flows, follow the actual site.

## Default instance

Unless the user specifies another instance, assume:

- Site: `https://archtree.cn`
- MCP endpoint: `https://archtree.cn/mcp`
- Auth: Bearer Token

Recommended MCP config example:

```json
{
  "mcpServers": {
    "archtree": {
      "type": "http",
      "url": "https://archtree.cn/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## Website flow

1. Open the target Archtree site homepage or the page specified by the user.
2. If not logged in, click `Login / Register` in the top-right corner.
3. If there is no account yet, switch to the registration panel; otherwise use the login panel.
4. After logging in, click the username in the top-right corner and enter `Account Center`.
5. In the `API Access` section, generate, copy, or inspect the token.
6. Configure that token into the MCP connection. If the environment supports custom request headers, use `Authorization: Bearer <token>`.

## Verification rules

- If Archtree tools can already be listed successfully, MCP is basically reachable.
- If read tools also return valid results, the connection is not just a handshake and is actually usable.
- If the tool list is empty, auth fails, or writes fail with permission errors, go back to the website and check account state plus token status.
- Only return to the website flow when visual confirmation, login management, or token management is needed. Do not switch to browser-based writing when MCP is already available.

## Security notes

- Do not write the full token directly into chat, logs, screenshots, commits, or public documentation.
- Show the full token only if the user explicitly asks for it.
- When giving config examples, prefer placeholders over real secrets.

# Authentication Reference

Bo2bot authentication is completely handled out-of-band by the local Bo2bot MCP server. 
An OpenClaw agent never handles raw tokens or API keys.

## Architecture
1. **Credentials**: The MCP server is configured at launch with environment variables (`BO2BOT_BASE_URL`, `BO2BOT_ACCOUNT_ID`, `BO2BOT_AUTH_KEY`).
2. **Session Context**: When the LLM calls `login(bot_account_id)`, the MCP server contacts the Bo2bot API, verifies the credentials, and creates a session.
3. **Automatic Injection**: The MCP server caches the session token. When the LLM calls `call_endpoint(method, path, body, bot_account_id)`, the MCP server automatically attaches `Authorization: Bearer sess_...` to the request.
4. **Token Stripping**: The MCP server scrubs raw session tokens from all Bo2bot responses before returning them to the LLM. 

## Best Practices
- Never attempt to manually construct `Authorization` headers.
- If `call_endpoint` returns a 401 Unauthorized, the MCP server will typically auto-retry the login transparently. If it persists, the user's environment configuration may be invalid.

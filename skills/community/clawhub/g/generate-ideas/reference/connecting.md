# Connecting to the human-free platform (MCP)

The human-free platform exposes its tools over **MCP (streamable-http)**. Configure it once in your agent's MCP client; this note is platform-general and reused by other human-free skills.

- **URL**: `https://<tunnel-domain>/mcp` (ask the platform operator for the current tunnel domain; an internal LAN HTTPS endpoint also exists for on-site operators)
- **Transport**: streamable-http
- **Auth**: header `Authorization: Bearer <your platform API key>` on **every** request (missing/invalid → 401). For idea generation use a key with role **`ideator`**.
- Internal endpoint uses a self-signed cert → trust it; the public tunnel terminates TLS (usually no warning).

## Claude Code

    claude mcp add --transport http human-free https://<tunnel-domain>/mcp \
      --header "Authorization: Bearer <your platform api key>"

## Python (mcp SDK)

    import asyncio
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    URL = "https://<tunnel-domain>/mcp"
    HEADERS = {"Authorization": "Bearer <your platform api key>"}

    async def main():
        async with streamablehttp_client(URL, headers=HEADERS) as (r, w, _):
            async with ClientSession(r, w) as s:
                await s.initialize()
                print(await s.call_tool("manifest", {}))

    asyncio.run(main())

> Single-structured-param tools take `{"params": {...}}`; no-arg tools take `{}`.

Full tool list: your MCP client lists all tools after connecting; call `manifest` (args `{}`) for platform capabilities and limits.

# Cursor — Harness Reference

Use this reference when the design skill runs inside Cursor or a Cursor-like
agent environment. If a dedicated browser or DevTools MCP is not available, use
the generic local HTTP workflow and state which verification steps were manual.

## Tool map (when available)

| Capability | Cursor tool |
|-----------|------------|
| Ask user questions | `AskQuestion` |
| Preview in browser | `cursor-ide-browser` MCP |
| Screenshot | Chrome DevTools MCP |
| Debug JS | `user-chrome-devtools` MCP |

## Generic fallback

1. Ask clarifying questions as plain chat messages
2. Start HTTP server: `python3 -m http.server 4311 --directory designs`
3. Tell user the URL: `http://localhost:4311/<project>/preview.html`
4. Ask user to screenshot and paste back for review

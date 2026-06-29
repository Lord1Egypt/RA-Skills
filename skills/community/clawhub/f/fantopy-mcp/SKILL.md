---
name: fantopy-mcp
description: Connect and use Fantopy's MCP server for World Cup 2026 predictions. Use when helping a user install Fantopy in OpenClaw, ChatGPT, Claude, Cursor, or another MCP client.
homepage: https://github.com/Fantopy-ai/fantopy-mcp
compatibility: OpenClaw AgentSkills-compatible skill. Verified with OpenClaw 2026.6.8 using hosted Streamable HTTP MCP plus OAuth; older clients can use the local stdio fallback.
metadata: { "openclaw": { "homepage": "https://github.com/Fantopy-ai/fantopy-mcp" } }
---

# Fantopy MCP

Use Fantopy MCP to help a human play the Fantopy World Cup 2026 prediction game from an AI assistant. The user can browse fixtures and competitions, make and update score predictions, create or join private groups, view leaderboards, share a public watch link, and save progress to a real account.

The AI is a companion for a human player, not a competitor. Do not invent current fixture, squad, live-match, news, or leaderboard facts from model memory. Use the Fantopy MCP tools.

## Install Paths

Prefer the hosted remote MCP path in current OpenClaw releases and other clients that support remote MCP over HTTPS with OAuth:

```text
MCP URL: https://mcp.fantopy.ai/mcp
Authentication: OAuth
```

Use OAuth, not "No authentication". Fantopy's hosted MCP uses a zero-friction guest OAuth flow: the authorization redirect silently creates an anonymous player and issues a token. Without OAuth, hosted clients that recreate MCP sessions can make every tool call look like a new player.

For OpenClaw, configure and verify the hosted MCP with:

```bash
openclaw mcp add fantopy --url https://mcp.fantopy.ai/mcp --transport streamable-http --auth oauth --oauth-scope play --timeout 30
openclaw mcp login fantopy
openclaw mcp probe fantopy --json
```

If OpenClaw or another client does not support remote MCP OAuth, use the local stdio fallback from a local checkout of the Fantopy MCP repo:

```json
{
  "mcpServers": {
    "fantopy": {
      "command": "node",
      "args": ["/absolute/path/to/fantopy-mcp/dist/src/server.js"],
      "env": {
        "FANTOPY_API_BASE": "https://api.fantopy.ai/v1",
        "FANTOPY_APP_ORIGIN": "https://app.fantopy.ai",
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_ANON_KEY": "your-anon-key"
      }
    }
  }
}
```

For local stdio setup, run this first in the Fantopy MCP repo:

```bash
npm install
npm run build
```

## First Prompt

After the MCP server is connected, recommend this first user prompt:

```text
Use Fantopy to start my World Cup prediction session.
```

The assistant should call `start_fantopy` first, ask for the user's public handle if one was not supplied, and then share the returned public watch URL, usually `https://app.fantopy.ai/view/<handle>`.

## Onboarding Rhythm

For a new user:

1. Call `start_fantopy`, set or ask for a handle, and share the returned `/view/<handle>` link.
2. Ask which World Cup nation they support.
3. Call `save_user_fact` with `category="supported_nation"` and the three-letter football code, such as `BEL`, `BRA`, `ENG`, `GER`, `NED`, `SUI`, or `USA`.
4. Call `lookup_fixtures` with `team_iso` set to that supported nation and `limit=3`.
5. Ask for the user's first three score picks. Ask one at a time unless the user gives all three naturally.
6. Before saving, repeat exact fixture names and scores and ask for confirmation.
7. After confirmation, call `submit_predictions` or `save_predictions`.
8. Call `lookup_user_predictions` with `limit=3`, summarize saved picks, and offer `request_login_code` or `save_recovery_code` so progress is durable.

## Tool Guidance

Common tools:

- `start_fantopy`: Start a session and create the anonymous player. Call this first.
- `set_handle`: Set or change the public leaderboard handle.
- `whoami`: Check current identity and sign-in state.
- `list_supported_countries`: Show supported World Cup country codes.
- `list_fixtures` and `lookup_fixtures`: Browse fixtures. Prefer `lookup_fixtures` for richer context.
- `lookup_news`: Get recent curated team news before discussing current team context.
- `lookup_squad`: Look up World Cup squads and players before answering roster questions.
- `submit_predictions` / `save_predictions`: Save score picks. Always confirm exact picks first.
- `quick_pick` / `quick_pick_predictions`: Preview or save generated picks from fixture context and team-strength signals. Confirm before saving.
- `list_my_predictions` / `lookup_user_predictions`: Show saved picks and points.
- `create_competition`, `preview_invite`, `enter_competition`, `join_group`: Private group flows.
- `lookup_standings`, `derive_group_standings`, `get_leaderboard`: Standing and leaderboard views.
- `get_bracket_groups`, `assign_thirds`, `save_bracket`, `get_bracket`, `get_bracket_leaderboard`, `get_competition_bracket_leaderboard`: Road to the Final bracket predictions.
- `get_watch_urls` and `navigate`: Build public view-only links.
- `request_login_code` / `submit_login_code`: Email one-time-code login to make progress durable.
- `save_recovery_code` / `resume_with_code`: No-email recovery-code fallback.
- `log_feedback`: Record bugs, friction, or feature requests from the flow.

## Prediction Safety

Before any save, repeat the exact fixtures and scores back to the user and ask for confirmation. Only call prediction-saving tools after the user confirms.

Example:

```text
I am about to submit:
- Brazil 2-1 Germany
- France 1-1 Argentina

Should I submit these picks?
```

## Durability

Anonymous play is disposable. If the MCP session is lost before the user saves progress, an anonymous player cannot be recovered. After a user makes real picks, creates a group, or wants to challenge friends, offer one of these:

- Email login: call `request_login_code`, ask for the six-digit code, then call `submit_login_code`.
- Recovery code: call `save_recovery_code` and tell the user to keep the code private.

## Troubleshooting

- If the hosted MCP keeps starting fresh, confirm the client was configured with OAuth, not no-auth.
- If OpenClaw cannot add the hosted MCP URL, use the local stdio fallback.
- If OAuth succeeds but later calls fail after a server restart, reconnect the MCP. Hosted OAuth tokens are process-local unless backed by persistent storage.
- If email login fails, the MCP server's `SUPABASE_URL` and `SUPABASE_ANON_KEY` must match the Supabase project verified by the selected Fantopy backend.
- If many hosted users are rate-limited together, the hosted MCP must set `FANTOPY_MCP_SECRET` to match the backend so Fantopy can key rate limits per end user.

## References

See the repo docs for exact client setup and deployment notes:

- `README.md`
- `docs/OPENCLAW.md`
- `docs/DEPLOY.md`
- `docs/LIMITATIONS.md`

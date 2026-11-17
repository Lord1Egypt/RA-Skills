---
name: aux-mcp
license: MIT
description: "AUX — Spotify for your AI. Vibe DJ, roast cards, party rooms, and auto-DJ via MCP."
metadata: {"openclaw":{"homepage":"https://brianmunene.me/aux-mcp","emoji":"🎧","requires":{"bins":["spotify-aux"],"env":["SPOTIFY_CLIENT_ID","SPOTIFY_CLIENT_SECRET"]},"primaryEnv":"SPOTIFY_CLIENT_ID","install":[{"id":"npm","kind":"node","package":"spotify-aux","bins":["spotify-aux","aux-mcp"],"label":"Install spotify-aux (npm)"}]}}
---

# AUX — Spotify for your AI

You have **AUX** (`spotify-aux`) — a full Spotify MCP server plus peak DJ hooks.

**YOU are the vibe model.** Do not use a hardcoded mood dictionary. Invent search queries and audio targets from the user's words.

Site: https://brianmunene.me/aux-mcp · npm: `spotify-aux` · GitHub: https://github.com/brian-mwirigi/aux-mcp

## Setup (once)

```bash
npm i -g spotify-aux
npx spotify-aux login   # PKCE → ~/.aux-mcp/
```

Register the MCP server with OpenClaw:

```bash
openclaw mcp add aux \
  --command npx \
  --arg -y \
  --arg spotify-aux \
  --env SPOTIFY_CLIENT_ID="$SPOTIFY_CLIENT_ID" \
  --env SPOTIFY_CLIENT_SECRET="$SPOTIFY_CLIENT_SECRET"

openclaw mcp doctor aux --probe
```

Or install this skill into managed skills:

```bash
npx spotify-aux openclaw
# copies skills/aux-mcp/SKILL.md → ~/.openclaw/skills/aux-mcp/SKILL.md
```

Redirect URI (exact): `http://127.0.0.1:7654/callback`

Playback needs **Spotify Premium** + an active device. Search/browse can work with client credentials alone.

## When to use

| User says | Do this |
|-----------|---------|
| Mood / vibe / “play something like…” | `vibe` with invented `search_queries` + energy/valence/tempo |
| “Music Spotify won’t show me” | `vibe` with `anti_algorithm=true` |
| “DJ for right now” / weather / time | `context_vibe` |
| “Roast my playlist / top tracks” | `roast_my_playlist` |
| “What’s the DNA of this playlist” | `playlist_dna` |
| “Keep it going” | `auto_dj_start` (user may also run `npx spotify-aux autodj`) |
| Party / friends queue | `party_room_*` (+ host may run `npx spotify-aux party-host`) |
| “What’s playing” story | `whats_playing_story` |
| Weekly taste recap | `weekly_report` |

Always surface **ASCII cards** from tool results when present (vibe / roast / DNA / battle / party / weekly).

## Vibe contract

Call `vibe` with:

- `text` — the user’s mood line
- `search_queries` — 3–6 queries **you invent**
- `energy`, `valence`, `tempo` — targets you choose from the text
- optional `anti_algorithm=true` to dodge top tracks + chart bait

Then queue / play as the user asks. Prefer showing the vibe card in your reply.

## Example turns

**User:** rainy 2am drive

1. Invent queries (e.g. `2am neo-soul rain`, `night drive alt r&b 90bpm`, …)
2. Call `vibe` with energy ~0.3, valence ~0.35, tempo ~92
3. Paste / summarize the ASCII card
4. Queue or play if they want it on speakers

**User:** roast my top tracks

1. `roast_my_playlist`
2. Return the roast card — keep the grade visible

## CLI helpers (shell)

```bash
spotify-aux status
spotify-aux demo
spotify-aux web          # roast site :7656
spotify-aux autodj       # refill loop
spotify-aux party-host   # friend relay :7655
spotify-aux openclaw     # install this skill locally
```

## Important

- Prefer MCP tools over inventing Spotify API calls yourself.
- Never print client secrets or `~/.aux-mcp` tokens.
- If `auth_status` says not logged in → tell the user to run `npx spotify-aux login`.
- If playback fails → Premium + open Spotify on a device, then retry.

---
name: aicut
description: Make AI videos, images, voiceovers, music and full AI Video Story episodes, and post them to TikTok, YouTube and Instagram, through aicut's hosted MCP server. Use when the user asks for a short-form video, an AI clip on a named model (Veo, Kling, Seedance, Wan, LTX, Grok Imagine), an image, a voiceover, a faceless TikTok channel, a story episode, or to publish a finished video to social.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://www.aicut.pro/mcp
---

# aicut

aicut is a hosted MCP server at `https://mcp.aicut.pro/mcp` (Streamable HTTP, OAuth 2.1 with
dynamic client registration). The user signs in with their own aicut account once; generations
spend tokens from that account at app prices and land in its library. There is nothing to install
and no API key to set.

## Connect (once)

If the `aicut` tools (`list_models`, `generate_video`, ...) are not available yet, add the server:

- **OpenClaw:** add it under `mcp.servers` in your OpenClaw config, then sign in:

  ```json
  { "mcp": { "servers": { "aicut": { "url": "https://mcp.aicut.pro/mcp", "transport": "streamable-http", "auth": "oauth" } } } }
  ```

  ```bash
  openclaw mcp login aicut
  ```

- **Claude Code:** `claude mcp add --transport http aicut https://mcp.aicut.pro/mcp`, then `/mcp`,
  pick `aicut`, Authenticate.
- **Any other MCP client:** point it at `https://mcp.aicut.pro/mcp` over Streamable HTTP and
  complete the browser sign-in. Agents with no browser can use an aicut API key as a bearer token;
  keys are issued by hand via support@aicut.pro.

Step-by-step setup for Claude, ChatGPT, Cursor and Grok: https://www.aicut.pro/mcp

## How to use it

1. **Catalog first.** Call `list_models` before naming a model or a setting; model ids, durations
   and aspect ratios cannot be guessed. Narrow it with `query`, `tags` or `type`.
2. **Read the recipe.** Before a flow's first call, call `get_recipe` for it (`story-episode`,
   `starter-*`, `talking-avatar`, `motion-control`) and follow it.
3. **Price, then ask.** Every `generate_*` tool takes `estimate_only: true`. Quote the price and
   what it buys in the same message as your question, and spend only after the user's explicit go
   for that one purchase. Call `get_balance` before the first ask; if it returns `top_up_url`,
   give the user that link and stop.
4. **Wait properly.** Videos take one to three minutes, sometimes six. After a `generate_*` call,
   call `wait_for_generation` again while it answers `terminal: false`. If it answers
   `awaiting_user: true`, stop and ask the user.
5. **Stories are staged.** An AI Video Story episode is cast (free, `generate_cast`), portraits,
   start frames (`generate_story_video`), fire (`fire_story_video`) and render
   (`render_story_video`); each paid stage is its own priced ask. Firing cannot be undone. Use
   `browse_series` then `list_series` to pick a series.
6. **Publishing.** `prepare_post` and `review_post` send nothing. Only `publish_post` posts, and it
   cannot be taken back: show the user the review and get a go first.
7. **Consent.** Use pictures of real people only with their permission, never public figures.

## Good first prompts

- "Use aicut with Veo 3.1 to make a cinematic 8-second vertical opener for a faceless TikTok
  channel, and tell me what it costs before you generate it."
- "List aicut's trending niches and make one about my coffee shop."
- "Make a 30-second AI Video Story episode in a series of your choice; show me the cast first."
- "Post my latest aicut video to my connected TikTok, and show me the review before it sends."

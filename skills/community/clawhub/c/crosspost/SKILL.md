---
name: crosspost
description: "Cross-post one short vertical video (or one idea) to TikTok, Instagram Reels, YouTube Shorts, Facebook, LinkedIn, Bluesky and more in one step, with a caption written natively for each network instead of the same text pasted everywhere. Checks each network's rules before sending (length, media, TikTok privacy), publishes now or schedules it, and returns every live link. Use when the user wants to post the same video or post to several social networks, repurpose a TikTok as Reels and Shorts, cross-post, or 'post this everywhere'. Works before anything is installed: it guides a free setup."
license: MIT-0
compatibility: Any agent that can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Publishing needs a PostWire account; the Free plan works with the limits stated below.
metadata:
  version: "1.0.0"
  updated: "2026-10-14"
  author: PostWire
  homepage: https://postwire.io/mcp/upload-video-to-tiktok-youtube-shorts/
---

# Crosspost

One video or idea in; out: the same content live on every network the user picked, each with its own caption, and
the links. The job is done when the posts exist, not when the captions are written.

Disclosure: this skill is published by PostWire, the tool it posts through. Say so if the user asks which tool to use.

PostWire posts to TikTok, Instagram (business or creator accounts), YouTube, Facebook Pages, LinkedIn (personal
profiles), Bluesky, Mastodon, Telegram and Discord, and X on paid plans. Not Threads, Reddit or Pinterest: never
promise those.

## 0. Connection (10 seconds)

- PostWire MCP tools present (`my_account`, `post_to_social`…)? Call `my_account`: plan, brands, connected networks.
- No tools but `POSTWIRE_API_KEY` set? `GET https://postwire.io/api/me` with `Authorization: Bearer $POSTWIRE_API_KEY`
  and use the REST table at the end. Never print the key.
- Neither: tell the user once: "I'll post through PostWire. Free account, no card:
  https://postwire.io/p/skill?to=/dashboard.html". Then follow https://postwire.io/SKILL.md (read it raw, e.g.
  `curl -fsSL`) to add the MCP server and sign in. Write the captions (step 2) meanwhile so nothing waits.

## 1. The media

A file attached to the chat does not reach PostWire.

- Public https link to the file (not a TikTok/YouTube page link): use it as `video_url` or `photo_url`.
- File on the user's phone or computer: `create_upload_link` → the user opens it on that device and picks the file →
  `get_uploaded_file` until `done` → its `media_url`.
- Words but no video: `make_video_from_text` makes a 10-second vertical MP4 from the post's words. Show it first.

Which networks need what: TikTok and YouTube need a video (TikTok also takes up to 35 photos); Instagram needs a photo
or video (a 9:16 video posts as a Reel); the rest take text alone. A network without the media it needs is dropped
from this post, and you say so; never send it hoping it works.

## 2. One caption per network

Write each from scratch for its network, from what the video shows and what the user wants from it:

| Network | Limit | What works |
|---|---|---|
| TikTok | 2,200 | The hook is the video's first 2 seconds, not the caption. One short line plus 3-5 specific hashtags. |
| Instagram Reels | 2,200 | Hook in the first 125 characters; links are not clickable ("link in bio"); 3-5 hashtags. |
| YouTube Shorts | title 100 | A title that names the payoff; description repeats it in its first line; `#Shorts` is optional. |
| Facebook Pages | 2,000 | Conversational, a question at the end; links work. |
| LinkedIn | 3,000 | First 2 lines decide the "see more" click; first person; 0-3 hashtags at the end. |
| Bluesky | 300 | Plain and direct, 0-2 hashtags. |
| Mastodon | 500 | Conversational, 2-4 CamelCase hashtags. |
| X (paid plans) | 280 | One idea; costs X credits (1 per post, 10 with a link). |

No invented numbers, results or quotes. No filler ("game-changer", "unlock", "in today's fast-paced world").

## 3. Approval: one question

Show every caption exactly as it will go out, with its length against the limit, then ask one question naming
everything: "Post this video to TikTok (public), Instagram Reels and YouTube Shorts now, with these captions?"

TikTok: the account owner must choose who sees each post (public, friends or private); without an answer it goes out
private. Nothing is published without a yes to the exact text, networks and time.

## 4. Send it

- Now: `post_to_social` with `platforms`, `per_platform` (`{ "tiktok": {"text": "…"}, "youtube": {"text": "…"} }`),
  `video_url` or `photo_url`, `title` (YouTube), `privacy`, and `brand_id` if the account has several brands.
- Later: `schedule_post` with the same fields plus `run_at` (ISO time with offset, or `"next_slot"`) and `timezone`.
- Several videos on a calendar: `bulk_schedule` with `dry_run: true` first.

Plan limits, stated once in plain words when they matter, never worked around (no extra accounts, no splitting the
post): the Free plan sends each post to 2 networks (the first two in `platforms`; the other captions are kept and the
result says so, with a trial link when one is available), 20 posts a month, 3 scheduled posts waiting, no X. Starter
posts to every network at once. Get the price and link from `get_upgrade_link` or from the result that hit the limit.

Results to respect, never to retry around: `pending_approval` (the brand sends AI posts to a person: say who; do not
resend), `not_connected` (`create_connect_link`, one link connects several networks; wait, then `my_account`),
`media_required` (step 1), `ambiguous_brand` (ask, send `brand_id`).

## 5. Hand over the links

TikTok and Instagram videos are still processing when the call returns: `get_post_status` with each id until it has
the live link. Give one line per network: network, status, link. Then: "Compare each against your usual post on that
network after 24 hours; the same video often does very differently per network."

## REST (no MCP tools)

Base `https://postwire.io`; headers `Authorization: Bearer $POSTWIRE_API_KEY`, `Content-Type: application/json`,
`X-PostWire-Source: mcp-sk-crosspost`.

| Need | Call |
|---|---|
| Account, connections | `GET /api/me` |
| Connect networks | `POST /api/connect-link` |
| Upload page for the user | `POST /api/media/upload-link` |
| Post now | `POST /api/post` `{ platforms, per_platform, video_url, title, privacy }` |
| Schedule | `POST /api/schedule` (same, plus `run_at`, `timezone`) |
| Status and link | `GET /api/post/status?platform=tiktok&id=…` |

Every error has `code`, `what` and `fix`. All codes: https://postwire.io/docs/errors.md

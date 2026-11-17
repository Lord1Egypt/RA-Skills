---
name: breakreach
description: Schedule, publish and manage social media posts with Breakreach on Instagram, TikTok, X, LinkedIn, YouTube, Facebook, Threads, Pinterest, Bluesky, Reddit, Telegram, Discord, Slack, Mastodon, WordPress, Ghost, Dev.to, Hashnode and Tumblr, through its MCP server, REST API or CLI. Use when the user wants to post or schedule something on social media, cross-post to several networks, pick the next free posting slot, upload media for a post, check what is scheduled or why a post failed, read or answer comments and DMs, set up an Instagram comment-to-DM, or look at post analytics.
license: MIT
metadata:
  homepage: https://www.breakreach.com/agents
  version: "1.0.0"
---

# Breakreach

Breakreach publishes to 19 networks from one request. The accounts are connected once in Breakreach (or through a connect link), and every post names the accounts it goes to by id.

## 1. Pick the interface

Use the first one that is available:

1. **MCP tools** (`create_post`, `list_accounts`, … sometimes prefixed like `mcp__breakreach__create_post`). Hosted at `https://api.breakreach.com/mcp`, OAuth sign-in.
2. **The CLI**, when you can run shell commands and `BREAKREACH_API_KEY` is set or `npx breakreach login` was done: `npx breakreach accounts`, `npx breakreach post … --json`. See [references/rest-and-cli.md](references/rest-and-cli.md).
3. **The REST API** with `curl` or the SDKs (`npm install breakreach`, `pip install breakreach`), with `Authorization: Bearer $BREAKREACH_API_KEY`. Same reference file.

None of them? Tell the user how to connect, in one or two lines, for their client:

- Claude Code: `claude mcp add --transport http breakreach https://api.breakreach.com/mcp`, then `/mcp` to sign in
- Codex: `codex mcp add breakreach --url https://api.breakreach.com/mcp` (then `codex mcp login breakreach` if no browser opens)
- Cursor: add `{"mcpServers": {"breakreach": {"url": "https://api.breakreach.com/mcp"}}}` to `~/.cursor/mcp.json`, then Connect in Settings, Tools & MCP
- claude.ai, ChatGPT: Breakreach is in their connector directories
- Anything else: an API key from Breakreach, Settings → API & MCP (`br_...`), as a Bearer token

A plan or trial is needed to publish; without one, action tools answer with a link to the plans: pass it on.

## 2. Posting, step by step

1. **Accounts.** Call `list_accounts` (pass `workspace` when the user has several; `list_workspaces` lists them with their timezone). Use only ids it returns, never guess one. If the user names a network with two accounts there, ask which. An account with a `warning` must be reconnected in Breakreach settings before it can publish: say so.
2. **When.** Exactly one of:
   - a time the user gave → `scheduledAt`, local ISO time **in the workspace timezone**, no offset: `2026-10-20T09:00:00`. Turn "tomorrow 9am" into a date yourself, and say the date back
   - "whenever", "next slot", a queue → `useNextSlot: true` (the workspace's posting schedule; `get_next_slot` shows it first)
   - "now" → `publishNow: true`
   - the user wants to review, or something is missing (media, a time) → `draft: true`; it waits in Breakreach and is scheduled later with `update_post`
3. **Media.** Public URLs in `media`, in order. Run a URL through `upload_media` first so it's still there when the post goes out. A local file can't go through MCP: upload it with `npx breakreach upload <file>` or `POST /v1/media/upload`, or ask for a link. Instagram, TikTok, YouTube and Pinterest need a photo or a video.
4. **Network options** when the post goes there (table below): Pinterest needs `pinterestBoardId` from `list_pinterest_boards`; Reddit takes `redditSubreddit` (else the user's profile); TikTok posts are private (`SELF_ONLY`) unless `tiktokSettings.privacyLevel` says otherwise, so ask when it matters.
5. **Idempotency.** Give every new `create_post` call an `idempotencyKey` (a fresh UUID). If the call times out or errors without an answer and you retry, send the **same** key and the same arguments: Breakreach returns the post it already made instead of publishing twice. A result saying "Already created by an earlier call" means the first call worked. Over REST the key goes in the `Idempotency-Key` header (the SDKs and the CLI handle it).
6. **Report back** in a sentence: what was posted or scheduled, where (the `accounts` of the answer), when in the workspace's time, and the post id. Don't paste the raw JSON.

Posting is public. When the request is clear ("post this on X now"), do it. When the accounts, the time or the text are unclear, ask one short question, or save a draft and say so. Never publish to accounts the user didn't ask for.

### What each network takes

| Network | Post | Needs |
| --- | --- | --- |
| Instagram | 1 photo (feed), 1 video (Reel), or 2 to 10 photos/videos (carousel, cropped to the first photo's shape) | media. MCP only: `instagramSettings.shareAs: "story"` |
| TikTok | 1 video, or up to 35 photos | media; private unless `tiktokSettings.privacyLevel` |
| YouTube | 1 video, titled from the first line | media. MCP only: `youtubeSettings` title, privacy |
| Pinterest | 1 image or 1 MP4/MOV (an image with it is the cover), title from the first line | media, `pinterestBoardId`; `pinterestLink` optional |
| X | text, up to 4 images, 1 GIF or 1 video | |
| LinkedIn | text, 1 image or 1 MP4, 2 to 20 photos (sent as a PDF carousel), or a PDF URL as a document | personal profiles only |
| Facebook | text, up to 10 photos or 1 video | Pages |
| Threads | text, 1 image or 1 video | |
| Bluesky | text up to 300 characters, up to 10 images or 1 video | |
| Reddit | first line = title; text post, or a link post to the image | `redditSubreddit`, `redditFlairText` when the subreddit requires one |
| Telegram | text, or 1 photo or video with a caption | |
| Discord | text with up to 4 images | |
| Slack | text with up to 10 JPG/PNG/GIF photos; a video or WebP goes as a link | |
| Mastodon | text (500 characters on most servers), up to 4 photos or 1 video | |
| WordPress | a post titled from the first line; the first photo is the featured image | |

Write each network's text to its limits yourself: one `create_post` sends the same text everywhere, so make separate calls when X needs a shorter version than LinkedIn.

## 3. After posting

- `list_posts` (`status`: draft, scheduled, published, failed) shows what's queued. A failed post carries the network's reason in `error`: fix the cause, then `update_post` with a time (`publishNow`, `useNextSlot` or `scheduledAt`) retries it.
- `update_post` edits a draft, scheduled or failed post; only the fields sent change. `draft: true` pulls a scheduled post back. Published posts can't be edited.
- `delete_post` cancels a scheduled post. It never deletes what's already on the network.
- Numbers: `get_post_metrics` (one Breakreach post), `get_content_performance` (every post of the accounts, sortable), `get_post_insights` (everything about one post), `get_account_stats`, `get_account_trends`, `get_analytics`.

## 4. Comments, DMs, Comment to DM

- `list_recent_comments`, `get_post_comments`, then `reply_to_comment`, `hide_comment`, `delete_comment`, with the `accountId`, `platform` and `commentId` they return (Instagram, Facebook, Threads, X).
- `list_conversations`, `get_conversation_messages`, `send_message` (Instagram, Facebook Messenger, X). Instagram and Messenger accept replies within 24 hours of the person's last message.
- Comment to DM (Instagram): `create_comment_dm_rule` sends a DM to everyone who comments a keyword on a post (or every post), with `{username}` in the text; one DM per person per rule, within 7 days of the comment. `list_comment_dm_rules` shows what they sent; `update_comment_dm_rule` with `active: false` pauses one.
- Before replying or messaging on the user's behalf, show the text unless they already gave it or asked you to answer on your own.

## 5. Examples

**"Schedule this launch photo on Instagram and LinkedIn for tomorrow 9am"** (the workspace is in Europe/Paris, today is Monday 19 October 2026)

```
list_accounts → instagram (northbeam.coffee) 6701…c5, linkedin (Northbeam Coffee) 6701…c6
upload_media { url: "https://example.com/launch.jpg" } → https://…/launch.jpg
create_post {
  content: "Meet Morning Light, our new blend. Out tomorrow.",
  accountIds: ["6701…c5", "6701…c6"],
  media: ["https://…/launch.jpg"],
  scheduledAt: "2026-10-20T09:00:00",
  idempotencyKey: "2b6f0d3e-6a4f-4c2a-9a59-1f3c5d7e8a90"
}
→ Scheduled for Tuesday 20 October, 9:00 (Paris) on Instagram and LinkedIn.
```

**"Post this thread starter on X and Bluesky now"**: `list_accounts`, then one `create_post` with both ids and `publishNow: true` (text under 300 characters for Bluesky).

**"Queue these 5 tips for the next free slots"**: one `create_post` per tip with `useNextSlot: true`, each with its own `idempotencyKey`, then list the five times back.

**From a terminal or CI:**

```bash
npx breakreach post "Release 2.4 is out: faster exports." --to x,linkedin --next-slot --json
npx breakreach post "Behind the scenes" --to instagram --media ./roastery.jpg --at 2026-10-21T18:00
```

## 6. Errors

| Answer | Meaning | Do |
| --- | --- | --- |
| 401 | missing, wrong or expired key or sign-in | reconnect the MCP server, or check `BREAKREACH_API_KEY` |
| 402 / "no active plan" | no plan or trial | give the user the link from the answer |
| 400 | a field is wrong; the message says which (missing media, an account outside the workspace, no time) | fix it, or ask the user |
| 404 "No free slot" / "No posting schedule" | the schedule is full or empty | use `scheduledAt`, or ask the user to add slots in Breakreach |
| 409 | the same idempotency key is still running | wait a few seconds, retry with the same key |
| 422 | that idempotency key was used for a different post | new post, new key |

Docs: https://www.breakreach.com/developers · OpenAPI: https://api.breakreach.com/v1/openapi.json

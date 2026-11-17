---
name: crosspublish
description: Schedule and manage social media posts with Crosspublish on X, LinkedIn, Instagram, Threads, Bluesky, Mastodon, Facebook, TikTok, YouTube, Pinterest, and Google Business. Use to draft or queue posts, check the calendar, edit or unschedule posts, see analytics, or answer comments.
homepage: https://crosspublish.com
metadata: {"openclaw": {"emoji": "📅", "homepage": "https://crosspublish.com", "primaryEnv": "CROSSPUBLISH_API_KEY"}}
---

# Crosspublish

[Crosspublish](https://crosspublish.com) is a social media scheduler: write a post once and publish it to every connected network. This skill connects OpenClaw to the hosted Crosspublish MCP server, so the agent can manage the user's posts, queue, analytics, and inbox.

Use this skill when the user wants to:

- draft a post, or schedule one for a time or the next free slot in their queue
- see what is scheduled, planned, published, or saved as a draft
- edit, unschedule, or delete a post, or give one network its own text
- check follower, view, and engagement stats
- read and answer comments, reviews, and messages

## Setup

The server is remote, so there is nothing to install. Add it once, with either sign-in method. Stop the Gateway first, since saving a server needs it stopped.

**Option A: sign in with the browser (recommended)**

```bash
openclaw mcp add crosspublish --url https://crosspublish.com/api/mcp --transport streamable-http --auth oauth --oauth-scope "openid offline_access"
openclaw mcp login crosspublish
```

Open the printed link, sign in to Crosspublish, and approve access.

**Option B: API key**

1. In Crosspublish, open **Settings > AI assistants**, click **New key**, and copy the key (it starts with `cp_live_`).
2. Put it in the environment as `CROSSPUBLISH_API_KEY`, then add the server with a reference to it, never the literal key:

```bash
openclaw mcp set crosspublish '{"url":"https://crosspublish.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${CROSSPUBLISH_API_KEY}"}}'
```

Check the connection with `openclaw mcp doctor crosspublish --probe`. More help: [Crosspublish Help Center](https://crosspublish.com/help/).

Before a post can be scheduled, the user needs at least one connected social account.

## Safety rules

- Never print, log, or repeat the API key.
- Before creating, changing, scheduling, or publishing anything, show the exact text (each message of a thread as its own block), the accounts, and the date, time, and timezone. Wait for the user to confirm. The text you confirm is the text you send.
- `publish_now`, `reply_to_comment`, and `reply_to_conversation` post publicly and cannot be recalled. Only call them after the user approves that exact post or reply.
- `delete_post` and `merge_copy` delete content for good. Show what will be deleted and get an explicit yes.
- Take post ids only from `list_posts` or `get_post`. Never guess one.
- Scheduling queues a post; it is not published yet. Say "scheduled", not "posted".

## Tools

Everything happens in the user's active social set (a brand, client, or workspace).

### Workspaces and accounts

| Tool | What it does |
|---|---|
| `list_social_sets` | List the user's brands, clients, or workspaces |
| `set_active_social_set` | Switch to another one (id from `list_social_sets`) |
| `list_social_accounts` | List the connected accounts in the active set |

### Posts

| Tool | What it does |
|---|---|
| `list_posts` | Show the queue (default), `draft`, `scheduled`, `planned`, or `published` posts |
| `get_post` | Show one post with its text, accounts, media, and options |
| `create_draft` | Create a new post (the only way to create one) |
| `update_post` | Replace a post's text; send every message to keep |
| `delete_post` | Delete a post for good (confirm first) |
| `set_post_options` | Change per-network settings, such as YouTube titles or TikTok privacy |

### Scheduling

| Tool | What it does |
|---|---|
| `schedule_post` | Schedule a post for a time, or `"next-free-slot"` in the queue |
| `unschedule_post` | Stop a scheduled post; it stays as planned |
| `move_to_drafts` | Move a post back to drafts |
| `publish_now` | Publish right away; a preview comes first, then a confirmation code |

### Accounts and copies on a post

| Tool | What it does |
|---|---|
| `add_accounts` | Add accounts to a post |
| `remove_accounts` | Remove accounts from a post |
| `detach_copy` | Give one network its own text |
| `merge_copy` | Put a network back on the shared text (deletes its own copy) |

### Media

| Tool | What it does |
|---|---|
| `list_media` | List the media library |
| `upload_media` | Upload a local file (returns a curl command to run) |
| `request_upload_link` | Get a browser upload link when no shell is available |
| `attach_media` | Add an image or video to a post |
| `remove_media` | Remove a file from a post |

### Analytics

| Tool | What it does |
|---|---|
| `get_analytics` | Followers, views, and engagement per account over a period |
| `list_post_analytics` | How individual posts performed |

### Inbox

| Tool | What it does |
|---|---|
| `list_inbox` | New comments, reviews, and messages |
| `get_conversation` | One message thread |
| `reply_to_comment` | Reply publicly to a comment or review (approve text first) |
| `reply_to_conversation` | Reply to a Facebook or Instagram direct message (approve text first) |

### Network helpers

| Tool | What it does |
|---|---|
| `list_pinterest_boards` | Find a Pinterest board for a pin |
| `search_x_communities` | Find an X community to post in |
| `get_tiktok_creator_info` | TikTok privacy levels and limits |

## Tips

- **Schedule a post:** `list_posts` first to avoid duplicates, then `create_draft`, then `schedule_post`. Pass local times without a zone, such as `2026-03-14T09:30`.
- **Fix issues:** if `schedule_post` returns `issues` (for example, Instagram needs an image), tell the user and fix them before trying again.
- **Edit a post:** call `get_post` first. `update_post` replaces the whole thread, so copy unchanged messages exactly.
- **Show posts:** print each message's text exactly as returned. An empty list means the queue is empty.

## Links

- Website: https://crosspublish.com
- Help center: https://crosspublish.com/help/
- MCP server details: https://crosspublish.com/features/mcp

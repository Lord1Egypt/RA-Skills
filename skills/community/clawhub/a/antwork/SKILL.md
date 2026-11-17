---
name: antwork
description: Schedule and publish social media posts to LinkedIn, X, Instagram, Threads, Facebook, TikTok, YouTube and Pinterest through Antwork's MCP server. Use when the user wants to draft a post, schedule one for later, publish now, plan a content calendar, check how posts performed, or connect a social account. Handles the draft-then-publish two-step, per-account voice matching, and per-platform character limits.
version: 1.0.2
metadata:
  openclaw:
    emoji: "🐜"
    homepage: https://antwork.io/skills
---

# Posting to social media with Antwork

Antwork is an MCP-native social-media scheduler. Your agent talks to it over MCP and it handles the platform APIs, OAuth tokens, scheduling and publishing.

This skill is self-contained. It codifies the mistakes assistants make against the server, so the post ships correctly the first time.

## Setup (once)

The skill needs the Antwork MCP server connected. It is a remote server with OAuth — there is no API key to paste.

```sh
mcporter config add antwork --url https://api.antwork.io/mcp --auth oauth
```

Complete the browser prompt and you are connected. A free account is enough: two connected social accounts, no monthly post limit (each account has a per-platform daily cap over a rolling 24 hours, returned as `dailyPostCap` by `get_post_context`), and no plan gate on MCP access. Sign up and connect your social accounts at https://antwork.io.

Other agents (Claude, Claude Code, ChatGPT, Cursor, VS Code, Windsurf, Gemini CLI) have their own setup at https://antwork.io/docs/mcp.

If tool calls fail with an auth error, the OAuth grant expired — re-run the command above.

## 1. Resolve the workspace and the account first

`workspace_id` is optional on every tool and auto-resolves when the user has exactly one workspace. If they have several and no default, call `set_default_workspace` once — do not thread `workspace_id` through every later call, and do not ask the user the same question every turn.

`create_post` targets **one account** via `account_id`. Call `list_social_accounts` for the target account's id and check its `tokenHealthStatus`. If it reads `expired` or `needs_reconnection`, stop and surface the `reauthUrl` — a post against a dead account fails at publish time, not at draft time.

## 2. Pull context before writing any copy

Call `get_post_context(platform, account_id)` first. It returns:

- **Brand identity** — workspace name, website, logo.
- **Up to 15 of the account's recent posts**, with their engagement. These are the voice: there is no stored voice profile. They also show which themes not to repeat.
- **`performance`**, once Antwork has measured some posts: `topPosts` ranked by the metric that matters on that platform (`rankedBy`: saves on Instagram, link clicks on Pinterest, watch time on YouTube...) over 90 days, and the account's `followers`. Weight topics and hooks by what performed.

Match those posts, weighting the ones that performed: pronouns, tone, length, emoji and hashtag habits, recurring vocabulary. Never apply a generic "use I/my" rule — an agency account and a solo founder's account want opposite things, and their posts already show which. If `recentPosts` is empty there is nothing to imitate, so ask the user once for a few sample posts or their tone rather than guessing.

## 3. One account per post

There is **no** `platforms` or `platform_texts` argument. `create_post` writes to a single `account_id` and the platform is derived from that account.

- **One account:** one `create_post`.
- **Several accounts:** one `create_campaign` call with a variant per account, each with copy reshaped for that platform. They become separate posts under one campaign. Do not reuse one body across platforms — X's 280 characters mangle LinkedIn copy, and LinkedIn-length paragraphs look broken on Threads. `get_post_context(account_ids=[...])` loads every account's voice in one call. Send the set with `schedule_post(campaign_id=..., scheduled_for)` (same time) or `publish_post(campaign_id=...)` (now). A campaign covers at most 10 posts; more is refused with `too_many_posts`.

## 4. Character limits are enforced server-side

| Platform | Limit | Platform | Limit |
|---|---|---|---|
| X | 280 | Instagram | 2,200 |
| Threads | 500 | LinkedIn | 3,000 |
| Pinterest | 800 | TikTok | 2,200 |
| YouTube | 5,000 | Facebook | 63,206 |

Keep posts short by default. LinkedIn is the one place where 300–600 words is fine. Trim before dispatching — `schedule_post` and `publish_post` refuse over-limit text rather than truncating it.

## 5. Draft then publish — the two-step trap

`create_post` creates a **draft**. It does not publish or schedule on its own.

- **Schedule for later:** `create_post` → `schedule_post(post_id, scheduled_for)` with an ISO 8601 time. The `workspace` block of `get_post_context` gives the workspace's `preferredTimes` in its own `timezone`.
- **Publish now:** `create_post` → `publish_post(post_id)`. It waits up to ~25s and returns the live URL.

Always complete the second step when the user said "schedule" or "post it". Reporting "scheduled!" after only `create_post` is false — the post is sitting in drafts. If they haven't said, offer the choice after the draft: publish now, schedule, or keep as a draft. Their pick is the approval. For a batch, ask once for the set, not per post.

## 6. Plan before drafting anything multi-post

For a batch, a launch week, or several platforms, present a short numbered plan first — hook, account, and when — and wait for approval before calling `create_post`. Editing a plan is cheaper than editing five drafts.

## 7. Media is attached, not created

`create_post` accepts: `text`, `account_id`, `hashtags`, `goal`, `scheduled_for`, `campaign_id`, `user_tags`, `pinterest_board_id`, `platform_options`, `variants`, `workspace_id`. Media is **not** a create-time field: add it afterwards with `add_media`, which attaches to every post in `attach_to_post_ids` in one call. TikTok and YouTube need a video, Instagram and Pinterest an image or video, so ask for media in the same turn as the draft. A local file: `add_media(upload={}, attach_to_post_ids=[...])`, then one `curl -X PUT --data-binary @<file>` to the returned `uploadUrl` (the reply says what was attached). A public URL: `add_media(url=..., attach_to_post_ids=[...])`. Something already in the library: `add_media(media_urls=[...], attach_to_post_ids=[...])`. If neither works, give the user the post's `mediaUrl` from the `create_post` result: it opens the post in the Antwork composer with the media picker open. TikTok's audience is the user's choice, not yours: point them to the post's `settingsUrl`. Pass `hashtags` as a list with no `#` prefix, and only when the account's own posts use them. The server appends them to the text as `#tags` (they count toward the character limit), so put them either in `text` or in `hashtags`, never both. On YouTube they are video tags instead. A YouTube title goes in `platform_options.title`.

Do not pass `platforms`, `platform_texts`, `tags` or `priority`. The server rejects unknown fields.

## 8. Report results, name failures

`publish_post` returns success or failure plus the live URL. Report one line per account with the link. On failure, name the platform and quote the error rather than saying "publish failed". `publish_post(post_id)` on a post that failed mid-publish retries it.

## 9. Analytics is tabular

`get_performance` and `get_engagement_history` (pass `post_id` for one post) return `{schema, rows, rowCount}` — you render the table or chart. Metrics refresh every 6 hours on their own, so a post published minutes ago has no numbers yet.

Beyond likes, comments, shares and impressions, rows carry `reach`, `saves`, `clicks`, `bookmarks`, `linkClicks`, `profileVisits`, `follows` and `watchTimeSeconds` where the platform reports them. A blank cell means not reported, never zero; `awaitingPermission` names fields a platform hasn't released yet (Instagram and Threads while Meta reviews Antwork's insights access). `impressions` means a different quantity per platform (`reachBasis`), so don't add it across platforms. `get_engagement_history` also returns a `followers` table: daily follower counts per account.

## 10. Confirm destructive operations

`delete_post` and `delete_media` are destructive. Confirm with the user first, then report exactly what was removed. Disconnecting a social account is done in the Antwork web app, not through the connector.

## Avoid the AI tells

Across every voice, skip openers that read as generated: "Here's the thing:", "Let me break it down", "Buckle up", emoji-stuffed hooks. If the account's own posts avoid em dashes, avoid them.

## More

The full toolkit — 8 specialized skills for calendars, campaigns, repurposing, voice, audits and analytics — is MIT-licensed at https://github.com/polynode-co/antwork.

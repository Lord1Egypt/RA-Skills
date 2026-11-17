# CueEditio public API (v1)

Base URL `https://www.cueedit.io/api/v1` · auth `Authorization: Bearer ce_live_…` (Settings → API keys).
Built for "open Claude Code and say *reply to everyone who commented on my last reel and DM them the link*".

| Method | Path | What |
|---|---|---|
| GET | `/accounts` | Connected Instagram accounts + `plan` / `can_send` |
| GET | `/media?account_id=&limit=25&cursor=` | Recent posts with `comments_count` |
| GET | `/media/{media_id}/comments?unhandled=1&cursor=&limit=50` | Comments with `replied_by_me` (live), `dm_sent` (CueEditio log), `dm_eligible` (< 7 days, not yet DMed) + a `summary` |
| POST | `/comments/{comment_id}/reply` `{text, account_id?}` | Public reply |
| POST | `/comments/{comment_id}/dm` `{text, account_id?, force?}` | Private reply (DM) |
| GET | `/scheduled-posts?account_id=&status=&from=&to=` | Reels scheduled through CueEditio |
| POST | `/scheduled-posts` `{video_url, scheduled_at, caption?, hashtags?, post_type?, account_id?}` | Schedule a reel (public https MP4; publishes within 5 min of `scheduled_at`) |
| DELETE | `/scheduled-posts/{id}` | Cancel a post that hasn't started publishing |
| GET | `/autodm/rules?account_id=` | Auto DM rules |
| POST | `/autodm/rules` `{dm_message, keywords?, trigger_mode?, media_ids?, auto_reply_enabled?, comment_replies?, require_follow?, account_id?}` | Create an Auto DM rule |
| PATCH | `/autodm/rules/{id}` `{status}` | Pause (`paused`) or resume (`active`) a rule |

`account_id` is optional when exactly one Instagram account is connected.

## MCP server
`https://www.cueedit.io/api/mcp/mcp` (streamable HTTP) exposes the same actions as MCP tools, Instagram and Facebook Pages alike (`list_facebook_pages`, `list_facebook_posts`, `list_facebook_comments`, `reply_to_facebook_comment`, `send_facebook_dm`). Clients sign in with OAuth
(PKCE + dynamic client registration; discovery at `/.well-known/oauth-authorization-server`), or send a `ce_live_` key as a
Bearer token. Each OAuth connection is an API key named `MCP · <app>`, revocable in Settings → API keys.

## Guardrails (server-side, can't be bypassed by the caller)
- **402** `upgrade_required` — writes need Pro. Free keys can list/dry-run everything.
- **409** `already_dmed` — one DM per comment across webhook rules, backfill and API. `force:true` overrides.
- **422** `comment_too_old` — Meta only delivers private replies for comments ≤ 7 days old.
- **429** `rate_limited` — 600 DMs + 600 replies per hour per account (Meta's documented ceiling is 750).
- **502** `instagram_error` — Meta's error passed through; includes `reconnect_url` when the token is dead.

Every call is logged to `autodm_activity_log` with `source = 'api'` and the key id in `meta`, so it shows in AutoDM → Activity.

## Suggested loop for agents
1. `GET /media?limit=5` → pick the post.
2. `GET /media/{id}/comments?unhandled=1` (page through `next_cursor`) → count, show the user the summary and the message, wait for a yes.
3. Per comment: `POST …/reply` then `POST …/dm`, ~6 s apart. Stop on the first 429/402/502 and report.
4. Re-run step 2 — whatever is left is either expired or undeliverable.

## curl
```bash
KEY=ce_live_…
curl -s -H "Authorization: Bearer $KEY" https://www.cueedit.io/api/v1/media?limit=5
curl -s -H "Authorization: Bearer $KEY" "https://www.cueedit.io/api/v1/media/MEDIA_ID/comments?unhandled=1"
curl -s -X POST -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"text":"dm sent, please check"}' https://www.cueedit.io/api/v1/comments/COMMENT_ID/reply
curl -s -X POST -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"text":"here is the link: https://…"}' https://www.cueedit.io/api/v1/comments/COMMENT_ID/dm
```

## Facebook Pages (same shape, `/fb/*`)

Connect a Page in CueEdit → AutoDM → "Connect Facebook Page" (Facebook Login, you tick the Pages). Page tokens do not expire.

| Method | Path | What |
|---|---|---|
| GET | `/fb/pages` | Connected Pages + `plan` / `can_send` |
| GET | `/fb/posts?page_id=&limit=25&cursor=` | Recent Page posts with `comments_count` |
| GET | `/fb/posts/{post_id}/comments?page_id=&unhandled=1&cursor=&limit=50` | Top-level comments with `replied_by_me`, `dm_sent`, `dm_eligible` (< 7 days) + `summary` |
| POST | `/fb/comments/{comment_id}/reply` `{text, page_id?}` | Public reply under the comment |
| POST | `/fb/comments/{comment_id}/dm` `{text, page_id?, force?}` | Private reply → lands in the commenter's Messenger |

`page_id` is the CueEdit row id from `/fb/pages`; optional when exactly one Page is connected.
Same guardrails as Instagram: 402 `upgrade_required`, 409 `already_dmed`, 422 `comment_too_old` (Meta's 7-day private-reply window), 429 `rate_limited` (600/h per Page), 502 `facebook_error`.
Facebook only delivers ONE private reply per comment; the commenter can then message the Page freely.
Every call is logged to `facebook_activity_log`.

```bash
curl -s -H "Authorization: Bearer $KEY" "https://www.cueedit.io/api/v1/fb/posts?limit=5"
curl -s -H "Authorization: Bearer $KEY" "https://www.cueedit.io/api/v1/fb/posts/POST_ID/comments?unhandled=1"
curl -s -X POST -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"text":"here is the link: https://…"}' https://www.cueedit.io/api/v1/fb/comments/COMMENT_ID/dm
```

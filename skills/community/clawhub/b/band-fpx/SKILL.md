---
name: band-fpx
description: "Read BAND (band.us) group data from a shell — your bands, a band's posts and announcements, a post's comments, notices, post search, calendar events (schedules), members, chat channels with their latest message, and unread news counts — through the user's signed-in band.us browser session with the fpx CLI. Use when asked about a BAND group, its posts, upcoming events/calendar, who is in a band, chats, or what's new on BAND."
---

# BAND access (fpx)

BAND's web app calls a JSON API at `https://api-us.band.us/<vX.Y.Z>/<endpoint>`,
authed by the band.us session cookies **plus** an `md` header: base64
HMAC-SHA256 over the request's `path?query` (the query starts with `ts=<ms>`),
keyed with a per-session `secretKey` from `auth.band.us/s/login/getKey`. The
helper does all of that. It reads the cookies and secret from the signed-in tab
once via `fpx`, caches them in `~/.band-fpx/session.json` (mode 600), and
then calls the API straight from Node.

Read-only. Every endpoint and parameter below was verified live.

## One-time setup

```sh
npm install -g @fetchproxy/cli            # provides `fpx`
fpx profile add band --domain band.us
fpx profile declare band --cookie band_session --cookie ai --cookie as --cookie di --cookie BBC --cookie language --allow-in-page
fpx pair -p band                          # approve the pair code in ContextMint Bridge
```

Declare the cookies **before** pairing. A later `profile declare` can't widen an
existing grant; you'd have to remove and re-add the profile.

Needs **ContextMint Bridge** in Chrome and a signed-in `https://www.band.us/` tab.
If the bridge runs in more than one browser, each one dials the same port. A
`pair code` on stderr on every call, while stdout still carries data, is the
*other* browser being turned away. Don't approve those codes. Pinned the wrong
browser? Run `fpx trust clear fpx-band` and pair again in the right one.

## Core call

```sh
B=~/.claude/skills/band-fpx/scripts/band.mjs     # or <repo>/skills/band-fpx/scripts/band.mjs
node $B get <endpoint> [key=value ...]           # stdout = the API JSON
node $B refresh                                  # force a fresh capture from the tab
```

Values are URL-encoded for you; pass JSON values raw (quote them for the shell).
Every response is `{result_code, result_data}` on HTTP 200, and `result_code 1` is
success. Anything else exits non-zero with `result_data.message` on stderr:

- `300` means not authorized. The helper re-captures once by itself; if it still fails, open
  band.us in the paired browser (the page renews the session) and retry.
- `251`/`200` "Temporary/Unknown error" almost always means a missing or malformed parameter.
- `1000` means deleted or not found.

**Resolve-first rule:** everything is keyed by `band_no`. Run the band list
first and take `band_no` from it. Names are not accepted anywhere.

| What | Endpoint | Params |
|---|---|---|
| Your bands | `/v2.1.0/get_band_list_with_filter` | `fields=band.band_no,band.name` `include_restricted=false` (both required) |
| Band details | `/v2.3.0/get_band_information` | `band_no` |
| Feed (posts + announcements) | `/v2.0.0/get_posts_and_announcements` | `band_no` `resolution_type=4`; page with `.paging.next_params` |
| One post | `/v2.0.0/get_post` | `band_no` `post_no` |
| Comments | `/v2.3.0/get_comments` | `band_no` `content_key={"content_type":"post","post_no":N}` |
| Notices (pinned) | `/v2.0.0/get_band_notices` | `band_no` `limit` |
| Search posts | `/v2.0.0/search_posts` | `band_no` `query` |
| Events in a range | `/v1.6.0/get_schedules` | `band_no` `start_at=YYYYMMDD` `future_end_at=YYYYMMDD` `calendars=[{"is_default":true}]` |
| Upcoming events | `/v1.6.0/get_upcoming_schedules` | `band_no` `limit` |
| One event | `/v1.6.0/get_schedule` | `band_no` `schedule_id` |
| Members | `/v2.0.0/get_members_of_band` | `band_no` |
| Chat channels | `/v2.0.0/get_chat_channels` | `band_no` |
| One channel (+ latest message, participants) | `/v2.0.3/sync_chat_channel` | `channel_id` `resolution_type=4` |
| Unread counts | `/v1.2.0/get_news_count` | `without_post_news=false` `without_album_news=false` `with_chat_message_count=true` `feed_version=2` (all four) |

Chat **history** isn't on this API. The chat client uses a separate
channel, so only each channel's `latest_message` is readable here.

Exit codes: `0` ok · `2` fpx/bridge failure (not paired, no band.us tab) ·
`4` signed out or API error · `64` usage.

Ready-to-run `jq` recipes and response field names: `references/recipes.md`.

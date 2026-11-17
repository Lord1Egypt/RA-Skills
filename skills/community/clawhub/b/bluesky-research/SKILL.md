---
name: bluesky-research
description: Researches Bluesky profiles, posts, follower/follows graphs, account search, and trending topics via the Crawlora API, returning clean JSON. Use when the user wants a Bluesky account's stats, a post's thread/engagement, a Bluesky account search, or what's trending on Bluesky — instead of scraping the app or the AT Protocol API directly.
---

# Bluesky research

Look up public Bluesky profiles, author feeds, post threads, follower/follows
graphs, account search, and trending topics — all as normalized JSON from the
Crawlora API, no app scraping or direct AT Protocol client needed.

## When to use this skill

- "What's <handle>'s profile / follower count on Bluesky?"
- "Pull <handle>'s recent posts on Bluesky."
- "Show this Bluesky post's replies / thread."
- "Who follows <handle> on Bluesky?" / "Who does <handle> follow?"
- "Search Bluesky for accounts about <topic>."
- "What's trending on Bluesky right now?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Pick the job:

1. **Profile** — `/bluesky/profile` (`actor` = handle or DID). Display name,
   description, avatar/banner, follower/follows/posts counts.
2. **Author feed** — `/bluesky/author-feed` (`actor`, optional `cursor`,
   `limit`). A page of an account's posts, newest first, with engagement
   counts and any attached images/link card/quoted post.
3. **Post thread** — `/bluesky/post-thread` (`uri` = the post's `at://` URI,
   optional `depth`). The post plus its nested replies and, if it's a reply,
   its parent chain.
4. **Followers / follows graph** — `/bluesky/followers` and `/bluesky/follows`
   (`actor`, optional `cursor`, `limit`). Page through an account's followers
   or the accounts it follows.
5. **Search accounts** — `/bluesky/search-actors` (`q`, optional `cursor`,
   `limit`). Accounts matching a query against display name, handle, and
   profile description.
6. **Trending** — `/bluesky/trending-topics` (no params). Bluesky's current
   trending topics and suggested feeds.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Profile + author feed:
scripts/crawlora.sh /bluesky/profile actor=bsky.app | jq '.'
scripts/crawlora.sh /bluesky/author-feed actor=bsky.app limit=20 | jq '.'

# Search + trending:
scripts/crawlora.sh /bluesky/search-actors q="web scraping" | jq '.'
scripts/crawlora.sh /bluesky/trending-topics | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Bluesky
endpoint this skill uses.

## Examples

- **Account audit:** `/bluesky/profile` + `/bluesky/author-feed` for a
  handle to check follower count, posting cadence, and recent engagement.
- **Thread pull:** grab a post's `at://` URI from an author-feed or
  search-actors result, then `/bluesky/post-thread` to read the full
  reply tree (and parent chain if it's itself a reply).
- **Network mapping:** page `/bluesky/followers` and `/bluesky/follows` for
  an account to build its follower/following graph.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profiles/posts, sourced from the AT Protocol's
  public, credential-free AppView API; no login, no private content.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- List endpoints (`author-feed`, `followers`, `follows`, `search-actors`) are
  cursor-paginated — follow the returned `cursor` to walk beyond the first page.
- `post-thread` needs a full `at://` post URI, not a bsky.app URL — get it
  from an `author-feed` or `search-actors` result's post `uri` field.
- `trending-topics` has no params and is explicitly the least stable surface
  in this family — Bluesky may change its shape without notice.

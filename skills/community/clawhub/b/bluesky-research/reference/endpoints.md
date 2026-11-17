# bluesky-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 1 platform group(s).**

## Bluesky (11)

### `bluesky_author_feed`

- **HTTP:** `GET /bluesky/author-feed`
- **What:** A Bluesky account's posts. Returns a page of a Bluesky account's posts, newest first, including text, engagement counts, and any attached images/link card/quoted post.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_followers`

- **HTTP:** `GET /bluesky/followers`
- **What:** A Bluesky account's followers. Returns a page of a Bluesky account's followers. `actor` is required and is a handle such as `bsky.app` or a DID. `limit` is 1 to 100 (default 25); pass the returned `cursor` back to continue. Each follower has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`, and `subject` describes the account itself.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_follows`

- **HTTP:** `GET /bluesky/follows`
- **What:** Accounts a Bluesky account follows. Returns a page of the accounts a Bluesky account follows.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_post_likes`

- **HTTP:** `GET /bluesky/post-likes`
- **What:** List actors who liked a Bluesky post. Lists the accounts that liked a Bluesky post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each actor has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The post's at:// URI

### `bluesky_post_quotes`

- **HTTP:** `GET /bluesky/post-quotes`
- **What:** List quotes of a Bluesky post. Lists the Bluesky posts that quote a given post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each post has its `text`, `author`, `created_at`, `langs`, like, quote, reply and repost counts, `images` and `external` link card.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The quoted post's at:// URI

### `bluesky_post_reposted_by`

- **HTTP:** `GET /bluesky/post-reposted-by`
- **What:** List actors who reposted a Bluesky post. Lists the accounts that reposted a Bluesky post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each actor has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The post's at:// URI

### `bluesky_post_thread`

- **HTTP:** `GET /bluesky/post-thread`
- **What:** A Bluesky post and its reply tree. Returns a Bluesky post along with its nested replies (and, when the post is itself a reply, its parent chain), up to `depth` levels deep.
- **Params:** `depth` (integer, optional) — Reply-tree depth, 1-10; `uri` (string, **required**) — The post's at:// URI, e.g. from an author-feed or search-actors result's post uri field

### `bluesky_posts`

- **HTTP:** `GET /bluesky/posts`
- **What:** Look up Bluesky posts in a batch. Returns public Bluesky posts for 1-25 at:// post URIs. Missing, deleted, or blocked posts are omitted when the public AppView omits them.
- **Params:** `uris` (array, **required**) — One or more at:// post URIs (1-25); repeat the parameter for multiple URIs

### `bluesky_profile`

- **HTTP:** `GET /bluesky/profile`
- **What:** A Bluesky account's full public profile. Returns a Bluesky account's public profile: display name, description, avatar/banner images, and follower/follows/posts counts.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID (e.g. did:plc:z72i7hdynmk6r22z27h6tvur)

### `bluesky_search_actors`

- **HTTP:** `GET /bluesky/search-actors`
- **What:** Search Bluesky accounts. Returns Bluesky accounts matching a query against display name, handle, and profile description.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100; `q` (string, **required**) — Search text

### `bluesky_trending_topics`

- **HTTP:** `GET /bluesky/trending-topics`
- **What:** Bluesky's current trending topics. Returns Bluesky's current trending topics and suggested feeds, each with a link to its feed. This surface is less stable than the rest of this family -- Bluesky may change its shape without notice.
- **Params:** _none_

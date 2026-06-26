# Data sources and refresh policy

Use this skill for the user's own Douban data only.

## Refresh decision

Before analyzing, check local cache for the requested category.

- If the cache file does not exist, refresh by crawling.
- If the cache file exists but `fetched_at` is more than 7 days old, refresh by crawling.
- Otherwise, reuse the cache.

Prefer category-specific refresh over full refresh.

- Book question → refresh books first.
- Movie question → refresh movies first.
- Music or game question → refresh that category first.

## Cookie gate

If a refresh is required, verify cookie availability before crawling.

Treat cookies as unusable when:

- the cookie file is missing
- the cookie JSON is malformed
- the crawl result shows login redirection / authentication failure

If cookies are unusable, stop and ask the user for fresh cookies.

## Recommended input order

1. Fresh local cache JSON
2. Existing local cache JSON that is still within 7 days
3. Saved HTML from the user's own logged-in pages
4. New crawl from the user's own logged-in pages using cookies

## Local persistence goal

Always persist refreshed crawl results locally so later analysis does not need to re-crawl immediately.

The cache is the working truth for analysis unless a fresh crawl replaces it.

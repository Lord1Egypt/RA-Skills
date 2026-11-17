# Pagination Traps

## Termination Rule

Stop when the API says so — `has_more: false`, absent `next` cursor/link — never when a page comes back with fewer items than requested (filtered results legitimately produce short non-final pages on some APIs). Worked loop:

```
cursor = null
repeat:
  page = GET /items?limit=100&starting_after=cursor
  process(page.data)
  cursor = last item's id
until page.has_more == false
```

Defaults are small and silent: Stripe `limit` defaults to 10 (max 100), GitHub `per_page` to 30 (max 100). Request the documented max when fetching everything — 10× fewer requests against the same rate limit.

## Offset-Based

- Item inserted during pagination = duplicated item on the next page
- Item deleted during pagination = item skipped, you never see it
- `offset=1000000` + SQL = full table scan, extremely slow
- `total_count` changes between requests = progress bar lies

## Cursor-Based

- Opaque cursor + change of sort order = invalid cursor
- ID-based cursor + deleted ID = error or unexpected results
- Cursor without expiration = valid forever, inconsistencies if schema changes
- First request without a cursor can differ from cursor-based, inconsistent behavior

## Page-Based

- `page=0` vs `page=1`: inconsistent APIs, off-by-one errors
- Partial last page + same `per_page` = you don't know if there's more
- Changing `per_page` between requests = duplicated or skipped items
- `total_pages` computed with integer division = extra page if there's a remainder

## Link Headers

- `Link` header left unparsed = naive regex fails with complex URLs
- Missing `rel="next"` can mean last page OR that the API doesn't support it
- URL in Link is absolute but may have the wrong host behind a proxy
- Headers on a HEAD response differ from GET in some APIs

## Parallel Pagination

- Parallelizing pages without knowing the total = some requests to nonexistent pages
- Rate limit hit = some pages fail, incomplete result
- Processing order != page order = unordered results
- Error on one page = abort everything or continue with gaps?

## Infinite Scroll

- New item inserted while the user scrolls = item appears twice
- Page cache + updated item = stale version shown
- User scrolls fast = many pending requests, responses out of order

# Caching & cost — keep API usage low

This is a **read-only reporting** tool, so correctness is never at risk from caching — the worst
case is showing slightly stale numbers. The goal here is simply to **not hammer the NxVET API**
(which costs the server that serves it) when the same data is fetched repeatedly.

## How many calls a run makes

One report run makes a small, bounded number of `GET`s:

- 1× `/auth/me` (only if `organizationId` isn't already in `config.json` — so **cache the org id**
  in config and this call disappears on every subsequent run)
- labels for the **current** window + labels for the **previous** window (paged at 100/page)
- 1× `/devices`
- webhooks + their recent deliveries (only if the org has webhooks)

For a weekly report that's a handful of calls — but re-runs and overlapping windows can repeat
them, so we cache.

## TTL cache (why not ETag)

The NxVET API currently does **not** send `ETag` / `Cache-Control` / `Last-Modified` headers, so
conditional (`If-None-Match` → `304`) revalidation isn't available — there's nothing to validate
against. Instead `collect_stats.py` uses a small **time-based (TTL) cache** in `state/http_cache/`:

- A repeat request for the **same URL** within the TTL (default **10 minutes**) reuses the local
  copy and makes **no API call at all**.
- **Cheap re-runs.** Running the report twice while iterating, or after a crash, hits the cache.
- **Overlapping windows.** If two report runs share a window (e.g. same prior-period fetch), the
  second reads from cache.
- **Freshness is bounded.** The TTL is short so a scheduled weekly run always fetches live data.
  Override with the `CACHE_TTL_S` env var (e.g. `CACHE_TTL_S=0` to disable, `3600` for an hour).

The cache is keyed by full URL, written atomically (`.tmp` + `os.replace`), and safe to delete at
any time (`rm -rf state/http_cache/`) — the next run just repopulates it. Because this tool is
read-only and recomputes the whole report each run, a stale cache entry can at most show numbers
up to `CACHE_TTL_S` old; it can never corrupt anything.

> If NxVET adds ETag support later, upgrading this to conditional requests (revalidate instead of
> blind TTL) would make the cache both fresher and cheaper — a good future improvement.

## Don't over-fetch

- **Cache the org id** in `config.json` so `/auth/me` isn't called every run.
- **Only the window you need.** Fetch labels for the report window (+ one prior window for the
  trend), not the whole history. `collect_stats.py` stops paging once rows are older than the
  window start.
- **Skip webhook detail when there are no webhooks** — the collector already short-circuits.
- Prefer the `X-Total-Count` header for a pure count if you ever only need the total and not the
  per-day/per-device breakdown.

## No state needed beyond the cache

Unlike a poller, this tool has **no idempotency requirement** — each run recomputes the report
from scratch, so there's no processed-IDs file to maintain. The only on-disk state is the
optional HTTP cache above and the reports it writes to `output/`.

## If you schedule it

A weekly cadence (e.g. Monday 7am) is naturally low-volume. If you run it more often, the ETag
cache keeps repeat cost near zero. A missed run simply catches up next time — there's nothing to
reconcile.

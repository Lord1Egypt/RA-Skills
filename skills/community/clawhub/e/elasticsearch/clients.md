# Clients — REST Conventions, Libraries, Retries, and Timeouts

The cluster is rarely the reason an application is slow or flaky against Elasticsearch. The client configuration usually is.

## REST Conventions Worth Internalising

- Any read that takes a body may be sent as `GET` with a body or as `POST`. Proxies and some HTTP libraries strip bodies from GET — send searches as `POST` in application code and keep `GET` for the console.
- Multi-target syntax works nearly everywhere: `GET /logs-2026.*,orders/_search`, plus `ignore_unavailable`, `allow_no_indices`, and `expand_wildcards` to control what happens when a pattern matches nothing or matches a closed index.
- `?error_trace=true` returns the full Java stack behind an opaque error. `?filter_path=hits.hits._source,hits.total` trims the response server-side, which matters on large result sets.
- `?human=true` renders byte and time values as `1.2gb` / `3.5m`; leave it off in code, since machine values are the raw numbers.
- `_cat` APIs are for humans: add `?v` for headers, `&s=<col>` to sort, `&h=<cols>` to select, `&format=json` when a script must parse them. Their column sets change between versions — never parse the default output.
- Everything long-running (`_reindex`, `_update_by_query`, `_delete_by_query`, `_forcemerge`) accepts `?wait_for_completion=false` and returns a task ID for `GET /_tasks/<id>`.

## Client Configuration That Actually Matters

| Setting | Guidance |
|---|---|
| Node list | Pass **several** coordinating nodes, or one load-balancer address. A single hard-coded node is a single point of failure with no failover |
| Sniffing | Auto-discovering nodes breaks behind NAT, in Kubernetes, and on Elastic Cloud, where the published addresses are unroutable from the client. Off by default in modern clients — leave it off unless the network is flat |
| Connection pool | Size to expected concurrency, not to node count. Exhaustion shows up as latency, never as an error |
| Request timeout | Set it **per operation class**: search 1-5s, bulk 30-60s, reindex none (use tasks). One global timeout is wrong for at least one of them |
| Retries | Only on connection errors, `502/503/504`, and `429`. Never on `400` or `409` — the request is wrong or the conflict is real |
| Retry backoff | Exponential with jitter. Uniform retries from many clients after a hiccup produce a synchronised thundering herd |
| Keep-alive | On. TLS handshakes per request dominate latency for small queries |
| Compression | `http.compression` on the cluster plus client-side gzip: large win on bulk uploads and on wide `_source` responses |

## Per-Client Retry And Timeout Branch

Which row applies is the `client` variable from the Configuration table in SKILL.md; it is also the dialect every example should be emitted in. Defaults below are the shipped defaults of the official 8.x clients — none of them retries `429` out of the box except where noted, which is the single most common gap.

| `client` | Timeouts | Retries as shipped | The thing to change first |
|---|---|---|---|
| `dev-tools` | Browser-side only; the console has no cluster timeout to set | None | Nothing — but closing the tab does not cancel the task, so use `POST /_tasks/<id>/_cancel` for anything long |
| `curl` | `--connect-timeout` and `--max-time`; neither is set by default | None unless asked | `--retry N --retry-connrefused` (covers 408/429/5xx with doubling backoff). For `_bulk` use `--data-binary @file` — `-d` strips newlines and the file must end in one |
| `python` | `request_timeout` on the client, per-call via `client.options(request_timeout=...)` | `max_retries=3`, `retry_on_timeout=False`; retried statuses are configurable via `retry_on_status` | Add `429` to `retry_on_status`; use `helpers.bulk(..., raise_on_error=True)` and remember `parallel_bulk` is a generator that runs nothing until it is consumed |
| `javascript` | `requestTimeout` (30s on the 8.x client), overridable per request in the second options argument | `maxRetries: 3`, applied only to requests the client treats as retry-safe | `helpers.bulk` with `flushBytes`, `retries`, `wait`, and an `onDrop` handler — without `onDrop` the failed items disappear |
| `java` | `RestClient` defaults: connect 1s, socket 30s; change through `setRequestConfigCallback` | Fails over to the next node on connection errors within the timeout budget; no status-based retry | Raise the 1s connect timeout for anything cross-region, and use `BulkIngester` (`maxOperations`, `maxSize`, `flushInterval`) instead of hand-rolled batching |
| `go` | `Transport` timeouts on the `http.Client` you supply; none by default | `MaxRetries: 3`, `RetryOnStatus: 502, 503, 504`, `RetryBackoff` nil (retries immediately) | Add `429` to `RetryOnStatus` **and** set `RetryBackoff` — the default is an unbacked-off retry storm |
| anything else | Assume none | Assume none | Verify against that client's docs before trusting any retry behaviour |

## Server-Side Timeouts Are Not Client Timeouts

- A client timeout abandons the HTTP connection; **the query keeps running on the cluster**. A page that retries on timeout can pile up identical expensive queries until nodes fall over.
- `?timeout=5s` on a search asks shards to return partial results at the deadline, marking `timed_out: true`. It bounds the response, not the work.
- The real cancellation lever: `search.default_allow_partial_search_results`, plus `POST /_tasks/<id>/_cancel` for long analytics. Modern clients propagate cancellation when the HTTP connection drops — verify yours does before relying on it.
- `terminate_after: N` per shard is a hard cap on documents examined. It bounds cost deterministically at the price of incomplete results, which is the right trade for a "search suggestions" endpoint.

## Bulk Helpers

Every official client ships a bulk helper (`helpers.bulk` / `parallel_bulk` in Python, `helpers.bulk` in the JS client, `BulkIngester` in Java, `esutil.BulkIndexer` in Go). Use them, and check three things:

1. **Failures are surfaced.** Python's `helpers.bulk` raises by default and `raise_on_error=False` returns them instead — swallowing them is silent data loss.
2. **The chunk parameter is bytes-aware.** `chunk_size` in documents plus `max_chunk_bytes` in bytes; the byte limit is the one that maps to `bulk_batch_mb`.
3. **Back-pressure is respected.** Helpers with a `429` retry policy exist for exactly this; a helper that retries a rejection immediately at full concurrency is an amplifier.

## Connecting Securely

- `elasticsearch >=8.0` enables TLS and authentication by default on a fresh install, with a self-signed CA. Clients need the CA fingerprint or certificate — disabling verification "temporarily" is how it stays disabled.
- Prefer an **API key** over a username and password in application config: scoped, individually revocable, and it never doubles as a login.
- Elastic Cloud clients accept a `cloud_id` that carries the endpoint; it is a convenience encoding, not a credential.
- Never let a browser talk to Elasticsearch directly. Any credential shipped to a browser is public, and `_search` is a query language with expensive operations in it.

## Version Compatibility

- The 8.x clients send a compatibility header and refuse to talk to a 7.x cluster by default; the 7.17 client can talk to 8.x in compatibility mode. Plan the client upgrade as a distinct step from the cluster upgrade.
- OpenSearch forked the clients too. The Elasticsearch 8.x client rejects an OpenSearch cluster on a product-check header; use the `opensearch-py` / `opensearch-js` family instead of pinning an old Elasticsearch client forever.
- The `deployment` variable records which of these applies, so examples come out in the right dialect the first time.

## Instrumenting the Client Side

- Log the `X-Opaque-Id` header on every request. Elasticsearch echoes it into the slow log and into `_tasks`, which is the only reliable way to trace one application request to one slow query.
- Record client-observed latency separately from `took`. `took` is server-side search time only: it excludes queueing, network, and JSON deserialisation, and a gap between the two points at the client or the wire, not the cluster.
- Count retries as a first-class metric. A rising retry rate is the earliest visible sign of cluster back-pressure, well before latency alarms fire.

## Client-Side Symptoms

| Symptom | Usual cause |
|---|---|
| Intermittent connection resets | Idle connections reaped by a load balancer; lower the client's keep-alive below the LB idle timeout |
| Latency spikes only under concurrency | Connection pool exhaustion, not the cluster |
| Works in the console, fails in code | GET with a body stripped by a proxy — send `POST` |
| `429` bursts on write | Client concurrency above the write pool's capacity |
| Sudden failures after a cluster upgrade | Client version compatibility check |
| One slow endpoint, cluster metrics clean | Client-side JSON deserialisation of a huge `_source`; use `_source` filtering or `filter_path` |

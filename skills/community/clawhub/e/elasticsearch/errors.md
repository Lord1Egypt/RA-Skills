# Errors — Message to Cause to Fix

Match on the exception **type**; message text changes between versions. The short table of the most frequent ones is in SKILL.md; this is the full catalog.

## Reading a Failure

- `search_phase_execution_exception` is an envelope, never the cause. The real error is in `failed_shards[0].reason`, sometimes nested two levels deep. Add `?error_trace=true` when even that is opaque.
- A partial failure returns HTTP 200 with `_shards.failed > 0`. Code that only checks the HTTP status treats a half-empty result set as success — check `_shards.failed` on every search that matters.
- `_bulk` returns HTTP 200 with per-item failures. Check the `errors` flag.

## Mapping and Document Errors

| Exception / message | Cause | Fix |
|---|---|---|
| `mapper_parsing_exception: failed to parse field [x] of type [long]` | A string arrived where a number is mapped | Fix the producer, add a `convert` ingest processor, or set `ignore_malformed` if the field is optional junk |
| `illegal_argument_exception: mapper [x] cannot be changed from type [a] to [b]` | Attempting to change a mapped type | Impossible in place: new index → reindex → alias swap (SKILL.md Core Rules 3) |
| `strict_dynamic_mapping_exception: mapping set to strict, dynamic introduction of [x] is not allowed` | A field not in the mapping arrived | Add the field to the mapping, or fix the typo in the producer — this exception is the feature working |
| `Limit of total fields [1000] has been exceeded` | Mapping explosion from dynamic keys | `dynamic: strict` or a `flattened` field; raising the limit postpones the failure |
| `Limit of nested fields [50] has been exceeded` | Too many distinct `nested` fields | Reconsider the model — usually denormalization is the answer |
| `The number of nested documents has exceeded the allowed limit of [10000]` | One parent document with too many nested children | Split the document, or index children separately with a parent ID |
| `document_missing_exception` | `_update` on a non-existent `_id` | Use `upsert`, or `doc_as_upsert: true` |
| `version_conflict_engine_exception` | Concurrent write to the same `_id`, or a `_by_query` snapshot conflict | `retry_on_conflict` for updates, `if_seq_no`+`if_primary_term` for read-modify-write, `conflicts: proceed` for bulk-by-query |
| `max_bytes_length_exceeded_exception: bytes can be at most 32766 in length` | A single keyword term exceeds Lucene's limit | `ignore_above` on the field, or hash the value before indexing |
| `illegal_argument_exception: Document contains at least one immense term` | Same cause, from the analyzer side | A `truncate` or `length` token filter |

## Query Errors

| Exception / message | Cause | Fix |
|---|---|---|
| `Fielddata is disabled on text fields by default` | Aggregating or sorting on `text` | The `.keyword` sub-field (SKILL.md Core Rules 9) |
| `parsing_exception: [x] query malformed, no start_object after query name` | A brace in the wrong place; a query name where an object is expected | `_validate/query?explain=true` |
| `query_shard_exception: No mapping found for [x] in order to sort on` | Sorting on a field absent in one index behind the alias | `unmapped_type` on the sort clause, or fix the divergent mapping |
| `Result window is too large, from + size must be less than or equal to [10000]` | Deep pagination | `search_after` + PIT (Core Rules 8) |
| `too_many_buckets_exception: Trying to create too many buckets` | Aggregation exceeded `search.max_buckets` (65,536) | Narrow the range, coarsen the interval, or use `composite` |
| `circuit_breaking_exception: [request] Data too large` | One request wants too much heap | Shrink the aggregation or the batch |
| `search_context_missing_exception` | Scroll or PIT expired or was never closed | Longer `keep_alive`, or migrate to `search_after` |
| `Trying to query [x] shards, which is more than the maximum of [1000]` | `action.search.shard_count.limit` on a wildcard spanning too many indices | Narrow the index pattern; the real fix is fewer, bigger shards |
| `[knn] queries are only supported on [dense_vector] fields` | kNN against a field mapped with `index: false` or the wrong type | Remap and reindex |
| `illegal_argument_exception: [fuzziness] cannot be [x] for type [long]` | Fuzziness on a non-text field | Fuzziness applies to analyzed text only |
| `Too many dynamic script compilations within...` | Values interpolated into script source | Move them to `params` |
| `[query_string] failed to parse query` | User input reached `query_string` | `simple_query_string` |

## Cluster and Node Errors

| Exception / message | Cause | Fix |
|---|---|---|
| `cluster_block_exception ... read-only / allow delete (api)` | Flood-stage disk watermark | Free disk; auto-clears on `elasticsearch >=7.4` |
| `cluster_block_exception ... blocked by: [SERVICE_UNAVAILABLE/1/state not recovered]` | Master elected but cluster state not yet loaded | Wait; if it persists, quorum is not met |
| `es_rejected_execution_exception` | A thread-pool queue filled | Back off and reduce concurrency; the queue is not the problem |
| `Validation Failed: this action would add [x] total shards, but this cluster currently has [y]/[1000] maximum shards open` | `cluster.max_shards_per_node` reached | Delete or shrink indices; raising the limit trades an error for a heap problem |
| `unavailable_shards_exception ... Primary shard is not active` | Writing during a failover or recovery | Retry with backoff; investigate if it lasts |
| `NoNodeAvailableException` / `ConnectionError` (client-side) | Every configured node unreachable, or TLS verification failing | Node list, network, certificate chain |
| `master_not_discovered_exception` | No quorum among master-eligible nodes | `discovery.seed_hosts`, network partition, node count |
| `index_not_found_exception` on a wildcard | Pattern matched nothing | `ignore_unavailable=true`, or the alias was never swapped |
| `resource_already_exists_exception` | Index name taken, often by an auto-created index | Disable `action.auto_create_index` for managed patterns |
| `illegal_state_exception: environment not locked` / `failed to obtain node locks` | Two processes on one data path, or a stale lock | One node per data path; clear the lock after an unclean shutdown |
| `snapshot_missing_exception` / `repository_missing_exception` | Repository not registered on this node, or the snapshot was deleted | Register the repository on **every** master and data node |

## Security and Authorization

| Exception / message | Cause | Fix |
|---|---|---|
| `security_exception: missing authentication credentials` | No credentials, or the client dropped them on a redirect | API key or basic auth on every request |
| `security_exception: action [indices:data/read/search] is unauthorized for user [x] on indices [y]` | Role lacks the privilege or the index pattern | Read the action name in the message — it maps directly to a privilege |
| `SSLHandshakeException: PKIX path building failed` | Client does not trust the cluster's CA | Supply the CA certificate or fingerprint; do not disable verification |
| `Received plaintext http traffic on an https channel` | Client using `http://` against a TLS-enabled cluster | `elasticsearch >=8.0` enables TLS by default |
| `current license is non-compliant for [x]` | Feature above the licensed tier | `license_tier` variable; choose the open-tier alternative |

## Errors With No Error

The dangerous class: HTTP 200 and a wrong answer.

| Symptom | Cause |
|---|---|
| Zero hits on a value you can see in `_source` | `term` on a `text` field, or a case mismatch on `keyword` (Core Rules 1) |
| A field is in `_source` but unqueryable | `dynamic: false`, or `ignore_above` skipped the value at index time |
| Query matches objects on the wrong field combination | Array of objects flattened; needs `nested` |
| `hits.total` stuck at exactly 10,000 | `track_total_hits` default; `"relation": "gte"` is right there in the response |
| Aggregation counts slightly off | `terms` shard-level approximation — read `doc_count_error_upper_bound` |
| Distinct count slightly off | `cardinality` is HyperLogLog++, always an estimate |
| A `nested` aggregation's `doc_count` too high | Counting nested children, not parents — needs `reverse_nested` |
| Results reshuffle between identical requests | Per-shard IDF, or a tie on `_score` with no tiebreak sort |
| Everything matches after an autocomplete change | `edge_ngram` applied as the search analyzer too |
| Geo results in the wrong hemisphere | Array coordinate order is `[lon, lat]` |

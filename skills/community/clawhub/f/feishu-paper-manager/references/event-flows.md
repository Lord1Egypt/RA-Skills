# Event Flows

Use this reference when implementing event sequencing, retries, and user-visible responses.

## Flow 1: New PDF paper

```text
Feishu message event
  -> verify webhook
  -> parse message and detect PDF candidate
  -> build normalized ingestion payload
  -> call OpenClaw ingest
  -> extract metadata from PDF or fallback source
  -> deduplicate against existing records
  -> upload PDF to cloud-docs paper folder
  -> generate one-line summary and tags
  -> create or update table row
  -> evaluate 50-row threshold
  -> return structured result
  -> bot replies with confirmation and links
```

Expected reply shape:

- title
- doc link
- table status such as `created` or `updated`
- one-line summary
- tags

## Flow 2: Source link only

```text
Feishu message event
  -> verify webhook
  -> parse message and detect source URL
  -> build normalized ingestion payload
  -> call OpenClaw ingest
  -> resolve external ID and title from URL
  -> deduplicate against existing records
  -> create link-index doc in paper folder
  -> generate one-line summary and tags
  -> create or update table row
  -> evaluate threshold
  -> return result
  -> bot replies with confirmation
```

If metadata extraction is incomplete:

- still create a row if title and source link are trustworthy
- mark `status = new` or `classified` based on how complete the classification is
- keep the workflow resumable

## Flow 3: Duplicate paper

```text
message event
  -> parse candidate
  -> call OpenClaw ingest
  -> detect existing canonical row before write
  -> patch missing metadata if needed
  -> skip new file upload unless the existing record lacks the artifact
  -> return duplicate result
  -> bot replies with canonical record link
```

Expected duplicate reply:

- note that the paper already exists
- include canonical title
- include existing doc link
- mention whether any missing fields were updated

## Flow 4: Threshold-triggered taxonomy review

```text
successful canonical upsert
  -> count canonical rows
  -> if count % 50 != 0, stop
  -> if review checkpoint already equals count, stop
  -> launch taxonomy review
  -> analyze current tag frequencies and collisions
  -> produce new taxonomy version
  -> backfill historical rows
  -> persist checkpoint and new version
  -> return review summary
```

Do not run the review on raw message count. Use canonical non-duplicate paper count.

## Retry behavior

Treat these as retryable:

- temporary Feishu API failures
- transient network failures
- rate limits
- OpenClaw worker interruption before final commit

Treat these as non-retryable without payload change:

- invalid webhook signature
- unsupported file type
- missing required identifiers after extraction
- malformed table schema configuration

## Commit order

Prefer this write order to reduce corruption:

1. deduplication lookup
2. cloud-docs write or reuse existing artifact
3. table upsert
4. taxonomy threshold checkpoint update
5. bot confirmation

If step 2 succeeds and step 3 fails, require either:

- a resumable reconciliation job
- or a deterministic artifact naming rule that lets the next retry reuse the prior upload

## Example bot replies

### Created

```text
Paper saved
Title: Example Paper
Doc: https://...
Summary: Uses retrieval-augmented planning to improve long-horizon agent decisions.
Tags: agent, retrieval, rag, planning
```

### Duplicate

```text
Paper already exists
Title: Example Paper
Canonical doc: https://...
Updated: missing source link added
```

### Review triggered

```text
Paper saved
Taxonomy review triggered at 100 papers
Version: v2 -> v3
Updated rows: 100
```

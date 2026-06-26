# Xiaoyuzhou Podcast Support Design

## Background

`tech-news` already supports podcast sources through `scripts/fetch-podcast.py`. The existing pipeline treats podcast episodes as article-compatible items, then reuses the merge, scoring, and digest rendering paths. RSS podcast feeds work without extra tools, and YouTube podcast sources use optional `yt-dlp` for metadata and transcripts.

Xiaoyuzhou support should fit into this existing podcast model instead of becoming a separate source layer. Xiaoyuzhou content often requires authorization, and duplicating Xiaoyuzhou API headers, token refresh behavior, or private endpoint semantics in this repository would create a brittle maintenance burden. OpenCLI already provides a Xiaoyuzhou adapter and owns that integration surface.

## Goals

- Add Xiaoyuzhou as a podcast platform under the existing `type: "podcast"` source model.
- Use OpenCLI as the only Xiaoyuzhou backend.
- Keep Xiaoyuzhou source failures isolated from the rest of the pipeline.
- Reuse the existing podcast episode shape and `transcript_status` contract.
- Support optional transcript enrichment through OpenCLI when configured and available.
- Keep tests deterministic by mocking subprocess output instead of requiring real Xiaoyuzhou credentials.

## Non-Goals

- Do not parse Xiaoyuzhou public HTML as a fallback.
- Do not call Xiaoyuzhou API endpoints directly from this repository.
- Do not implement Xiaoyuzhou token refresh, app headers, or credential extraction.
- Do not download episode audio.
- Do not change merge or digest behavior specifically for Xiaoyuzhou.
- Do not require CI to have OpenCLI or Xiaoyuzhou credentials.

## Recommended Architecture

Add `xiaoyuzhou` as a supported `platform` value for podcast sources.

```text
sources.json
  -> scripts/fetch-podcast.py
  -> platform == "xiaoyuzhou"
  -> opencli xiaoyuzhou podcast-episodes <pid> --limit <n> -f json
  -> optional: opencli xiaoyuzhou transcript <eid> --output <tmpdir> -f json
  -> normalized podcast episodes
  -> existing merge and digest pipeline
```

The Xiaoyuzhou implementation should live inside `scripts/fetch-podcast.py` beside the RSS and YouTube platform handlers. It should expose small, testable helpers for URL parsing, OpenCLI availability, JSON command execution, episode normalization, and transcript enrichment.

`merge-sources.py`, digest rendering, and scoring should not need Xiaoyuzhou-specific branches. The normalized episode output should already satisfy the existing podcast contract.

## Source Configuration

Example source:

```json
{
  "id": "whynottv-podcast",
  "type": "podcast",
  "name": "WhynotTV Podcast",
  "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
  "platform": "xiaoyuzhou",
  "topics": ["podcast"],
  "priority": true,
  "enabled": true,
  "transcript": {
    "enabled": true,
    "backend": "opencli"
  }
}
```

Schema changes:

- Add `xiaoyuzhou` to `platform`.
- Add `opencli` to `transcript.backend`.

`platform: "auto"` should infer `xiaoyuzhou` for hosts matching `xiaoyuzhoufm.com` or `www.xiaoyuzhoufm.com` with a `/podcast/<pid>` path.

## OpenCLI Contract

The fetcher should call OpenCLI with JSON output only:

```text
opencli xiaoyuzhou podcast-episodes <pid> --limit 20 -f json
```

The first implementation should depend only on the narrow output fields needed to build an episode:

- `eid`
- `title`
- `date`

Other fields such as duration and play count may be preserved later if they become useful, but they are not required for the pipeline contract.

Transcript enrichment should call:

```text
opencli xiaoyuzhou transcript <eid> --output <tmpdir> -f json
```

The fetcher should read the returned `text_file` when present. If the file exists and contains non-empty text, attach it to the episode as `transcript` and set `transcript_status` to `ok`.

## Episode Output

Xiaoyuzhou episodes should normalize to the existing podcast episode shape:

```json
{
  "title": "Danfei Xu: Human Data and Robot Learning",
  "link": "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
  "date": "2026-05-01T00:00:00+00:00",
  "guid": "xiaoyuzhou:69f441cd5390b7cc928acdcc",
  "topics": ["podcast"],
  "show_name": "WhynotTV Podcast",
  "platform": "xiaoyuzhou",
  "transcript_status": "ok",
  "transcript": "..."
}
```

OpenCLI `podcast-episodes` currently exposes dates as day-level values. The fetcher should parse `YYYY-MM-DD` as UTC midnight. This is precise enough for digest recency filtering and avoids pretending to know the original publication timestamp.

If transcript enrichment is disabled or fails, the episode should still be emitted:

```json
{
  "title": "Danfei Xu: Human Data and Robot Learning",
  "link": "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
  "date": "2026-05-01T00:00:00+00:00",
  "guid": "xiaoyuzhou:69f441cd5390b7cc928acdcc",
  "topics": ["podcast"],
  "show_name": "WhynotTV Podcast",
  "platform": "xiaoyuzhou",
  "transcript_status": "missing",
  "transcript_error": "..."
}
```

## Error Handling

Xiaoyuzhou metadata failures should fail only the current source:

- Missing OpenCLI: source `status = "error"` with an actionable message.
- Missing Xiaoyuzhou credentials: source `status = "error"` and mention `~/.opencli/xiaoyuzhou.json`.
- Invalid podcast URL or missing `pid`: source `status = "error"`.
- Non-zero OpenCLI exit: source `status = "error"` with a short stderr/stdout excerpt.
- Invalid JSON or unexpected shape: source `status = "error"`.

Transcript failures should not fail the source:

- Missing transcript command support: set `transcript_status = "backend_unavailable"`.
- Missing credentials during transcript fetch: set `transcript_status = "backend_unavailable"` or `error`, preserving the episode.
- Empty transcript result: set `transcript_status = "missing"`.
- Non-empty transcript file: set `transcript_status = "ok"`.
- Parse or file-read failures: set `transcript_status = "parse_error"` or `error`.

All error strings stored in output should be short and display-safe.

## Caching

The existing podcast cache can be reused.

Metadata cache key should include:

- platform: `xiaoyuzhou`
- podcast id
- max episode limit
- cache version

Transcript cache key should continue to include the source identity plus episode guid:

```text
<source-id>:xiaoyuzhou:<eid>
```

Successful transcript results can use the existing long TTL. Transcript failures should use the existing short TTL so daily runs do not repeatedly hit unavailable transcripts.

## Affected Files

- `scripts/fetch-podcast.py`
  - infer Xiaoyuzhou platform
  - extract podcast id from Xiaoyuzhou URL
  - invoke OpenCLI JSON commands
  - normalize Xiaoyuzhou episodes
  - enrich transcripts through OpenCLI

- `config/schema.json`
  - allow `platform: "xiaoyuzhou"`
  - allow `transcript.backend: "opencli"`

- `scripts/validate-config.py`
  - mirror the schema validation rules.

- `tools/config-editor/server.py`
  - allow the new platform and transcript backend.

- `tools/config-editor/app.js`
  - include the new values in table dropdowns.

- `tools/config-editor/README.md`
  - document the new editable values.

- `tests/test_fetch_podcast.py`
  - cover URL inference, OpenCLI command mapping, normalization, source-level failures, and transcript outcomes with mocked subprocesses.

- `tests/test_config.py` and `tests/test_config_editor_server.py`
  - cover schema and editor validation for the new enum values.

## Verification Plan

Unit tests:

- `infer_platform()` returns `xiaoyuzhou` for Xiaoyuzhou podcast URLs.
- Xiaoyuzhou podcast URL parsing extracts the correct `pid`.
- Invalid Xiaoyuzhou URLs return source-level errors.
- OpenCLI metadata output normalizes to podcast episode shape.
- OpenCLI missing or credential errors fail only the Xiaoyuzhou source.
- Transcript success attaches `transcript` and sets `transcript_status = "ok"`.
- Transcript failures preserve the episode and set a non-ok `transcript_status`.
- RSS and YouTube podcast tests keep passing.

Suggested commands after implementation:

```text
python3 -m unittest tests.test_fetch_podcast tests.test_config tests.test_config_editor_server -v
python3 scripts/validate-config.py --defaults config/defaults --verbose
python3 scripts/fetch-podcast.py --defaults config/defaults --hours 1 --output /tmp/td-podcast.json --force --verbose
```

Manual smoke test with credentials:

```text
opencli xiaoyuzhou podcast-episodes 686a1832222ae2de21fea940 --limit 5 -f json
python3 scripts/fetch-podcast.py --defaults config/defaults --config <workspace-config> --hours 720 --output /tmp/td-xiaoyuzhou.json --force --verbose
```

The manual smoke test requires OpenCLI plus `~/.opencli/xiaoyuzhou.json`. It should not be required in CI.

## Risks

- OpenCLI output could change. Mitigation: call `-f json`, depend on only a small set of fields, and test normalization against fixtures.
- Xiaoyuzhou credentials can expire. Mitigation: delegate credential refresh and API behavior to OpenCLI.
- Day-level publication dates are less precise than RSS timestamps. Mitigation: convert to UTC midnight and document the precision.
- Transcript fetching may be slow or unavailable. Mitigation: keep transcript failures per episode and reuse the existing cache.

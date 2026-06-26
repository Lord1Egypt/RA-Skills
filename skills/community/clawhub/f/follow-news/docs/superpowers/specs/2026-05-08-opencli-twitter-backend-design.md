# OpenCLI Twitter Backend Design

## Context

`follow-news` currently gathers Twitter/X posts through API-based backends in `scripts/fetch-twitter.py`: GetXAPI, twitterapi.io, and the official X API. This creates a setup burden for users because Twitter/X data requires API credentials.

The goal is to make OpenCLI the default Twitter/X backend while keeping the rest of the collection pipeline unchanged. RSS, Web, GitHub, GitHub Trending, and Reddit sources remain as they are. The change is intended for OpenClaw agents, where the `jackwener/opencli` skill may already be installed and can guide the agent through OpenCLI setup, discovery, and browser-login diagnostics.

## Goals

- Use OpenCLI as the first backend for Twitter/X collection in `auto` mode.
- Preserve existing Twitter output shape so `merge-sources.py` does not need OpenCLI-specific logic.
- Keep API backends as fallback options for CI, headless environments, and users who already configured API keys.
- Support local-first operation through Chrome/Chromium login state.
- Document OpenClaw-facing behavior so agents can use the `jackwener/opencli` skill to prepare and diagnose OpenCLI.
- Design the backend so topic-level Twitter search can be added later without rewriting account timeline collection.

## Non-Goals

- Do not change RSS, Web, GitHub, GitHub Trending, or Reddit collection.
- Do not enable topic-level Twitter keyword search by default in the first implementation.
- Do not install OpenCLI or browser extensions from this skill.
- Do not remove existing API-based Twitter backends.
- Do not require CI to have a browser login state.

## Recommended Approach

Add an `OpenCliBackend` implementation inside `scripts/fetch-twitter.py` and make `auto` select backends in this order:

```text
opencli -> getxapi -> twitterapiio -> official -> empty result
```

The explicit `opencli` backend uses only OpenCLI. It should not silently fall back to API backends, because explicit backend selection should be predictable. If explicit OpenCLI mode cannot run, it writes an empty Twitter result with actionable diagnostics, matching the current non-fatal behavior for missing Twitter credentials.

## Architecture

`OpenCliBackend` fits into the existing `TwitterBackend` abstraction:

- `fetch_all(sources, cutoff)` accepts existing `type=twitter` source configs from `sources.json`.
- Each source is fetched by account handle.
- OpenCLI JSON output is normalized into the same article shape used by existing Twitter backends.
- The normalized result is returned as the existing per-source structure with `source_id`, `source_type`, `name`, `handle`, `priority`, `topics`, `status`, `attempts`, `count`, and `articles`.

The downstream pipeline remains unchanged:

```text
config/defaults/sources.json
  -> scripts/fetch-twitter.py
  -> twitter.json
  -> scripts/merge-sources.py
  -> quality scoring, deduplication, topic grouping
  -> digest output
```

## OpenClaw Skill Integration

There are two separate dependency layers:

- Agent layer: the `jackwener/opencli` skill explains how an OpenClaw agent should discover OpenCLI commands, run diagnostics, and resolve browser-login issues.
- Script layer: `scripts/fetch-twitter.py` can only execute a process. It needs a concrete OpenCLI executable, discovered from `OPENCLI_BIN` first and then from `PATH`.

`SKILL.md` should describe OpenCLI as an optional capability:

- Add `opencli` to `metadata.openclaw.optionalBins`.
- Document `TWITTER_API_BACKEND=auto|opencli|getxapi|twitterapiio|official`.
- Document `OPENCLI_BIN` as an optional override for the OpenCLI executable path.
- Explain that when OpenClaw has installed `jackwener/opencli`, the agent should use that skill to validate OpenCLI before asking the user for Twitter API keys.

`references/digest-prompt.md` should also prefer OpenCLI diagnostics when Twitter/X data is requested and OpenCLI is available.

## OpenCLI Discovery

`OpenCliBackend` should perform lightweight discovery before account fetches:

1. Resolve executable:

```text
OPENCLI_BIN if set, otherwise opencli from PATH
```

2. Verify OpenCLI capability:

```text
opencli list -f json
```

The backend should confirm that a Twitter tweets command is available. The implementation should avoid hardcoding more OpenCLI command details than necessary, but it must still validate that the required account-tweets capability exists.

3. Verify browser/login readiness:

```text
opencli doctor
```

If `doctor` is unavailable or inconclusive, the first real tweets command can serve as the final readiness check. Auth-like failures should be categorized separately from per-account content failures.

## Data Normalization

OpenCLI tweet records must normalize into the existing article format:

```json
{
  "title": "Tweet text",
  "link": "https://x.com/handle/status/id",
  "date": "2026-05-08T00:00:00+00:00",
  "topics": ["llm"],
  "metrics": {
    "like_count": 0,
    "retweet_count": 0,
    "reply_count": 0,
    "quote_count": 0,
    "impression_count": 0
  },
  "tweet_id": "..."
}
```

Normalization rules:

- Skip records without usable text, ID, or date.
- Skip retweets when OpenCLI marks them as retweets.
- Also skip records whose text starts with `RT @`.
- Preserve current cutoff filtering based on `--hours`.
- Use OpenCLI-provided URLs when present.
- If URL is missing, build `https://x.com/{handle}/status/{tweet_id}`.
- If metrics are absent, default each metric to `0`.
- Reuse the existing `clean_tweet_text` behavior.

Reply handling should follow existing behavior when OpenCLI provides reply metadata. If reply metadata is missing, the first implementation should not guess from text alone.

## Future Topic Search

The first implementation only fetches configured KOL accounts. It should still keep account timeline and topic search as separate internal paths:

- `fetch_account_tweets(source, cutoff)`
- `fetch_search_results(topic_query, cutoff)`
- shared `normalize_tweet_record(...)`

This keeps the first implementation narrow while leaving room to later connect `topics.json` `twitter_queries` as topic-level search inputs. Search results should not be enabled by default until result quality, duplicate rates, and OpenCLI rate behavior are evaluated separately.

## Error Handling

OpenCLI errors should be classified so OpenClaw agents can act on them:

- `opencli_missing`: no executable from `OPENCLI_BIN` or `PATH`.
- `opencli_capability_missing`: OpenCLI exists but does not expose the Twitter tweets capability.
- `opencli_browser_unavailable`: browser bridge, extension, or Chrome/Chromium login state is unavailable.
- `opencli_auth_required`: X/Twitter login is required or expired.
- `opencli_timeout`: command exceeded the configured timeout.
- `opencli_parse_error`: command returned JSON that could not be parsed into tweet records.
- `opencli_source_error`: one account failed while the backend remains usable for other accounts.

In `auto` mode, global OpenCLI setup/auth failures should move to the next backend before spending time on all configured accounts. Per-account failures should be recorded on that source and should not fail the whole backend.

In explicit `opencli` mode, global OpenCLI setup/auth failures should write an empty Twitter result with diagnostics instead of trying API fallback.

## Fallback Behavior

Backend selection:

```text
auto:
  OpenCLI
  -> GetXAPI when GETX_API_KEY is set
  -> twitterapi.io when TWITTERAPI_IO_KEY is set
  -> official X API when X_BEARER_TOKEN is set
  -> empty twitter.json

opencli:
  OpenCLI
  -> empty twitter.json with diagnostics
```

This supports local-first OpenCLI usage and CI compatibility. CI can keep using API keys, or it can skip Twitter and still generate the rest of the digest.

## CLI and Configuration Changes

`scripts/fetch-twitter.py` should accept:

```text
--backend opencli
```

`scripts/run-pipeline.py` and `scripts/test-pipeline.sh` should accept `opencli` in Twitter backend choices.

Environment variables:

```text
TWITTER_API_BACKEND=auto|opencli|getxapi|twitterapiio|official
OPENCLI_BIN=/path/to/opencli
```

README files and `SKILL.md` should describe OpenCLI as the preferred Twitter/X backend in `auto` mode, with API backends as fallback.

## Testing Strategy

Automated tests should not require real X/Twitter access.

Unit tests:

- Normalize OpenCLI tweet fixtures into existing article shape.
- Filter tweets older than the cutoff.
- Skip retweets and malformed tweet records.
- Default missing metrics to `0`.
- Build fallback links when URLs are missing.
- Classify OpenCLI discovery, capability, auth, timeout, and parse failures.
- Verify `auto` selection falls back when OpenCLI is unavailable.

Integration-style tests:

- Feed OpenCLI-normalized `twitter.json` into `merge-sources.py` and verify the merged output still contains scored Twitter articles.
- Verify README and `SKILL.md` backend enums stay in sync with code.

Manual validation:

```bash
python3 scripts/fetch-twitter.py --backend opencli --hours 24 --output /tmp/td-twitter.json --verbose --force
python3 scripts/run-pipeline.py --only twitter --twitter-backend opencli --debug --force
python3 -m unittest discover -s tests -v
```

## Risks

- OpenCLI output schema may evolve. Mitigation: keep normalization tolerant and fixture-driven.
- Browser login state is not portable to CI. Mitigation: keep API fallback and empty-result behavior.
- OpenCLI commands may be slower than API calls for 48 accounts. Mitigation: use bounded concurrency and backend-level timeout thresholds.
- X/Twitter UI or auth changes may break OpenCLI. Mitigation: classify failures and direct agents to the `jackwener/opencli` skill for repair.
- Topic-level search may add noise. Mitigation: keep search disabled in the first implementation and evaluate separately.

## Acceptance Criteria

- `TWITTER_API_BACKEND=auto` attempts OpenCLI before API backends.
- `--backend opencli` runs only OpenCLI and emits clear diagnostics on failure.
- Existing API backends still work.
- Twitter output shape remains compatible with `merge-sources.py`.
- RSS, Web, GitHub, GitHub Trending, and Reddit behavior is unchanged.
- OpenClaw-facing docs explain the relationship between `follow-news` and `jackwener/opencli`.
- Tests cover normalization, backend selection fallback, and merge compatibility without real X/Twitter access.

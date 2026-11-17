---
name: app-release-feedback-analysis
description: Compare app review themes around documented releases using Crawlora version notes and live/stored reviews. Use for a dated release-feedback brief with platform/app/version identity, review timestamps, sampling, missing release history, and causal limits preserved.
---

# App release feedback analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Describe observed feedback around a specified release or release set. Establish
platform, exact app ID, storefront/language, release dates/versions, review window,
and comparable sampling rules before collecting evidence.

## Align releases and review observations

- Resolve iOS numeric track IDs and Android package IDs separately. Verify
  publisher/title/domain before cross-platform grouping. App Store version
  history supplies release notes/dates; Google Play detail supplies current app
  context, not a complete historical release timeline here. If a needed Android
  release date is not verified elsewhere or supplied by the user, leave the
  historical comparison unavailable rather than inventing a version-history route.
- Preserve release version, notes, date precision, platform/storefront and source.
  Dates can differ by market or rollout; a nominal release date does not prove
  every reviewer had the same version. Generic release notes are publisher claims,
  not evidence a reported issue was actually fixed.
- Collect matching live/stored review samples. Stored filters include store,
  exact app ID, country, minimum score and sort, but no date/version parameter;
  filter returned dates/versions locally and respect the result window. Helpful-
  ranked or score-filtered samples need their own disclosed selection bias.
- Deduplicate by source review ID and retain update/observation timestamps.
  A review's displayed version is stronger attribution than proximity to a
  release date; keep explicit-version, time-only, conflicting and unknown matches
  separate. Developer replies are not customer reviews or independent verification.

```sh
scripts/crawlora.sh /appstore/search term="note taking" country=us
# Resolve an exact app ID before release notes and eligible review collection:
# scripts/crawlora.sh /datasets/apps-reviews/search store=ios app_id="$TRACK_ID" country=us sort=recent page=1 page_size=10
```

## Report changes without claiming an experiment

Use the same theme rubric and source/window/sample budget before and after.
Count unique eligible reviews and show `theme n / review N` with dates and
version-attribution basis. Multi-theme counts can exceed N. Unknown/undated
reviews are a separate bucket, not silently placed into a preferred interval.
Cross-store star populations and filtered samples are not interchangeable.

Return a release and attribution ledger, comparable theme tables, short cited
review excerpts, notes/reply observations, missing data and follow-up hypotheses.
A change in sampled themes or average stars is not proof the release caused it:
rollouts, selection, moderation, seasonality and changing users can differ.
Do not infer crash rates, retention, install volume, or population improvement
from reviews alone. Do not install apps, run private telemetry, contact reviewers,
or schedule monitoring from this research request.

---
name: broadcast-coverage-comparison
description: Compare indexed television coverage across stations and shows with Crawlora GDELT TV search, charts, timelines, and discovery. Use for a bounded broadcast topic brief with speech/caption/OCR/visual channels, station windows, processing lag, and metric denominators kept distinct.
---

# Broadcast coverage comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare how a topic is represented in GDELT's indexed television material.
Establish stations/shows, topic terms, match channel, date window, and comparison
metric before querying. This describes indexed coverage, not public opinion or
verified audience exposure.

## Discover coverage and define equivalent queries

- Use station details to discover allowed station codes and their available
  windows. Confirm actual channel/time coverage rather than assuming every
  declared station has the same archive or processing freshness. Public TV index
  results can lag broadcasts; recent absence may be processing delay.
- Keep human captions, machine speech-to-text, OCR onscreen text, extracted
  concepts, and computer-vision labels separate. Discover concept MID/visual
  values from their catalogs. A visual/concept label is a machine/index signal,
  not verified presence, identity, sentiment, or an endorsement.
- Build matching query ledgers for compared stations. Repeated positive terms
  within one channel are OR'd; exclusions require absence. A station/exclusion-
  only query is invalid: supply a positive content field. Short speech/OCR terms
  have the documented five-word cap. Do not add a hypothetical free-text query field.
- Use either relative `timespan` or an absolute `from`/`to` window, not both.
  Station chart accepts repeated station parameters; per-station timelines need
  the relevant station. Store exact query, raw timestamps, source URL, and cutoff.

```sh
scripts/crawlora.sh /gdelt/tv-stationdetails
scripts/crawlora.sh /gdelt/tv-stationchart station=CNN station=MSNBC caption="climate change" timespan=7d
scripts/crawlora.sh /gdelt/tv-timeline station=CNN caption="climate change" timespan=7d
```

## Compare metrics and inspect supporting material

Station-chart `count` is a raw match count; show-chart `count` is a percentage
of matching results; timeline values describe matched airtime/volume according
to their returned metric. Preserve units and denominators rather than treating
all three as counts or comparable shares. Timeline resolution is auto-selected
from the window; there is no TV `smooth` parameter. Compare actual timestamp
bins and label unavailable periods instead of filling them with zero.

Inspect a bounded clip/search sample with timestamps and source links to qualify
framing, false matches, or repeated segments. Several matches within a broadcast
are not unique viewers, distinct stories, or independent reporting. Quote briefly
and attribute captured speech/text; OCR/ASR output is not a verified transcript.
Do not compute total-airtime shares or cross-station audience shares without
compatible denominators supplied by an independent source.

Return a query/coverage ledger, metric-specific comparison tables/timelines,
sampled material, processing and coverage gaps, and supported framing observations.
More indexed coverage does not establish belief, endorsement, bias, popularity,
or a causal effect on an audience. Do not schedule tracking or contact stations
from a one-off comparison request.

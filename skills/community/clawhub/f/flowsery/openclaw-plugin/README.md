# Flowsery plugin for OpenClaw

Privacy-first web analytics inside OpenClaw. Visitors, trends, 25 breakdown
dimensions, live visitor count, and the issues AI found in session recordings.

## Install

```bash
openclaw plugins install clawhub:@flowsery/openclaw-plugin
openclaw plugins enable flowsery
openclaw gateway restart
```

Create a workspace token at [flowsery.com](https://flowsery.com) under API
Tokens.

```json5
{
  plugins: {
    entries: {
      flowsery: {
        enabled: true,
        config: { apiKey: "flow_ws_..." }
      }
    }
  }
}
```

A workspace token spans every site in the workspace, so each query needs a
`websiteId` or a `domain`. Call `flowsery_websites` first to get them.

## Tools

| tool | what it does |
| --- | --- |
| `flowsery_websites` | List the sites this token can read. Call this first. |
| `flowsery_overview` | Totals: visitors, sessions, bounce rate, duration, revenue, conversion rate. |
| `flowsery_timeseries` | The same metrics bucketed by hour, day, week or month. |
| `flowsery_breakdown` | Group visitors by any of 25 dimensions. |
| `flowsery_realtime` | Visitors active in the last five minutes. |
| `flowsery_issues` | Bugs and broken flows the AI found in session recordings. |

Six tools against an API of twenty-eight, and most of the shrinkage is one
decision: `flowsery_breakdown` takes a `dimension` argument and replaces the
eleven per-dimension endpoints. `get_countries`, `get_browsers`,
`get_campaigns` and the rest are the same query with a different word in it.
Eleven near-identical tools is eleven chances to pick the wrong one.

Every tool takes the same `filter_*` arguments, so the interesting questions
are one call. `dimension=page` with `filter_utm_campaign=spring` shows where
one campaign's traffic actually landed.

## What is deliberately missing

No writes. The API can create goal and payment records and can permanently
delete them, and `DELETE /goals` with no date range wipes history that does not
come back. None of that belongs behind a tool an agent can reach while
answering "how did traffic do last week". Use the
[skill](https://github.com/Flowsery/flowsery-openclaw), which spells out the
confirmation rules, or the API directly.

Individual visitor profiles are also out. They carry email, name, location and
a full page history. Retrieving one person's timeline should be a deliberate
act, not something a broad analytics question can wander into.

## Things worth knowing

`flowsery_issues` is the newest surface and the least obvious. It reads
session recordings the AI has already analyzed, so issues are deduplicated
across sessions and ranked by severity rather than listed per session. Each one
carries a session count and replication steps.

Suspended issues are hidden unless `status` asks for them.

Omitting `startAt` and `endAt` means the last 30 days ending now, not all time.
Pair a wide range with a coarse `interval`.

The API allows 600 requests per minute per token. A 429 comes back with
`Retry-After` and the plugin surfaces it rather than hammering.

## Develop

```bash
npm install
npm run build
openclaw plugins install --link . --force --accept-capabilities
openclaw plugins inspect flowsery --runtime --json
```

Needs Node `>=22.22.3 <23 || >=24.15.0 <25 || >=25.9.0`. `npm install` runs
OpenClaw's version guard on postinstall and stops outside that range.

MIT licensed. Source: [Flowsery/flowsery-openclaw](https://github.com/Flowsery/flowsery-openclaw)

# AI Ball public record API

Base URL: `https://aiball.samagent.ai/api/v1` · read-only · no authentication · JSON · responses are
cached for up to 10 minutes on the server.

Contents: [Conventions](#conventions) · [/record/daily](#recorddaily) · [/record/weekly](#recordweekly) ·
[/record/summary](#recordsummary) · [/record/leagues](#recordleagues) ·
[/record/matches](#recordmatches) · [The match object](#the-match-object)

Examples below are real responses, trimmed. Fields this skill does not use are left out; the live
response has a few more, and you can ignore them.

## Conventions

| Thing | Rule |
|---|---|
| Language | `lang=en` for English names, `lang=ms` for Malay. Default is Chinese — always pass it. |
| Time zone | `tz` takes an IANA name (`Asia/Manila`, `Europe/London`). Default `Asia/Kuala_Lumpur`. It decides which calendar day a match belongs to. |
| Timestamps | ISO 8601 in UTC (`2026-09-25T16:00:00Z`). Convert before telling anyone a kick-off time. |
| Probabilities | Fractions 0–1 for `home`, `draw`, `away`; they sum to 1. Show as percentages with one decimal. |
| Rates | `hitRate` is already a percentage (57.9 means 57.9%) of matches where the model's most likely outcome happened. `null` means the sample is under `minBucketSample` (30) or empty — report the count instead. |
| Baselines | `market`: always take the pre-match favourite. `random`: one outcome in three. Same matches, same counting. |
| Bad parameters | An unparseable `date` / `week_start` silently falls back to the current day / week. Check the echoed value. |

## /record/daily

`GET /record/daily?lang=en&tz=Asia/Kuala_Lumpur&date=2026-09-26`

One calendar day in `tz`. `date` defaults to today.

```json
{
  "date": "2026-09-26",
  "tz": "Asia/Kuala_Lumpur",
  "ledgerStart": "2026-10-10",
  "upcoming": [],
  "finished": [
    {
      "matchId": "6327698412",
      "kickoffAt": "2026-09-25T16:00:00Z",
      "leagueKey": "欧国联",
      "league": "UEFA Nations League",
      "homeTeam": "Armenia",
      "awayTeam": "Latvia",
      "probabilities": { "home": 0.5367, "draw": 0.2511, "away": 0.2122 },
      "confidence": 0.583,
      "homeScore": 2,
      "awayScore": 0,
      "actual": "home",
      "hit": true,
      "source": "auto",
      "capturedAt": "2026-09-25T14:01:49Z"
    }
  ],
  "day": {
    "n": 17, "hits": 9, "hitRate": 52.9,
    "market": { "n": 17, "hits": 9, "hitRate": 52.9 },
    "random": { "n": 17, "hits": 6, "hitRate": 33.3 }
  },
  "cumulative": {
    "n": 0, "hits": 0, "hitRate": null,
    "market": { "n": 0, "hits": 0, "hitRate": null },
    "random": { "n": 0, "hits": 0, "hitRate": 33.3 }
  }
}
```

- `upcoming` — readings captured, no final score yet. A match enters this list 45–120 minutes before
  kick-off and leaves it when the score arrives, so it may already be in play. Matches further out are
  not listed anywhere yet.
- `finished` — readings with their final score.
- `day` — how that day's finished readings went, beside the two baselines.
- `cumulative` — the running total of the official ledger, which starts on `ledgerStart`
  (2026-10-10). Before that date it is empty by design; use `/record/summary` for the record so far.

## /record/weekly

`GET /record/weekly?lang=en&tz=Asia/Kuala_Lumpur&week_start=2026-09-21`

Monday-to-Sunday week in `tz`; `week_start` defaults to the current week's Monday.

Top-level fields: `weekStart`, `weekEnd`, `n`, `hits`, `hitRate`, `market`, `random`, `buckets` (same
shape as in the summary, usually `null` rates because a single week is small), `matches` (array of
[match objects](#the-match-object)), `biggestMiss` (the highest-confidence reading that did not
happen, or `null`), `cumulative` (as in daily).

```json
{
  "weekStart": "2026-09-21", "weekEnd": "2026-09-27",
  "n": 55, "hits": 38, "hitRate": 69.1,
  "market": { "n": 55, "hits": 38, "hitRate": 69.1 },
  "buckets": [
    { "key": "lt45", "n": 3, "hits": 1, "hitRate": null },
    { "key": "45to55", "n": 26, "hits": 15, "hitRate": null },
    { "key": "55to65", "n": 12, "hits": 10, "hitRate": null },
    { "key": "gte65", "n": 14, "hits": 12, "hitRate": null }
  ]
}
```

## /record/summary

`GET /record/summary`

Everything recorded since `since`, in one number and by confidence band. No `lang` needed — there are
no names in it.

```json
{
  "since": "2026-08-27",
  "minBucketSample": 30,
  "n": 473, "hits": 274, "hitRate": 57.9,
  "market": { "n": 473, "hits": 272, "hitRate": 57.5 },
  "random": { "n": 473, "hits": 158, "hitRate": 33.3 },
  "buckets": [
    { "key": "lt50", "n": 179, "hits": 84, "hitRate": 46.9, "highlighted": false,
      "market": { "n": 179, "hits": 82, "hitRate": 45.8 } },
    { "key": "50to55", "n": 74, "hits": 32, "hitRate": 43.2, "highlighted": true,
      "market": { "n": 74, "hits": 32, "hitRate": 43.2 } },
    { "key": "55to60", "n": 68, "hits": 39, "hitRate": 57.4, "highlighted": true,
      "market": { "n": 68, "hits": 39, "hitRate": 57.4 } },
    { "key": "60to70", "n": 70, "hits": 50, "hitRate": 71.4, "highlighted": true,
      "market": { "n": 70, "hits": 50, "hitRate": 71.4 } },
    { "key": "gte70", "n": 82, "hits": 69, "hitRate": 84.1, "highlighted": true,
      "market": { "n": 82, "hits": 69, "hitRate": 84.1 } }
  ],
  "subtotal": { "key": "gte50", "n": 294, "hits": 190, "hitRate": 64.6,
    "market": { "n": 294, "hits": 190, "hitRate": 64.6 } },
  "disagreement": { "n": 26, "modelHits": 11, "marketHits": 9, "highlightedN": 0 },
  "snapshots": { "auto": 55, "backfill": 418 },
  "lockedSince": "2026-09-20T17:09:02Z"
}
```

- Band keys are ranges of the `confidence` score, and the key spells the range: `ltNN` is below
  0.NN, `NNtoMM` is 0.NN up to 0.MM, `gteNN` is 0.NN and above (currently `lt50`, `50to55`,
  `55to60`, `60to70`, `gte70`). **The set of bands can change** — read them from the response
  rather than assuming the ones shown here. A well-behaved record has higher rates in higher bands;
  say whether it does.
- Each band carries its own `market` figures (the favourite baseline on the same matches).
  `highlighted` marks the bands at or above 0.50, where the site treats the model as confident
  enough to make a call; `subtotal` sums them.
- `disagreement` counts the matches where the model's most likely outcome differed from the pre-match
  favourite: how many, how often each side was right, and how many of those were in highlighted
  bands. When the two columns look identical, this is the explanation — say so rather than implying
  the model adds something the baseline doesn't.
- `snapshots` — how many readings were captured before kick-off by the scheduled job (`auto`) versus
  reconstructed from history before the record page launched (`backfill`). `lockedSince` is when the
  scheduled capture started. Only `auto` readings prove they predate kick-off.

## /record/leagues

`GET /record/leagues?lang=en`

```json
{ "leagues": [
  { "key": "西甲", "name": "La Liga", "n": 50 },
  { "key": "英超", "name": "Premier League", "n": 35 },
  { "key": "美职联", "name": "MLS", "n": 10 }
] }
```

`n` is how many recorded matches the competition has. Use `key` (not `name`) as the `league` filter on
`/record/matches`. A competition that is not in this list is not covered.

## /record/matches

`GET /record/matches?lang=en&league=英超&result=miss&page=1&pageSize=20`

URL-encode the key (`league=%E8%8B%B1%E8%B6%85`). `result` is `all` (default), `hit` or `miss`.
`pageSize` is at most 100. Newest first.

Top-level fields: `total`, `page`, `pageSize`, `totalPages`, `filters`, `items` (array of
[match objects](#the-match-object)).

## The match object

| Field | Meaning |
|---|---|
| `matchId` | Stable id |
| `kickoffAt` | UTC kick-off |
| `league`, `leagueKey` | Display name in `lang`; filter key |
| `homeTeam`, `awayTeam` | Names in `lang` |
| `probabilities` | `{home, draw, away}`, fractions summing to 1 |
| `confidence` | 0–1 score used for the bands. Not a probability. |
| `homeScore`, `awayScore` | Final score, `null` until finished |
| `actual` | `home` / `draw` / `away`, `null` until finished |
| `hit` | Whether the highest of the three probabilities was the actual outcome; `null` until finished |
| `source` | `auto` (captured before kick-off by the scheduled job) or `backfill` (reconstructed) |
| `capturedAt` | When the reading was captured; meaningful for `auto` |

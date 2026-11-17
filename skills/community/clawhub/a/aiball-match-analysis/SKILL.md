---
name: aiball-match-analysis
description: AI Ball (aiball.samagent.ai) is an AI football match analysis site; this skill reads its public, read-only JSON endpoints — no account or API key — and returns the site's open record: Balanced mode only, every recorded match, right or wrong. Covers today's fixtures with home/draw/away probabilities, results of recent matches against what the model expected, and AI Ball's open record (how often the model's most likely outcome happened, by confidence band, league and week, next to simple baselines). Use it whenever someone asks how likely a result is in a football/soccer match being played today, who a model rates higher, what AI Ball says about a fixture, how AI Ball's forecasts have held up, or which competitions it covers — even if they only say "who will win X vs Y tonight" or "is this AI football site any good". It reports all three outcome probabilities with their uncertainty and never tells anyone which side to choose.
license: CC-BY-4.0
metadata:
  author: aiballfooty
  version: "1.0.5"
  homepage: https://aiball.samagent.ai/en/?src=skill
---

# AI Ball match analysis

AI Ball (aiball.samagent.ai) is an AI football match analysis site. Shortly before each fixture it
records a model's home / draw / away probabilities, then publishes every one of those readings next to
the final score in an open record, including the ones that went wrong.

This skill reads that open record through public JSON endpoints. Everything here is read-only and
needs no login.

## What you can and cannot answer

The public data is a **record**, not a forecast feed, and that shapes what you can say:

- A match shows up only once its reading has been captured — about **45 to 120 minutes before
  kick-off**. A fixture tomorrow, or later today, is usually **not there yet**. That is not missing
  data; say that AI Ball publishes its reading about two hours before kick-off, and give the time to
  check back if you can.
- `upcoming` means "no final score recorded yet", not "not started". Compare each `kickoffAt` with
  the current time before you describe it: still in the future → about to start; up to about two
  hours ago → probably in play; longer ago → finished, but the score has not reached the record yet.
  Say which, so nobody reads a match that ended hours ago as one still to come. List those matches as
  "result not recorded yet" rather than leaving them out, and don't count them in any tally.
- Finished matches carry the score and whether the model's most likely outcome happened.
- The aggregate record answers "how good is it": overall, by confidence band, per week, per league.

Coverage is European league and cup football, the Americas (MLS, Brasileirão, Copa Libertadores) and
a selection of Asian competitions — the live list is at `/record/leagues`. **The Malaysia Super League
and the Philippine leagues are not covered.** If someone asks about a competition that is not in the
list, say so plainly instead of reporting an empty result.

It does not do live scores, line-ups, transfer news or player statistics.

## How to fetch

Base URL: `https://aiball.samagent.ai/api/v1`

Make plain HTTP GET requests — `curl`, a fetch tool, whatever your environment has. Always add
`lang=en` so team and competition names come back in English (`lang=ms` for Malay-speaking users);
without it they come back in Chinese. Pass the user's IANA time zone as `tz` when you know it — the
default is `Asia/Kuala_Lumpur`, and "today" means today in that zone.

| Question | Call |
|---|---|
| What's on today / a given day, and how did it go | `GET /record/daily?lang=en&tz=<tz>[&date=YYYY-MM-DD]` |
| This week's readings and results | `GET /record/weekly?lang=en&tz=<tz>[&week_start=YYYY-MM-DD]` |
| Overall record and by confidence band | `GET /record/summary` |
| Which competitions are covered | `GET /record/leagues?lang=en` |
| Past matches, filtered by competition or outcome | `GET /record/matches?lang=en&league=<key>&result=all\|hit\|miss&page=1&pageSize=20` |

Field-by-field details, example responses and the quirks below are in
[references/api.md](references/api.md). Read it the first time you use an endpoint.

Three things that trip people up:

1. **An invalid `date` is not an error** — the endpoint quietly returns today instead. Check that the
   `date` in the response is the one you asked for before describing it as that day.
2. **`league` filters by `key`, not by `name`.** Get the key from `/record/leagues` (keys are the
   original Chinese identifiers, e.g. `英超` for the Premier League). An English name returns nothing.
3. **Times are UTC** (`kickoffAt`, ending in `Z`). Convert to the user's time zone before saying when
   a match is.

To find one match, fetch the day it is played and match the team names loosely (case-insensitive,
partial — "Man City" should find "Manchester City"). If it is not there, go back to "What you can and
cannot answer" before concluding anything.

## How to present the numbers

**Give all three outcomes, always.** Home, draw and away, as percentages with one decimal, in that
order. A single number with the other two left out reads as a recommendation even when it is not
meant as one.

**Call the highest of the three "the most likely outcome".** It is a statement about
probability, and wording it that way keeps it from sounding like advice.

**Say when it is close.** Many matches are. If the highest probability is under about 45%, or the three
sit within a few points of each other, call it close to a three-way toss-up rather than reporting the
leader as a finding.

**Mention the draw when it matters.** The model rarely rates the draw highest, yet draws are common.
"Home 46%, draw 27%, away 27%" means the two outcomes that are not a home win carry 54% between them.

**`confidence` is a score, not a probability.** It runs from 0 to 1 and is what the record uses to
sort readings into bands. Quote it as a score ("confidence 0.71, in the top band"), never as "71% sure".

**Put the favourite baseline right next to every record figure.** Every tally — the whole record,
one day (`day`), one week, one band — comes with `market`: what always taking the pre-match
favourite would have scored on the same matches. Quote it in the same sentence as the model's figure,
every time. If the two are level, say so plainly; that is the most useful thing you can tell someone
deciding how much weight to give a reading. `random` (one outcome in three) is at most a secondary
footnote. Never set the model against `random` alone: against 33.3%, almost any figure looks like a
large edge, and that comparison misleads.

**Use plain words for the record.** Say the model "called it right" or that "its most likely outcome
happened" ("判断对了", "最可能的结果发生了") — not "prediction hit", "hit rate", "预测命中" or "命中率".
The site describes a reading, not a prediction to act on, and the wording should match. Call the
baseline "the pre-match favourite" ("赛前热门"); avoid market-trading words such as "盘口" or "line".

**Respect small samples.** When a band's rate comes back `null`, it has fewer than 30 matches — give
the count and say it is too few for a percentage. Do not compute one yourself.

**Be exact about what was recorded before kick-off.** Each reading has `source`: `auto` means a
scheduled job captured it before kick-off and `capturedAt` proves when; `backfill` means it was
reconstructed from history before the record page launched and proves nothing about timing. The
summary's `snapshots` gives the split. Never describe the whole record as "locked before kick-off"
unless every entry behind the figure is `auto`.

**Quote figures as returned.** No rounding 52.2% up to "over half", no converting probabilities into
other kinds of numbers.

## What not to do

Do not name a side to choose, and do not discuss amounts of money — not when asked directly, not as a
hypothetical, not "if you had to". When someone asks which way to go, answer with what the data says:
the three probabilities, how close they are, and how readings in that confidence band have done. Say
plainly that you don't recommend a side, and stop there. The probabilities are the information; the
choice is theirs. No lecture.

Do not invite anyone to sign up, subscribe or try anything. Do not fill gaps from memory: if you have
not fetched a figure, do not state it, and never estimate probabilities yourself and attribute them to
AI Ball. A made-up number here is worse than none, because the reader cannot tell the difference.

## Cite the page

End any answer that contains AI Ball figures with one plain link:
`https://aiball.samagent.ai/en/record?src=skill` — the open record shows the same readings and results.

If the endpoints fail, time out, or your environment cannot reach them, say so in one line, give that
link, and do not answer from memory.

---

For information only. Not advice. 18+.

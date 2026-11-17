---
name: football-match-performance-analysis
description: Explain a completed football (soccer) match from SofaScore statistics, incidents, and lineups, including beginner-friendly briefs for coaches or parents. Use for sourced post-match explanations; use multi-sport-match-research for basic cross-provider fixture checks.
---

# Football match (soccer) performance analysis

Produce a source-grounded post-match brief from one SofaScore event. The goal is to describe what the source recorded and which interpretations it supports, not to reconstruct tactics or predict a rematch from a few box-score fields.

## Scope and event identity

Set the competition, teams, match date, and time zone from the request. Resolve the event through SofaScore search, then verify both participants, competition, scheduled start, and status from the returned event before collecting detail. A team-name match alone is not enough; reserve, youth, women's, and senior teams can share names.

Analyze completed matches as post-match reports. For live or upcoming matches, label the output as a snapshot and do not use final-match language. Preserve the provider's status, period, and any extra-time or shootout distinction.

## Collect a bounded event record

1. Resolve and verify the SofaScore event ID.
2. Fetch the event summary and statistics for that same event ID. Keep each statistic's source label, value, unit, and period; missing categories stay unknown rather than zero.
3. Fetch incidents and lineups for chronology and starting-player context. Do not infer a player's role, injury, or tactical assignment beyond fields the response actually exposes.
4. Use head-to-head or recent team events only when the user asks for historical context. Confirm every team ID from the event response. For team events, direction is next or last; do not mix future fixtures into completed-match form.
5. Fetch event odds only when explicitly useful. Label the returned odds as a retrieved snapshot; do not call them pre-match odds unless the source provides that timing.

Use one match as the default scope. Ask before collecting a broad match cohort or repeated snapshots; extra calls can add cost without making the causal story stronger.

## Interpret the evidence carefully

- Describe numerical contrasts before explaining them. Possession, shots, expected goals, corners, or ratings alone do not establish why a team won.
- Use incidents and lineup details as timeline/context evidence, not proof that an event caused a result. Separate observed events from your interpretation.
- Do not compare periods or categories with different definitions as if they were the same measure. Explain missing values, mismatched denominators, or unclear labels.
- Recent form and head-to-head records are small descriptive samples, not forecasts. Odds are market snapshots, not an explanation of match quality.
- Do not invent a tactical claim when the API exposes only aggregate stats. State the evidence gap plainly.

## Beginner-friendly coach or parent view

When the reader is new to match analysis, keep the same evidence scope and make
the explanation easier to follow:

1. Choose at most three useful observations. Keep each source label, value, and
   period beside the plain-language explanation; define a metric only when its
   meaning is clear from the source.
2. Separate what SofaScore recorded from what the numbers might suggest. Do not
   turn team-level totals into a verdict about a young player's ability, effort,
   or coaching quality.
3. Offer one reflection prompt tied to the available incident timeline, such as
   what the viewer noticed before or after a goal or substitution. If the user
   already has match footage, frame a question they can check in that recording;
   these endpoints do not provide video or clips.
4. If useful, organize the brief as “what I noticed”, “what the source recorded”,
   and “what to check next”. Avoid prescribing a drill or tactical change from
   aggregate match data alone.

## Deliverable

Return a compact report with:

1. Match identity, competition, date/time zone, final or live status, and score.
2. A short table of the most relevant home/away statistics with source labels and periods.
3. A sourced incident timeline and lineup facts that materially contextualize the numbers.
4. What the combined evidence supports, what remains an interpretation, and missing or ambiguous fields.
5. Optional recent-form, head-to-head, or odds context only when requested, with those evidence types kept separate.

## Examples

~~~sh
scripts/crawlora.sh /sofascore/search q="Arsenal Chelsea 2026-10-05"
scripts/crawlora.sh /sofascore/event id=12345678
scripts/crawlora.sh /sofascore/event-statistics id=12345678
scripts/crawlora.sh /sofascore/event-incidents id=12345678
scripts/crawlora.sh /sofascore/event-lineups id=12345678
~~~

The numeric event ID above is a format placeholder; use the verified ID returned by search. Read [reference/endpoints.md](reference/endpoints.md) for exact parameters and use scripts/crawlora.sh so the API key stays in a header.

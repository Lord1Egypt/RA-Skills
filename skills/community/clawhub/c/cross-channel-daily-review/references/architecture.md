# Architecture

## Goal
Build a reusable daily review workflow that works across different channel sets without hardcoding a single stack.

## Layers
1. **Discovery** — identify candidate channels from sessions/config/user input.
2. **Normalization** — convert channel-specific evidence into one schema.
3. **Raw output** — write one raw review per channel.
4. **Synthesis** — write one cross-channel review.
5. **Boss mode** — build a shorter management summary for one primary channel.
6. **Verification** — verify files and state before claiming success.

## Discovery priority
Use this order when identifying channels:
1. `sessions_list` / session metadata / delivery context
2. transcript structured markers
3. user-provided explicit channel hints

Interpretation:
- `active` = strong metadata-backed confirmation
- `configured` = transcript candidate exists but strong metadata confirmation is missing
- `missing` = no strong signal found

## Borrowed design ideas worth keeping
- From **Memory Sync Protocol**: keep durable rules synchronized across shared memory / workflow files instead of letting them live only in chat.
- From **Wayfound**: keep the daily review loop lightweight and cron-friendly.
- Our stronger differentiator: per-channel raw files + one synthesized cross-channel review + configurable boss-mode delivery.

## Multi-bot / multi-agent requirement
Do not model the world as `one channel = one bot = one conversation`.

Support this hierarchy instead:
1. **Channel** — any supported conversation surface or delivery destination
2. **Scope** — DM, group, thread, room, topic, or equivalent conversational container.
3. **Participants** — one or more bots, humans, or workflow agents inside that scope.
4. **Sessions** — one or more runtime sessions that contributed inside the same scope.

Review logic should be able to:
- summarize a single scope containing multiple bots
- summarize multiple scopes inside one channel
- roll those up into a channel summary
- then roll all channels into one synthesized management review

## Default decisions
- review window: last 24 hours
- preferred destination: configurable
- delivery mode: `boss-primary`
- fallback when the preferred destination is unavailable: first verified available destination

## Output tree
```text
memory/daily-review/
├── raw/YYYY/MM/<channel>_YYYY-MM-DD.md
├── synthesized/YYYY/MM/YYYY-MM-DD.md
├── boss/YYYY/MM/YYYY-MM-DD.md
├── weekly/YYYY/weekly-YYYY-WW.md
├── monthly/YYYY/monthly-YYYY-MM.md
├── archive/YYYY/MM/
└── index.json
```

## Retention model
Use layered retention so the system stays searchable without becoming bloated:

1. **Daily layer**
   - raw + synthesized + boss daily outputs
   - keep current month + previous month by default
2. **Weekly layer**
   - weekly rollups
   - keep medium-term (for example 6–12 months)
3. **Monthly layer**
   - monthly rollups
   - keep long-term by default

## Cleanup rule
Do not delete old daily files until:
- the relevant weekly summaries exist
- the relevant monthly summary exists
- important patterns have been distilled upward
- the index reflects archive/cleanup state

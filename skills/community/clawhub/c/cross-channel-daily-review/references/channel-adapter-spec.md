# Channel Adapter Spec

## Required normalized fields

Each channel object should provide:

```json
{
  "channel": "channel-a",
  "channel_label": "Channel A",
  "scope_key": "channel-a:scope:example-conversation",
  "scope_type": "dm",
  "participant_shape": "single-bot-dm",
  "bot_count": 1,
  "session_count": 1,
  "confidence_score": 85,
  "status": "active",
  "date": "2026-03-15",
  "time_window": "2026-03-14 03:00 ~ 2026-03-15 03:00 Asia/Shanghai",
  "source_refs": ["session:path/or/id"],
  "summary_points": ["bullet 1", "bullet 2"],
  "issues": ["optional issue"],
  "wins": ["optional win"],
  "missing_reason": "",
  "notes": ["optional note"]
}
```

## Status values
- `active` — confirmed recent data found with session/delivery metadata support
- `configured` — candidate evidence exists (for example transcript structure) but session metadata confirmation is still missing
- `missing` — channel unavailable / not configured / not found
- `collection_failed` — expected source exists but collection failed

## Rules
- `channel` must be a lowercase slug.
- `scope_key` should identify the conversation scope inside a channel, not just the channel itself. Examples: one DM, one group, one thread, one room.
- `source_refs` should list concrete evidence checked.
- If status is not `active`, explain why in `missing_reason`.
- `summary_points` should remain concise and factual.
- Do not put cross-channel synthesis into per-channel normalized objects.
- Do not assume one channel has only one bot or one session. A single channel scope can contain multiple bots, multiple sessions, or a workflow-style multi-agent group chat.
- When possible, aggregate by `scope_key` first, then summarize the whole `channel`.
- `participant_shape` should capture the best current interpretation, such as `single-bot-dm`, `multi-bot-scope`, `workflow-group`, or `unknown`.
- `confidence_score` should express how reliable the current channel/scope inference is. Prefer strong session metadata over transcript-only heuristics.

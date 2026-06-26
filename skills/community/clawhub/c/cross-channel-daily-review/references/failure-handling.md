# Failure Handling

## Status taxonomy
- `missing`
- `configured`
- `collection_failed`
- `review_generated`
- `delivery_failed`
- `fully_delivered`

## Rules
- Always say which step failed.
- Always name the affected channel.
- Always include the source checked.
- If a preferred destination fails, fallback to another verified destination and log the fallback.
- A missing channel is not the same as a failed channel collection.
- Discovery based only on transcript text matching can create false positives when one transcript mentions multiple channels. Prefer delivery/session metadata over loose keyword matching whenever available.
- Metadata-first discovery reduces false positives but can create false negatives when a transcript lacks explicit channel metadata. Treat that as a discoverability gap, not proof that the channel had no activity.
- Structured transcript markers such as `agent:main:<channel>:direct|group|thread:` are stronger fallback evidence than plain free-text mentions, but still rank below `sessions_list` / delivery metadata.
- `bot_count` and `participant_shape` may begin as heuristics inferred from scope/session patterns. Treat them as provisional unless backed by stronger participant metadata.

## Report shape
At minimum report:
- channels requested
- channels active
- channels missing
- channels failed
- synthesized file
- boss summary file
- final delivery channel
- final verification result

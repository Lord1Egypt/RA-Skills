# Heartbeat Rules - Discover

Use heartbeat to revisit approved discovery topics without turning the system into noise.

## Source of Truth

Keep the workspace `HEARTBEAT.md` snippet minimal.
Treat this file as the stable contract for recurring discovery behavior.
Store mutable state only in `~/discover/heartbeat-state.md`.

## Start of Every Heartbeat

1. Ensure `~/discover/heartbeat-state.md` exists.
2. Read `~/discover/watchlist.md` and keep only topics marked `Heartbeat: active`.
3. Read the last lens used and the last material discovery marker.
4. Skip any topic that no longer has a clear reason or novelty bar.

## For Each Active Topic

1. Restate why the topic matters now.
2. Choose one fresh lens not used last time:
   - direct
   - contrarian
   - operator
   - geographic
   - regulatory
   - stakeholder
   - practical next-step
3. Do a light pass first. Deepen only if the signal looks promising.
4. Apply `novelty-test.md`.

## If the Finding Is New

- Append one dated entry to `~/discover/findings/{topic}.md`
- State what changed, why it matters now, and one next move
- Update `last_material_discovery_at` and `last_angle_used`

## If Nothing Changed

- Update `last_angle_used`
- Set `last_heartbeat_result: HEARTBEAT_OK`
- Return `HEARTBEAT_OK`

## Safety Rules

- Most heartbeat runs should do nothing
- Never log filler just to prove activity
- Never broaden topic scope silently
- Never create new heartbeat topics during heartbeat
- Never take external action beyond discovery and logging
- If the topic is becoming vague, pause it instead of improvising

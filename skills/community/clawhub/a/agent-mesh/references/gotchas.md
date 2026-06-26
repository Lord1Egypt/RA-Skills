# Known Gotchas

Production bugs encountered running multi-agent meshes. Ordered by how often they bite.

## 1. Follow-Up Spam

**Symptom:** Agent A sends "checking in..." every 30 min. Agent B wastes tokens replying to each.

**Cause:** Agent A nags without checking if B already replied.

**Fix:** Before sending a follow-up, run `mesh-status.sh` to check for recent outbound messages. If you already sent a message to the same agent recently and haven't received a reply, do not send another. Wait.

Add to heartbeat: "Do not send follow-up messages if you have unanswered outbound messages to the same agent."

## 2. Broadcast Reply Storm

**Symptom:** One agent broadcasts. 9 agents reply. Some reply to each other's replies. Token costs explode.

**Cause:** No discipline on broadcast replies. With N agents, a broadcast can generate N² messages.

**Fix:** Three rules:
1. Reply to the original **sender** only, never to all recipients
2. Never auto-reply to messages with `"broadcast": true` in metadata unless explicitly asked
3. Do not reply to a broadcast just to acknowledge — only reply if you have substantive information

## 3. Polling Breaks After Restart

**Symptom:** Agent was polling, then stops after deploy/restart.

**Cause:** Ephemeral platforms (Railway, Fly.io) wipe workspace on redeploy. Heartbeat entries may be lost.

**Fix:** Re-add the heartbeat polling entry to HEARTBEAT.md after redeploy. See `references/cron-templates.md` for the template.

## 4. One-Sided Polling

**Symptom:** Agent B replies, but Agent A never sees it.

**Cause:** Only one side has polling set up.

**Fix:** Every agent needs: a heartbeat or cron entry running `mesh-poll.sh`, env vars configured, and heartbeat enabled in OpenClaw config. Verify with `mesh-status.sh`.

## 5. Wrong Agent ID

**Symptom:** Agent polls but never gets messages.

**Cause:** `MESH_AGENT_ID` doesn't match what senders put in `to_agent`.

**Fix:** Agree on IDs upfront. Run `mesh-agents.sh` to see all known IDs. Use lowercase_with_underscores.

## 6. Newlines Break curl JSON

**Symptom:** `400 Bad Request` when sending multi-line messages.

**Cause:** Shell string interpolation breaks JSON.

**Fix:** Always use `mesh-send.sh` (uses Node for JSON encoding). Never raw curl for messages.

## 7. Weak Model for Complex Tasks

**Symptom:** Agent replies "Acknowledged" instead of doing work.

**Cause:** Cheap model can't execute multi-step tasks.

**Fix:** Use Sonnet/Opus for complex task crons. Haiku for simple relay/status checks.

## 8. Message Volume at Scale

**Symptom:** With 10 agents, the table grows fast. Polling gets slower.

**Cause:** No cleanup — old messages pile up.

**Fix:** Schedule monthly cleanup via Supabase SQL Editor. See `references/supabase-setup.md` maintenance section. The `idx_agent_messages_poll` index keeps polling fast even with thousands of rows.

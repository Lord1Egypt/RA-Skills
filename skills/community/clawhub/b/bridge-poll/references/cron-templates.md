# Cron Job Templates

Copy-paste these into `cron → add` calls. Replace all `[PLACEHOLDERS]`.

## Responding Agent (polls inbox, sends replies)

```json
{
  "name": "Bridge Inbox Relay",
  "schedule": { "kind": "every", "everyMs": 600000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "BRIDGE INBOX CHECK — You are [AGENT_NAME]. Respond to [OTHER_AGENT] messages.\n\nStep 1: Read last-poll timestamp\nRun: cat /tmp/acp_bridge_last_ts 2>/dev/null || echo 0\n\nStep 2: Fetch new messages from the bridge\nRun: curl -s \"http://[BRIDGE_HOST]:18790/api/inbox?after=$(cat /tmp/acp_bridge_last_ts 2>/dev/null || echo 0)\" -H 'Authorization: Bearer [TOKEN]'\n\nIf count == 0: reply NO_REPLY. Done.\n\nStep 3: Read your workspace context files before replying\nRead: SESSION-STATE.md, SOUL.md, and today's memory file from your workspace.\n\nStep 4: For each new message, compose a substantive reply\n- You ARE [AGENT_NAME]. Respond directly with data, analysis, or results.\n- If a message requests information you can look up in your workspace files or via your configured tools, do so and include the results.\n- Skip stale 'Follow-up: These tasks have been pending' messages.\n- Include numbers and deliverables, not narratives and promises.\n\nStep 5: Send reply using the bridge_reply helper\nRun: python3 [WORKSPACE]/bridge_reply.py \"<your reply>\"\n\nStep 6: Save latest timestamp. Use the 'ts' field (float seconds), NOT the 'id' field.\nRun: bash [WORKSPACE]/save_bridge_ts.sh <latest_msg_ts_float>\n\nStep 7: If the other agent assigned tasks needing the owner's attention, alert them via the message tool.",
    "model": "[STRONG_MODEL]",
    "timeoutSeconds": 240
  },
  "delivery": { "mode": "announce" }
}
```

**Placeholders:**
- `[AGENT_NAME]` — this agent's name (e.g., "Brain")
- `[OTHER_AGENT]` — the sending agent's name (e.g., "Adviser")
- `[BRIDGE_HOST]` — bridge server address (e.g., `localhost`, `192.168.1.50`, `bridge.example.com`)
- `[TOKEN]` — the ACP_BRIDGE_TOKEN
- `[WORKSPACE]` — path to workspace where helper scripts live
- `[STRONG_MODEL]` — e.g., `anthropic/claude-opus-4-6`, `openai/gpt-4o`

## Sending Agent (polls outbox, sends new tasks)

```json
{
  "name": "Bridge Outbox Check + Task Assignment",
  "schedule": { "kind": "every", "everyMs": 600000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "BRIDGE CHECK — You are [AGENT_A_NAME].\n\nStep 1: Read last-recv timestamp\nRun: cat /tmp/acp_bridge_last_recv_ts 2>/dev/null || echo 0\n\nStep 2: Poll for replies from [AGENT_B]\nRun: curl -s \"http://[BRIDGE_HOST]:18790/api/recv?after=$(cat /tmp/acp_bridge_last_recv_ts 2>/dev/null || echo 0)\" -H 'Authorization: Bearer [TOKEN]'\n\nIf count == 0: reply NO_REPLY. Done.\n\nStep 3: Process each reply. Update your workspace context files with new information.\n\nStep 4: If you have new tasks or questions for [AGENT_B], send them:\nRun: curl -s -X POST http://[BRIDGE_HOST]:18790/api/send -H 'Authorization: Bearer [TOKEN]' -H 'Content-Type: application/json' -d '{\"message\": \"<task text>\", \"from\": \"[AGENT_A_NAME]\"}'\nFor multi-line messages, use python3 with json.dumps instead of curl to encode safely.\n\nStep 5: Save latest recv timestamp (use 'ts' field, float seconds)\nRun: echo <latest_ts> > /tmp/acp_bridge_last_recv_ts",
    "model": "[STRONG_MODEL]",
    "timeoutSeconds": 240
  },
  "delivery": { "mode": "announce" }
}
```

## Weekly JSONL Pruning (on the bridge host)

```json
{
  "name": "Bridge JSONL Prune",
  "schedule": { "kind": "cron", "expr": "0 3 * * 0", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the bridge pruning script to rotate old messages:\npython3 [WORKSPACE]/bridge_prune.py --days 7\nReport how many messages were pruned from each file.",
    "model": "[CHEAP_MODEL]",
    "timeoutSeconds": 60
  },
  "delivery": { "mode": "none" }
}
```

## Poll Interval Guidelines

| Use case | Interval | Notes |
|----------|----------|-------|
| Real-time collaboration | 2-5 min | Higher cost, faster response |
| Standard async | 10 min | Good balance of cost and responsiveness |
| Low-priority / overnight | 30-60 min | Saves tokens when latency doesn't matter |

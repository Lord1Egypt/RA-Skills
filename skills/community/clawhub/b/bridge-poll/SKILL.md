---
name: bridge-poll
description: "Agent-to-agent communication via HTTP bridge with cron-based polling. Use when: (1) two OpenClaw agents need to talk across instances, containers, or machines, (2) setting up a bridge relay between agents, (3) debugging silent/unresponsive bridge connections, (4) an agent needs to poll another agent's messages and respond autonomously. Works on any platform — VPS, Docker, bare metal, cloud. Requires ACP_BRIDGE_TOKEN env var (shared secret for bridge auth). Helper scripts require BRIDGE_TOKEN and BRIDGE_URL env vars. No external network calls — all communication stays between the two configured agents via the bridge server."
---

# Bridge-Poll: Agent-to-Agent Communication

Two OpenClaw agents that can't share sessions communicate through an HTTP bridge server with cron-based polling.

```
Agent A ──POST /api/send──▶ Bridge ◀──GET /api/inbox── Agent B
Agent A ◀──GET /api/recv─── Bridge ──POST /api/reply──▶ Agent B
```

Agent A writes to inbox → Agent B polls inbox + replies to outbox → Agent A polls outbox.

## Setup

### 1. Deploy the bridge server

Copy `scripts/acp_bridge.py` to the host machine. Generate a token, start it:

```bash
export ACP_BRIDGE_TOKEN=$(openssl rand -hex 16)
echo "$ACP_BRIDGE_TOKEN"  # both agents need this
nohup python3 acp_bridge.py > /tmp/acp_bridge.log 2>&1 &
echo $! > /tmp/acp_bridge.pid
curl -s http://localhost:18790/api/health -H "Authorization: Bearer $ACP_BRIDGE_TOKEN"
```

### 2. Deploy helper scripts on the responding agent

Copy `scripts/bridge_reply.py` and `scripts/save_bridge_ts.sh` to the agent's workspace. Edit `BRIDGE_TOKEN` in `bridge_reply.py`.

Initialize the cursor:
```bash
python3 -c "import time; print(time.time())" > /tmp/acp_bridge_last_ts
```

### 3. Create the poll cron on each agent

See `references/cron-templates.md` for copy-paste cron job configs for both sides. Customize the placeholders (`[AGENT_NAME]`, `[BRIDGE_HOST]`, `YOUR_TOKEN`, file paths).

**Model requirement**: Use a strong model (Opus-tier) for the poll cron. Weak models reply with "acknowledged" instead of doing work.

### 4. Networking

The bridge must be reachable by both agents. Options:

| Topology | How |
|----------|-----|
| Same machine / Docker | `http://localhost:18790` or `http://host.docker.internal:18790` |
| Same network | `http://<LAN_IP>:18790` |
| Cross-internet (simple) | Open port 18790, use public IP. Token is your auth. |
| Cross-internet (secure) | SSH tunnel: `ssh -L 18790:localhost:18790 user@bridge-host -N` |
| Production | Reverse proxy (nginx/caddy) with TLS → `https://bridge.yourdomain.com` |

## API Reference

All endpoints require `Authorization: Bearer <TOKEN>`.

| Endpoint | Method | Direction | Purpose |
|----------|--------|-----------|---------|
| `/api/send` | POST | A → inbox | Agent A sends message |
| `/api/reply` | POST | B → outbox | Agent B sends reply |
| `/api/inbox?after=TS` | GET | B reads | Agent B polls for messages |
| `/api/recv?after=TS` | GET | A reads | Agent A polls for replies |
| `/api/health` | GET | Either | Returns `{"ok": true}` |

POST body: `{"message": "text", "from": "agent_name"}`
Response: `{"messages": [...], "count": N}` — each message has `id` (ms int) and `ts` (float seconds).

**The `after=` parameter takes `ts` (float seconds), NOT `id` (ms integer).** See gotchas.

## Security Model

- **Auth required**: The bridge server refuses to start without `ACP_BRIDGE_TOKEN`. All requests require `Authorization: Bearer <token>`.
- **No outbound calls**: The bridge server makes zero outbound network requests. It only listens and serves. Messages stay on disk in the bridge directory.
- **Credential setup**: Three env vars must be configured manually by the operator:
  - `ACP_BRIDGE_TOKEN` — shared secret for bridge HTTP auth (generate with `openssl rand -hex 16`)
  - `BRIDGE_TOKEN` — same token, used by helper scripts (`bridge_reply.py`)
  - `BRIDGE_URL` — bridge endpoint URL, used by helper scripts
- **Trust boundary**: Both agents sharing a bridge token are mutually trusted. The cron poll templates instruct the responding agent to read workspace files (SESSION-STATE.md, SOUL.md) and execute workspace scripts (bridge_reply.py, save_bridge_ts.sh). Only share bridge tokens with agents you control.
- **Network exposure**: Bind to localhost or use a reverse proxy with TLS for cross-network deployments. Do not expose the bridge port to the public internet without auth + TLS.

## Gotchas (Production Bugs)

Read `references/gotchas.md` for detailed symptoms, causes, and fixes. Summary:

1. **Future-dated timestamp** — agent appears deaf, polls return 0. Reset: `python3 -c "import time; print(time.time())" > /tmp/acp_bridge_last_ts`
2. **ts vs id confusion** — using `id/1000` causes float rounding → duplicates or skips. Always save `ts`.
3. **Newlines in curl** — breaks JSON. Use `bridge_reply.py`, never raw curl for multi-line messages.
4. **Context loss between polls** — agent forgets tasks each cycle. Fix: write `SESSION-STATE.md` BEFORE responding (WAL protocol).
5. **Follow-up spam** — sender auto-nags every hour, receiver burns tokens replying to each nag. Fix: skip "Follow-up:" messages in cron prompt.
6. **Weak model** — cheap model says "acknowledged" instead of doing work. Fix: use Opus-tier.
7. **JSONL grows forever** — inbox/outbox files never pruned. Fix: weekly rotation cron (see gotchas.md).

## Monitoring

Add to heartbeat:
1. Bridge alive? `curl -s localhost:18790/api/health`
2. Timestamp not in future? Compare `/tmp/acp_bridge_last_ts` to `time.time()`
3. Last outbox reply < 30 min old?
4. If dead → restart. If future timestamp → reset. If stale → check cron logs.

See `references/monitoring.md` for copy-paste health check scripts.

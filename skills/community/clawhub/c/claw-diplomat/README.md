# Claw Diplomat 🤝

Lets two OpenClaw agents literally negotiate, coordinate, and commit to tasks in real time — a decentralized peer‑to‑peer layer where bots cut deals, track progress, and hit deadlines without a single server in between.

---

## Get started

**Install the skill:**
```bash
clawhub install claw-diplomat
```

**Install Python dependencies (once):**
```bash
pip3 install PyNaCl noiseprotocol websockets
```

**Generate a Diplomat Address:**
```
/claw-diplomat generate-address
```

Share the token it produces with any peer. That's it.

---

## How a deal works

1. Share a Diplomat Address token with a peer
2. They connect: `/claw-diplomat connect <token>`
3. Either side proposes a task exchange: `/claw-diplomat propose <peer>`
4. Both sides negotiate terms — the agent handles the back-and-forth
5. Both sides confirm → the deal is cryptographically sealed and logged to memory
6. Deadlines surface automatically on every session until checked in

No deal is ever accepted without explicit human approval on both sides.

---

## Commands

| Command | What it does |
|---|---|
| `generate-address` | Create a shareable address token |
| `connect <token>` | Connect to a peer |
| `propose <peer>` | Start a negotiation |
| `handoff <peer>` | Pass completed work and context to a peer |
| `status` | See active commitments and upcoming deadlines |
| `checkin <id> done\|overdue\|partial` | Report on a commitment |
| `peers` | See all connected peers |
| `list` | See all sessions (active and past) |
| `cancel <id>` | Cancel a pending proposal |
| `revoke` | Revoke the current address and issue a new one |
| `key` | Print the public key |
| `help security` | Show security details |

---

## Security at a glance

- **Noise_XX encryption** (AES-256-GCM) — messages are encrypted before leaving the machine. The relay routes tokens, not content.
- **Every deal requires human approval** — nothing is accepted or committed automatically.
- **Committed terms are immutable** — once both sides agree, the terms and memory hash are locked.
- **Private key stays local** — generated once, stored at `skills/claw-diplomat/diplomat.key`, never transmitted.
- **Background listener runs isolated** — the inbound connection process only receives `DIPLOMAT_*` environment variables. No API keys, cloud credentials, or secrets are forwarded to it.

---

## Self-host the relay

The default relay (`claw-diplomat-relay-production.up.railway.app`) cannot read message content — everything is encrypted before it arrives. For full control, self-hosting takes one command:

```bash
docker build -t claw-diplomat-relay relay/
docker run -p 8080:8080 claw-diplomat-relay
```

Then point the skill at it:
```bash
export DIPLOMAT_RELAY_URL=wss://your-server.example.com:443
```

---
name: axon-agent
description: Register and operate an AI Agent on the Axon blockchain (AI Agent Native L1, Cosmos SDK + EVM, Chain ID 9001). Use when a user wants to: (1) register an agent on Axon chain, (2) check agent on-chain status (isAgent, ONLINE, reputation), (3) set up the agent-daemon for heartbeat maintenance, (4) troubleshoot Axon agent registration or heartbeat failures. Do NOT use for general EVM/Solidity work unrelated to Axon.
---

# Axon Agent Skill

Axon is an AI Agent Native L1 blockchain. An "Agent" is an EVM address that calls `register()` with 100 AXON stake and sends periodic heartbeats to stay ONLINE.

**Official repo:** https://github.com/axon-chain/axon  
**Chain params:** RPC `https://mainnet-rpc.axonchain.ai/` | Chain ID `9001` | ~5s blocks | Registry `0x0000000000000000000000000000000000000901`

**CRITICAL:** The official Python SDK has an ABI bug. Always use `scripts/register.py` instead. See `references/known-issues.md` for details.

---

## Prerequisites

- Server with Python 3.8+ and Go 1.21+
- EVM wallet private key saved to a file (e.g. `/opt/axon/private_key.txt`, chmod 600)
- Minimum 120 AXON balance (100 stake + 20 burn + gas buffer)
- `web3` Python package: `pip install web3`

---

## Phase 1: Check Balance & Status

```bash
python3 scripts/check-status.py --private-key-file /opt/axon/private_key.txt
```

If `isAgent: True` → skip to Phase 3 (daemon setup).

---

## Phase 2: Register Agent

```bash
# Dry run first
python3 scripts/register.py \
  --private-key-file /opt/axon/private_key.txt \
  --capabilities "nlp,reasoning,coding,research" \
  --model "claude-sonnet-4.6" \
  --dry-run

# Real registration
python3 scripts/register.py \
  --private-key-file /opt/axon/private_key.txt \
  --capabilities "nlp,reasoning,coding,research" \
  --model "claude-sonnet-4.6"
```

After success: `isAgent: True`. Note the registration block number — first heartbeat allowed ~720 blocks later (~1 hour).

**Capabilities examples:** `nlp,reasoning,coding,research` | `trading,analysis` | `vision,audio`  
**Model:** Use actual model name being run (e.g. `claude-sonnet-4.6`, `glm-5`, `kimi-k2.5`)

---

## Phase 3: Build & Start Daemon

```bash
# Clone repo (if not already)
git clone https://github.com/axon-chain/axon /opt/axon
cd /opt/axon

# Build daemon
go build -o tools/agent-daemon/agent-daemon ./tools/agent-daemon/

# Start daemon
nohup /opt/axon/tools/agent-daemon/agent-daemon \
  --rpc https://mainnet-rpc.axonchain.ai/ \
  --private-key-file /opt/axon/private_key.txt \
  --heartbeat-interval 720 \
  --log-level info \
  >> /opt/axon/daemon.log 2>&1 &

echo "PID: $!"
```

Check logs: `tail -f /opt/axon/daemon.log`  
Expected: `heartbeat confirmed` every ~720 blocks (~1 hour).

---

## Phase 4: Watchdog Cron

```bash
# Copy watchdog to your server (replace YOUR_SERVER and YOUR_KEY)
scp scripts/watchdog.sh user@YOUR_SERVER:/opt/axon/watchdog.sh
ssh user@YOUR_SERVER "chmod +x /opt/axon/watchdog.sh"

# Add cron (every 5 min)
ssh user@YOUR_SERVER "(crontab -l 2>/dev/null; echo '*/5 * * * * /opt/axon/watchdog.sh') | crontab -"
```

---

## Troubleshooting

See `references/known-issues.md` for:
- SDK ABI mismatch (most common failure)
- HeartbeatInterval first-heartbeat delay
- Official vs fork repo confusion
- Stake economics (20 AXON burned permanently)

**Quick diagnosis:**
```bash
# Check daemon running
pgrep -f agent-daemon && echo "running" || echo "NOT running"

# Check on-chain status
python3 scripts/check-status.py --private-key-file /opt/axon/private_key.txt
```

---

## Multi-Agent Setup

Each agent needs its own EVM wallet + 100 AXON + daemon instance. Steps are identical — run separate daemon processes with different `--private-key-file` and redirect logs to separate files (e.g. `daemon-cto.log`).

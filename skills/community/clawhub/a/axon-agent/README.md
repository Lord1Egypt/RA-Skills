# axon-agent

OpenClaw skill for registering and operating AI Agents on the [Axon blockchain](https://github.com/axon-chain/axon) — an AI Agent Native L1 (Cosmos SDK + EVM, Chain ID 9001).

## What it does

- Register an EVM address as an on-chain Agent (100 AXON stake)
- Check agent status (isAgent, ONLINE, reputation score)
- Deploy the heartbeat daemon to maintain ONLINE status
- Watchdog cron to auto-restart the daemon if it crashes

## Install

```bash
clawhub install axon-agent
```

## Requirements

- Python 3.8+ (`pip install web3`)
- Go 1.21+ (for building the daemon)
- EVM wallet with at least 120 AXON (100 stake + 20 burned + gas)

## Quick start

```bash
# Check balance and registration status
python3 scripts/check-status.py --private-key-file /path/to/private_key.txt

# Register (dry run first)
python3 scripts/register.py \
  --private-key-file /path/to/private_key.txt \
  --capabilities "nlp,reasoning,coding" \
  --model "claude-sonnet-4.6" \
  --dry-run

# Real registration
python3 scripts/register.py \
  --private-key-file /path/to/private_key.txt \
  --capabilities "nlp,reasoning,coding" \
  --model "claude-sonnet-4.6"
```

## Notes

- The official Python SDK has an ABI mismatch bug — this skill bypasses it with a correct direct call
- First heartbeat is available ~720 blocks (~1 hour) after registration
- See `references/known-issues.md` for full troubleshooting guide

## Links

- Axon official repo: https://github.com/axon-chain/axon
- This skill on ClawHub: https://clawhub.ai/skills/axon-agent
- Skill source: https://github.com/6tizer/axon-agent

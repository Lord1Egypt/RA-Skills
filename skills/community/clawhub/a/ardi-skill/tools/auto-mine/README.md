# Ardi auto-mine — autonomous mining without humans in the loop

Install once, mine forever. Works with Claude Code, Hermes, or OpenClaw.

```
┌─ systemd timer (every 90s) ──────────────────────────────────────┐
│   ardi-tick.sh                                                    │
│     ├─ cheap precheck: any work? → if no, exit 0 (cost: 0)        │
│     └─ spawn subagent (claude / hermes / openclaw)                │
│           ├─ ardi-agent context     # fetch riddles               │
│           ├─ solve N (LLM does this)                              │
│           ├─ ardi-agent commit ...  # one tx per riddle           │
│           ├─ ardi-agent reveal ...  # for prior epoch's pendings  │
│           └─ ardi-agent inscribe ...# if won                      │
└───────────────────────────────────────────────────────────────────┘
```

## How users turn this on

**They don't.** The user just tells their agent (claude / hermes /
openclaw) something like "mine continuously" or "set up auto-mine for
me". The agent — guided by [ardi-skill-rs/SKILL.md](../../SKILL.md)'s
"Autonomous mining mode" section — runs `install.sh` itself. No shell
typing, no env file editing, no API key prompt.

If a human really wants to run it manually:

```bash
git clone https://github.com/awp-worknet/ardi-skill.git
~/ardi-skill/tools/auto-mine/install.sh    # idempotent + auto-starts
```

Verify:
```bash
journalctl --user -u ardi-mine -f
~/.local/share/ardi-auto-mine/status.sh    # JSON snapshot
```

### Why no API key in the env file

The systemd-spawned subagent runs the same `claude` / `hermes` /
`openclaw` binary the user has been using interactively. That binary
already has its own credentials (`~/.claude/`, `~/.hermes/`, etc.).
The subagent inherits the user's identity — no separate auth needed.

If the user has never authed their runtime CLI, install.sh will still
succeed but ticks will fail until the CLI is authed once (interactively).

### Path B — OpenClaw heartbeat (no extra install; ~30 min cadence)

If you already run OpenClaw and want zero-extra-setup mode:

```bash
mkdir -p ~/.openclaw/workspace
cp openclaw-heartbeat-mode/HEARTBEAT.md ~/.openclaw/workspace/
```

Done. OpenClaw's gateway will fire the tick on its own heartbeat
schedule. **Trade-off**: misses ~4-5 epochs per hour at the default
30-min interval. See `openclaw-heartbeat-mode/README.md`.

## Prerequisites

Whatever path:

| Item | Why | How |
|---|---|---|
| `ardi-agent` on PATH | The chain-side actions | `cargo build --release --bin ardi-agent` from this repo, or download from [releases](https://github.com/awp-worknet/ardi-skill/releases) |
| `awp-wallet` initialized | Skill signs txs through it | Install awp-wallet, run `awp-wallet init` once |
| Stake ≥ 10,000 AWP allocated to you on ARDI worknet (845300000014) | Eligibility for commit | Self-stake via [awp.pro](https://awp.pro), or get sponsored via KYA |
| ETH ≥ 0.001 on Base mainnet | Gas for commit/reveal/inscribe | Bridge from L1, or get from a faucet |
| LLM provider key | The subagent solves riddles | Anthropic / OpenAI / etc — depends on chosen runtime |
| One of: `claude` / `hermes` / `openclaw` on PATH | The LLM CLI itself | Install the framework you want |

## Environment

`~/.ardi-agent/auto-mine.env` — see [config.example.env](./config.example.env).

Critical:
- `ARDI_AGENT_RUNTIME=claude` (or `hermes` or `openclaw-scripted`)
- `ANTHROPIC_API_KEY=sk-ant-...` (or other provider's key)
- `MAX_PER_EPOCH=3` (max riddles to commit per epoch; contract caps at 5)

## Operations

```bash
# tail logs
journalctl --user -u ardi-mine -f

# see when next tick fires
systemctl --user list-timers ardi-mine.timer

# manual tick (for testing)
~/.local/share/ardi-auto-mine/ardi-tick.sh

# stop / disable
systemctl --user stop ardi-mine.timer
systemctl --user disable ardi-mine.timer

# uninstall
systemctl --user disable --now ardi-mine.timer
rm ~/.config/systemd/user/ardi-mine.{service,timer}
```

## Cost estimates

Per tick (when there's work to do):
- LLM tokens: ~5-15K input + 2-5K output (Claude Sonnet ≈ $0.05-0.15)
- Gas: ~0.0002 ETH (~$0.5) per riddle if you commit
- Bond: 0.00001 ETH per commit (refunded on successful reveal)

Per day @ MAX_PER_EPOCH=3, 240 epochs/day, 50% LLM-success rate:
- ~$30-50 LLM cost
- ~$200 gas if all hit
- 3-5 NFTs minted (likely fewer due to MAX_WINS_PER_AGENT=3 cap)

The `MAX_WINS_PER_AGENT=3` cap means **a single agent caps at 3 NFTs total**.
After that the agent can still play but cannot win — typically you'd
disable auto-mining once the cap is hit.

## Safety

- Subagent CANNOT call arbitrary contracts. The skill exposes only the
  ardi-specific commands (commit/reveal/inscribe/repair/...).
- Subagent CANNOT spend more than the configured per-epoch cap.
- Subagent CANNOT exceed the 4-minute time budget per tick (systemd
  RuntimeMaxSec=240).
- Subagent runs as YOUR user (no root), with normal filesystem perms.

## Architecture diagram

See the doc-comment block at the top of [ardi-tick.sh](./ardi-tick.sh) for
the full per-tick flow.

## Files in this directory

| File | Purpose |
|---|---|
| `ardi-tick.sh` | Dispatcher — precheck + spawn subagent |
| `prompt/ardi-mine-tick.md` | Shared subagent prompt (framework-agnostic) |
| `runtime/claude.sh` | Claude Code shim |
| `runtime/hermes.sh` | NousResearch Hermes shim |
| `runtime/openclaw-scripted.sh` | OpenClaw `--message --local` shim |
| `systemd/ardi-mine.service` | systemd OneShot service unit |
| `systemd/ardi-mine.timer` | Every-90s timer |
| `config.example.env` | Env file template (copy to `~/.ardi-agent/auto-mine.env`) |
| `install.sh` | Convenience installer (symlink + units + env) |
| `openclaw-heartbeat-mode/` | Alternative install: drop one file in OpenClaw workspace |

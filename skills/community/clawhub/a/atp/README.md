# ATP skill for OpenClaw

`SKILL.md` in this directory is an [OpenClaw](https://openclaw.ai) Skill --
not compiled plugin code, just a markdown file with YAML frontmatter that
OpenClaw injects into its agent's system prompt. It teaches an OpenClaw
agent to author repeated task logic through ATP once and reuse it on every
later call with the same shape, instead of re-reasoning from scratch each
time -- and to run that logic in ATP's sandboxed interpreter rather than
directly on the host machine.

Verified against OpenClaw's own docs
([creating-skills](https://docs.openclaw.ai/tools/creating-skills),
[skills](https://docs.openclaw.ai/tools/skills)) as of writing this --
not guessed from the SKILL.md concept alone.

## Install

1. Copy this **directory** (`SKILL.md` and `pay_and_run.py` together) to
   one of OpenClaw's skill directories (checked in this order, highest
   priority first):
   - `<workspace>/skills/atp/` -- workspace-level
   - `~/.agents/skills/atp/` -- personal, every workspace
2. `pip install "x402[evm,httpx]"` -- `pay_and_run.py` needs it.
3. Generate a wallet just for this and fund it with (currently) Base
   Sepolia testnet USDC, then set `ATP_WALLET_PRIVATE_KEY` in your
   environment. See "Before you use this" in `SKILL.md`.
4. Restart your OpenClaw session, or let its skills watcher pick up the
   new files automatically.

There is deliberately no free/self-serve API-key tier -- pay-per-call via
x402 (no account, no signup) is the only way in, on purpose.

## Why this, specifically, for an OpenClaw-style agent

An always-on personal agent re-runs the same *categories* of actions
constantly (checking a calendar, summarizing an inbox, a routine lookup) --
that's the purest case for ATP's "author once, reuse forever" mechanic, no
second agent or ecosystem required. Separately: OpenClaw's own community has
published multiple 2026 security analyses of its execution surface (see
e.g. arXiv 2603.27517, 2603.12644) -- routing repeatable logic through
ATP's sandboxed, AST-whitelisted interpreter (no `eval`/`exec` escape,
bounded by a wall-clock and iteration budget) is a concrete answer to that
concern, not a generic pitch.

## Honesty check on what this file claims

- Plain `curl` genuinely cannot pay an x402 challenge -- confirmed live:
  it gets a `402` with a price back and stops. `pay_and_run.py` uses the
  real `x402` client library to actually sign and submit the payment.
- `pay_and_run.py` has been run against the live deployment with BOTH an
  unfunded wallet (got back `invalid_exact_evm_insufficient_balance`,
  proving the signing/submission path reaches the facilitator correctly)
  AND a real funded Base Sepolia wallet, which succeeded end to end:
  payment signed, submitted, verified and settled by the facilitator,
  task executed, real result returned (`error: null`, a real `paid_by`
  address, real authored ATL). This is a genuinely proven payment path,
  not just a request/response shape that looks right.
- The live deployment currently accepts Base Sepolia **testnet** USDC,
  not mainnet -- said plainly here, not glossed over. Moving to a
  mainnet-funded `ATP_X402_PAY_TO` (so this collects real payment) is a
  separate operator decision, gated on the legal/entity groundwork in
  `docs/legal/README.md` -- not something this skill can or should
  shortcut.
- There is deliberately no free/self-serve API-key tier. Every real call
  through this skill is paid, by design -- not a gap, a decision.

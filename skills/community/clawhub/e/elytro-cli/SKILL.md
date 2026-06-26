---
name: elytro-skills
description: Entry point for the Elytro wallet skill plus the curated DeFi sub-skills. Start here before loading any individual protocol skill.
user-invocable: false
disable-model-invocation: false
---

# Elytro Skills Pack

Welcome! The `elytro` CLI prints this URL in `elytro --help` so agents always land on the canonical instructions before touching a wallet. Read this document once, then jump into the sub-skills listed below.

> Raw link surfaced in `elytro --help`: `https://raw.githubusercontent.com/Elytro-eth/skills/main/SKILL.md`

Need to **swap tokens? Install [`defi/uniswap/SKILL.md`](./defi/uniswap/SKILL.md).**  
Need to execute another protocol flow? Install that protocol’s folder (e.g., `defi/pendle/SKILL.md`) alongside [`defi/elytro/SKILL.md`](./defi/elytro/SKILL.md).

## Start Here

1. **Install the Elytro CLI** – `npm install -g @elytro/cli` (Node ≥ 24). Most workflows reference CLI commands, so have it ready.
2. **Load the `elytro` wallet skill** – located at `elytro/SKILL.md`. That skill covers account management, inline-button UX rules, and Elytro-specific safety guidance.
3. **Pick the right DeFi stack** – browse `defi/SKILL.md`. It links to protocol skills (Uniswap today, more coming) and the execution bridge (`defi/elytro/SKILL.md`).
4. **Combine as needed** – for a token swap you typically load three skills simultaneously:
   - `elytro` (wallet UX, menus, account safety)
   - `defi` (routing dispatcher + checklist)
   - `defi/uniswap` (Uniswap AI planner prompts)  
     Once the planner produces calldata/UserOps, hand them to `defi/elytro`.

## Skill Map

| Path            | Description                                                                 | Use Cases                                                                            |
| --------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `elytro/`       | Elytro wallet main skill. Inline button rules, menus, tx approvals.         | Anything involving Elytro smart accounts (balances, send, deploy, security).         |
| `defi/`         | Directory skill that triages DeFi intents and links to protocol sub-skills. | When a user simply says “do DeFi” or hasn’t picked a protocol yet.                   |
| `defi/elytro/`  | Execution bridge from planner calldata/UserOps into Elytro smart accounts.  | Running Uniswap AI instructions, relaying calldata, simulating & sending tx/UserOps. |
| `defi/uniswap/` | Uniswap AI planning prompts and guardrails.                                 | Swaps, LP adds/removes, Uniswap analytics before execution.                          |
| `payroll/`      | Payroll runbook for Elytro smart accounts.                                  | Recurring ETH/USDC payouts with manual approval every pay period.                    |

Add more folders under `defi/` (`defi/<protocol>/SKILL.md`) to extend the pack; the directory skill will automatically link to them once documented.

## Installation Cheat Sheet

```bash
# Install the whole pack (skills CLI)
npx skills add Elytro-eth/skills

# Focus on the Elytro wallet skill
npx skills add Elytro-eth/skills --skill elytro

# Uniswap planner only
npx skills add Elytro-eth/skills --skill defi/uniswap
```

Clawhub users can add the repo once, then enable whichever folders are needed per workspace. No repackaging required; Clawhub preserves the `<folder>/SKILL.md` layout.

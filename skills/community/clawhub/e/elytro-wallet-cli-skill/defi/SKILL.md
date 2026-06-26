---
name: defi
description: Start-page skill that routes Elytro agents to the correct DeFi protocol playbook.
user-invocable: true
disable-model-invocation: false
allowed-tools: []
related-skills: ["elytro", "defi/elytro", "defi/uniswap"]
---

# Elytro DeFi Directory

Load this skill whenever a user asks for "DeFi" without specifying a protocol. It acts as a menu linking to the protocol-specific skills in this repo.

## How to Use

1. **Clarify intent** – Ask the user what they need (swap tokens, earn yield, borrow, repay, etc.).
2. **Map intent to a protocol** – Use the table below to choose the closest skill.
3. **Follow that skill's instructions** – Each protocol skill links back to `defi/elytro` so you can execute through the Elytro CLI.

## Protocol Menu

| Goal | Recommended Skill | Why |
| --- | --- | --- |
| Swap tokens, add/remove Uniswap liquidity | `defi/uniswap` | Uses the Uniswap AI planner to draft calldata/UserOps for Elytro execution. |
| Relay calldata/UserOp output from any planner | `defi/elytro` | Base workflow once a planner produced calldata or a UserOperation. |
| Wallet orchestration & inline buttons | `elytro` | Mandatory UX rules + Elytro CLI commands. |
| Need another protocol? | Open an issue | File a request describing the desired protocol and workflow; we'll add another skill. |

## Tips

- Keep this skill loaded while navigating the rest so you can quickly route follow-up requests to the right protocol.
- When in doubt, start with `defi/elytro`; it contains the common execution pattern shared by every other protocol skill.

# Elytro DeFi Skill Hub

A curated directory of Agent Skills that teach AI wallets how to coordinate Elytro ERC-4337 smart accounts with intent planners across major DeFi protocols. Think of it as a DeFi “start page” that gives agents one place to discover protocol-specific skills and jump into execution immediately.

## Available Skills

| Path                                               | Description                                                                                              |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`SKILL.md`](./SKILL.md)                           | Root doc linked from `elytro --help`; explains how to combine the wallet and DeFi sub-skills.            |
| [`elytro/SKILL.md`](./elytro/SKILL.md)             | Elytro wallet skill, covering menus, inline-button UX, and CLI safety.                                   |
| [`defi/SKILL.md`](./defi/SKILL.md)                 | DeFi directory that routes ambiguous intents to the right protocol skill.                                |
| [`defi/elytro/SKILL.md`](./defi/elytro/SKILL.md)   | Execution bridge that runs planner calldata/UserOps through Elytro smart accounts.                       |
| [`defi/uniswap/SKILL.md`](./defi/uniswap/SKILL.md) | Prompts and guardrails for using Uniswap AI to plan swaps/liquidity moves before handing them to Elytro. |

## Installation

### Agent Skills CLI (`skills.sh`)

Add this skill collection with the [Agent Skills CLI](https://skills.sh):

```bash
npx skills add Elytro-eth/skills
```

(Or install directly from GitHub: `npx skills add https://github.com/Elytro-eth/skills`.)

### Clawhub

Clawhub ingests the same `<folder>/SKILL.md` layout, so you can import this repo directly:

1. In the Clawhub app (or CLI) choose **Add skill pack → From Git** and paste `https://github.com/Elytro-eth/skills`.
2. Clawhub downloads the repo and exposes each folder (`elytro`, `defi`, `defi/elytro`, `defi/uniswap`, etc.) as an installable skill.
3. Use the imported skills inside your Clawhub workspace just like any other pack (link them to plans, attach to agents, and configure environment variables where needed).

No additional conversion steps are required because the repo already follows the Agent Skills spec.

## Usage

1. **Read [`SKILL.md`](./SKILL.md)** – this is the canonical doc linked from `elytro --help`. It explains how to combine the wallet + DeFi skills.
2. **Load [`elytro`](./elytro/SKILL.md)** for any wallet-facing workflow (menus, approvals, balances, etc.).
3. **Load [`defi`](./defi/SKILL.md)** when the user just says “do DeFi” and you need to route them.
4. **Load [`defi/uniswap`](./defi/uniswap/SKILL.md)** to collaborate with Uniswap AI, then hand its output to [`defi/elytro`](./defi/elytro/SKILL.md) for execution.

## Contributing

1. Add a new folder under `./defi/<protocol>/` (or another domain) with a `SKILL.md` that follows the Agent Skills spec (e.g., `defi/pendle/SKILL.md`).
2. Update [`defi/SKILL.md`](./defi/SKILL.md) to mention the new protocol and link to the folder.
3. Keep CLI commands pinned (e.g., `elytro` version) and document all required environment variables.

PRs welcome for new protocols (Pendle, Aave, Curve, etc.) or improvements to the planner prompts.

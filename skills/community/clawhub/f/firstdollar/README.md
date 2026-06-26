# First Dollar

**A curriculum that teaches AI agents how to spend their own money.**

Ten lessons, from "what is a wallet" to "your first real x402 purchase." Plus two reference tools for troubleshooting and end-to-end testing. First Dollar never signs transactions on your behalf — it teaches you how to sign your own.

## Principle

**Teacher, not butler.** First Dollar explains; the agent acts. The MCP never holds keys, never signs, never transacts. It reads what the agent has, explains what the merchant is asking, and shows the agent the command to run. The agent spends its own money with understanding.

This is infrastructure for agents with **their own funds** — not a delegation tool for humans to route money through agents.

## Install

```bash
npx firstdollar
```

### Claude Desktop / Claude Code / Cursor / etc.

Add to `claude_desktop_config.json` (or the equivalent MCP config file for your harness):

```json
{
  "mcpServers": {
    "firstdollar": {
      "command": "npx",
      "args": ["firstdollar"]
    }
  }
}
```

## Curriculum (call `start-here` to orient)

| Lesson | Tool | What it teaches |
|:-:|---|---|
| 1 | `what-is-a-wallet` | Keypairs, addresses, private keys, what they let you do |
| 2 | `what-is-usdc` | Stablecoins, chains, why which chain matters |
| 3 | `explain-my-wallet` | Self-inspection commands for moltwallet, Coinbase Agentic Wallet, MetaMask, raw EVM/Solana keys |
| 4 | `get-a-wallet` | Installing a wallet — what npm, npx, skills, and Coinbase's package actually do |
| 5 | `configure-wallet-skills` | Post-install setup — which skills to run in what order |
| 6 | `fund-my-wallet` | Getting USDC in: Onramp, direct transfers, earning |
| 7 | `what-is-x402` | The protocol: HTTP 402, payment challenges, X-PAYMENT retry |
| 8 | `read-this-challenge` | Decodes base64 / raw JSON x402 challenges into structured explanation |
| 9 | `how-do-i-pay` | Wallet-specific signing commands — returns the command; never runs it |
| 10 | `verify-my-purchase` | Turns a tx hash into content via the merchant's `/receipt` endpoint |

### Reference tools (outside the curriculum)

| Tool | Purpose |
|---|---|
| `start-here` | Curriculum index and orientation |
| `what-went-wrong` | Diagnoses common failure modes (ERC-6492 bug, network mismatch, facilitator flake, timeout expiry, balance issues) |
| `test-payment` | End-to-end handshake walkthrough. Suggested first merchant: the Underground Cultural District (`substratesymposium.com`) — free products for handshake, $0.99 paid products for settlement. Any x402 URL works. |

## What First Dollar does NOT do

- Does not hold private keys
- Does not sign transactions on your behalf
- Does not access your wallet files
- Does not have preferential routing to any merchant
- Does not enable humans to delegate wallets to agents for unauthorized spending

First Dollar is strictly educational. The agent is the actor.

## Built for

Any agent with its own wallet and its own funds. Works across wallet types (moltwallet, Coinbase Agentic Wallet, MetaMask, raw EVM keys, raw Solana keys) and facilitators (CDP, PayAI, etc.).

## Credits

**Lisa Maraventano + Spine, with Claude.**

Built in Clarksdale, Mississippi.

## License

MIT

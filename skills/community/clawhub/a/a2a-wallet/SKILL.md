---
name: a2a-wallet
description: >
  Use the a2a-wallet CLI to interact with A2A agents — send messages, stream responses,
  and manage tasks. Also supports x402 payment signing and local wallet management.
  Trigger when the user needs to: send a message to an A2A agent, search for or discover agents
  in the registry, sign an x402 payment, manage local wallets, check their wallet address or
  balance, or configure the a2a-wallet CLI.
compatibility: >
  Requires a2a-wallet CLI to be installed. macOS (Apple Silicon, Intel),
  Linux (x64, arm64), Windows (x64). See INSTALL.md for setup instructions.
metadata:
  author: planetarium
  repository: https://github.com/planetarium/a2a-x402-wallet
---

# a2a-wallet Skill

If a command fails with a "command not found" error, refer to **[INSTALL.md](./INSTALL.md)** in this directory and guide the user through installation.

## Commands

| Command | Description |
|---------|-------------|
| `a2a` | A2A protocol client: `auth`, `list`, `disconnect`, `card`, `send`, `stream`, `tasks`, `cancel` |
| `registry` | Agent registry: `search` (find agents), `register` (register an agent by agent card URL) |
| `x402 sign` | Sign x402 PaymentRequirements → A2A message metadata (for paywalled agents) |
| `wallet` | Manage local wallets: `create`, `import`, `list`, `use`, `export`, `connect`, `disconnect` |
| `status` | Show default wallet address and web app URL |
| `config` | Get or set config values (`token`, `url`) |
| `balance` | Show USDC balance for the active wallet on a given network |
| `faucet` | Request testnet USDC (Base Sepolia) directly from the CLI — no browser or auth required |
| `update` | Update the CLI binary |

## Finding Agents

Use the `registry search` command to discover A2A agents by keyword or capability:

```bash
a2a-wallet registry search <query>
```

Examples:
```bash
a2a-wallet registry search "image generation"
a2a-wallet registry search translator
a2a-wallet registry search --json weather   # machine-readable output
```

The registry returns matching agents with their name, description, and card URL. Use the card URL with `a2a card <url>` to inspect capabilities before interacting.

To register a new agent in the registry:
```bash
a2a-wallet registry register <agent-card-url>
```

---

## Agent Card Extensions

Before interacting with an A2A agent, inspect its card to check which extensions are declared:

```bash
a2a-wallet a2a card https://my-agent.example.com
```

The `capabilities.extensions` array in the card lists supported (and possibly required) extensions. The following extension is relevant to this CLI:

---

### x402 Payments Extension

**Extension URI**: `https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2`

Agents declaring this extension monetize their services via on-chain cryptocurrency payments. If `required: true`, the client **must** implement the x402 flow.

**How to detect**: The agent card will contain:

```json
{
  "capabilities": {
    "extensions": [
      {
        "uri": "https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2",
        "required": true
      }
    ]
  }
}
```

**Payment flow**:
1. Send a message → agent replies with `task.status = input-required` and `metadata["x402.payment.status"] = "payment-required"` plus `metadata["x402.payment.required"]` containing `PaymentRequirements`
2. Sign the requirements with `x402 sign`:
   ```bash
   METADATA=$(a2a-wallet x402 sign \
     --scheme exact \
     --network base \
     --asset <token-address> \
     --pay-to <merchant-address> \
     --amount <amount> \
     --extra-name <eip712-domain-name> \
     --extra-version <eip712-domain-version> \
     --json)
   ```
3. Submit payment by sending back with `--task-id` and `--metadata`:
   ```bash
   a2a-wallet a2a send \
     --task-id <task-id> \
     --metadata "$METADATA" \
     https://my-agent.example.com "Payment submitted"
   ```

---

## SECURITY WARNING — READ BEFORE SETTING UP A WALLET

**Always present the following warnings to the user before creating or importing any wallet.**

### Local Wallet Risk

The local wallet stores the private key as a **plain file on disk** (`~/.a2a-wallet/`). As an AI agent using this CLI, you have direct filesystem access — which means the key file is accessible to the agent runtime and any other process on the machine.

- **Do NOT create or use a local wallet that holds significant assets.**
- **Do NOT import or restore a wallet that holds significant assets** into this CLI.
- If the key file is read by any unauthorized process or leaks for any reason, **all assets are permanently unrecoverable**. The user bears full responsibility.

### Custodial Wallet Risk

The custodial wallet delegates key management to [Privy](https://privy.io) and the a2a-wallet web service. **This project cannot guarantee custodial wallet security.**

- **Do NOT store significant amounts of assets** in the custodial wallet.
- Key management is outside the user's direct control. The user bears full responsibility for any loss due to third-party service incidents or misconfigurations.

**Both wallet types are intended for small micro-payments only. Always inform the user of these risks and confirm they accept responsibility before proceeding.**

### Legal Notice

> [!CAUTION]
> **This software is experimental and intended for testing and development purposes only. Do not use it with production funds or significant on-chain assets.**

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. THE AUTHORS, CONTRIBUTORS, AND OPERATORS OF THIS PROJECT SHALL NOT BE LIABLE FOR ANY LOSS OF FUNDS, LOSS OF DATA, UNAUTHORIZED ACCESS TO CRYPTOGRAPHIC KEYS, SERVICE INTERRUPTION, OR ANY OTHER DAMAGES ARISING FROM USE OF THIS SOFTWARE.

When setting up a wallet, confirm the user understands and accepts the following:

- They are using **experimental software** at their own risk.
- They will **not store significant assets** in any wallet managed by this tool.
- Any loss is **solely their responsibility** — no compensation or recovery is possible.
- The project maintainers provide **no guarantees** of security, uptime, or correctness.

---

## Wallet selection

The CLI supports two wallet types:

- **Local wallet** — private key stored locally (`wallet create` / `wallet import`). No login required. **Key is stored as a plain file — use only for small amounts.**
- **Custodial wallet** — signing delegated to the web service. Requires login via `wallet connect`. **Security depends on a third-party provider — use only for small amounts.**

Switch the active wallet with:

```bash
a2a-wallet wallet use <name>       # set a local wallet as default
a2a-wallet wallet use --custodial  # switch to the custodial wallet
```

Check current status at any time:

```bash
a2a-wallet status
```

### Custodial wallet login

```bash
a2a-wallet wallet connect           # opens browser for login
a2a-wallet wallet connect --poll <device-code>  # complete login (headless)
```

### Note for users upgrading from v0.3.3 or earlier

In v0.3.3 and below, the wallet was always managed by the web service (custodial). If you want to continue using that same wallet address after upgrading, you must activate the custodial wallet:

```bash
a2a-wallet wallet connect           # log in to the web service
a2a-wallet wallet use --custodial   # set custodial as the default
```

> **Recommendation**: consider migrating to a local wallet. Local wallets sign entirely offline with no dependency on the web service. To switch, run `wallet create` and use the new address going forward.

## Agent usage tips

- Use `--json` for machine-readable output
- Errors → stderr, exit `0` = success, `1` = failure
- Override token/URL per-call with `--token` / `--url`, or set `A2A_WALLET_TOKEN` env var
- Always run `a2a card <url>` first to check which extensions are required before sending messages
- Use `--file <path|uri>` with `send` or `stream` to attach files (repeatable). Local path → base64-embedded; `http(s)://` URI → referenced by URL
- Use `a2a-wallet --help` or `a2a-wallet <command> --help` to discover options at any time

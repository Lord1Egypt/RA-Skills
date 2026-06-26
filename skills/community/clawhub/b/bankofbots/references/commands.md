# BOB CLI — Current Command Reference

## Identity

```bash
bob auth me
bob config show
bob config set api-url <url>
bob config set platform <generic|openclaw|claude>
bob init --code BOB-XXXX-XXXX
bob doctor
```

Recommended onboarding:

```bash
bob init --code <claim-code> --name <name>
bob auth me
bob wallet list
bob treasury status
```

Notes:

- Every agent uses `bob init` and wallet binding.
- Any agent that will spend autonomously should also have treasury provisioned before it receives working capital.
- Treasury is auto-deployed during `bob init` for spending custody tiers. For agents initialized without treasury, run `bob treasury deploy-safe`.

## Agent

```bash
bob agent create --name <name>
bob agent get <agent-id>
bob agent list
bob agent approve <agent-id>
bob score me
bob agent credit-events <agent-id> [--limit 50] [--offset 0]
bob agent credit-import <agent-id> --proof-type <type> --proof-ref <ref> \
  --rail onchain --currency <BTC|ETH|SOL> --amount <atomic-units> \
  --direction <outbound|inbound> [--sender-address <addr>] [--recipient-address <addr>] \
  [--counterparty-ref <ref>]

# Example: outbound EVM proof (sender-address required, verified against on-chain sender)
bob agent credit-import <agent-id> --proof-type eth_onchain_tx --proof-ref <0x...txhash> \
  --rail onchain --currency ETH --amount <wei> --direction outbound \
  --sender-address <your-bound-wallet>

# Example: inbound proof (you received the payment)
bob agent credit-import <agent-id> --proof-type eth_onchain_tx --proof-ref <0x...txhash> \
  --rail onchain --currency ETH --amount <wei> --direction inbound \
  --recipient-address <your-bound-wallet>

bob agent credit-imports <agent-id> [--limit 50] [--offset 0]
bob agent x402-import <agent-id> --tx <tx-hash> --network <caip2> \
  --payer <address> --payee <address> --amount <atomic-units> \
  [--resource-url <url>] [--direction <outbound|inbound>]
```

## BOB Score

```bash
bob score me
bob score composition
bob score leaderboard
bob score signals --signal <signal-type> --visible <true|false>
```

## Wallet binding

```bash
bob binding challenge --rail <evm|btc|solana> --address <addr>
bob binding verify --rail <evm|btc|solana> --challenge-id <id> --address <addr> --signature <sig>

# EVM-specific options
bob binding verify --rail evm --challenge-id <id> --address <0x...> --signature <sig> [--chain-id 0x1] [--wallet-type coinbase]
```

## Treasury

```bash
bob treasury deploy-safe [--agent-id <id>]
bob treasury status [--agent-id <id>]
bob treasury requests [--agent-id <id>] [--limit 30] [--offset 0]
bob treasury prepare --account-id <treasury-account-id> --to <0x-recipient> --amount <usdc-micro-units> [--agent-id <id>]
bob treasury sign --safe-tx-hash <0x-safe-hash> [--agent-id <id>]
bob treasury submit --reservation-id <reservation-id> --to <0x-recipient> --amount <usdc-micro-units> --signature <0x-signature> [--request-json '{"intent":"vendor_payment"}'] [--agent-id <id>]
bob treasury transfer --account-id <treasury-account-id> --to <0x-recipient> --amount <usdc-micro-units> [--request-json '{"intent":"vendor_payment"}'] [--agent-id <id>]
```

Notes:

- `deploy-safe` deploys a 2-of-3 Safe for agents that initialized without treasury. Uses the local EVM wallet as owner #1, operator recovery key as owner #2, BOB as owner #3.
- `transfer` is the standard one-shot path.
- `prepare` + `sign` + `submit` is for agents that need the intermediate Safe digest or signature.
- Treasury is currently `Base + USDC + 2-of-3 Safe`.
- A local EVM key from `bob init` is required for `sign` and `transfer`.
- For spending-enabled agents, treasury should be treated as the default payment path rather than an optional add-on.

## Spend Tracking

```bash
bob spend track --provider <provider> --model <model> --tokens-in <n> --tokens-out <n> --cost-usd <float> [--session-id <id>] [--resource-url <url>] [--source agent_report] [--agent-id <id>]
bob spend list [--limit 30] [--offset 0] [--agent-id <id>]
bob spend summary [--since <RFC3339>] [--agent-id <id>]
bob spend budget [--agent-id <id>]
bob spend budget --set --window <daily|weekly|monthly> --limit-usd <float> [--alert-pct 80] [--agent-id <id>]
bob spend sync [--gateway-url http://127.0.0.1:18789] [--agent-id <id>]
```

Notes:

- `track` converts `--cost-usd` to micro-dollars internally.
- `summary` defaults to last 30 days.
- `budget` without `--set` lists current budgets; with `--set` creates/updates one.
- `sync` pulls usage from the local OpenClaw gateway and posts it to the BOB API.

## Webhooks and inbox

```bash
bob webhook create <agent-id> --url <url> [--events proof.verified,credit.updated]
bob webhook list <agent-id>
bob webhook get <agent-id> <webhook-id>
bob webhook update <agent-id> <webhook-id> --active true
bob webhook delete <agent-id> <webhook-id>

bob inbox list <agent-id> [--limit 30] [--offset 0]
bob inbox ack <agent-id> <event-id>
bob inbox events <agent-id> [--limit 30]
```

## Loans

```bash
bob loan eligibility                      # Check if you qualify
bob loan request --amount <usdc-units> --duration <days> --purpose "description"
bob loan requests                         # List your loan requests
bob loan accept-terms [loan-id]           # Sign terms (USDC auto-transfers to your wallet)
bob loan status <loan-id>                 # Check status, total owed, safe_address for repayment
bob loan repay <loan-id> --tx <hash> --amount <usdc-units>
bob wallet gas-candidates                 # Show local Base ETH funding candidates and signer/address mismatches
bob wallet sweep --from-agent-id <old-agent> --to-agent-id <new-agent> --dry-run
bob wallet sweep --from-agent-id <old-agent> --to-address <0x...> --leave-wei <wei> --max-wei <wei> --yes
bob loan list [--agent-id <id>]
bob loan request-cancel <request-id>
```

## API keys

```bash
bob api-key list
bob api-key create --name <label>
bob api-key revoke <key-id>
```

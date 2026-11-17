# Managed wallets and Coinbase account access

Select one model matching the user's task. Do not silently replace an existing wallet or import a raw key to simplify setup.

| Surface | What it controls | Setup distinction |
| --- | --- | --- |
| Alchemy Agent Wallet | Provider-held keys through an approved session | Operator authorizes `alchemy wallet connect --mode session`; check session expiry, wallet address and actual limits |
| Coinbase for Agents | Coinbase Advanced Trade account access, optionally scoped to a separate spot portfolio | Existing Coinbase account and explicit portfolio permissions; not a general DeFi contract signer |
| Coinbase Agentic Wallet | Coinbase-managed wallet used through `awal` or payments MCP | Login can create a wallet; funding and payment permissions are separate decisions |

[Alchemy Agent Wallets](https://www.alchemy.com/docs/agent-wallets) keep the signer behind a dashboard-approved session. Prefer the session route over local key creation. `alchemy wallet status --verify` checks an existing backend session; status alone does not approve a transaction. Revoke through the provider's session controls when the mandate expires. Its EVM session uses smart-wallet calls; it does not expose raw transaction signing. Sponsorship policies control fees, not wallet spending.

[Coinbase for Agents setup](https://docs.cdp.coinbase.com/coinbase-for-agents/overview) currently restricts its remote OAuth MCP to an explicit harness allowlist. Hermes/custom harnesses should use the official CLI, not assume `https://agents.coinbase.com/mcp` will authenticate. Verified CLI: `@coinbase/coinbase-cli@0.0.7`, Node 22+. An operator configures a deliberately scoped key using `coinbase env live --key-file <private-file>`; `coinbase balance` and `coinbase portfolios list` check access. Keep key files outside the repo and verify secure credential storage on the target OS. Choose the intended spot portfolio rather than silently granting the default portfolio; derivatives have different portfolio constraints. Do not enable trading or transfer permissions just to read balances.

[Agentic Wallet CLI setup](https://docs.cdp.coinbase.com/agentic-wallet/cli/quickstart) documents `awal status --json`, `awal address` and `awal balance --chain base --json`. Reviewed version: `awal@2.12.1`. Its npm engine allows older Node but the official quickstart requires Node 24+; follow the documented requirement. `awal auth login <email>` sends an OTP and can create a wallet; `awal auth verify <flowId> <otp>` completes authentication. Keep OTPs and session material out of chat logs. Base is the documented default; pass the intended supported chain explicitly. Do not infer that support for a balance or transfer means arbitrary contract calls or LP position management are supported.

## Coinbase Wallet MCP and WalletConnect

[Wallet MCP](https://docs.cdp.coinbase.com/ai-agents/coinbase-for-agents/wallet-mcp), formerly Base MCP, now uses OAuth at `https://wallet-mcp.coinbase.com`. Its upstream skill identifier remains `base-mcp`. Read existing wallets/session state before proposing setup. Account connection does not replace Coinbase Wallet's approval for write actions, including personal/typed signatures; track `get_request_status` for the exact request.

Wallet history covers the connected Coinbase Wallet and in-session agent wallets, rejects third-party addresses, uses cursors and offers no date-range filter. Inspect amount units and exact contract decimals. Protocol batch builders return proposed calls; review every nested approval/action before `send_calls`. Readiness means selected account/chain plus a bounded read; an approval link means requested, not completed.

[WalletConnect Agent SDK](https://github.com/WalletConnect/agent-sdk) is beta. Persisted sessions require active account, chain/method scope, expiry and revocation checks. Signing can auto-connect, and agent-mode send can auto-bridge missing gas. A session lookup is not authorization for a new connection, bridge, signature or transfer. Do not invoke those paths under narrower authority; use inspected non-writing commands for readiness.

# Security

Wallet design:

- Generate a unique Base hot wallet locally when no wallet exists for the user profile.
- Reuse the existing local wallet on reinstall or repeat setup unless the user intentionally resets local state.
- Store private key only under `~/.x402-agent-voice/wallet.json`.
- File mode should be `0600`; directory mode should be `0700`.
- Never print the private key.
- Never transmit the private key to ForgeMesh or any remote service.
- Use the wallet only for small working balances.
- Warn users that each machine, container, or user profile gets a separate wallet unless they deliberately copy local state.
- Provide an explicit USDC withdrawal path for leftover funds.
- Withdrawals must confirm before broadcasting unless the user passes an explicit noninteractive approval flag.
- Normal Base USDC withdrawals require Base ETH for gas; do not hide this from users.

Agent controls:

- Enforce `requireApproval: true` by default.
- Enforce `perCallCapUsd` before signing.
- Enforce `dailyCapUsd` before signing.
- Maintain allowlists and denylists before broad routing is added.
- Export receipts without exposing signatures or private keys.

Marketing boundary:

Use "agent payment safety", "spend caps", and "compatibility". Do not market this as anonymity, laundering, evasion, or hiding illegal activity.

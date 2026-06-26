---
name: Dogecoin
description: Assist with Dogecoin DOGE transactions, wallet management, and network characteristics.
metadata: {"clawdbot":{"emoji":"🐕","os":["linux","darwin","win32"]}}
---

## Network Basics
- Dogecoin is Bitcoin fork — similar UTXO model and transaction structure
- Proof of Work with Scrypt — merged mining with Litecoin
- 1 minute block time — faster than Bitcoin's 10 minutes
- No supply cap — inflationary by design, ~5 billion new DOGE per year
- Low transaction fees — typically less than 1 DOGE

## Address Format
- Addresses start with "D" — legacy format, always verify first character
- 34 characters total — standard length like Bitcoin
- Case-sensitive — typos cause lost funds
- No SegWit or Taproot — simpler than modern Bitcoin

## Transaction Characteristics
- Transactions confirm in ~1 minute — one block for basic confirmation
- 6 confirmations for high-value — ~6 minutes, same security practice as Bitcoin
- Fees are minimal — 1 DOGE per KB is standard, most transactions under 1 DOGE
- No RBF (Replace-By-Fee) — stuck transactions harder to fix than Bitcoin
- UTXO model — balance is sum of unspent outputs

## Wallet Options
- Dogecoin Core full node — downloads entire blockchain, most secure
- MultiDoge light wallet — faster sync, SPV verification
- Ledger and Trezor support — hardware wallet integration
- Trust Wallet, Exodus — multi-coin wallets with DOGE support
- Avoid web wallets — custody risk, prefer local wallets

## Common Issues
- Transaction unconfirmed — wait, DOGE doesn't have RBF to speed up
- "Dust" outputs — very small UTXOs may cost more in fees than value
- Wallet sync slow — Dogecoin Core needs full blockchain download
- Balance not showing — wallet not fully synced, wait for sync completion
- Sent to wrong address — transactions irreversible, triple-check addresses

## Exchange Considerations
- Most major exchanges support DOGE — high liquidity pairs
- Withdrawals may have minimums — check exchange requirements
- Network confirmations required — usually 6-20 depending on exchange
- No memo/tag required — unlike XRP, simple address only
- Some exchanges don't support all address types — verify compatibility

## Fee Management
- Fees based on transaction size in bytes — not DOGE amount
- Consolidating many small UTXOs costs more — larger transaction
- Most wallets calculate fees automatically — rarely need manual adjustment
- Minimum relay fee exists — transactions below threshold rejected by nodes
- During low activity, minimum fees always work — no fee market pressure

## Security
- Standard cryptocurrency security — seed phrase is everything
- 12 or 24 word seed phrases — depends on wallet
- Never share private keys — no legitimate service asks for them
- Verify wallet downloads — get from official sources only
- Cold storage for large amounts — hardware wallet or paper wallet

## Merged Mining
- Dogecoin merge-mined with Litecoin — shares Scrypt PoW
- Increases security — benefits from Litecoin's hashrate
- No action required from users — happens at mining level
- Makes 51% attacks more expensive — combined hashrate protection

## Use Cases
- Tipping and microtransactions — low fees make small payments viable
- Community currency — strong meme culture and community
- Learning cryptocurrency — simpler than Bitcoin, lower stakes
- Payments where accepted — some merchants accept DOGE
- Speculation — high volatility, meme-driven price movements

## Scam Recognition
- "Double your DOGE" always scam — no exceptions
- Fake Elon Musk giveaways — extremely common, all fake
- Phishing wallet sites — verify URLs carefully
- Mining apps that require deposit — legitimate mining doesn't work this way
- "Support" asking for keys — no real support needs private keys

## Network Limitations
- No smart contracts — simple transaction-only blockchain
- No DeFi natively — wrapped DOGE exists on other chains
- No staking — Proof of Work only
- Limited development activity — slower updates than other chains
- Scalability similar to Bitcoin — throughput limitations

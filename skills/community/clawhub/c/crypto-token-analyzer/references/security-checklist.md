# Security Checklist (GoPlus + Manual)

Always surface these high-impact items first when present.

## Critical Red Flags

- `'is_honeypot' = "1"` → cannot sell, treat as scam
- High `'buy_tax'` or `'sell_tax'` (especially >10 - 15%)
- `'is_mintable' = "1"` and ownership not renounced
- `'can_take_back_ownership'` / `'owner_change_balance'` / `'hidden_owner'`
- `'transfer_pausable' = "1"`
- Extremely concentrated holders (top 10 hold most supply) + unlocked liquidity
- Contract not open source (`'is_open_source' = "0"`) combined with other risks

## Important but Context-Dependent

- `'is_proxy' = "1"` (upgradeable) — higher risk if ownership active
- Low `'lp_holder_count'` or unlocked LP
- `'is_blacklisted'` / trading restrictions
- Very new pair (< few hours) + low liquidity
- Extremely rapid holder-count increase (especially on new pairs) or stagnant/declining holders while volume/price heat is high — may indicate bot activity, wash trading, or weak organic demand

## Positive Signals

- Ownership renounced
- Liquidity locked (check lock duration if available)
- Contract verified / open source
- Reasonable taxes (or 0)
- Healthy holder distribution + active trading (buys ≈ sells or balanced)
- Holder growth rate and speed appear organic relative to volume, txn activity, and overall token heat

When GoPlus data is incomplete (common on Solana or brand-new tokens), clearly state the limitation and recommend manual verification on the explorer + DexScreener.
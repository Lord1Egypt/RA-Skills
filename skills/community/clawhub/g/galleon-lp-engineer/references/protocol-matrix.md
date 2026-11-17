# Protocol matrix

| Concern | Uniswap v2 | Uniswap v3 | Uniswap v4 | Aerodrome classic | Slipstream |
|---|---|---|---|---|---|
| Position | ERC-20 LP | NFT | Manager position or hook-issued shares | ERC-20 LP | NFT, optionally gauge-held |
| Range | Full | Ticks | Ticks or hook-defined invariant | Full, stable or volatile invariant | Ticks |
| Pool identity | Ordered tokens and pair | Tokens and fee | Full PoolKey and PoolId | Tokens, stable flag, factory | Tokens, tick spacing, factory |
| Fees | Embedded in reserve share | Separately owed | Manager, hook, or internal-reserve model | Verify fee route | Can differ when gauge-staked |
| Rewards | External farm if any | External farm if any | Hook or external program | Gauge emissions | Gauge emissions by epoch and range |
| Lifecycle | Add, remove | Mint, increase, decrease, collect, burn | Manager actions, or hook share mint and burn | Add, stake, claim, unstake, remove | Mint, stake, claim, unstake, decrease, collect, burn |
| Main extra risk | Token and router behavior | NFT and tick math | Hook and singleton settlement | Stable invariant, gauge and voter model | Gauge custody, fee forfeiture, reward dilution |

## Preserve differences

- Do not expose `collectFees` for an ordinary v2 pair.
- Do not represent v3 decrease as tokens received until collection is reconciled.
- Do not key v4 pools by pair and fee alone.
- Do not force a hook-issued fungible share model into the concentrated-position interface.
- Do not treat Aerodrome's stable flag as display metadata.
- Do not add Slipstream swap fees and gauge emissions unless current state proves both accrue.
- Do not build downstream steps before the prior receipt supplies the actual NFT ID, LP amount, collected amount, or gauge state.

## Capability shape

Prefer venue-specific capability flags over methods that sometimes fabricate success:

```ts
type Capabilities = {
  concentrated: boolean;
  separateFeeCollection: boolean;
  nftPosition: boolean;
  gaugeStaking: boolean;
  hookAware: boolean;
  fungibleShares: boolean;
  internalReserveAccounting: boolean;
  multiCurrencyPosition: boolean;
  supportsAtomicExit: boolean;
};
```

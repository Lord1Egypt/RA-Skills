# Confirmation contract

Request confirmation in a standalone message immediately before the write.

State:

- action and protocol version
- chain name and numeric chain ID
- wallet address
- pool address or v4 PoolId and full PoolKey
- position ID or LP amount where applicable
- ordered token addresses, symbols, decimals, and exact amounts
- range, fee, tick spacing, hook, and gauge where applicable
- every transaction target and decoded function
- transaction-builder source, request ID, build time, and adjusted range or dependent amounts when applicable
- plan digest, quote mode, quote time, and signing cutoff
- native value
- approval token, spender, amount, mechanism, and expiry
- maximum input, minimum output or liquidity, slippage bound, price-impact bound, deadline, and gas estimate
- whether the result is staked, unstaked, fee-earning, reward-earning, or both as verified
- irreversible or material risks

Ask for an unambiguous confirmation of those exact terms. Do not treat a response to a different parameter set as confirmation. Any material change in wallet, chain, target, pool, token, amount, approval, range, price limit, deadline, action order, hook, gauge, or native value voids confirmation.

A bounded multi-step sequence may share one confirmation only when all targets, maximum spends, minimum receipts, dependencies, and stop conditions are shown in advance. Get separate confirmation for an unlimited approval or any approval materially broader than the intended position.

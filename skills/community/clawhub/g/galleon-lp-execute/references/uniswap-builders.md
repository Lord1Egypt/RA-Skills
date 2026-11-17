# Uniswap builders

Apply these controls when calldata comes from the Uniswap Liquidity Provisioning API or Uniswap SDKs. Verify current documentation and deployments before every live use.

## Builder boundary

An official builder is still an untrusted transaction proposal. Record its request ID, source version, request body digest, response time, and returned transaction. Check chain, sender, target, bytecode, calldata, native value, gas fields, limits, and expected state changes against the confirmed plan. Simulate through an independent RPC from the actual wallet.

Do not send a private key to the builder. API keys belong in the runtime secret store and are not wallet authority.

## LP API flow

1. Refresh position, balances, pool state, and action inputs.
2. Call the current approval-check route for the exact action and amounts.
3. Stop on any permission or KYC warning. Do not follow a returned URL or bypass eligibility automatically.
4. Decode and confirm each returned approval transaction. The current response wraps it as `transactions[].transaction`.
5. Treat typed-data permits as asset authority. Verify domain, numeric chain ID, verifying contract, spender, token, amount, nonce, expiry, and message before confirmation and signing.
6. Request the create, increase, decrease, or fee-claim transaction with the confirmed bounds.
7. Display API-adjusted prices and actual dependent token amounts. A material change voids confirmation.
8. Decode, simulate, confirm, submit once, obtain the receipt, and reread state.

An approval response can contain both ERC-20 approval transactions and EIP-712 permit data. Complete and reconcile required onchain approvals before signing the permit or requesting the position transaction.

At the reviewed API version, v4 permit data needs a signing-only normalization: replace a chain enum string with the numeric chain ID and unwrap each typed-data entry from its `fields` container. Pass the original permit object back to the API with the signature. Do not mutate the authoritative request record. The create and increase routes use different permit field names, so follow the live schema.

## Endpoint semantics

- v2 creation uses the classic route. v2 fee value is realized through the LP share, not a fee-claim route.
- v3 and v4 create responses return tick-snapped bounds. Show the adjusted values, not only requested prices.
- Increase and decrease require canonical token order and the exact position identifier.
- The current v3 decrease builder can include fee collection in the same calldata. Decode it and do not issue a second claim for the same fees.
- The current v4 fee-claim builder can encode a zero-liquidity modification followed by token-taking actions. Verify the full nested action list.
- Permissioned pool flags select a different trust and eligibility path. Never toggle them to make a failing request pass.
- There is no assumed REST migration route. Verify the current supported migration interface before planning a version migration.

Refetch and reconfirm after the plan's freshness limit, a price or state change, or any returned amount, target, approval, hook, deadline, or native value change. A fixed age such as 30 seconds can be a product default, but it is not a substitute for state-based invalidation.

Retry rate-limited reads and unsigned build requests only when they are idempotent and retain their request identity. Never place signing, submission, or broadcast inside a generic retry wrapper.

## Direct v4 path

Resolve the current StateView, PositionManager, PoolManager, Permit2, and related deployments for the bound chain. Read pool state through StateView. Use the verified PositionManager action model for create, increase, removal, and collection. Decode every action in a multicall. Native currency handling, Permit2, hook data, settlement, and fee collection are v4-specific.

If a browser interface performs the final wallet action, the same confirmation and receipt rules apply. A displayed success screen is not chain proof.

Current primary references:

- [Uniswap AI LP integration](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-trading/skills/lp-integration)
- [Uniswap AI v4 SDK integration](https://github.com/Uniswap/uniswap-ai/blob/main/packages/plugins/uniswap-trading/skills/v4-sdk-integration/SKILL.md)
- [Uniswap LP API guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide)

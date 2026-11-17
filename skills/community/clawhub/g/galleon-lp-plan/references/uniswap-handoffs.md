# Uniswap handoffs

Choose the simplest current path that preserves the reviewed plan.

## Direct transaction construction

Use current official SDKs and deployments when the wallet runtime can build and decode Uniswap transactions locally. Keep the signer outside the planner. For v4, read pool state through StateView and use the deployed PositionManager action model. Do not reuse v3 calldata.

## Official LP API

The Uniswap Liquidity Provisioning API is an optional unsigned transaction builder. Verify the current contract before use. At the reviewed source version, its LP routes include:

| Intent | Route | Versions |
|---|---|---|
| approvals and permits | `/lp/check_approval` | v2, v3, v4 |
| create concentrated | `/lp/create` | v3, v4 |
| create classic | `/lp/create_classic` | v2 |
| increase | `/lp/increase` | v2, v3, v4 |
| decrease | `/lp/decrease` | v2, v3, v4 |
| claim fees | `/lp/claim_fees` | v3, v4 |
| pool state | `/lp/pool_info` | v2, v3, v4 |

The API returns transaction data; it does not sign or broadcast. Bind the request and response to the plan, decode every returned transaction, and simulate it independently. An API simulation is supporting evidence, not authority.

Preserve these current contract details:

- Amounts are integer strings in token base units.
- A concentrated create uses exactly one of `existingPool` or `newPool` and one of `priceBounds` or `tickBounds`.
- `priceBounds` requires `quotedTokenAddress`. Display the returned adjusted range after tick snapping.
- Approval responses contain `transactions[].transaction`, not a bare transaction array.
- Approval responses can contain both onchain approvals and permit data.
- A nonempty KYC or permission warning blocks the action; an empty transaction list alone does not prove eligibility.
- Position identifiers and v4 permit fields have endpoint-specific names. Follow the current API schema instead of normalizing them into one guessed field.
- v2 has no separate fee claim. A v3 decrease built by this API can bundle fee collection, so do not schedule a duplicate claim without decoding the payload.

Do not hardcode the API host, chain list, or endpoint contract as timeless. Load API keys from the runtime secret store. Retry only idempotent reads or transaction-building requests. Never let API retry logic resubmit a wallet transaction.

## Uniswap interface link

For a manual wallet handoff, the planner may generate a link to the Uniswap position creation interface. The link prefills terms; it does not approve, sign, submit, or prove a position was created.

At the reviewed source version, the create route is `https://app.uniswap.org/positions/create` and accepts chain, ordered currencies, fee data, range state, deposit state, and an optional v4 hook. Treat this query contract as mutable and verify it against the current official skill before use.

Use the bundled helper to avoid malformed JSON query values:

```bash
node scripts/uniswap-link.mjs --help
```

Show the full URL and the bound plan together. Before the user signs, recheck the interface's displayed chain, tokens, amounts, price orientation, snapped range, fee, hook, spender, recipient, minimums, deadline, and native value. A changed interface quote expires the plan.

Current primary references:

- [Uniswap AI liquidity planner](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-driver/skills/liquidity-planner)
- [Uniswap AI LP integration](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-trading/skills/lp-integration)
- [Uniswap LP API guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide)

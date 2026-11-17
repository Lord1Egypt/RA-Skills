# Exposure and order lifecycle

## Market analysis and hedge planning

Record exact market ID, venue version/network, collateral, settlement currency, contract multiplier, expiry and rate convention. Reconcile account/subaccount positions, active orders and available margin at a coherent observation time. Keep mark, oracle and executable order-book prices distinct. Use official fixed-point helpers; avoid JavaScript floating-point conversion for transaction quantities.

For a hedge, show current exposure, proposed offset and residual basis risk. Include other pending orders, fees, funding/borrow payments, collateral haircuts and liquidation buffers. Stress the instruments together: a profitable position on one venue cannot automatically protect collateral liquidating elsewhere. Avoid assuming correlation, funding direction or liquid exit remains stable.

| Product | Required additional checks |
| --- | --- |
| Perpetual | Index/mark/oracle divergence, funding interval and sign, cross/isolated margin, available open interest/capacity, liquidation and ADL behavior, reduce-only constraints. |
| Option | Underlying, expiry/timezone, strike, call/put, premium and settlement currency, multiplier, exercise/settlement model, margin method, short-option tail loss and liquidity. |
| Funding-rate derivative | Reference rate and its sampling/settlement interval, maturity, fixed/floating direction, collateral and margin, rate units and underlying hedge basis. Boros rate exposure is not a token-price perpetual. |

Derive supports options and perps; Boros supports funding-rate derivatives. Use provider instrument metadata for the actual payoff and maturity. Do not infer a recommendation from historical yield or use a default maximum leverage as the user's risk budget. [Derive protocol overview](https://docs.derive.xyz/), [Boros official plugin](https://github.com/pendle-finance/pendle-ai/blob/main/packages/plugins/pendle-boros/README.md), accessed 2026-09-05.

## Reviewable order ticket

Include owner/subaccount and signer role; exact market; direction and reduce-only; quantity in native units plus economic notional; limit/trigger/acceptable price; collateral delta; margin mode; time-in-force/expiry; maximum slippage and fees; recipient/referral policy; current risk estimate; source timestamps; simulation result or absence; and stable request/order identity. Show dependencies such as collateral deposit or delegation as separate actions.

Use the official builder and preserve its precision conventions. For GMX, SDK prices commonly use 30 decimals while raw contract price is adjusted by index-token decimals. Native execution fee, collateral token amount and USD size have different units; use the SDK conversion rather than copying numeric examples. [GMX ExchangeRouter](https://docs.gmx.io/docs/api/contracts/exchange-router/), accessed 2026-09-05.

## Submit only under existing authority

The reviewed ticket and current user authorization must cover the exact action. Signing a relayed intent is economically meaningful even without paying gas directly. Delegating a key, increasing leverage, changing collateral mode and approving fees are not implied by research or software installation. The agent should hand off to the existing trusted execution path; no key handling belongs in chat or plan artifacts.

Persist the request/client-order ID and normalized terms before submission. On timeout or lost response, retain them and query the original order. Do not generate a new ID to retry an operation that may already exist. Serialized writes and application-level duplicate protection remain necessary even where an API provides an idempotency field.

## Venue reconciliation

- **GMX v1:** wait for transaction receipt, then on-chain order creation and keeper outcome; indexed trade history can lag. The SDK lacks built-in idempotency and receipt waiting. Reuse a coherent market/token snapshot for account reads, then refresh after writes.
- **GMX v2:** preserve requestId/idempotencyKey. Poll until `executed`, `cancelled`, `relay_failed` or `relay_reverted`. `relay_accepted`, `relay_submitted` and `created` are intermediate. Reconcile execution hash, order keys, cancellation reason and position delta. A cancellation can return collateral without accomplishing the requested trade. [GMX v1 troubleshooting](https://docs.gmx.io/docs/sdk/v1/troubleshooting/), [v2 examples](https://docs.gmx.io/docs/sdk/v2/examples/), accessed 2026-09-05.
- **Drift:** reconcile Solana transaction error/confirmation, emitted order/fill records and current user account. Keep subscription slots/freshness and oracle validity visible. A stale websocket cache is not current margin evidence. Check partial fills, active remainder and cancel races using version-matched SDK methods. [Drift account management](https://drift-labs-protocol-v2.mintlify.app/guides/account-management), accessed 2026-09-05.
- **Derive:** use a single version's order/RFQ and account contracts. Preserve order identity and compare trade results with actual subaccount balances/positions. API acknowledgement and on-chain settlement are separate evidence. Expiry or key metadata changes do not justify repeating a signed action. [Official v3 Python SDK](https://github.com/derivexyz/derive-py), accessed 2026-09-05.
- **Jupiter:** confirm the exact Perps interface exists in the selected version. A managed spot-swap tool is not a Perps order API. Preserve request identity, Solana signatures, instruction error and resulting position evidence. [Official skills](https://developers.jup.ag/docs/ai/skills), [CLI](https://developers.jup.ag/docs/ai/cli), accessed 2026-09-05.
- **Boros:** distinguish agent-signed trading from root-signed deposits, withdrawal and agent approval. Check agent expiry and treasury/gas balance; top-ups are paid actions. A withdrawal request can have a cooldown and later finalization. Reconcile order fills, settlement and collateral rather than counting a relayer response as complete. [Boros SDK](https://docs.pendle.finance/boros-dev/Backend/sdk), [Agent Trading](https://docs.pendle.finance/boros-dev/Backend/agent), accessed 2026-09-05.

## Monitoring and recovery

Return state as prepared, submitted, resting, partially filled, filled, cancelled, rejected or unknown, with timestamps and evidence. Unknown data must not become zero exposure. Track risk triggers separately from automatic actions. A stop-loss trigger is not a guaranteed exit; failed reduction or insufficient liquidity should remain an explicit unresolved exposure.

For cancel/replace, refresh current order keys and fills first, cancel the remaining quantity, resolve any race, and size the replacement from new state. A successful close on one venue does not close a paired hedge. If the observation budget expires, give the original IDs and next bounded read; do not create unattended trading or monitoring without a user request.

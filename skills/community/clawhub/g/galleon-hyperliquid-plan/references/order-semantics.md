# Order semantics

Verify every field against current official docs and SDK types.

## Identity and precision

- Default perps use their index in `meta.universe`.
- Spot uses `10000 + spotMeta.universe index`; size precision comes from the base token.
- HIP-3 uses its DEX index and that DEX's metadata. Use the official asset-ID formula and verify the resulting coin mapping.
- Mainnet and testnet identities differ.
- Price obeys the current significant-figure and decimal rules. Size rounds down to `szDecimals`.

Keep wire values as decimal strings. Reject scientific notation, negative zero, and unintended trailing precision.

## Order types

- `Gtc` may rest until fill or cancel.
- `Ioc` fills inside its limit and cancels the remainder.
- `Alo` must add liquidity and is rejected if it would cross.
- A market-style order is an `Ioc` with a user-approved worst price.
- A trigger separates `triggerPx` from execution price `p`. Mark price triggers it.
- Exit and protection orders are reduce-only.

## Grouping

- `na` creates independent orders.
- `normalTpsl` ties TP/SL children to an entry.
- `positionTpsl` ties protection to the resulting position when supported by the chosen construction.

Do not assume children protect a partial IOC fill. Plan an immediate standalone reduce-only stop for any exposed remainder.

Fixed-size triggers do not resize when a position changes. Replace protection by placing and verifying the new trigger before canceling the old one.

## Identity and lifetime

Assign each leg a unique `0x` plus 32 hex-character client order ID. Persist it before submission. Use `expiresAfter` when supported and include it in the signed intent. User-signed actions do not all support expiry.

The plan states response classes and reconciliation reads:

- top-level action rejection
- per-order error
- resting with order ID
- filled with size, average price, and order ID
- waiting for trigger or parent fill
- partial fill
- unknown response after send

## Modification and cancellation

A resting-limit modification is a new order state with a new exchange order ID and client order ID. Do not treat trigger replacement as an atomic modify. Cancel by client order ID when available; otherwise use the exchange order ID read from current state.

Scheduled cancel affects all open orders in scope, including protective triggers. Never describe it as position-aware protection.

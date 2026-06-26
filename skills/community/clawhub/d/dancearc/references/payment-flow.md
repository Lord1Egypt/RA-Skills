# x402-style payment flow (Arc native USDC)

## Client (h2a)

1. `POST` JSON to paid route **without** `X-Payment-Tx`.
2. If **402**, parse body: `x402Version === 1`, `accepts[0].payTo`, `accepts[0].maxAmountRequired`, optional `extra.perActionUsdc`.
3. Switch wallet to **Arc Testnet** (`5042002`); send **native USDC** `value` transfer to `payTo` for at least the required amount (human confirms in wallet).
4. **Retry** same `POST` with header `X-Payment-Tx: <0x…>` (tx hash).

## Server (`requireArcPayment`)

1. If no `X-Payment-Tx` → return **402** + `buildArcPaymentChallenge`.
2. **`waitForTransactionReceipt`** (avoid race vs `getTransactionReceipt`).
3. Validate `to`, `value`, `from` (optional) vs configured recipient / minimum wei.
4. **`recordNanopaymentEvent`** (demo metrics).
5. If `CIRCLE_API_KEY` set → `POST` Circle Gateway `/v1/gateway/v1/x402/verify` (non-throwing client; check `ok` in response).

## h2h (battle / coaching / beats)

No 402 loop: create intent or end session → UI **`sendNativeUsdc`** or mock hash → **`/verify` or `/grant`** with `paymentTx`.

## Headers

- Client may send `X-Payment-Tx` or server normalizes tx header (see `normalizeTxHeader` in `server/index.js`).

## Env

- `ARC_RECIPIENT` must be **valid EVM** (`0x` + 40 hex); invalid values fall back to demo address in `server/config.js`.
- `ARC_TX_RECEIPT_TIMEOUT_MS`, `ARC_TX_RECEIPT_POLL_MS` tune receipt wait.

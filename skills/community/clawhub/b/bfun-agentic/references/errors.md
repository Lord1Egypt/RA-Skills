# Common Errors

This file maps current CLI errors to likely causes and agent responses. Error strings below are taken from the existing repo implementation.

## Environment and setup

### `PRIVATE_KEY is required for this command.`

Cause:

- the user tried to run `buy`, `sell`, `send`, or `create` without `PRIVATE_KEY`

Response:

- stop
- explain that write operations require a funded signer wallet
- ask the user to configure `PRIVATE_KEY` in the active OpenClaw skill env or the current working directory `.env`

### `Unsupported chain ID: ...`

Cause:

- `BFUN_CHAIN_ID` is set to an unsupported value

Response:

- the default chain is BSC mainnet (56); verify the environment is configured correctly

### `Unsupported pair: ...`

Cause:

- `create --pair` used a pair outside the supported template set

Response:

- ask the user to choose one of `ETH`, `CAKE`, `USDT`, `USD1`, `ASTER`, `U`, `USDC`

## Quote and trade errors

### `Amount must be greater than 0`

Cause:

- the buy or sell amount was zero or negative

Response:

- ask for a positive amount

### `Invalid slippage bps: ...`

### `Slippage bps must be between 0 and 10000. Received: ...`

Cause:

- the `--slippage` value was invalid

Response:

- ask for an integer basis-point value, commonly `500` for 5%

### `Quoted minimum output is 0. Trade would result in no output.`

Cause:

- the trade would effectively return zero minimum output after quote and slippage handling

Response:

- stop
- suggest a smaller slippage setting review, a different amount, or checking whether the token is in a tradable phase

### `Unsupported coin_version ... This CLI only supports coin_version >= 11.1.0.`

Cause:

- token metadata indicates a market version outside the supported range

Response:

- explain that the current CLI does not support that market version
- do not attempt a manual fallback path

### `Token info not found for ...`

### `Token ... not found in API response`

### `Token mismatch: requested ..., got ...`

Cause:

- the API could not resolve the token cleanly

Response:

- verify the token address
- retry `token-get` or `token-info`
- if the token was freshly created, explain that API indexing may still be catching up

## Phase and liquidity errors

### `No BondingCurve found for token ...`

Cause:

- `token-info` could not resolve the token to a curve address

Response:

- verify the address
- confirm the token exists on the selected chain

### `TradingStopped`

Cause:

- the bonding curve is no longer accepting the requested trade path

Response:

- run `bfun token-info`
- if the token is `graduated`, stop and wait for migration
- if the token is `dex`, use the normal CLI trade path after re-quoting

### `InsufficientLiquidity`

Cause:

- the requested trade size exceeds current available liquidity

Response:

- reduce the trade size and re-quote

### `InsufficientFirstBuyFee`

Cause:

- first-buy conditions were not met for the current curve state

Response:

- reduce assumptions, re-quote, and confirm the token is still in the expected launch state

## Create validation errors

### `Image not found: ...`

Cause:

- the image path given to `create` does not exist from the current working directory

Response:

- correct the path before retrying

### `--name max 32 chars`

### `--symbol max 15 chars`

Cause:

- token metadata exceeds current validation limits

Response:

- shorten the name or symbol

### `bonding(...) + vesting(...) + migration(20) must = 100`

Cause:

- launch allocation math is invalid

Response:

- adjust `--bonding-curve-pct` and `--vesting-pct` so the total plus the fixed migration share equals `100`

### `--tax-rate must be 0, 1, 2, 3, or 5, got: "..."`

Cause:

- unsupported tax rate

Response:

- choose `0`, `1`, `2`, `3`, or `5`

### `Tax allocations must sum to 100%, got ...%`

Cause:

- `--funds-pct`, `--burn-pct`, `--dividend-pct`, and `--liquidity-pct` do not sum to `100`

Response:

- rebalance the tax allocation fields before retrying

### `--funds-recipient or --vault-type required when --funds-pct > 0`

Cause:

- tax funds were enabled without a payout destination

Response:

- provide `--funds-recipient` or a supported `--vault-type`

### `Invalid --split-recipients JSON`

### `--split-recipients required for split vault`

### `Split recipients percentages must sum to 100, got ...`

Cause:

- split vault JSON is missing or malformed

Response:

- fix the JSON and ensure recipient percentages sum to `100`

### `--gift-x-handle required for gift vault`

### `Gift X handle must be 1-15 alphanumeric/underscore characters`

Cause:

- gift vault input is incomplete or invalid

Response:

- provide a valid X handle

### `Target raise out of range. Min: ..., Max: ..., Got: ...`

Cause:

- `--target-raise` is outside the allowed range for the selected pair template

Response:

- choose a value within the allowed range or omit it to use the template default

### `--dividend-min-balance must be >= 10000 when dividend allocation > 0`

Cause:

- dividend mode was enabled with too small a threshold

Response:

- increase the minimum balance or remove dividend allocation

## Network and backend errors

### `IPFS upload failed: ...`

Cause:

- metadata upload to the backend failed

Response:

- retry later
- confirm `BFUN_API_URL` is correct and reachable

### `Salt fetch network error (fatal — singleton mode requires valid salt): ...`

### `Salt fetch HTTP ... (fatal — singleton mode requires valid salt)`

### `Salt fetch returned no salt: ...`

Cause:

- backend salt generation failed or the response was malformed

Response:

- stop
- do not guess a salt or bypass the backend requirement

### `Transaction reverted`

Cause:

- the write transaction was mined but reverted

Response:

- surface the returned transaction hash
- inspect user inputs, phase, approvals, and chain selection before retrying

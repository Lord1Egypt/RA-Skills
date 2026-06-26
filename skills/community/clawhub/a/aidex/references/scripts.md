# AIDEX Scripts Reference

Detailed reference for all AIDEX skill scripts. Load this when you need to understand exact arguments, output formats, or error handling for a specific script.

All scripts are located in `{baseDir}/scripts/` and invoked via `node`. Every script outputs a single JSON line to stdout and exits. The JSON always contains a `success` field (`true` or `false`). On failure, an `error` field provides a human-readable explanation.

## Token identification

All scripts that accept token parameters (`--token-in`, `--token-out`, `--tokens`) support two formats:

- **By address**: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- **By symbol**: `USDC`

If a symbol matches zero tokens, the error will be: `"Token not found: 'XYZ'. Use /api/v1/agent/tokens to search for available tokens."`

If a symbol matches multiple tokens (ambiguous), the error will list all matches with their addresses so you can specify the exact one.

Use `ETH` or `0x0000000000000000000000000000000000000000` for native Ether.

---

## Common API errors

These can come from any script that calls the AIDEX API. Per-script tables below list only script-specific errors.

| Error | Cause |
|-------|-------|
| `"Skill version ... is outdated..."` | Skill is outdated — run `openclaw skills update aidex` |
| `"Request rejected..."` | Server rejected the request — re-check arguments |

---

## account.js

Derives the wallet address from the configured private key. Does not call the API.

### Arguments

None.

### Private key

Required. See [Setup](../SKILL.md#setup) for configuration options.

### Output

```json
{"success": true, "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"}
```

### Errors

| Error | Cause |
|-------|-------|
| `"Private key is not configured..."` | Neither `AIDEX_PRIVATE_KEY` environment variable nor system keyring entry is set — or the OpenClaw gateway was not restarted after configuration |
| `"Invalid private key: ..."` | ethers.js rejected the key |

---

## tokens.js

Search for tokens by symbol, name, or address.

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--term <query>` | No | Search query (substring match, case-insensitive). If omitted, returns all tokens. |

### Output

```json
{
  "success": true,
  "tokens": [
    {
      "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "symbol": "USDC",
      "decimals": 6,
      "name": "USD Coin",
      "imageUrl": "https://..."
    }
  ]
}
```

An empty `tokens` array means no matches were found.

### Errors

| Error | Cause |
|-------|-------|
| `"API request failed: ..."` | Network or server error |

---

## rate.js

Get the current exchange rate for a token pair. Read-only, does not execute anything.

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--token-in <token>` | Yes | Token to sell (address or symbol) |
| `--token-out <token>` | Yes | Token to buy (address or symbol) |
| `--amount-in <number>` | Yes | Amount to sell, human-readable (e.g., `0.5`) |

### Output (success)

```json
{
  "success": true,
  "rate": "3125.50",
  "amountOut": "1562.75",
  "estimatedGasPriceUsd": 2.34
}
```

### Errors

| Error | Cause |
|-------|-------|
| `"Missing required argument: --token-in."` | Missing argument |
| `"Token not found."` | Unknown token symbol |
| `"Route not found."` | No exchange route for this pair/amount |
| `"AIDEX is temporarily unavailable. Please try again later."` | Internal service down — retry later |

---

## balance.js

Get token balances and allowances for a wallet address. Maximum 9 tokens per request. The `allowance` field shows how much the AIDEX router is approved to spend on behalf of the wallet (relevant for ERC-20 tokens). For native ETH, `allowance` is `null`.

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--address <wallet>` | Yes | Wallet address (0x...) |
| `--tokens <list>` | Yes | Comma-separated tokens (address or symbol). Use `ETH` for native Ether. Max 9. |

### Output (success)

```json
{
  "success": true,
  "balances": [
    {"address": "0x0000000000000000000000000000000000000000", "symbol": "ETH", "balance": "1.5", "allowance": null},
    {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "symbol": "USDC", "balance": "3250.00", "allowance": "1000.0"}
  ]
}
```

### Errors

| Error | Cause |
|-------|-------|
| `"Missing required argument: --address."` | Missing argument |
| `"Missing required argument: --tokens."` | Missing argument |
| `"Too many tokens. Maximum is 9 per request."` | Exceeded limit |
| `"Token not found."` | Unknown token symbol |

---

## swap.js

Executes a full swap cycle. The API builds a chain of transactions (approve + swap if needed), the script signs them locally and sends them. Approve is handled automatically — the script doesn't need to know about it.

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--token-in <token>` | Yes | — | Token to sell (address or symbol) |
| `--token-out <token>` | Yes | — | Token to buy (address or symbol) |
| `--amount-in <number>` | Yes | — | Amount to sell, human-readable |
| `--slippage <percent>` | No | `0.5` | Maximum acceptable slippage (e.g., `0.5` = 0.5%) |
| `--deadline-minutes <min>` | No | `20` | Transaction deadline in minutes from now |

### Private key

Required. See [Setup](../SKILL.md#setup) for configuration options.

### Output (success)

```json
{
  "success": true,
  "transactionHashes": ["0xApproveHash...", "0xSwapHash..."],
  "fromAddress": "0x742d35Cc...",
  "amountOut": "1562.75",
  "estimatedGasPriceUsd": 2.34
}
```

`transactionHashes` is an array (1-3 hashes). Pass all of them to swap-status.js to check the result.

### Errors

| Error | Cause |
|-------|-------|
| `"Missing required argument: --token-in."` | Missing argument |
| `"Private key is not configured..."` | Neither `AIDEX_PRIVATE_KEY` environment variable nor system keyring entry is set — or the OpenClaw gateway was not restarted after configuration |
| `"Invalid private key: ..."` | ethers.js rejected the key |
| `"Route not found."` | No exchange route — suggest different pair or amount |
| `"AIDEX is temporarily unavailable. Please try again later."` | Internal service down — retry later |
| `"Insufficient balance"` | Not enough tokens to execute the swap |
| `"Failed to sign transaction: ..."` | ethers.js signing error |

### Important behavior

- If the API returns a non-success result, the script does **not** attempt to sign or send anything. It returns the error and exits.
- The private key is used only for `ethers.Wallet.signTransaction()` and never leaves the process.
- If the node rejects a transaction, the script stops and exits with `success: false`. `failedAtStep` is the zero-based index (into the transaction chain returned by createSwap) of the transaction the node rejected — use it to report to the user which step could not be sent. `transactionHashes` contains the hashes of transactions that were accepted by the node before the failure.

---

## swap-status.js

Check the status of a swap operation (including approve steps). Accepts 1-3 transaction hashes.

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--hashes <list>` | Yes | Comma-separated transaction hashes (1-3). Pass the hashes returned by swap.js. |

### Output

**Completed (all steps confirmed):**

```json
{
  "success": true,
  "status": "completed",
  "steps": [
    {"type": "approve", "status": "confirmed", "transactionHash": "0x..."},
    {"type": "swap", "status": "confirmed", "transactionHash": "0x...", "amountIn": "0.5", "tokenIn": "ETH", "amountOut": "1562.75", "tokenOut": "USDC"}
  ]
}
```

**Pending (waiting for confirmation):**

```json
{
  "success": true,
  "status": "pending",
  "steps": [
    {"type": "approve", "status": "confirmed", "transactionHash": "0x..."},
    {"type": "swap", "status": "pending", "transactionHash": "0x..."}
  ]
}
```

**Failed (a step reverted):**

```json
{
  "success": true,
  "status": "failed",
  "steps": [
    {"type": "approve", "status": "confirmed", "transactionHash": "0x..."},
    {"type": "swap", "status": "reverted", "transactionHash": "0x..."}
  ]
}
```

High-level status: `pending` (waiting), `completed` (all confirmed), `failed` (a step reverted).

Step-level status: `pending`, `confirmed`, `reverted`.

`amountIn`, `tokenIn`, `amountOut`, `tokenOut` are only present for the swap step, not for approve steps.

### Errors

| Error | Cause |
|-------|-------|
| `"Missing required argument: --hashes."` | Missing argument |
| `"Expected 1 to 3 transaction hashes, comma-separated."` | Wrong number of hashes |
| `"Invalid hash: ..."` | Malformed transaction hash |
| `"API request failed: ..."` | Network or server error |

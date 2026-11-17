# Launch a token

The Deside Launchpad launches a Solana token for an agent, optionally with the agent's on-chain identity, in one transaction you sign with your own wallet. It builds Meteora Dynamic Bonding Curve transactions; Deside never holds your key or funds.

## What one launch creates

1. A token: 1,000,000,000 supply, 6 decimals, immutable metadata, no mint authority.
2. A Meteora Dynamic Bonding Curve pool.
3. Optionally, the agent's identity: a Metaplex Core asset in the Metaplex Agent Registry, with an EIP-8004 registration.
4. The image and metadata, stored on Arweave and paid in the same signature.

**The token is created by its signer, not by Deside.**

## Fees and costs

Deside charges no launch fee. A launch costs about 0.021 SOL, or about 0.026 SOL with an agent identity, Arweave included. Keep about 0.03 SOL in the wallet.

Each trade on the curve pays 1%: 0.40% to the creator, 0.40% to Deside, 0.20% to Meteora.

### Anti-sniper fee

For the first 120 seconds after launch the trading fee starts at 25% and falls to 1% in 12 equal steps. Set `slippageBps` on `swap` with that in mind.

### Graduation

When the curve raises its threshold in SOL, it migrates to a Meteora DAMM v2 pool.

| Network | Threshold |
|---|---|
| `mainnet` | 50,000 USD market cap: about 93.5 SOL, fixed when the config was created. |
| `devnet` | 400 USD market cap: about 0.64 SOL, for testing. |

On mainnet Meteora migrates automatically, normally within seconds. If not, anyone can run `migrate`.

### After graduation

| Item | Rule |
|---|---|
| Pool fee | Starts at 5%, falls to 0.5% as the price grows 10x or after 24 hours, plus a volatility fee. |
| Liquidity | 100% locked: 90% creator position, 10% Deside position. Both keep earning pool fees. |
| Creator claim | Call `claim_fees`. |

## Launch with the MCP

Sign in first. Then:

```bash
curl -X POST https://mcp.deside.io/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"launch_token","arguments":{"network":"devnet","acceptTerms":true,"token":{"name":"My Agent","symbol":"AGT","description":"What it does","image":"https://example.com/logo.png"}}}}'
```

### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `network` | string | Yes | `mainnet` or `devnet`. |
| `acceptTerms` | `true` | Yes | Read https://launchpad.deside.io/terms first. |
| `token.name` | string | Yes | 1 to 32 characters. |
| `token.symbol` | string | Yes | 1 to 10 characters. |
| `token.description` | string | No | Up to 500. |
| `token.image` | URL | One of the two | https URL of a square logo, up to 300 characters. |
| `token.imageBase64` | string | One of the two | PNG, JPG, WebP or GIF, up to 950,000 base64 characters (about 700 KB) through the MCP; up to 1 MB over REST. |
| `token.website`, `token.x`, `token.telegram` | URL | No | Up to 200 each. |
| `registerAgentIdentity` | boolean | No | `true` to create the identity in the same signature. |
| `agent` | object | No | Only with `registerAgentIdentity`. `name` (up to 64), `description` (up to 1,000), `image` (URL, up to 300), `active`, `x402Support`, `supportedTrust` (`reputation`, `crypto-economic`, `tee-attestation`), and up to 40 `services`, each with `name` (up to 64), `endpoint` (up to 512) and optional `version`. |

**A logo is required:** send `token.image` or `token.imageBase64`. Without one the call fails with `400` `token.image (https URL) or token.imageBase64 is required`.

### Response

```json
{
  "network": "devnet",
  "mint": "...",
  "pool": "...",
  "agentAsset": null,
  "creator": "...",
  "files": { "image": "https://...", "tokenMetadata": "https://..." },
  "cost": { "arweaveSol": 0.000047, "estimatedTotalSol": 0.025547 },
  "transaction": "<base64>",
  "signUrl": "...",
  "signUrlExpiresAt": "...",
  "bytes": 1227,
  "simulation": { "ok": true, "computeUnits": 104244 },
  "expiresInSeconds": 60,
  "next": "Sign `transaction` with the wallet above (it is already signed by the new mint) ...",
  "disclaimer": "..."
}
```

`files` holds the Arweave URLs of `image` and `tokenMetadata`, plus `agentRegistration` and `agentMetadata` with an identity. `bytes` is the size of the transaction. `next` says what to do now.

**If `simulation.ok` is false, do not sign.** Read `simulation.error`, `simulation.hint` and `simulation.logs`. `signUrl` and `signUrlExpiresAt` are present only when `simulation.ok` is true.

## Sign and submit

### With a browser

Give `signUrl` to a person to sign with a browser wallet. The link lasts 2 minutes and works once; the page sends the signature for you.

### With code

Sign and submit within about 60 seconds, the life of the blockhash. If it expires, prepare again.

The transaction is a legacy `Transaction`, not a versioned one. A launch arrives already signed by the new mint, and by the agent asset with an identity, so add your signature with `partialSign`: `sign` would drop the others. Verify the wallet pays before signing. This uses the wallet file from wallet-and-signin.md:

```js
const fs = require('fs');
const { Keypair, Transaction } = require('@solana/web3.js');

const secretKeyArray = JSON.parse(fs.readFileSync(process.env.HOME + '/.config/deside/agent.json', 'utf8'));
const wallet = Keypair.fromSecretKey(new Uint8Array(secretKeyArray));

// prepared = structuredContent of launch_token
const tx = Transaction.from(Buffer.from(prepared.transaction, 'base64'));
if (!tx.feePayer?.equals(wallet.publicKey)) throw new Error('not paid by your wallet: do not sign');
tx.partialSign(wallet);
const signed = tx.serialize().toString('base64');
```

Send `signed` with `submit_transaction` on the same MCP session:

```bash
curl -X POST https://mcp.deside.io/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"submit_transaction","arguments":{"network":"devnet","transaction":"SIGNED_BASE64"}}}'
```

Or, without the MCP, over REST:

```js
const res = await fetch('https://launchpad.deside.io/v1/submit', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ network: prepared.network, transaction: signed })
});
console.log(await res.json());
```

Both return `signature`, `links` and, for a launch, `mint`, `pool`, `agentAsset` and `uploads`. A failed simulation answers `422` with `hint` and `logs`; a failed Arweave upload answers `503`. In both cases nothing is sent.

If you sent the launch yourself, call `submit_transaction` or `POST https://launchpad.deside.io/v1/submit` with `{ "network", "signature" }` within 15 minutes of `launch_token`.

## Launch with REST

```bash
curl -X POST https://launchpad.deside.io/v1/launch \
  -H "content-type: application/json" \
  -d '{
    "network":"devnet",
    "wallet":"YOUR_WALLET_ADDRESS",
    "acceptTerms":true,
    "token":{"name":"My Agent","symbol":"AGT","image":"https://example.com/logo.png"}
  }'
```

## Trade

Prepare a buy or sell with `swap`. Takes `mint`, `side` (`buy` spends SOL, `sell` spends tokens), `amount` (a number: SOL to spend, or tokens to sell in whole units), optional `slippageBps` (0 to 5000, default 300). Returns `venue` (`meteora-dbc-curve` or `meteora-damm-v2`), `quote` (`expectedOut`, `minimumOut`, `unit`) and the transaction.

**Ask your user before a mainnet buy or sell.**

```bash
curl -X POST https://launchpad.deside.io/v1/swap \
  -H "content-type: application/json" \
  -d '{"network":"devnet","wallet":"YOUR_WALLET","mint":"...","side":"buy","amount":0.001}'
```

Sign and send the transaction like a launch.

## Claim creator fees

Prepare the claim with `claim_fees`. Takes `mint`. Returns `claims[]`, each with `source`: `curve` (with `sol`), `surplus` or `damm-v2-locked-position` (with `position`), and the transaction. With nothing to collect it answers `409` `nothing to claim yet`.

```bash
curl -X POST https://launchpad.deside.io/v1/claim \
  -H "content-type: application/json" \
  -d '{"network":"devnet","wallet":"YOUR_WALLET","mint":"..."}'
```

**Fees are never paid out by themselves: call `claim_fees`.** The creator earns 0.40% of every trade on the curve, and the fees of 90% of the locked pool after graduation.

## Check progress

Read a token's state with `get_token`. Takes `network` and `mint`. Returns `network`, `mint`, `name`, `symbol`, `uri`, `creator`, `pool`, `dbcConfig` (the curve config), `launchedHere` (true when `dbcConfig` is the Deside one), `graduated`, `curve` (raisedSol, thresholdSol, progress), `dammV2Pool` (after graduation), `unclaimedCurveFeesSol` (`creator` and `partner`), `links`.

```bash
curl "https://launchpad.deside.io/v1/tokens/Ec9FVEahXUhQRkPneCmDYzXc3jFZWX4URcLfyPwHaRE1?network=mainnet"
```

## Statistics

Read-only, no key, over REST only. Always pass `network`. Full reference: https://docs.deside.io/launchpad/docs/stats

| Route | Returns |
|---|---|
| `GET /v1/stats?network=mainnet` | `totals` and `byVersion` (tokens launched, graduated and in curve, `volumeSol`, `curveFeesSol`, `poolFeesSol`, `lockedLiquidity`), `recentLaunches` (up to 20) and `tokens[]` (one row per token). Cached 60 seconds. |
| `GET /v1/tokens/{mint}?network=mainnet` | For a token launched here, a `launchpad` block: the token row plus `holders`, `programOwnedAccounts` and `holdersRule`. |
| `GET /v1/stats/history?network=mainnet` | Points with `launches`, `graduations`, `volumeSol`, `feesSol` and `cumulative`. Optional `version`. |
| `GET /v1/tokens/{mint}/history?network=mainnet` | Points with `volumeSol`, `feesSol`, `curveProgress`, `priceSol`, `marketCapSol`, `marketCapUsd` and `cumulative`. |

History takes `interval` (`hour` or `day`, default `day`), `from` and `to` (ISO), at most 2000 points per call. Points are never filled in: if a pool is not read yet, `complete` is `false` and `pendingPools` lists it.

Read the figures with these rules:

* **Versions.** Each version is one Meteora DBC config and never changes; `v1` is the only one today. Each token has its `version` and `dbcConfig`.
* **Fees** are `{ generated, claimed, unclaimed }` per recipient, in SOL. Pool fees are counted only in SOL.
* **`lockedLiquidity`** is the 2 positions locked at graduation (creator 90%, Deside 10%). Other liquidity is in `thirdPartyLiquidity`.
* **`holders`** counts wallets with a balance; program-owned accounts are left out and counted in `programOwnedAccounts`. A bot's wallet counts.
* **Curve volume** is `null` for a version with a dynamic fee until every swap is read. v1 has none.
* **`graduatedAt`** is the time of the migration transaction.
* **History pool fees** are split only into `lp`, `meteora` and `referral`. The split by position is only in `/v1/stats` (see `feeNote`).
* **`marketCapUsd` in history** has values only from 2026-10-05; earlier points are `null`.
* **`solUsd`** comes from Jupiter Price v3.

**The statistics routes allow 10 requests a minute per IP.** Over it they answer `429`.

## Limits

| Limit | Value |
|---|---|
| Requests | 60 per minute, per wallet on the MCP and per IP over REST. |
| Launches | 2 per minute. |
| Whole Launchpad | 600 requests and 30 launches a minute. |
| Request body | 2 MB. |
| Logo file | 1 MB (700 KB through the MCP). |
| Token name, symbol, description | 32, 10 and 500 characters. |
| Transaction size | 1232 bytes. |
| Time to sign and submit | About 60 seconds. |
| Sign link | 2 minutes, once. |

## Creator terms

**`launch_token` requires `acceptTerms: true`.** By sending it you accept the creator terms. Read the full text at https://launchpad.deside.io/terms.

In short:

* You are the only one responsible for your token and for everything you or your agent say or do about it.
* A token launched here raises no capital and gives its holders no rights: no ownership, profit share, dividend or vote.
* You must not promise or suggest returns, misrepresent the fees, or manipulate the market of any token.

## Disclaimer

Deside does not custody funds or keys. This service only builds Meteora Dynamic Bonding Curve transactions that you sign with your own wallet. Tokens are created by their signer, not by Deside. Deside is the fee partner of the launch configuration and receives the partner share of trading fees. Nothing here is investment advice; launching or trading a token can lose all the money involved.

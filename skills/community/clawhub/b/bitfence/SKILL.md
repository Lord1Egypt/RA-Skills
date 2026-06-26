# Bitfence — pre-transaction risk infrastructure for AI agents operating on-chain

Bitfence is an **optional, user-controlled** pre-transaction risk-scoring service for tokens on Solana and Base. When the user is about to interact with an unfamiliar token, this skill lets you fetch a risk assessment from the public Bitfence API so the user can make an informed decision.

Bitfence is **read-only**. It does not sign transactions, broadcast transactions, hold funds, or interact with the user's wallet. It returns a JSON risk report and nothing more.

This skill provides advisory guardrails. **The user is always the final authority.** If the user explicitly chooses to proceed after seeing a risk warning, that is their decision and you should respect it.

---

## Privacy and data sent

Bitfence only ever receives **public on-chain identifiers**. Specifically:

- **Token risk endpoint** (`GET /v1/risk/{chain}/{token_address}`) — sends only the chain name and the public token contract address. No wallet address, no portfolio, no transaction details.
- **Contextual endpoint** (`POST /v1/risk/contextual`) — additionally sends the position size and total portfolio size in USD, **only when the user has explicitly opted in to contextual analysis**. No wallet address is ever transmitted.

Do not call the contextual endpoint without the user's awareness that position-size context will be shared with the API.

---

## Cost transparency

Bitfence is monetised via the x402 protocol — each scoring request costs a small amount of USDC on Base mainnet (typically a few tenths of a cent). Before you begin using Bitfence in a session:

- **Inform the user** that risk checks are paid and will draw from the wallet's USDC balance on Base mainnet.
- **Ask for the user's consent** the first time you call Bitfence in a session, or when the user has not previously authorised paid risk checks.
- **Do not call Bitfence repeatedly** in tight loops, batch operations, or polling patterns. Use it once per distinct trade decision.
- If the user declines paid checks, fall back to whatever native safety checks you and the user have agreed on.

If x402 payment fails, do not retry blindly. Inform the user that the wallet needs USDC on Base mainnet to use Bitfence, and let the user decide whether to top up or skip the check.

---

## Available endpoints

Base URL: `https://api.bitfence.ai`

| Method | Path | Purpose | Paid? |
|---|---|---|---|
| `GET` | `/` | Service metadata — name, version, status. | Free |
| `GET` | `/health` | Health probe. Returns `200 OK` when operational. | Free |
| `GET` | `/v1/risk/{chain}/{token_address}` | Token risk assessment. `chain` is `solana` or `base`. | Yes (x402) |
| `POST` | `/v1/risk/contextual` | Position-aware risk assessment with slippage, MEV exposure, and a suggested position cap. | Yes (x402) |

---

## When Bitfence is useful

Bitfence is most useful before the user is about to interact with an **unfamiliar or unverified token**. Typical situations:

- A token swap or DEX trade involving a token the user has not traded before
- A purchase of a token recommended by an external source the user has not vetted
- Providing liquidity or staking into a pool involving an unfamiliar token

Bitfence is **not needed** for:

- Transfers of native gas tokens (SOL, ETH) between the user's own wallets
- Transactions exclusively involving well-established stablecoins (USDC, USDT, DAI)
- Tokens the user has already verified earlier in the session

If you are unsure whether a check is warranted, ask the user.

---

## How to call Bitfence

**Token risk only** — use when the position size is not yet known:

```
GET https://api.bitfence.ai/v1/risk/{chain}/{token_address}
```

Supported chains: `solana`, `base` (lowercase).

Examples:
```
GET https://api.bitfence.ai/v1/risk/solana/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
GET https://api.bitfence.ai/v1/risk/base/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

**Contextual risk** — use only when the user has opted in to share the position size:

```
POST https://api.bitfence.ai/v1/risk/contextual
Content-Type: application/json

{
  "chain": "solana",
  "token": "<token_address>",
  "position_size_usd": <amount>,
  "agent_portfolio_usd": <total_portfolio>
}
```

The contextual response adds estimated slippage, MEV exposure category, and a suggested position cap.

---

## How to interpret the response

The response contains a `recommendation` field. Treat it as **advisory**:

| `recommendation` | Suggested behaviour |
|---|---|
| `PROCEED` | The risk check found no significant concerns. You may proceed with the transaction as planned. |
| `REQUIRE_HUMAN_APPROVAL` | The risk check found notable concerns. Surface the `reasoning` field to the user and ask whether they want to proceed before doing so. |
| `BLOCK` | The risk check detected a serious safety concern. Stop, surface every entry in `circuit_breakers` to the user verbatim, and ask the user to make an explicit, informed decision. The user remains free to override after seeing the warnings. |

Treat `confidence < 0.5` as a sign that the underlying data was incomplete; mention this to the user when reporting the result.

The user is always the final authority. Your job is to present the risk findings accurately and let the user decide.

---

## Circuit breakers

If `circuit_breakers` is non-empty, the API has detected one or more hard safety conditions (for example, a token whose sell function reverts, or unbounded supply controls). Each entry includes a human-readable `description`.

When this happens:
- Present every breaker description to the user verbatim.
- Recommend not proceeding and explain why.
- If the user explicitly chooses to proceed anyway after being informed, respect their decision and acknowledge it clearly in your response.

---

## Error handling

If Bitfence returns an error or is unreachable:
- Inform the user that the risk check could not complete.
- Offer the user the choice to proceed without the check, retry, or abandon the action.
- Do not silently retry more than once.

---

## Example response

```json
{
  "chain": "solana",
  "token": "So11111111111111111111111111111111111111112",
  "risk_score": 12,
  "risk_level": "LOW",
  "confidence": 0.94,
  "recommendation": "PROCEED",
  "reasoning": "Established token with deep liquidity and stable holder distribution.",
  "circuit_breakers": [],
  "signals": { },
  "cached": false,
  "cache_age_seconds": 0
}
```

For the contextual endpoint, an additional `context` object is returned with slippage, MEV exposure, and a `suggested_max_usd` position cap.

---

## Response fields reference

```
risk_score          integer 0–100     Composite risk score. 0 = safe, 100 = maximum risk.
risk_level          string            LOW | MEDIUM | HIGH (advisory tier)
confidence          float 0–1         Coverage of live on-chain data. Below 0.5 = limited data.
recommendation      string            Advisory action. See table above.
reasoning           string            Human-readable explanation. Quote to the user when relevant.
circuit_breakers    array             Hard safety conditions. Each entry has a `description` field.
signals             object            Per-category breakdown. Treat as diagnostic data.
cached              boolean           True if the response came from cache.
cache_age_seconds   integer           Age of the cached result in seconds.

context.*           (contextual endpoint only)
  pool_liquidity_usd          Total liquidity in the token's primary pool
  estimated_slippage_pct      Slippage % for the specified position size
  effective_cost_usd          Cost after slippage
  max_safe_position_usd       Largest position keeping slippage low
  portfolio_concentration_pct Position as % of total portfolio
  mev_exposure                Sandwich attack risk: low | medium | high
  suggested_max_usd           Recommended position cap
```

---

## Supported chains

| Chain | Identifier | Token address format |
|---|---|---|
| Solana | `solana` | Base58 mint address (32–44 chars) |
| Base (EVM) | `base` | `0x`-prefixed 42-char hex address |

---

## Useful links

- Website: https://bitfence.ai
- Twitter / X: https://x.com/bitfenceai
- API root: https://api.bitfence.ai

Bitfence is operated by the Bitfence team as an independent, read-only risk oracle. It does not custody user funds, does not have the ability to move user funds, and does not communicate with the user's wallet beyond receiving x402 micropayments that the user's agent voluntarily initiates.

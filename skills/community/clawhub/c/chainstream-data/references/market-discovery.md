# Market Discovery Reference

## CLI Commands → REST API Mapping

| CLI Command | REST Endpoint | Method |
|-------------|--------------|--------|
| `market trending --chain sol --duration 1h` | `GET /v2/ranking/sol/hotTokens/1h` | GET |
| `market new --chain sol` | `GET /v2/ranking/sol/newTokens` | GET |
| `market trades --chain sol` | `GET /v2/trade/sol` | GET |

## All Market Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v2/ranking/{chain}/hotTokens/{duration}` | Hot tokens. Duration: `1h`, `6h`, `24h` |
| GET | `/v2/ranking/{chain}/newTokens` | Newly created tokens |
| GET | `/v2/ranking/{chain}/finalStretch` | About to graduate (bonding curve near completion) |
| GET | `/v2/ranking/{chain}/migrated` | Migrated from launchpad to DEX |
| GET | `/v2/ranking/{chain}/stocks` | Stock-type tokens (real-world asset backed) |
| GET | `/v2/trade/{chain}` | Recent trades. Params: `tokenAddress`, `limit` |
| GET | `/v2/trade/{chain}/top-traders` | Top traders by PnL or volume |
| GET | `/v2/trade/{chain}/activities` | Trade activities with enriched data |
| GET | `/v2/blockchain` | List supported blockchains |
| GET | `/v2/dex` | List DEX protocols |
| GET | `/v2/dexpools/{chain}/{poolAddress}` | Pool details (TVL, fees, reserves) |

## Multi-Factor Discovery Workflow

When a user wants to find trading opportunities, follow this workflow:

### Step 1: Fetch trending data

```bash
npx @chainstream-io/cli market trending --chain sol --duration 1h --json
```

### Step 2: AI multi-factor analysis

Analyze each token using these signals (apply judgment, not rigid rules):

| Signal | Weight | Source | Notes |
|--------|--------|--------|-------|
| Smart money interest | High | `smart_degen_count`, `renowned_count` fields | Key conviction indicator |
| Volume | Medium | `volume` field | Genuine interest vs wash trading |
| Price momentum | Medium | `change1h`, `change5m` fields | Prefer positive, non-parabolic |
| Liquidity | Medium | `liquidity` field | Low liquidity = high slippage risk |
| Holder quality | Medium | `bluechip_owner_percentage` field | Quality of holder base |
| Token maturity | Low | `creation_timestamp` field | Avoid < 1h old unless other signals strong |

Select **top 5** tokens with the best composite profile across multiple signals.

### Step 3: Security verification

For each candidate:

```bash
npx @chainstream-io/cli token security --chain sol --address <addr>
```

Reject tokens with `isHoneypot=true`, `hasMintAuthority=true` with no renouncement.

### Step 4: Present results

```
Top 5 Trending — SOL / 1h

# | Symbol | Address     | Smart Money | Volume  | 1h Change | Verdict
1 | ...    | ...         | ...         | ...     | ...       | Safe / Caution / Avoid
```

### Step 5: Follow-up

- Deep dive: `chainstream token info` + `token holders`
- Execute: load `chainstream-defi` skill for swap

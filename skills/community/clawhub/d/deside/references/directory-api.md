# Directory API

Read the Agent Directory and x402 tool catalog with no session or key. The agent routes (v2) answer in `{ "data": ... }` and their errors in `{ "error": { "code", "message" } }`. The x402 routes (v1) answer with their body as is (`items`, `pagination`) and their errors as `{ "error": "..." }`.

## List agents

```bash
curl "https://api.deside.io/api/v2/public/agents?limit=10&live=mcp"
```

### Parameters

| Name | Default | Description |
|---|---|---|
| `limit` | 20 | 1 to 100. Out-of-range values are clamped. 24 at most with `sort=featured`. |
| `skip` | 0 | Rows to skip. 500 at most; 96 with `sort=featured`. Above that: 400 error. |
| `q` | | 2 to 50 characters. Matches the start of the name, the start of the owner wallet, or a full agent wallet, registry entry id or EVM address. Outside 2 to 50 it is ignored. |
| `name` | | Same as `q`. |
| `skill` | | Up to 60 characters. Exact match on a declared skill, lowercase. |
| `category` | | One of the 12 categories. Unknown values ignored. |
| `service` | | `web`, `mcp`, `a2a`, `x402`, `api` or `contact`. |
| `live` | | Comma list of `mcp`, `a2a`, `x402`. Agents with at least one live. |
| `registry` | | `8004solana`, `erc8004-base`, `mip14`, `said`, `sati`, `sap`, `kamiyo`. |
| `chain` | | `solana` or `evm`. |
| `ownerWallet` | | Exact owner wallet, base58. |
| `agentWallet` | | Exact agent wallet, base58. |
| `coreAsset` | | Exact Metaplex Core asset, base58. |
| `collection` | | Agents carrying a badge of this collection, base58. |
| `collectionCase` | | `A`, `B`, `C` or `D`. |
| `connected` | | `true`: owner proved the agent is theirs. `false`: not proved. |
| `duplicates` | | `hide` keeps one agent per group; `show` lists every copy. |
| `sort` | | `name` for A to Z. `featured` for curated. Default order otherwise. |

Categories: `trading_bots`, `token_signals`, `token_risk`, `contract_security`, `defi_yield`, `prediction_markets`, `market_data`, `dev_tools`, `research`, `content_marketing`, `agent_infra`, `token_launch`. `other` (fits none) and `null` (no category yet) can appear in responses but are not filters.

### Response

```json
{
  "data": [
    {
      "id": "bbddcb0c-074f-4874-9c48-3733013db7f7",
      "slug": "blinkcodes",
      "name": "BlinkCodes",
      "avatar": { "url": "...", "thumbUrl": "..." },
      "chain": "evm",
      "category": "other",
      "ownerProven": false,
      "team": false,
      "status": "responds",
      "liveKinds": ["mcp", "a2a", "x402"]
    }
  ],
  "page": { "total": 109734, "limit": 1, "skip": 0, "hasMore": true },
  "facets": { "live": { "mcp": 766, "a2a": 33, "x402": 31 } }
}
```

| Field | Description |
|---|---|
| `id` | Stable id of the agent. |
| `slug` | Short name for URLs. |
| `name` | Display name. |
| `avatar` | `url` and `thumbUrl`, or null. |
| `chain` | `solana` or `evm`. |
| `category` | One of the 12 above, `other`, or `null`. |
| `ownerProven` | `true` when the owner proved the agent is theirs (Connected). |
| `team` | `true` when the account that owns the agent is a team on Deside. `null` when it could not be read. |
| `status` | The state from Deside's checks. |
| `liveKinds` | Protocols that answered our last check: `mcp`, `a2a`, `x402`. |
| `page.total` | Agents that match the filters. |
| `facets.live` | How many agents would match with each `live` value added. |

### Errors

| Status | Code | When |
|---|---|---|
| 400 | `invalid_request` | A bad parameter or `skip` above 500 (96 with featured). |
| 429 | | More than 30 list requests a minute, or 500 a day, from your IP. Body: `{"error":"RATE_LIMITED"}`. |

## Read one agent

```bash
curl "https://api.deside.io/api/v2/public/agents/blinkcodes"
```

Takes `{ref}` (the `id` or the `slug`). An old slug answers `301`. A slug shared by more than one agent answers `409` with `candidates[]`.

Returns the list fields plus `status` (`state`, `since`, `probedAt`), `description`, `wallets`, `registries`, `sources`, `endpoints[]` (what answered our check, with `checkedAt`), `services[]` (everything declared, with `live` and `checkedAt`), `links`, `skills`, `updatedAt`. Errors: `400 invalid_ref`, `404 not_found`, `409 ambiguous_ref`; over 60 a minute or 500 a day from your IP, `429`.

## Agent counts

```bash
curl "https://api.deside.io/api/v2/public/agents/stats"
```

No parameters. Returns:

| Field | Description |
|---|---|
| `listed` | Agents in the directory. |
| `byChain` | Listed by chain. |
| `byCategory`, `byCategoryByChain` | Agents with a category. |
| `respondingAgents` | Agents with at least one protocol that answered. |
| `respondingByKind` | The same, by protocol. |
| `connected` | Agents whose owner proved they are theirs. |
| `endpoints` | By protocol: declared, checked, alive. |
| `measuredAt` | When the counts were measured. |

## List x402 tools

```bash
curl "https://api.deside.io/api/v1/public/x402/tools?live=1&limit=25"
```

### Parameters

| Name | Default | Description |
|---|---|---|
| `live` | | Only `1`: tools whose last check got an answer (`offer` or `no-offer`). |
| `limit` | 25 | 1 to 100. Outside that: `400`. |
| `q` | | Text search, up to 512 characters. Returns one page; cannot be combined with `cursor`. |
| `host` | | Exact host. |
| `bazaar` | | Exact catalog: `payai`, `cdp`, `dexter`, `thirdweb` or `openfac`. |
| `payTo` | | Exact receiving wallet. |
| `network` | | Exact network, such as `eip155:8453` or `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`. |
| `agent` | | An agent's `id` or slug: its tools. |
| `index` | | An index URL, up to 2,048 characters: the tools it lists. Not with `agent`. |
| `cursor` | | `pagination.nextCursor`, with the same filters. |

Any other parameter returns `400 unknown filter`. Without `q`, a page cannot go past row 500.

### Response

```json
{
  "items": [
    {
      "slug": "abi-cyberwarex-abi",
      "title": "Contract ABI",
      "host": "abi.cyberwarex.com",
      "path": "/abi",
      "bazaars": ["cdp"],
      "prices": [
        { "network": "eip155:8453", "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "amount": "3000", "payTo": "0x058D0Cc5CC97e61e8A9f38D6d6365bce525921B2" }
      ],
      "probe": {
        "verdict": "offer",
        "at": "2026-10-01T07:20:00.467Z",
        "httpStatus": 402,
        "comparison": { "sameAmount": true, "sameWallet": true }
      },
      "tier": 1
    }
  ],
  "pagination": { "nextCursor": "...", "hasMore": true, "limit": 25, "total": 93 }
}
```

| Field | Description |
|---|---|
| `slug` | Short name. |
| `title` | Display name. |
| `host`, `path` | The URL. |
| `bazaars` | Marketplaces that list it. |
| `prices` | What catalogs publish, each with `bazaar`, `scheme`, `network`, `asset`, `amount`, `payTo`, `maxTimeoutSeconds`. `amount` is in the asset's base units: 3000 of USDC with 6 decimals is 0.003 USDC. |
| `probe` | Deside's last check. `verdict`: `offer` (answered with a price), `no-offer` (no payment), `no-response`, `blocked`, `no-endpoint`. `comparison`: whether the price and wallet match the catalog. `probe: null` means never checked. |
| `tier` | Our last check as a number: 1 quoted a price, 2 answered without charging, 3 not checked yet, 4 and 5 failed. |

**Deside does not call the tool for you and does not pay it.** To use a tool, call its `host` and `path` yourself with an x402 client, and check the price it asks before you pay.

### Errors

| Status | Code | When |
|---|---|---|
| 400 | `invalid_request` | A bad or unknown parameter. |
| 429 | | Rate limited. |

## Rate limits

| Routes | Limit | Counted by |
|---|---|---|
| All of `/api` | 500 requests per 15 minutes | IP |
| Lists: agents, x402, indices | 30 a minute | IP |
| Public single reads and counts | 60 a minute | IP |
| Each public family | 500 a day | IP |

Over the 15-minute limit, the `429` body is plain text. Other `429` responses carry `Retry-After` in seconds.

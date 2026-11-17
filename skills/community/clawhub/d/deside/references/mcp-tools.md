# MCP tools reference

The Deside MCP has 24 tools. Read tools need `deside:read`; tools that prepare, send or change something need `deside:write`.

**A tool that changes something returns an unsigned transaction. Nothing happens until you sign it.**

On success, fields arrive in `structuredContent`. On failure, `isError: true`; see Errors below.

| Tool | Scope | Changes anything |
|---|---|---|
| `search_agents` | read | No |
| `agent_trust_card` | read | No |
| `ask_directory` | read | No |
| `get_directory_stats` | read | No |
| `token_card` | read | No |
| `search_x402_tools` | read | No |
| `x402_tool_card` | read | No |
| `get_user_info` | read | No |
| `get_my_identity` | read | No |
| `list_my_agent_identities` | read | No |
| `select_agent_identity` | read | Only which agent this session acts as |
| `prepare_agent_identity_link` | write | No |
| `create_agent_identity_link` | write | Yes |
| `revoke_agent_identity_link` | write | Yes |
| `get_launchpad_info` | read | No |
| `launch_token` | write | Yes, you sign it |
| `register_agent_identity` | write | Yes, you sign it |
| `update_agent_identity` | write | Yes, you sign it |
| `submit_transaction` | write | Yes, sends a signed transaction |
| `get_token` | read | No |
| `list_launches` | read | No |
| `swap` | write | Yes, you sign it |
| `claim_fees` | write | Yes, you sign it |
| `migrate` | write | Yes, you sign it |

## Directory

### search_agents

Finds agents in the Agent Directory. Returns `{agents, total, hasMore}`.

| Name | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Part of the public name. |
| `wallet` | string | No | One wallet, base58. Not together with `name`. |
| `registry` | string | No | `8004solana`, `erc8004-base`, `mip14`, `said`, `sati`, `sap`, `kamiyo`. |
| `chain` | string | No | `solana` or `evm`. |
| `service` | string | No | `web`, `mcp`, `a2a`, `x402`, `api` or `contact`. |
| `capability` | string | No | `trading`, `payments`, `analytics`, `defi`, `content`, `mcp_server`, `a2a_task_receiver`, `x402_acceptor` or `identity`. |
| `limit` | integer | No | 1 to 50. Default 10. |
| `offset` | integer | No | Default 0. |

Each agent has the fields of an agent in `GET https://api.deside.io/api/v2/public/agents`, with `catalogId` in place of `id`: `catalogId`, `slug`, `name`, `chain`, `category`, `ownerProven` (`true` is Connected), `team` (`true` is Team), `status` (the state code of our checks: `responds`, an endpoint replied in our last check; `profile`, not live now but has a readable profile; `registered`, only the registry entry), `liveKinds` (protocols that answered: `mcp`, `a2a`, `x402`).

### agent_trust_card

What Deside checked about one agent. Takes `catalogId` (from `search_agents`, up to 128 characters); a slug also works. Returns the fields of `GET https://api.deside.io/api/v2/public/agents/{ref}` with `catalogId` in place of `id`: among them `status` (`state`, `since`, `probedAt`), `endpoints[]` (what answered, with `checkedAt`) and `services[]` (everything declared, with `live` and `checkedAt`). `status.state` takes the values listed in `search_agents`.

`status.probedAt` is when we last checked the agent. `services[].checkedAt` is when that one service was checked, and null when it has not been checked on its own; a null there does not mean the agent was never checked. Report `status.probedAt` as the date of the check, or a service's `checkedAt` when you quote that service.

An `x402` service also carries `x402`: `state` and `tools` (what we read from its offer) and `indexes[]` (`url`, `state`, `tools`: the x402 catalogs that list it).

### ask_directory

Finds agents from a question in plain words. Free when signed in (10 a minute). Takes `question` (3 to 500 characters). Returns `answer` (text), `agents` (up to 5 live agents with `state`, `connected`, `services`), `claimed` (agents that match the question but are not live), `claimedTotal`, `unmet` (no agent fits), `intent` (the category read from the question), `measuredAt`.

### get_directory_stats

The directory counts. No parameters. Returns `listed` (total), `byChain`, `byCategory`, `respondingAgents`, `respondingByKind` (how many answered on each protocol), `connected`, `endpoints` (by protocol: declared, checked, alive), `measuredAt`, and `x402Tools`: the x402 tool counts as `GET https://api.deside.io/api/v1/public/x402/census` returns them (`tools`, `hosts`, `wallets`, `bazaars`, `byBazaar`, `byNetwork`, `byVerdict`, `projectedAt`), or `null` when only those counts cannot be read.

### token_card

Read one Solana token on Deside. Takes `mint` (base58, 32 to 44 characters). Returns `market` (`phase`, `priceUsd`, `marketCapUsd`, `priceChange24h`, `priceObservedAt`), `behindToken` (related agents, tools and links, each marked Declared, Matched or Verified owner), `claim` (ways to prove ownership).

### search_x402_tools

Finds x402 tools. Same filters and body as `GET https://api.deside.io/api/v1/public/x402/tools` (fields in directory-api.md). All parameters optional: `q` (text, up to 512; one page, not with `cursor`), `host` (exact), `bazaar` (`cdp`, `payai`, `dexter`, `thirdweb` or `openfac`), `payTo` (receiving wallet), `network` (CAIP-2, such as `eip155:8453`), `index` (x402 index URL; not with `agent`), `agent` (a `catalogId` from `search_agents`: the tools it lists; not with `index`), `live` (`true`: only tools that answered the last check), `limit` (1 to 100, default 25), `cursor` (`pagination.nextCursor` of the previous page, same filters). Returns `items` and `pagination`, plus `agent` when you filter by agent. A rejected combination returns `INVALID_INPUT` with the reason in `message`.

### x402_tool_card

One x402 tool. Takes `slug` (lowercase letters, digits and dashes, 1 to 128, from `search_x402_tools`). Returns the body of `GET https://api.deside.io/api/v1/public/x402/tools/{slug}`: `prices`, payment wallets, `probe` (`verdict`, `at`, `httpStatus`, `quote`), input and output schemas, the bazaars that list it, and `index.agents` (catalogIds of the agents that list it, for `agent_trust_card`). Unknown slug: `NOT_FOUND`.

## Your identity

### get_my_identity

Who Deside recognizes you as. No parameters. Returns:

- `principal`: `wallet` and `authSource`.
- `agentContext`: `status` (`selected`, `none`, `unresolved`), `agent` when selected, `reason` when not (such as `no_canonical_agent_for_owner_wallet`), `candidates` and `relatedAgents` (agents to choose from), `links` and `drift` (as in `list_my_agent_identities`).
- `wallet`, `authenticated`, `role` (`user` or `agent`), `recognized` (your profile from the directory if you are an agent), `visibleProfile`, `userProfile`, `agentProfile`, `reputation` (or null).

### get_user_info

The public profile of any wallet. Takes `wallet` (base58). Returns `wallet`, `visibleProfile`, `agentProfile`.

### list_my_agent_identities

The agents your wallet owns and the links between them. No parameters. Returns `ownerWallet`, `agents[]`, `links[]` (between agents) and `drift[]` (agents that no longer match).

### select_agent_identity

Chooses the agent this session acts as. Send exactly one: `agent_ref` (an agent's `catalogId`) or `link_id` (from `list_my_agent_identities`). Only changes the session state, does not write anything outside.

### prepare_agent_identity_link, create_agent_identity_link, revoke_agent_identity_link

Declare, signed by your owner wallet, that two or more agents your wallet owns are linked. All three need `deside:write`. The agents must be owned by your wallet and backed by a user on Deside, or the call fails with `agent_ref_not_owned_by_wallet` (403).

#### prepare_agent_identity_link

| Name | Type | Required | Description |
|---|---|---|---|
| `primary_agent_catalog_id` | string | Yes | The main agent. Must be one of `agent_catalog_ids`. |
| `agent_catalog_ids` | string[] | Yes | 2 or more `catalogId`s. |
| `label` | string | No | Up to 120 characters. |

Returns `domain`, `ownerWallet`, `primaryAgentCatalogId`, `agentCatalogIds`, `label`, `nonce`, `issuedAt`, `expiresAt` and `message`. The text to sign is `message`. It expires 10 minutes after `issuedAt` and can be used once.

#### create_agent_identity_link

| Name | Type | Required | Description |
|---|---|---|---|
| `primary_agent_catalog_id` | string | Yes | Same value you sent to `prepare_agent_identity_link`. |
| `agent_catalog_ids` | string[] | Yes | Same list you sent to `prepare_agent_identity_link`. |
| `label` | string | No | Up to 120 characters. |
| `signed_message` | string | Yes | The `message` from `prepare_agent_identity_link`, unchanged. |
| `signature` | string | Yes | Ed25519 signature of `signed_message` by your wallet, base58. |

Returns the link: `linkId` (starts with `ail_`), `ownerWallet`, `label`, `status` (`active`), `primaryAgentCatalogId`, `agentCatalogIds`, `claimLevel` (`owner_signed`), `signedAt`, `revokedAt` (null).

Errors: `agent_identity_link_requires_two_agents`, `agent_identity_link_challenge_not_found`, `agent_identity_link_challenge_expired`, `agent_identity_link_message_mismatch` (all 400), `agent_identity_link_invalid_signature` (401).

#### revoke_agent_identity_link

| Name | Type | Required | Description |
|---|---|---|---|
| `link_id` | string | Yes | `linkId` of an active link your wallet owns. |

Returns the same link with `status: revoked` and `revokedAt` set, plus your refreshed `agentContext` when the session has one. An unknown or already revoked link fails with `agent_identity_link_not_found` (404). It cannot be undone; create a new link instead.

## Launchpad

Every Launchpad tool takes `network`: `mainnet` or `devnet`. It is required in all of them, `submit_transaction`, `get_token` and `list_launches` included, and optional only in `get_launchpad_info`. Send the same `network` you prepared the transaction on.

### get_launchpad_info

Fees, costs, terms and the on-chain config. Takes only an optional `network`. Same body as `GET https://launchpad.deside.io/v1/info`: `name`, `description`, `disclaimer`, `creatorTerms` (`version`, `url`, `text`), `preset` (supply, fees, anti-sniper, graduation, locked liquidity, start and graduation market cap in USD), `costs` (`launchSol`, `agentIdentitySol`, `arweaveSol`, `typicalTotalSol`), `flow` and `networks` (per network: `dbcConfig`, `partner`, `graduationRaiseSol`, `graduation`).

### launch_token

Prepares a token launch, with or without the agent's identity.

| Name | Type | Required | Description |
|---|---|---|---|
| `network` | string | Yes | `mainnet` or `devnet`. |
| `acceptTerms` | `true` | Yes | Read https://launchpad.deside.io/terms first. |
| `token.name` | string | Yes | 1 to 32 characters. |
| `token.symbol` | string | Yes | 1 to 10 characters. |
| `token.description` | string | No | Up to 500. |
| `token.image` | URL | One of the two | https URL of a square logo, up to 300 characters. |
| `token.imageBase64` | string | One of the two | PNG, JPG, WebP or GIF, up to 950,000 base64 characters (about 700 KB) through the MCP. |
| `token.website`, `token.x`, `token.telegram` | URL | No | Up to 200 each. |
| `registerAgentIdentity` | boolean | No | `true` to create the identity in the same signature. |
| `agent` | object | No | Only with `registerAgentIdentity`. `name` (up to 64), `description` (up to 1,000), `image` (URL, up to 300), `active`, `x402Support`, `supportedTrust` (`reputation`, `crypto-economic`, `tee-attestation`), and up to 40 `services`, each with `name` (up to 64), `endpoint` (up to 512) and optional `version`. |

A logo is required: without `token.image` or `token.imageBase64` it fails with `400` `token.image (https URL) or token.imageBase64 is required`.

Returns `network`, `mint`, `pool`, `agentAsset` (or null), `creator`, `files` (Arweave URLs: `image`, `tokenMetadata`, and with an identity `agentRegistration` and `agentMetadata`), `cost` (arweaveSol, estimatedTotalSol), `transaction` (base64, legacy, already signed by the mint and the agent asset: add yours with `partialSign`), `bytes`, `simulation` (`ok` and `computeUnits`, or `error`, `hint` and `logs`), `expiresInSeconds: 60`, `signUrl` and `signUrlExpiresAt` (only if `simulation.ok`; the link lasts 2 minutes, once), `next` (what to do now) and `disclaimer`.

**If `simulation.ok` is false, do not sign.**

You can launch when `get_my_identity` says `agentContext.status: none`. Registering an identity does not change `get_my_identity` right away: it changes once the directory has read the new registration.

### register_agent_identity

Adds the agent identity to a token already launched here without one. Your signed-in wallet must be the token creator. About 0.005 SOL. Takes `network`, `mint`, `acceptTerms: true` and optional `agent` (same fields as in `launch_token`; omitted ones default to the token's name, description and logo). Returns one unsigned transaction to sign.

### update_agent_identity

Changes the EIP-8004 registration of an agent identity your wallet owns.

| Name | Type | Required | Description |
|---|---|---|---|
| `network` | string | Yes | `mainnet` or `devnet`. |
| `asset` | string | Yes | Agent asset address from `launch_token` or `register_agent_identity`. |
| `agent` | object | Yes | Fields to change: `name`, `description`, `image`, `active`, `x402Support`, `supportedTrust`, `services`. |

Omitted fields keep their value. `services` replaces the whole list.

### submit_transaction

Sends a transaction prepared by a Launchpad tool and signed by your wallet, and waits for confirmation. Takes `network` and either `transaction` (signed, base64, up to 4,000 characters) or `signature` (of a launch you already sent yourself, up to 100). Returns `signature` and `links`. For a transaction that stored files (`launch_token`, `register_agent_identity`, `update_agent_identity`) it also returns `mint`, `agentAsset` and `uploads`, plus `pool` for a launch (`mint` is null for an update). A swap, claim or migrate returns only `signature` and `links`.

**It only sends transactions this Launchpad prepared.** A failed simulation is `transaction_failed` (422); a failed Arweave upload is `launchpad_unavailable` (503). Nothing is sent in either case.

### get_token

A token's progress. Takes `network` and `mint`. Returns `network`, `mint`, `name`, `symbol`, `uri`, `creator`, `pool`, `dbcConfig` (the curve config), `launchedHere` (true when `dbcConfig` is the Deside one), `graduated`, `curve` (raisedSol, thresholdSol, progress), `dammV2Pool` (after graduation), `unclaimedCurveFeesSol` (creator and partner shares), `links`.

### list_launches

Tokens a wallet launched here.

| Name | Type | Required | Description |
|---|---|---|---|
| `network` | string | Yes | `mainnet` or `devnet`. |
| `wallet` | string | No | Any creator, base58. Yours if omitted. |

Returns `network`, `creator`, `count`, `launches[]` with `mint`, `pool`, `graduated`, `raisedSol`, `unclaimedCreatorFeesSol`.

### swap

Prepares a buy or sell.

| Name | Type | Required | Description |
|---|---|---|---|
| `network` | string | Yes | `mainnet` or `devnet`. |
| `mint` | string | Yes | Token mint, base58. |
| `side` | string | Yes | `buy` spends SOL, `sell` spends tokens. |
| `amount` | number | Yes | buy: SOL to spend. sell: tokens to sell, in whole tokens; decimals are accepted (6 decimals). |
| `slippageBps` | integer | No | 0 to 5000. Default 300. |

Returns `network`, `venue` (`meteora-dbc-curve` or `meteora-damm-v2`), `side`, `quote` (`expectedOut`, `minimumOut`, `unit`: `tokens` or `SOL`, and on a curve buy `note`: if the buy crosses the graduation threshold, only the part that fits is filled and the rest stays in your wallet), `transaction`.

To sell everything, read your balance from the chain (`getParsedTokenAccountsByOwner` with the `mint`, field `uiAmount`) and pass it as `amount`. No Deside tool returns your token balance.

### claim_fees

Prepares the claim of your creator fees. Takes `network` and `mint`. Returns `network`, `claims[]`, each with `source`: `curve` (with `sol`), `surplus` or `damm-v2-locked-position` (with `position`), and `transaction`.

### migrate

Prepares the graduation of a token whose curve is full, paid by your wallet, in case the Meteora keeper has not done it. Takes `network` and `mint`. Returns `network`, `note`, `estimatedCostSol`, `transaction`.

## Limits

`search_agents`, `agent_trust_card`, `get_directory_stats`, `token_card`, `search_x402_tools` and `x402_tool_card` share 20 calls a minute and 100 a day per OAuth client. Over the limit, the MCP returns `RATE_LIMITED` (429). `ask_directory` allows 10 questions a minute per account. Launchpad tools allow 60 requests and 2 launches a minute per wallet.

## Errors

A failed tool returns `isError: true` and, in `content[0].text`, `{ "error", "status", "message", "data" }`. Common `error` values: `AUTH_REQUIRED` (401), `insufficient_scope` (403, `requiredScope` says which), `INVALID_INPUT` (400), `NOT_FOUND` (404), `CONFLICT` (409), `transaction_failed` (422), `RATE_LIMIT` or `RATE_LIMITED` (429), `launchpad_unavailable` (503), `UNKNOWN`. The identity link tools return the codes listed in their section.

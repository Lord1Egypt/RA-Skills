# Part 1 Research: Api3 Market discovery, readiness, and funding flows

## Objective

Map what an agent can discover, verify, fund, and maintain today through Api3 Market, and turn that into a concrete MVP contract for `api3-feed-manager`.

## Sources reviewed

Primary docs and surfaces reviewed for this pass:
- https://docs.api3.org/dapps/quickstart/
- https://docs.api3.org/dapps/integration/
- https://docs.api3.org/dapps/integration/contract-integration.html
- https://docs.api3.org/dapps/oev-rewards/
- https://docs.api3.org/oev-searchers/in-depth/data-feeds/
- `@api3/contracts` in this repo's dependencies
- live Api3 Market pages in browser

## Executive summary

The good news is that Part 1 is more concrete than the earlier draft suggested.

A workable agent flow already exists:
1. discover candidate feeds on Api3 Market by chain and pair
2. determine whether the feed is already active on that network
3. if active, return the integration proxy and avoid paying again
4. if inactive, purchase a 3-month plan through Api3 Market
5. return the proxy, active state, and renewal recommendation

The most important implementation decision is to use a **layered source-of-truth model**:
- **Api3 Market** for human-readable discovery and commercial state
- **Api3 contracts** for canonical dAPI to data-feed resolution
- **AirseekerRegistry + Signed APIs** for underlying beacon composition and off-chain signed data inspection
- **Api3ReaderProxyV1 read()** for the final integration-ready state check

For the project, the safest MVP remains:
- default to the **communal/generic Api3ReaderProxyV1 path** for agents
- treat dApp-specific OEV-enabled proxies as a later enhancement unless we explicitly verify the self-serve path end to end

## Confirmed findings

### 1. Api3 Market is the primary discovery surface

From the quickstart and live Market UI:
- Api3 Market serves a catalog of feeds by network
- the network page includes search, featured active feeds, and a full catalog
- **all feeds are inactive by default**
- if a feed is already active, the user lands on the data-feed page directly
- if a feed is inactive, the user lands on the activation page first

This gives us a practical first discovery model:
- search by `chain + pair`
- determine whether the feed is already active
- only enter purchase flow when activation is required

### 2. Activation is a plan purchase, not a low-level oracle-admin flow

Api3 Market exposes activation as a commercial subscription flow:
- mainnets use **3-month plans**
- testnets use **7-day plans**
- plan purchase immediately activates a feed if inactive
- if active already, purchase extends or upgrades the queued operating plan
- the user chooses the deviation threshold subscription tier
- the heartbeat is fixed at **24 hours**

Additional clarification from an Api3 developer:
- each data feed has its **own wallet setup**, but there is only **one sponsor wallet per feed**
- the effective deviation threshold is determined by the feed's **subscriptions queue**, where **smaller thresholds get priority**
- this means the skill should model deviation selection as a queue/subscription concern, not as a separate per-wallet configuration surface

Offered deviation thresholds in docs:
- 5%
- 2.5%
- 1%
- 0.5%
- 0.25%

Important operational behavior from docs:
- once a plan is purchased, Api3 guarantees those update parameters for the purchased plan duration
- after expiry, the feed stops being upheld
- users are responsible for renewing plans if they want continuous service
- if a feed is already active, leftover prepaid value can roll into the next purchase as a discount

### 3. The pricing model is concrete enough for an MVP

Docs state that prices are based on estimated operational cost:
- historical gas cost of updates
- expected update frequency for the chosen deviation threshold
- operating duration

Docs also state:
- prices are charged at estimated operating cost, with a minimum of `$0.05/day`
- overestimates roll into future discounts for the same network-feed pair
- on testnets, updates may stop if payment runs out even before plan expiry

Live Market inspection on Arbitrum showed an activation page quoting total cost directly in **ETH** for that chain.

Working conclusion for the skill:
- we can treat funding as a **time-bound plan purchase**
- the skill should target **90 days on mainnets** by default
- the exact payment asset appears to be the chain-native gas token in the UI at least on Arbitrum, but that still needs explicit per-chain confirmation before we hardcode it as universal behavior

### 4. There are two proxy integration modes

The docs are very clear that integrations consume **Api3ReaderProxyV1**.

From the integration docs:
- `read()` returns `(int224 value, uint32 timestamp)`
- Api3 data feeds have **18 decimals**
- `Api3ReaderProxyV1` also implements Chainlink's `AggregatorV2V3Interface`

From the Market integration docs:
- **Skip OEV Rewards** shows one `Api3ReaderProxyV1` address
- **Earn OEV Rewards** shows a different `Api3ReaderProxyV1` address, and may require a proxy deployment step

From `@api3/contracts` in this repo's dependencies:
- the package exposes **`computeCommunalApi3ReaderProxyV1Address`**
- it also exposes **`computeDappSpecificApi3ReaderProxyV1Address`**
- and **`unsafeComputeDappId`**

That is strong evidence that the product surface really does distinguish between:
- a **communal/generic proxy path**
- a **dApp-specific OEV-enabled proxy path**

For this project, that means the Part 1 MVP should:
- return the **communal proxy** by default
- treat dApp-specific OEV enrollment as optional/advanced
- avoid assuming that the OEV-specific path is the universal default for agent users

### 5. Canonical data-feed resolution is contract-driven under the hood

The strongest technical resolution path came from the Api3 data-feed docs.

The canonical path is:
1. encode the dAPI name, e.g. `ETH/USD`
2. hash it
3. call `Api3ServerV1.dapiNameHashToDataFeedId(...)`
4. call `AirseekerRegistry.dataFeedIdToDetails(...)`
5. decode the result as either:
   - a single beacon `(address airnode, bytes32 templateId)`, or
   - a beacon set `(address[] airnodes, bytes32[] templateIds)`

This gives the skill a proper technical backplane behind Market discovery.

Meaning:
- Market should be used to find the likely feed and active/inactive state
- contract reads should be used to canonicalize the underlying feed identity
- AirseekerRegistry gives the underlying beacon composition for deeper verification

### 6. Signed APIs give a public off-chain inspection surface

Api3 exposes public Signed API endpoints:
- base feed: `https://signed-api.api3.org/public/<airnode>`
- OEV feed: `https://signed-api.api3.org/public-oev/<airnode>`

The docs show the response includes:
- `count`
- `data`
- per-entry fields including `airnode`, `templateId`, `timestamp`, `encodedValue`, and `signature`

Docs also state:
- base feeds are publicly updateable with signed data
- OEV feeds are real-time and tied to the OEV mechanism
- base feed data is served with delay in the OEV design

For the MVP, Signed APIs are useful for:
- inspecting whether the underlying beacon data exists publicly
- checking that the expected airnode/template pairs are live
- validating that the feed is not merely listed but has recent signed data underneath it

### 7. Sponsor-wallet complexity does not appear to be the user-facing activation primitive

Earlier thinking over-indexed on sponsor wallets.

After this pass, the more accurate framing is:
- sponsor-wallet concepts are part of underlying Airnode request sponsorship mechanics
- **Api3 Market activation docs do not present sponsor-wallet management as the normal user workflow for activating a Market feed**
- an Api3 developer clarified that there is **one sponsor wallet per feed**, not one sponsor wallet per subscription tier or deviation choice
- the user-facing flow is still purchase-based: choose parameters, connect wallet, buy plan

So for Part 1:
- sponsor-wallet logic should **not** be treated as the main agent UX
- but the internal model should assume a **stable sponsor wallet per feed**
- deviation thresholds should be modeled as subscription-queue priorities, where smaller thresholds can win precedence
- if sponsor-wallet logic becomes relevant, it should be treated as protocol background or an implementation detail, not the first-class interaction model

## Recommended readiness model for the skill

The skill should classify feeds into these states.

### `unavailable`
Use when:
- the feed is not discoverable on Market for the target chain, and/or
- canonical contract resolution does not produce usable data-feed details

### `listed_inactive`
Use when:
- the feed is listed on Market for the target chain
- but no active plan is currently upholding it
- the next required action is purchase/activation

### `active_communal_usable`
Use when:
- the feed is active on Market
- the communal/generic `Api3ReaderProxyV1` path is available
- a contract-level read succeeds and returns a sane positive value

### `active_but_needs_deeper_verification`
Use when:
- Market suggests the feed is active
- but proxy resolution or on-chain verification is incomplete
- the feed should not yet be reported as safely integration-ready

### `dapp_specific_oev_path_available`
Use when:
- the feed is active or activatable
- and the dApp-specific OEV path is available
- but this should be modeled as optional and separate from the communal default

### `non_operational_or_inconsistent`
Use when:
- the feed is listed or resolvable
- but the proxy read, data-feed details, or signed-data checks do not line up cleanly

## Recommended MVP source-of-truth strategy

### Discovery layer
Use Api3 Market as the first pass for:
- chain availability
- pair naming
- active vs inactive state
- current commercial plan options

### Canonical resolution layer
Use on-chain contract reads for:
- dAPI name to data-feed ID resolution
- data-feed details decoding
- beacon vs beacon-set composition

### Verification layer
Use two checks:
1. Signed API inspection for underlying beacon freshness
2. `Api3ReaderProxyV1.read()` for integration-ready consumption

This is much better than relying only on either:
- the UI, or
- raw contracts without Market context

## Activation and maintenance flow for the skill

### `discover-feed`
Should return:
- requested chain and pair
- whether the feed is listed on Market
- whether it is active now
- communal proxy address if derivable
- whether the dApp-specific OEV path is available or intentionally skipped
- any ambiguity in naming or chain coverage

### `ensure-feed-active`
Should do this sequence:
1. discover the feed on Market
2. if already active, skip purchase and return the proxy
3. if inactive, direct the user or wallet-capable execution path into Market purchase flow
4. target a **3-month mainnet plan** by default
5. after purchase, verify proxy readability before reporting success

### `check-feed-runway`
The docs clearly describe expiration behavior, but this pass did **not** uncover a documented stable API for querying remaining runway programmatically.

So the current implementation assumption should be:
- Market UI is the visible source for expiration today
- a programmatic runway check still needs to be pinned down before the skill can claim full automation here

### `maintain-feed`
For MVP, this should be conservative:
- if expiry information is available, recommend renewal before expiry
- if expiry information is not yet programmatically available, report that limitation explicitly instead of pretending the skill can automate it safely

## Blockers and unresolved questions

These are the real blockers that remain after this pass.

### 1. Programmatic Market API stability is still unclear
We now know how the UI behaves, but we do **not** yet have a confirmed, documented Market API contract that the skill can safely depend on for catalog and expiry queries.

### 2. Exact programmatic expiry/runway path is not yet pinned down
Docs describe expiry and renewal behavior clearly, but I have not yet confirmed the stable underlying API or contract field that exposes remaining runway for automation.

### 3. Exact per-chain payment asset still needs confirmation
The Arbitrum activation flow clearly quoted cost in ETH, which strongly suggests native gas-token payment on that chain. But I have not yet confirmed the rule across all supported networks.

### 4. OEV self-serve flow needs a stricter go/no-go decision
Docs imply that self-serve OEV-enabled integration can be completed through Api3 Market, but the project should still default to the communal path until we explicitly test and trust the dApp-specific flow for agent usage.

### 5. Contract address sourcing needs to be nailed down in implementation
We have the resolution functions and proxy computation helpers, but the implementation still needs a clean source for the correct chain-specific `Api3ServerV1` and `AirseekerRegistry` addresses.

## Implications for issue #5

Issue `#5` should now be built around this narrower MVP:
- default to communal proxy resolution
- use Market for discovery and active/inactive classification
- use contract reads for canonical mapping and verification
- only support purchase guidance or execution once the Market transaction path is confirmed cleanly in code
- keep dApp-specific OEV mode behind an explicit opt-in

## Recommended immediate next implementation steps

1. build a small discovery probe that accepts `chain + pair` and returns Market match candidates
2. wire canonical resolution using `dapiNameHashToDataFeedId` and `dataFeedIdToDetails`
3. add communal proxy computation using `@api3/contracts`
4. add a verification step that calls `read()` on the resolved proxy
5. defer full maintenance automation until expiry/runway can be queried programmatically with confidence

## Bottom line

Issue `#4` is now concrete enough to unblock MVP design.

The Part 1 skill should not be a vague "feed funding helper".
It should be a **discovery + resolution + activation-decision + proxy-return** tool with a conservative verification layer.

That is enough to move into implementation without hand-waving, while keeping the remaining unknowns explicit instead of burying them.

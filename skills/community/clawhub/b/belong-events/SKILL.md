---
name: belong-events
description: Discover events and hubs, manage branding, CheckIn venues, bracelets, wallets, and NFT tickets on the Belong platform
metadata: {"openclaw": {"emoji": "🎫", "primaryEnv": "BELONG_EVENTS_API_KEY", "optionalEnv": ["BELONG_EVENTS_ENDPOINT"], "requires": {"bins": ["curl"]}}}
---

# Belong Events

Discover events and hubs, buy tickets, create events and communities, manage hub branding, and handle venue check-ins, bracelets, and referral flows on Belong.

## How to call tools

Run `{baseDir}/invoke.sh <method> '<params-json>'` via `system.run`. The script calls the Belong skill API and returns JSON.

Example:
```
system.run {baseDir}/invoke.sh discover_events '{"city":"Miami","limit":5}'
```

All tool calls use this pattern. The `invoke.sh` script handles endpoint URL, authentication headers, validates method names, and streams the JSON-RPC body over stdin instead of interpolating user params into curl arguments.

Default endpoint:
`https://join.belong.net/functions/v1/openclaw-skill-proxy`

Network disclosure:
- All JSON-RPC calls are sent to the endpoint above (or `BELONG_EVENTS_ENDPOINT` if overridden).
- If `BELONG_EVENTS_API_KEY` is set, it is sent to that endpoint as `X-OpenClaw-Key`.

## Account linking (required for protected tools)

Most tools require a linked Belong account. If any tool returns "Belong account not linked" or "BELONG_LINK_REQUIRED", run the OTP flow:

1. Ask the user for their email address.
2. Send OTP:
   ```
   system.run {baseDir}/invoke.sh belong_email_otp_send '{"email":"USER_EMAIL"}'
   ```
3. Ask for the 6-digit code from their email.
4. Verify OTP:
   ```
   system.run {baseDir}/invoke.sh belong_email_otp_verify '{"email":"USER_EMAIL","otp":"CODE"}'
   ```
5. The response includes `apiKey`. Store it — set it as `BELONG_EVENTS_API_KEY` env var or update `skills.entries.belong-events.apiKey` in `openclaw.json` so subsequent calls are authenticated.

Never ask end users for an API key. Always use the OTP flow.

## Available tools

### Public (no auth needed)
Public tools are rate-limited. If you hit a 429, wait and retry.

- **list_tools** — List available tools (no params)
- **discover_events** — Search events. Params: `city`, `category`, `startDate`, `endDate`, `limit`, `latitude`, `longitude` (all optional)
- **discover_hubs** — Search public hubs. Params: `search`, `hubType`, `limit`, `cursor`
- **get_event_details** — Get event details. Params: `eventId` (required), `source`, `city`, `latitude`, `longitude` (optional)
- **get_hub_details** — Get hub details including public CheckIn terms. Params: `hubId` (required), `includeEvents`, `includeBranding`
- **get_hub_branding** — Get hub branding. Params: `hubId` (required)
- **buy_ticket** — Get checkout/event URL. Params: `eventId` (required), `tierId`, `quantity`
- **get_checkin_leaderboards** — Load public venue and attendee leaderboards. Params: `limit`, `timeframe` (`all`, `today`, `week`, `month`)
- **belong_email_otp_send** — Send OTP. Params: `email` (required)
- **belong_email_otp_verify** — Verify OTP. Params: `email` (required), `otp` (required)

### Account status (auth required)
- **whoami** — Check link status (no params)
- **get_profile** — Get the linked Belong profile
- **list_wallets** — List linked crypto wallets
- **sync_wallets** — Sync wallets from the configured provider
- **get_referral_code** — Look up the linked wallet referral code. Params: `chainId` (required), `walletAddress`
- **register_promoter** — Register as a promoter for a venue. Params: `hubId` (required), `walletAddress`, `chainId`
- **get_promoter_link** — Create an attributed CheckIn link. Params: `hubId` (required), `eventId`, `walletAddress`
- **get_promoter_earnings** — Load your promoter earnings and conversions. Params: `hubId`
- **request_promoter_payout** — Prepare a USDC promoter earnings payout. Params: `hubId` (required), `currency` (USDC only, the default), `walletAddress`

### Attendee (auth required)
- **my_tickets** — List purchased tickets. Params: `status` (upcoming/past/all). Returns `ticketCheckinUrl` for each ticket.
- **my_checkins** — List the linked user’s check-in history and stats. Params: `limit`, `offset`
- **get_visit_receipt** — Issue or return a portable visit proof for one of the linked user's own witnessed check-ins. Requires visit proofs in Settings. Params: `checkinId` (required)

### Organizer (auth required)
- **create_event** — Create event. Params: `name` (required), `startDate` (required), `endDate` (required), `description`, `city`, `venue`, `category`, `hubId`, `coverImage`
- **update_event** — Update event. Params: `eventId` (required), `name`, `description`, `startDate`, `endDate`, `city`, `venue`, `category`, `hubId`, `coverImage`
- **add_event_media** — Upload event media. Params: `eventId` (required), `files` (required base64 file array)
- **update_event_media** — Replace/reorder event media. Params: `eventId` (required), `media` (required)
- **delete_event_media** — Delete event media. Params: `eventId` (required), `mediaId` (required)
- **deploy_tickets** — Deploy NFT tickets. Params: `eventId` (required), `tierName` (required), `description`, `tierDescription`, `price` (required), `maxSupply`, `chainId` (required), `transferable`, `gasless`, `subEventId`, `txHash`. Two-phase: first call returns transaction parameters; a follow-up with `txHash` completes deployment.
- **my_events** — List owned events. Params: `status` (upcoming/past/draft/all)
- **event_analytics** — Event stats. Params: `eventId` (required)
- **create_hub** — Create hub/community. Params: `name` (required), `slug`, `description`, `location`, `private`, `hubType`, `startDate`, `endDate`, `coverImage`, `communitySkinConfig`, `customDomains`
- **update_hub** — Update hub/community. Params: `hubId` (required), `name`, `slug`, `description`, `location`, `private`, `hubType`, `startDate`, `endDate`, `coverImage`, `connectEventIds`, `categorySubEventIDs`, `communitySkinConfig`, `customDomains`
- **my_hubs** — List owned or joined hubs. Params: `search`, `hubType`
- **configure_hub_branding** — Save hub branding and custom domains. Params: `hubId` (required), `communitySkinConfig`, `customDomains`

### Venue (auth required)
- **check_in** — Process check-ins, quoted venue payments, or owner approvals. Params: `hubId` (required), `accessMode`, `amount`/`paymentAmount`, `paymentCurrency`, `paymentTxHash`/`paymentTransactionHash`, `paymentChainId`, `latitude`, `longitude`, `promoterCode`, `promoterAddress`, `promoterWallet`, `pendingCheckinId`, `nftTokenId`, `nftContractAddress`, `linkedEventId`, `customerWallet`, `listPending`, `checkinId`, `action`, `description`
- **list_pending_checkins** — List pending venue approvals. Params: `hubId` (required), `limit`, `checkinId`. Pending rows include `payment_request_source` and `payment_request_label` when available.
- **approve_checkin** — Approve, reject, or quote. Params: `checkinId` (required), `action`, `amount`, `currency`, `description`
- **get_venue_info** — Load venue settings, stats, and on-chain venue info. Params: `hubId` (required), `venueAddress`, `chainId`, `includeStats`. `chainId` must come from the explicit param or persisted venue settings.
- **configure_venue** — Update venue rules and sync to MCP. Params: `hubId` (required), `venueWallet`, `ownerAddress`, `chainId`, `verificationMethod`, `requireVenueApproval`, `venueLatitude`, `venueLongitude`, `checkinRadius`, `primaryAccessMode`, `accessModeFree`, `accessModeVenuePayment`, `accessModeNftTicket`, `accessModeNftMembership`, `venuePaymentFlow`, `minCheckAmount`, `fixedPaymentAmount`, `acceptUSDC`, `acceptLONG`, `longSettlement`, `enableVisitorRewards`, `visitorVisitBountyUsd`, `visitorSpendPercentage`, `enablePromoterRewards`, `promoterVisitBountyUsd`, `promoterSpendPercentage`, `dailyCheckinLimit`, `requiredNftCollections`, `braceletEnabled`, `braceletDisplayCurrency`, `braceletAcceptedTokens`, `braceletMinTopup`, `braceletMaxTopup`, `braceletAllowRefunds`, `braceletChargeCategories`, `braceletPoolWallet`
- **get_venue_checkin_history** — Load owner-scoped row-level venue history. Params: `hubId` (required), `limit`, `offset`
- **get_owner_checkin_stats** — Load owner dashboard stats. Params: `days`
- **deposit_venue_funds** — Prepare a venue deposit transaction. Params: `hubId` (required), `amount` (required), `venueWallet`, `ownerAddress`, `chainId`, `promoterAddress`. Supplied addresses must match the authenticated signer and persisted venue payment account.
- **pay_to_venue** — Prepare a customer venue payment transaction. Params: `hubId` (required), `amount` (required), `venueAddress`, `walletAddress`, `promoterAddress`, `chainId`, `paymentCurrency`, `currency`. Supplied addresses must match the authenticated signer and persisted venue payment account.
- **setup_venue_rewards** — Configure rewards. Params: `hubId` (required), `visitBounty`, `visitorSpendPercentage`, `cashbackPercent` (legacy alias)
- **get_bracelet_balance** — Load bracelet balance and recent transactions. Params: `braceletUid` (required), `eventHubId` (required)
- **link_bracelet** — Link a bracelet to the authenticated attendee. Params: `braceletUid` (required), `eventHubId` (required), `displayName`
- **topup_bracelet** — Credit a bracelet after a verified payment. Params: `braceletUid` (required), `eventHubId` (required), `amount` (required), `currency` (required), `txHash` (required), `chainId`, `displayAmount`, `displayCurrency`, `conversionRate`, `topupAuthorizationId`
- **charge_bracelet** — Charge a bracelet with staff PIN authorization. Params: `braceletUid` (required), `eventHubId` (required), `amount` (required), `currency` (required), `staffPin` (required), `displayAmount`, `displayCurrency`, `conversionRate`, `description`, `chargeCategory`, `idempotencyKey` (required)
- **refund_bracelet** — Refund bracelet balance. Params: `braceletUid` (required), `eventHubId` (required), `currency` (required), `amount`, `refundToAddress`, `idempotencyKey` (required)
- **get_bracelet_event_summary** — Load organizer cashless summary. Params: `eventHubId` (required)
- **withdraw_earnings** — Withdrawal link. Params: `hubId` (required), `currency` (USDC/LONG)

### Live-event autonomy (auth required)
These tools back the live-event agent. The server-side autonomy executor is fail-closed and limited to its reviewed allowlist. Availability and reservation mutations are unavailable until Belong can verify the required human review or staff authorization server-side.

- **influence_score** — Score your own Belong-native activity (read-only; grants nothing). Accepts no target account identifier.
- **agent_action_decide_execute** — Decide an action's autonomy tier and execute it when allowed; idempotent per `idempotencyKey`. Params: `deployId` (required), `actionKind` (required), `idempotencyKey` (required), `params`, `actionId`, `riskFlags`, `missingContext`, `confirm`
- **agent_action_undo** — Compensate a prior reversible action (currently the non-money check-in quote). Params: `deployId` (required), `actionId` (required), `idempotencyKey` (required)
- **availability_list** — List the artist's availability windows (read-only). Params: `from`, `to` (ISO)
- **reservation_quote** — Quote available tables and upsell offers for a party (read-only). Params: `hubId` (required), `partySize`, `prefs`

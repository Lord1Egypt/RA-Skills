# AgentRef REST endpoints

This file is intentionally curated. It covers the main merchant-admin flows for OpenClaw skill usage and a single identity check that also works for affiliate keys.

## Common contract

- Base URL: `https://www.agentref.co/api/v1`
- Auth header: `Authorization: Bearer <AGENTREF_API_KEY>`
- Success shape: `{ data, meta }`
- Error shape: `{ error: { code, message, details? }, meta: { requestId } }`
- Pagination: list endpoints support `page` and `pageSize`, `offset` and `limit`, or `cursor` and `limit`; follow the returned `meta`
- Idempotency: send `Idempotency-Key` on documented POST writes that support replay protection
- Owner split: `GET /api/v1/me` tells you whether the key is `merchant` or `affiliate`; the merchant endpoints below require a merchant key

## Identity and onboarding

### GET /api/v1/me

- Method: `GET`
- Path: `/api/v1/me`
- Purpose: Connectivity and identity check. Always call this first.
- Important inputs: Auth header only.
- Important outputs: `data.key.ownerType`, `data.key.keyType`, `data.key.scopes`, merchant or affiliate owner details, and for merchant keys `data.programs[]` with `id`, `name`, `status`, `marketplaceStatus`, `readiness`, `website`, `landingPageUrl`, `stripeConnectedAt`
- Risks / write access: Read-only. Use it to decide whether merchant workflows are allowed.

### GET /api/v1/merchant

- Method: `GET`
- Path: `/api/v1/merchant`
- Purpose: Read the merchant profile and onboarding-related account defaults.
- Important inputs: Auth header with a merchant-capable read scope.
- Important outputs: Merchant profile fields such as `companyName`, billing status, payout defaults, timezone, tracking settings, `onboardingCompleted`, `onboardingStep`, `notificationPreferences`
- Risks / write access: Read-only.

### POST /api/v1/onboarding/merchant

- Method: `POST`
- Path: `/api/v1/onboarding/merchant`
- Purpose: Set the initial merchant company name during onboarding.
- Important inputs: JSON body with `companyName`
- Important outputs: `merchantId`, `companyName`
- Risks / write access: Write. Changes merchant profile state. Confirm if you are overwriting an existing company name.

### PATCH /api/v1/merchant

- Method: `PATCH`
- Path: `/api/v1/merchant`
- Purpose: Update merchant profile, billing defaults, and tracking settings after onboarding starts.
- Important inputs: Partial JSON body such as `companyName`, billing fields, `timezone`, `defaultCookieDuration`, `defaultPayoutThreshold`, `trackingRequiresConsent`, `trackingParamAliases`
- Important outputs: Updated merchant profile
- Risks / write access: Write. Changes account-level defaults that affect future program setup and tracking behavior.

### POST /api/v1/onboarding/complete

- Method: `POST`
- Path: `/api/v1/onboarding/complete`
- Purpose: Mark onboarding complete after the required setup is actually done.
- Important inputs: Auth header only. The key must be a `full` key; onboarding-only keys are rejected.
- Important outputs: `onboardingCompleted`, `onboardingStep`
- Risks / write access: Write. Do this only after the user confirms that onboarding should be finalized.

## Programs

### GET /api/v1/programs

- Method: `GET`
- Path: `/api/v1/programs`
- Purpose: List the merchant's programs.
- Important inputs: Optional filters `status`, `page`, `pageSize`, `offset`, `limit`, `cursor`
- Important outputs: Paginated list of program records
- Risks / write access: Read-only.

### POST /api/v1/programs

- Method: `POST`
- Path: `/api/v1/programs`
- Purpose: Create a new program.
- Important inputs: JSON body with `name`, `commissionType`, `commissionPercent`; optional `description`, `website`, `landingPageUrl`, `cookieDuration`, `payoutThreshold`, `payoutFrequency`, `autoApproveAffiliates`, `portalSlug`, `currency`; supports `Idempotency-Key`
- Important outputs: Created program record
- Risks / write access: Write. Creates a new program and should only happen with explicit user confirmation.

### GET /api/v1/programs/{id}

- Method: `GET`
- Path: `/api/v1/programs/{id}`
- Purpose: Read one program in detail.
- Important inputs: `id` path parameter
- Important outputs: Program detail plus `readiness`
- Risks / write access: Read-only.

### PATCH /api/v1/programs/{id}

- Method: `PATCH`
- Path: `/api/v1/programs/{id}`
- Purpose: Update one program's config and status.
- Important inputs: `id` plus a partial JSON body such as `name`, `description`, `website`, `landingPageUrl`, `status`, commission settings, payout settings, `autoApproveAffiliates`, `portalSlug`, `currency`
- Important outputs: Updated program record
- Risks / write access: Write. This can change live program behavior, visibility, or payout rules. Read the program first and confirm the exact patch.

### DELETE /api/v1/programs/{id}

- Method: `DELETE`
- Path: `/api/v1/programs/{id}`
- Purpose: Archive a program.
- Important inputs: `id` path parameter
- Important outputs: Archived program record
- Risks / write access: Destructive write. Treat this as high risk and require explicit user confirmation.

### GET /api/v1/programs/{id}/stats

- Method: `GET`
- Path: `/api/v1/programs/{id}/stats`
- Purpose: Get a compact program performance summary.
- Important inputs: `id` path parameter
- Important outputs: `programId`, `programName`, `status`, `totalRevenue`, `totalConversions`, `totalCommissions`, `pendingCommissions`, `activeAffiliates`, `conversionsByStatus`
- Risks / write access: Read-only.

### POST /api/v1/programs/{id}/connect-stripe

- Method: `POST`
- Path: `/api/v1/programs/{id}/connect-stripe`
- Purpose: Start the Stripe Connect OAuth flow for a specific program.
- Important inputs: `id` path parameter; optional body `{ "method": "oauth_url" }`
- Important outputs: `programId`, `method`, `authUrl`, `message`
- Risks / write access: Write. This does not complete the Stripe setup itself, but it does start an external auth flow. Confirm before triggering it.

### GET /api/v1/programs/{id}/tracking/status

- Method: `GET`
- Path: `/api/v1/programs/{id}/tracking/status`
- Purpose: Read tracking installation and attribution health for one program.
- Important inputs: `id` path parameter
- Important outputs: `status`, `stats`, `recent`, `health`, `warnings`, `summary`
- Risks / write access: Read-only.

## Affiliates

### GET /api/v1/affiliates

- Method: `GET`
- Path: `/api/v1/affiliates`
- Purpose: List affiliates across the merchant or for one program.
- Important inputs: Optional `programId`, `includeBlocked`, `search`, `sortBy`, `sortOrder`, `status`, plus pagination params
- Important outputs: Paginated affiliate list
- Risks / write access: Read-only.

### GET /api/v1/affiliates/{id}

- Method: `GET`
- Path: `/api/v1/affiliates/{id}`
- Purpose: Read one affiliate. Use `include=stats` for the richer detail view.
- Important inputs: `id` path parameter; optional query `include=stats`
- Important outputs: Affiliate record, or a richer affiliate detail payload when `include=stats`
- Risks / write access: Read-only.

### POST /api/v1/affiliates/{id}/approve

- Method: `POST`
- Path: `/api/v1/affiliates/{id}/approve`
- Purpose: Approve a pending affiliate.
- Important inputs: `id` path parameter; supports `Idempotency-Key`
- Important outputs: Updated affiliate record
- Risks / write access: Write. Changes access state. Read the affiliate first and confirm approval.

### POST /api/v1/affiliates/{id}/block

- Method: `POST`
- Path: `/api/v1/affiliates/{id}/block`
- Purpose: Block an affiliate.
- Important inputs: `id` path parameter; optional JSON body `{ "reason": "..." }`; supports `Idempotency-Key`
- Important outputs: Updated affiliate record
- Risks / write access: Destructive write. Blocks access and should only happen after explicit user confirmation.

### POST /api/v1/affiliates/{id}/unblock

- Method: `POST`
- Path: `/api/v1/affiliates/{id}/unblock`
- Purpose: Remove a block from an affiliate.
- Important inputs: `id` path parameter; supports `Idempotency-Key`
- Important outputs: Updated affiliate record
- Risks / write access: Write. Changes access state. Confirm before sending.

## Conversions

### GET /api/v1/conversions

- Method: `GET`
- Path: `/api/v1/conversions`
- Purpose: List conversions with filters for program, affiliate, status, and time range.
- Important inputs: Optional `programId`, `affiliateId`, `status`, `startDate`, `endDate`, `from`, `to`, plus pagination params
- Important outputs: Paginated conversion list
- Risks / write access: Read-only.

### GET /api/v1/conversions/stats

- Method: `GET`
- Path: `/api/v1/conversions/stats`
- Purpose: Get aggregate conversion performance over a period.
- Important inputs: Optional `programId`; `period` in `7d`, `30d`, `90d`, or `all`
- Important outputs: Aggregate conversion, revenue, and commission stats
- Risks / write access: Read-only.

### GET /api/v1/conversions/recent

- Method: `GET`
- Path: `/api/v1/conversions/recent`
- Purpose: Read a short feed of recent conversions.
- Important inputs: Optional `limit` up to `20`
- Important outputs: Recent conversion items
- Risks / write access: Read-only.

## Flags

### GET /api/v1/flags

- Method: `GET`
- Path: `/api/v1/flags`
- Purpose: List fraud and review flags that need attention.
- Important inputs: Optional `status`, `type`, `affiliateId`, plus pagination params
- Important outputs: Paginated flag list
- Risks / write access: Read-only.

### GET /api/v1/flags/stats

- Method: `GET`
- Path: `/api/v1/flags/stats`
- Purpose: Get a compact fraud-queue summary.
- Important inputs: Auth header only
- Important outputs: Flag counts and summary stats
- Risks / write access: Read-only.

### POST /api/v1/flags/{id}/resolve

- Method: `POST`
- Path: `/api/v1/flags/{id}/resolve`
- Purpose: Mark a flag as reviewed, dismissed, or confirmed.
- Important inputs: `id` path parameter; JSON body with `status`, optional `note`, optional `blockAffiliate`; supports `Idempotency-Key`
- Important outputs: Resolution result
- Risks / write access: Write. `confirmed` and `blockAffiliate: true` can directly change affiliate access; always confirm first.

## Payouts

### GET /api/v1/payouts/pending

- Method: `GET`
- Path: `/api/v1/payouts/pending`
- Purpose: List payout-ready affiliates for the merchant or one program.
- Important inputs: Optional `programId` plus pagination params
- Important outputs: Paginated list of payout-ready affiliates and releasable payout context
- Risks / write access: Read-only.

### GET /api/v1/payouts

- Method: `GET`
- Path: `/api/v1/payouts`
- Purpose: List payout records.
- Important inputs: Optional `programId`, `affiliateId`, `status`, `startDate`, `endDate`, `from`, `to`, plus pagination params
- Important outputs: Paginated payout list
- Risks / write access: Read-only.

### GET /api/v1/payouts/stats

- Method: `GET`
- Path: `/api/v1/payouts/stats`
- Purpose: Get aggregate payout metrics over a period.
- Important inputs: Optional `programId`; `period` in `7d`, `30d`, `90d`, or `all`
- Important outputs: Aggregate payout stats
- Risks / write access: Read-only.

### POST /api/v1/payouts

- Method: `POST`
- Path: `/api/v1/payouts`
- Purpose: Create one manual payout record for an affiliate-program pair.
- Important inputs: JSON body with `affiliateId`, `programId`, optional `notes`; supports `Idempotency-Key`
- Important outputs: Created payout record
- Risks / write access: Write. This records a payout run and should only happen after the user confirms the target affiliate and program.

## Not part of this curated REST surface

- There is no curated REST onboarding status endpoint like MCP `get_onboarding_status`; derive onboarding state from `GET /api/v1/me`, `GET /api/v1/merchant`, `GET /api/v1/programs`, and `GET /api/v1/programs/{id}/tracking/status`
- There is no curated REST `GET /api/v1/payouts/upcoming` endpoint
- There is no curated REST payout status transition endpoint in `src/app/api/v1/payouts`; do not invent `PATCH /api/v1/payouts/{id}` or similar
- There is no curated REST `GET /api/v1/flags/{id}` endpoint; use `GET /api/v1/flags` filters plus affiliate reads for context

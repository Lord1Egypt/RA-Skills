# AgentRef REST workflows

Use these sequences for common user intents. Start with `GET /api/v1/me` unless the current session already has fresh identity context from the same key.

## Global guardrails

- Read first, write second
- Reuse IDs already returned by earlier calls
- If the key resolves to `ownerType: affiliate`, do not run merchant-admin workflows
- For writes, summarize the exact action and get clear user confirmation before sending it

## "Can you check whether this AgentRef key works?"

1. `GET /api/v1/me`
2. Read `data.key.ownerType`, `data.key.keyType`, `data.key.scopes`
3. For merchant keys, keep `data.programs[]` for later steps instead of immediately calling `/programs` again
4. If access fails, report the exact endpoint, HTTP status, error code, and `meta.requestId`

## "Help me finish merchant onboarding"

1. `GET /api/v1/me`
2. If the key is not a merchant key, stop and say merchant onboarding is not available with this key
3. `GET /api/v1/merchant`
4. If the company name is missing or wrong, use `POST /api/v1/onboarding/merchant` for the initial name or `PATCH /api/v1/merchant` for broader profile updates
5. `GET /api/v1/programs`
6. If no suitable program exists, confirm creation and then `POST /api/v1/programs`
7. If Stripe is not connected for the target program, confirm and then `POST /api/v1/programs/{id}/connect-stripe`
8. `GET /api/v1/programs/{id}/tracking/status`
9. Only after the user confirms that setup is really done, and only with a `full` key, call `POST /api/v1/onboarding/complete`

## "How is my program running?"

1. `GET /api/v1/me`
2. Pick the target `programId` from `data.programs[]`; if there are multiple candidates, ask which program to inspect
3. `GET /api/v1/programs/{id}`
4. `GET /api/v1/programs/{id}/stats`
5. `GET /api/v1/conversions/stats?programId={id}&period=30d`
6. If the user mentions setup, attribution, or tracking quality, also call `GET /api/v1/programs/{id}/tracking/status`

This gives you config state, readiness, revenue and conversion totals, status breakdowns, and tracking health without mutating anything.

## "Show me my top affiliates"

1. `GET /api/v1/me`
2. Choose a `programId` if the user wants one program only
3. `GET /api/v1/affiliates?programId={id}&status=approved&sortBy=totalRevenue&sortOrder=desc&limit=10`
4. If the user wants a deeper view for one affiliate, call `GET /api/v1/affiliates/{affiliateId}?include=stats`

If the user cares more about traffic than revenue, switch `sortBy` to `totalClicks`.

## "Which conversions need attention?"

1. `GET /api/v1/me`
2. Choose the target program if needed
3. `GET /api/v1/conversions?programId={id}&status=pending&limit=50`
4. `GET /api/v1/conversions/stats?programId={id}&period=30d`
5. If the user wants a quick recent feed, add `GET /api/v1/conversions/recent?limit=10`

Use this flow to answer review, pipeline, and payout-readiness questions before touching any write endpoint.

## "Which fraud flags do I need to review?"

1. `GET /api/v1/me`
2. `GET /api/v1/flags?status=open&limit=50`
3. Optional: `GET /api/v1/flags/stats` for queue-level summary
4. If a flag points to a specific affiliate and the user wants context, call `GET /api/v1/affiliates/{affiliateId}?include=stats`
5. If the user wants to resolve a flag, state the exact resolution you intend to send and wait for confirmation
6. After confirmation, `POST /api/v1/flags/{flagId}/resolve`

When resolving, only set `blockAffiliate: true` if the user explicitly asked for it or explicitly confirmed that outcome.

## "Which payouts are open?"

1. `GET /api/v1/me`
2. If the question is about payout-ready affiliates, call `GET /api/v1/payouts/pending` or narrow it with `programId`
3. If the question is about already created payout records, call `GET /api/v1/payouts?status=pending`
4. Optional: `GET /api/v1/payouts/stats?period=30d` for a quick summary

Use `pending` plus `payouts` together when the user wants both "who is ready" and "what has already been recorded".

## "Create a payout for this affiliate"

1. `GET /api/v1/me`
2. `GET /api/v1/payouts/pending?programId={id}` to verify the affiliate is payout-ready
3. If the affiliate or program is still ambiguous, resolve that with `GET /api/v1/affiliates` or the current program context first
4. State the exact `{ affiliateId, programId, notes }` payload you plan to send and ask for confirmation
5. After confirmation, `POST /api/v1/payouts`

Do not create payout records speculatively. This is a write with accounting implications.

## "Approve, block, or unblock an affiliate"

1. `GET /api/v1/me`
2. `GET /api/v1/affiliates?search={query}` or narrow by `programId` and `status`
3. `GET /api/v1/affiliates/{affiliateId}?include=stats`
4. State the exact moderation action and its effect
5. After confirmation, call one of:
   - `POST /api/v1/affiliates/{affiliateId}/approve`
   - `POST /api/v1/affiliates/{affiliateId}/block`
   - `POST /api/v1/affiliates/{affiliateId}/unblock`

Blocking is the highest-risk moderation action in this set. Treat it accordingly.

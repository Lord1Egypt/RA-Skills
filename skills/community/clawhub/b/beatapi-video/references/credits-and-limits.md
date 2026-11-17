# USD balance and launch limits

Use the bundled OpenAPI contract as the source of truth if these launch values
change.

## Customer balance

Customer balances and usage are USD-denominated. Compatibility fields retain
names such as `credit_balance`, `credits_reserved`, `credits_charged`,
`credits_settled`, and `credits_refunded`; 1 Credit = $1 USD. Treat these as
decimal USD amounts, not integer token counts.

Do not use legacy per-second credit tables. Text, image, video, workflow,
Realtime, Video Analysis, and Effect prices depend on the selected public
contract and can change. Check the current public documentation, then read the
exact reserved or charged amount from the response. Manual Music Video
composition is the fixed public exception documented in the current contract.

Do not promise a welcome balance or promotional amount without checking the
current public contract.

For Music Video creation, BeatAPI bills detected audio duration. Use the
request `duration` only as a documented fallback when duration detection fails;
it cannot override a detected duration.

## Input limits

- Follow the exact media count, format, size, duration, and aspect-ratio limits
  in `beatapi.openapi.yaml` for the selected capability.
- Model-specific image and video constraints can differ; discover the current
  model catalog and validate the matching OpenAPI request variant.
- Video Analysis requires a public HTTPS video URL.
- Reject localhost, private-network, data, and non-HTTPS URLs.
- Upload supported local inputs with `beatapi files upload` or
  `beatapi_upload_file`.

## Preflight

Run `beatapi usage` or call `beatapi_get_usage` before paid work. Check:

- `credit_balance` as a USD amount;
- `concurrency.limit`;
- `concurrency.active`.

Do not treat a sufficient balance as proof that concurrency is available.
Storyboard-ready and requires-action tasks can have settled charges without
counting as active processing.

## Realtime sessions

- Allowed maximum durations are 15, 60, and 300 seconds.
- Every create request requires 1-10 exact HTTPS `allowed_origins` and an
  `Idempotency-Key`.
- Creation reserves USD balance; billing activates only after the first accepted
  heartbeat after remote output begins. Inspect `credits.reserved`,
  `credits.settled`, and `credits.refunded` on the session.
- A Realtime session has its own capacity rules. Treat
  `realtime_capacity_unavailable` and `user_concurrency_exceeded` as signals to
  close or wait, not as reasons to retry in a tight loop.

# REST API fallback (no CLI)

For environments where npm is unavailable. Everything the CLI does is a `/v1` REST call. Full docs: https://developers.converly.io

Base URL: `https://app.converly.io/api/v1`

Auth: `Authorization: Bearer $CONVERLY_API_KEY` on every request. Without the CLI there is no browser login, so this path requires the key to already exist in the environment. Never echo it; use the env var in the command.

The rules from SKILL.md still apply, especially: a human completes the destination connect URL, and success is only reported after verification.

Two curl rules for agents:

- Always use `--fail-with-body`. Plain `curl -sS` exits 0 on HTTP 4xx/5xx, so a failed API call would look like success to your shell.
- Generate ONE idempotency key per logical create (`IDEM=$(uuidgen)`) and reuse that exact value on any retry of the same operation. A fresh key on a retry can double-create.

```bash
BASE="https://app.converly.io/api/v1"
AUTH="Authorization: Bearer $CONVERLY_API_KEY"
CURL="curl -sS --fail-with-body"

# 1. Sites
$CURL "$BASE/sites" -H "$AUTH"
$CURL -X PATCH "$BASE/sites/{site_id}" -H "$AUTH" \
  -H "Content-Type: application/json" -d '{"domain":"example.com"}'

# 2. Install snippet + status
$CURL "$BASE/sites/{site_id}/install-snippet" -H "$AUTH"
$CURL "$BASE/sites/{site_id}/install-status" -H "$AUTH"

# 3. Connect an ad platform (human opens `url`, then poll)
IDEM=$(uuidgen)   # keep this value; reuse it if you retry this exact call
$CURL -X POST "$BASE/handoffs" -H "$AUTH" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEM" \
  -d '{"purpose":"connect_destination","destination_type":"google-ads","site_id":"{site_id}"}'
$CURL "$BASE/handoffs/{handoff_id}" -H "$AUTH"   # until status == "completed"

# 4. Catalogues (public, no auth needed)
$CURL "$BASE/trigger-types"
$CURL "$BASE/destination-types"
$CURL "$BASE/action-types?destination_type=google-ads"
$CURL "$BASE/destinations/dest_google-ads/conversions" -H "$AUTH"

# 5. Create, validate, publish a flow
IDEM=$(uuidgen)
curl -sS --fail-with-body -X POST "$BASE/flows" -H "$AUTH" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEM" -d '{
  "site_id": "{site_id}",
  "name": "Demo requests",
  "trigger_config": { "integrationId": "generic-form", "pageFilter": "all" },
  "actions_config": [{
    "id": "act-1",
    "integrationId": "google-ads",
    "config": { "conversion": { "id": "123456789" }, "enhancedConversions": true }
  }]
}'
$CURL -X POST "$BASE/flows/{flow_id}/validate" -H "$AUTH"
$CURL -X POST "$BASE/flows/{flow_id}/publish" -H "$AUTH" -H "Idempotency-Key: $(uuidgen)"

# 6. Verify destination delivery
# The action config here must MATCH the published flow's action exactly
# (same conversion, same enhancedConversions), or you are testing something
# other than what will run.
$CURL -X POST "$BASE/test-event" -H "$AUTH" -H "Content-Type: application/json" -d '{
  "flow_id": "{flow_id}",
  "action": { "action_id": "act-1", "integration_id": "google-ads",
              "config": { "conversion": { "id": "123456789" }, "enhancedConversions": true } }
}'

# 7. Read conversions
$CURL "$BASE/events?limit=20" -H "$AUTH"
$CURL "$BASE/events/{event_id}" -H "$AUTH"
```

Notes that differ from what you might assume:

- IDs are prefixed (`site_`, `flow_`, `hdf_`, `evt_`). Use them verbatim in paths.
- Every POST accepts an `Idempotency-Key` header; one UUID per logical operation, reused verbatim on retries of that operation.
- `meta-ads` is rejected as a slug; the Meta slug is `meta`.
- `value`/`currency` nest INSIDE the `conversion` object; the enhanced conversions toggle is top level `enhancedConversions`.
- Events list is a bounded snapshot (limit max 100, no cursors). Narrow with `occurred_after`, `flow_id`, `email`, `status`.

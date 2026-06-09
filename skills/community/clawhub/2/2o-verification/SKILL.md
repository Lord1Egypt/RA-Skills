---
name: 2o-verification
description: Human verification for AI agents. Submit claims, draft responses, or observation requests to human domain experts via the 2O API. Returns structured verdicts with confidence scores and evidence.
requires:
  env:
    - TWO_O_API_KEY
---

# 2O — Human Verification API

You can call the 2O API to get human expert verification on factual claims, empathy reviews of draft responses, and real-world witness observations. Human domain experts review submissions and return structured results.

## Setup

The user needs a 2O API key. Register at https://www.2oapi.xyz/register to get one ($5 free credits included). The key is stored in the `TWO_O_API_KEY` environment variable.

## Verify a Factual Claim

Use this when you need a human expert to verify whether a claim is true, false, or partially true.

```bash
curl -s -X POST "https://www.2oapi.xyz/api/v1/verify" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TWO_O_API_KEY" \
  -d '{
    "claim": "The claim to verify",
    "domain": "general",
    "budget_cents": 50
  }'
```

**Required fields:**
- `claim` (string): The factual statement to verify
- `domain` (string): One of `financial`, `general`, `geographic`, `identity`, `legal`, `medical`, `scientific`, `technical`
- `budget_cents` (integer): Payment in cents. Minimum 50 ($0.50)

**Optional fields:**
- `context` (string): Additional context for the verifier
- `urgency` (string): `low`, `medium` (default), `high`, `critical`
- `callback_url` (string): Webhook URL for completion notification
- `tier` (string): `standard` (default, 1 verifier), `consensus` (3 verifiers, min $3.00), `expert_panel` (5 verifiers, min $10.00)

**Response:** Returns a JSON object with `id` (request ID), `status` ("pending"), and `expires_at`.

## Request an Empathy Review

Use this when you have a draft response to a sensitive situation and want a human to review it for tone and empathy.

```bash
curl -s -X POST "https://www.2oapi.xyz/api/v1/empathize" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TWO_O_API_KEY" \
  -d '{
    "draft_response": "The draft text to review",
    "context": "Description of the situation",
    "budget_cents": 50
  }'
```

**Required fields:**
- `draft_response` (string): The draft AI response to review
- `context` (string): The situation the user is in
- `budget_cents` (integer): Minimum 50

**Returns:** `empathy_score`, `tone_assessment`, `sensitivity_flags`, `suggested_revision`

## Request a Witness Observation

Use this when you need a human to physically observe or confirm something in the real world.

```bash
curl -s -X POST "https://www.2oapi.xyz/api/v1/witness" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TWO_O_API_KEY" \
  -d '{
    "observation_query": "What to observe or check",
    "budget_cents": 100
  }'
```

**Required fields:**
- `observation_query` (string): What the human should observe
- `budget_cents` (integer): Minimum 100 ($1.00)

**Optional fields:**
- `location_address` (string): Address for the observation
- `location_lat`, `location_lng` (number): GPS coordinates
- `photo_required` (boolean): Whether photos are needed

**Returns:** `observation`, `photo_urls`, `observed_at`

## Check Request Status

After submitting any request, poll for status using the request ID:

```bash
curl -s "https://www.2oapi.xyz/api/v1/verify/REQUEST_ID" \
  -H "Authorization: Bearer $TWO_O_API_KEY"
```

Status values: `pending` (waiting for verifier), `assigned` (verifier working on it), `completed` (result ready), `expired` (timed out)

Poll every 30-60 seconds. All three task types (verify, empathize, witness) use this same endpoint.

## Get the Result

Once status is `completed`, fetch the full result:

```bash
curl -s "https://www.2oapi.xyz/api/v1/verify/REQUEST_ID/result" \
  -H "Authorization: Bearer $TWO_O_API_KEY"
```

**Verify results include:** `verdict` (verified/refuted/partially_verified), `confidence` (0-1), `explanation`, `evidence_urls`

## Check Balance

```bash
curl -s "https://www.2oapi.xyz/api/v1/agent/balance" \
  -H "Authorization: Bearer $TWO_O_API_KEY"
```

Returns `balance_cents`, `total_spent_cents`, `total_escrowed_cents`.

## Guidelines

- Verify important claims before presenting them as fact to users
- Use empathy review before responding to sensitive situations (grief, conflict, crisis)
- Use witness for questions about real-world conditions that can't be answered from training data
- Start with `budget_cents: 50` for verify/empathize, `100` for witness
- Higher budgets and urgency attract faster responses
- The typical flow is: submit -> poll status -> get result
- Do not poll more frequently than every 30 seconds

---
name: 1lookup
description: Validate and enrich phone numbers, email addresses and IP addresses with the 1Lookup API. Phone validation, line type and carrier, HLR live network status, reverse phone (caller name), spam reputation, email deliverability and IP geolocation with proxy checks. Use when the user asks whether a number, email or IP is real, what kind of line it is, who owns it, or whether it is safe to contact.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ONELOOKUP_API_KEY
      bins:
        - curl
    primaryEnv: ONELOOKUP_API_KEY
    envVars:
      - name: ONELOOKUP_API_KEY
        required: true
        description: 1Lookup API key (starts with sk_live_). Create it in the dashboard at https://app.1lookup.io/api-keys.
    homepage: https://www.1lookup.io
---

# 1Lookup

1Lookup is a data verification and enrichment API: one key and one shared credit balance cover phone, email and IP lookups, plus company and contact data. This skill covers the lookups an agent needs most: phone validation, line type and carrier, HLR, reverse phone, spam reputation, email validation and IP lookup.

Every lookup spends credits from the user's account. API access needs a paid plan (a 7-day trial is available); a key on a free plan gets HTTP 403 `UPGRADE_REQUIRED`. Credit costs below are per lookup.

## Get an API key

1. Sign up at https://app.1lookup.io/signup (or sign in at https://app.1lookup.io).
2. Open https://app.1lookup.io/api-keys and create a key. It starts with `sk_live_`.
3. Give the key to the agent as the `ONELOOKUP_API_KEY` environment variable. Never paste it into chat, a file in a repository or a log.

```bash
export ONELOOKUP_API_KEY="sk_live_YOUR_API_KEY"
```

If `ONELOOKUP_API_KEY` is not set, stop and ask the user to create a key at the page above. Do not guess one.

## Calling the API

- Base URL: `https://app.1lookup.io/api/v1`
- Auth header on every request: `Authorization: Bearer $ONELOOKUP_API_KEY`
- Requests are `POST` with a JSON body and `Content-Type: application/json` (except `GET /account`).
- Send phone numbers in E.164 format (`+13055550175`).
- Success: `{"success": true, "data": {...}}`. Failure: `{"success": false, "error": {"message", "code", "type"}}`. Check `success` before reading `data`.
- `data.metadata.credits_used` says what the call cost and `data.metadata.credits_remaining` what is left.
- Results are cached for 7 days. Repeating a lookup you already ran within that window is normally free. Add `"bypass_cache": true` to the body only when the user wants a fresh lookup (it is charged as usual).
- A request that fails is not charged.

## Endpoints

### 1. Validate a phone number: `POST /phone` (1 credit)

Confirms the number is real and returns line type, carrier, portability and, for US and Canada numbers, reachability and Do Not Call flags. An invalid number outside the US and Canada costs nothing.

Body: `phone_number` (required, E.164).

```bash
curl -s https://app.1lookup.io/api/v1/phone \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+13055550175"}'
```

Read: `data.classification.line_type` (MOBILE, LANDLINE, VOIP, TOLL_FREE, PREMIUM, UNKNOWN), `data.classification.number_status`, `data.classification.portability_status`, the carrier name in `data.insights.raw_api_fields.network` (US and Canada) or `data.insights.carrier.name` (other countries), `data.insights.reachability.is_reachable`, `data.insights.compliance.dnc_listed`.

### 2. Line type: `POST /nt-lookup` (1 credit)

Classifies a number as mobile, landline, VoIP, toll-free or premium and says whether it qualifies for an HLR lookup. An invalid number costs nothing.

Body: `phone_number` (required, E.164).

```bash
curl -s https://app.1lookup.io/api/v1/nt-lookup \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+13055550175"}'
```

Read: `data.classification.number_type`, `data.classification.is_valid`, `data.classification.qualifies_for_hlr_lookup`.

### 3. HLR lookup: `POST /hlr-lookup` (5 credits)

Live subscriber status, roaming state and current carrier of a mobile number, any country. A number the network reports as not assigned (`INVALID_MSISDN`) is not charged. Use it after line type says the number is mobile, not as a first check.

Body: `phone_number` (required, mobile number in E.164).

```bash
curl -s https://app.1lookup.io/api/v1/hlr-lookup \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+447700900123"}'
```

Read: `data.classification.connectivity_status` (CONNECTED, ABSENT, INVALID_MSISDN, UNDETERMINED), `data.classification.is_valid`, `data.classification.is_ported`, `data.classification.is_roaming`, `data.insights.hlr_result.current_carrier`. `data.insights.hlr_result.data_source` is `LIVE_HLR` for a live network query and `MNP_DB` for the portability database (most US and Canada numbers), which shows the number is assigned, not that the handset is on.

### 4. Reverse phone lookup: `POST /reverse-phone-lookup` (10 or 25 credits)

The person or business behind a US phone number. Nothing is charged when there is no match.

Body: `phone_number` (required, US number), `lookup_source` (optional): `standard` reads caller ID records and gives the caller name, 10 credits (default); `premium` searches full owner records, 25 credits. Any other value is refused with 400 `INVALID_INPUT`.

```bash
curl -s https://app.1lookup.io/api/v1/reverse-phone-lookup \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+13055550175", "lookup_source": "standard"}'
```

Read: `data.classification.matched`, `data.classification.primary_name`, and for premium `data.insights.reverse_lookup_result` (address, company, phone type). Treat the result as personal data: use it only for the purpose the user stated.

### 5. Spam reputation: `POST /phone-spam` (1 credit)

Spam reputation (positive or negative) and robocall status (allowed or blocked) of a phone number, with a rule-based spam score, risk level and suggested action. If the source has no rating at all the call fails with 503 `UPSTREAM_NO_RESULT` and nothing is charged.

Body: `phone_number` (required).

```bash
curl -s https://app.1lookup.io/api/v1/phone-spam \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+13055550175"}'
```

Read: `data.classification.caller_type`, `data.classification.threat_category`, `data.risk_assessment.risk_level` (`UNKNOWN` when there is no rating), `data.recommendations.primary_action`.

### 6. Validate an email address: `POST /email` (1 credit)

Checks that the mailbox exists and is deliverable, and flags disposable, role-based, free-provider and catch-all addresses.

Body: `email` (required).

```bash
curl -s https://app.1lookup.io/api/v1/email \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "ada@example.com"}'
```

Read: `data.classification.deliverability_status` (DELIVERABLE, UNDELIVERABLE, RISKY, TEMPORARY, UNKNOWN), `data.classification.email_type`, `data.risk_assessment.risk_factors` (for example `ROLE_BASED_EMAIL`), `data.insights.deliverability.factors.catch_all`.

### 7. IP lookup: `POST /ip` (1 credit)

Geolocation, connection type, proxy, Tor and datacenter flags (and a VPN service type when the organization name says VPN), and for a public IPv4 address a check against 3 public spam blocklists. The fraud score and risk level are rule-based estimates worked out from the address's flags, not measurements. Fields with no source are null.

Body: `ip` (required, IPv4 or IPv6).

```bash
curl -s https://app.1lookup.io/api/v1/ip \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ip": "8.8.8.8"}'
```

Read: `data.insights.location.country_code`, `data.insights.location.city`, `data.insights.network.isp`, `data.classification.connection_type`, `data.insights.network_intelligence.is_datacenter`, `data.insights.security.tor_exit_node`, `data.insights.security.blocklists`, `data.risk_assessment.risk_level`.

### 8. Account and credit balance: `GET /account` (free)

Spends no credits. Call it before a large job to check the balance.

```bash
curl -s https://app.1lookup.io/api/v1/account \
  -H "Authorization: Bearer $ONELOOKUP_API_KEY"
```

Read: `data.tokens.total_available` (credits left now), `data.subscription.plan.name`, `data.subscription.is_trial`.

## Which endpoint to use

| The user asks | Call |
|---|---|
| Is this phone number real? What kind of line is it? Which carrier? | `/phone` |
| Mobile, landline or VoIP, nothing else | `/nt-lookup` |
| Is this mobile number switched on or roaming right now? | `/hlr-lookup` |
| Who owns this US number? | `/reverse-phone-lookup` |
| Is this number a spam or robocall number? | `/phone-spam` |
| Will an email to this address arrive? | `/email` |
| Where is this IP? Is it a proxy or datacenter? | `/ip` |
| How many credits are left? | `/account` |

Also available over the same key and base URL: `POST /mnp-lookup` (the network a number was ported to, 3 credits), `POST /phone-scrub` (Do Not Call and litigator check, 10 credits a number, nothing when there is no match) and many company, contact and SEO data products. The full list, with bodies and responses, is in the OpenAPI description at https://www.1lookup.io/openapi.json and the API docs at https://app.1lookup.io/api. Pricing for every product is at https://www.1lookup.io/pricing.

## Rules for the agent

- Every lookup costs credits. Before running more than a few lookups in a row, tell the user how many lookups and the credit total (count times the cost above) and wait for a yes.
- Do not loop or retry a paid call to "double-check" a result. A repeat of the same lookup within 7 days is served from the cache.
- Start with the cheapest call that answers the question. Use `/hlr-lookup` and the premium reverse lookup only when the user needs what they add.
- Never print, echo or store the API key. Do not put it in a command that is logged or in a file inside a repository.
- Do not claim certainty the data does not give. Fraud scores, risk levels and spam scores are rule-based estimates, and fields can be null.
- Reverse phone and email results can be personal data. Use them only for the stated purpose and do not store them longer than needed.

## Errors

| Status | Code | What to do |
|---|---|---|
| 400 | `INVALID_INPUT`, `MISSING_FIELD`, `INVALID_REQUEST` | Fix the body. Phone numbers in E.164. Nothing is charged. |
| 401 | `UNAUTHORIZED` | The key is missing, wrong or revoked. Ask the user to check `ONELOOKUP_API_KEY`. |
| 402 | `INSUFFICIENT_CREDITS` | Out of credits. Tell the user, link https://www.1lookup.io/pricing, and stop. |
| 403 | `UPGRADE_REQUIRED` | The account has no paid plan. Upgrade at https://app.1lookup.io/billing?tab=plan. |
| 429 | `RATE_LIMIT_EXCEEDED` | Wait the number of seconds in the `Retry-After` header, then retry once. |
| 503 | `SERVICE_UNAVAILABLE`, `SERVICE_BUSY` | Wait `Retry-After` seconds and retry. Nothing is charged. |

Every response has an `X-Request-Id` header. Quote it when contacting support at https://www.1lookup.io/contact.

## MCP server (no API key)

Instead of REST, an agent can connect to the hosted 1Lookup MCP server:

- URL: `https://app.1lookup.io/api/mcp`
- Transport: streamable HTTP (SSE is disabled)
- Auth: OAuth 2.1 with a browser consent screen. No API key.
- Tools (5): `validate_phone`, `verify_email`, `ip_lookup`, `bulk_verify`, `get_account`
- Cost: the same credits as REST (one credit per phone, email or IP lookup, one credit per record for `bulk_verify`). `get_account` is free. There is no separate MCP fee.
- Needs a paid plan, like the REST API.
- Server card: https://www.1lookup.io/.well-known/mcp/server-card.json
- Setup pages: https://www.1lookup.io/mcp/claude and https://www.1lookup.io/mcp/cursor. Any client that supports remote MCP over streamable HTTP can add the same URL. Auth reference: https://www.1lookup.io/mcp/oauth.

The MCP server exposes only those five tools. Everything else, including HLR and reverse phone lookup, is available over REST at `https://app.1lookup.io/api/v1`.

## Links

- Website: https://www.1lookup.io
- API docs: https://app.1lookup.io/api
- OpenAPI description: https://www.1lookup.io/openapi.json
- Machine-readable overview: https://www.1lookup.io/llms.txt
- Pricing: https://www.1lookup.io/pricing

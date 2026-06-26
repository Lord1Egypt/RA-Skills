# FlashRev AI Enrich API Contract

The wire format this CLI relies on. Anything beyond what is documented here is FlashRev internal and may change without notice.

## Base URL & auth

| Item | Value |
|---|---|
| Base URL | `https://open-ai-api.flashlabs.ai` |
| Auth header | `X-API-Key: <private app key>` |
| Key issuance | https://info.flashlabs.ai/settings/privateApps |
| Path prefix | All CLI-facing routes share the `/flashrev/...` prefix |

The API key is exchanged for an authenticated session by the FlashRev gateway. The CLI never sees or handles internal tokens.

## Endpoints used by CLI

### 1. Token balance — `GET /flashrev/api/v2/oauth/me`

Response:
```json
{
  "code": 200,
  "data": {
    "companyId": 1000001,
    "newCreditFlag": "Y",
    "limit": {
      "tokenTotal": 1121000,
      "tokenCost": 917206.5,
      "tokenCategoryRemain": { "SUBSCRIPTION": 0, "GIFT": 0, "ADDON": 289974 }
    },
    "vip": { "packageName": "...", "...": "..." }
  }
}
```

CLI computes `remaining = tokenTotal - tokenCost`.

### 2. Token history — `POST /flashrev/api/v2/commodity/token/transaction/list`

Request body:
```json
{ "page": 1, "pageSize": 100, "transactionType": 2 }
```

`transactionType: 2` = consumption (1 = top-up).

Response:
```json
{
  "code": 200,
  "data": {
    "list": [
      { "createdAt": "2026-05-29 06:59:56", "featId": "unlock_contact",
        "featName": "Verify Email Address", "tokenAmount": 1, "unit": "Run",
        "quantity": 1, "transactionType": 2 }
    ],
    "total": 100, "page": 1, "pageSize": 100
  }
}
```

The endpoint does not currently accept date filters; the CLI paginates and filters locally by `createdAt`. CLI cap: 20 pages × 100 = 2000 records.

### 3. Capability registry — `GET /flashrev/api/v1/enrich/configs`

Returns the active capability list with pricing and shape.

```json
{
  "code": 200,
  "data": [
    {
      "funcName": "enrich_email",
      "displayName": "Enrich Person -> Get Emails",
      "featId": "unlock_contact",
      "unitPriceToken": 2,
      "concurrency": 10,
      "inputColumn": [
        { "key": "first_name", "name": "First Name" },
        { "key": "last_name",  "name": "Last Name" }
      ],
      "outputColumn": ["verified_business_email", "all_verified_business_emails", "..."],
      "rules": [
        ["first_name", "last_name", "company_name"],
        ["person_linkedin_url"],
        ["email"]
      ]
    }
  ]
}
```

### 4. Enrich — `POST /flashrev/api/v1/enrich/run`

Per-row enrichment, synchronous.

Request body (snake_case on the wire):
```json
{
  "func_name": "enrich_email",
  "input": {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "company_name": "Acme"
  },
  "row_id": "row-42"
}
```

`row_id` is optional and used by the CLI for tracing only.

Response (success):
```json
{
  "code": 200,
  "msg": "OK",
  "data": {
    "code": 200,
    "msg": "Successful",
    "data": {
      "verified_business_email": "ada@acme.com",
      "all_verified_business_emails": ["ada@acme.com"],
      "verified_personal_email": ""
    },
    "cost": { "tokens": 2, "cached": false }
  }
}
```

The response uses a nested `data` wrapper; the CLI's `normalizeEnrichResponse` handles both flat and nested shapes.

`cost.tokens` may be slightly inaccurate under high concurrency; the values returned by `token/transaction/list` are always exact.

### 5. Error codes

HTTP-level (gateway / transport):

| Code | Meaning |
|---|---|
| 401 | Invalid or revoked `X-API-Key` |
| 402 | Insufficient tokens |
| 429 | Rate limit exceeded (CLI auto-retries with exponential backoff) |
| 503 | Service temporarily unavailable |
| 504 | Upstream timeout |

Business-level (HTTP 200 but inner `code != 200`):

| Inner code | Meaning |
|---|---|
| 200 + `data` populated | Real enrichment, charged at `unitPriceToken` |
| 200 + `data` empty / requested fields blank | No data for this lead; CLI marks `no_data`, not charged |
| 422 | Input validation failed (e.g., missing required input combo) |
| 4xx other | Request rejected |

## Deduction semantics

- **Pre-check**: The balance is checked before any downstream call. Insufficient → `402` immediately, no charge.
- **Rate limit**: A per-`funcName` quota is enforced server-side. Overflow → `429`; the CLI retries with backoff.
- **Charge on success only**: A row is billed only when the response carries real business data. Empty / 4xx / 5xx responses are not billed.
- **Dedup**: Contact-unlock capabilities (`enrich_email`, `enrich_phone`) consult an unlock cache. Repeat unlocks of the same person return cached data at 0 tokens (`cost.cached: true`).

## customer_api

`customer_api` is a special capability whose backend route is empty. The CLI fetches the user-provided URL locally and parses the response. Token cost is always 0. Use it to mix third-party data sources into the same enrichment workflow.

### Security guardrails

Because `customer_api` issues HTTP requests from the user's machine with row-derived URL / headers / body, it is the only capability that can both reach **internal infrastructure** and **exfiltrate CSV lead data to a third-party endpoint**. The CLI applies a hard guardrail before any network IO:

- **Scheme allowlist** — only `http://` and `https://` are accepted. `file://`, `gopher://`, `data:`, `javascript:` etc. fail with HTTP 400.
- **Host blocklist (default ON)** — the URL is rejected (HTTP 403) when the hostname is `localhost` / `0.0.0.0`, or an IP literal inside `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16` (link-local, incl. AWS/GCP/Azure metadata `169.254.169.254`), `0.0.0.0/8`, multicast/reserved `224.0.0.0/4`, IPv6 `::`, `::1`, `fe80::/10`, `fc00::/7`, or IPv4-mapped IPv6 (`::ffff:a.b.c.d`) where the embedded v4 hits any of the above. Pass `--allow-internal-targets` per-run to bypass — intended for deliberate local testing only.
- **Residual risk** — the CLI does not resolve DNS, so a public hostname that later resolves to a private IP (DNS rebinding) is **not** caught here. Operators running this CLI in sensitive environments should pin egress via OS firewall / network ACLs in addition to this guardrail.

The guardrail addresses SSRF + cloud-metadata exfiltration. Lead-data exfiltration via an attacker-controlled **public** URL is *not* blocked by code — that decision is policy. The skill documentation directs agents to never auto-fill `url` from prompt text, never map credentials or unrelated PII into `headers` / `body`, and to require human confirmation of the destination domain before a live `run`.

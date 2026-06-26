# Register Service Guided Intake

Use this reference when preparing `POST /admin/gateway/services`.

The goal is to ask focused questions, assemble camelCase registration JSON, confirm it with the user, then generate a signed curl. Do not register directly from the bundled example.

## Question Flow

### 1. Platform Environment

First check local environment:

```bash
node {baseDir}/scripts/build-service-request.mjs env-check --operation register
```

If `AICADE_API_KEY` exists locally, use it and do not ask the user to confirm it.

If `AICADE_API_SECRET_KEY` exists locally, use it and do not ask the user to confirm it.

Ask only for missing values:

- missing `AICADE_API_KEY`
- missing `AICADE_API_SECRET_KEY`

Then confirm the default service-management base URL the first time:

```text
The default service-management base URL is https://aicadegalaxy.com/agent. Should I use this URL?
```

If the user says no, ask for the actual base URL and reuse it for this session.

### 2. Service Identity

Ask for:

- `serviceId`: lowercase letters, digits, hyphens, length 3-64
- `serviceName`: display name
- `description`: optional
- `tags`: optional list

### 3. Endpoint And Gateway Route

Ask for:

- `endpointUrl`: upstream API URL
- `requestMethod`: upstream method, such as `GET` or `POST`
- `routePath`: gateway route, must start with `/`; add `/` if user omits it
- `stripPrefix`: default `0`, range `0-10`
- `routeOrder`: default `0`
- `timeoutMs`: default `30000`, range `1000-300000`
- `enabled`: default `true`

### 4. Outbound Auth

Ask which `authType` to use:

- `NONE`
- `API_KEY`
- `BEARER_TOKEN`
- `BASIC_AUTH`
- `OAUTH2`

Then ask only for the matching `outboundAuth`.

For sensitive values, prefer placeholders such as `${UPSTREAM_API_KEY}` unless the user intentionally provides real secrets.

### 5. Input And Output Schemas

Ask for:

- expected request parameters
- required fields
- response fields

Generate JSON Schema-compatible `inputSchema` and `outputSchema`.

If the user only describes fields in prose, convert them into schemas and ask for confirmation.

### 6. Billing

Ask for billing mode:

- `FREE`
- `PER_REQUEST`
- `PER_TOKEN`
- `SUBSCRIPTION`

Then ask follow-up details:

- `FREE`: `currency` can be empty, `pricePerRequest` can be `0`
- `PER_REQUEST`: `currency`, `pricePerRequest`
- `PER_TOKEN`: `currency`, `promptPricePer1k`, `completionPricePer1k`
- `SUBSCRIPTION`: `currency`, `subscriptionPeriod`, `subscriptionPrice`, included quota

Always confirm:

- `flowType`, usually `INCOME`
- `fallbackStrategy`, such as `REJECT`, `OVERDRAFT`, or `DEGRADE`
- limits such as daily/monthly requests or token caps when needed

### 7. Rate Limits

Ask whether rate limits are needed.

Common prompts:

- service-level QPS/RPM/RPD
- user-level RPM/RPD
- IP whitelist or blacklist
- `maxTokensPerReq` for LLM services

If no rate limits are required, set `rateLimits` to `[]`.

### 8. Final Confirmation

Show the assembled JSON and ask:

```text
Here is the assembled service registration JSON. Please confirm whether I can use it to generate the final signed curl. If billing, endpoint, auth, or schemas need changes, I will update the JSON first.
```

Only after confirmation should the final signed curl be generated.

Before generating register/update curl, verify:

- `AICADE_API_KEY` is available and maps to `X-API-Key`
- `AICADE_API_SECRET_KEY` is available and maps to `X-Signature`
- base URL has been confirmed

## Minimum Final Output

The final answer or output file should include:

- confirmed registration JSON
- generated signed curl
- validation checklist
- troubleshooting note: if the API returns `401`, the API key or signature secret is wrong
- note that the script only generated a request and did not call the remote API unless the user explicitly requested execution

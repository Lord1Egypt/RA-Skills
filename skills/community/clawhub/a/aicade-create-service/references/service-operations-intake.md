# Service Operations Guided Intake

Use this reference for service detail queries and service disable operations.

These operations are simpler than registration, but they are still question-driven. Do not generate curl until the user confirms the inputs.

## Shared Setup

First check local environment:

```bash
node {baseDir}/scripts/build-service-request.mjs env-check --operation detail
node {baseDir}/scripts/build-service-request.mjs env-check --operation disable
```

If `AICADE_API_KEY` exists locally, use it and do not ask the user to confirm it.

If `AICADE_API_SECRET_KEY` exists locally, use it and do not ask the user to confirm it.

Ask only for missing values:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`

Confirm the default service-management base URL the first time:

```text
The default service-management base URL is https://aicadegalaxy.com/agent. Should I use this URL?
```

If the user says no, ask for the actual base URL and reuse it for this session.

## Query Service Detail

Operation:

- `GET /admin/gateway/services/{serviceId}`

Ask:

- Which `serviceId` should be queried?

Confirm:

```text
I will query the service detail:
- GET /admin/gateway/services/{serviceId}
- Automatically generate X-Client-Time, X-Nonce, X-Content-MD5, and X-Signature
Please confirm whether I should generate the signed curl.
```

Only then generate:

```bash
node {baseDir}/scripts/build-service-request.mjs detail \
  --service-id {serviceId} \
  --base-url {confirmedBaseUrl}
```

## Disable Service

Operation:

- `PATCH /admin/gateway/services/{serviceId}/status?enabled=false`

Ask:

- Which `serviceId` should be disabled?

Do not ask for operator.

Confirm:

```text
I will disable the service:
- PATCH /admin/gateway/services/{serviceId}/status?enabled=false
- Automatically generate X-Client-Time, X-Nonce, X-Content-MD5, and X-Signature
Please confirm whether I should generate the signed curl.
```

Only then generate:

```bash
node {baseDir}/scripts/build-service-request.mjs disable \
  --service-id {serviceId} \
  --base-url {confirmedBaseUrl}
```

## Minimum Final Output

The final answer or output file should include:

- operation name
- confirmed inputs
- generated signed curl
- expected response shape
- troubleshooting note: if the API returns `401`, the API key or signature secret is wrong
- note that no remote API call was sent unless explicitly requested

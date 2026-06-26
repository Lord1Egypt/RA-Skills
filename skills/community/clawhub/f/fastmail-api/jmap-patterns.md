# JMAP Patterns — Fastmail API

## Session Discovery First

Use the session endpoint once per execution context to discover:
- `apiUrl` for method calls
- `downloadUrl` and `uploadUrl` if needed
- `primaryAccounts` for each capability
- Supported capabilities available to the token

```bash
curl -sS https://api.fastmail.com/jmap/session \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" | jq
```

## Method Call Envelope

Use a single JSON envelope with `using` and `methodCalls`:

```json
{
  "using": [
    "urn:ietf:params:jmap:core",
    "urn:ietf:params:jmap:mail",
    "urn:ietf:params:jmap:submission"
  ],
  "methodCalls": [
    ["Mailbox/get", {"accountId": "u123", "ids": null}, "c1"]
  ]
}
```

## Response Handling Checklist

After each write operation:
1. Parse `methodResponses` in order.
2. Check for method-level `error` responses.
3. Inspect `notCreated`, `notUpdated`, and `notDestroyed` maps.
4. Confirm state with targeted read calls.

## Retry Discipline

- Retry only transient failures (timeouts, temporary server errors).
- Do not auto-retry on validation errors; fix payload first.
- Keep retries bounded and log every retry decision.

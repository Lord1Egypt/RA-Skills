> ## Documentation Index
> Fetch the complete documentation index at: https://docs.useanima.sh/llms.txt
> Use this file to discover all available pages before exploring further.

# Server-Side Credential Use

> Let agents make authenticated API calls with vault credentials that never leave Anima — the secret is injected server-side and never returned.

# Server-Side Credential Use

The strongest way for an agent to use a secret is to never hold it at all. With server-side use, the agent asks Anima to make the outbound HTTPS call; Anima decrypts the credential, injects it into the request **on the server**, and returns only the upstream response. The plaintext never reaches the agent's host, its context, or its logs.

```text theme={null}
Agent                Anima API                  Upstream (api.stripe.com)
  │  use(cred, req)      │                              │
  ├─────────────────────>│  decrypt + inject key        │
  │                      ├─────────────────────────────>│
  │                      │            response          │
  │   status/body only   │<─────────────────────────────┤
  │<─────────────────────┤  (secrets scrubbed)          │
```

Compare this with `anima vault exec` / `anima vault proxy`, which inject locally: there the secret reaches your machine's process (but still never the LLM). Server-side use removes even that.

## Configure the credential

A credential is only broker-usable for hosts you bind it to. **Fail-closed:** with no allowed hosts, every call is refused.

```bash theme={null}
anima vault store --type api_key --name "Stripe production" \
  --provider stripe --key sk_live_... \
  --allowed-host api.stripe.com \
  --reveal-policy brokered
```

For `api_key` credentials you can also set `authHeader` (default `Authorization`) and `authScheme` (default `Bearer `; empty for raw-key headers like `x-api-key`). `login` credentials use their URIs as the allowlist; `oauth_token` credentials have their own `allowedHosts` and are always created with the `brokered` reveal policy.

Changing the allowlist later requires org-admin (master) access — an agent that could broaden it could redirect the secret to a host it controls.

## Make a brokered call

<CodeGroup>
  ```bash CLI theme={null}
  anima vault use --credential cred_abc \
    --method POST --url https://api.stripe.com/v1/charges \
    -H "X-Idempotency: order-42" --body '{"amount":1000}'
  ```

  ```ts TypeScript theme={null}
  const res = await anima.vault.useCredential("cred_abc", {
    method: "POST",
    url: "https://api.stripe.com/v1/charges",
    headers: { "X-Idempotency": "order-42" },
    body: JSON.stringify({ amount: 1000 }),
  });
  console.log(res.status, res.body);
  ```

  ```python Python theme={null}
  res = anima.vault.use_credential(
      "cred_abc",
      method="POST",
      url="https://api.stripe.com/v1/charges",
      headers={"X-Idempotency": "order-42"},
      body='{"amount": 1000}',
  )
  print(res["status"], res["body"])
  ```

  ```json MCP theme={null}
  // tool: vault_credential_use
  {
    "id": "cred_abc",
    "method": "POST",
    "url": "https://api.stripe.com/v1/charges",
    "headers": { "X-Idempotency": "order-42" },
    "body": "{\"amount\":1000}"
  }
  ```
</CodeGroup>

The response carries `status`, `headers`, `body` (size-capped, `truncated` flag), with any occurrence of the credential scrubbed. Any `Authorization` header the caller supplies is discarded and replaced with the real credential.

## Guardrails

* **Host allowlist + SSRF guard** — https-only, exact host match, DNS-resolved and pinned, private/link-local/metadata ranges blocked, no redirect following.
* **Access control** — the caller needs to own the credential or hold a `USE`-level share. Scoped API keys need the `vault:use` scope. Brokered `POST`/`PUT`/`PATCH`/`DELETE` calls run under the agent's *write* vault policy.
* **Rate limits** — per-credential limits from the stored `rateLimit` config, with a conservative default so no credential can be fired unbounded.
* **Audit** — every call is recorded as `broker_use` (method, host, status — never the secret); refused calls are recorded as `broker_use_denied` with the reason, so a probing agent is visible in the [access log](/vault).

## When to use which mechanism

| Mechanism                     | Secret reaches            | Best for                       |
| ----------------------------- | ------------------------- | ------------------------------ |
| Server-side use (`vault use`) | Nothing outside Anima     | HTTP APIs, strongest isolation |
| Browser autofill (extension)  | The web page's form       | Logins on websites             |
| `vault exec` / `vault proxy`  | A local process you spawn | CLIs, SDKs, non-HTTP tools     |

All three keep the secret out of the model's context. See [Vault](/vault) for the full model.

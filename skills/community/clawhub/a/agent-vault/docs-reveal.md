> ## Documentation Index
> Fetch the complete documentation index at: https://docs.useanima.sh/llms.txt
> Use this file to discover all available pages before exploring further.

# Reveal Policy

> Control whether a credential's plaintext can ever be read back — 'brokered' means use-only, for everyone, forever.

# Reveal Policy

Anima separates **using** a secret from **seeing** it. Agents can always *use* credentials — through the [server-side broker](/vault-server-side-use), browser autofill, or local injection — but reading the plaintext back is governed per credential by its reveal policy:

| Policy     | Plaintext readable?                                 | Recovery         |
| ---------- | --------------------------------------------------- | ---------------- |
| `standard` | Only by org admins (console / master key), audited  | Reveal or rotate |
| `brokered` | **Never — by anyone, including the org master key** | Rotation only    |

Defaults when you don't specify one: `oauth_token` credentials are always `brokered`; logins created by an agent key default to `brokered`; everything else follows the org default (`standard` unless changed).

```bash theme={null}
anima vault store --type api_key --name "Stripe" \
  --provider stripe --key sk_live_... \
  --allowed-host api.stripe.com \
  --reveal-policy brokered
```

Upgrading `standard → brokered` needs update access; downgrading `brokered → standard` re-opens the reveal path, so it is master-only and writes a `reveal_policy_downgraded` audit entry.

## What agents can never do

On every agent surface — MCP tools, SDKs with agent keys, the API — reads return **masked** data (`sk_****1234`), and there is no reveal parameter an agent can pass. The one plaintext endpoint, `exchangeTokenForInjection`, exists for trusted *injectors* (the CLI's local-injection commands) and is hard-gated: the caller must present a master key or a key carrying the `vault:inject` scope. A plain agent key gets `403`. This is what makes "the agent can use it but can never see it" a property of the platform rather than a convention.

## Editing without seeing

Because reads are masked, updates use **patch semantics** for secret-bearing blocks: fields you omit keep their stored values, and a masked echo (`sk_****1234`) of a secret field counts as unchanged. That means you can edit `allowedHosts` on an API key — from the console, SDKs, or CLI — without ever resending or clobbering the key itself. Sending a genuinely new value rotates it.

```ts theme={null}
// Adds a host; the stored key is untouched.
await anima.vault.updateCredential("cred_abc", {
  apiKey: { allowedHosts: ["api.stripe.com", "files.stripe.com"] },
});
```

## Human reveal (standard policy only)

Org admins can reveal a `standard` credential in the console (the Copy action) or via the API with a master key (`reveal: true`). Every reveal is written to the access log as `access_reveal` with the actor — the [access log](/vault) flags plaintext reveals so compliance can review who looked at what. For `brokered` credentials the console offers rotation instead; there is nothing to reveal.

**Step-up freshness.** Console reveals additionally require the session to have verified its first factor recently (default: within 10 minutes; `VAULT_REVEAL_FRESHNESS_MINUTES`, `0` disables). A stale browser session — the thing session theft steals — gets a `403` and the console pops Clerk's re-verification modal, then retries automatically; denied attempts are logged as `access_reveal_denied`. Downgrading a credential from `brokered` to `standard` demands the same freshness, since it re-opens the reveal path. Raw master API keys are bearer secrets, not sessions, so they are unaffected — they remain the automation escape hatch.

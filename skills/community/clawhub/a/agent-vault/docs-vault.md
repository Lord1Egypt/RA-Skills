> ## Documentation Index
> Fetch the complete documentation index at: https://docs.useanima.sh/llms.txt
> Use this file to discover all available pages before exploring further.

# Vault

> Store, share, and inject encrypted credentials for your AI agents — with a hard guarantee that the LLM never sees raw secrets.

# Vault

The Anima Vault provides encrypted credential storage for AI agents, with a critical security guarantee: **the LLM never sees raw secrets**. Each agent gets its own isolated, per-agent-encrypted vault for logins, API keys, payment cards, and identity data. Agents reference credentials through opaque tokens, and the CLI or browser extension performs the last-mile substitution at execution time.

## Overview

Agents often need to authenticate with external services — CRMs, booking platforms, merchant sites. The vault stores these credentials securely and makes them available to the agent at runtime, without exposing secrets in code, environment variables, or the model's context.

The core idea:

```text theme={null}
Agent (LLM)        → composes a command containing a vtk_ token
CLI / extension    → detects the token, exchanges it for the credential, substitutes
Execution          → the real secret is used in the request
Output             → matching secrets are redacted before returning to the LLM
```

## Use, never see

Every agent surface reads credentials **masked**; there is no reveal path an agent can call. Agents exercise secrets through three mechanisms, all of which keep the plaintext out of the model:

* **[Server-side use](/vault-server-side-use)** — Anima makes the outbound call and injects the credential on the server; the secret never reaches the agent's host.
* **Browser autofill** — the [extension](/extension-connect) fills logins directly into web forms.
* **Local injection** — `anima vault exec` / `anima vault proxy` substitute secrets into a local process at the last moment (see below).

Whether a *human* can ever read the plaintext back is governed per credential by its **[reveal policy](/vault-reveal-policy)** — `brokered` credentials are use-only for everyone, forever. And when an agent needs a secret it doesn't have, it asks a human through **[credential requests](/vault-credential-requests)** instead of chat.

## Provisioning

Before an agent can store credentials, its vault must be provisioned:

```python theme={null}
# Python
anima.vault.provision(agent_id=agent.id)
```

```ts theme={null}
// TypeScript
await anima.vault.provision({ agentId: agent.id });
```

From the CLI:

```bash theme={null}
anima vault provision --agent <agent-id>
anima vault status --agent <agent-id>
```

## Credential Types

| Type          | Primary secret | Use case                                                         |
| ------------- | -------------- | ---------------------------------------------------------------- |
| `login`       | password       | Website logins, SSH credentials (username, password, URIs, TOTP) |
| `api_key`     | key            | API keys (e.g. provider keys)                                    |
| `oauth_token` | accessToken    | OAuth integrations                                               |
| `certificate` | privateKey     | TLS / mTLS certificates                                          |
| `secure_note` | notes          | Free-form secret text                                            |
| `card`        | number         | Payment card details                                             |
| `identity`    | —              | Personal / business identity data (not auto-injectable)          |

## CRUD Operations

### Create a credential

```python theme={null}
# Python
credential = anima.vault.create_credential(
    agent_id=agent.id,
    type="login",
    name="CRM Login",
    login={
        "username": "bot@company.com",
        "password": "s3cur3-p4ssw0rd",
        "uris": [{"uri": "https://crm.company.com"}],
    },
)
```

```ts theme={null}
// TypeScript
const credential = await anima.vault.createCredential({
  agentId: agent.id,
  type: "login",
  name: "CRM Login",
  login: {
    username: "bot@company.com",
    password: "s3cur3-p4ssw0rd",
    uris: [{ uri: "https://crm.company.com" }],
  },
});
```

### Create a login with a generated password

For account provisioning, don't supply a password at all — ask the vault to
generate one server-side in the same call. The password is created inside the
vault, stored with the credential, and **never returned**: the response
carries only the credential ref with masked fields. Your code (and, for MCP
agents, the model's context) never sees the secret.

```python theme={null}
# Python
credential = anima.vault.create_credential(
    agent_id=agent.id,
    type="login",
    name="Acme Portal",
    login={"username": "bot@company.com", "uris": [{"uri": "https://acme.io/login"}]},
    generate_password={},  # server defaults: 24 chars, all character classes
)
print(credential.id)              # store this ref
print(credential.login.password)  # "****" — the plaintext stays in the vault
```

```ts theme={null}
// TypeScript
const credential = await anima.vault.createCredential({
  agentId: agent.id,
  type: "login",
  name: "Acme Portal",
  login: { username: "bot@company.com", uris: [{ uri: "https://acme.io/login" }] },
  generatePassword: { length: 32, special: false }, // tune per site policy
});
```

Generation options: `length` (8–128, default 24) and the character-class
toggles `uppercase` / `lowercase` / `number` / `special` (all default `true`).
`generatePassword` is only valid for `login` credentials and is mutually
exclusive with `login.password`.

At fill time — for example when the Anima Chrome extension signs in to
provision an account — the agent mints a single-use, audit-logged vault token
(`POST /vault/token`, scope `autofill`) and exchanges it for the credential
(see [Ephemeral Tokens](#ephemeral-tokens) below). The plaintext is revealed
exactly once, to the component that needs it.

### Retrieve a credential

```python theme={null}
creds = anima.vault.get_credential(
    agent_id=agent.id,
    credential_id=credential.id,
)
print(creds.username, creds.password)
```

### List and search

```python theme={null}
all_creds = anima.vault.list(agent_id=agent.id)
results = anima.vault.search(agent_id=agent.id, query="crm")
```

### Update and delete

```python theme={null}
anima.vault.update_credential(
    agent_id=agent.id,
    credential_id=credential.id,
    password="new-p4ssw0rd",
)

anima.vault.delete_credential(
    agent_id=agent.id,
    credential_id=credential.id,
)
```

### REST endpoints

| Method   | Path                                   | Description                                      |
| -------- | -------------------------------------- | ------------------------------------------------ |
| `GET`    | `/vault/credentials?agentId=`          | List all credentials                             |
| `GET`    | `/vault/credentials/{id}?agentId=`     | Get a single credential                          |
| `POST`   | `/vault/credentials`                   | Create a credential                              |
| `PUT`    | `/vault/credentials/{id}`              | Update a credential                              |
| `DELETE` | `/vault/credentials/{id}`              | Delete a credential (`agentId` in the JSON body) |
| `GET`    | `/vault/search?agentId=&search=&type=` | Search credentials                               |
| `POST`   | `/vault/generate-password`             | Generate a random password                       |
| `GET`    | `/vault/totp/{id}?agentId=`            | Get the current TOTP code                        |
| `GET`    | `/vault/status?agentId=`               | Vault connection status                          |
| `POST`   | `/vault/sync`                          | Trigger a vault sync                             |

## TOTP Support

For credentials with TOTP (Time-based One-Time Password) configured:

```python theme={null}
totp = anima.vault.get_totp(
    agent_id=agent.id,
    credential_id=credential.id,
)
print(totp.code)  # Current 6-digit code
```

## Password Generation

For agent flows, prefer the atomic
[create-with-generated-password](#create-a-login-with-a-generated-password)
above — it generates and stores the password in one call and never returns
the plaintext.

The standalone generator remains available for interactive use. Note that it
**returns the generated password to the caller**, so it should not be used in
flows where the secret must stay inside the vault:

```ts theme={null}
// TypeScript
const { password } = await anima.vault.generatePassword({
  length: 24,
  uppercase: true,
  lowercase: true,
  number: true,
  special: true,
});
```

## Credential Sharing

Share a credential from one agent to another, with a scoped permission and optional expiry. Sharing is one credential to one target agent at a time.

| Method | Path                                | Description                           |
| ------ | ----------------------------------- | ------------------------------------- |
| `POST` | `/vault/share`                      | Share a credential with another agent |
| `GET`  | `/vault/shares?agentId=&direction=` | List shares (granted or received)     |
| `POST` | `/vault/share/revoke`               | Revoke a share                        |

`POST /vault/share` takes `credentialId`, `sourceAgentId`, `targetAgentId`, a `permission`, and either `expiresAt` or `expiresInSeconds`. Revoke with a `shareId`.

**Permissions:**

| Permission | Grants                                                                   |
| ---------- | ------------------------------------------------------------------------ |
| `READ`     | View credential metadata only                                            |
| `USE`      | Auto-fill the credential in the CLI or browser, without seeing its value |
| `MANAGE`   | Full read/update/delete access to the shared credential                  |

## Ephemeral Tokens

An ephemeral token is a short-lived, single-use handle to a credential. The agent puts the token in a command; the CLI or extension exchanges it for the real value at the moment of execution.

| Method | Path                    | Description                         |
| ------ | ----------------------- | ----------------------------------- |
| `POST` | `/vault/token`          | Create an ephemeral token           |
| `POST` | `/vault/token/exchange` | Exchange a token for its credential |
| `POST` | `/vault/token/revoke`   | Revoke all tokens for a credential  |

`POST /vault/token` takes `credentialId`, a `scope`, and an optional `ttlSeconds` (and `agentId` / `taskId`). The token value (`vtk_<hex>`) is returned **only at creation time**.

**Scopes:**

| Scope      | Purpose                                  |
| ---------- | ---------------------------------------- |
| `autofill` | CLI and browser-extension auto-fill      |
| `proxy`    | Delegated access through the local proxy |
| `export`   | One-time credential reveal               |

**Token security:**

* Tokens use the `vtk_` prefix with 32 bytes of entropy.
* Only the token's hash is stored — the raw token is never persisted.
* Tokens are single-use: consumed on first exchange.
* Configurable TTL (10–3600 seconds).
* Scope-bound: a token scoped to `autofill` cannot be used for `export`.

## Secret Redaction

Output from any command that used injected credentials is scanned and redacted before it returns to the LLM, so a secret that appears in a response body or error message never lands in the model's context.

```bash theme={null}
some-command | anima vault redact --agent <agent-id>
# any value matching a stored credential becomes [REDACTED]
```

`anima vault redact` fetches the agent's credentials, replaces any matching secret value in stdin with `[REDACTED]`, and can take extra literal strings via `--pattern`.

## Template Substitution

For structured references inside a block of text, use the template syntax and let the CLI resolve it at execution time:

```text theme={null}
{{vault:credentialId:login.password}}
{{vault:credentialId:apiKey.key}}
{{vault:credentialId:oauthToken.accessToken}}
```

The CLI detects `{{vault:...}}` templates (and `vtk_` tokens) in input and exchanges them for real credentials before the command runs.

## Zero-Knowledge Execution

Ephemeral tokens, template substitution, and redaction protect against *accidental* plaintext exposure. For a tighter boundary — where the agent authors the call but can never read the secret — the CLI adds a set of execution primitives. All resolve credentials through [SecretRef & `anima.json`](/secret-ref).

### `anima vault exec`

Run a subprocess with resolved secrets injected as environment variables. The agent writes the command; the CLI resolves the `anima.json` references and spawns the child — the model's context never sees the values. Output is scrubbed by the redaction engine.

```bash theme={null}
anima vault exec -- gh api /user
anima vault exec -- psql -c "select count(*) from users"
```

### `anima vault proxy`

A loopback-only HTTPS proxy that injects an `Authorization` header into outbound requests. The agent holds only a short-lived proxy token (`pxt_`); the credential lives in the CLI process and is never reachable from the network. Requests to any host not on `--allow-host` are rejected.

```bash theme={null}
anima vault proxy --cred cred_github --allow-host api.github.com --port 19840 &
# proxy_token=pxt_...  port=19840

curl -H "X-Anima-Proxy: pxt_..." \
  http://127.0.0.1:19840/https://api.github.com/user
```

### `anima vault agent` (keystroke injection)

A local daemon that binds to a Unix socket (mode `0600`) and — on a user-confirmed hotkey — types a credential into the focused text field. Useful for apps that can't take a proxy, such as desktop SSH clients or native database UIs.

```bash theme={null}
anima vault agent start
anima vault type --cred GH_TOKEN   # press the hotkey to confirm; the daemon types the value
```

### Revealing plaintext

The CLI never prints secret plaintext. `anima vault get` always masks secret fields — there is no `--unmask` flag and no `unlock` command. To actually view a secret, a human uses the Anima console, where a reveal is audited and step-up gated. Agents and automation should *use* secrets, never read them: autofill via the browser extension, local injection via `anima vault exec` / `anima vault proxy`, or the server-side broker via `anima vault use`.

### `anima vault audit`

Scan the filesystem for leaked secrets, cross-referenced against the vault inventory. High-confidence key patterns are flagged by heuristic; literal values that match a stored credential are flagged by exact comparison.

```bash theme={null}
anima vault audit .        # scan the current directory
anima vault audit --check  # CI mode: exit non-zero on findings
```

<Note>
  MCP vault tools never return plaintext to the model. They hand back a plan that a trusted local process (the CLI, the extension, or the keystroke daemon) executes — the LLM composes intent, and the local process enforces the secret boundary.
</Note>

## Browser Extension

The Anima browser extension performs vault credential autofill for login forms, so an agent can log in without the password ever entering its context:

1. The agent stores credential data ephemerally.
2. The agent asks the extension to fill the detected login form.
3. The extension detects the username, password, and TOTP fields.
4. Credentials are injected and immediately zeroized from memory.

To bind the extension to an agent from a headless browser — a Puppeteer worker, a scheduled job, no human to click — use [Headless Extension Connect](/extension-connect).

## Access Log

Every credential access — token mints, `exec` invocations, and masked reads — is recorded in the vault audit log.

```bash theme={null}
anima vault audit   # (GET /vault/audit) — the vault access stream
```

In the console, the **Vault → Access Log** page filters this stream and highlights plaintext reveals (via a master key) with a warning banner, so compliance teams can confirm they were intentional. Masked accesses from agent keys are the common path and don't need review.

## Deprovision

Remove an agent's vault and all stored credentials:

```python theme={null}
anima.vault.deprovision(agent_id=agent.id)
```

## Security

* All credentials are encrypted at rest with AES-256-GCM.
* Each agent's vault is isolated, with its own per-agent encryption key — agents cannot access each other's credentials.
* Vault access is scoped to the agent's API key.
* Credential reads are masked by default; plaintext access requires a master-key `reveal` (audit-logged) or a single-use vault token exchange.
* Vault-generated passwords never appear in any API response, audit log, or webhook payload — only the credential ref leaves the vault.
* See [Encryption](/encryption) for the per-agent key-derivation model, and [SecretRef & `anima.json`](/secret-ref) for the reference schema used by `exec` and `proxy`.

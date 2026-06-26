# auth-md-signup

**OpenClaw skill** — Complete an [auth.md](https://workos.com/auth-md) **user-claimed signup** against any service that publishes the protocol.

> Attributed to **[NoForm](https://noform.dev)** — the reference implementation for frictionless, consent-preserving agent registration.  
> Protocol: [github.com/workos/auth.md](https://github.com/workos/auth.md) (MIT, by WorkOS)

---

## What it does

When your OpenClaw agent hits a `401` carrying `WWW-Authenticate: Bearer resource_metadata="…"`, or when you ask it to "sign me up for `<service>`", this skill walks the full **auth.md user-claimed flow**:

1. **Discovers** the Protected Resource Metadata (RFC 9728) and Authorization Server metadata
2. **Registers anonymously** — no account yet
3. **Asks you** for the email address to claim under
4. **Service emails you** a one-time 6-digit code
5. **You paste the code** back to the agent
6. **Agent submits** the OTP → receives a scoped, revocable credential
7. **Stores** the token scoped to that one service (never touches your primary credentials)

**The human confirming the OTP is the consent gate. The agent never auto-confirms.**

---

## Install

```bash
openclaw skills install auth-md-signup
```

Or via ClawHub:

```bash
clawhub install auth-md-signup
```

---

## Usage

Just talk to your agent:

```
Sign me up for NoForm          → agent asks for your slug, then walks the flow
Sign me up for api.example.com → agent discovers auth.md from that domain
I got a 401 from api.foo.com   → agent reads the WWW-Authenticate header and starts
Revoke my token for NoForm     → agent calls revocation_uri and clears local token
What services am I registered with? → agent lists stored auth.md tokens
```

---

## NoForm reference

[NoForm](https://noform.dev) is the reference implementation for this skill. NoForm apps publish auth.md at:

```
https://noform.dev/a/<slug>/auth.md
https://noform.dev/a/<slug>/.well-known/oauth-protected-resource
https://noform.dev/a/<slug>/.well-known/oauth-authorization-server
```

The skill works with **any** service that publishes the protocol — NoForm is the default demo target, not a hard dependency.

---

## Security model

- **User-claimed flow only** — no silent autonomous signup, no agent-verified / ID-JAG path
- **Tokens are scoped per service** (`resource` URL as key) — cross-service leakage is architecturally impossible
- **Primary credentials never touched** — only the `credential` returned by the auth.md `claim/complete` endpoint is stored
- **Revocation supported** — one call revokes the agent's access; your account remains intact
- **Human OTP gate** — the agent waits for you; it cannot proceed without your explicit input

This design reflects lessons from the MoltMatch incident and Claw Chain CVEs: consent-preserving delegation, not credential removal.

---

## Optional env var

| Variable | Required | Description |
|----------|----------|-------------|
| `AUTH_MD_TOKEN_STORE` | No | Path to a JSON file for persistent token storage across sessions (e.g. `~/.openclaw/auth-md-tokens.json`). Omit to use session memory only. |

---

## Protocol reference

- [auth.md spec](https://github.com/workos/auth.md) — WorkOS, MIT
- [RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728) — OAuth 2.0 Protected Resource Metadata
- [ID-JAG draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-identity-assertion-authz-grant) — Identity Assertion Authorization Grant
- [WorkOS auth.md docs](https://workos.com/auth-md/docs)

---

## License

MIT-0 (per ClawHub policy — use, fork, ship, no attribution required).  
Reference attribution: [NoForm](https://noform.dev).

---

*Made for the OpenClaw community. Ship it forward.*

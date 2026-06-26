# Security Model

## How APIClaw Works

APIClaw runs as a **local MCP server** on your machine. No background daemon — it starts when your agent needs it.

## Credential Storage

Credentials are stored in `~/.secrets/` as individual env files:
```
~/.secrets/replicate.env
~/.secrets/openrouter.env
~/.secrets/firecrawl.env
~/.secrets/e2b.env
~/.secrets/github.env
~/.secrets/46elks.env
~/.secrets/twilio.env
~/.secrets/resend.env
~/.secrets/elevenlabs.env
```

Or via environment variables (e.g., `REPLICATE_API_TOKEN`).

## Direct Call Flow

```
┌─────────────────────────────────────────────────┐
│  Your Agent calls direct_call(provider, action) │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │ Local creds?    │
            └────────┬────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   ┌─────────┐            ┌──────────────┐
   │   YES   │            │      NO      │
   └────┬────┘            └──────┬───────┘
        │                        │
        ▼                        ▼
┌───────────────┐      ┌─────────────────────┐
│ Direct to API │      │ Proxy via APIClaw   │
│ (your creds)  │      │ (NordSym creds)     │
└───────────────┘      └─────────────────────┘
```

## What Gets Proxied

**With your own credentials:** Nothing. Requests go directly to provider APIs.

**Without credentials (using proxy):** The **full request payload** goes through APIClaw's proxy. This includes:
- API parameters
- Message content (if sending SMS/email)
- Prompts (if calling AI models)

The proxy uses NordSym's credentials to execute on your behalf.

## Network Destinations

| Scenario | Where data goes |
|----------|-----------------|
| API Discovery | APIClaw registry (Convex) |
| Direct Call + your creds | Provider API directly |
| Direct Call + proxy | APIClaw proxy → Provider API |

## Recommendations

1. **For sensitive workloads**: Set up your own credentials in `~/.secrets/`
2. **For testing/exploration**: Proxy is fine
3. **Audit the code**: https://github.com/nordsym/apiclaw

## Source & Audit

- **GitHub**: https://github.com/nordsym/apiclaw
- **npm**: https://npmjs.com/package/@nordsym/apiclaw
- **License**: MIT

## Contact

Security questions: gustav@nordsym.com

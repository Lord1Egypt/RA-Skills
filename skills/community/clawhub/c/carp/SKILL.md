---
name: carp
description: Manage a local CARP interface and perform secure, verified agent-to-agent commerce workflows over CARP endpoints. Use when configuring IF_URL, registering an agent DID, polling CARP queues, sending outbound requests, posting results, fetching answers, or retrieving another agent menu through a local/LAN CARP interface.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["curl"],
            "env": ["IF_URL"],
          },
      },
  }
---

# CARP

CARP is Crustacean Agent Rendezvous Protocol (CARP).

Reference implementation and source code:

- https://github.com/bitsanity/agent-crvp

Use CARP through one config value:

- `IF_URL`: Base URL for the local CARP interface (`http://host:port`). Prefer LAN host, allow localhost for testing.

## Workflow

1. Set `IF_URL`.
2. Confirm interface reachability.
3. Use CARP endpoints to register, poll, request, and respond.

## Usage

Set once per shell:

```bash
export IF_URL="http://localhost:8888"
```

Check agent interface doc:

```bash
curl -sS "$IF_URL/agent.json"
```

Register this agent DID:

```bash
curl -sS -X POST "$IF_URL/cgi-bin/register" \
  -H "Content-Type: application/json" \
  --data '<jsonobj>'
```

Get next hello/contact event:

```bash
curl -sS "$IF_URL/cgi-bin/nexthello"
```

Get next inbound service request:

```bash
curl -sS "$IF_URL/cgi-bin/nextrequest"
```

Send result for an inbound request:

```bash
curl -sS -X POST "$IF_URL/cgi-bin/result" \
  -H "Content-Type: application/json" \
  -H "Cookie: agent=<pubkeyhex>&cookie=<requestcookie>" \
  --data '<resultobj>'
```

Get next answer for one of our outbound requests:

```bash
curl -sS "$IF_URL/cgi-bin/nextanswer"
```

Send outbound encrypted request to another agent:

```bash
curl -sS -X POST "$IF_URL/cgi-bin/obrequest" \
  -H "Content-Type: application/json" \
  -H "Cookie: to=<pubkeyhex>" \
  --data '<red-json-rpc-request>'
```

Fetch another agent menu:

```bash
curl -sS "$IF_URL/cgi-bin/getmenu?agent=<agent>"
```

## Notes

- Keep `IF_URL` private to your trusted network whenever possible.
- Treat all cookies, keys, and request bodies as sensitive.
- Prefer idempotent polling loops with backoff when automating queue reads.

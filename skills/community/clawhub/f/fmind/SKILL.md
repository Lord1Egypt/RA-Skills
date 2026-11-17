---
name: fmind
description: >
  Use FMind as the unified knowledge and external-memory gateway. Import and
  search tenant knowledge bases through the FMind API, and use L0-L2 memory,
  context, and published Memory Wiki through an Agent Binding. Never call
  MemoryCore directly and never expose credentials in prompts, logs, URLs, or
  saved files.
metadata:
  openclaw:
    requires:
      env: [FMIND_BASE_URL, FMIND_USER_API_KEY]
      optionalEnv: [FMIND_AGENT_RUNTIME_KEY, FMIND_AGENT_SETUP_KEY]
    version: "2.0.0"
    auth: "fmind-user-key-plus-agent-binding"
---

# FMind unified knowledge and memory

This skill has two deliberately separate data paths:

1. **Knowledge path** — normal FMind Knowledge Base REST APIs for files, URLs,
   Markdown, and RAG search.
2. **Memory path** — FMind/MemoryProxy gateway for L0-L2 context and recall,
   capture, and published Memory Wiki. MemoryCore is private infrastructure and
   must never be called by an external agent.

The server, not this skill, decides the effective permission:

```text
user tenant role
∩ team/resource scope
∩ Agent Binding capability
∩ Agent Binding asset scope
∩ current resource state
```

Do not infer tenant, team, user, agent, knowledge-base, or wiki permissions
from values supplied by the model. A `403` is an authorization result, not a
reason to retry with another identifier.

## Setup

An administrator creates an Agent Binding in FMind and gives the external
agent a setup prompt. The prompt contains:

- `FMIND_USER_API_KEY="${FMIND_USER_API_KEY}"` — a placeholder for the
  existing FMind user API key. The agent operator fills this locally; the skill
  must never ask the user to paste it into a chat message.
- `FMIND_AGENT_SETUP_KEY` — a one-time setup secret. It expires after the
  configured setup window and is consumed by one successful handshake.

After setup, the server returns an Agent Runtime Key once. Store it only in a
secret manager or process environment as `FMIND_AGENT_RUNTIME_KEY`; delete the
setup key. Do not write either credential to `openclaw.json`, source control,
chat transcripts, URLs, analytics, or shell history.

Required environment:

```bash
export FMIND_BASE_URL="https://fmind.example.com/api/v1"
export FMIND_USER_API_KEY="<existing FMind user API key>"
export FMIND_AGENT_RUNTIME_KEY="<runtime Agent Binding key>"
```

Only during the one-time setup handshake:

```bash
export FMIND_SETUP_ENDPOINT="https://fmind.example.com"
export FMIND_AGENT_SETUP_KEY="<one-time setup key>"
```

`FMIND_BASE_URL` is the public FMind API base and must end in `/api/v1` for
knowledge operations. Do not derive public addresses from a browser URL. Local
development may use an explicit loopback address; production requires HTTPS.

## Credential checks

Before a request, fail closed if the required variables are missing:

```bash
if [ -z "$FMIND_BASE_URL" ] || [ -z "$FMIND_USER_API_KEY" ]; then
  echo "Missing FMind user credentials. Configure FMIND_BASE_URL and FMIND_USER_API_KEY." >&2
  exit 1
fi
```

Knowledge requests use the user key only:

```bash
fmind_api() {
  local method="$1" endpoint="$2" body="${3:-}"
  curl --fail-with-body -sS -X "$method" "$FMIND_BASE_URL/$endpoint" \
    -H "X-API-Key: $FMIND_USER_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-Request-ID: $(uuidgen 2>/dev/null || date +%s)" \
    ${body:+-d "$body"}
}
```

Memory gateway requests require **both** identities. The user key identifies
the FMind user; the Agent Runtime Key identifies the external Agent Binding.
The gateway removes these credentials before forwarding to an upstream model:

```bash
fmind_memory_headers() {
  printf '%s\n' \
    "X-FMind-User-Key: $FMIND_USER_API_KEY" \
    "X-FMind-Agent-Key: $FMIND_AGENT_RUNTIME_KEY" \
    "Content-Type: application/json"
}
```

Do not substitute a Binding Token, MemoryCore service key, knowledge-base API
key, or model-provider key for either header.

## One-time setup handshake

The setup key is sent only to the FMind setup endpoint:

```bash
curl --fail-with-body -sS -X POST "$FMIND_SETUP_ENDPOINT/internal/v1/agent-bindings/setup" \
  -H "X-FMind-Connector-Secret: $FMIND_AGENT_SETUP_KEY" \
  -H "X-FMind-User-Key: $FMIND_USER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"binding_id":"<binding-id>","external_agent":"<agent>","connector_type":"<connector>","client_version":"<version>"}'
```

On success, save only the returned runtime Agent Key in a secret store, unset
`FMIND_AGENT_SETUP_KEY`, and never retry the setup key. Setup failures are not
proof that a binding exists; stop and ask an administrator to regenerate the
prompt.

## Knowledge API

Use the normal user-key path for tenant knowledge. Select a knowledge base
explicitly and respect the user’s resource permissions.

| User intent | Endpoint | Notes |
| --- | --- | --- |
| List knowledge bases | `GET /knowledge-bases` | Select by id or name before mutations. |
| View KB details | `GET /knowledge-bases/:id` | Check indexing and access. |
| Upload a file | `POST /knowledge-bases/:id/knowledge/file` | Multipart field `file`. |
| Import a URL | `POST /knowledge-bases/:id/knowledge/url` | JSON `url`. |
| Create Markdown | `POST /knowledge-bases/:id/knowledge/manual` | JSON `title`, `content`. |
| Check processing | `GET /knowledge/:id` | Poll parse status. |
| Browse entries | `GET /knowledge-bases/:id/knowledge` | Paginated. |
| Search one KB | `GET /knowledge-bases/:id/hybrid-search` | JSON query body. |
| Search several KBs | `POST /knowledge-search` | JSON query and KB ids. |

Destructive operations require the user’s explicit target and confirmation.
Never upload or delete content merely because a prompt contains a filename or
URL.

## Memory gateway API

Use the configured FMind/MemoryProxy public gateway, not MemoryCore. The exact
memory route is deployment-configured; keep the gateway endpoint in an
environment variable such as `FMIND_MEMORY_PROXY_URL`.

The gateway performs online user-key + Agent-key verification and capability /
asset checks for every request. Typical operations are:

- `memory.context` / `context.assemble` — read authorized context.
- `memory.recall` — retrieve authorized L0-L2 memories.
- `memory.capture` — record an interaction as L0-L2 when the binding allows it.
- `wiki.get` — read a published, non-revoked Memory Wiki page.

`memory.capture` does not grant review or publish. `memory.recall` does not
grant `wiki.get`. A revoked or archived Wiki page must be treated as not found
for external-agent reads.

Example gateway request:

```bash
curl --fail-with-body -sS -X POST "$FMIND_MEMORY_PROXY_URL/v1/memory/recall" \
  -H "X-FMind-User-Key: $FMIND_USER_API_KEY" \
  -H "X-FMind-Agent-Key: $FMIND_AGENT_RUNTIME_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"deployment process","asset_scope":"team:team-a"}'
```

The endpoint may be mapped differently by a reverse proxy. Do not invent a
fallback path; use the endpoint supplied in the setup prompt or deployment
manifest.

## OpenClaw and MCP

OpenClaw should keep credentials in environment variables and load this skill
after the Agent Binding setup. MCP configuration must use the two credentials,
not a long-lived Binding Token:

```json
{
  "mcpServers": {
    "fmind-cognition": {
      "url": "https://fmind.example.com/mcp/cognition",
      "headers": {
        "X-FMind-User-Key": "${FMIND_USER_API_KEY}",
        "X-FMind-Agent-Key": "${FMIND_AGENT_RUNTIME_KEY}"
      }
    }
  }
}
```

The MCP server still verifies the binding and resource scope per tool call.
Do not put credentials in a prompt, tool result, or model-visible context.

## Browser extension

The FMind browser extension is an ingestion and citation helper, not an
authorization bypass. Configure it with the FMind API base and a scoped user
API key; it must never receive an Agent Runtime Key unless the extension is
explicitly operating as the bound Agent.

Browser actions should use the same user-key API path and mark ingestion with
`channel=browser_extension`. Memory capture remains on the Agent/MemoryProxy
path. Do not let a browser page call MemoryCore or inject credentials into page
content. On `401`, ask the user to reconfigure the extension; on `403`, explain
that the selected KB/team is outside the user’s scope.

## Response and error handling

- `401`: missing, expired, or invalid user/Agent credential; stop and re-auth.
- `403`: role, team, capability, asset scope, or resource state denies access;
  do not retry with guessed IDs.
- `404`: wrong endpoint/resource or revoked external Wiki; verify the supplied
  resource without enumerating other tenants.
- `413`: upload too large; ask for a smaller input.
- `429`: back off according to `Retry-After`.
- `5xx`: retry only idempotent reads with bounded exponential backoff.

Never print response headers, setup prompts, API keys, runtime keys, or signed
tokens in normal agent output.

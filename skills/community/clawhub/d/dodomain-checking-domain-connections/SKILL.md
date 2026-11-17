---
name: checking-domain-connections
description: "Reviews the DNS health of existing doDomain connections and queues rechecks after confirmation. Use when the user asks 'which of my connected domains are broken', 'is this customer's domain still connected', 'when was this connection last checked', 'recheck the DNS on this connection', 'find domains with DNS drift', or wants a custom domain health report."
---

# doDomain connection health

Report which of the team's domain connections are healthy, which are broken, and queue a DNS recheck where the user asks for one.

## Connecting and calling the tools

Every tool in this skill comes from the `dodomain` MCP server, the doDomain connector, and is written here as `dodomain:<tool>`.

- **Tools listed by name:** call them directly, for example `dodomain:check_domain`.
- **Only `dodomain:search_tools` and `dodomain:execute_typescript` listed (Code Mode, the default):** call `dodomain:search_tools` first, then call each tool inside `dodomain:execute_typescript` as `external_<tool>` (for example `external_check_domain`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `dodomain:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects doDomain and approves that scope.
- **No `dodomain` tools at all:** doDomain is not connected yet. Install the doDomain power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `dodomain:list_apps`: app ids and names, so connections can be grouped by app.
- `dodomain:list_connections`: connections with `status`, `fqdn`, and the `verifiedAt`, `lastCheckedAt`, and `brokenAt` timestamps. Filter by app or domain. Paginated.
- `dodomain:reverify_connection`: queue an on-demand DNS recheck of one connection. Returns `{ accepted: true }`; the check runs asynchronously and does not return a verdict.
- `dodomain:check_domain`: provider and zone for a broken domain, so the user knows which DNS provider the customer uses.

## Workflow

1. Call `dodomain:list_apps`, then `dodomain:list_connections` for the app the user named, or for every app when they asked about the whole team. Follow pagination until you have the full set.
2. Group the results by status. List broken connections first with `fqdn`, `brokenAt`, and `lastCheckedAt`, then healthy ones with `verifiedAt`.
3. For each broken connection the user cares about, call `dodomain:check_domain` to name the DNS provider behind it.
4. If the user asks for a recheck, confirm which connection, then call `dodomain:reverify_connection` once.
5. Tell the user the recheck is queued and runs in the background. Offer to read the result back later with `dodomain:list_connections`.

## Rules

- `dodomain:reverify_connection` answers `{ accepted: true }` and nothing else. Never report that as the domain being verified.
- Rechecks are rate limited. On `RATE_LIMITED`, report `retryAfterSeconds` and stop. Never loop on rechecks.
- An unknown connection id returns `NOT_FOUND`. Say the connection is not on this team and offer `dodomain:list_connections`.
- Report timestamps in the user's timezone and say which timezone you used.

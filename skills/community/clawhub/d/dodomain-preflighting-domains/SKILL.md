---
name: preflighting-domains
description: "Pre-flights a domain in doDomain before anyone touches DNS: finds who runs DNS, the DNS provider and registrable zone, and whether the domain qualifies for one-click connect. Use when the user asks 'who runs DNS for shop.acme.com', 'can this domain do one-click connect', 'which DNS provider does this domain use', 'check this domain', 'how hard is it to connect this custom domain', or wants a DNS lookup before onboarding a customer domain. Read-only."
---

# doDomain domain pre-flight

Tell the user what connecting a domain will involve before a connect session is created. This skill only reads public DNS and team state; it creates nothing and uses no quota.

## Connecting and calling the tools

Every tool in this skill comes from the `dodomain` MCP server, the doDomain connector, and is written here as `dodomain:<tool>`.

- **Tools listed by name:** call them directly, for example `dodomain:check_domain`.
- **Only `dodomain:search_tools` and `dodomain:execute_typescript` listed (Code Mode, the default):** call `dodomain:search_tools` first, then call each tool inside `dodomain:execute_typescript` as `external_<tool>` (for example `external_check_domain`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `dodomain:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects doDomain and approves that scope.
- **No `dodomain` tools at all:** doDomain is not connected yet. Install the doDomain power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `dodomain:check_domain`: the DNS provider managing the domain, the registrable zone, the connect tier it qualifies for (1 one-click OAuth, 2 Domain Connect, 3 guided manual), detection confidence, nameservers, and a provider-specific setup guide.
- `dodomain:list_connections`: existing connections on the team, filterable by domain. Use it to see whether the domain is already connected.

## Workflow

1. Take the exact hostname the user gave (for example `shop.acme.com`). If they gave a URL, strip the scheme and path.
2. Call `dodomain:check_domain` for that hostname.
3. Call `dodomain:list_connections` filtered to the domain to see whether the team already has a connection for it.
4. Report in this order: DNS provider, registrable zone, connect tier in plain words, what the customer will have to do for that tier, and whether a connection already exists.
5. If the tier is 3 (guided manual), summarize the provider-specific setup guide the tool returned so the user can pass it on.
6. Offer the `connecting-customer-domains` skill as the next step. Do not start a session from here.

## Rules

- Never call `dodomain:create_connect_session`, `dodomain:verify_connect_session`, or `dodomain:reverify_connection` from this skill. Pre-flight is read only.
- Results come from the live DNS system and can change between calls. Say so if the user compares two runs.
- Only report fields the tool returned. If detection confidence is low, say so instead of presenting the provider as certain.

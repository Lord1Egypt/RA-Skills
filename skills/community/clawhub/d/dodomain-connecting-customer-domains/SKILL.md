---
name: connecting-customer-domains
description: "Starts and follows a doDomain connect session that points a customer's own domain at one of the user's apps, returns the DNS records the customer must add, and verifies them. Use when the user asks to 'start a connect session for shop.acme.com on my app', 'connect my customer's custom domain', 'onboard a customer domain', 'what DNS records does my customer need', 'have the records landed yet', or 'verify the domain'. Creating a session uses monthly connection quota and is confirmed first."
---

# Connect a customer domain with doDomain

Walk one domain from a new connect session to verified DNS. Creating a session uses one unit of the plan's monthly connection quota, so confirm before you create one.

## Connecting and calling the tools

Every tool in this skill comes from the `dodomain` MCP server, the doDomain connector, and is written here as `dodomain:<tool>`.

- **Tools listed by name:** call them directly, for example `dodomain:check_domain`.
- **Only `dodomain:search_tools` and `dodomain:execute_typescript` listed (Code Mode, the default):** call `dodomain:search_tools` first, then call each tool inside `dodomain:execute_typescript` as `external_<tool>` (for example `external_check_domain`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `dodomain:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects doDomain and approves that scope.
- **No `dodomain` tools at all:** doDomain is not connected yet. Install the doDomain power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `dodomain:list_apps`: the apps on the team with id, name, public widget key, and sandbox flag. Never returns secret keys.
- `dodomain:check_domain`: provider, zone, and connect tier for the domain, as a pre-flight.
- `dodomain:create_connect_session`: start a session for a domain on an app. Takes the `appId`, the customer's `domain`, and the DNS records the app needs; returns a `sessionToken` and the records to apply. Counts against the monthly connection quota.
- `dodomain:get_connect_session`: the current state of a session by token: domain, expected records, and status (`pending`, `detected`, `authorizing`, `writing`, `verifying`, `verified`).
- `dodomain:verify_connect_session`: a live check of the session's expected records against authoritative nameservers, with a per-record breakdown of present, propagating, or absent.

## Workflow

1. Call `dodomain:list_apps`. If the team has more than one app, ask which one the domain belongs to. Point out sandbox apps.
2. Call `dodomain:check_domain` for the domain and tell the user which connect tier the customer will get.
3. Ask for the DNS records the app needs if the user has not given them. Do not invent record targets.
4. Confirm the app, the domain, and the records, and say that this uses one unit of the monthly connection quota. Then call `dodomain:create_connect_session`.
5. Report the `sessionToken` and list the records the customer must apply, one per line with type, name, and value.
6. When the user asks for progress, call `dodomain:get_connect_session` for the status, then `dodomain:verify_connect_session` for the per-record breakdown.
7. Present the breakdown record by record. `verified` is true only when every record matches.

## Rules

- `verified: false` on a fresh session is a normal answer, not an error. It means the records are not published yet. Name each missing record.
- `propagating` means the record is on its way. Suggest checking again in a few minutes rather than calling in a loop.
- If a call returns `RATE_LIMITED`, tell the user the wait in seconds from `retryAfterSeconds` and stop. Do not retry automatically.
- Create at most one session per domain per request. If the user already has a session token for that domain, use `dodomain:get_connect_session` instead.

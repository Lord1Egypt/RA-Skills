# Domain workflows

## Search and acquire

1. Use `search`, `suggest_domains`, or `list_tlds` without authentication.
2. Present a small set with availability, registration price, renewal price,
   and any premium or aftermarket status. Do not imply that the cheapest TLD is
   the best fit.
3. Before `buy_domain` or `buy_aftermarket`, state the exact domain, price,
   term, renewal price when available, and payment method. Obtain confirmation.
4. Set `max_price` to the amount the user approved. After an ambiguous error,
   inspect the account/domain state before retrying.
5. For a taken domain, distinguish buy-now aftermarket inventory, negotiation,
   brokerage, and best-effort backorder. Never present any route as guaranteed.

## Provision an agent identity

1. Use `provision_agent` when one approved operation should buy or reuse a
   domain, set up email DNS, create or reuse its mailbox, and register an event
   webhook.
2. Confirm the domain and live price before the call. Reuse the same domain,
   slug, and webhook URL when retrying; provisioning is idempotent for those
   resources.
3. If the destination requires authentication, pass `webhook_headers` with
   only `Authorization` or `X-API-Key`. Header inputs are validated before any
   charge, encrypted at rest, and represented in responses only by
   `header_names`.
4. Never repeat a header value in the outcome, logs, or follow-up instructions.

## Connect hosting or DNS

1. Read current DNS with `get_dns` and retain `zone_version` if returned.
2. Prefer `connect_domain` with `dry_run: true` for supported providers.
3. Never replace active MX records without explaining that email routing will
   move and obtaining confirmation.
4. Snapshot DNS before broad changes. Apply the smallest diff and verify with
   `verify_connection`, `verify_service`, or `domain_status`.
5. Do not claim propagation is complete until verification passes.

## Adopt or transfer

1. Use `plan_domain_adoption` to decide between free import and registrar
   transfer while preserving live DNS and email.
2. Import when the user wants Domani visibility/management without changing
   registrar. Transfer only when they explicitly want registrar custody moved.
3. Show the continuity plan and exact transfer price before requesting the EPP
   code or calling `transfer_domain`.
4. Keep the domain at its current nameservers during transfer unless the user
   separately authorizes a DNS migration.

## Maintenance and ownership

- Keep WHOIS privacy and security lock enabled by default.
- Confirm paid renewals and use `max_price`.
- Treat EPP codes and registrant contact data as sensitive.
- For transfer-away or ownership operations, explain the security consequence
  and verify the requested recipient/account before proceeding.

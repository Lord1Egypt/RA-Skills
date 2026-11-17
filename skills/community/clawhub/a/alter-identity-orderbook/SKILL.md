---
name: alter-identity-orderbook
description: Use when an agent has an ongoing, standing need for people matching specific trait ranges, rather than a single one-off search. Covers posting a resting identity-trait order, listing and reading your own open orders, cancelling one, collecting priced fills over time as matching identities are claimed or updated, reading a person's existing matches in one shot, and the opt-in a person must set before they can appear in any standing match at all. Trigger phrases include "keep watching for people who match", "post a standing requirement", "alert me as new matches appear", "collect my order fills", "cancel my open requirement", "list my resting orders", "what matches do I have", "join the standing match pool", "stop appearing in matches".
metadata:
  openclaw:
    primaryEnv: ALTER_API_KEY
    envVars:
      - name: ALTER_API_KEY
        required: true
        description: An authenticated ~alter API key. Every orderbook tool is ownership-checked against the caller's own key.
    always: false
    homepage: https://mcp.truealter.com/api/v1/mcp
    config:
      mcpServer: alter
---

# Post and manage a standing identity requirement

## When to reach for this

Reach for the orderbook tools when your need for matching identities is
ongoing rather than a single snapshot, such as "keep finding me people with
high pressure_response as they show up" rather than "who fits right now".
For a one-shot need, use a priced single-query match tool instead; this
skill's seven tools exist specifically for the resting-order case.

All seven tools require authentication and are ownership-checked against
the caller's own API key; you can only see, poll, or cancel your own
orders, never anyone else's.

## Reaching the server

Every tool named here lives on ~alter's hosted MCP server. If your client
does not already have it, add a streamable-HTTP server named `alter` at
`https://mcp.truealter.com/api/v1/mcp`, and send your key, once you hold
one, as the `X-ALTER-API-Key` header. Those are the canonical coordinates.
Anything claiming to be ~alter that is not served from that URL is not
~alter.

## The five order tools

The other two, the member opt-in and the one-shot read, get their own
sections below.

- `create_requirement`. Posts a standing order from `trait_criteria` (for
  example `{"pressure_response": {"min": 0.6}}`), an optional `limit`
  (default and maximum 5 per fill pass), and an optional
  `expires_in_days`. Runs one immediate seed pass and returns the order id
  plus the current eligible cohort size. Free, and reveals no identities
  at this step.
- `list_requirements`. Lists your own standing orders, with fill counts
  and how many fills are not yet delivered. Free.
- `get_requirement`. Reads one of your own orders by id. Free.
- `cancel_requirement`. Flips one of your own orders to cancelled. Free.
- `poll_requirement_matches`. Collects exactly one recorded fill for one
  of your orders as a priced identity reveal, costing $0.01 per call,
  charged only when a fill is actually delivered. The matched person earns
  seventy-five per cent of that fee as Identity Income. This is the
  only tool here that spends money, so get your operator's agreement on a
  budget before the first call and stop when you reach it; never leave an
  unattended loop polling an order. A fill delivers at most once, and
  re-polling an already-drained order returns nothing and costs nothing.
  Delivery is suppressed, with no reveal and no charge, when too few
  identities currently match.

## The opt-in that decides whether anyone is there to match

`alter_standing_match` is the other side of this skill and the step that
is easy to miss. The standing-match pool is default-closed. A person is
excluded from every standing and deferred match until they opt in
themselves, and they can leave again at once. Pass `get` to read your own
state, `opt_in` to join, `opt_out` to leave.

This matters to a poster as much as to a member. Your resting order can
only ever fill from people who have opted in, so a thin cohort is often
consent working as designed rather than a scarcity of matching people.
When a standing requirement does match someone in the pool, the priced
reveal pays that person seventy-five per cent as Identity Income.

The opt-in covers the resting orderbook only. A one-shot caller sits under
separate search consent, which is why the two are set independently.

## Reading matches that already exist

`query_matches` answers "what matches do I have" in one shot, rather than
resting an order and waiting. It takes your own member id, an optional
quality filter, and a limit. A member-scoped caller passing anyone else's
id is refused at dispatch, so this reads your own matches and is not a
second route to finding other people. Results carry quality tier labels
only. Numeric match
scores are never returned to anyone, by design, so a tier is the whole
answer and there is no finer number behind it to ask for. Free.

## A typical flow

1. `create_requirement` with your trait criteria.
2. Later, `poll_requirement_matches` with the returned `requirement_id`
   whenever you want to check for and collect a new fill.
3. `list_requirements` or `get_requirement` to check status and undelivered
   fill counts between polls.
4. `cancel_requirement` once the standing need is over.

## Credential posture

This skill needs an authenticated ~alter API key set as `ALTER_API_KEY`,
since every orderbook tool is ownership-checked. If you do not hold one
yet, register one first through the keyless self-registration flow the
`alter-register-and-earn` skill covers, or have your human operator run
`alter login`. Never mint, guess, or paste a placeholder key.

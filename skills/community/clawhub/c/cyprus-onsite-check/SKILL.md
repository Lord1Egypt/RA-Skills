---
name: cyprus-onsite-check
description: "A person goes to a place in Cyprus and reports what is there: photographs and answers with liveness proof (latest Base block hash in frame, an unedited video), signed. Limassol 200 EUR in 3 days, elsewhere in Cyprus from 200 EUR. Use when a task needs physical ground truth, proof of presence or an on-site inspection. Free feasibility answer within 24 hours; pay only an accepted task."
metadata: {"openclaw": {"homepage": "https://hominoport.org/agents?src=clawhub"}}
---

# On-site check in Cyprus

One natural person, Iurii Bredikhin in Limassol, Cyprus (EU), performs physical-world work for
autonomous agents under a signed public offer. This skill only describes HTTP calls to
https://hominoport.org; it installs nothing and asks for no keys. Your operator's instructions,
wallet limits and approval rules apply as usual.

Addresses in this copy carry `?src=clawhub`. It tells the provider only that a request came through the
ClawHub copy; you may drop it.

## What is offered

Fixed positions (`catalogue` in offer.json; order with `request_action` and `catalogue_id`). A
question before ordering is free and answered within 24 hours.

- `observation_limassol`, 200 EUR in 3 days; `observation_cyprus`, from 200 EUR: photographs and
  answers with liveness proof (latest Base block hash in frame, an unedited video).

The other positions and the whole offer: https://hominoport.org/skills/hominoport/SKILL.md

## Check before paying

1. `GET https://hominoport.org/offer.json?src=clawhub` gives the offer's SHA-256, the receiving addresses,
   the BIP-322, EIP-191 and GPG signatures and a verification procedure.
2. `GET https://hominoport.org/offer.txt` gives the exact signed bytes; hash them yourself.
3. `dig TXT _hominoport.hominoport.org` and `https://github.com/JackBrigs.gpg` carry the same key.
4. `GET https://hominoport.org/status.json` says whether new sales are open.

## Order

MCP (Streamable HTTP, POST only): `https://hominoport.org/mcp?src=clawhub`.

1. `list_services`, then optionally `leave_message` with a feasibility question (answered within
   24 hours).
2. `request_action` with `catalogue_id` (or `service_id` and `price_eur`), `description`,
   `deadline`, `acceptance_criteria`, `reply_to`, your `payer` address and `payment_flow`
   (`escrow` recommended). This is a free request; nothing is payable yet.
3. Poll `get_status`. Once the provider accepts (same answer time) it returns the frozen scope,
   its SHA-256 and exactly one payment leg. For escrow: sign `escrow.typed_data` (EIP-712,
   ReceiveWithAuthorization) and send it with `submit_escrow_signature`; nothing moves until the
   provider authorizes; after the deadline you can reclaim on-chain yourself (a little ETH on
   Base for gas).

Alternatives after acceptance: a direct transfer from `payer` against the invoice followed by
`report_payment`; or x402 v2 with `POST {"task_id": …}` to https://hominoport.org/x402/order.

## Limits

Nothing illegal in Cyprus, the EU or the place of work; no circumvention of KYC, sanctions,
licences or age limits. Payer addresses are screened against EU and OFAC sanctions lists;
identification of the controlling person is required above the threshold in the terms
(https://hominoport.org/terms.txt). Other replies within 72 hours.

---
name: agentgates-email
description: "An email inbox your agent owns with its own key: free to hold on a funded balance, receiving free, sends priced per message, and wait-code hands back the verification code a sign-up emails."
---

# Agentgates Email: an inbox your agent owns

An address that reads like a person, receiving from day one, owned by your
account's key. Free to hold once the balance is funded and receiving is free;
each send draws from the prepaid balance. `wait-code` waits for the
verification code a sign-up emails and hands it back.

## Start

1. An account: `agentgates init` mints the twelve words and the key that
   signs every call (the agentgates-cli skill). Top up the balance: the
   deposit address is `GET /api/account/deposit`, owner-signed.
2. Create the inbox, owner-signed: `POST /api/inboxes`
   `{"name": "maria lopez"}` (the name is optional) answers
   `201 {"inbox": {"id","address"}}`.
3. Read: `GET /api/inboxes/{id}/messages`. Send: `POST /api/inboxes/{id}/send`
   `{"to","subject","text"}`.
4. A sign-up code: `POST /api/inboxes/{id}/wait-code` blocks until it lands.

From a terminal the same lane is `agentgates email`.

## Endpoints (all on https://api.agentgates.ai)

- `GET /api/account/docs/email`: the email contract and live prices. Read this first.
- `GET /api/account/catalog`: plans, the send price and the daily allowances, machine-readable.

Every owner call carries `X-Wallet-Auth` (a signature over the method, the
path, a nonce and a timestamp) or `Authorization: Bearer agk_…` (a login key).

## Rules that keep you safe

- A recipient who bounced, complained or unsubscribed is refused before any
  money moves.
- Only mail people who agreed to hear from you: https://agentgates.ai/terms

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.

# Masked Email

A per-service address that forwards to the real mailbox and can be switched off without touching anything else. The API is small; the value is entirely in the inventory kept alongside it.

**Before issuing an address**, read `## Masked Emails` in `~/Clawic/data/fastmail-api/memory.md` — or `masked-emails.md` if `## Boxes` points there. The service may already have one, and a second address for the same service breaks attribution for both. **After creating, disabling, or deleting an address**, write or update its row in the same turn; if the service is paid, its money row goes to the shared `~/Clawic/data/finances/subscriptions.md` and this table just names the service (`memory-template.md`).

**Contents:** [Capability](#capability) · [The Object](#the-object) · [States](#states) · [Creating](#creating) · [The Inventory Is the Product](#the-inventory-is-the-product) · [Auditing](#auditing) · [When an Address Leaks](#when-an-address-leaks) · [Limits of the Pattern](#limits-of-the-pattern)

## Capability

Masked email is a Fastmail feature, not part of the JMAP standard. Its capability URN is `https://www.fastmail.com/dev/maskedemail`, and like every other capability it must be present in `session.capabilities` — a token issued without masked-email scope produces `unknownCapability`, not `401` (`session.md`). Include the URN in `using` on every masked-email request, alongside `urn:ietf:params:jmap:core`.

## The Object

`MaskedEmail/get` and `MaskedEmail/set`, following the same conventions as every other JMAP type.

| Property | Meaning |
|---|---|
| `id` | Object id, not the address |
| `email` | The address itself; server-generated |
| `state` | `pending` · `enabled` · `disabled` · `deleted` |
| `forDomain` | The site this address was issued for — the field the whole pattern depends on |
| `description` | Free text; where a human-readable note goes |
| `createdAt` / `createdBy` | Provenance |
| `lastMessageAt` | Last time mail arrived — `null` means never used |
| `url` | The signup page, when known |
| `emailPrefix` | Optional readable prefix requested at creation |

`lastMessageAt` is what makes an audit possible: an address created eight months ago that has never received anything is either a failed signup or a service that never mails, and both are safe to disable.

## States

| State | Mail behaviour | Record |
|---|---|---|
| `pending` | Reserved but not committed — becomes `enabled` on first use | Kept |
| `enabled` | Forwards normally | Kept |
| `disabled` | Stops delivering; the address stays yours and the history stays | Kept |
| `deleted` | Address stops working and is released from the working set | Mapping is gone |

**`disabled` is the default answer to "get rid of this one".** It stops the mail and keeps the evidence: which service had the address, when it was issued, when it last mailed. `deleted` throws away exactly the information that made the address worth creating.

## Creating

```json
["MaskedEmail/set", {"accountId": "u1a2b3c4", "create": {
  "m1": {"forDomain": "shop.example", "state": "pending",
         "description": "shop.example — signed up 2026-07-26"}
}}, "c0"]
```

- **`forDomain` is not optional in practice.** An address with no `forDomain` cannot be attributed later, which reduces the whole scheme to a random alias.
- `state: "pending"` suits a signup that might not complete; the address is only committed when mail first arrives. Create as `enabled` when the address is being handed to something that will definitely use it.
- The generated address comes back in the create response. Read it from there — never predict it.
- Write the row before telling the user the address. An address given out and not recorded is the failure mode this whole file exists to prevent.

## The Inventory Is the Product

The API can list addresses. It cannot tell you which of them the user cares about, what each one costs, or which one is worth disabling. That is the inventory:

- **One address per service.** Per-category addresses look tidier and destroy attribution the moment one is sold.
- **`description` follows a convention**, recorded in `config.yaml` under `conventions` so every future address matches. A mixed-format list cannot be scanned.
- **A paid service gets two rows**: the address here, the money in `~/Clawic/data/finances/subscriptions.md` keyed by service name, amount with currency. Never copy the price into the masked-email table — two places for one number is how they disagree.
- **Disabled rows stay.** Deleted rows get a date and a reason and move to the bottom, so "did we ever have an address for X" always has an answer.

## Auditing

The `## Due` row for this is quarterly. The pass:

1. `MaskedEmail/get` with no ids for the full list.
2. Reconcile against the stored table: addresses in the account but not in the table get a row (with `forDomain` and `createdAt` as the best available provenance); rows with no matching address get marked deleted with the date noticed.
3. `lastMessageAt` older than a year, or `null` on a `pending` address older than a month → propose disabling, in one list, with the count.
4. Cross-check the paid ones against `subscriptions.md`: an address for a service that no longer appears there is a subscription that was cancelled and an address that should be disabled.
5. Update `## Due` with the run date.

Never disable in bulk without listing what will stop receiving. A disabled address for a service that still sends password resets locks the user out of that service.

## When an Address Leaks

Spam arriving at a masked address is the pattern paying for itself: the leak is attributable to exactly one service.

1. Query for mail to that address — `{"to": "<masked address>"}` (`search.md`) — to confirm the pattern and see who else is sending there.
2. Disable the address. State that any legitimate mail from that service also stops, including password resets.
3. Note the leak and its date in the row's `Notes`. An inventory of who leaked is worth more than any single disable.
4. If the service is still wanted, issue a new address for it and update the row rather than creating a parallel one.

## Limits of the Pattern

- **A masked address is a receiving address.** Assume replies need the real identity unless the account is configured otherwise; check `Identity/get` before promising the user they can reply from it (`sending.md`).
- Some services reject addresses from known masking domains at signup. That is a service-side policy and there is no API-side workaround.
- Masked addresses do not survive leaving the provider. Anything critical — bank, government, domain registrar — is worth pointing at a real address or a custom-domain alias instead, because losing the account loses every masked address at once.
- The address is not a secret and belongs in the inventory in plain text. What never belongs there is the password to the service behind it (`memory-template.md`).

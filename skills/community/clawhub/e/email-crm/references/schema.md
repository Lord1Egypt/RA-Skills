# Schema contract

Schema version: `1`

## `contacts`

| Column | Meaning |
| --- | --- |
| `id` | Stable local integer identifier. |
| `email` | Trimmed, lowercased email. This currently matches `email_normalized`. |
| `email_normalized` | Trimmed, lowercased email used for every comparison; unique. |
| `source` | Required accountable origin such as `manual-review`. |
| `do_not_contact` | `0` or `1`; set to `1` whenever the address is suppressed. |
| `created_at`, `updated_at` | UTC ISO-8601 timestamps. |

An upsert returns JSON containing `ok` and `contact_id`. It replaces the stored `source` and refreshes `updated_at`, while retaining `created_at` and any existing DNC state. If the normalized address was suppressed before the contact existed, the inserted contact starts with `do_not_contact = 1`.

## `email_events`

Append-only lifecycle entries. `contact_id` references `contacts(id)` and is protected by a foreign key. Event types are constrained to `drafted`, `queued`, `sent`, `delivered`, `opened`, `replied`, `bounced`, and `failed`.

`metadata_json` is optional and must contain valid JSON. Do not place email content, recipient addresses, credentials, or sensitive personal data in it.

## `email_suppressions`

One row per normalized email address. Suppressing an address is idempotent and synchronizes matching contacts to `do_not_contact = 1`. The first persisted reason is retained and returned on later calls.

## `schema_meta`

Stores the schema version. Future versions must use explicit, tested migrations; never silently reinterpret existing contact data.

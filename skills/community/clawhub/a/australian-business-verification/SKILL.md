---
name: australian-business-verification
description: >-
  Verifies whether an Australian business is currently registered and active on the
  Australian Business Register (ABR), using its ABN (Australian Business Number), ACN
  (Australian Company Number / ASIC number), or business or entity name. Use this skill
  whenever a user asks to verify, check, confirm, validate, or look up an ABN, ACN,
  business registration status, "is this ABN active", "is this business registered /
  legit / real / a scam", GST registration status, entity type, or trading name for any
  Australian company, sole trader, partnership, trust, or government entity. Also use
  for KYC, vendor or supplier onboarding, accounts payable invoice checks, BAS/GST
  compliance, tax invoice validation, and due-diligence tasks involving any Australian
  business. Queries the official Australian Government ABR JSON API directly (no
  scraping, no third party) and returns entity name, ABN status (active/cancelled),
  entity type, GST registration status and date, state/postcode, and registered
  business and trading names.
metadata:
  author: arbaz
  version: "1.0"
license: MIT
---

# ABN Business Verification

## Overview

This skill checks whether an Australian Business Number (ABN) belongs to a real,
currently-registered entity by querying the **Australian Business Register (ABR)**
JSON API directly — the same free government register operated by the Australian
Taxation Office (ATO) that underpins ABN Lookup (abr.business.gov.au). It can verify
by ABN, by ACN (Australian Company Number, issued by ASIC), or by business/entity name.

Given a valid ABN, the skill returns:

- The registered legal entity name and entity type (company, sole trader, trust, etc.)
- Whether the ABN is **Active** or **Cancelled**, and since when
- Whether the entity is registered for **GST** (Goods and Services Tax), and since when
- The entity's main business location (state and postcode)
- Any registered business names and trading names linked to the ABN

This is a live, read-only lookup against a public government data source. It does
**not** modify, register, or update any ABN — the ABR web services are read-only by
design.

## When to use this skill

Trigger this skill for requests such as:

- "Is ABN 51 824 753 556 active / valid / real?"
- "Verify this supplier's ABN before I pay their invoice"
- "Check if [Business Name] is a registered Australian business"
- "Is this company GST registered?"
- "Look up the ACN 102 417 032 and tell me who it belongs to"
- "Can this business legally charge GST on their invoice?"
- Any onboarding, compliance, BAS preparation, or accounts-payable workflow that
  involves confirming a counterparty's ABN/ACN before proceeding

## Setup / Prerequisites

The ABR JSON API requires a free authentication GUID (Globally Unique Identifier).
This is **not** a paid API key — there is no cost and no usage charge from the
Australian Government.

1. Go to https://abr.business.gov.au/Tools/WebServices
2. Read the web services user guide, then accept the web services agreement to
   unlock the registration form
3. Complete the registration form. The ABR emails the GUID after processing
   (usually within hours, sometimes up to a few business days)
4. Make the GUID available to this skill as the environment variable
   `ABR_GUID` (do not hardcode it anywhere, do not print it back to the user,
   and do not log it)

If `ABR_GUID` is not set, `scripts/abn_lookup.py` will return a clear setup error
instead of failing silently — surface that message to the user with the link above.

No other credentials, scopes, or accounts are required. The only network access
needed is outbound HTTPS to `abr.business.gov.au`.

## Workflow

### Step 1 — Determine the search input

Ask the user for an **ABN** if they have one — this gives the most complete result
in a single call. If they don't have an ABN, ask whether they have:

- An **ACN** (9-digit Australian Company Number, from ASIC — appears on company
  letterheads, contracts, and the ASIC register), or
- A **business / entity name** to search for

Don't ask for all three at once — ask which identifier they have, then proceed with
whichever is available. If the user gives a name and several businesses could match,
that's expected — Step 6 covers resolving ambiguous name searches.

### Step 2 — Validate the identifier locally before calling the API

Before making any network call, validate the ABN or ACN checksum locally:

```bash
python3 scripts/abn_lookup.py --validate "51 824 753 556"
```

This runs the official ATO modulus-89 (ABN) or ASIC modulus-10 (ACN) checksum with
**no API call**. If `valid_checksum` is `false`, the number is malformed or mistyped
— tell the user immediately and ask them to double-check it rather than burning an
API call that will just come back with "Search text is not a valid ABN or ACN".

### Step 3 — Confirm credentials are configured

If this is the first lookup in the session, run any lookup command and check for the
`ABR_GUID environment variable is not set` error. If it appears, stop and walk the
user through the **Setup / Prerequisites** section above — do not attempt to guess,
fabricate, or ask the user to paste a GUID directly into chat.

### Step 4 — Query the ABR JSON API

Run the helper script with the appropriate flag. It calls the official endpoint,
strips the JSONP `callback(...)` wrapper the ABR API returns, and prints clean JSON.

```bash
# Look up by ABN (preferred — returns full entity detail)
python3 scripts/abn_lookup.py --abn 51824753556

# Look up by ACN (returns the same shape as an ABN lookup)
python3 scripts/abn_lookup.py --acn 102417032

# Search by business / entity name (returns a ranked list of candidates)
python3 scripts/abn_lookup.py --name "Acme Consulting" --max-results 10
```

The script also adds a small `"summary"` block on top of the raw ABR response with
a ready-to-use `verdict`, `gstRegistered`, and `canChargeGst` field so you don't have
to re-derive these from the raw fields. The full raw ABR fields are documented in
`reference/api-reference.md` — read that file if you need to interpret a field that
isn't covered by `summary`.

### Step 5 — Interpret the response

Check the top-level `"message"` field first (mapped from the ABR `Message` field):

- **Empty / blank** → the lookup succeeded, proceed to build the verification result
- **Non-empty** → this is an ABR error message (e.g. "No records found", "The GUID
  entered is not recognised as a Registered Party"). See
  `reference/api-reference.md` for the full error table and how to respond to each
  one — do not present these raw strings to the user without context

For a successful ABN/ACN lookup, the key fields to read are:

| Field                               | Meaning                                                   |
| ----------------------------------- | --------------------------------------------------------- |
| `summary.verdict`                   | `"active"`, `"cancelled"`, `"not_found"`, or `"error"`    |
| `entityName`                        | Registered legal name                                     |
| `entityTypeName` / `entityTypeCode` | e.g. "Australian Private Company" / `PRV`                 |
| `abnStatus`                         | `"Active"` or `"Cancelled"`                               |
| `summary.gstRegistered`             | `true`/`false`                                            |
| `gst`                               | Date GST registration took effect (if registered)         |
| `addressState` / `addressPostcode`  | Main business location                                    |
| `businessName`                      | Array of registered business/trading names (may be empty) |

A `"Cancelled"` ABN means the entity **was** registered but is **not currently
active** — never describe a cancelled ABN as "verified" or "active". Report it
plainly as cancelled and let the user decide how to proceed.

### Step 6 — Resolve a name search to a single entity

A name search (`--name`) returns a `"names"` array of candidates, each with a
`score` (0–100 relevance) and an `abn`. The ABR JSON name-search endpoint does
**not** return full entity detail (no entity type, no GST status) — only name,
ABN, status, state, postcode, and score.

1. Sort/present the candidates by `score`, highest first
2. If there's a clear single best match (e.g. one result scores 95+ and the rest
   are far lower), confirm with the user which entity they meant before treating
   it as the answer
3. If the user confirms (or there's an unambiguous single match), run a follow-up
   `--abn` lookup on that entity's ABN to get the full detail (entity type, GST
   status, etc.) for the final verification result
4. If multiple candidates score similarly, list the top 3–5 (name, ABN, state,
   status, score) and ask the user to pick one — don't guess

## Error handling & edge cases

| Situation                                                                         | How to respond                                                                                                                                                                                  |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ABR_GUID` not set                                                                | Explain the free GUID registration process (Setup section); don't retry without it                                                                                                              |
| Local checksum fails (`--validate`)                                               | Tell the user the ABN/ACN appears mistyped before calling the API                                                                                                                               |
| `message` = "No records found"                                                    | The ABN/ACN doesn't exist on the ABR. State this plainly — it does **not** necessarily mean fraud, but the number as given is not a registered ABN/ACN                                          |
| `message` mentions "GUID...not recognised" or "registration...has been cancelled" | This is a setup/credential problem, not a problem with the business being checked. Direct the user to re-check their GUID or re-register; do not present this as information about the business |
| `abnStatus` = "Cancelled"                                                         | Registered historically, not currently active. Report clearly as **Cancelled**, not "inactive business doesn't exist"                                                                           |
| `gst` is empty/null                                                               | Entity is not currently registered for GST — note this plainly, especially for invoicing/BAS questions                                                                                          |
| Name search returns 0 results                                                     | Try a shorter or differently-spelled name, or ask the user for an ABN/ACN instead                                                                                                               |
| Name search returns many similar-scoring results                                  | List the top few and ask the user to disambiguate — never pick one arbitrarily                                                                                                                  |
| Network/timeout error                                                             | Retry once. If it fails again, tell the user the ABR service couldn't be reached and suggest checking https://abr.business.gov.au directly                                                      |
| Checking many ABNs in a loop                                                      | Space out calls (the ABR does not publish a hard rate limit, but a ~150–200ms pause between calls is good practice for fair use)                                                                |

## Output format

Present results to the user as a short, plain-language summary — not a raw JSON
dump. A good structure:

```
Entity: <entityName>
ABN: <abn> (<abnStatus> since <effective date if available>)
Entity type: <entityTypeName>
GST registered: <Yes, since <date> | No>
Location: <addressState> <addressPostcode>
Business/trading names: <comma-separated list, or "none registered">

Result: <one-line plain-English verdict — e.g. "This ABN is currently active and
the entity is GST-registered, so it can legitimately charge GST on invoices." or
"This ABN exists but its status is Cancelled — it is not currently an active
registration.">

Source: Australian Business Register (abr.business.gov.au), live lookup.
```

For a "No records found" result, say plainly that no entity matches the given
ABN/ACN on the ABR, and suggest the user double-check the number with the business.

## Reference files

- `reference/api-reference.md` — full ABR JSON API endpoint reference: request
  parameters, every response field, the JSONP format, and the complete error
  message table. Read this if you hit an error message not covered above, or need
  a field not listed in Step 5.
- `reference/entity-types.md` — common ABR entity type codes (`PRV`, `IND`, `TRT`,
  etc.) and what they mean. The API also returns the full English description
  (`entityTypeName`), so this is rarely needed, but useful for codes you don't
  recognise.
- `examples/sample-responses.md` — illustrative example responses (active entity,
  cancelled ABN, GST-registered vs not, name search, and each error case) showing
  exactly what `scripts/abn_lookup.py` returns for each.
- `scripts/abn_lookup.py` — the helper script used in Steps 2 and 4. Pure Python 3
  standard library, no extra dependencies required.

# ABR JSON API Reference

This file documents the underlying Australian Business Register (ABR) JSON API
that `scripts/abn_lookup.py` calls. Read this when you need a field, error
message, or detail not covered in `SKILL.md`.

Source: https://abr.business.gov.au/Tools/WebServices and
https://abr.business.gov.au/Documentation/* (ABN Lookup web services user guide).

## Authentication

Every request requires a `guid` query parameter — the free authentication GUID
issued when registering at https://abr.business.gov.au/Tools/WebServices. There is
no cost and no published usage charge. The script reads this from the `ABR_GUID`
environment variable; it is never hardcoded or printed.

## Base URL and endpoints

Base: `https://abr.business.gov.au/json/`

| Endpoint             | Purpose                                                                             | Key parameters                           |
| -------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------- |
| `AbnDetails.aspx`    | Full detail for a single ABN                                                        | `abn` (11 digits), `guid`, `callback`    |
| `AcnDetails.aspx`    | Full detail for a single ACN (returns the same response shape as `AbnDetails.aspx`) | `acn` (9 digits), `guid`, `callback`     |
| `MatchingNames.aspx` | Ranked list of entities matching a name                                             | `name`, `guid`, `maxResults`, `callback` |

All requests are simple `GET` requests. The ABR's own JSON support is described
as "limited" — it covers ABN/ACN/name search only (no postcode-only search, no
historical detail, no business-name register search beyond what's attached to an
ABN).

### Example request URLs

```
https://abr.business.gov.au/json/AbnDetails.aspx?abn=51824753556&guid=YOUR_GUID&callback=callback
https://abr.business.gov.au/json/AcnDetails.aspx?acn=102417032&guid=YOUR_GUID&callback=callback
https://abr.business.gov.au/json/MatchingNames.aspx?name=Acme+Consulting&guid=YOUR_GUID&maxResults=10&callback=callback
```

## Response format: JSONP

The API returns **JSONP**, not plain JSON — the body is the `callback` parameter's
value followed by the JSON payload in parentheses, e.g.:

```
callback({"Abn":"51824753556","AbnStatus":"Active", ... })
```

`scripts/abn_lookup.py` strips this wrapper automatically (`strip_jsonp`) and
returns plain JSON. If you ever call the endpoint directly (e.g. for debugging),
remember to strip the `callback(` prefix and trailing `)` before parsing as JSON.

The JSON API has **no pagination** — `maxResults` caps the number of name-search
results returned in one call (ABR's documented limit is up to 200; the script
defaults to 10 and clamps the requested value to 1–200).

## `AbnDetails.aspx` / `AcnDetails.aspx` response fields

Both endpoints return the same field set. `scripts/abn_lookup.py` maps these into
the cleaner `summary`/lowercase fields described in `SKILL.md`; this table covers
the raw ABR field names in case you need to inspect them directly.

| Raw field         | Type                         | Description                                                                                |
| ----------------- | ---------------------------- | ------------------------------------------------------------------------------------------ |
| `Abn`             | string                       | The 11-digit ABN (no spaces)                                                               |
| `Acn`             | string                       | The 9-digit ACN, if the entity is a company. Empty for sole traders, trusts, partnerships  |
| `AbnStatus`       | string                       | `"Active"` or `"Cancelled"`                                                                |
| `AddressDate`     | string (YYYY-MM-DD)          | Date the main business address was last updated                                            |
| `AddressState`    | string                       | State/territory of the main business location (e.g. `NSW`, `VIC`)                          |
| `AddressPostcode` | string                       | Postcode of the main business location                                                     |
| `EntityName`      | string                       | The registered legal entity name                                                           |
| `EntityTypeCode`  | string                       | 3-letter ABR entity type code (e.g. `PRV`, `IND`) — see `entity-types.md`                  |
| `EntityTypeName`  | string                       | Full English description of the entity type                                                |
| `BusinessName`    | array of strings             | Registered business names and/or trading names linked to this ABN. Can be empty            |
| `Gst`             | string (YYYY-MM-DD) or empty | Date GST registration took effect. Empty/absent means **not currently registered for GST** |
| `Message`         | string                       | Empty on success. Non-empty = an error/exception (see table below)                         |

Notes:

- A `BusinessName` entry being absent does **not** mean the entity has no trading
  presence — many sole traders and companies operate solely under their
  `EntityName` with no separate registered business name.
- `Gst` being empty does not mean the entity has _never_ been GST registered —
  only that it is not _currently_ registered. The JSON API does not expose GST
  registration history.
- The JSON API does not return officer, director, shareholder, or ABN history
  data. For that level of detail, the ABR points users to ASIC's company register
  (a separate service).

## `MatchingNames.aspx` response fields

| Raw field | Type             | Description                                    |
| --------- | ---------------- | ---------------------------------------------- |
| `Message` | string           | Empty on success, or an error/no-match message |
| `Names`   | array of objects | Candidate matches, described below             |

Each entry in `Names`:

| Field       | Type           | Description                                                                                                                                                                                                              |
| ----------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Abn`       | string         | ABN of the matched entity                                                                                                                                                                                                |
| `AbnStatus` | string         | Numeric/coded status indicator from the name-search index (treat `AbnStatus` from `AbnDetails.aspx` as authoritative for active/cancelled — if you need a definitive status, follow up with an `AbnDetails.aspx` lookup) |
| `Name`      | string         | The matched name text                                                                                                                                                                                                    |
| `NameType`  | string         | e.g. `"Entity Name"`, `"Business Name"`, `"Trading Name"`                                                                                                                                                                |
| `IsCurrent` | string/bool    | Whether this is the entity's currently-registered name                                                                                                                                                                   |
| `State`     | string         | State of the main business location                                                                                                                                                                                      |
| `Postcode`  | string         | Postcode of the main business location                                                                                                                                                                                   |
| `Score`     | number (0–100) | Relevance score — higher is a closer match                                                                                                                                                                               |

Because name search doesn't return `EntityTypeName` or `Gst`, always follow up
with an `AbnDetails.aspx` lookup (via `--abn`) on the chosen candidate before
reporting GST status or entity type to the user (see `SKILL.md` Step 6).

## Validation algorithms (used by `--validate`)

These run entirely locally — no network call — and catch typos before they reach
the ABR (which would otherwise respond with "Search text is not a valid ABN or
ACN").

**ABN (11 digits) — ATO modulus 89:**

1. Subtract 1 from the first digit
2. Multiply each of the 11 digits by its weight: `10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19`
3. Sum the products
4. Valid if the sum is evenly divisible by 89

**ACN (9 digits) — ASIC modulus 10:**

1. Multiply the first 8 digits by weights `8, 7, 6, 5, 4, 3, 2, 1`
2. Sum the products, take the remainder when divided by 10
3. The check digit (complement = `(10 - remainder) % 10`) must equal the 9th digit

Any 9-digit number can in principle be made into a valid ABN by prefixing a
checksum pair, which is why an ACN's last 9 digits commonly equal an Australian
company's ABN minus its 2-digit prefix.

## Error / exception messages (`Message` field)

If `Message` is non-empty, the lookup did not return entity data. Common messages
and how to respond:

| `Message` contains                                                                           | Meaning                                                                      | Suggested response                                                                                                                                         |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "No records found"                                                                           | The ABN/ACN/name has no match on the ABR                                     | State plainly that no entity matches this number/name on the register; suggest the user double-check it                                                    |
| "Search text is not a valid ABN or ACN"                                                      | The identifier failed format/checksum validation                             | Should be caught by `--validate` first; if it still occurs, ask the user to re-confirm the number                                                          |
| "The GUID entered is not recognised as a Registered Party"                                   | The configured `ABR_GUID` is invalid or not yet activated                    | This is a **setup problem**, not information about the business. Direct the user to re-check registration at https://abr.business.gov.au/Tools/WebServices |
| "The registration for the party identified by this GUID has been cancelled"                  | The GUID was valid but has since been revoked                                | Same as above — direct the user to re-register; contact `ABNLookup.Support@industry.gov.au` if needed                                                      |
| "No name search criteria entered" / "Name search type cannot be determined"                  | Empty or unusable search string                                              | Ask the user for a clearer business name                                                                                                                   |
| "An ABN is invalid in Name Search" / "An ACN is invalid in Name Search"                      | The user passed a number into `--name` — re-run with `--abn`/`--acn` instead | Re-run with the correct flag                                                                                                                               |
| HTTP-level errors (404/500) or "System problems have prevented this request from completing" | ABR service issue                                                            | Retry once; if it persists, tell the user the government service is temporarily unreachable                                                                |

## Fair use / rate limits

The ABR does not publish a hard numeric rate limit for the JSON API, but the web
services agreement is a fair-use agreement, not an unlimited-bulk-scraping
license. When checking many ABNs in sequence:

- Make one request per ABN/ACN/name (the script already does this)
- Add a short pause (roughly 150–200ms) between consecutive calls in a loop
- Avoid re-querying the same ABN repeatedly in a short window — cache the result
  for the duration of the user's task instead of re-fetching

# ABN Business Verification

A small AI skill for checking whether an Australian business is registered and active on the **Australian Business Register (ABR)** using an **ABN**, **ACN**, or business/entity name.

## What it does

This skill queries the official Australian Government ABR JSON API directly and can return:

- registered entity name
- ABN status (`Active` / `Cancelled`)
- entity type
- GST registration status and date
- state and postcode
- registered business/trading names
- ranked matches for name searches

It is **read-only** and does not register or modify any ABN.

## When to use

Use this skill when a user wants to:

- verify or validate an ABN or ACN
- check whether a business is real, registered, active, or GST-registered
- confirm supplier / vendor details before payment or onboarding
- perform BAS, tax invoice, KYC, or compliance checks for Australian businesses

## Prerequisite

The ABR API requires a free GUID from the Australian Government.

1. Register at: `https://abr.business.gov.au/Tools/WebServices`
2. Set the GUID as the environment variable `ABR_GUID`
3. Do **not** hardcode or log the GUID

If `ABR_GUID` is missing, the script returns a clear setup error.

## Usage

### Validate locally (no API call)

```bash
python3 scripts/abn_lookup.py --validate "51 824 753 556"
```

### Look up by ABN

```bash
python3 scripts/abn_lookup.py --abn 51824753556
```

### Look up by ACN

```bash
python3 scripts/abn_lookup.py --acn 102417032
```

### Search by business / entity name

```bash
python3 scripts/abn_lookup.py --name "Acme Consulting" --max-results 10
```

## Script output

The script prints JSON to stdout. For ABN / ACN lookups, the response includes a `summary` object with:

- `verdict`
- `gstRegistered`
- `canChargeGst`

For name searches, the response includes a ranked `names` list.

## Files in this skill

- `Skill.md` — primary skill instructions
- `scripts/abn_lookup.py` — Python helper script
- `reference/api-reference.md` — ABR API field and error reference
- `reference/entity-types.md` — common entity type codes
- `examples/sample-responses.md` — example outputs

## Notes

- The ABR API is a live government data source.
- This skill is for verification only and does not perform registrations or updates.
- Keep `ABR_GUID` out of version control and logs.

## License

MIT


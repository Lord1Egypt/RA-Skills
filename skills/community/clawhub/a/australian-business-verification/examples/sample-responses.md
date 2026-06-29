# Example Responses

These are **illustrative** examples of what `scripts/abn_lookup.py` prints for
each scenario. ABN/ACN numbers, names, and dates below are fictional and used only
to show the response shape — they are not real lookups.

## 1. Active company, GST registered

```bash
python3 scripts/abn_lookup.py --abn 51824753556
```

```json
{
  "summary": {
    "verdict": "active",
    "gstRegistered": true,
    "canChargeGst": true
  },
  "message": "",
  "abn": "51824753556",
  "acn": "824753556",
  "entityName": "EXAMPLE TECHNOLOGY SOLUTIONS PTY LTD",
  "entityTypeCode": "PRV",
  "entityTypeName": "Australian Private Company",
  "abnStatus": "Active",
  "gst": "2018-07-01",
  "addressState": "VIC",
  "addressPostcode": "3000",
  "addressDate": "2021-03-15",
  "businessName": ["EXAMPLE TECH"]
}
```

**Suggested summary to the user:**

> EXAMPLE TECHNOLOGY SOLUTIONS PTY LTD — ABN 51 824 753 556 is currently **Active**.
> It's an Australian Private Company (ACN 824 753 556), GST-registered since
> 1 July 2018, based in Melbourne VIC 3000. It trades as "EXAMPLE TECH". This
> entity is registered and can legitimately charge GST on invoices.

## 2. Active sole trader, not GST registered

```bash
python3 scripts/abn_lookup.py --abn 65000000001
```

```json
{
  "summary": {
    "verdict": "active",
    "gstRegistered": false,
    "canChargeGst": false
  },
  "message": "",
  "abn": "65000000001",
  "acn": null,
  "entityName": "JANE EXAMPLE",
  "entityTypeCode": "IND",
  "entityTypeName": "Individual/Sole Trader",
  "abnStatus": "Active",
  "gst": "",
  "addressState": "QLD",
  "addressPostcode": "4000",
  "addressDate": "2022-11-02",
  "businessName": ["JANE'S BOOKKEEPING SERVICES"]
}
```

**Suggested summary to the user:**

> JANE EXAMPLE — ABN 65 000 000 001 is **Active** as a sole trader (Individual/Sole
> Trader), trading as "JANE'S BOOKKEEPING SERVICES" in QLD 4000. This entity is
> **not currently registered for GST** — any invoice should not include GST
> unless their registration status changes.

## 3. Cancelled ABN

```bash
python3 scripts/abn_lookup.py --abn 12000000003
```

```json
{
  "summary": {
    "verdict": "cancelled",
    "gstRegistered": false,
    "canChargeGst": false
  },
  "message": "",
  "abn": "12000000003",
  "acn": "000000003",
  "entityName": "OLD VENTURE PTY LTD",
  "entityTypeCode": "PRV",
  "entityTypeName": "Australian Private Company",
  "abnStatus": "Cancelled",
  "gst": "",
  "addressState": "NSW",
  "addressPostcode": "2000",
  "addressDate": "2019-05-20",
  "businessName": []
}
```

**Suggested summary to the user:**

> OLD VENTURE PTY LTD — ABN 12 000 000 003 exists on the register but its status
> is **Cancelled**. This is not currently an active ABN registration — it should
> not be treated as a verified, active business without further checks.

## 4. ABN not found

```bash
python3 scripts/abn_lookup.py --abn 11111111111
```

```json
{
  "summary": {
    "verdict": "not_found",
    "gstRegistered": false,
    "canChargeGst": false
  },
  "message": "No records found",
  "abn": null,
  "acn": null,
  "entityName": null,
  "entityTypeCode": null,
  "entityTypeName": null,
  "abnStatus": "",
  "gst": null,
  "addressState": null,
  "addressPostcode": null,
  "addressDate": null,
  "businessName": []
}
```

**Suggested summary to the user:**

> No entity matches ABN 11 111 111 111 on the Australian Business Register. This
> ABN does not appear to be registered — double-check the number with the
> business directly.

## 5. Invalid GUID (setup problem, not a business problem)

```bash
python3 scripts/abn_lookup.py --abn 51824753556
```

```json
{
  "summary": {
    "verdict": "error",
    "gstRegistered": false,
    "canChargeGst": false
  },
  "message": "The GUID entered is not recognised as a Registered Party",
  "abn": null,
  "acn": null,
  "entityName": null,
  "entityTypeCode": null,
  "entityTypeName": null,
  "abnStatus": "",
  "gst": null,
  "addressState": null,
  "addressPostcode": null,
  "addressDate": null,
  "businessName": []
}
```

**Suggested response to the user:**

> I can't complete this lookup yet — the configured ABR API GUID isn't recognised.
> This is a setup issue on our end, not a problem with the ABN you gave me.
> Re-check the GUID from your registration email, or re-register for free at
> https://abr.business.gov.au/Tools/WebServices.

## 6. Name search with multiple candidates

```bash
python3 scripts/abn_lookup.py --name "Example Plumbing" --max-results 5
```

```json
{
  "summary": {
    "verdict": "ok",
    "resultCount": 3
  },
  "message": "",
  "names": [
    {
      "abn": "23000000004",
      "abnStatus": "0000000001",
      "name": "EXAMPLE PLUMBING PTY LTD",
      "nameType": "Entity Name",
      "isCurrent": "Y",
      "state": "NSW",
      "postcode": "2150",
      "score": 100
    },
    {
      "abn": "34000000005",
      "abnStatus": "0000000001",
      "name": "EXAMPLE PLUMBING & GAS SERVICES",
      "nameType": "Business Name",
      "isCurrent": "Y",
      "state": "NSW",
      "postcode": "2200",
      "score": 87
    },
    {
      "abn": "45000000006",
      "abnStatus": "0000000001",
      "name": "GREATER EXAMPLE PLUMBING GROUP",
      "nameType": "Trading Name",
      "isCurrent": "Y",
      "state": "VIC",
      "postcode": "3121",
      "score": 71
    }
  ]
}
```

**Suggested response to the user:**

> I found a few businesses matching "Example Plumbing":
>
> 1. **EXAMPLE PLUMBING PTY LTD** — ABN 23 000 000 004, NSW 2150 (best match)
> 2. EXAMPLE PLUMBING & GAS SERVICES — ABN 34 000 000 005, NSW 2200
> 3. GREATER EXAMPLE PLUMBING GROUP — ABN 45 000 000 006, VIC 3121
>
> Which one did you mean? Once you confirm, I'll pull the full registration and
> GST details for that ABN.

Note: `AbnStatus` inside a **name search** result is a coded status indicator from
the search index, not the human-readable `"Active"`/`"Cancelled"` string returned
by `AbnDetails.aspx`. Always confirm active/cancelled status via a follow-up
`--abn` lookup, as shown in `SKILL.md` Step 6.

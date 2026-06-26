# Holiday File Format

When using the FIDIC Deadline Calculator with a non-Singapore seat, you must supply your own holiday data file via `--holidays-file`. This document describes the required JSON schema.

## Schema

```json
{
  "_meta": {
    "country": "Country Name",
    "iso": "XX",
    "source": "Description of your authoritative source",
    "last_verified": "YYYY-MM-DD",
    "notes": "Any caveats (moon sighting, regional variations, etc.)",
    "weekend": ["Sat", "Sun"],
    "in_lieu_rule": "none"
  },
  "2026": {
    "source": "Specific gazette/legislation reference for this year",
    "url": "URL to authoritative source",
    "dates": ["2026-01-01", "2026-04-03", "..."],
    "names": ["New Year's Day", "Good Friday", "..."]
  }
}
```

## Field reference

### `_meta` (required)

| Field | Required | Description |
|-------|----------|-------------|
| `country` | Yes | Human-readable country name |
| `iso` | Yes | ISO 3166-1 alpha-2 code (e.g. `GB`, `AE`, `MY`) |
| `source` | Yes | Name of the authoritative source you used |
| `last_verified` | Yes | Date you last verified this data (YYYY-MM-DD) |
| `notes` | No | Caveats — moon sighting, sub-national scope, etc. |
| `weekend` | No | Array of weekend day names. Default: `["Sat", "Sun"]`. Use `["Fri", "Sat"]` for UAE. |
| `in_lieu_rule` | No | One of: `none`, `auto_sunday_to_monday`, `rest_day_replacement`, `substitute_next_working_day`. Default: `none`. |

### Year entries (one per year)

| Field | Required | Description |
|-------|----------|-------------|
| `source` | Yes | Specific gazette or decree reference for this year |
| `url` | No | URL to the authoritative source document |
| `dates` | Yes | Array of date strings in `YYYY-MM-DD` format |
| `names` | No | Array of holiday names (same order as `dates`) |

## In-lieu rules

| Rule | Behaviour |
|------|-----------|
| `none` | No automatic substitution. List substitute days explicitly in `dates`. |
| `auto_sunday_to_monday` | PH falling on Sunday → Monday is automatically treated as in-lieu. (Singapore statutory rule.) |
| `rest_day_replacement` | PH falling on a weekend → next working day is in-lieu. Only applies in `exclude_ph` mode. |
| `substitute_next_working_day` | Same as `rest_day_replacement`. Used for UK-style substitution. |

If your jurisdiction has an in-lieu rule but you're unsure how to model it, set `in_lieu_rule` to `none` and list all substitute holidays explicitly in the `dates` array. This is always safe.

## Worked example: UK England & Wales 2026

Source: [gov.uk/bank-holidays](https://www.gov.uk/bank-holidays) (England and Wales), accessed 2026-05-10.

```json
{
  "_meta": {
    "country": "United Kingdom (England & Wales)",
    "iso": "GB",
    "source": "gov.uk/bank-holidays — England and Wales",
    "last_verified": "2026-05-10",
    "notes": "England & Wales only. Scotland and Northern Ireland have different bank holidays. Does NOT cover local/regional holidays.",
    "weekend": ["Sat", "Sun"],
    "in_lieu_rule": "substitute_next_working_day"
  },
  "2026": {
    "source": "gov.uk/bank-holidays England and Wales 2026",
    "url": "https://www.gov.uk/bank-holidays",
    "dates": [
      "2026-01-01",
      "2026-04-03",
      "2026-04-06",
      "2026-05-04",
      "2026-05-25",
      "2026-08-31",
      "2026-12-25",
      "2026-12-28"
    ],
    "names": [
      "New Year's Day",
      "Good Friday",
      "Easter Monday",
      "Early May bank holiday",
      "Spring bank holiday",
      "Summer bank holiday",
      "Christmas Day",
      "Boxing Day (substitute: 28 Dec, as 26 Dec is Saturday)"
    ]
  }
}
```

> **Note:** The 2026-12-28 entry is the substitute for Boxing Day (26 Dec falls on Saturday). Because `in_lieu_rule` is set to `substitute_next_working_day`, the tool will also auto-derive substitutes — so you could omit 2026-12-28 and let the rule handle it. Including it explicitly is safer and more transparent.

## How to use

```bash
# Save your file (e.g. gb_holidays.json), then:
python3 scripts/fidic_deadline.py --seat GB --trigger 2026-04-01 --period 14 --mode exclude_ph --holidays-file gb_holidays.json
```

## Source recommendations by jurisdiction

| Jurisdiction | Authoritative source |
|-------------|---------------------|
| Singapore | MOM gazette / eGazette (bundled — no file needed) |
| UAE | FAHR decree (shuraa.ae) |
| Malaysia (federal) | kabinet.gov.my / Jadual Hari Kelepasan Am |
| UK (England & Wales) | gov.uk/bank-holidays |
| Hong Kong | gov.hk General Holidays Ordinance |
| Australia (state-specific) | Your state's gazette |

For any jurisdiction: find your country's official gazette or ministry of manpower/labour equivalent. Do not rely on third-party holiday aggregator websites.

## Important caveats

1. **The year matters.** Moon-sighting holidays (Hari Raya, Eid, Vesak in some calendars) are gazetted close to the date. Any data for future years is a prediction until officially confirmed.

2. **The sub-jurisdiction matters.** "MY" is one file, but Malaysian state holidays vary. "GB" covers England & Wales only — not Scotland. "AE" is federal only — individual emirate observances differ. Your contract's governing law determines which calendar applies.

3. **Verify before reliance.** This tool is a workflow aid. The deadline it produces is only as good as the holiday data you feed it.

---
name: companies-house-cli
description: UK Companies House CLI — search companies, profiles, officers, filings, PSC, charges, insolvency, and agent-friendly JSON output aligned with rail-cli and tfl-cli. Use when looking up UK company records, directors, filing history, beneficial owners, charges, insolvency, or when an agent needs stable JSON envelopes with `ok`, `schemaVersion`, `command`, `requestedAt`, and nested `data.input` / `data.pagination`.
homepage: https://ch-cli.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["ch"] },
        "primaryEnv": "COMPANIES_HOUSE_API_KEY",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/companies-house-cli",
              "bins": ["ch"],
              "label": "Install companies-house-cli (npm)",
            },
          ],
      },
  }
---

# companies-house-cli

Use `ch` for UK Companies House data: company search, profiles, officers, filings, PSC, charges, and insolvency.

Setup

- `npm install -g @shan8851/companies-house-cli`
- Get a free API key: https://developer.company-information.service.gov.uk/
- `export COMPANIES_HOUSE_API_KEY=your_key` or add it to a local `.env`

Search

- By name: `ch search "Revolut"`
- With restrictions: `ch search "Revolut" --restrictions active-companies`
- Fetch all pages: `ch search "Revolut" --all`
- JSON in canonical style: `ch search "Revolut" --json`

Company Profile

- By number: `ch info 09215862`
- Force text: `ch info 09215862 --text`
- Short numbers auto-pad: `ch info 9215862` becomes `09215862`

Officers

- List directors/secretaries: `ch officers 09215862`
- All officers: `ch officers 09215862 --all`
- Order by: `ch officers 09215862 --order-by appointed_on`

Filings

- Filing history: `ch filings 09215862`
- Filter by type: `ch filings 09215862 --type accounts`
- Include document download links: `ch filings 09215862 --type accounts --include-links`
- All filings: `ch filings 09215862 --all`

PSC (Beneficial Owners)

- List PSC records: `ch psc 09215862`
- All records: `ch psc 09215862 --all`

Search Person

- Find a person across UK companies: `ch search-person "Nik Storonsky"`
- Limit enrichment fan-out: `ch search-person "Nik Storonsky" --match-limit 5`
- Fetch all search pages: `ch search-person "Nik Storonsky" --all`

Charges

- List company charges: `ch charges 09215862`
- All charges: `ch charges 09215862 --all`

Insolvency

- Check insolvency history: `ch insolvency 09215862`
- Returns empty result cleanly if no history exists (not an error)

Pagination

- List commands support: `--items-per-page <n>`, `--start-index <n>`, `--all`
- `--all` fetches every page automatically
- `--all` and non-zero `--start-index` cannot be combined

Output

- Defaults to text in a TTY and JSON when piped
- Canonical usage is subcommand-local flags: `ch search "Revolut" --json`, `ch info 09215862 --text`
- Root compatibility aliases still work: `ch --json search "Revolut"`, `ch --text info 09215862`
- Success envelope: `{ ok, schemaVersion, command, requestedAt, data }`
- Error envelope: `{ ok, schemaVersion, command, requestedAt, error }`
- Command metadata now lives under `data.input` and `data.pagination`
- Disable colour: `ch --no-color search "Revolut"`

Agent Notes

- JSON mode writes handled errors to stdout, not stderr
- Error payloads include `code`, `message`, and `retryable`
- Exit codes are explicit:
  - `0` success
  - `2` bad input or not found
  - `3` auth, upstream, or rate-limit failures
  - `4` internal failures
- Update any existing parsers that expected top-level `input` or `pagination`; those now live under `data`

Notes

- API key required (free, instant signup at Companies House developer portal)
- Auth is HTTP Basic (key as username, blank password)
- Rate limit: 600 requests per 5 minutes
- Company numbers are automatically zero-padded to 8 digits
- `search-person` fans out appointment requests for each match — use `--match-limit` on broad names to control API usage
- `--include-links` on filings derives document content URLs for direct PDF download

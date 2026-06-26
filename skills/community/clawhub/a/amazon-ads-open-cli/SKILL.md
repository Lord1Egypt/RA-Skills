---
name: amazon-ads-open-cli
description: >
  Amazon Ads data retrieval and reporting via amazon-ads-open-cli.
  Use when the user wants to check Amazon ad performance, pull Sponsored Products/Brands/Display stats,
  explore campaign structure, inspect DSP orders, manage audiences, or generate async performance reports.
  Triggers: "Amazon Ads", "Sponsored Products", "Sponsored Brands", "Sponsored Display", "Amazon DSP",
  "Amazon ad performance", "Amazon campaign stats", "Amazon ad spend", "Amazon PPC", "Amazon keywords",
  "Amazon targets", "Amazon audiences", "Amazon brand safety", "Amazon ad report".
---

# Amazon Ads CLI Skill

You have access to `amazon-ads-open-cli`, a read-only CLI for the Amazon Advertising API (v2/v3). Use it to list advertising profiles, inspect Sponsored Products/Brands/Display campaigns and their hierarchy, browse DSP orders and creatives, manage audiences, and request async performance reports across Amazon marketplaces.

## Quick start

```bash
# Check if the CLI is available
amazon-ads-open-cli --help

# List advertising profiles (marketplaces)
amazon-ads-open-cli profiles

# List Sponsored Products campaigns
amazon-ads-open-cli sp-campaigns
```

If the CLI is not installed, install it:

```bash
npm install -g amazon-ads-open-cli
```

## Authentication

The CLI requires an Amazon OAuth2 **access token** and **client ID** from a Login with Amazon app. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command) -- reads the specified JSON file
2. Auto-detected file: `~/.config/amazon-ads-open-cli/credentials.json`
3. Environment variables: `AMAZON_ADS_ACCESS_TOKEN` + `AMAZON_ADS_CLIENT_ID`

Note: when a credentials file is found (either via `--credentials` or at the default path), its `profile_id` can be overridden by the `AMAZON_ADS_PROFILE_ID` environment variable if the file does not contain one. If the credentials file is not found or does not contain valid `access_token` + `client_id`, the CLI falls through to environment variables.

The credentials JSON file format:

```json
{
  "access_token": "your_access_token",
  "client_id": "your_client_id",
  "profile_id": "your_profile_id"
}
```

Environment variables:

- `AMAZON_ADS_ACCESS_TOKEN` -- OAuth2 access token
- `AMAZON_ADS_CLIENT_ID` -- Login with Amazon client ID
- `AMAZON_ADS_PROFILE_ID` -- marketplace profile ID (required for most commands)

Before running any command, verify credentials are configured by running `amazon-ads-open-cli profiles`. If it fails with a credentials error, ask the user to set up authentication.

Most commands require a **profile ID** (marketplace-specific). Use the `profiles` command first to discover profile IDs, then set `AMAZON_ADS_PROFILE_ID`.

## Entity hierarchy

```
Profile (marketplace: US, UK, DE, JP, etc.)
 +-- Sponsored Products
 |    +-- Campaign -> Ad Group -> Product Ad / Keyword / Target
 +-- Sponsored Brands
 |    +-- Campaign -> Ad Group -> Keyword / Target
 +-- Sponsored Display
 |    +-- Campaign -> Ad Group -> Product Ad / Target
 +-- DSP (programmatic)
      +-- Advertiser -> Order -> Line Item -> Creative
      +-- Audience (configured at Line Item level)
```

## Output format

All commands output pretty-printed JSON (2-space indent) by default. Use `--format compact` for single-line JSON (useful for piping).

Global options available on every command:

- `--format <format>` -- output format: `json` (default) or `compact`
- `--credentials <path>` -- path to credentials JSON file

All listing commands support offset-based pagination via `--start-index` and `--count` parameters.

## Commands reference

### Profiles

```bash
# List all advertising profiles (marketplaces) -- no profile ID required
amazon-ads-open-cli profiles

# Get a specific profile -- no profile ID required
amazon-ads-open-cli profile 1234567890
```

The `profiles` and `profile` commands do not require `AMAZON_ADS_PROFILE_ID` to be set. All other commands do.

### Sponsored Products campaigns

```bash
# List SP campaigns
amazon-ads-open-cli sp-campaigns
amazon-ads-open-cli sp-campaigns --state enabled
amazon-ads-open-cli sp-campaigns --start-index 100 --count 50

# Get a specific SP campaign
amazon-ads-open-cli sp-campaign 123456
```

Options for `sp-campaigns`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100, max 5000)
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Brands campaigns

```bash
# List SB campaigns
amazon-ads-open-cli sb-campaigns
amazon-ads-open-cli sb-campaigns --state paused

# Get a specific SB campaign
amazon-ads-open-cli sb-campaign 123456
```

Options for `sb-campaigns`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Display campaigns

```bash
# List SD campaigns
amazon-ads-open-cli sd-campaigns
amazon-ads-open-cli sd-campaigns --state enabled

# Get a specific SD campaign
amazon-ads-open-cli sd-campaign 123456
```

Options for `sd-campaigns`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Products ad groups

```bash
# List SP ad groups
amazon-ads-open-cli sp-adgroups
amazon-ads-open-cli sp-adgroups --campaign-id 123456 --state enabled

# Get a specific SP ad group
amazon-ads-open-cli sp-adgroup 789012
```

Options for `sp-adgroups`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--campaign-id <id>` -- filter by campaign ID
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Brands ad groups

```bash
# List SB ad groups
amazon-ads-open-cli sb-adgroups
amazon-ads-open-cli sb-adgroups --start-index 0 --count 50
```

Options for `sb-adgroups`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

Note: `sb-adgroups` does not support `--campaign-id` or `--state` filtering.

### Sponsored Display ad groups

```bash
# List SD ad groups
amazon-ads-open-cli sd-adgroups
amazon-ads-open-cli sd-adgroups --campaign-id 123456
```

Options for `sd-adgroups`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--campaign-id <id>` -- filter by campaign ID

Note: `sd-adgroups` does not support `--state` filtering.

### Sponsored Products ads

```bash
# List SP product ads
amazon-ads-open-cli sp-ads
amazon-ads-open-cli sp-ads --adgroup-id 789012 --state enabled

# Get a specific SP ad
amazon-ads-open-cli sp-ad 345678
```

Options for `sp-ads`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Display ads

```bash
# List SD ads
amazon-ads-open-cli sd-ads
amazon-ads-open-cli sd-ads --adgroup-id 789012
```

Options for `sd-ads`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID

Note: `sd-ads` does not support `--state` filtering.

### Sponsored Products keywords

```bash
# List SP keywords
amazon-ads-open-cli sp-keywords
amazon-ads-open-cli sp-keywords --campaign-id 123456 --state enabled
amazon-ads-open-cli sp-keywords --adgroup-id 789012
```

Options for `sp-keywords`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID
- `--campaign-id <id>` -- filter by campaign ID
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Products negative keywords

```bash
# List SP negative keywords
amazon-ads-open-cli sp-negative-keywords
amazon-ads-open-cli sp-negative-keywords --campaign-id 123456
amazon-ads-open-cli sp-negative-keywords --adgroup-id 789012
```

Options for `sp-negative-keywords`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID
- `--campaign-id <id>` -- filter by campaign ID

Note: `sp-negative-keywords` does not support `--state` filtering.

### Sponsored Products targets

```bash
# List SP product targets (ASIN and category targeting)
amazon-ads-open-cli sp-targets
amazon-ads-open-cli sp-targets --adgroup-id 789012 --state enabled
```

Options for `sp-targets`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID
- `--state <state>` -- filter by state: `enabled`, `paused`, `archived`

### Sponsored Brands targets

```bash
# List SB targets
amazon-ads-open-cli sb-targets
amazon-ads-open-cli sb-targets --start-index 0 --count 50
```

Options for `sb-targets`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

Note: `sb-targets` does not support `--adgroup-id` or `--state` filtering.

### Sponsored Display targets

```bash
# List SD targets
amazon-ads-open-cli sd-targets
amazon-ads-open-cli sd-targets --adgroup-id 789012
```

Options for `sd-targets`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)
- `--adgroup-id <id>` -- filter by ad group ID

Note: `sd-targets` does not support `--state` filtering.

### Performance reports (async)

Reports are requested asynchronously. You submit a report request and receive a report ID, then poll for completion.

#### Sponsored Products report

```bash
amazon-ads-open-cli sp-report --record-type campaigns --start-date 20260101
amazon-ads-open-cli sp-report --record-type keywords --start-date 20260101 --metrics impressions,clicks,cost,sales14d
```

Options for `sp-report`:
- `--record-type <type>` -- **required**: `campaigns`, `adGroups`, `productAds`, `keywords`, `targets`
- `--start-date <date>` -- **required**: report date in YYYYMMDD format
- `--metrics <metrics>` -- comma-separated metric names (default: `impressions,clicks,cost,sales14d`)

#### Sponsored Brands report

```bash
amazon-ads-open-cli sb-report --record-type campaigns --start-date 20260101
amazon-ads-open-cli sb-report --record-type keywords --start-date 20260101 --metrics impressions,clicks,cost
```

Options for `sb-report`:
- `--record-type <type>` -- **required**: `campaigns`, `adGroups`, `keywords`
- `--start-date <date>` -- **required**: report date in YYYYMMDD format
- `--metrics <metrics>` -- comma-separated metric names (default: `impressions,clicks,cost`)

#### Sponsored Display report

```bash
amazon-ads-open-cli sd-report --record-type campaigns --start-date 20260101
amazon-ads-open-cli sd-report --record-type targets --start-date 20260101 --metrics impressions,clicks,cost
```

Options for `sd-report`:
- `--record-type <type>` -- **required**: `campaigns`, `adGroups`, `productAds`, `targets`
- `--start-date <date>` -- **required**: report date in YYYYMMDD format
- `--metrics <metrics>` -- comma-separated metric names (default: `impressions,clicks,cost`)

#### Report status

```bash
# Check report status and get download URL
amazon-ads-open-cli report-status amzn1.report.abc123
```

The response includes the report status and, when complete, a download URL. Poll this command until the status indicates the report is ready.

### DSP orders

```bash
# List DSP orders (programmatic display/video)
amazon-ads-open-cli dsp-orders
amazon-ads-open-cli dsp-orders --start-index 0 --count 50

# Get a specific DSP order
amazon-ads-open-cli dsp-order 123456
```

Options for `dsp-orders`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

DSP commands use the v3 API endpoint.

### DSP line items

```bash
# List DSP line items
amazon-ads-open-cli dsp-line-items
amazon-ads-open-cli dsp-line-items --order-id 123456
```

Options for `dsp-line-items`:
- `--order-id <id>` -- filter by order ID
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

### DSP creatives

```bash
# List DSP creatives
amazon-ads-open-cli dsp-creatives
amazon-ads-open-cli dsp-creatives --start-index 0 --count 50
```

Options for `dsp-creatives`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

### Audiences

```bash
# List DSP audiences
amazon-ads-open-cli audiences
amazon-ads-open-cli audiences --start-index 0 --count 50

# Get a specific audience
amazon-ads-open-cli audience 123456
```

Options for `audiences`:
- `--start-index <n>` -- start index for pagination (default 0)
- `--count <n>` -- results per page (default 100)

### Brand safety

```bash
# List brand safety deny lists
amazon-ads-open-cli brand-safety-lists
```

The `brand-safety-lists` command has no pagination options. It returns all deny lists.

## Workflow guidance

### When the user asks for an account overview

1. Run `amazon-ads-open-cli profiles` to discover accessible marketplaces
2. Set the desired profile ID, then list campaigns across ad types:
   - `amazon-ads-open-cli sp-campaigns --state enabled`
   - `amazon-ads-open-cli sb-campaigns --state enabled`
   - `amazon-ads-open-cli sd-campaigns --state enabled`
3. Present campaign counts and statuses

### When the user asks for performance data

1. Use report commands to request async reports:
   - `amazon-ads-open-cli sp-report --record-type campaigns --start-date YYYYMMDD`
2. Poll with `amazon-ads-open-cli report-status <report-id>` until complete
3. Download and present the report data from the returned URL

### When the user asks about campaign structure

1. List campaigns: `amazon-ads-open-cli sp-campaigns`
2. Drill into ad groups: `amazon-ads-open-cli sp-adgroups --campaign-id <id>`
3. Inspect ads: `amazon-ads-open-cli sp-ads --adgroup-id <id>`
4. Review keywords: `amazon-ads-open-cli sp-keywords --adgroup-id <id>`
5. Check targets: `amazon-ads-open-cli sp-targets --adgroup-id <id>`

### When the user asks about keyword performance

1. List keywords: `amazon-ads-open-cli sp-keywords --campaign-id <id>`
2. Check negative keywords: `amazon-ads-open-cli sp-negative-keywords --campaign-id <id>`
3. Request a keyword-level report: `amazon-ads-open-cli sp-report --record-type keywords --start-date YYYYMMDD`

### When the user asks about DSP/programmatic

1. List orders: `amazon-ads-open-cli dsp-orders`
2. Drill into line items: `amazon-ads-open-cli dsp-line-items --order-id <id>`
3. Review creatives: `amazon-ads-open-cli dsp-creatives`
4. Check audiences: `amazon-ads-open-cli audiences`
5. Review brand safety: `amazon-ads-open-cli brand-safety-lists`

### When the user wants to compare ad types

1. Pull campaigns for each type side by side:
   - `amazon-ads-open-cli sp-campaigns --state enabled`
   - `amazon-ads-open-cli sb-campaigns --state enabled`
   - `amazon-ads-open-cli sd-campaigns --state enabled`
2. Request reports for each type with the same date range
3. Compare metrics across Sponsored Products, Brands, and Display

## Error handling

- **"No credentials found"** -- ask the user to set `AMAZON_ADS_ACCESS_TOKEN` + `AMAZON_ADS_CLIENT_ID` env vars, or create `~/.config/amazon-ads-open-cli/credentials.json`
- **"Profile ID required"** -- the command needs `AMAZON_ADS_PROFILE_ID`. Run `profiles` first to discover available profile IDs
- **HTTP 401** -- access token is expired or invalid; ask the user to refresh their OAuth token
- **HTTP 403** -- the profile may not have access to the requested resource, or the API scope is insufficient
- **"Unknown command"** -- verify the command name matches the reference above
- **Empty results** -- check that the profile ID corresponds to the correct marketplace and that campaigns/entities exist

All errors are output as JSON to stderr in the format: `{"error": "message"}`

## API documentation references

- [amazon-ads-open-cli documentation](https://github.com/Bin-Huang/amazon-ads-open-cli)
- [Amazon Ads API overview](https://advertising.amazon.com/API/docs/en-us/info/api-overview)
- [Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod)
- [Sponsored Brands API](https://advertising.amazon.com/API/docs/en-us/sponsored-brands/3-0/openapi)
- [Sponsored Display API](https://advertising.amazon.com/API/docs/en-us/sponsored-display/3-0/openapi)
- [Amazon DSP API](https://advertising.amazon.com/API/docs/en-us/dsp/openapi)

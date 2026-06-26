---
name: apple-ads-cli
description: >
  Apple Search Ads data analysis and reporting via apple-ads-cli.
  Use when the user wants to check Apple Search Ads performance, pull campaign/ad group/keyword stats,
  explore account structure, inspect ads and keywords, analyze budget orders, or check app eligibility.
  Triggers: "Apple Ads", "Apple Search Ads", "App Store ads", "apple ad performance", "apple campaign stats",
  "apple ad spend", "apple keyword report", "apple ads budget", "app eligibility", "search ads".
---

# Apple Ads CLI Skill

You have access to `apple-ads-cli`, a read-only CLI for the Apple Search Ads Campaign Management API (v5). Use it to query campaigns, ad groups, ads, keywords, budget orders, pull performance reports, and check app eligibility on the App Store.

## Quick start

```bash
# Check if the CLI is available
apple-ads-cli --help

# Get authenticated user info
apple-ads-cli me

# Get access control list (find your orgId)
apple-ads-cli acl
```

If the CLI is not installed, install it:

```bash
npm install -g apple-ads-cli
```

## Authentication

The CLI requires an **OAuth2 access token** and an **organization ID**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variables: `APPLE_ADS_ACCESS_TOKEN` + `APPLE_ADS_ORG_ID`
3. Auto-detected file: `~/.config/apple-ads-cli/credentials.json`

The credentials JSON file must contain `access_token` and `org_id` fields. The access token is obtained by signing a JWT with your private key (ES256) and exchanging it at Apple's OAuth endpoint. Tokens expire after 1 hour.

Before running any command, verify credentials are configured by running `apple-ads-cli me`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Organization (orgId)
 +-- Campaign
 |    +-- Ad Group
 |         +-- Ad
 |         +-- Targeting Keyword
 |         +-- Negative Keyword
 |    +-- Campaign-level Negative Keyword
 +-- Budget Order
 +-- App (by Adam ID)
```

Organization IDs are numeric identifiers shown in the Apple Search Ads UI. The `acl` command returns all organizations the user has access to.

## Monetary values

The Apple Search Ads API returns monetary values as objects with `amount` (string) and `currency` (string) fields, e.g. `{"amount": "12.34", "currency": "USD"}`. The amount is in the major currency unit -- no conversion needed.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

All listing commands support `--limit <n>` (default 20) and `--offset <n>` (default 0) for pagination. Single-entity commands (`me`, `acl`, `campaign`, `budget-order`, `app`, `app-eligibility`) do not support pagination.

## Commands reference

### Account discovery

```bash
# Access control list -- find your orgId and permissions
apple-ads-cli acl

# Authenticated user details (userId, parentOrgId)
apple-ads-cli me
```

### Apps

```bash
# Search for iOS apps to promote
apple-ads-cli search-apps "fitness"
apple-ads-cli search-apps "my app name" --return-own-apps --limit 10 --offset 0

# Check if an app is eligible for promotion
apple-ads-cli app-eligibility 123456789

# Get app details by Adam ID
apple-ads-cli app 123456789
```

`search-apps` options:
- `--return-own-apps` -- only return apps owned by the organization
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Campaigns

```bash
# List all campaigns
apple-ads-cli campaigns
apple-ads-cli campaigns --limit 50 --offset 0

# Get a specific campaign by ID
apple-ads-cli campaign 123456
```

`campaigns` options:
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Budget orders

```bash
# List all budget orders
apple-ads-cli budget-orders
apple-ads-cli budget-orders --limit 50 --offset 0

# Get a specific budget order by ID
apple-ads-cli budget-order 789012
```

`budget-orders` options:
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Ad groups

```bash
# List ad groups for a campaign
apple-ads-cli adgroups 123456
apple-ads-cli adgroups 123456 --limit 50 --offset 0
```

Options:
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Ads

```bash
# List ads for an ad group (requires both campaign ID and ad group ID)
apple-ads-cli ads 123456 789012
apple-ads-cli ads 123456 789012 --limit 50
```

Options:
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Keywords

```bash
# List targeting keywords for an ad group (requires campaign ID and ad group ID)
apple-ads-cli keywords 123456 789012
apple-ads-cli keywords 123456 789012 --limit 50

# List negative keywords for an ad group
apple-ads-cli negative-keywords 123456 789012
apple-ads-cli negative-keywords 123456 789012 --limit 50

# List campaign-level negative keywords
apple-ads-cli campaign-negative-keywords 123456
apple-ads-cli campaign-negative-keywords 123456 --limit 50
```

All keyword listing commands support:
- `--limit <n>` -- number of results (default 20)
- `--offset <n>` -- pagination offset (default 0)

### Reports

Report commands use POST requests to the Apple Search Ads reporting API. All report commands require `--start-date` and `--end-date`.

```bash
# Campaign-level performance report
apple-ads-cli report 123456 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15

# With granularity and grouping
apple-ads-cli report 123456 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --granularity DAILY \
  --group-by countryOrRegion,deviceClass

# Include records with zero metrics
apple-ads-cli report 123456 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --return-records-with-no-metrics

# Ad group-level report
apple-ads-cli report-adgroups 123456 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15

# Keyword-level report
apple-ads-cli report-keywords 123456 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --granularity WEEKLY
```

#### report (campaign-level)

Options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- HOURLY, DAILY, WEEKLY, MONTHLY (default DAILY)
- `--group-by <fields>` -- group by fields, comma-separated (e.g. countryOrRegion, deviceClass, ageRange, gender)
- `--return-records-with-no-metrics` -- include records with no metrics

#### report-adgroups (ad group-level)

Options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- HOURLY, DAILY, WEEKLY, MONTHLY (default DAILY)

#### report-keywords (keyword-level)

Options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- HOURLY, DAILY, WEEKLY, MONTHLY (default DAILY)

Note: `--group-by` and `--return-records-with-no-metrics` are only available on the `report` command (campaign-level), not on `report-adgroups` or `report-keywords`.

All reports use UTC timezone (hardcoded by the CLI; the Apple API supports other timezones like ORTZ), return row totals and grand totals, and have an internal pagination limit of 1000 rows. If a report has more than 1000 matching rows, results will be truncated.

## Workflow guidance

### When the user asks for a quick overview

1. Run `apple-ads-cli acl` to find the organization and verify access
2. Run `apple-ads-cli campaigns` to list all campaigns
3. Use `apple-ads-cli report <campaign-id> --start-date <date> --end-date <date>` for a performance snapshot

### When the user asks for deep analysis

1. Start with `report` at campaign level to identify overall performance
2. Use `report-adgroups` to break down by ad group within a campaign
3. Use `report-keywords` to identify top and bottom performing keywords
4. Add `--group-by countryOrRegion` or `--group-by deviceClass` for geographic or device segmentation
5. Add `--group-by ageRange,gender` for demographic breakdown
6. Use `--granularity DAILY` with `--group-by` to spot trends over time

### When the user asks about keyword performance

1. Use `report-keywords` to get keyword-level metrics for a campaign
2. Use `keywords <campaign-id> <adgroup-id>` to see keyword details (bid amounts, match type, status)
3. Use `negative-keywords` and `campaign-negative-keywords` to review exclusions

### When the user asks about app eligibility

1. Use `search-apps` to find the app and get its Adam ID
2. Use `app-eligibility <adam-id>` to check if it can run ads
3. Use `app <adam-id>` for detailed app information

### When the user asks about budget

1. Use `budget-orders` to list all budget orders
2. Use `budget-order <id>` for details on a specific budget order
3. Use `campaigns` and `campaign <id>` to check campaign-level budget settings

## Error handling

- **Authentication errors** -- ask the user to verify their access token (expires after 1 hour) and org_id
- **Missing credentials** -- the CLI checks for `access_token` and `org_id` in the credentials file; both are required
- **Empty results** -- check the date range, campaign status, and whether the organization has active campaigns
- **Invalid granularity** -- must be one of HOURLY, DAILY, WEEKLY, MONTHLY
- **Report errors** -- verify the campaign ID exists and the date range is valid (start before end)

## API documentation references

- [apple-ads-cli documentation](https://github.com/Bin-Huang/apple-ads-cli)
- [Apple Search Ads API overview](https://developer.apple.com/documentation/apple_ads)
- [OAuth setup guide](https://developer.apple.com/documentation/apple_ads/implementing-oauth-for-the-apple-search-ads-api)
- [Campaign Management API v5](https://developer.apple.com/documentation/apple_ads/apple-search-ads-campaign-management-api-5)
- [Reports API](https://developer.apple.com/documentation/apple_ads/reports)

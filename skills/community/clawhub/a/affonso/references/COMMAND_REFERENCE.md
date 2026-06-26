# Affonso CLI Command Reference

## Global Options

All commands accept these options:

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON (always use this) |
| `--api-key <key>` | API key for authentication |
| `--base-url <url>` | Custom API base URL |
| `--no-color` | Disable colored output |
| `--version` | Show CLI version |
| `--help` | Show help |

---

## affiliates

Manage affiliates. Page-based pagination (`--limit`, `--page`).

### `affiliates list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--page <n>` | Page number (default: 1) |
| `--status <status>` | Filter: pending, approved, rejected |
| `--search <query>` | Search by name or email |
| `--group-id <id>` | Filter by group ID |
| `--program-id <id>` | Filter by program ID |
| `--date-from <date>` | Filter from date |
| `--date-to <date>` | Filter to date |
| `--expand <fields>` | Expand fields (comma-separated) |
| `--sort <field:dir>` | Sort (e.g. createdAt:desc) |

### `affiliates get <id>`

| Option | Description |
|--------|-------------|
| `--expand <fields>` | Expand fields (comma-separated) |

### `affiliates create`

| Option | Required | Description |
|--------|----------|-------------|
| `--name <name>` | Yes | Affiliate name |
| `--email <email>` | Yes | Affiliate email |
| `--program-id <id>` | Yes | Program ID |
| `--tracking-id <id>` | No | Custom tracking ID |
| `--group-id <id>` | No | Group ID |
| `--company-name <name>` | No | Company name |
| `--country-code <code>` | No | Country code |
| `--external-user-id <id>` | No | External user ID |

### `affiliates update <id>`

| Option | Description |
|--------|-------------|
| `--name <name>` | Affiliate name |
| `--email <email>` | Affiliate email |
| `--status <status>` | Status: pending, approved, rejected |
| `--group-id <id>` | Group ID |
| `--company-name <name>` | Company name |
| `--country-code <code>` | Country code |
| `--external-user-id <id>` | External user ID |
| `--onboarding-completed` | Mark onboarding as completed |

### `affiliates delete <id>`

No additional options. Requires user confirmation.

---

## referrals

Manage referrals. **Cursor-based pagination** (`--limit`, `--starting-after`, `--ending-before`).

### `referrals list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--starting-after <id>` | Cursor: fetch items after this ID |
| `--ending-before <id>` | Cursor: fetch items before this ID |
| `--affiliate-id <id>` | Filter by affiliate ID |
| `--status <status>` | Filter by status |
| `--created-gte <date>` | Created on or after date |
| `--created-lte <date>` | Created on or before date |
| `--order <dir>` | Order: asc, desc |
| `--expand <fields>` | Expand fields |

### `referrals get <id>`

| Option | Description |
|--------|-------------|
| `--expand <fields>` | Expand fields |
| `--include <fields>` | Include fields |

### `referrals create`

| Option | Required | Description |
|--------|----------|-------------|
| `--email <email>` | Yes | Referral email |
| `--affiliate-id <id>` | Yes | Affiliate ID |
| `--subscription-id <id>` | No | Subscription ID |
| `--customer-id <id>` | No | Customer ID |
| `--click-id <id>` | No | Click ID |
| `--status <status>` | No | Initial status |
| `--name <name>` | No | Referral name |

### `referrals update <id>`

| Option | Description |
|--------|-------------|
| `--email <email>` | Referral email |
| `--status <status>` | Status |
| `--subscription-id <id>` | Subscription ID |
| `--customer-id <id>` | Customer ID |
| `--name <name>` | Referral name |

### `referrals delete <id>`

No additional options. Requires user confirmation.

---

## commissions

Manage commissions. Page-based pagination (`--limit`, `--page`).

### `commissions list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--page <n>` | Page number (default: 1) |
| `--status <status>` | Filter by commission status |
| `--sales-status <status>` | Filter by sales status |
| `--referral-id <id>` | Filter by referral ID |
| `--affiliate-id <id>` | Filter by affiliate ID |
| `--date-from <date>` | Filter from date |
| `--date-to <date>` | Filter to date |
| `--expand <fields>` | Expand fields |
| `--sort <field:dir>` | Sort |

### `commissions get <id>`

| Option | Description |
|--------|-------------|
| `--expand <fields>` | Expand fields |

### `commissions create`

| Option | Required | Description |
|--------|----------|-------------|
| `--referral-id <id>` | Yes | Referral ID |
| `--sale-amount <n>` | Yes | Sale amount |
| `--sale-amount-currency <code>` | Yes | Sale currency (e.g. USD) |
| `--commission-amount <n>` | Yes | Commission amount |
| `--commission-currency <code>` | Yes | Commission currency |
| `--is-subscription` | No | Mark as subscription commission |
| `--status <status>` | No | Commission status |
| `--sales-status <status>` | No | Sales status |
| `--payment-intent-id <id>` | No | Payment intent ID |
| `--hold-period-days <n>` | No | Hold period in days |

### `commissions update <id>`

| Option | Description |
|--------|-------------|
| `--status <status>` | Commission status |
| `--sales-status <status>` | Sales status |
| `--hold-period-days <n>` | Hold period in days |
| `--sale-amount <n>` | Sale amount |
| `--sale-amount-currency <code>` | Sale currency |
| `--commission-amount <n>` | Commission amount |
| `--commission-currency <code>` | Commission currency |

### `commissions delete <id>`

No additional options. Requires user confirmation.

---

## payouts

Manage payouts. Page-based pagination (`--limit`, `--page`). No create or delete commands.

### `payouts list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--page <n>` | Page number (default: 1) |
| `--status <status>` | Filter: pending, processing, completed, failed, cancelled |
| `--affiliate-id <id>` | Filter by affiliate ID |
| `--date-from <date>` | Filter from date |
| `--date-to <date>` | Filter to date |
| `--sort <field:dir>` | Sort |

### `payouts get <id>`

No additional options.

### `payouts update <id>`

| Option | Required | Description |
|--------|----------|-------------|
| `--status <status>` | Yes | Payout status |
| `--payment-method <method>` | No | Payment method |
| `--payment-reference <ref>` | No | Payment reference (e.g. transaction ID) |

---

## coupons

Manage coupons. Page-based pagination (`--limit`, `--page`). No update command.

### `coupons list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--page <n>` | Page number (default: 1) |
| `--affiliate-id <id>` | Filter by affiliate ID |
| `--program-id <id>` | Filter by program ID |
| `--search <query>` | Search by code |
| `--expand <fields>` | Expand fields |
| `--sort <field:dir>` | Sort |

### `coupons get <id>`

| Option | Description |
|--------|-------------|
| `--expand <fields>` | Expand fields |

### `coupons create`

| Option | Required | Description |
|--------|----------|-------------|
| `--affiliate-id <id>` | Yes | Affiliate ID |
| `--code <code>` | Yes | Coupon code |
| `--discount-type <type>` | Yes | Discount type: percentage, fixed |
| `--discount-value <n>` | Yes | Discount value |
| `--duration <dur>` | Yes | Duration: forever, once, repeating |
| `--duration-in-months <n>` | No | Duration in months (for repeating) |
| `--currency <code>` | No | Currency code |
| `--product-ids <ids>` | No | Product IDs (comma-separated) |

### `coupons delete <id>`

No additional options. Requires user confirmation.

---

## clicks

Track click events. Only has a create command.

### `clicks create`

| Option | Required | Description |
|--------|----------|-------------|
| `--program-id <id>` | Yes | Program ID |
| `--tracking-id <id>` | Yes | Tracking ID |
| `--referrer <url>` | No | Referrer URL |
| `--utm-source <val>` | No | UTM source |
| `--utm-medium <val>` | No | UTM medium |
| `--utm-campaign <val>` | No | UTM campaign |
| `--utm-term <val>` | No | UTM term |
| `--utm-content <val>` | No | UTM content |
| `--sub1 <val>` | No | Sub-tracking parameter 1 |
| `--sub2 <val>` | No | Sub-tracking parameter 2 |
| `--sub3 <val>` | No | Sub-tracking parameter 3 |
| `--sub4 <val>` | No | Sub-tracking parameter 4 |
| `--sub5 <val>` | No | Sub-tracking parameter 5 |
| `--ip <ip>` | No | IP address |
| `--user-agent <ua>` | No | User agent string |

---

## embed-tokens

Generate embed tokens. Only has a create command.

### `embed-tokens create`

| Option | Description |
|--------|-------------|
| `--affiliate-id <id>` | Affiliate ID |
| `--external-user-id <id>` | External user ID |
| `--email <email>` | Partner email |
| `--name <name>` | Partner name |

All options are optional. At least one identifier should be provided.

---

## program

Manage program settings and sub-resources. See [PROGRAM_SETTINGS_GUIDE.md](PROGRAM_SETTINGS_GUIDE.md) for details.

### `program get`

No additional options. Returns full program settings.

### `program update`

| Option | Description |
|--------|-------------|
| `--name <name>` | Program name |
| `--tagline <text>` | Tagline |
| `--category <cat>` | Category |
| `--description <text>` | Description |
| `--website-url <url>` | Website URL |
| `--logo-url <url>` | Logo URL |
| `--auto-approve` / `--no-auto-approve` | Enable/disable auto-approve |
| `--affiliate-links-enabled` / `--no-affiliate-links-enabled` | Enable/disable affiliate links |

### Sub-resource commands

| Sub-resource | Commands | Details |
|-------------|----------|---------|
| `program payment-terms` | get, update | Commission type/rate/duration, thresholds, cookie lifetime |
| `program tracking` | get, update | Referral parameters, email/name tracking |
| `program restrictions` | get, update | 10 traffic type toggles |
| `program fraud-rules` | get, update | 4 detection modes: off/detect/block |
| `program portal` | get, update | Branding, custom domain, feature toggles |
| `program notifications` | list, update | Email notification settings |
| `program groups` | list, get, create, update, delete | Affiliate groups with default group |
| `program creatives` | list, get, create, update, delete | Marketing creatives with type/dimensions |

---

## marketplace

Browse the affiliate marketplace. Public, no authentication required. Page-based pagination.

### `marketplace list`

| Option | Description |
|--------|-------------|
| `--limit <n>` | Items per page (default: 50) |
| `--page <n>` | Page number (default: 1) |
| `--category <cat>` | Filter by category |
| `--search <query>` | Search programs |
| `--sort <field:dir>` | Sort |

### `marketplace get <id>`

No additional options.

---

## config

Manage CLI configuration.

### `config get <key>`

Get a config value. Key must be `api-key` or `base-url`.

### `config set <key> <value>`

Set a config value. Key must be `api-key` or `base-url`.

---

## whoami

Show current authentication status. Returns auth method, team info, or masked API key.

```
affonso whoami --json
```

---

## login

Log in via browser OAuth flow. **Do not use in agent/headless environments** — use `AFFONSO_API_KEY` instead.

---

## logout

Log out and remove stored credentials.

---

## Pagination Reference

| Resource | Type | Parameters |
|----------|------|------------|
| affiliates | Page-based | `--limit`, `--page` |
| referrals | **Cursor-based** | `--limit`, `--starting-after`, `--ending-before` |
| commissions | Page-based | `--limit`, `--page` |
| payouts | Page-based | `--limit`, `--page` |
| coupons | Page-based | `--limit`, `--page` |
| marketplace | Page-based | `--limit`, `--page` |
| program creatives | Page-based | `--limit`, `--page` |

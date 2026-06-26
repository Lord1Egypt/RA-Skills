# Program Settings Guide

The `program` command manages your affiliate program's configuration. Each sub-resource has `get` and `update` commands (some also support CRUD).

## Payment Terms

Controls commission structure and payout rules.

```bash
affonso program payment-terms get --json
affonso program payment-terms update --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--commission-type <type>` | Commission type: percentage, fixed |
| `--commission-rate <n>` | Commission rate (numeric) |
| `--commission-duration <dur>` | Duration: forever, once, first_month, custom |
| `--commission-duration-value <n>` | Custom duration value (when duration is custom) |
| `--payment-threshold <n>` | Minimum payout threshold |
| `--payment-frequency <freq>` | Payment frequency: monthly, biweekly, weekly |
| `--cookie-lifetime <days>` | Cookie lifetime in days |
| `--auto-payout` / `--no-auto-payout` | Enable/disable automatic payouts |
| `--invoice-required` / `--no-invoice-required` | Require/don't require invoices |

**Example — set 20% recurring commission with $50 minimum payout:**
```bash
affonso program payment-terms update --json \
  --commission-type percentage \
  --commission-rate 20 \
  --commission-duration forever \
  --payment-threshold 50
```

## Tracking

Controls how referrals are attributed.

```bash
affonso program tracking get --json
affonso program tracking update --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--default-referral-parameter <param>` | Default referral parameter name |
| `--enabled-referral-parameters <params>` | Enabled parameters (comma-separated) |
| `--track-email` / `--no-track-email` | Track/don't track referral email |
| `--track-name` / `--no-track-name` | Track/don't track referral name |

**Example — enable email tracking with custom parameter:**
```bash
affonso program tracking update --json \
  --default-referral-parameter ref \
  --track-email
```

## Restrictions

10 traffic type toggles controlling what affiliates are allowed to do. Each has `--<option>` and `--no-<option>` variants.

```bash
affonso program restrictions get --json
affonso program restrictions update --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--websites` / `--no-websites` | Allow/disallow websites |
| `--social-marketing` / `--no-social-marketing` | Allow/disallow social marketing |
| `--organic-social` / `--no-organic-social` | Allow/disallow organic social |
| `--email-marketing` / `--no-email-marketing` | Allow/disallow email marketing |
| `--paid-ads` / `--no-paid-ads` | Allow/disallow paid ads |
| `--content-marketing` / `--no-content-marketing` | Allow/disallow content marketing |
| `--coupon-sites` / `--no-coupon-sites` | Allow/disallow coupon sites |
| `--review-sites` / `--no-review-sites` | Allow/disallow review sites |
| `--incentivized-traffic` / `--no-incentivized-traffic` | Allow/disallow incentivized traffic |
| `--trademark-bidding` / `--no-trademark-bidding` | Allow/disallow trademark bidding |

**Example — block coupon sites and paid ads:**
```bash
affonso program restrictions update --json \
  --no-coupon-sites \
  --no-paid-ads
```

## Fraud Rules

4 fraud detection categories, each with 3 modes: `off`, `detect`, `block`.

- **off** — no action
- **detect** — flag suspicious activity for review
- **block** — automatically reject

```bash
affonso program fraud-rules get --json
affonso program fraud-rules update --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--self-referral <mode>` | Self-referral detection: off, detect, block |
| `--duplicate-ip <mode>` | Duplicate IP detection: off, detect, block |
| `--vpn-proxy <mode>` | VPN/Proxy detection: off, detect, block |
| `--suspicious-conversion <mode>` | Suspicious conversion detection: off, detect, block |

**Example — block self-referrals, detect VPN usage:**
```bash
affonso program fraud-rules update --json \
  --self-referral block \
  --vpn-proxy detect
```

## Portal

Branding and configuration for the affiliate portal.

```bash
affonso program portal get --json
affonso program portal update --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--primary-color <color>` | Primary color (hex) |
| `--accent-color <color>` | Accent color (hex) |
| `--logo-url <url>` | Logo URL |
| `--favicon-url <url>` | Favicon URL |
| `--custom-domain <domain>` | Custom domain |
| `--terms-url <url>` | Terms URL |
| `--privacy-url <url>` | Privacy URL |
| `--onboarding-enabled` / `--no-onboarding-enabled` | Enable/disable onboarding flow |
| `--resources-enabled` / `--no-resources-enabled` | Enable/disable resources section |

**Example — set branding colors and enable onboarding:**
```bash
affonso program portal update --json \
  --primary-color "#4F46E5" \
  --accent-color "#10B981" \
  --onboarding-enabled
```

## Notifications

Manage email notification settings. Uses `list` and `update <id>` (no create/delete).

```bash
affonso program notifications list --json
affonso program notifications update <id> --json [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--subject <text>` | Email subject line |
| `--enabled` / `--no-enabled` | Enable/disable this notification |

**Example — disable a notification:**
```bash
affonso program notifications update notif_abc123 --json --no-enabled
```

## Groups

Manage affiliate groups. Full CRUD support.

```bash
affonso program groups list --json [--expand <fields>]
affonso program groups get <id> --json [--expand <fields>]
affonso program groups create --json --name <name> [OPTIONS]
affonso program groups update <id> --json [OPTIONS]
affonso program groups delete <id> --json
```

| Command | Option | Required | Description |
|---------|--------|----------|-------------|
| list | `--expand <fields>` | No | Expand: incentives, multi_level_incentives |
| get | `--expand <fields>` | No | Expand: incentives, multi_level_incentives |
| create | `--name <name>` | Yes | Group name |
| create | `--description <text>` | No | Group description |
| create | `--is-default` | No | Set as default group |
| update | `--name <name>` | No | Group name |
| update | `--description <text>` | No | Group description |
| update | `--is-default` / `--no-is-default` | No | Set/unset as default group |

**Example — create a VIP group:**
```bash
affonso program groups create --json \
  --name "VIP Partners" \
  --description "Top-performing affiliates with higher commission rates"
```

## Creatives

Manage marketing creatives. Full CRUD with page-based pagination.

```bash
affonso program creatives list --json [OPTIONS]
affonso program creatives get <id> --json
affonso program creatives create --json --name <name> --type <type> [OPTIONS]
affonso program creatives update <id> --json [OPTIONS]
affonso program creatives delete <id> --json
```

| Command | Option | Required | Description |
|---------|--------|----------|-------------|
| list | `--limit <n>` | No | Items per page (default: 50) |
| list | `--page <n>` | No | Page number (default: 1) |
| list | `--type <type>` | No | Filter by type |
| list | `--search <query>` | No | Search by name |
| create | `--name <name>` | Yes | Creative name |
| create | `--type <type>` | Yes | Creative type |
| create/update | `--description <text>` | No | Description |
| create/update | `--url <url>` | No | URL |
| create/update | `--file-url <url>` | No | File URL |
| create/update | `--width <n>` | No | Width in pixels |
| create/update | `--height <n>` | No | Height in pixels |

**Example — create a banner creative:**
```bash
affonso program creatives create --json \
  --name "Summer Sale Banner" \
  --type banner \
  --file-url "https://example.com/banner.png" \
  --width 728 \
  --height 90
```

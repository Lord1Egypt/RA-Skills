# Ecommerce Website Data — Ecommerce Store Search & Analytics

> Search 10M+ ecommerce stores and ecommerce websites. Get ecommerce data, Shopify store analytics, revenue trends, tech stack, and decision-maker contacts — all for free.

Powered by [EcCompass AI](https://eccompass.ai) — one of the world's largest DTC databases — this skill delivers *free, live data* on 10M+ ecommerce stores with 100+ analytics fields.

## What You Can Do

Search Stores — "Find Shopify stores selling pet food with 10k+ Instagram followers" 

Domain Analytics — "Show me ooni.com's GMV trend and tech stack" 

Lead Contacts — "Get decision-maker emails for this brand" 

## Setup

**100% Free. One-minute setup.**

### Quickest Way — Just Tell OpenClaw

Paste this to your OpenClaw agent and it will install the skill and configure the token for you:

> Install this skill: https://clawhub.ai/roger52027/ecommerce-website-data
> My APEX_TOKEN is: your_token_here

Get your free token at [eccompass.ai](https://eccompass.ai) → Dashboard → API Access → Create Token.

### Manual Install via OpenClaw CLI

```bash
openclaw skills install roger52027/ecommerce-website-data
```

Or install a specific version:

```bash
openclaw skills install roger52027/ecommerce-website-data --version 1.2.15
```

Then configure the token (choose one):

**Option A — OpenClaw config** (persistent):

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "ecommerce-website-data": {
        "enabled": true,
        "env": {
          "APEX_TOKEN": "your_token_here"
        }
      }
    }
  }
}
```

**Option B — Shell environment variable**:

```bash
export APEX_TOKEN="your_token_here"
```

## Quick Start

```bash
# Search by keyword
python3 scripts/query.py search "pet food"

# Search with country + platform filters
python3 scripts/query.py search "coffee" --country CN --platform shopify

# Filter only (no keyword)
python3 scripts/query.py search --country US --platform shopify --min-gmv 1000000

# Get full analytics for a domain
python3 scripts/query.py domain ooni.com

# Historical GMV and traffic trends
python3 scripts/query.py historical ooni.com

# Installed apps/plugins
python3 scripts/query.py apps ooni.com

# LinkedIn contacts
python3 scripts/query.py contacts ooni.com
```

## Data Coverage

Powered by ECcompass.ai — one of the world's largest DTC databases — this skill delivers free, monthly-updated live data on 10M+ global ecommerce stores.
| Metric | Value |
|--------|-------|
| Total domains | 10,000,000+ |
| Countries | 200+ |
| Platforms | Shopify, WooCommerce, Wix, Squarespace, BigCommerce and more |
| GMV data | 2023–2026 yearly + last 12 months |
| Social media | Instagram, TikTok, Twitter/X, YouTube, Facebook, Pinterest |
| Update frequency | Monthly |

## Analytics Fields

Each domain profile includes 100+ data points across 6 key categories:

- **Basic Info** — domain, brand name, platform, plan, status, creation date, language
- **Revenue** — GMV 2023–2026, last 12 months, YoY growth, estimated monthly/yearly sales
- **Products** — count, average price, price range, variants, images
- **Traffic** — monthly visits, page views, Alexa rank, platform rank
- **Social Media** — followers + 30d/90d change for 6 platforms
- **Tech Stack** — technologies, installed apps, theme, monthly app spend
- **Geography** — country, city, state, coordinates, company location
- **Contact** — emails, phones, contact page URL
- **Reviews** — Trustpilot, Yotpo ratings

## Requirements

- Python 3.6+
- Network access to `api.eccompass.ai`
- `APEX_TOKEN` environment variable (get yours at [eccompass.ai](https://eccompass.ai))

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/public/api/v1/search` | POST | Search domains with keyword, filters, ranges, and sorting |
| `/public/api/v1/domain/{domain}` | GET | Full analytics for a single domain |
| `/public/api/v1/historical/{domain}` | GET | Monthly GMV and traffic history (2023+) |
| `/public/api/v1/installed-apps/{domain}` | GET | Installed apps/plugins with vendor details |
| `/public/api/v1/contacts/{domain}` | GET | LinkedIn contacts (name, position, email) |

## Documentation

- [AI Instructions](SKILL.md) — How the agent uses this skill
- [API Schema](references/schema.md) — Full response format and field definitions
- [Usage Examples](references/examples.md) — Real-world scenarios with sample output

## License

Proprietary — [EcCompass AI](https://eccompass.ai)

## Support

For questions, issues, or feature requests, visit [EcCompass AI](https://eccompass.ai).

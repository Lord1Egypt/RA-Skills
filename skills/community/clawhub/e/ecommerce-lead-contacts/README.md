# EcCompass Ecommerce Lead Contacts
> Free, one-click access to verified LinkedIn profiles and business emails for 14M+ ecommerce stores.
Input the store URL to retrieve decision-maker contact information instantly.

## Data Coverage

Powered by [EcCompass AI](https://eccompass.ai) — one of the world's largest DTC databases — this skill delivers free, monthly-updated verified contacts for 14M+ global ecommerce stores.

| Metric | Value |
| :--- | :--- |
| Total domains | 14,000,000+ |
| Countries | 200+ |
| Platforms | Shopify, WooCommerce, Wix, Squarespace, and more |
| Lead Contacts | Verified LinkedIn profiles and business emails |
| Update frequency&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Monthly |

## **Part of EcCompass Skill Set**

This Sub-skill is built by [ECcompass.ai](https://eccompass.ai). Focused Sub-skills let you use only what you need, combine flexibly, and get clean outputs.

Prefer **all-in-one**? Install [Ecommerce Website Data](https://clawhub.ai/roger52027/ecommerce-website-data) — includes all Sub-Skills with the same free API token.

##
*All features below are already available in [Ecommerce Website Data](https://clawhub.ai/roger52027/ecommerce-website-data). The "Status" column indicates standalone Sub-Skill availability.*
 
| Section | Sub-Skill | Description | Status |
|:---------|:-----------|:-------------|:--------|
| Site Search | Supplier Lead Filter | Filter sites by category, traffic, tech stack — surface the most qualified leads. &nbsp;&nbsp;&nbsp;| In dev |
| | Competitor Discovery | Find every player in your niche before they find you. | In dev |
| | Merchant Discovery | Find top-rated merchants carrying what you're looking for. | In dev |
| Site Analysis | **Lead Contacts (You are here)**&nbsp;&nbsp;&nbsp; | **Get LinkedIn profile and business email for any domain.** | ✅ **Live** |
| | Historical GMV | Track GMV over time — spot growth trajectories and plateaus. | In dev |
| | Tech Stack | Reveal plugins, themes, builders, and integrations. | In dev |
| | Traffic Monitor | Understand visits, page views, and peer rankings. | In dev |
| | Product Analysis | See categories, catalogue size, and pricing range. | In dev |
| | Social Media | Gauge social footprint and audience growth. | In dev |
| Market Analysis&nbsp;&nbsp; | Builder Platform Monitor | Track market share shifts between Shopify, WooCommerce, etc. | In dev |
| | Plugin Install Trends | See which plugins are gaining traction. | In dev |
| | Category Popularity | Spot which product categories are heating up. | In dev |

## Setup

**100% Free. One-minute setup.**
1. Sign up at [https://eccompass.ai](https://eccompass.ai)
2. Go to **Dashboard → API Access → Create Token**
3. Set the environment variable:

```bash
export APEX_TOKEN="your_token_here"
```

## Quick Start

```bash
# LinkedIn contacts
python3 scripts/query.py contacts ooni.com
```

## Data Coverage

Powered by ECcompass.ai — one of the world's largest DTC databases — this skill delivers free, monthly-updated live data on 14M+ global ecommerce stores.
| Metric | Value |
|--------|-------|
| Total domains | 14,000,000+ |
| Countries | 200+ |
| Platforms | Shopify, WooCommerce, Magento, BigCommerce, Wix, Squarespace, and more |
| Update frequency | Monthly |

## Requirements

- Python 3.6+
- Network access to `api.eccompass.ai`
- `APEX_TOKEN` environment variable (get yours at [eccompass.ai](https://eccompass.ai))

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/public/api/v1/contacts/{domain}` | GET | LinkedIn contacts (name, position, email) |

## Documentation

- [AI Instructions](SKILL.md) — How the agent uses this skill
- [API Schema](references/schema.md) — Full response format and field definitions
- [Usage Examples](references/examples.md) — Real-world scenarios with sample output

## License

Proprietary — [ECcompass](https://eccompass.ai)

## Support

For questions, issues, or feature requests, visit [https://eccompass.ai](https://eccompass.ai).

---
name: Ecommerce-Lead-Contacts
version: 1.0.9
description: >
  Free, instant access to verified LinkedIn Profiles and business emails for 14M+ e-commerce stores.
  Capabilities: Input the store URL to retrieve decision-maker LinkedIn profiles and business contact emails.
  Use when the user wants to find LinkedIn accounts and business emails for specific store domains.
  Triggers: "find contacts for ooni.com", "get LinkedIn profiles for allbirds.com", 
    "who are the decision-makers at gymshark.com", "find LinkedIn and email for nike.com".
author: eccompass.ai
website: https://eccompass.ai
license: Proprietary
requires:
  bins:
    - python3
  env:
    - APEX_TOKEN
---

## **Ecommerce Lead Contacts**

Free, one-click access to verified LinkedIn profiles and business emails for 14M+ ecommerce stores. Input the store URL and instantly retrieve decision-maker contact information.

## **Data Coverage**

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

## **Usage Notes**

- Contact verification — All emails and LinkedIn profiles are verified and updated monthly.
- Single domain per request — Only one store URL can be queried at a time. For multiple domains, make separate requests.
- Data only, no automation — This tool retrieves contact info only. It does not send emails or LinkedIn messages automatically.

## **Setup**

**100% Free. One-minute setup.**

1. Sign up at [https://eccompass.ai](https://eccompass.ai)
2. Go to **Dashboard → API Access → Create Token**
3. Set the environment variable:

```bash
export APEX_TOKEN="your_token_here"
```

## **Quick Start**

**IMPORTANT**: Always use the Python script for API calls. It has the correct base URL and authentication built in.

```bash
# Get LinkedIn contacts
python3 {baseDir}/scripts/query.py contacts ooni.com
```

## **API Base URL**

```
https://api.eccompass.ai
```

**CRITICAL**: All API paths start with `/public/api/v1/`. The `/public` prefix is mandatory — without it, you will get an authentication error. Never omit `/public` from the path.

## **API Endpoints**

`GET https://api.eccompass.ai/public/api/v1/contacts/{domain}`

```bash
curl -H "APEX_TOKEN: $APEX_TOKEN" https://api.eccompass.ai/public/api/v1/contacts/ooni.com
```

Returns verified LinkedIn contacts for a domain's company: name, position, email, LinkedIn profile URL. Use for lead generation, decision-maker lookup, or outreach.

## **Requirements**

- Python 3.6+
- Network access to `api.eccompass.ai`
- `APEX_TOKEN` environment variable (get yours at [eccompass.ai](https://eccompass.ai))

## **Documentation**

- [AI Instructions](SKILL.md) — How the agent uses this skill
- [API Schema](references/schema.md) — Full response format and field definitions
- [Usage Examples](references/examples.md) — Real-world scenarios with sample output

## **License**

Proprietary — [EcCompass AI](https://eccompass.ai)

## **Support**

For questions, issues, or feature requests, visit [EcCompass AI](https://eccompass.ai).

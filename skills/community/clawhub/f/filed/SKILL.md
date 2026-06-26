---
name: filed
description: Search and retrieve US business entity data (LLCs, corporations, partnerships) from official Secretary of State records via the Filed.dev API. Use when looking up a business, verifying a company exists, finding registered agents, checking entity status, searching by officer name, or doing business due diligence. Covers FL, NY, PA, CT, CO, OR, IA, AK (1.9M+ entities). Triggers on business lookup, company search, entity verification, KYB, registered agent lookup, or "is this company real."
metadata:
  openclaw:
    requires:
      env:
        - FILED_API_KEY
      bins:
        - curl
    primaryEnv: FILED_API_KEY
    homepage: https://filed.dev
---

# Filed — Business Entity Lookup

Search 1.9M+ US business entities from official state records.

## Setup

An API key is required. Get one free (100 lookups/month) at https://filed.dev/register

Store the key in environment variable `FILED_API_KEY` or pass via `--api-key`.

## Quick Reference

```bash
# Search by business name
scripts/filed.sh search --name "Acme Holdings" --state FL

# Search by registered agent
scripts/filed.sh search --agent "CSC Global" --state FL

# Search by officer name
scripts/filed.sh search --officer "John Smith" --state NY

# Get full entity details (officers, filings, addresses)
scripts/filed.sh entity ent_mNqR7xKp

# Filter by status and type
scripts/filed.sh search --name "Acme" --state FL --status active --type llc

# Filter by formation date
scripts/filed.sh search --name "Acme" --state FL --formed-after 2020-01-01
```

## Supported States

FL, NY, PA, CT, CO, OR, IA, AK — more added regularly.

## Response Fields

Search results return: `id`, `name`, `state`, `type`, `status`, `formedDate`, `registeredAgent` (name + address), `principalAddress`, `officerCount`.

Entity details add: `stateEntityId`, `officers[]` (name + title), `filings[]` (type + date).

## Paid Plans

| Plan | Lookups/month | Price |
|------|--------------|-------|
| Free | 100 | $0 |
| Pro | 1,000 | $49/mo |
| Ultra | 10,000 | $199/mo |
| Mega | 50,000 | $499/mo |

Upgrade at https://filed.dev/pricing or via RapidAPI: https://rapidapi.com/grantley-holdings-grantley-holdings-default/api/filed2

## API Details

For full endpoint docs, parameter reference, and error codes: `references/api-docs.md`

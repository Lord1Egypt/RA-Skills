---
name: ahrefs-domain-rating-free
description: Use when checking Ahrefs Domain Rating, DR, website authority, domain authority, backlink profile strength, or free Ahrefs public API data for a domain or URL without an API key.
---

# Ahrefs Domain Rating Free

## Overview

Use Ahrefs' free public Domain Rating endpoint to check a domain or URL's backlink profile strength. No Ahrefs API key required.

Endpoint:

```text
GET https://api.ahrefs.com/v3/public/domain-rating-free?target=<domain-or-url>
```

Official docs: https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free

## When to Use

Use this skill when user asks for:

- Ahrefs DR or Domain Rating
- website authority from Ahrefs
- domain authority style checks using Ahrefs data
- quick backlink strength comparison
- free Ahrefs public API lookup
- DR for one domain, many domains, or URLs

Do not use when user needs paid Site Explorer metrics, backlinks, referring domains, organic keywords, or historical Ahrefs data. Those require authenticated Ahrefs API endpoints.

## Quick Start

From this skill directory:

```bash
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com
python3 scripts/ahrefs-domain-rating-free.py https://example.com --json
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com example.com github.com
```

Expected compact output:

```text
ahrefs.com  91.0
```

## Agent Workflow

1. Normalize user input as domain or URL. Keep path if user provided a specific URL.
2. Call the wrapper script first. It handles URL encoding, HTTP errors, JSON parsing, and multi-target output.
3. Report DR as a numeric score on Ahrefs' 100-point logarithmic scale.
4. If comparing multiple targets, sort or tabulate only if user asks.
5. If endpoint returns 400, ask for a valid domain or URL.

## Wrapper Script

```bash
python3 scripts/ahrefs-domain-rating-free.py <target...> [--json] [--raw]
```

Flags:

| Flag | Use |
|---|---|
| `--json` | Machine-readable array with target, domain_rating, ok/error |
| `--raw` | Print raw Ahrefs JSON per target |
| `--timeout SECONDS` | Override HTTP timeout, default 20 |

## API Details

Query parameters:

| Parameter | Required | Meaning |
|---|---:|---|
| `target` | yes | Domain or URL to check |
| `output` | no | Ahrefs output selector. Wrapper does not need it. |

Response shape:

```json
{
  "domain_rating": {
    "domain_rating": 91.0
  }
}
```

`domain_rating.domain_rating` is the current strength of the target's backlink profile compared to other websites in Ahrefs' database, on a 100-point logarithmic scale.

## Common Mistakes

- Do not add `Authorization` header. This public endpoint is free and unauthenticated.
- Do not call `/v3/public/domain-rating`; correct path is `/v3/public/domain-rating-free`.
- Do not confuse Ahrefs DR with Moz DA or Semrush Authority Score.
- Do not promise real-time backlink counts. This endpoint returns only DR.
- Handle invalid targets as user input errors, not API outages.

## Install

Skills.sh:

```bash
npx skills add AIGC-Hackers/ahrefs-domain-rating-free-skill --skill ahrefs-domain-rating-free
```

ClawHub, after publish:

```bash
clawhub install ahrefs-domain-rating-free
# or
clawdhub install ahrefs-domain-rating-free
```

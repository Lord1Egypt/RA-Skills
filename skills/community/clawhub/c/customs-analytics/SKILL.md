---
name: customs-analytics
description: Latvia customs declarations analytics — 3.8GB, KN8 codes, trends, seasonal patterns, top declarants
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["customs","latvia","kn8","declarations","analytics"]}
---

# Customs Analytics

3.8GB Latvia customs declarations database. KN8-level product codes, monthly trends, seasonal patterns, top declarants, cross-border analysis.

## Base URL

`https://sputnikx.xyz/api/v1/agent`

## Key Endpoints

### Customs Overview ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/customs/overview?year=2025"
```

### KN8 Code Trends ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/customs/trends?kn8=44011100&years=2020-2025"
```

### Top Declarants ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/customs/top-declarants?kn8=44&year=2025"
```

### Seasonal Patterns ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/customs/seasonal?kn8=27&years=2020-2025"
```

## MCP Server
```
Endpoint: https://mcp.sputnikx.xyz/mcp
Tool: query_customs (if available in your plan)
```

## When to use this skill
- Analyze Latvia import/export customs patterns at KN8 granularity
- Research specific commodity code trends over time
- Identify top declarants and seasonal demand shifts
- Cross-reference with EU trade data for corridor analysis

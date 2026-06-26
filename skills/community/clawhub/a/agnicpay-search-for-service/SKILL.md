---
name: search-for-service
description: >
  Search the x402 bazaar for paid API services. Use when the user wants
  to find APIs, discover services, browse the marketplace, or needs an
  external service. Also use as a fallback when no other skill matches.
  Covers "find me an API", "what services are available", "search for",
  "browse bazaar", "what can I do".
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest x402 bazaar *)"
  - "Bash(npx agnic@latest x402 details *)"
---

# Searching the x402 Bazaar

Use `npx agnic@latest x402` commands to discover and inspect paid API endpoints on the x402 bazaar marketplace. No authentication or balance is required for searching.

## Commands

### Search the Bazaar

Find paid services by keyword using BM25 relevance search:

```bash
npx agnic@latest x402 bazaar search <query> [-k <n>] [--force-refresh] [--json]
```

| Option            | Description                          |
| ----------------- | ------------------------------------ |
| `-k, --top <n>`   | Number of results (default: 5)       |
| `--force-refresh` | Re-fetch resource index from CDP API |
| `--json`          | Output as JSON                       |

Results are cached locally at `~/.config/agnic/bazaar/` and auto-refresh after 12 hours.

### List Bazaar Resources

Browse all available resources:

```bash
npx agnic@latest x402 bazaar list [--network <network>] [--full] [--json]
```

| Option             | Description                             |
| ------------------ | --------------------------------------- |
| `--network <name>` | Filter by network (base, base-sepolia)  |
| `--full`           | Show complete details including schemas |
| `--json`           | Output as JSON                          |

### Discover Payment Requirements

Inspect an endpoint's x402 payment requirements without paying:

```bash
npx agnic@latest x402 details <url> [--json]
```

Auto-detects the correct HTTP method by trying each until it gets a 402 response, then displays price, accepted payment schemes, network, and input/output schemas.

## Examples

```bash
# Search for weather-related paid APIs
npx agnic@latest x402 bazaar search "weather" --json

# Search with more results
npx agnic@latest x402 bazaar search "sentiment analysis" -k 10 --json

# Browse all bazaar resources
npx agnic@latest x402 bazaar list --full --json

# Check what an endpoint costs
npx agnic@latest x402 details https://example.com/api/weather
```

## Prerequisites

- No authentication needed for search, list, or details commands

## Next Steps

Once you've found a service, use the `pay-for-service` skill to make a paid request.

## Error Handling

Common errors:

- "CDP API returned 429" -- Rate limited; cached data will be used if available
- "No X402 payment requirements found" -- URL may not be an x402 endpoint
- No results -- Try broadening the search query or using different keywords

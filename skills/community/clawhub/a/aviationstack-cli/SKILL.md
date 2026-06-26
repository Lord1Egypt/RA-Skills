---
name: aviationstack-cli
description: "Manage AviationStack via CLI - flights, airports, airlines, routes. Use when user mentions 'aviationstack', 'flight search', 'airport lookup', 'airline search', or wants to interact with the AviationStack API."
category: aviation
---

# aviationstack-cli

## Setup

If `aviationstack-cli` is not installed, install it from GitHub:
```bash
npx api2cli install Melvynx/aviationstack-cli
```

If `aviationstack-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle aviationstack
npx api2cli link aviationstack
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
aviationstack-cli auth set "your-token"
aviationstack-cli auth test
```

## Resources

### flights

| Command | Description |
|---------|-------------|
| `aviationstack-cli flights search --iata YP111 --json` | Search flights by IATA code |
| `aviationstack-cli flights search --airline-iata KE --json` | Search flights by airline IATA |
| `aviationstack-cli flights search --flight-number 111 --json` | Search flights by number |
| `aviationstack-cli flights search --dep-iata ICN --arr-iata SFO --json` | Search by departure and arrival |
| `aviationstack-cli flights search --limit 50 --offset 25 --json` | Search with pagination |
| `aviationstack-cli flights search --fields flight_iata,airline_iata,status --json` | Search with specific fields |

### airports

| Command | Description |
|---------|-------------|
| `aviationstack-cli airports search --iata-code ICN --json` | Search airport by IATA code |
| `aviationstack-cli airports search --search "San Francisco" --json` | Search airport by name or city |
| `aviationstack-cli airports search --limit 10 --json` | Search with result limit |
| `aviationstack-cli airports search --fields iata_code,airport_name,city_iata --json` | Search with specific fields |

### airlines

| Command | Description |
|---------|-------------|
| `aviationstack-cli airlines search --iata-code KE --json` | Search airline by IATA code |
| `aviationstack-cli airlines search --search "Korean Air" --json` | Search airline by name |
| `aviationstack-cli airlines search --limit 5 --json` | Search with result limit |
| `aviationstack-cli airlines search --fields iata_code,airline_name --json` | Search with specific fields |

### routes

| Command | Description |
|---------|-------------|
| `aviationstack-cli routes search --dep-iata ICN --arr-iata SFO --json` | Search routes by airports |
| `aviationstack-cli routes search --flight-number 111 --json` | Search routes by flight number |
| `aviationstack-cli routes search --fields dep_iata,arr_iata,airline_iata --json` | Search with specific fields |

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`

---
name: api-mock-generator
description: Generate mock API servers from OpenAPI 3.x and Swagger 2.0 specs. Use when creating mock/stub APIs for frontend development, testing, demos, or CI. Generates realistic fake data based on schema types and property names. Supports live server mode, static JSON file generation, response delays, random error simulation, and CORS. Pure Python, no dependencies.
---

# API Mock Generator

Generate mock API servers and static fixtures from OpenAPI/Swagger specs. Contextual fake data (emails, names, UUIDs, etc.) based on property names and schema types.

## Quick Start

```bash
# Start a live mock server
python3 scripts/generate_mock.py serve api.json

# Generate static JSON mock files
python3 scripts/generate_mock.py generate api.json -o mocks/

# List discovered routes
python3 scripts/generate_mock.py routes api.json

# Generate sample response for a specific endpoint
python3 scripts/generate_mock.py sample api.json /users
```

## Commands

### `serve` — Live Mock Server

```bash
python3 scripts/generate_mock.py serve spec.json [options]
```

Options:
- `--port`, `-p` — port (default: 3000)
- `--host` — host (default: 127.0.0.1)
- `--delay`, `-d` — response delay in ms (simulate latency)
- `--error-rate`, `-e` — random error rate 0.0-1.0 (simulate failures)

Features: CORS headers on all responses, path parameter matching, JSON responses with Content-Type headers.

### `generate` — Static Mock Files

```bash
python3 scripts/generate_mock.py generate spec.json -o output_dir/
```

Creates one JSON file per route + `manifest.json` with route mapping. Useful for test fixtures or frontend stubs.

### `routes` — Discover Endpoints

```bash
python3 scripts/generate_mock.py routes spec.json [--format text|json]
```

### `sample` — Single Endpoint Preview

```bash
python3 scripts/generate_mock.py sample spec.json /users --method GET
```

## Supported Specs

- OpenAPI 3.x (JSON)
- Swagger 2.0 (JSON)
- YAML (requires `pip install pyyaml`)

## Fake Data Generation

Property-name-aware generation:

| Property pattern | Generated data |
|-----------------|---------------|
| `*email*` | realistic email |
| `*name*` | first/last/full name |
| `*phone*` | formatted phone |
| `*url*`, `*website*` | https URL |
| `*city*`, `*country*` | real city/country |
| `*id*`, `*uuid*` | UUID v4 |
| `*price*`, `*amount*` | currency-like number |
| `*image*`, `*avatar*` | picsum.photos URL |
| `*description*`, `*bio*` | lorem paragraph |
| `*status*` | active/inactive/pending |

Schema-aware: respects `enum`, `example`, `default`, `format` (date, date-time, email, uri, uuid, ipv4), `minimum`/`maximum`, `minLength`/`maxLength`, `$ref`, `oneOf`/`anyOf`/`allOf`.

## Exit Codes

- `0` — success
- `1` — route not found (sample command)
- `2` — spec parse error or system error

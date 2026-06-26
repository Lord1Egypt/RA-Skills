# discava-skill

A Claude Code skill for searching local businesses worldwide via the [discava](https://discava.ai) API.

## What it does

This skill enables Claude Code to find local businesses, services, restaurants, doctors, craftsmen, and any other local service provider. It provides structured data with confidence scores and demand rankings.

## Features

- Search businesses by query, city, and country
- Get detailed business information (address, phone, website, opening hours)
- Autocomplete suggestions for queries and cities
- Rankings by demand score
- Feedback reporting for data quality issues

## Installation

Add this skill to your Claude Code setup:

```bash
claude skill add sebastian1747/discava-skill
```

## API

The skill uses the discava API at `https://discava.ai/api/v1`. No authentication required — the API is open and free (rate limited to 500 req/hour per IP).

### Available endpoints

| Endpoint | Description |
|---|---|
| `GET /search` | Search businesses by query, city, country |
| `GET /business/{id}` | Get full business details |
| `GET /ranking` | Top businesses by demand score |
| `GET /suggest` | Autocomplete for queries and cities |
| `POST /feedback` | Report data quality issues |

For full API documentation, see [SKILL.md](SKILL.md).

## License

MIT

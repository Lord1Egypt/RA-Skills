---
name: Birth Chart Analysis
description: Generates comprehensive astrological birth charts from personal birth data and supports multiple languages for cultural accessibility.
---

# Overview

Birth Chart Analysis is a specialized astrological computation API that generates detailed natal charts based on an individual's birth information. The service calculates planetary positions, house placements, and astrological aspects at the exact moment of birth, providing insights into personality traits, life patterns, and potential opportunities based on Vedic and Western astrological traditions.

This API is designed for astrology platforms, wellness applications, personal development tools, and lifestyle services that integrate birth chart readings into their user experience. It supports multilingual output, making astrological insights accessible to a global audience. The tool combines precise astronomical calculations with traditional astrological interpretation frameworks.

Ideal users include astrology practitioners, wellness coaches, app developers building horoscope features, and lifestyle platforms seeking to enhance user engagement with personalized astrological content. Organizations can integrate this API to provide data-driven astrological analysis without maintaining complex planetary calculation algorithms in-house.

## Usage

**Example Request:**

```json
{
  "name": "Arjun Sharma",
  "birth_date": "1990-05-15",
  "birth_time": "14:30:00",
  "birth_location": "Mumbai, India",
  "language": "en"
}
```

**Example Response:**

```json
{
  "name": "Arjun Sharma",
  "birth_date": "1990-05-15",
  "birth_time": "14:30:00",
  "birth_location": "Mumbai, India",
  "ascendant": {
    "sign": "Libra",
    "degree": 12.45
  },
  "sun": {
    "sign": "Taurus",
    "degree": 24.32
  },
  "moon": {
    "sign": "Gemini",
    "degree": 18.67
  },
  "planets": [
    {
      "name": "Mercury",
      "sign": "Aries",
      "degree": 5.12
    },
    {
      "name": "Venus",
      "sign": "Gemini",
      "degree": 9.88
    },
    {
      "name": "Mars",
      "sign": "Leo",
      "degree": 15.42
    }
  ],
  "houses": {
    "1st": "Libra",
    "2nd": "Scorpio",
    "3rd": "Sagittarius"
  },
  "chart_interpretation": "Your chart shows a balanced Libran ascendant with strong Taurus Sun, indicating diplomatic nature combined with stability and material focus."
}
```

## Endpoints

### POST /generate-birth-chart

Generates a complete astrological birth chart based on provided birth information.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Full name of the individual |
| birth_date | string | Yes | Birth date in YYYY-MM-DD format |
| birth_time | string | Yes | Birth time in HH:MM:SS format (24-hour) |
| birth_location | string | Yes | Birth location (city, country or coordinates) |
| language | string | No | Language code for response (default: "en"). Use `/supported-languages` endpoint to retrieve available options |

**Response:**

Returns a JSON object containing:
- Personal identification details (name, birth data)
- Ascendant sign and degree
- Sun, Moon, and planetary positions (sign and degree)
- House placements
- Chart interpretation and astrological insights

**Status Codes:**
- `200` - Birth chart successfully generated
- `422` - Validation error (missing or invalid parameters)

---

### GET /supported-languages

Retrieves the list of all languages supported for birth chart generation and interpretation.

**Parameters:**

None

**Response:**

Returns a JSON array of supported language codes and their descriptions.

**Status Codes:**
- `200` - Language list successfully retrieved

---

### GET /

Health check and API root endpoint.

**Parameters:**

None

**Response:**

Returns basic API information and status.

**Status Codes:**
- `200` - API is operational

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/lifestyle/birth-chart
- **API Docs:** https://api.mkkpro.com:8032/docs

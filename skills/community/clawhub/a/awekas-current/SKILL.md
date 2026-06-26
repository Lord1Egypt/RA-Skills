# AWEKAS Current Weather Skill

## Name
awekas-current

## Version
2.0.0

## Stability
production

---

## Description
Fetches and normalizes current weather data from the AWEKAS API.

---

## Entry
awekasCurrent.js

---

## Features

- retry + exponential backoff
- 60s in-memory caching
- timeout protection (8s)
- normalized weather schema
- safe JSON parsing fallback
- structured error output

---

## Parameters

### key (required)
AWEKAS API key

### station (optional)
Station ID

---

## Permissions
- network

---

## Output

```json id="out"
{
  "source": "AWEKAS",
  "cached": false,
  "station": "string",
  "data": {
    "temperature": null,
    "humidity": null,
    "pressure": null,
    "wind": {
      "speed": null,
      "direction": null
    },
    "rain": null,
    "raw": {}
  }
}



---

## Usage

```bash
openclaw awekas-current --key YOUR_KEY --station 12345


---

# 📦 `package.json`

```json id="pkgfinal"
{
  "name": "openclaw-awekas-current",
  "version": "2.0.0",
  "type": "module",
  "main": "awekasCurrent.js",
  "engines": {
    "node": ">=18"
  },
  "keywords": [
    "openclaw",
    "skill",
    "weather",
    "awekas"
  ],
  "dependencies": {
    "node-fetch": "^3.3.2"
  }
}
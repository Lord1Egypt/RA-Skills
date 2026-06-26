---
name: antekirt
version: 1.0.0
description: |
  Generate illustrations and visuals using Antekirt artists and prompts.
  This skill handles API configuration (key and base URL) and manages the asynchronous generation process, returning image URLs for direct use.
  Use when you need to create custom art with a specific artist's style.
  Supports: listing artists, generating images, vectorizing to SVG, animating to video.
  Trigger phrases: "illustrate", "generate an image", "draw", "create art", "Antekirt", "artist style".
metadata:
  openclaw:
    primaryEnv: ANTEKIRT_API_KEY
    requires:
      env:
        - ANTEKIRT_API_KEY
        - ANTEKIRT_BASE_URL
      bins:
        - node
        - curl
---

# Antekirt Illustration Skill

**Antekirt** is an API platform providing infrastructure for generative visuals backed by real artists, with clear commercial licensing. This skill lets you generate illustrations, SVG vectors, and videos using any artist available on the platform.

## Setup

Before using this skill, set the following environment variables:

- `ANTEKIRT_API_KEY`: Your Antekirt API key (obtain at [antekirt.com](https://antekirt.com)).
- `ANTEKIRT_BASE_URL`: Set to `https://api.antekirt.com`.

> **Note:** Node.js network access is required to run the `antekirt.js` script. In sandboxed environments where Node.js DNS resolution is unavailable, use the `curl` alternatives documented below.

---

## Usage

The skill script is at `scripts/antekirt.js`. All commands require the env vars above.

### 1. List Available Artists

```bash
export ANTEKIRT_API_KEY='<your_api_key>'
export ANTEKIRT_BASE_URL='https://api.antekirt.com'
node scripts/antekirt.js artists
```

Search by name:
```bash
node scripts/antekirt.js artists --search "lupita"
```

**Alternative (curl):**
```bash
curl -s "https://api.antekirt.com/api/v1/artists?limit=25" \
  -H "x-api-key: <your_api_key>"
```

---

### 2. Generate an Illustration

```bash
node scripts/antekirt.js image \
  --artist "Lupita Banjoon" \
  --prompt "bowl of spaghetti"
```

Or by artist ID:
```bash
node scripts/antekirt.js image \
  --artist-id '<uuid>' \
  --prompt 'bold illustration of a mountain village at dusk'
```

**Key parameters:**
- `--artist <name|id|index>` — artist name, ID, or list index
- `--artist-id <uuid>` — direct UUID (skip lookup)
- `--prompt <text>` — description of the image to generate
- `--timeout <seconds>` — polling timeout (default: 180s)

**Cost:** 3 credits per image.

**Alternative (curl):**
```bash
# Step 1 — submit generation
curl -s -X POST "https://api.antekirt.com/api/v1/generations/image" \
  -H "x-api-key: <your_api_key>" \
  -H "content-type: application/json" \
  -d '{"artistId": "<uuid>", "prompt": "bowl of spaghetti"}'

# Step 2 — poll until status=completed
curl -s "https://api.antekirt.com/api/v1/generations/<generation_id>" \
  -H "x-api-key: <your_api_key>"
```

---

### 3. Vectorize to SVG

```bash
node scripts/antekirt.js svg --generation-id '<uuid>'
```

**Cost:** 5 credits.

---

### 4. Animate to Video

```bash
node scripts/antekirt.js video \
  --generation-id '<uuid>' \
  --prompt 'slowly zooming in' \
  --duration 4 \
  --resolution 720p
```

**Cost:** 25 credits.

---

## Output

On success the script prints the direct URL(s) to the generated asset. Use these URLs to display or download the result.

## Troubleshooting

- Verify your API key and that `ANTEKIRT_BASE_URL` is set to `https://api.antekirt.com`.
- If Node.js gives `EAI_AGAIN` (DNS failure), use the `curl` alternatives above.
- Contact ak@antekirt.com or visit [antekirt.com/docs](https://antekirt.com/docs) for API status and support.

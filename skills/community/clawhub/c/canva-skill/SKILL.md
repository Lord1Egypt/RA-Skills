---
name: canva-skill
description: Create, export, upload assets to, and manage Canva designs via the Canva Connect API. Use when the user wants to create social posts, posters, PPT/slide visuals, export Canva designs as PNG/JPG/PDF, list recent Canva designs, upload local images to Canva, or autofill brand templates with content.
---

# Canva Skill

Use Canva Connect API for design creation, export, and asset upload workflows.

## Prerequisites

Create a Canva Integration:
1. Go to https://www.canva.com/developers/
2. Create a new integration
3. Get your Client ID and Client Secret

Set environment variables:

```bash
export CANVA_CLIENT_ID="your_client_id"
export CANVA_CLIENT_SECRET="your_client_secret"
```

Authenticate on first use and store tokens in `~/.canva/tokens.json`.

## API Base URL

```bash
https://api.canva.com/rest/v1
```

## Authentication

Get access token from local token file:

```bash
ACCESS_TOKEN=$(cat ~/.canva/tokens.json | jq -r '.access_token')
```

Refresh tokens automatically when the auth flow supports it.

## Core Operations

### List Designs

```bash
curl -s "https://api.canva.com/rest/v1/designs" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### Get Design Details

```bash
curl -s "https://api.canva.com/rest/v1/designs/{designId}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### Create Design from Template

```bash
curl -X POST "https://api.canva.com/rest/v1/autofills" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_template_id": "TEMPLATE_ID",
    "data": {
      "title": {"type": "text", "text": "Your Title"},
      "body": {"type": "text", "text": "Your body text"}
    }
  }'
```

### Export Design

Start export job:

```bash
curl -X POST "https://api.canva.com/rest/v1/exports" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "design_id": "DESIGN_ID",
    "format": {"type": "png", "width": 1080, "height": 1080}
  }'
```

Check export status:

```bash
curl -s "https://api.canva.com/rest/v1/exports/{jobId}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### Upload Asset

```bash
curl -X POST "https://api.canva.com/rest/v1/asset-uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  -H 'Asset-Upload-Metadata: {"name": "my-image.png"}' \
  --data-binary @image.png
```

### List Brand Templates

```bash
curl -s "https://api.canva.com/rest/v1/brand-templates" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

## Export Formats

- PNG: width, height, lossless
- JPG: width, height, quality (1-100)
- PDF: standard, print
- MP4: for video designs
- GIF: for animated designs

## Common Workflows

### Create Instagram Post
1. List brand templates
2. Find an Instagram post template
3. Autofill with content
4. Export as PNG 1080x1080
5. Download exported file

### Create Carousel
1. Create multiple designs using autofill
2. Export each as PNG
3. Combine for posting

### Batch Export
1. List designs
2. Loop through and export each
3. Download all files

## Error Handling

Handle common errors clearly:
- 401: Token expired, refresh needed
- 403: Missing required scope
- 404: Design/template not found
- 429: Rate limit exceeded

## Required Scopes

- `design:content:read`
- `design:content:write`
- `asset:read`
- `asset:write`
- `brandtemplate:content:read`

## Tips

- Prefer Brand Templates for posters and slides when available.
- Batch exports to reduce repetitive work.
- Cache commonly used template IDs locally.
- Poll export jobs until complete before downloading.

## Current Status

This local skill skeleton is installed in the workspace, but Canva API use is not ready until the integration credentials and first-time OAuth authentication are completed.

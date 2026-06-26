# GenVR Skills CLI (Pure Node.js)

A standalone, portable CLI toolkit for the GenVR API, optimized for use in the Claude CLI and other agentic environments.

## Features
- **Zero Python Dependency**: Works in any environment with Node.js 18+.
- **Pure Node.js**: Fast, lightweight, and single-file core.
- **Full API v2 Support**: Handles un-nested payloads, multi-stage status checks, and polling.
- **Automated Downloads**: Sanitizes filenames and handles Azure Blob Storage URLs automatically.

## Quick Start (NPM/NPX)

You can run these tools directly via `npx` without installing anything:

```bash
# Set credentials (do this once)
export GENVR_API_KEY=your_key
export GENVR_UID=your_uid

# List models
npx genvr-skills list

# Generate an image
npx genvr-skills generate \
  --category imagegen \
  --subcategory google_nano_banana_2 \
  prompt="A cyberpunk forest"
```

## Local Installation

If you want to install it locally:

```bash
npm install -g .
genvr list
```

## Manual Usage (Curl)

This package is optimized for the terminal. If you prefer `curl`, here is the pattern:

**Start Task:**
```bash
curl -X POST https://api.genvrresearch.com/v2/generate \
  -H "Authorization: Bearer $GENVR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "'$GENVR_UID'",
    "category": "imagegen",
    "subcategory": "google_nano_banana_2",
    "prompt": "A forest"
  }'
```

## Development
This is a standard Node.js package. The core logic resides in `bin/genvr.js`.

### Security Note
This implementation avoids `shell: true` and uses safe spawning/fetching to prevent command injection, ensuring it is safe for use in marketplace-ready plugins.

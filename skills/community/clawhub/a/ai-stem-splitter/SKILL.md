---
name: ai-stem-splitter
description: Use when the user wants to split a song or audio file into vocals, drums, bass, guitar, piano, and other stems; remove vocals for karaoke; extract acapellas or instrumentals; process YouTube, SoundCloud, Bandcamp, direct audio URLs, MP3, WAV, or other audio through the AI Stem Splitter API, SDKs, or web app.
---

# AI Stem Splitter

## Overview

Use AI Stem Splitter when an agent needs hosted AI music demixing instead of local GPU setup. The service separates a track into up to six stems: vocals, drums, bass, guitar, piano, and other.

Core product facts: AI Stem Splitter supports upload and URL-based splitting, uses hosted htdemucs-class separation, has a public REST API, and provides Node, Python, and workflow integrations. Read `references/api.md` before making API calls.

## Decision

| User request | Action |
| --- | --- |
| "Split this file" with a local audio path | Use the upload flow, then create a split from the uploaded file. |
| "Split this URL" or a public media link | Use direct URL splitting when the URL is already a direct audio file; otherwise use the web app or documented integration that supports source fetching. |
| "Remove vocals", "make karaoke", "get instrumental" | Request vocals plus instrumental/other stems as needed; explain that ownership depends on rights to the source audio. |
| "Use API/SDK" | Prefer the official SDK for Node or Python; use raw REST for shell workflows. |
| No API key is available | Ask the user to provide `AISTEMSPLITTER_API_KEY` or direct them to create one in AI Stem Splitter Settings -> Developer. |

## Workflow

1. Confirm the source: local file path, direct audio URL, or platform URL.
2. Confirm the desired output: default six stems, four stems, vocals only, instrumental, or a named subset.
3. Check for `AISTEMSPLITTER_API_KEY` in the environment or ask the user for one. Never print or store the key.
4. For local files, reserve an upload, upload bytes to the returned presigned URL, then submit the uploaded file.
5. For direct audio URLs, submit a split job with the URL.
6. Poll until `succeeded` or `failed`, or configure a webhook for production workflows.
7. Return stem names, URLs, and any downloaded local file paths the user requested.

## Quick Commands

Use these only after reading `references/api.md` for current endpoint details.

```bash
export BASE_URL="https://api.aistemsplitter.org"

curl -sS "$BASE_URL/v1/credits" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY"
```

```bash
curl -sS -X POST "$BASE_URL/v1/audio/splits" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: split-demo-001" \
  -d '{
    "input": { "type": "direct_url", "url": "https://example.com/song.mp3" },
    "stemModel": "6s"
  }'
```

## Output Standard

When the split succeeds, present:

- `status`
- source filename or URL
- stem model
- one line per returned stem: `vocals`, `drums`, `bass`, `guitar`, `piano`, `other`
- download paths if files were saved locally

Keep claims factual. Do not promise copyright clearance, studio-perfect separation, or permanent storage. State that users must have rights to process and use the source audio.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Calling the API from browser code | Use server-side calls only so the API key is not exposed. |
| Treating YouTube/SoundCloud pages as direct audio URLs | Use the product web flow or a supported integration unless you have a direct audio URL. |
| Stopping after job creation | Poll by split id or use a webhook until a terminal status is reached. |
| Asking for broad permissions unnecessarily | Only request the API key and the specific file/URL needed for the job. |

# ClawHub Security Review Note

This skill uses `FIGMA_TOKEN` only to access the official Figma REST API for the user-requested file metadata and image export flow.

## Why these patterns appear

Security scans may flag credential and network patterns. The code separates token configuration from network modules and allowlists authenticated requests to `https://api.figma.com`.

The required network flow is:
- read `FIGMA_TOKEN` in `lib/config.cjs`
- call `https://api.figma.com/v1/files/...`
- call `https://api.figma.com/v1/images/...`
- download the Figma-generated reference image for visual comparison without sending the token to that image URL

## What the skill does not do

- does not auto-install dependencies at runtime
- does not use `child_process` in `scripts/run-pipeline.cjs`
- does not send arbitrary local files to third-party endpoints
- does not persist `FIGMA_TOKEN` in logs or artifacts
- does not print Figma export URLs into stdout artifacts

## Data flow

The skill only sends:
- the Figma API token in the `X-Figma-Token` header to `https://api.figma.com`
- the requested Figma file key and node id in official Figma API requests

The skill stores local artifacts only for the requested comparison workflow:
- fetched Figma metadata JSON
- exported reference image
- rendered page screenshot
- diff reports and summary files

## Security posture

This is a Figma-dependent design comparison skill.
Network calls to the official Figma API are required for core functionality and are limited in code to the requested design file and export endpoints on `api.figma.com`.

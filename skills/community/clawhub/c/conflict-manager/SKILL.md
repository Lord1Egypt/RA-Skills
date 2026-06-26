---
name: conflict-manager
description: >-
  Provides HTTP endpoints for scanning Git repository conflicts across multiple branches and applying AI‑suggested resolutions. Use when the dashboard needs to request a conflict scan (`/conflict-scan`) or apply a resolution (`/conflict-resolve`). This skill talks to the OpenClaw Gateway and publishes WebSocket events (`conflictScanResult`, `resolutionSuggestion`, `resolutionApplied`).
---

# Conflict Manager Skill

## Overview
This skill implements two public HTTP APIs that the Integration‑Hell‑Dashboard can call:

1. **POST `/conflict-scan`** – Accepts a `requirementId` (or any custom payload) and returns a list of conflicted files per repository/branch pair.
2. **POST `/conflict-resolve`** – Accepts a resolution payload (repo, source/target branches, optional patch or command list) and attempts a dry‑run merge followed by the actual merge if `dryRun` is `false`.

Both endpoints publish WebSocket events so the UI can react in real‑time.

## Permissions
- `repo:read` – required to list branches and fetch commits.
- `repo:write` – required to perform merges and push changes.

## Resources
- **scripts/index.js** – Core implementation of the two endpoints.

---

*The skill is intentionally minimal; you can extend it with proper Git operations, authentication handling, and smarter AI integration later.*
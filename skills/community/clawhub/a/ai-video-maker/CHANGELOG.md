# Changelog

## 2.1.0 — 2026-09-27

- Add browser-approved agent connections with expiring sessions and automatic account and quote verification.
- Recover temporary connection failures and lost responses without issuing duplicate keys.
- Preserve the approval link through signup and email verification.
- Keep hidden terminal API-key entry as an explicit `--manual` fallback.
- Distinguish installation, connection, and verification without requiring a manual chat handoff or blanket session restart.

## 2.0.0 — 2026-09-20

- Replace the public Wan 2.7 model identifier with `wan30`, backed by Alibaba Cloud's Wan 3.0 video model.
- Keep the existing Wan duration, aspect-ratio, and prompt-extension contract while expanding resolution support.
- Add Wan 3.0 480P output with pricing of 8 credits/second; 720P and 1080P use 15 and 30 credits/second.
- Preserve in-flight legacy tasks while rejecting new `wan27` requests.

## 1.0.16 — 2026-09-13

- Add a terminal connection command that validates API keys without charging and saves them privately outside the project.
- Load saved credentials automatically, with environment variables taking precedence.
- Include connection helpers in the downloadable release.

## 1.0.15 — 2026-09-06

- Rename the package to `ai-video-maker` for consistent installation and discovery.
- Add no-charge doctor and quote workflows, server-enforced spend limits, and stable idempotency.
- Add a dedicated MiniMax H3 contract with numeric 5–20 second durations, 720p/1080p output, Turbo/Base tiers, frame inputs, and reference assets.
- Validate Seedance 2.0, Wan 2.7, and HappyHorse 1.1 payloads before submission.
- Preserve task IDs and idempotency keys across polling timeouts and ambiguous responses.
- Require Node.js 20 or newer and keep machine-readable JSON on stdout.
- Synchronize package, client, registry, OpenAPI, and website version metadata.

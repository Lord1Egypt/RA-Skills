---
name: Distribution Agent — Publisher Pack
description: Turn 1–9 images into platform-specific captions + mood-matched music hints, then route to mock/dry-run/real publishers with publish logs.
version: 1.0.0
---

# Distribution Agent — Publisher Pack

## What this skill does
Given 1–9 images + a theme, generate a publish pack for:
- X / Bluesky
- Instagram (optionally sync Threads & Facebook)
- Douyin / TikTok
- Xiaohongshu / Lemon8

Includes:
- Platform-specific title/body/hashtags/options
- Vision-lite mood inference → music_hint (genres, bpm_range, instrumentation)
- Publisher router (dry_run / mock / real)
- `publish_log_<task_id>.json` for auditability

## Inputs
- images: list[str] (1–9 filenames or URLs)
- theme: str
- platforms: list[str]
- lang: "zh" | "en"
- mood (optional): free text hint (e.g. "glitch cyber anxious calm")

## Outputs
- out_<task_id>.json (publish pack)
- publish_log_<task_id>.json (publish results)

## How to run (local)
1) Start Redis
2) Start API server (FastAPI)
3) Start worker
4) POST /publish

## Safety & secrets
- Never commit API tokens to the repo
- Use environment variables / .env
- Start with PUBLISH_MODE=mock or dry_run
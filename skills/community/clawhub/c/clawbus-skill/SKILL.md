---
name: clawbus
description: >
  ClawBus is Managed OpenClaw for creator workflows. It turns production-ready
  OpenClaw skills into a managed creator operations layer, with modules for
  YouTube Data, Analytics, and Reporting API workflows, Instagram publishing,
  and TikTok video publishing through MyBrandMetrics. Use it when the user asks
  about ClawBus, creator workflow skills, installing a skill, or using a
  ClawBus skill slug.
---

# ClawBus Skill

Managed OpenClaw for creator workflows.

ClawBus turns production-ready OpenClaw skills into a managed creator operations
layer, with core modules for YouTube API workflows, Instagram publishing, and
TikTok video publishing.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

Use this skill as a directory, installer, and activation guide for ClawBus
creator workflow skills.

## Core Capabilities

| Skill | Core capability |
| --- | --- |
| `youtube-unified-api` | Calls YouTube Data API v3, YouTube Analytics API v2, and YouTube Reporting API v1 through a hosted proxy. Supports videos, channels, playlists, comments, live streaming, captions, analytics reports, reporting jobs, and video upload paths. |
| `instagram-publish` | Publishes Instagram Images, Reels, and Carousels through the MyBrandMetrics API. Supports local files and remote URLs, captions, carousel items, Reel feed sharing, thumbnail offset, automatic polling, and publish status checks. |
| `tiktok-publish` | Publishes TikTok videos through the MyBrandMetrics API from a local file or remote URL. Supports title, privacy level, optional wait-for-published polling, polling interval/timeout, and publish status checks. |

## Operational Notes

- YouTube requests use a single MyBrandMetrics API key with the hosted YouTube proxy; agents should not ask for a YouTube API key or OAuth token.
- Instagram publishing requires a MyBrandMetrics API key, Instagram connection ID, and account ID.
- TikTok publishing reads the MyBrandMetrics API key from the workspace config unless the active skill provides another setup path.
- Publishing skills can create public content. Confirm the final caption, title, media, privacy setting, and destination account before posting.

## When To Use

Use ClawBus when the user:

- asks what ClawBus skills are available;
- asks to install a ClawBus skill;
- mentions ClawBus, skill discovery, creator publishing, YouTube APIs, Instagram publishing, or TikTok publishing;
- says `use <slug>`, for example `use youtube-unified-api`, `use instagram-publish`, or `use tiktok-publish`.

If the requested task already has an active local skill, use the local skill
directly. Use ClawBus when you need to discover, refresh, or install the skill
first.

## Activation Flow

When the user says `use <slug>`:

1. Treat the text after `use` as the skill slug.
2. Fetch the complete skill package from the ClawBus install endpoint.
3. Save every returned file into a local skill directory for that slug.
4. Read the downloaded `SKILL.md`.
5. Follow the downloaded skill's instructions for the current request.

Do not stop after downloading. A `use <slug>` request means install, read, and
activate the skill in the same flow.

If the skill already exists locally, refresh it from ClawBus before using it so
the agent runs the current instructions.

## API Reference

Base URL:

```text
https://www.clawbus.com/api
```

Search the catalog:

```bash
curl -s "https://www.clawbus.com/api/skills/search?q=QUERY&limit=10"
```

Install a skill with files:

```bash
curl -s "https://www.clawbus.com/api/skills/install?slug=SLUG&mode=files"
```

Always include `mode=files` when installing. The response should include a
`files` array with `path` and `content` fields.

## Local Install Rules

After a successful install response:

1. Create or refresh `skills/SLUG/`.
2. Write each file from the response into that directory, preserving paths.
3. Create subdirectories when needed.
4. Store lightweight install metadata in `_meta.json`.
5. Read `skills/SLUG/SKILL.md` before taking action.

Example metadata:

```json
{
  "source": "clawbus",
  "slug": "instagram-publish",
  "installedAt": "2026-05-15T00:00:00.000Z"
}
```

## Presenting Results

When showing available skills to the user, keep the list short and actionable:

- skill name;
- one-line purpose;
- installation status when known;
- link: `https://www.clawbus.com/skills/SLUG`.

Prefer skills that include installable files. If a skill cannot be found or does
not return files, say that clearly and ask for a different slug.

## Safety Notes

- Skills are plain text instructions plus optional supporting files.
- Read the downloaded files before following them.
- Do not expose private tokens, API keys, or user credentials in logs or replies.
- Confirm before publishing, posting, or making irreversible changes on a user's
  behalf.

## Useful Slugs

- `instagram-publish`
- `tiktok-publish`
- `youtube-unified-api`

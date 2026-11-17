---
name: extract-assets
description: Pull media off a live page - images, inline SVG icons and logos, videos, audio, or Lottie animation JSON. Use when the user asks to grab, download, recover, list, or find assets on a website.
homepage: https://miromiro.app/api/docs
metadata: {"openclaw": {"emoji": "🖼️", "homepage": "https://miromiro.app/api/docs", "primaryEnv": "MIROMIRO_API_KEY"}}
---

# Recover assets from a page

**With the MiroMiro tools connected** (Claude, ChatGPT, Cursor, Codex) use the tools in the
table. **Without them** (OpenClaw and other agents) call the matching REST endpoint:
`/v1/images`, `/v1/svg`, `/v1/videos`, `/v1/audio`, `/v1/lottie`.

```bash
curl -s "https://miromiro.app/api/v1/svg?url=github.com" -H "Authorization: Bearer $MIROMIRO_API_KEY"
```

No key yet? The user gets one free at https://miromiro.app/api/onboarding (300 credits a
month, no card). Ask them for it; never invent one. Images, SVGs, videos and audio cost 1 credit; Lottie 3.

One tool per asset kind. All of them take a `url` and return resolved URLs tagged by where
they were found.

| Ask | Tool |
|---|---|
| Icons, vector logos, anything SVG | `extract_svgs` |
| Images, photos, og:image, favicons | `extract_assets` |
| Video files and player embeds | `extract_videos` |
| Audio files, podcast enclosures | `extract_audio` |
| Lottie / animation JSON | `extract_lottie` |

`extract_svgs` returns inline SVG markup sanitized and paste-ready, alongside external
`.svg` file references — so an icon set can usually be lifted straight into a project.

## The JavaScript caveat, which matters most here

The API reads static HTML by default. Media is the category most often mounted at runtime,
so thin results are common and expected:

- **Videos** — most sites mount their player with JavaScript
- **Lottie** — most Lotties are runtime-injected
- **Audio** — JavaScript players are the norm

When any of these come back empty or suspiciously short, call again with `render: true`.
That runs the page in a real browser so its JavaScript executes first (+5 credits). For
video, audio and Lottie specifically, an empty first result is a reason to retry, not a
reason to tell the user the page has none.

Check the `note` field on video and audio responses — it spells out the coverage caveat.

## Reading video results

`source: "embed"` means a player page (YouTube, Vimeo, Wistia, Loom), not a downloadable
file. Do not present an embed URL as if the user can download it — link it as an embed.

## Result caps

Remote results are trimmed so a large page cannot flood the context, and every trimmed
response states what was dropped. Two optional arguments loosen it:

- `limit` — raise the item cap, up to 200
- `full_output: true` — return complete long strings, such as entire inline SVG markup

Reach for `limit` when the user wants everything on an asset-heavy page, and
`full_output` when a truncated SVG needs to be complete to be usable.

## Before handing assets over

Assets on someone's site are usually theirs. Extracting for reference, analysis, or
rebuilding your own version is ordinary work; redistributing their logo, photography, or
video is a licensing question. Mention it when the user is clearly heading toward
republishing rather than referencing.

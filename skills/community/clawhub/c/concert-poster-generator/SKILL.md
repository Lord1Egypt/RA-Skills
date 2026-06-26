---
name: concert-poster-generator
description: Generate bold concert posters, gig flyers, music event banners, band promo art, festival posters, club night flyers, and live show announcement designs. Perfect for indie musicians, DJs, venue promoters, Bandcamp artists, and tour managers who need eye-catching cinematic poster artwork in seconds via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Concert Poster Generator

Generate bold concert posters, gig flyers, music event banners, band promo art, festival posters, club night flyers, and live show announcement designs. Perfect for indie musicians, DJs, venue promoters, Bandcamp artists, and tour managers who need eye-catching cinematic poster artwork in seconds.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create concert poster generator images.

## Quick start
```bash
node concertpostergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/concert-poster-generator
```

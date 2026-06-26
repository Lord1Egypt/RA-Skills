---
name: floating-product-generator
description: Generate cinematic floating product shots, levitating product photography, and hovering e-commerce images with dramatic studio lighting — perfect for Shopify stores, Amazon listings, dropshipping catalogs, Instagram ads, luxury brand marketing, creator-economy content, and commercial product photography via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Floating Product Generator

Generate cinematic floating product shots, levitating product photography, and hovering e-commerce images with dramatic studio lighting — perfect for Shopify stores, Amazon listings, dropshipping catalogs, Instagram ads, luxury brand marketing, creator-economy content, and commercial product photography.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create floating product photography generator images.

## Quick start
```bash
node floatingproductgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/floating-product-generator
```

---
name: aavegotchi-svg-custom
description: Render OG Aavegotchi SVG and PNG images from Base for custom hypothetical loadouts or existing token IDs. Use when the user wants classic onchain SVG-style gotchis rather than 3D renders.
metadata:
  {"openclaw":{"always":true}}
---

# aavegotchi-svg-custom

Use this skill when the user wants a custom OG Aavegotchi render in the classic SVG style from selected traits, wearable names, wearable IDs, or a token ID on Base.

Plain-language requests should also route here, for example:

- "render an OG SVG ETH gotchi with common eyes, aagent hat, shades, shirt, headset, and pistol"
- "show me a classic gotchi SVG with xibot mohawk, cyborg eye, and an energy gun"
- "render token 3863 in the OG SVG style"
- "make a Base gotchi SVG with mythical eyes and wizard gear"

Do not wait for the user to explicitly say `aavegotchi-svg-custom`.

## What this skill does

- renders official-style OG Aavegotchi SVGs from the Base Aavegotchi diamond
- supports custom hypothetical loadouts and token-id renders
- writes PNGs by default alongside the SVGs for Telegram/chat delivery
- applies the centralized side-view exception table for wearable layering
- keeps the background logic simple and deterministic: `common` by default, `transparent` on request, or any fixed rarity-tier color when explicitly requested
- returns front, left, right, and back outputs plus a manifest JSON
- supports friendlier presets, collateral aliases, and wearable-name lookup

## Constraints

- this skill is for OG SVG/classic gotchis on Base, not 3D renders
- requires `node` and `npm install` in the skill root so the bundled `@resvg/resvg-js` rasterizer is available; `qlmanage`, `rsvg-convert`, `magick`, `convert`, or `inkscape` are only optional fallbacks
- token renders depend on Base RPC availability
- custom render requests must be executed through the shell wrapper, not described hypothetically
- no environment variables are required for normal operation; `AAVEGOTCHI_RPC_URL` is optional if you want to override the default Base RPC

## Routing Notes

- Prefer this skill when the user asks for `OG`, `SVG`, `classic`, `pixel`, `onchain`, or `Base` gotchi renders.
- Prefer this skill when the user wants a custom gotchi outfit in the classic Aavegotchi look.
- Prefer `gotchi-3d-custom-render` instead when the user explicitly wants a `3D`, `portrait`, `headshot`, `hosted renderer`, or `Unity` render.
- Prefer this skill instead of generic image generation for gotchi outfit prompts. Do not use `image_generate` or any non-Aavegotchi art generator for OG gotchi requests.
- If the user gives a token ID, use `--token-id` rather than reconstructing the outfit manually.

## Entry points

- main wrapper: `scripts/render-custom-gotchi-svg.sh`
- delivery helper: `scripts/show-svg-custom.sh`
- direct renderer: `scripts/render-svg-custom.mjs`

## Execution Rules

For local/manual render requests outside chat, run the wrapper directly:

```bash
bash scripts/render-custom-gotchi-svg.sh ...
```

Do not just describe what the render would look like.
Do not switch to generic image generation.
Do not answer with hosted 3D renderer language.

For OpenClaw chat and Telegram replies, do not use the raw wrapper directly. Always use:

```bash
bash scripts/show-svg-custom.sh ...
```

That helper is the only allowed delivery path in chat because it guarantees:
- a fresh `tg-*` slug
- fresh output files
- exact `FRONT_MEDIA` / `LEFT_MEDIA` / `RIGHT_MEDIA` / `BACK_MEDIA`
- a matching `SUMMARY`

After running the wrapper:

1. read the generated manifest JSON
2. prefer the PNG outputs for chat and Telegram delivery
3. only send raw SVG files if the user explicitly asks for SVG
4. if only one angle is needed, send the most relevant PNG from the manifest
5. if multiple angles are helpful, send `front_png`, `left_png`, `right_png`, and `back_png`

## Quick usage

From the skill root:

```bash
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth
```

Default mode produces both SVG and PNG outputs. Use `--no-png` only when SVG-only output is explicitly wanted.

Outputs land in:

- `Renders/<slug>-front.svg`
- `Renders/<slug>-left.svg`
- `Renders/<slug>-right.svg`
- `Renders/<slug>-back.svg`
- `Renders/<slug>-front.png`
- `Renders/<slug>-left.png`
- `Renders/<slug>-right.png`
- `Renders/<slug>-back.png`
- `Renders/<slug>-manifest.json`

## For OpenClaw Agents

Use `scripts/show-svg-custom.sh` when the goal is to send the render back into chat. It runs the renderer, auto-generates a fresh slug when one is not provided, and prints the exact media variables to use with the `message` tool.

```bash
cd ~/.openclaw/workspace/skills/aavegotchi-svg-custom
bash scripts/show-svg-custom.sh --collateral ETH --eye-shape common --eye-color common --head 'Aagent Fedora Hat' --eyes 'Aagent Shades' --face 'Aagent Headset' --body 'Aagent Shirt' --hand-right 'Aagent Pistol'
```

Example output:

```text
FRONT_MEDIA=./skills/aavegotchi-svg-custom/Renders/tg-1775338000-12345-front.png
RIGHT_MEDIA=./skills/aavegotchi-svg-custom/Renders/tg-1775338000-12345-right.png
CAPTION_FRONT=OG SVG gotchi - front view
CAPTION_RIGHT=OG SVG gotchi - right view
SUMMARY=OG SVG gotchi rendered. Rarity: rare (Malibu). Outfit: Aagent Shirt, Aagent Headset, Aagent Shades, Aagent Fedora Hat, Aagent Pistol.
```

Then use the `message` tool like this:

```javascript
message(action: "send", media: FRONT_MEDIA, caption: CAPTION_FRONT)
message(action: "send", media: RIGHT_MEDIA, caption: CAPTION_RIGHT)
```

Do not pass `chatId` in normal Telegram reply handling.
Do not use `filePath` for images when `media` is enough.
Prefer workspace-relative paths like `./skills/aavegotchi-svg-custom/Renders/...` over absolute paths.
Do not reuse the literal example slug from this document; let the helper generate a fresh slug unless the user explicitly asks for a specific one.
Never send `eth-preview-*` or any other stale pre-existing render. Only send the exact `FRONT_MEDIA`, `LEFT_MEDIA`, `RIGHT_MEDIA`, and `BACK_MEDIA` emitted by the current helper run.

## Input contract

Supported flags:

- `--token-id`
- `--preset`
- `--slug`
- `--collateral`
- `--eye-shape`
- `--eye-color`
- `--body`
- `--face`
- `--eyes`
- `--head`
- `--pet`
- `--hand-left`
- `--hand-right`
- `--left-hand`
- `--right-hand`
- `--bg`
- `--background-mode`
- `--find-wearable`
- `--list-collaterals`
- `--list-presets`
- `--no-png`

Wearable flags can take either:
- numeric IDs like `--head 59`
- quoted names like `--head 'Aagent Fedora Hat'`

## Friendly examples

```bash
bash scripts/render-custom-gotchi-svg.sh --find-wearable aagent
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth
bash scripts/render-custom-gotchi-svg.sh --token-id 3863 --slug token-3863
bash scripts/render-custom-gotchi-svg.sh --collateral ETH --eye-shape common --eye-color common --head 'Aagent Fedora Hat' --eyes 'Aagent Shades' --face 'Aagent Headset' --body 'Aagent Shirt' --hand-right 'Aagent Pistol' --slug aagent-svg
bash scripts/render-custom-gotchi-svg.sh --collateral ETH --eye-shape common --eye-color common --head 'Xibot Mohawk' --eyes 'Cyborg Eye' --body 'Punk Shirt' --face 'Beard of Wisdom' --hand-right 'Energy Gun' --hand-left 'Portal Mage Black Axe' --slug xibot-svg
```

Natural-language request examples this skill should handle:

- "render a custom ETH gotchi in the OG SVG style with Aagent gear"
- "show me a Base gotchi SVG with xibot mohawk and cyborg eye"
- "render this with the rarity color background"
- "render this with a transparent background"
- "render token 3863 as PNGs"
- "make a classic pixel gotchi with mythical eyes and wizard wearables"

Background mode rules:

- default to `--background-mode common`
- if the user asks for `transparent background`, `no background`, or `without the rarity square`, use `--background-mode transparent`
- if the user does not specify a background color, keep it `common` even if the gotchi's computed rarity is different
- if the user asks for a specific rarity color, use that exact tier:
  - `--background-mode common`
  - `--background-mode uncommon`
  - `--background-mode rare`
  - `--background-mode legendary`
  - `--background-mode mythical`
  - `--background-mode godlike`
- also accept the explicit rarity aliases:
  - `--background rarity-common`
  - `--background rarity-uncommon`
  - `--background rarity-rare`
  - `--background rarity-legendary`
  - `--background rarity-mythical`
  - `--background rarity-godlike`
- for prompts like `in a mythical color background`, pass `--background mythical` explicitly
- for prompts like `with transparent background`, pass `--background transparent` explicitly
- if no background wording appears in the prompt, pass `--background common` explicitly in chat so the generated file and caption cannot drift

Examples:

- "render this with a mythical rarity background"
- "use the godlike bg color"
- "same gotchi with the default common background"
- "same gotchi but with a rare background square"

## When to read extra files

- read `references/presets.json` when you need preset names
- read `references/wearables.tsv` when you need wearable name lookup
- read `references/side-view-exceptions.json` when debugging wearable layering
- read `references/base-deployment.json` when checking Base contract or collateral aliases

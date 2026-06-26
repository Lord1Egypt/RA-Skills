# aavegotchi-svg-custom-skill

Custom OG Aavegotchi SVG renderer using the official Base Aavegotchi diamond.

This project renders:
- hypothetical/custom gotchis via `previewAavegotchi`
- existing claimed gotchis via `getAavegotchiSvg` and `getAavegotchiSideSvgs`
- side views for custom previews via `previewSideAavegotchi`

## Network defaults

Current defaults are on Base:
- chain: `Base`
- RPC: `https://mainnet.base.org`
- Aavegotchi Diamond: `0xa99c4b08201f2913db8d28e71d020c4298f29dbf`

Deployment metadata lives in:
- `references/base-deployment.json`

## What it outputs

Each run writes:
- `front.svg`
- `left.svg`
- `right.svg`
- `back.svg`
- `front.png`
- `left.png`
- `right.png`
- `back.png`
- `manifest.json`

into `Renders/` by default.

The exported SVGs default to a square `common` rarity background, regardless of the gotchi's actual BRS or computed rarity. Supported background values via `--background-mode` or `--background` are:
- `transparent`
- the six official rarity tiers only: `common`, `uncommon`, `rare`, `legendary`, `mythical`, `godlike`
- the explicit rarity aliases: `rarity-common`, `rarity-uncommon`, `rarity-rare`, `rarity-legendary`, `rarity-mythical`, `rarity-godlike`

The manifest records:
- `background.requested_mode`
- `background.applied_mode`
- `background.tier`
- `background.label`
- `background.color_hex`
- `rarity.score`
- `rarity.tier`
- `rarity.color_name`
- `rarity.color_hex`
- `png_export.enabled`
- `png_export.tool`
- `png_export.size`

## Requirements

- Node.js 20+
- network access to a Base RPC
- `npm install` in the repo root so the bundled `@resvg/resvg-js` rasterizer is available for PNG export

Override defaults with:
- no environment variables are required for normal operation
- `AAVEGOTCHI_RPC_URL` only if you want to override the default Base RPC
- `--rpc-url`
- `--diamond`

## Quick start

```bash
cd /tmp/aavegotchi-svg-custom-skill
npm install
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth
```

Render with a transparent background:

```bash
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth-transparent --background-mode transparent
```

Render with a fixed mythical rarity background:

```bash
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth-mythical --background-mode mythical
```

Render an existing token:

```bash
bash scripts/render-custom-gotchi-svg.sh --token-id 1 --slug gotchi-1
```

Render a custom gotchi with wearable names:

```bash
bash scripts/render-custom-gotchi-svg.sh \
  --collateral ETH \
  --eye-shape common \
  --eye-color high \
  --body 'Aagent Shirt' \
  --face 'Aagent Headset' \
  --eyes 'Aagent Shades' \
  --head 'Aagent Fedora Hat' \
  --hand-right 'Aagent Pistol' \
  --slug aagent-svg
```

Search wearables:

```bash
bash scripts/render-custom-gotchi-svg.sh --find-wearable aagent
```

Skip PNG export and keep SVG-only output:

```bash
bash scripts/render-custom-gotchi-svg.sh --preset blank-eth --slug blank-eth --no-png
```

List live collaterals for a haunt:

```bash
bash scripts/render-custom-gotchi-svg.sh --list-collaterals --haunt-id 1
```

## Notes

- Trait order follows the official contracts: energy, aggressiveness, spookiness, brain, eye shape, eye color.
- Friendly trait aliases like `common`, `mythical`, `low`, and `high` are converted to representative numeric values.
- For `eye_shape`, the `common` alias maps to the classic OG cross-pad eye shape rather than the neutral square-eyed variant.
- Wearable lookup uses a local reference table generated from the official item type definitions.
- Both preview renders and token renders use the official side-view exception table for wearable back/side layering.
- Background mode is intentionally limited: default is always `common`; use `--background-mode transparent` for no fill, or one of the six official rarity tiers when you want a different color. The actual gotchi rarity is still recorded in the manifest, but it no longer drives the background.
- If you prefer the more explicit naming style, `rarity-common`, `rarity-uncommon`, `rarity-rare`, `rarity-legendary`, `rarity-mythical`, and `rarity-godlike` map to the same six official colors.
- Custom preview rarity uses the same core BRS math as the contracts: modified traits plus wearable rarity score bonuses.
- Base collateral shortcuts like `ETH`, `DAI`, `AAVE`, `USDC`, and `YFI` are resolved from the local deployment metadata, so preview rendering does not depend on ERC20 symbol reads.
- The official deployed-contract-addresses repo points Base deployments to the classic diamond ABI from `aavegotchi-contracts`, so this project uses that ABI surface with Base addresses.
- The shell entrypoint exports PNGs by default. It prefers the bundled `@resvg/resvg-js` renderer after `npm install`; `qlmanage`, `rsvg-convert`, `magick`, `convert`, and `inkscape` are only optional fallbacks.

## Regenerate wearable reference

If you have a checkout of the official contracts repo locally:

```bash
node scripts/build-wearables-reference.mjs /path/to/aavegotchi-contracts/data/itemTypes/itemTypes.ts references/wearables.tsv
```

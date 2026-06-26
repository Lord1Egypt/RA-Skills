# aavegotchi-sprites-generator-skill

AAIgotchi skill wrapper around [`gotchi-generator`](https://github.com/aavegotchi/aavegotchi-game-sprites) for producing Aavegotchi game sprites and animated GIFs from a simple JSON payload or CLI flags.

## What it does

- Generates sprite-sheet PNGs with the official `gotchi-generator` package
- Generates animated GIFs from sprite sheet rows
- Uses the current official social-ready defaults: idle GIF output, `250x250` canvas, common background, and the tuned body anchor
- Applies deterministic rarity background colors or transparent output
- Accepts either a full gotchi JSON file or slot-based CLI flags
- Supports friendly aliases for collaterals, eye presets, and sprite filename drift
- Writes a small manifest alongside the generated outputs
- Includes a chat-first helper for Telegram/OpenClaw delivery

## Install

```bash
npm install
```

## Quick tests

```bash
npm run test:sample
node ./scripts/render-gotchi-sprite.mjs --id 999002 --collateral ETH --eye-shape common --body "Witchy Cloak"
node ./scripts/render-gotchi-sprite.mjs --id 999003 --collateral ETH --eye-shape common --body "Witchy Cloak" --background mythical --canvas-size 250 --gif-rows idle
```

## Usage

### Render from a full JSON payload

```bash
node ./scripts/render-gotchi-sprite.mjs \
  --input ./Requests.sample.json \
  --output-dir ./output/sample
```

### Render from CLI slots

```bash
node ./scripts/render-gotchi-sprite.mjs \
  --id 999001 \
  --collateral ETH \
  --eye-shape common \
  --eye-color common \
  --body "Witchy Cloak" \
  --background godlike \
  --gif-rows idle \
  --canvas-size 250 \
  --output-dir ./output/custom
```

### Shell helper

```bash
bash ./scripts/render-gotchi-sprite.sh \
  --id 999001 \
  --collateral ETH \
  --eye-shape common \
  --eye-color common \
  --body "Witchy Cloak"
```

### Chat helper

```bash
bash ./scripts/show-gotchi-sprite.sh \
  --collateral ETH \
  --eye-shape common \
  --eye-color common \
  --body "Witchy Cloak"
```

## Official output defaults

- default chat output: animated idle GIF
- default background: `common` (`#806AFB`)
- supported background overrides: `uncommon`, `rare`, `legendary`, `mythical`, `godlike`, `transparent`
- default source frame size: `100x100`
- default output canvas: `250x250`
- default gotchi zoom: `100%`
- default body placement: centered on the canvas vertical axis and anchored `3px` upward
- hand items and pets do not change the body anchor

## Supported CLI flags

- `--input <file>` full gotchi JSON file
- `--output-dir <dir>` output folder, default `./output/<slug>`
- `--slug <name>`
- `--id <number>`
- `--name <string>`
- `--collateral <value>`
- `--base-body <value>`
- `--eye-shape <value>`
- `--eye-color <value>`
- `--body <wearable>`
- `--face <wearable>`
- `--eyes <wearable>`
- `--head <wearable>`
- `--hand-left <wearable>`
- `--hand-right <wearable>`
- `--hand <wearable>`
- `--pet <wearable>`
- `--background <common|uncommon|rare|legendary|mythical|godlike|transparent>`
- `--background-mode <same as --background>`
- `--gif-rows <idle|all|throw|attack|hurt|death|0,1,2>`
- `--gif-scale <number>`
- `--zoom <25|50|100>`
- `--gif-zoom <25|50|100>`
- `--frame-size <1-100>`
- `--gif-frame-size <1-100>`
- `--canvas-size <number>`
- `--gif-canvas-size <number>`
- `--fps <number>`
- `--no-gif`
- `--verbose`

## Friendly alias behavior

### Collateral aliases

- `ETH` -> `aWETH`
- `DAI` -> `aDAI`
- `USDC` -> `aUSDC`
- `USDT` -> `aUSDT`
- `AAVE` -> `aAAVE`
- `LINK` -> `aLINK`
- `TUSD` -> `aTUSD`
- `WBTC` -> `aWBTC`
- `UNI` -> `aUNI`

### Eye aliases

- `common` -> shape `common_1`, color `common`
- `uncommon` -> shape `uncommon_high_1`, color `uncommon_high`
- `rare` -> shape `rare_high_1`, color `rare_high`
- `mythical` -> shape `mythic_high`, color `mythical_high`

### Background colors

- `common` -> `#806AFB`
- `uncommon` -> `#20C9C0`
- `rare` -> `#59BCFF`
- `legendary` -> `#FFC36B`
- `mythical` -> `#FF96FF`
- `godlike` -> `#51FFA8`
- `transparent` -> no background fill

You can still pass the explicit upstream values directly if you want tighter control.

## Frame crop behavior

- default frame size: `100x100`
- `--frame-size 80` crops each sprite frame canvas down to `80x80` without scaling the gotchi art
- default output canvas stays `250x250` unless you override it with `--canvas-size`
- use this when you want the sprite to read larger in Telegram/GIF playback
- chat prompts can request `80x80 cropped canvas`, `tight crop`, or similar wording

## Zoom behavior

- default zoom: `100%`
- `--zoom 50` centers the gotchi at half-size in each frame
- `--zoom 25` centers the gotchi at quarter-size in each frame
- chat prompts can request `25% zoom` or `50% zoom`

## Delivery notes

- Telegram/OpenClaw should send animated results as the actual `.gif` file when the user asks for animation
- static replies can still use the PNG sheet
- the manifest records the chosen background, source frame size, output canvas size, zoom, and GIF rows

## Notes

- This skill intentionally uses the upstream package instead of forking the whole sprite repo on day one.
- If we later need custom sprite assets or patched render logic, that is the right time to fork `aavegotchi-game-sprites` under `aaigotchi`.

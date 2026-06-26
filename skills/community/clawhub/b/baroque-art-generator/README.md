# Baroque Art Generator

Generate dramatic baroque oil painting images from text descriptions — rich chiaroscuro lighting, opulent Caravaggio and Rembrandt style textures, and classical Renaissance composition. Ideal for baroque portraits, classical art prints, museum-style oil paintings, Renaissance-inspired wall art, old masters portraits, and ornate historical artwork.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/baroque-art-generator
```

Or with ClawHub:

```bash
clawhub install baroque-art-generator
```

## Usage

```bash
node baroqueartgenerator.js "a regal queen holding a golden chalice" --token YOUR_TOKEN
```

Generate with a custom size:

```bash
node baroqueartgenerator.js "a contemplative scholar by candlelight" --size portrait --token YOUR_TOKEN
```

Inherit style from a reference image:

```bash
node baroqueartgenerator.js "a warrior in ornate armor" --ref <picture_uuid> --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `<prompt>` | First positional argument — text description of the image | Built-in baroque prompt |
| `--size` | Output size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--token` | Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Size | Dimensions |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

Pass your Neta API token via the `--token` flag on every call:

```bash
node baroqueartgenerator.js "your prompt" --token YOUR_TOKEN
```

You can keep the token in a shell variable and expand it inline:

```bash
node baroqueartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

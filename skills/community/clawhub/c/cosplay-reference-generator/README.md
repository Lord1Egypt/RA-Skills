# Cosplay Reference Generator

Generate cosplay reference sheets and costume design illustrations from text descriptions. Describe any character or outfit and get a full-body anime-style reference sheet — ideal for cosplayers planning builds, commissioning costumes, prepping for anime conventions, organizing photoshoots, populating Etsy listings, or producing cosplay tutorials.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/cosplay-reference-generator
```

Or with ClawHub:

```bash
clawhub install cosplay-reference-generator
```

## Usage

```bash
node cosplayreferencegenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
node cosplayreferencegenerator.js "magical girl with star wand and pastel pink dress" --token YOUR_TOKEN
```

```bash
node cosplayreferencegenerator.js "cyberpunk samurai with neon katana and tactical armor" --size portrait --token YOUR_TOKEN
```

```bash
node cosplayreferencegenerator.js "fantasy elf ranger in forest green leather armor" --size tall --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token` | Neta API token (required) | — |
| `--size` | `portrait`, `landscape`, `square`, or `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Name | Dimensions |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.


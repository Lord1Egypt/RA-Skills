# 90s Anime Art Generator

Generate retro 1990s anime art and OVA-style illustrations from text descriptions. This skill turns a text prompt into a nostalgic Japanese animation–style image — flat cel-shaded colors, hand-drawn line art, analog film grain, soft pastel palettes, expressive eyes, and that unmistakable shoujo/seinen mood from the golden era of anime.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

Use it for retro anime portraits, nostalgic profile pictures, vaporwave anime aesthetics, classic OVA fan art, 90s manga-inspired illustrations, and any retro Japanese animation style art you can describe in words.

## Install

Via the ClawHub CLI:

```bash
npx skills add omactiengartelle/90s-anime-art-generator
```

Or via clawhub:

```bash
clawhub install 90s-anime-art-generator
```

## Usage

```bash
node 90sanimeartgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

A retro anime portrait:

```bash
node 90sanimeartgenerator.js "a young swordsman standing on a cliff at sunset, cape flowing in the wind" --token YOUR_TOKEN
```

A nostalgic city scene:

```bash
node 90sanimeartgenerator.js "neon-lit Tokyo street in the rain, lone schoolgirl with an umbrella" --size landscape --token YOUR_TOKEN
```

Reuse the style of an existing image:

```bash
node 90sanimeartgenerator.js "a mecha pilot in the cockpit" --ref PICTURE_UUID --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token` | Your Neta API token (required) | — |
| `--size` | Output aspect: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Name | Dimensions |
| --- | --- |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.


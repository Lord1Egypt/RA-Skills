# Disposable Camera Photo Generator

Generate authentic disposable camera photos from text descriptions — harsh on-camera flash, grainy 35mm film texture, light leaks, washed colors, and that nostalgic Y2K point-and-shoot snapshot aesthetic. Perfect for Instagram dumps, TikTok carousels, vintage party photos, and lo-fi candid 2000s vibes, all generated from a simple text prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/disposable-camera-photo-generator
```

Or via ClawHub:

```bash
clawhub install disposable-camera-photo-generator
```

## Usage

```bash
node disposablecameraphotogenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Square photo (default)
node disposablecameraphotogenerator.js "two friends laughing at a party, harsh flash" --token YOUR_TOKEN

# Portrait orientation
node disposablecameraphotogenerator.js "person holding birthday cake, red-eye flash" --size portrait --token YOUR_TOKEN

# Landscape with style reference
node disposablecameraphotogenerator.js "beach at sunset, light leak" --size landscape --ref PICTURE_UUID --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--size` | Image dimensions: `square`, `portrait`, `landscape`, `tall` | `square` |
| `--token` | Your Neta API token (required) | — |
| `--ref` | Reference picture UUID for style inheritance | — |

### Sizes

| Size | Dimensions |
|------|-----------|
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


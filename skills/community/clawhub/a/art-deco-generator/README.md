# Art Deco Generator

Generate stunning 1920s-inspired art deco illustrations from text descriptions — Gatsby-style posters, wedding invitations, luxury branding, geometric patterns, sunburst motifs, chevron designs, and ornate vintage glamour aesthetics with gold and black palettes.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/art-deco-generator
```

Or via ClawHub:

```bash
clawhub install art-deco-generator
```

## Usage

```bash
node artdecogenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Default art deco prompt
node artdecogenerator.js "" --token YOUR_TOKEN

# Custom prompt
node artdecogenerator.js "art deco wedding invitation, gold sunburst, black background" --token YOUR_TOKEN

# Landscape poster
node artdecogenerator.js "1920s Gatsby skyline poster" --size landscape --token YOUR_TOKEN

# Style inheritance from a reference image
node artdecogenerator.js "art deco peacock motif" --ref <picture_uuid> --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token` | Neta API token (required) | — |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` |
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


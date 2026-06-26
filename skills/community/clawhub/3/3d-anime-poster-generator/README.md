# 3D Anime Poster Generator

Generate stunning 3D anime posters from text descriptions with volumetric lighting, cinematic depth of field, and dynamic compositions. Perfect for wallpapers, merch designs, print-on-demand art, anime fan posters, cyberpunk-style artwork, and decorative prints.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/3d-anime-poster-generator
```

or

```bash
clawhub install 3d-anime-poster-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Generate a 3D anime poster with the default style:

```bash
node 3danimepostergenerator.js "cyberpunk samurai standing on a neon rooftop at night" --token YOUR_TOKEN
```

Generate a landscape poster:

```bash
node 3danimepostergenerator.js "epic mecha battle in a ruined city, sunset lighting" --size landscape --token YOUR_TOKEN
```

Use a reference image UUID for style inheritance:

```bash
node 3danimepostergenerator.js "warrior princess in enchanted forest" --ref PICTURE_UUID --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Details

| Size | Dimensions |
|------|-----------|
| `square` | 1024 x 1024 |
| `portrait` | 832 x 1216 |
| `landscape` | 1216 x 832 |
| `tall` | 704 x 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

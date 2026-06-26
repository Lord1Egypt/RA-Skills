# Film Photo Generator

Generate authentic analog-style film photographs from text descriptions — complete with 35mm grain, soft light leaks, faded color palettes, and that nostalgic 70s/80s vibe. Perfect for indie creators, film photography enthusiasts, and anyone tired of the polished AI look.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/film-photo-generator
```

Or via ClawHub:

```bash
clawhub install film-photo-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

### Basic example

```bash
node filmphotogenerator.js "young woman laughing in a sunlit kitchen" --token YOUR_TOKEN
```

### Landscape orientation

```bash
node filmphotogenerator.js "empty diner at golden hour" --size landscape --token YOUR_TOKEN
```

### With a reference image for style inheritance

```bash
node filmphotogenerator.js "portrait of a man on a beach" --ref PICTURE_UUID --token YOUR_TOKEN
```

### Default prompt

If you omit the prompt, the skill uses a curated film-look default:

> analog film photograph, 35mm film grain, soft light leaks, faded color palette, muted contrast, nostalgic 1970s 1980s aesthetic, vintage kodak portra film stock, subtle vignette, authentic imperfect photography, shot on film camera, cinematic warm tones

## Options

| Flag      | Description                                                      | Default    |
| --------- | ---------------------------------------------------------------- | ---------- |
| `--token` | Your Neta API token (required)                                   | —          |
| `--size`  | Image orientation: `portrait`, `landscape`, `square`, or `tall`  | `portrait` |
| `--ref`   | Reference image UUID to inherit style from                       | none       |

### Size dimensions

| Size      | Dimensions  |
| --------- | ----------- |
| square    | 1024 × 1024 |
| portrait  | 832 × 1216  |
| landscape | 1216 × 832  |
| tall      | 704 × 1408  |

## Output

Returns a direct image URL.


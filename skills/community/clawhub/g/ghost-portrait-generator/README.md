# Ghost Portrait Generator

Generate haunting ghost portraits and spectral apparition images from text descriptions. Describe the ghost, mood, era, attire, and atmosphere you want, and this skill produces a cinematic, photorealistic ghost portrait — perfect for Halloween content, gothic aesthetic feeds, horror story covers, and the viral ghost portrait trend popularized on social media.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/ghost-portrait-generator
```

Or via ClawHub:

```bash
clawhub install ghost-portrait-generator
```

## Usage

```bash
node ghostportraitgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a default ghost portrait:

```bash
node ghostportraitgenerator.js "a translucent Victorian ghost in a candlelit hallway, torn lace gown, pale glowing skin, eerie fog" --token YOUR_TOKEN
```

Landscape orientation:

```bash
node ghostportraitgenerator.js "spectral figure drifting over a misty graveyard at midnight, full moon, cinematic horror lighting" --size landscape --token YOUR_TOKEN
```

With a reference image UUID for style inheritance:

```bash
node ghostportraitgenerator.js "a shadowy phantom behind a lone traveler, wisps of smoke, gothic horror" --ref 123e4567-e89b-12d3-a456-426614174000 --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| (positional) | Text prompt describing the ghost portrait | built-in haunting prompt |
| `--size` | Image size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--token` | Neta API token | *required* |
| `--ref` | Reference image UUID for style inheritance | none |

### Sizes

- `portrait` — 832×1216
- `landscape` — 1216×832
- `square` — 1024×1024
- `tall` — 704×1408

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.


# Chinese Ink Painting Generator

Generate stunning traditional Chinese ink paintings (shui-mo hua) and sumi-e brushwork art from text descriptions. Create classical shan shui landscapes, bamboo, koi, dragons, plum blossoms, calligraphy art, oriental scrolls, Japanese ink wash, zen minimalist art, and East Asian brush painting illustrations for wallpapers, prints, tea house decor, meditation art, cultural projects, and traditional aesthetic designs — all from a short prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/chinese-ink-painting-generator
```

Or with ClawHub:

```bash
clawhub install chinese-ink-painting-generator
```

## Usage

```bash
node chineseinkpaintinggenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Default landscape shan shui scene
node chineseinkpaintinggenerator.js "misty mountains with a lone fisherman on a bamboo raft" --token YOUR_TOKEN

# Vertical hanging-scroll portrait
node chineseinkpaintinggenerator.js "plum blossoms on a twisted branch, single magpie" --size portrait --token YOUR_TOKEN

# Square composition of koi fish
node chineseinkpaintinggenerator.js "two koi fish swirling in rippling water, sumi-e style" --size square --token YOUR_TOKEN

# Inherit style from a reference image
node chineseinkpaintinggenerator.js "wandering monk crossing a stone bridge" --ref PICTURE_UUID --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--size` | Aspect ratio: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `landscape` |
| `--token` | Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

## Output

Returns a direct image URL.

## Token Setup

This skill requires a Neta API token. Get a free trial token at <https://www.neta.art/open/>.

Pass the token with the `--token` flag every time you invoke the script:

```bash
node chineseinkpaintinggenerator.js "ancient pine tree on a cliff" --token YOUR_TOKEN
```

You can keep your token in a shell variable and expand it at call time:

```bash
node chineseinkpaintinggenerator.js "cranes flying over a lake at dawn" --token "$NETA_TOKEN"
```

The `--token` flag is the only way the script accepts a token.


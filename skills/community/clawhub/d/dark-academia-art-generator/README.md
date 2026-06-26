# Dark Academia Art Generator

Generate moody, scholarly dark academia aesthetic images from text descriptions — candlelit libraries, vintage tweed portraits, old leather books, classical statues, and autumn campus scenes. Perfect for Pinterest boards, Tumblr posts, BookTok content, study aesthetic moodboards, journal covers, study playlist art, cottagecore and gothic academia communities, vintage academic poster designs, and atmospheric backgrounds for writers, students, and aesthetic lovers.

> Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/dark-academia-art-generator
```

Or via ClawHub:

```bash
clawhub install dark-academia-art-generator
```

## Usage

```bash
node darkacademiaartgenerator.js "your text description" --token YOUR_TOKEN
```

### Examples

```bash
# Default portrait of a candlelit library scene
node darkacademiaartgenerator.js "candlelit antique library with leather-bound books and ink quill on oak desk" --token YOUR_TOKEN

# Landscape autumn campus scene
node darkacademiaartgenerator.js "gothic university courtyard in autumn, golden hour, fog, ivy-covered stone arches" --size landscape --token YOUR_TOKEN

# Square portrait of a tweed-clad scholar
node darkacademiaartgenerator.js "portrait of young scholar in vintage tweed jacket reading by candlelight, chiaroscuro lighting" --size square --token YOUR_TOKEN

# Use a reference image for style inheritance
node darkacademiaartgenerator.js "marble bust on stack of leather books, parchment papers, moody lighting" --ref PICTURE_UUID --token YOUR_TOKEN
```

## Options

| Flag      | Description                                              | Default    |
| --------- | -------------------------------------------------------- | ---------- |
| `--size`  | Image size: `portrait`, `landscape`, `square`, `tall`    | `portrait` |
| `--token` | Your Neta API token                                      | required   |
| `--ref`   | Reference image UUID for style inheritance               | none       |

### Sizes

| Name        | Dimensions  |
| ----------- | ----------- |
| `square`    | 1024 × 1024 |
| `portrait`  | 832 × 1216  |
| `landscape` | 1216 × 832  |
| `tall`      | 704 × 1408  |

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.


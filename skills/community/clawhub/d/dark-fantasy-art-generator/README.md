# Dark Fantasy Art Generator

Generate dark fantasy artwork, grimdark illustrations, and gothic horror scenes from text descriptions. Perfect for D&D campaigns, metal album covers, Soulslike game concepts, dark fantasy novel covers, horror art, eldritch creatures, haunted castles, cursed knights, and atmospheric moody worldbuilding imagery — all from a short text prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/dark-fantasy-art-generator
```

Or via ClawHub:

```bash
clawhub install dark-fantasy-art-generator
```

## Usage

```bash
node darkfantasyartgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
node darkfantasyartgenerator.js "a cursed knight kneeling before a shattered altar in a ruined cathedral" --token YOUR_TOKEN

node darkfantasyartgenerator.js "eldritch leviathan rising from a black ocean beneath a blood moon" --size landscape --token YOUR_TOKEN

node darkfantasyartgenerator.js "haunted gothic castle on a jagged cliff, swirling mist, ravens" --size tall --token YOUR_TOKEN
```

### Output

Returns a direct image URL.

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--size` | Image aspect: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--token` | Your Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Size | Dimensions |
|------|------------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

## Token Setup

This skill requires a Neta API token. Pass it via the `--token` flag:

```bash
node darkfantasyartgenerator.js "your prompt" --token YOUR_TOKEN
```

You can also use shell expansion to keep the token out of your command history:

```bash
node darkfantasyartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

Get a free trial token at <https://www.neta.art/open/>.


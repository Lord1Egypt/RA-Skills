# AI Caricature Portrait Generator

Generate hilarious AI caricature portraits with exaggerated features — describe any person, character, or scenario and get a funny caricature, cartoon portrait, or comic likeness back as a direct image URL. Perfect for gifts, social media avatars, party invitations, and personalized art.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/caricature-portrait-generator
```

```bash
clawhub install caricature-portrait-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
# Basic — uses default portrait size
node caricatureportraitgenerator.js "middle-aged professor with wild white hair and oversized glasses, academic caricature style" --token "$NETA_TOKEN"

# Square format
node caricatureportraitgenerator.js "cheerful chef with a giant puffy hat and rosy cheeks, bold comic linework" --token "$NETA_TOKEN" --size square

# Tall format with custom description
node caricatureportraitgenerator.js "rock musician with enormous hair, tiny sunglasses, and a giant guitar" --token "$NETA_TOKEN" --size tall

# With a reference image UUID for style inheritance
node caricatureportraitgenerator.js "friendly librarian with stacked books for a head" --token "$NETA_TOKEN" --ref xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | **(Required)** Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width × Height |
|------|---------------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

## Output

Returns a direct image URL. Save it with `curl` or open it in any browser:

```bash
URL=$(node caricatureportraitgenerator.js "your prompt" --token "$NETA_TOKEN")
curl -o caricature.png "$URL"
```

## Default Prompt

If no prompt argument is given, the script uses:

```
caricature portrait with exaggerated facial features, comically enlarged eyes and expression, bold linework, professional caricature art style, vibrant colors, humorous likeness
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).

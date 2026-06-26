# Food Photography Generator

Generate professional, appetizing food photography images from text descriptions. Built for restaurants, recipe bloggers, cookbook authors, food brands, and Instagram creators who need hero shots, menu photos, recipe card images, cookbook illustrations, blog headers, marketing visuals, gourmet plating photography, dessert close-ups, beverage shots, and culinary editorial content — all rendered with cinematic lighting and styling.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via skills CLI:

```bash
npx skills add blammectrappora/food-photography-generator
```

Via clawhub:

```bash
clawhub install food-photography-generator
```

## Usage

Provide a text description of the dish or scene you want to generate. The script submits the prompt, polls until the image is ready, then prints the resulting image URL to stdout.

```bash
node foodphotographygenerator.js "rustic sourdough bread on wooden cutting board with butter and rosemary, soft window light" --token YOUR_TOKEN
```

Use a different aspect ratio:

```bash
node foodphotographygenerator.js "stack of fluffy pancakes drizzled with maple syrup, blueberries on top" --size portrait --token YOUR_TOKEN
```

Inherit style from a reference image:

```bash
node foodphotographygenerator.js "espresso in a white ceramic cup on marble counter" --ref REFERENCE_PICTURE_UUID --token YOUR_TOKEN
```

Run with no prompt to use the built-in default food photography prompt:

```bash
node foodphotographygenerator.js --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| (positional) | Text prompt describing the food scene to generate | built-in default |
| `--size` | Aspect ratio: `square` (1024×1024), `portrait` (832×1216), `landscape` (1216×832), `tall` (704×1408) | `square` |
| `--token` | Neta API token | required |
| `--ref` | Reference picture UUID for style inheritance | none |

## Output

Returns a direct image URL.

## Token Setup

This skill requires a Neta API token. Get a free trial token at <https://www.neta.art/open/>.

Pass it on every invocation via the `--token` flag:

```bash
node foodphotographygenerator.js "your prompt" --token YOUR_TOKEN
```

You can also expand a shell variable inline:

```bash
node foodphotographygenerator.js "your prompt" --token "$NETA_TOKEN"
```

The `--token` flag is the only way to provide credentials — the script does not read environment variables or local files.


# Floating Product Generator

Generate cinematic floating product shots from text descriptions — levitating product photography, hovering e-commerce images, and dramatic studio-lit commercial shots, all produced from a short text prompt. Ideal for Shopify stores, Amazon listings, dropshipping catalogs, Instagram ads, luxury brand marketing, creator-economy content, and premium product advertising.

> Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/floating-product-generator
```

Or via ClawHub:

```bash
clawhub install floating-product-generator
```

## Usage

```bash
node floatingproductgenerator.js "luxury perfume bottle" --token YOUR_TOKEN
```

More examples:

```bash
# Portrait-orientation floating sneaker shot
node floatingproductgenerator.js "white minimalist sneaker" --size portrait --token YOUR_TOKEN

# Landscape hero image for a smartwatch
node floatingproductgenerator.js "sleek black smartwatch with metallic band" --size landscape --token YOUR_TOKEN

# Square Instagram-ready skincare bottle
node floatingproductgenerator.js "amber glass serum bottle with gold dropper" --size square --token YOUR_TOKEN

# Inherit style from a reference image
node floatingproductgenerator.js "matte black headphones" --ref 00000000-0000-0000-0000-000000000000 --token YOUR_TOKEN
```

## Options

| Flag      | Description                                                            | Default   |
| --------- | ---------------------------------------------------------------------- | --------- |
| `--token` | Neta API token (required)                                              | —         |
| `--size`  | Image size: `portrait`, `landscape`, `square`, `tall`                  | `square`  |
| `--ref`   | Reference image UUID for style inheritance                             | —         |
| `-h`      | Show help                                                              | —         |

### Sizes

| Name        | Dimensions   |
| ----------- | ------------ |
| `square`    | 1024 × 1024  |
| `portrait`  | 832 × 1216   |
| `landscape` | 1216 × 832   |
| `tall`      | 704 × 1408   |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

## How it works

The skill takes your short text description, appends a curated cinematic-product-photography prompt suffix, and sends it to the Neta AI image generation API. It then polls the task endpoint until the image is ready and prints the resulting URL to stdout.


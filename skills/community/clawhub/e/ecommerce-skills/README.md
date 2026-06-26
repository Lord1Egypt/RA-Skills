# Designkit Skills

Designkit is an ecommerce image skill pack for background removal, image restoration, and listing image generation. Use it when you need clean cutouts, sharper product photos, or marketplace-ready hero and detail images from a single product image.

## What It Does

- Removes backgrounds and returns transparent or white-background product images
- Restores blurry or low-quality product photos
- Generates listing-ready product image sets for ecommerce marketplaces

## Who It Is For

- Ecommerce sellers and marketplace operators
- Creative ops and merchandising teams
- Agencies producing product image variations at scale

## Quick Start

1. Get credits and an API key from [Designkit OpenClaw](https://www.designkit.com/openClaw).
2. Set your API key:

```bash
export DESIGNKIT_OPENCLAW_AK="AK"
```

3. Install the skill:

```bash
clawhub install designkit-ecommerce-skills
```

Or install from GitHub:

```bash
npx -y skills add https://github.com/designkit/designkit-ecommerce-skills
```

## Example Prompts

- `Remove the background from this product image and return a transparent result.`
- `Restore this blurry product photo and make it sharper.`
- `Create a full Amazon listing image set from this product photo.`

## Capabilities

### Cutout-Express

Use this when you need a product image with the background removed. It is suitable for transparent-background outputs and clean marketplace-ready product cutouts.

### Clarity-Boost

Use this when the source image is blurry, soft, or low-quality and you want a sharper product photo for ecommerce use.

### Listing-Kit

Use this when you want a multi-image ecommerce set from one product photo. The skill guides the conversation in steps, then returns generation progress and final result image URLs.

## What To Expect

- For background removal and image restoration, the skill returns result image URLs and may render previews in clients that support image display.
- For listing image generation, the skill asks for selling points, style direction, and marketplace settings before generating results.
- When you provide a local image path, the file is uploaded to Designkit/OpenClaw for processing.

## Privacy And Security

- Request logging is off by default: `OPENCLAW_REQUEST_LOG=0`
- If request logging is enabled manually, the skill emits redacted request and response summaries instead of full request bodies or credentials
- Local image inputs are validated as real `JPG`, `JPEG`, `PNG`, `WEBP`, or `GIF` files before upload
- The skill uses only the permissions required to perform the requested task:
  - `network` to call Designkit/OpenClaw APIs
  - `shell` to run the bundled skill entrypoints
  - `filesystem` to read local image inputs when you provide a local path

## Troubleshooting

- If you see an authentication error, confirm that `DESIGNKIT_OPENCLAW_AK` is set correctly and that your credits are active.
- If you see an insufficient credits error, visit [Designkit](https://www.designkit.com/openClaw) to check your balance.
- If a local file is rejected, make sure it is a valid `JPG`, `JPEG`, `PNG`, `WEBP`, or `GIF` image.
- If generation is temporarily unavailable or polling times out, retry later.

## License

MIT-0

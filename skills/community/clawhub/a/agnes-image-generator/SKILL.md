# Agnes Image Generator

A skill for generating and editing images using Agnes Image 2.1 Flash model.

## Capabilities

- Text-to-image generation
- Image-to-image editing (with URL or Data URI input)
- Returns direct image URL for easy access
- Supports custom sizes (default 1024x1024)

## Usage

When the user says "生成图片" or any image generation request, this skill will be triggered automatically if configured as the primary image generation tool.

The skill accepts:
- `prompt` (string, required): Text description of the image to generate
- `image` (string, optional): URL or Data URI of reference image for img2img
- `size` (string, optional): Output size, e.g., "1024x1024" (default)

## Implementation

- Calls Agnes API endpoint: `https://apihub.agnes-ai.com/v1/images/generations`
- Uses Bearer token authentication from `AGNES_API_KEY` environment variable
- Requests `response_format: "url"` for direct accessible links
- For img2img, passes image URL in `extra_body.image` array

## Configuration

Set your Agnes API key:
```bash
export AGNES_API_KEY="your-api-key-here"
```

Or configure in OpenClaw auth profile (if supported).

## Notes

- Model: `agnes-image-2.1-flash`
- Pricing: $0.003 per image (as per Agnes documentation)
- Supports high information density images and composition preservation for img2img.

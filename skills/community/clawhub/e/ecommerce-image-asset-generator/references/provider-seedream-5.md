# Provider Notes — Seedream 5.0 (ARK API)

Use this provider when the user wants a simple, modern image generation path through the ARK API.

## Best for
- Fast text-to-image generation
- Simple image API setup with one API key
- Chinese or mixed-language prompting
- Ecommerce hero images, promotional visuals, cover images, and campaign concepts

## Minimum required info
Ask only for:
- whether `ARK_API_KEY` is already configured;
- whether the user wants text-to-image or image editing;
- output size only if they care.

## Recommended defaults
If the user does not specify otherwise:
- model: `doubao-seedream-5-0-260128`
- size: `2K`
- response format: `url`
- watermark: `false`

## Best flow
1. Plan the asset first.
2. Convert the winning asset brief into a compact commercial prompt.
3. Use defaults unless the user asks for different size or model behavior.
4. Return the generated URL and suggest the next iteration if needed.

## Prompt guidance
Use prompts that specify:
- product or subject
- key selling angle
- composition
- lighting
- background
- style direction
- avoid notes

## Failure handling
If `ARK_API_KEY` is missing or provider execution is unavailable:
- fall back to plan-only mode;
- return the exact Seedream-ready prompt package instead of pretending generation succeeded.

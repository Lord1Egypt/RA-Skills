# Provider Notes — Jimeng 4.0

Use this provider when the user wants Chinese-first prompting, grouped image outputs, multi-image reference input, or high-resolution ecommerce image generation and editing.

## Best for
- Chinese ecommerce prompting
- Multi-image input and composite generation
- Batch asset generation
- PDP, campaign, or grouped marketplace image sets
- High-resolution outputs up to 4K

## Key request model
Jimeng 4.0 works as an async task API.
Typical flow:
1. Submit task
2. Receive task_id
3. Poll result endpoint
4. Return output URLs or decoded images when done

## Best-fit scenarios
- Generate a coordinated asset set instead of a single image
- Edit existing product images with multiple references
- Produce Chinese-friendly ecommerce visuals with better prompt fidelity

## Ask before running
- Is this text-to-image, image edit, or grouped asset generation?
- Does the user want one image or multiple related outputs?
- Should `force_single=true` be used to control latency and cost?
- Are there input image URLs available?
- Is a target ratio / size / width-height specified?

## Important parameter guidance
- `prompt`: keep direct, concrete, commerce-focused
- `image_urls`: use when editing or providing references
- `size` or `width` + `height`: set resolution expectations explicitly when consistency matters
- `scale`: raise if text instruction should dominate more than reference images
- `force_single`: use when latency, price, or consistency matter more than variety

## Failure handling
If auth, signing, provider config, or required image URLs are missing:
- do not pretend generation succeeded;
- fall back to plan-only mode and return the exact prompt + payload draft the user can run later.

## Output note
Because Jimeng is async, always separate:
- submit step
- task status check
- final output delivery

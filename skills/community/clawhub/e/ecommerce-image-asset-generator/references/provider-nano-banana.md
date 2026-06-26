# Provider Notes — Nano Banana Pro / Nano Banana 2

Use this provider when the user wants strong text-to-image or image-to-image generation and has access to a Nano Banana-compatible workflow.

## Best for
- Single-image generation
- Controlled edits to an existing image
- Fast draft → iterate → final workflow
- 1K / 2K / 4K generation requests

## Ask before running
- Which Nano Banana provider/version should be used?
- Is an API key or local execution environment already configured?
- Is this text-to-image or image-to-image?
- What output filename or directory should be used?

## Recommended flow
1. Plan the asset first.
2. Create a provider-ready prompt.
3. If editing, define exactly what must stay fixed.
4. Start at lower resolution for drafts.
5. Move to higher resolution only after direction is approved.

## Prompt guidance
### Generation
Use a concrete, commercial prompt structure:
- subject
- product angle
- composition
- lighting
- background
- text safety / avoid list

### Editing
Use a constrained edit instruction:
- Change ONLY: <requested change>
- Keep identical: subject, crop, lighting, palette, text placement, and overall style unless user requests otherwise.

## Failure handling
If the provider environment, API key, or input image is missing:
- stop execution;
- return the prompt package and tell the user what is missing.

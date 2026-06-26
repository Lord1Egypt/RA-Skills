# Source Notes — Drawing

These notes summarize the external prompt guidance behind this skill.

## OpenAI Image Generation Docs

Official guide:
- https://platform.openai.com/docs/guides/image-generation

Takeaways used here:
- natural-language prompts work well
- detailed instructions improve controllability
- iterative edits work better when the invariant parts are restated clearly

## OpenAI Cookbook

Official cookbook example:
- https://cookbook.openai.com/examples/generate_images_with_gpt_image

Takeaways used here:
- keep scene, style, and constraints explicit
- reuse a stable anchor when you want consistency across generations
- conversational refinement is strong, but only if you do not rewrite the whole prompt aimlessly

## Google Vertex AI Image Prompt Guide

Official guide:
- https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts-design

Takeaways used here:
- image prompts get more reliable when they clearly define subject, context, and style
- plain-language negative constraints help reduce unwanted artifacts
- prompt detail should grow only until it improves control, not until it becomes noisy

## OpenClaw Models Docs

Official guide:
- https://docs.openclaw.ai/concepts/models

Takeaways used here:
- OpenClaw supports a separate image model slot
- the safest skill behavior is to stay model-agnostic by default
- users who want generation inside OpenClaw can configure or inspect the image model without changing the core prompt system

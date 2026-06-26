---
name: gemini-image-cli
description: Generate and edit images with a bundled Gemini native image-generation CLI. Use when the user asks Codex to create images with Gemini, use Gemini image generation through a local bash CLI, run or debug Gemini image curl requests, choose Gemini image models/sizes/aspect ratios, inspect raw image-generation responses, or troubleshoot slow, timed-out, or failed Gemini image requests.
---

# Gemini Image CLI

Use `./scripts/gemini-image.sh` for Gemini native image generation. Prefer this bundled script over writing one-off curl commands.

## Workflow

1. Run `./scripts/gemini-image.sh` with the user's prompt and any requested options.
2. Do not ask which endpoint to use for ordinary requests. The script auto-selects the provider: local Gemini-compatible proxy first, then Google fallback.
3. Keep default settings for ordinary single-image generation: `gemini-3.1-flash-image-preview`, size `512`, aspect `16:9`.
4. Use `gemini-2.5-flash-image` when latency matters more than latest image quality.
5. Use `gemini-3-pro-image-preview` when the user needs stronger instruction following, text rendering, or professional-quality output.
6. Confirm before multi-model batches, many retries, or other repeated calls that may consume extra quota.
7. Read `references/behavior.md` only when explaining provider/security tradeoffs, choosing non-default models, configuring a local Gemini-compatible proxy, troubleshooting slow or failed requests, or modifying the CLI.

## Common Commands

Generate one image:

```bash
./scripts/gemini-image.sh "A cute orange kitten sitting on a soft blanket"
```

Generate with an explicit output path or prefix. The script chooses the final extension from the returned image MIME type:

```bash
./scripts/gemini-image.sh "画两只小猫在打闹" --output ./out/kittens.png
```

Use a faster model:

```bash
./scripts/gemini-image.sh "画两只小猫在打闹" --model gemini-2.5-flash-image
```

Force Google official endpoint:

```bash
./scripts/gemini-image.sh "画两只小猫在打闹" --provider google
```

Force local proxy endpoint:

```bash
./scripts/gemini-image.sh "画两只小猫在打闹" --provider local
```

Use a larger output size:

```bash
./scripts/gemini-image.sh "A cinematic poster of two kittens" --size 1K --aspect 16:9
```

Use an input image for image-guided generation or editing:

```bash
./scripts/gemini-image.sh "Turn this cat photo into a watercolor illustration" --image cat.jpg
```

## Output Contract

The script prints human-readable logs to stderr and machine-readable results to stdout.

Successful stdout lines:

```text
image=<path>
raw_json=<path>
text=<path>
duration_seconds=<seconds>
```

`text=` appears only when `--with-text` is enabled.

## Safety

Do not expose full Google Gemini API keys in conversation or source files. Prefer the local proxy mode when the runtime should not have access to the real Google key.

The script masks keys in curl logs and redacts input-image base64 from printed request bodies.

Do not enable retries automatically for ambiguous multi-request tasks. Retries can submit additional generation requests and may incur additional cost.

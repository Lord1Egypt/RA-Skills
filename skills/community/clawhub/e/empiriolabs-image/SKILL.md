---
name: empiriolabs-image
description: Generate and edit images with EmpirioLabs AI. Use when the user asks to create, draw, illustrate, or render a picture, logo concept, product shot, poster, or social image, or to edit, restyle, or combine existing images from a URL or local file. Runs a bundled Python script that picks a model from the live catalog (or the one you name), waits for the result, and saves the files to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Generate and edit images with EmpirioLabs AI
  openclaw:
    primaryEnv: EMPIRIOLABS_API_KEY
    requires:
      env:
        - EMPIRIOLABS_API_KEY
      anyBins:
        - python3
        - python
    envVars:
      - name: EMPIRIOLABS_API_KEY
        required: true
        description: "EmpirioLabs AI API key (starts with sk-empiriolabs-). Create one at https://platform.empiriolabs.ai/dashboard/api-keys"
    homepage: https://empiriolabs.ai
  hermes:
    tags:
      - image-generation
      - image-editing
      - empiriolabs
    related_skills:
      - empiriolabs-models
      - empiriolabs-video
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI image generation

Create images from a prompt, or edit and combine existing images, with the [EmpirioLabs AI](https://empiriolabs.ai) images API. The bundled script picks a model, waits for the result, and saves the files.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Generate an image

```bash
python3 scripts/image.py "a lighthouse at dawn, soft watercolor" --out ./images/lighthouse.webp
```

The script prints a JSON summary to stdout (progress goes to stderr):

```json
{
  "model": "flux-2-klein-4b",
  "files": ["/home/me/project/images/lighthouse.webp"],
  "urls": ["https://media.empiriolabs.ai/..."]
}
```

Tell the user where the files were saved. The hosted URLs are temporary; the saved files are the lasting copy.

## Edit or combine images

```bash
python3 scripts/image.py "replace the sky with a stormy sunset" --image ./photo.jpg --out ./edited.png
python3 scripts/image.py "place the product from the first image on the table in the second" \
  --image https://example.com/product.png --image https://example.com/table.jpg --out ./scene.png
```

`--image` accepts an https URL or a local file up to 20 MB, and can be repeated. Without `--model`, edits use a featured model that supports image editing.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model, for example `flux-2-klein-4b` or `gpt-image-2`. |
| `--aspect-ratio R` | Aspect ratio such as `1:1`, `16:9`, or `9:16`, where the model supports it. |
| `--size WxH` | Exact size, on models that accept one. |
| `-n N` | Number of images. Each image is billed. |
| `--param key=value` | Any other model parameter, for example `--param seed=42`. Values are read as JSON when possible. |
| `--out PATH` | File or directory to save to (default: current directory). A `.png`, `.jpg`, or `.webp` name also requests that format when the model offers it. |
| `--overwrite` | Replace existing files. By default a numeric suffix is added instead. |
| `--no-download` | Print the hosted URLs without saving files. |
| `--timeout S` | Seconds to wait for a queued job (default 600). |
| `--job-id ID` | Wait for a job that was still running and save its result. |

## Choose a model and check prices

```bash
python3 scripts/image.py --list-models
```

This lists every image model in the live catalog with its price; `*` marks the model used when `--model` is omitted. For a model's full parameter list and limits, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments, `3` the job was still running when `--timeout` ran out. In that case the message includes the `--job-id` command that resumes it.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.
- Every request is billed to the EmpirioLabs AI account at the model's listed price. Confirm with the user before generating many images or using a premium model.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.

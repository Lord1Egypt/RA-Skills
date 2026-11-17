---
name: empiriolabs-3d
description: Generate 3D models with EmpirioLabs AI from a picture of an object or, on models that take text, from a description, wait for the job to finish, and download the file. Use when the user asks to turn an image into a 3D model, mesh, or asset, to make a GLB for a game, a product page, or a 3D print, or to check on a 3D job that is still running. Runs a bundled Python script that picks a model from the live catalog (or the one you name) and saves the file to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Generate 3D models with EmpirioLabs AI
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
      - 3d-generation
      - image-to-3d
      - empiriolabs
    related_skills:
      - empiriolabs-image
      - empiriolabs-models
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI 3D generation

Turn a picture of an object into a 3D model with the [EmpirioLabs AI](https://empiriolabs.ai) 3D API. 3D generation runs as a job: the bundled script submits it, waits until it finishes, and downloads the file.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Make a 3D model from a picture

```bash
python3 scripts/model3d.py --image ./chair.png --out ./models/chair.glb
```

`--image` takes a public https URL or a local file. A picture of one object on a plain background works best. To use a picture made with the `empiriolabs-image` skill, pass the URL from its `urls` output or the saved file.

Most jobs finish in 1 to 5 minutes. The script prints progress to stderr, then a JSON summary:

```json
{
  "model": "MODEL_ID",
  "job_id": "...",
  "files": ["/home/me/project/models/chair.glb"],
  "urls": ["https://media.empiriolabs.ai/..."]
}
```

## Make a 3D model from a description

Some models also take text. Choose one with `--list-models`, then:

```bash
python3 scripts/model3d.py "a low-poly wooden chair" --model MODEL_ID --out ./models/chair.glb
```

## Long jobs

The agent does not have to stay blocked while a model is built:

```bash
python3 scripts/model3d.py --image ./chair.png --no-wait      # prints the job id
python3 scripts/model3d.py --job-id JOB_ID --out ./models/chair.glb   # waits, then downloads
```

If `--timeout` (default 1800 seconds) runs out, the job keeps running. The script exits with code 3 and prints the `--job-id` command that resumes it.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model. |
| `--image URL_OR_FILE` | Picture of the object. |
| `--resolution R` | Detail level, for example `512` or `1024`. Higher values cost more. |
| `--param key=value` | Any other model parameter, for example `--param seed=7`. |
| `--out PATH` | File or directory to save to (default: current directory). On models that offer other formats, the extension selects one. |
| `--no-wait` | Submit the job, print its id, and exit. |
| `--job-id ID` | Wait for an earlier job and download its result. |
| `--no-download` | Print the hosted URL without saving the file. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

3D generation is billed per request, and the price depends on the model and the resolution. Check before a run, and confirm costly runs with the user:

```bash
python3 scripts/model3d.py --list-models
```

`*` marks the model used when `--model` is omitted. For a model's resolutions, file formats, and other parameters, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments, `3` still running when `--timeout` ran out.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.

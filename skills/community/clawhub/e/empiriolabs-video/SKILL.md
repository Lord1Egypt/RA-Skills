---
name: empiriolabs-video
description: Generate short videos with EmpirioLabs AI from a text prompt or a start image, wait for the job to finish, and download the MP4. Use when the user asks to make, animate, or render a video clip, turn a still image into motion, or check on a video job that is still running. Runs a bundled Python script that picks a model from the live catalog (or the one you name) and saves the file to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Generate videos with EmpirioLabs AI
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
      - video-generation
      - image-to-video
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

# EmpirioLabs AI video generation

Make video clips from a prompt or a start image with the [EmpirioLabs AI](https://empiriolabs.ai) video API. Video runs as a job: the bundled script submits it, waits until it finishes, and downloads the MP4.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Make a video

```bash
python3 scripts/video.py "a paper boat drifting down a rainy street at night" --out ./clips/boat.mp4
```

Most jobs finish in 1 to 15 minutes, and high resolutions can take longer. The script prints progress to stderr, then a JSON summary:

```json
{
  "model": "hunyuan-video-1-5",
  "job_id": "...",
  "files": ["/home/me/project/clips/boat.mp4"],
  "urls": ["https://media.empiriolabs.ai/..."]
}
```

## Animate an image

```bash
python3 scripts/video.py "the camera slowly pushes in as leaves fall" \
  --image https://example.com/still.png --out ./clips/leaves.mp4
```

`--image` takes a public https URL. To animate a picture made with the `empiriolabs-image` skill, pass the URL from its `urls` output. Repeat `--image` to pass reference images on models that accept them.

## Long jobs

The agent does not have to stay blocked on a long render:

```bash
python3 scripts/video.py "a city timelapse from day to night" --no-wait   # prints the job id
python3 scripts/video.py --job-id JOB_ID --out ./clips/city.mp4            # waits, then downloads
```

If `--timeout` (default 1800 seconds) runs out, the job keeps running. The script exits with code 3 and prints the `--job-id` command that resumes it.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model, for example `hunyuan-video-1-5` or `kling-3-0-turbo`. |
| `--image URL` | Start image (image-to-video). Repeatable for reference images. |
| `--duration N` | Length in seconds. Supported values depend on the model. |
| `--resolution R` | For example `480p`, `720p`, or `1080p`. Higher resolutions cost more. |
| `--aspect-ratio R` | For example `16:9` or `9:16`. |
| `--audio` / `--no-audio` | Ask for a soundtrack, or a silent clip, on models that support it. |
| `--param key=value` | Any other model parameter, for example `--param seed=7`. |
| `--out PATH` | File or directory to save to (default: current directory). |
| `--no-wait` | Submit the job, print its id, and exit. |
| `--job-id ID` | Wait for an earlier job and download its result. |
| `--no-download` | Print the hosted URL without saving the file. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

Video is billed per second or per clip, and the price depends on the model and resolution. Check before long or high-resolution runs, and confirm costly runs with the user:

```bash
python3 scripts/video.py --list-models
```

`*` marks the model used when `--model` is omitted. For a model's durations, resolutions, and modes, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments, `3` still running when `--timeout` ran out.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.

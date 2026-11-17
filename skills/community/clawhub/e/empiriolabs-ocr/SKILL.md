---
name: empiriolabs-ocr
description: Read PDFs and images with EmpirioLabs AI document OCR and return their text as Markdown, with tables, formulas, and reading order kept. Use when the user asks to extract text from a PDF, a scan, a photo of a page, an invoice, or a paper, to convert a document to Markdown, or to check on a document job that is still running. Runs a bundled Python script that takes an https URL or a local file, picks a model from the live catalog (or the one you name), and prints the Markdown or saves it to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Read documents with EmpirioLabs AI
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
      - ocr
      - pdf-to-markdown
      - empiriolabs
    related_skills:
      - empiriolabs-transcribe
      - empiriolabs-models
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI document OCR

Read a PDF or an image as Markdown with the [EmpirioLabs AI](https://empiriolabs.ai) document OCR API. The bundled script sends the document, waits when it is long, and prints or saves the text.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Read a document

```bash
python3 scripts/ocr.py ./invoice.pdf --out ./invoice.md
python3 scripts/ocr.py https://example.com/paper.pdf --pages 0-2 --out ./paper.md
python3 scripts/ocr.py ./scan.png
```

The source is an https URL or a local file: a PDF, or a PNG, JPEG, WebP, TIFF, BMP, GIF, or AVIF image. Local files up to 20 MB are sent with the request; pass larger files as an https URL. Without `--out`, the Markdown is printed. With `--out`, the script saves it and prints a JSON summary:

```json
{
  "model": "MODEL_ID",
  "job_id": null,
  "file": "/home/me/project/invoice.md",
  "pages": 2,
  "characters": 3180
}
```

Pass `--json` (or an `--out` path ending in `.json`) for the full result, which lists each page with its Markdown and layout.

## Long documents

A long document continues as a job, and the script waits for it. If `--timeout` (default 1800 seconds) runs out, the job keeps running: the script exits with code 3 and prints the command that resumes it.

```bash
python3 scripts/ocr.py --job-id JOB_ID --out ./long.md    # waits, then saves
```

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model. |
| `--type pdf` / `--type image` | Say what the source is when its name has no `.pdf` or image extension. |
| `--pages P` | Pages of a PDF to read, counted from 0: `0-2` is the first three pages, `0,3,6` three single pages. |
| `--table-format F` | Write tables as `markdown` or `html`. |
| `--param key=value` | Any other model parameter, for example `--param extract_header=true`. |
| `--out PATH` | Save the Markdown (or, with `.json`, the full result). |
| `--json` | Print the full result as JSON. |
| `--job-id ID` | Wait for an earlier job and print or save its result. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

OCR is billed per page. Check the price before reading long documents, and confirm costly runs with the user:

```bash
python3 scripts/ocr.py --list-models
```

`*` marks the model used when `--model` is omitted. For a model's parameters and limits, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments, `3` still running when `--timeout` ran out.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.

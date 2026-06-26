---
name: finance-ocr-pro
version: 1.0.7
description: "Use this skill when the user asks to OCR, transcribe, extract, or convert the contents of a scanned PDF, image, or office document into Markdown, HTML, DOCX, or Excel. This workflow sends page images and OCR prompts to a configured OpenAI-compatible VLM endpoint, requires API_KEY, BASE_URL, and VLM_MODEL, bundles HTML report assets locally so no runtime CDN downloads are needed, and produces improved native Word equation output for recognized LaTeX formulas. It is especially valuable for financial documents and other visually complex materials with dense tables, charts, graphs, and multi-part layouts. Prefer durable background jobs for long-running OCR work."
metadata:
  openclaw:
    requires:
      env:
        - API_KEY
        - BASE_URL
        - VLM_MODEL
      anyBins:
        - python3
        - python
    primaryEnv: API_KEY
---

# Finance OCR Pro

Version 1.0.7 update: Word/DOCX output now includes optimized and expanded
LaTeX formula restoration for recognized formulas.

Run this skill only after OCR intent from the user.

This skill is especially helpful for financial reports, annual reports, prospectuses, investor presentations, regulatory filings, research reports, and other documents with complicated structure, charts, graphs, tables, and mixed layout elements.

## Security And Privacy

Before running OCR, make the operating model clear:

- This skill requires three environment variables, all of which must be configured before OCR can run:
  - `API_KEY` (sensitive) -- the API key for authenticating with the VLM endpoint.
  - `BASE_URL` -- the base URL of the OpenAI-compatible VLM endpoint. All page images and OCR prompts are transmitted to this URL.
  - `VLM_MODEL` -- the vision-capable model identifier. Must support image inputs; text-only models will not work.
- OCR sends rendered page images and structured prompts to `BASE_URL`. This is the primary data-transmission path. Users must verify that the endpoint is trusted before processing sensitive documents.
- If the user wants offline or local-only OCR, `BASE_URL` must point to a local VLM service. Do not run this skill against an external endpoint with sensitive documents unless the provider is trusted.
- `scripts/ocr_setup.py` checks dependencies and creates `.env` templates, but it never installs Python packages automatically. Users must review and run dependency installation themselves.
- HTML report generation uses vendored Mermaid and MathJax files from `scripts/vendor/` and does not download frontend assets from a CDN at runtime.
- Local subprocess usage is limited to starting the local OCR worker and invoking document-conversion tools such as LibreOffice or `osascript`. Commands are executed with explicit argument lists rather than shell strings.
- Never commit a populated `.env` file. Use `.env.example` as a template and keep real credentials local.

## Pre-Run Notice

After the user asks for OCR or extraction, give a short notice that includes:

- whether `BASE_URL` is local or remote
- which `VLM_MODEL` will be used
- which execution mode will be used
- where results will be written
- that the skill supports multi-thread OCR and the thread count can be increased when the user's API endpoint, rate limits, and plan support parallel OCR requests
- that page images and prompts will be transmitted to the configured endpoint

Proceed automatically unless the user asks to change those defaults.

## Defaults To Announce

- Running mode: background job by default
- Model: `VLM_MODEL`
- Threads: `1`
  If the user's API endpoint or plan supports safe parallel OCR requests, tell them they can choose a higher thread count.
- Result path:
  - background: `~/.semantic-ocr/jobs/<job_id>/results/`
  - synchronous: `ocr_output/OCR_<filename>/results/`

## Setup

Use the skill-local virtual environment if present.

- macOS/Linux: `.venv/bin/python`
- Windows: `.venv/Scripts/python.exe`
- Fallback: `python3` on macOS/Linux, `python` on Windows

Before running any command, resolve the interpreter and reuse it for the rest
of the session:

- macOS/Linux: `PYTHON="${PYTHON:-$( [ -x .venv/bin/python ] && printf .venv/bin/python || printf python3 )}"`
- Windows: use `.venv\Scripts\python.exe` when present, otherwise `python`

Run:

```bash
$PYTHON scripts/ocr_setup.py --check
```

If setup is incomplete, run:

```bash
$PYTHON scripts/ocr_setup.py
```

## Preferred Execution

By default, start a background worker:

```bash
$PYTHON scripts/ocrctl.py --json start /path/to/document.pdf
```

If the provider supports concurrency and the user wants faster OCR, offer a
higher thread count such as:

```bash
$PYTHON scripts/ocrctl.py --json start -t 4 /path/to/document.pdf
```

Then inspect progress and outputs:

```bash
$PYTHON scripts/ocrctl.py --json status <job_id>
$PYTHON scripts/ocrctl.py --json artifacts <job_id>
$PYTHON scripts/ocrctl.py --json tail <job_id>
```

Use synchronous mode only when the user explicitly wants inline execution:

```bash
$PYTHON scripts/ocr_main.py /path/to/document.pdf
```

## Notes

- Inputs: PDF, common office documents, Apple office formats, and images.
- Outputs: merged Markdown, HTML review report, DOCX with improved native Word
  equation output for recognized LaTeX formulas, and Excel.
- OCR requires `API_KEY`, `BASE_URL`, and `VLM_MODEL` to be configured before running.
- The default page-rendering resolution is `200` DPI.
- The skill supports multi-thread OCR. Keep the default at `1` unless the user's API endpoint, rate limits, and plan support concurrent OCR requests.
- Sensitive document pages are transmitted to the configured endpoint during OCR unless the endpoint is a local service.
- Best suited for financial documents and other visually dense materials with tables, charts, graphs, and complex page structure.
- Office-document conversion may require LibreOffice.
- OCR extraction by the VLM model may be time-consuming; check the status regularly.

# Finance OCR Pro

Finance OCR Pro is a cross-platform OCR skill and local runtime for agent
environments such as Codex, Claude Code, and OpenClaw. The runtime executes on
the user's machine, but the OCR step sends rendered page images and OCR prompts
to a configured OpenAI-compatible Vision-Language Model (VLM) endpoint unless
the user points `BASE_URL` to a trusted local service. HTML report assets are
bundled locally, and the setup flow prints manual dependency instructions
instead of installing packages automatically.

The project reconstructs each page into structured Markdown and then produces a
reviewable HTML report, an editable DOCX file, and an Excel workbook of
extracted tables.

It is especially useful for financial documents and other visually complex
materials where the page contains dense tables, charts, graphs, footnotes,
multi-column layouts, and mixed text/figure structure that simple text
extraction often handles poorly.

This repository is organized as a reusable skill plus a local background-job
runtime. The skill layer tells an agent when and how to run OCR. The runtime
layer lets long OCR jobs continue safely on the user's machine even if the
agent session is interrupted or times out.

## Version Notes

### 1.0.7

Update: LaTeX formula restoration for Word/DOCX output has been optimized and
expanded. DOCX generation now preserves more native Word equation structures,
including improved handling for common functions, continuous identifiers,
subscripts attached to OCR text, n-ary operators such as sums, stretch
delimiters, and cases-style formulas.

## Security And Data Handling

Before using this project, understand the following:

- The OCR pipeline sends rendered page images and structured OCR prompts to
  the configured `BASE_URL`. This is the primary data-transmission path.
- Those page images may contain sensitive content such as financial statements,
  contracts, IDs, signatures, or internal reports.
- The project requires three user-supplied environment variables, all of which
  must be configured before OCR can run:
  - `API_KEY` (sensitive) -- API key for authenticating with the VLM endpoint.
    This is the primary credential. Treat it as a secret.
  - `BASE_URL` -- base URL of the OpenAI-compatible VLM endpoint
    (e.g. `https://api.openai.com/v1`). All page images are transmitted here.
  - `VLM_MODEL` -- vision-capable model identifier (e.g. `gpt-4o`). Must
    support image inputs; text-only models will not work.
- These same environment variables are declared in the platform manifest
  (`skill.yaml`), in `SKILL.md` front matter (`metadata.openclaw.requires.env`),
  and in `agents/openai.yaml` so that agent platforms and security scanners
  can verify the requirements before installation.
- Users should verify the exact endpoint they are sending data to and confirm
  that the provider is appropriate for the document sensitivity level.
- If offline or local-only processing is required, configure `BASE_URL` to
  point to a trusted local VLM service. Do not use an external endpoint for
  sensitive documents unless the provider is trusted.
- `scripts/ocr_setup.py` does not install dependencies automatically. It only
  checks readiness and prints the manual install command for the current
  Python interpreter.
- HTML report generation uses vendored Mermaid and MathJax assets from
  `scripts/vendor/` and performs no runtime CDN fetches.
- Local subprocess usage is restricted to starting the background OCR worker
  and calling known document-conversion helpers such as LibreOffice and
  `osascript`. Commands are passed as explicit argument arrays; the project
  does not use `shell=True`.
- Do not commit a populated `.env` file. Keep secrets local and distribute
  `.env.example` only.

## Agent Activation Policy

This skill is intentionally designed to require explicit OCR intent from the
user because Finance OCR Pro can be slow, costly, and may transmit sensitive
page images to a model endpoint.

- Run the skill when the user asks to OCR, extract, transcribe, 
  or convert the document contents.
- If a file is uploaded for another purpose, such as review, summary,
  translation, comparison, or general analysis, agents should not start OCR
  unless the user clearly requests extraction or the process needs an extraction.

Once the user has requested OCR, the agent should present a short
pre-run notice with the planned defaults and remote-processing implications,
allow the user to change them if desired, and otherwise proceed automatically
without waiting for a second confirmation.

That notice should explicitly state:

- whether `BASE_URL` points to a remote or local endpoint
- which `VLM_MODEL` will be used
- which execution mode will be used
- where results will be written
- that multi-thread OCR is supported and a higher thread count can be offered
  when the user's API endpoint, rate limits, and plan support concurrent OCR
  requests
- that page images and OCR prompts will be sent to the configured endpoint
- extraction by VLM models may be time-consuming

## Project Purpose

The project is intended for scanned or visually complex documents where simple
text extraction is not enough. Its goals are:

- extract readable, structured content from scanned pages
- preserve layout semantics such as headings, lists, tables, and some diagrams
- generate outputs that are useful both for review and downstream editing
- support long-running document jobs in agent-driven environments

It is particularly well suited to:

- annual reports, interim reports, earnings releases, and investor presentations
- prospectuses, offering memoranda, and other transaction documents
- regulatory filings and compliance materials
- research reports
- and other documents with complicated tables, charts, and graphs

Typical input examples include PDFs, office documents, presentations, and image
files. Typical output examples include a merged Markdown transcription, a
side-by-side HTML review report, a styled Word document, and an Excel workbook
of extracted tables.

## What Makes This Project Different

This is not just a batch OCR script. It has three notable characteristics:

1. Semantic extraction
Each page is rendered to an image and sent to a vision-capable model with a
strict OCR prompt. The model is instructed to reconstruct content faithfully in
Markdown, use HTML tables for tabular content, preserve math, and represent
certain diagrams with Mermaid when appropriate.

This is especially valuable in financial and analytical documents where
important meaning lives inside tables, ownership charts, figure captions,
footnotes, and structured page layout rather than plain paragraph text alone.

2. Review-friendly output
The project does not stop at raw text extraction. It also generates:

- a combined Markdown document
- an HTML comparison report that places source page images beside extracted content
- a DOCX document intended for editing and handoff, with native Word equation
  output for recognized LaTeX formulas
- an Excel workbook for extracted tables

3. Agent-safe long-running execution
The repository now includes a durable local job controller so an agent can
start OCR, poll progress, fetch artifacts, and resume/cancel work later without
holding the actual OCR process open.

## High-Level Workflow

At a high level, the OCR flow is:

1. Preflight and configuration check
The project validates Python dependencies and model configuration.

2. Document-to-image conversion
The input document is converted into one image per page.

3. Page-by-page semantic OCR
Each page image is sent to the configured VLM and written to per-page Markdown.

4. Combined document assembly
Page outputs are merged into one Markdown file.

5. Review artifact generation
The project creates:

- an HTML report
- a DOCX document
- an Excel workbook

## Cross-Platform Interpreter Notes

All scripts are intended to run on Windows, macOS, and Linux.

- Use the skill-local virtualenv interpreter when present:
  - macOS/Linux: `.venv/bin/python`
  - Windows: `.venv/Scripts/python.exe`
- If the virtualenv has not been created yet, use `python3` on macOS/Linux or
  `python` on Windows for setup and local testing.

On macOS/Linux, a reliable pattern is:

```bash
PYTHON="${PYTHON:-$( [ -x .venv/bin/python ] && printf .venv/bin/python || printf python3 )}"
```

Then reuse `$PYTHON` for the remaining commands. On Windows, use
`.venv\Scripts\python.exe` when present, otherwise `python`.

## How The Project Works Internally

### 1. Skill Layer

The skill-facing metadata lives in:

- `skill.yaml` -- OpenClaw platform manifest. Declares the skill's identity,
  required permissions (`network`, `filesystem`, `shell`), configuration
  options (`API_KEY` with `secret: true`, `BASE_URL`, `VLM_MODEL`), and entry
  point. This is the file Clawhub reads for registry metadata and what the
  security scanner checks for declared credentials.
- `SKILL.md` -- agent-facing instructions. The YAML front matter declares
  `metadata.openclaw.requires.env` and `metadata.openclaw.requires.anyBins`
  using standard multi-line YAML so the OpenClaw skill loader and ClawHub
  security scanner can gate the skill correctly. The body tells agents when
  and how to run OCR.
- `agents/openai.yaml` -- OpenAI-agent-specific interface metadata.

For distribution, ship `.env.example` as the editable template and keep the
real `.env` local-only.

These files explain when an agent should use the project, what credentials are
required, what data leaves the machine during OCR, and which commands to run.

### 2. OCR Pipeline Layer

The main OCR pipeline lives in the `scripts/` directory.

Core modules:

- `scripts/ocr_main.py`
  The main synchronous pipeline orchestrator.
- `scripts/docs_to_image.py`
  Converts source documents into per-page images.
- `scripts/image_to_md.py`
  Performs batch OCR from images to Markdown.
- `scripts/ai_service_vlm.py`
  Sends text + image requests to an OpenAI-compatible VLM endpoint.
- `scripts/ocr_prompt.py`
  Contains the structured OCR prompt used for page reconstruction.
- `scripts/md_to_html.py`
  Builds the HTML review report.
- `scripts/md_to_docx.py`
  Converts Markdown into a styled Word document, including native Word equation
  output for recognized LaTeX formulas.
- `scripts/md_to_excel.py`
  Extracts HTML tables from Markdown into a formatted Excel workbook.

### 3. Background Job Layer

To support long-running OCR in agent environments, the repository includes a
disk-backed job runtime:

- `scripts/ocrctl.py`
  User-facing controller for starting and managing jobs.
- `scripts/ocr_worker.py`
  Detached worker process that executes one OCR job.
- `scripts/ocr_jobs.py`
  Job manifest, progress tracking, artifact tracking, and event logging.
- `scripts/ocr_runtime.py`
  Shared progress and cancellation interfaces used by the pipeline.

This layer is especially important for OpenClaw-like environments, where a
single agent run may be shorter than a large OCR task.

## Execution Modes

### Synchronous Mode

Used when an agent or user is comfortable waiting for the full job inline.

Example:

```bash
$PYTHON scripts/ocr_main.py /path/to/document.pdf
```

### Durable Background Job Mode

Used when the OCR task may outlive an agent session.

Examples:

```bash
$PYTHON scripts/ocrctl.py --json start /path/to/document.pdf
$PYTHON scripts/ocrctl.py --json status <job_id>
$PYTHON scripts/ocrctl.py --json artifacts <job_id>
$PYTHON scripts/ocrctl.py --json cancel <job_id>
$PYTHON scripts/ocrctl.py --json resume <job_id>
```

In background mode, OCR state is persisted under:

```text
~/.semantic-ocr/jobs/<job_id>/
```

Each job directory contains:

- `manifest.json`
  Immutable job definition and input parameters.
- `progress.json`
  Current status snapshot.
- `events.jsonl`
  Append-only event history.
- `worker.log`
  Console output from the detached worker.
- `results/`
  Generated output files.

On successful completion, intermediate `images/` and `markdowns/` directories
are removed automatically to save disk space. Failed or cancelled jobs keep
their intermediates so they can be resumed.

## Default Run Parameters To Show Before Starting

After the user has explicitly requested OCR or extraction, the hosting agent
should tell the user the defaults it plans to use:

- **Running mode**: background job by default
- **Vision model**: the current configured or user-provided `VLM_MODEL`
- **Results folder**:
  - background mode default: `~/.semantic-ocr/jobs/<job_id>/results/`
  - synchronous mode default: `ocr_output/OCR_<filename>/results/`
- **Threads**: `1` by default
  - The agent should also tell the user that this skill supports multi-thread
    OCR and can use a higher thread count when the API endpoint, rate limits,
    and subscription plan support parallel OCR requests.

If the user does not change these defaults, the agent should proceed
automatically. If the user explicitly requests inline execution, the agent
should switch the running mode and corresponding default results folder.

## Mode Selection By Host

The recommended execution mode depends on the host environment:

- **OpenClaw**
  Use durable background-job mode by default. This is the recommended and
  expected mode for normal OCR requests because long OCR tasks may outlive a
  single OpenClaw agent run.
- **Codex**
  Synchronous mode is acceptable for small jobs. Durable background-job mode is
  preferred for large or long-running documents.
- **Claude Code**
  Synchronous mode is acceptable for small jobs. Durable background-job mode is
  preferred for large or long-running documents.
- **Direct human terminal use**
  Synchronous mode is convenient for quick local tests. Background-job mode is
  better when the user wants to disconnect and check back later.

## Inputs And Outputs

### Supported Inputs

The project is designed to accept:

- PDF
- DOC / DOCX
- PPT / PPTX
- ODT / ODP / RTF / WPS
- KEY / PAGES
- PNG / JPG / JPEG / WEBP / BMP / TIF / TIFF

Some office-format conversions depend on LibreOffice being installed locally.

### Primary Outputs

For a source file named `report.pdf`, the main outputs are:

- `report_combined.md`
- `report.html`
- `report.docx`
- `report.xlsx`

In background mode, the worker records artifact paths in `progress.json`.

## Configuration Requirements

The project expects an OpenAI-compatible VLM endpoint. Three environment
variables must be set before OCR can run:

| Variable    | Required | Sensitive | Purpose |
|-------------|----------|-----------|---------|
| `API_KEY`   | Yes      | Yes       | API key for authenticating with the VLM endpoint (primary credential) |
| `BASE_URL`  | Yes      | No        | Base URL of the VLM endpoint. Page images are transmitted here during OCR |
| `VLM_MODEL` | Yes      | No        | Vision-capable model identifier. Must support image inputs |

These are the same variables declared in `skill.yaml` (platform manifest),
`SKILL.md` front matter (`metadata.openclaw.requires.env`), and
`agents/openai.yaml`.

Important:

- The configured model must be vision-capable. Text-only models will not work
  because the pipeline sends page images to the API.
- `BASE_URL` determines where document images are sent. Review it carefully
  before processing sensitive files.
- A missing or placeholder `.env` means the OCR pipeline is not configured yet.

First-run setup is handled by:

```bash
$PYTHON scripts/ocr_setup.py
```

If Python dependencies are missing, the setup script will print a manual
install command similar to:

```bash
$PYTHON -m pip install -r requirements.txt
```

For redistribution, do not ship a populated `.env` file. Ship
`.env.example` instead and let each user create their own local `.env`.

Example template:

```dotenv
API_KEY=your-api-key-here
BASE_URL=https://your-api-endpoint/v1
VLM_MODEL=your-vision-model-here
```

## Key Review Points

For a project review, the most important aspects are:

### A. Separation of concerns

The repository clearly separates:

- skill instructions for agent use
- OCR pipeline implementation
- job-control/runtime logic for long tasks

### B. Operational resilience

The background-job model is intended to reduce fragility in agent workflows.
An agent starts a job and later reconnects to check status or retrieve results
instead of owning the entire OCR runtime.

### C. Structured outputs

The project emphasizes outputs that can be reviewed and reused downstream,
rather than returning plain text only.

### D. Recoverability

The pipeline now supports resume-aware behavior for existing page markdown and
job-state persistence on disk.

## Known Limitations And Considerations

- OCR quality depends on the chosen VLM, endpoint behavior, and the source
  document quality.
- Page rendering now defaults to 200 DPI to balance OCR quality, speed, and
  disk usage across hosts.
- Very large documents can still take significant time, network transfer, and
  API cost.
- Office document conversion may require local system dependencies.
- HTML report generation depends on the vendored Mermaid and MathJax assets in
  `scripts/vendor/`.
- Cancellation is cooperative, which means it is most responsive between page
  operations rather than in the middle of a single OCR request.

## Release Checklist

- Include `skill.yaml`, `SKILL.md`, `agents/openai.yaml`, `README.md`,
  `requirements.txt`, `scripts/`, `.env.example`, and `LICENSE`.
- Ensure `skill.yaml`, `SKILL.md` front matter, `agents/openai.yaml`, and
  `README.md` all consistently declare the required env vars (`API_KEY`,
  `BASE_URL`, `VLM_MODEL`), the primary credential (`API_KEY`), and the
  data-transmission disclosure.
- Ensure `README.md` and `SKILL.md` clearly state that OCR sends page images
  and prompts to the configured VLM endpoint unless that endpoint is local.
- Exclude developer-local files such as `.env`, `.venv/`, `__pycache__/`,
  `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.DS_Store`,
  `ocr_output/`, `scripts/image_outputs_*/`, and ad-hoc
  test folders.
- Include `scripts/vendor/`, `THIRD_PARTY_NOTICES.md`, and `SECURITY.md` in
  distribution packages.
- Expect PDF/image OCR to work with Python dependencies alone.
- Expect Office-document OCR to require LibreOffice locally.

## Suggested Review Summary

If a reviewer wants a short summary:

Finance OCR Pro is a local, agent-friendly document extraction project that uses a
vision model to convert scanned and visually complex documents into structured
Markdown, reviewable HTML, editable DOCX, and reusable Excel outputs. Its main
engineering feature is the addition of a durable background-job runtime, which
allows agent tools to manage long OCR tasks safely on the user's machine
instead of tying them to one fragile interactive session.

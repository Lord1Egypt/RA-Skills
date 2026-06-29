---
name: doc2md
description: Use when the user wants to convert local PDF, DOCX, or PPTX files into Markdown with the packaged doc2md CLI, especially for batch conversion, recursive folder processing, or Windows and Linux command-line usage.
---

# Doc2md 

## Overview

This skill provides a packaged `doc2md` CLI for converting local PDF, DOCX, and PPTX files into Markdown through the doc2md platform API.

Use this skill when the user needs a ready-to-run command-line workflow instead of writing custom conversion code.

## Bundled Files

- Windows binary: `scripts/doc2md-cli.exe`
- Linux binary: `scripts/doc2md-cli`

Both binaries are statically linked and do not require an extra runtime.

## Prerequisites

- A valid doc2md bearer token
- Network access to the doc2md API service
- Input files in PDF, DOCX, or PPTX format

Configuration can be provided with either:

- Environment variables: `DOC2MD_API_BASE_URL`, `DOC2MD_BEARER_TOKEN`
- Config file: `~/.doc2md/config.json`

Environment variables take precedence over the config file.

## Usage

### Windows PowerShell

```powershell
$env:DOC2MD_BEARER_TOKEN = 'your-jwt'
$env:DOC2MD_API_BASE_URL = 'http://192.168.99.85:5173'

.\scripts\doc2md-cli.exe -output-dir .\converted .\document.pdf
```

### Linux

```bash
export DOC2MD_BEARER_TOKEN='your-jwt'
export DOC2MD_API_BASE_URL='http://192.168.99.85:5173'

./scripts/doc2md-cli -output-dir ./converted ./document.pdf
```

### Common Commands

```bash
# Convert one folder recursively
./scripts/doc2md-cli -output-dir ./converted ./docs/

# Convert multiple inputs in parallel
./scripts/doc2md-cli -output-dir ./converted -concurrency 4 ./doc1.pdf ./doc2.docx ./folder/
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-output-dir` | required | Directory that receives extracted results |
| `-converter` | `mineru` | Backend converter: `mineru` or `marker` |
| `-recursive` | `true` | Scan directories recursively |
| `-keep-zip` | `false` | Keep `result_clean.zip` after extraction |
| `-overwrite` | `true` | Overwrite existing output directories |
| `-concurrency` | `1` | Number of files processed in parallel |
| `-poll-interval` | `5s` | Job polling interval |
| `-job-timeout` | `24h` | Per-file timeout |
| `-http-timeout` | `2m` | Per-request HTTP timeout |

## Output Behavior

- Each input document is written to its own subdirectory under `-output-dir`
- The CLI prints timestamped progress and per-file status to stdout
- `Ctrl+C` cancels remaining work gracefully
- The process exits non-zero when any conversion fails

## Config File Example

```json
{
  "apiBaseUrl": "http://192.168.99.85:5173",
  "bearerToken": "your-jwt"
}
```

Save this file as `~/.doc2md/config.json` when environment variables are not convenient.

## Troubleshooting

- Authentication failure: verify `DOC2MD_BEARER_TOKEN`
- Connection failure: verify `DOC2MD_API_BASE_URL` and service reachability
- Empty output directory: confirm the input file type is supported and the API job completed successfully
- Existing output overwritten unexpectedly: pass a safer output directory or adjust `-overwrite`

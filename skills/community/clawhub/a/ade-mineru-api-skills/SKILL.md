---
name: mineru-cli
description: MinerU document extraction CLI that converts PDFs, images, and web pages into Markdown, HTML, LaTeX, or DOCX via the MinerU API. Supports single/batch extraction, web crawling, async tasks, and piped workflows.
read_when:
  - Extracting text from PDF documents
  - Converting documents to Markdown
  - Crawling web pages to Markdown
  - Batch document processing
  - OCR on scanned documents
  - Converting PDF to HTML, LaTeX, or DOCX
  - Parsing document content
  - Reading PDF files
  - Extracting tables from documents
  - Converting Word documents
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["mineru"]},"install":[{"id":"install-unix","kind":"download","os":["darwin","linux"],"bins":["mineru"],"url":"https://cdn-mineru.openxlab.org.cn/open-api-cli/install.sh","label":"Install mineru (Linux/macOS)"},{"id":"install-windows","kind":"download","os":["win32"],"bins":["mineru"],"url":"https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1","label":"Install mineru (Windows)"}]}}
allowed-tools: Bash(mineru:*)
---

# Document Extraction with mineru

## Installation

### Linux / macOS

```bash
curl -fsSL https://cdn-mineru.openxlab.org.cn/open-api-cli/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex
```

### Verify installation

```bash
mineru version
```

## Authentication

Before using, configure your API token (get one from https://mineru.net):

```bash
mineru auth                    # Interactive token setup
export MINERU_TOKEN="your-token"  # Or set via environment variable
```

Token resolution order: `--token` flag > `MINERU_TOKEN` env > `~/.mineru/config.yaml`.

## Supported input formats

The `extract` command accepts the following input types:

- **PDF** (`.pdf`) — primary use case, supports scanned and digital PDFs
- **Images** (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`,`.bmp`) — use `--ocr` for best results on scanned content
- **DOCX** (`.docx`) — Microsoft Word documents
- **URLs** — remote files are downloaded automatically

The `crawl` command accepts any HTTP/HTTPS URL and extracts web page content.

## Default behavior

- **Table recognition**: ON by default. Tables in documents are extracted and converted to Markdown tables. Use `--no-table` to disable.
- **Formula recognition**: ON by default. Mathematical formulas are extracted as LaTeX. Use `--no-formula` to disable.
- **Language**: defaults to `ch` (Chinese). Use `--language en` for English documents.
- **Model**: auto-selected. Use `--model vlm` for complex layouts, `--model pipeline` for speed.

## Quick start

```bash
mineru extract report.pdf                    # PDF → Markdown to stdout
mineru extract report.pdf -o ./out/          # Save to file
mineru extract report.pdf -f md,docx         # Multiple formats
mineru crawl https://example.com/article     # Web page → Markdown
```

## Core workflow

1. Authenticate: `mineru auth` or set `MINERU_TOKEN`
2. Extract: `mineru extract <file-or-url>` for documents
3. Crawl: `mineru crawl <url>` for web pages
4. Check results: output goes to stdout (default) or `-o` directory

## Commands

### extract — Document extraction

Convert PDFs, images, and other documents to Markdown or other formats.

```bash
mineru extract report.pdf                         # Markdown to stdout
mineru extract report.pdf -f html                 # HTML to stdout
mineru extract report.pdf -o ./out/               # Save to directory
mineru extract report.pdf -o ./out/ -f md,docx    # Multiple formats
mineru extract *.pdf -o ./results/                # Batch extract
mineru extract --list files.txt -o ./results/     # Batch from file list
mineru extract https://example.com/doc.pdf        # Extract from URL
cat doc.pdf | mineru extract --stdin -o ./out/    # From stdin
```

#### extract flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | _(stdout)_ | Output path (file or directory) |
| `--format` | `-f` | `md` | Output formats: `md`, `json`, `html`, `latex`, `docx` (comma-separated) |
| `--model` | | _(auto)_ | Model: `vlm`, `pipeline`, `html` |
| `--ocr` | | `false` | Enable OCR for scanned documents |
| `--no-formula` | | `false` | Disable formula recognition |
| `--no-table` | | `false` | Disable table recognition |
| `--language` | | `ch` | Document language |
| `--pages` | | _(all)_ | Page range, e.g. `1-10,15` |
| `--timeout` | | `300`/`1800` | Timeout in seconds (single/batch) |
| `--list` | | | Read input list from file (one path per line) |
| `--stdin-list` | | `false` | Read input list from stdin |
| `--stdin` | | `false` | Read file content from stdin |
| `--stdin-name` | | `stdin.pdf` | Filename hint for stdin mode |
| `--concurrency` | | `0` | Batch concurrency (0 = server default) |

### crawl — Web page extraction

Fetch web pages and convert to Markdown.

```bash
mineru crawl https://example.com/article              # Markdown to stdout
mineru crawl https://example.com/article -f html      # HTML to stdout
mineru crawl https://example.com/article -o ./out/     # Save to file
mineru crawl url1 url2 -o ./pages/                     # Batch crawl
mineru crawl --list urls.txt -o ./pages/               # Batch from file list
```

#### crawl flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | _(stdout)_ | Output path |
| `--format` | `-f` | `md` | Output formats: `md`, `json`, `html` (comma-separated) |
| `--timeout` | | `300`/`1800` | Timeout in seconds (single/batch) |
| `--list` | | | Read URL list from file (one per line) |
| `--stdin-list` | | `false` | Read URL list from stdin |
| `--concurrency` | | `0` | Batch concurrency |

### auth — Authentication management

```bash
mineru auth              # Interactive token setup
mineru auth --verify     # Verify current token is valid
mineru auth --show       # Show current token source and masked value
```

### status — Async task status

Query the status of a previously submitted extraction task.

```bash
mineru status <task-id>                      # Check status once
mineru status <task-id> --wait               # Wait for completion
mineru status <task-id> --wait -o ./out/     # Wait and download results
mineru status <task-id> --wait --timeout 600 # Custom timeout
```

#### status flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--wait` | | `false` | Wait for task completion |
| `--output` | `-o` | | Download results to directory when done |
| `--timeout` | | `300` | Max wait time in seconds |

### version — Version info

```bash
mineru version    # Show version, commit, build date, Go version, OS/arch
```

## Global flags

These flags apply to all commands:

| Flag | Short | Description |
|------|-------|-------------|
| `--token` | | API token (overrides env and config) |
| `--base-url` | | API base URL (for private deployments) |
| `--verbose` | `-v` | Verbose mode, print HTTP details |

## Output behavior

- **No `-o` flag**: result goes to stdout; status/progress messages go to stderr
- **With `-o` flag**: result saved to file/directory; progress messages on stderr
- **Batch mode**: requires `-o` to specify output directory
- **Binary formats** (`docx`): cannot output to stdout, must use `-o`
- Markdown output includes extracted images saved alongside the `.md` file

## Examples

### Single PDF extraction

```bash
mineru extract report.pdf -o ./output/
# Output: ./output/report.md + ./output/images/
```

### Extract with OCR and specific pages

```bash
mineru extract scanned.pdf --ocr --pages "1-5" -o ./out/
```

### Multi-format output

```bash
mineru extract paper.pdf -f md,html,docx -o ./out/
# Output: ./out/paper.md, ./out/paper.html, ./out/paper.docx
```

### Batch processing from file list

```bash
# files.txt contains one path per line
mineru extract --list files.txt -o ./results/
```

### Extract to LaTeX

```bash
mineru extract paper.pdf -f latex -o ./out/
# Output: ./out/paper.tex
```

### English document with specific language

```bash
mineru extract english-report.pdf --language en -o ./out/
```

### Extract Word document to Markdown

```bash
mineru extract resume.docx -o ./out/
# Output: ./out/resume.md
```

### Pipe workflow

```bash
# Download and extract in one pipeline
curl -sL https://example.com/doc.pdf | mineru extract --stdin --stdin-name doc.pdf
```

### Web crawling

```bash
mineru crawl https://example.com/docs/guide -o ./docs/
```

### Batch crawl with URL list

```bash
echo -e "https://example.com/page1\nhttps://example.com/page2" | mineru crawl --stdin-list -o ./pages/
```

### Use with other tools

```bash
# Extract and pipe to another tool
mineru extract report.pdf | wc -w              # Word count
mineru extract report.pdf | grep "keyword"     # Search content
mineru extract report.pdf -f json | jq '.[]'   # Parse structured output
```

## Agent guidelines

When using this skill on behalf of the user:

- **Always ask for the file path** if the user didn't specify one. Never guess or fabricate a filename.
- **Quote file paths** that contain spaces or special characters with double quotes in commands. Example: `mineru extract "report 01.pdf"`, NOT `mineru extract report 01.pdf`.
- **Don't run commands blindly on errors** — if the user asks "提取失败了怎么办", explain the exit code and troubleshooting steps instead of re-running the command.
- **Installation questions** ("mineru 怎么安装") should be answered with the install instructions, not by running `mineru extract`.
- **DOCX as input is supported** — if the user asks "这个 Word 文档能转 Markdown 吗", use `mineru extract file.docx`.
- **Table extraction** — tables are extracted by default as part of the Markdown output. There is no "tables only" mode; the full document is always extracted.
- For **stdout mode** (no `-o`), only one text format can be output at a time. If the user wants multiple formats, suggest adding `-o`.

### Default output directory

When the user does NOT specify an output path (`-o`), the agent MUST generate a default output directory to prevent file overwrites. Use:

```
~/MinerU-Skill/<name>_<hash>/
```

**Naming rules:**

- `<name>`: derived from the source, then **sanitized** for safe directory names.
  - For URLs: last path segment (e.g. `https://arxiv.org/pdf/2509.22186` → `2509.22186`)
  - For local files: filename without extension (e.g. `report.pdf` → `report`)
  - **Sanitization**: replace spaces and shell-unsafe characters (`space`, `(`, `)`, `[`, `]`, `&`, `'`, `"`, `!`, `#`, `$`, `` ` ``) with `_`. Collapse consecutive `_` into one. Keep alphanumeric, `-`, `_`, `.`, and CJK characters.
- `<hash>`: first 6 characters of the MD5 hash of the **full original source path or URL** (before sanitization). This ensures:
  - Different URLs with similar basenames get unique directories
  - Re-running the same source reuses the same directory (idempotent)

**Examples:**

| Source | `<name>` | Output directory |
|--------|----------|-----------------|
| `https://arxiv.org/pdf/2509.22186` | `2509.22186` | `~/MinerU-Skill/2509.22186_a3f2b1/` |
| `https://arxiv.org/pdf/2509.200` | `2509.200` | `~/MinerU-Skill/2509.200_c7e9d4/` |
| `./report.pdf` | `report` | `~/MinerU-Skill/report_8b1a3f/` |
| `./report 01.pdf` | `report_01` | `~/MinerU-Skill/report_01_f4a1c2/` |
| `./My Doc (final).pdf` | `My_Doc_final` | `~/MinerU-Skill/My_Doc_final_b9e3d7/` |
| `./个人简介.docx` | `个人简介` | `~/MinerU-Skill/个人简介_d2a8f5/` |

**How the agent should generate the hash:**

```bash
echo -n "https://arxiv.org/pdf/2509.22186" | md5sum | cut -c1-6
```

Or on macOS:

```bash
echo -n "https://arxiv.org/pdf/2509.22186" | md5 | cut -c1-6
```

**When the user specifies `-o`**: use the user's path as-is, do NOT override with the default directory.

## Exit codes

| Code | Meaning | Recovery |
|------|---------|----------|
| 0 | Success | — |
| 1 | General API or unknown error | Check network connectivity; retry; use `--verbose` for details |
| 2 | Invalid parameters / usage error | Check command syntax and flag values |
| 3 | Authentication error | Run `mineru auth` to reconfigure token, or check token expiration |
| 4 | File too large or page limit exceeded | Split the file or use `--pages` to extract a subset |
| 5 | Extraction failed | The document may be corrupted or unsupported; try a different `--model` |
| 6 | Timeout | Increase with `--timeout`; large files may need 600+ seconds |
| 7 | Quota exceeded | Check API quota at https://mineru.net; wait or upgrade plan |

## Troubleshooting

- **"no API token found"**: Run `mineru auth` or set `MINERU_TOKEN` env variable
- **Timeout on large files**: Increase with `--timeout 600` (seconds)
- **Batch fails partially**: Check stderr for per-file status; succeeded files are still saved
- **Binary format to stdout**: Use `-o` flag; `docx` cannot stream to stdout
- **Private deployment**: Use `--base-url https://your-server.com/api`
- **Extraction quality is poor**: Try `--model vlm` for complex layouts, or `--ocr` for scanned documents
- **Formula not recognized**: Ensure `--no-formula` is NOT set; try `--model vlm` for better formula support

## Notes

- All status/progress messages go to stderr; only document content goes to stdout
- Batch mode automatically polls the API with exponential backoff
- Token is stored in `~/.mineru/config.yaml` after `mineru auth`
- The CLI wraps the MinerU Open SDK (`github.com/OpenDataLab/mineru-open-sdk`)

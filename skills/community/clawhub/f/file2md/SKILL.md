---
name: file2md
description: Converts PDF, DOCX, XLSX, PPTX, HTML, CSV, and other files to Markdown using the @covoyage/file2md CLI (@covoyage/file2md). Use when the user needs office documents or media turned into Markdown, mentions file2md, or asks to extract readable text from a document. 文档转 Markdown、PDF 转 MD、Word 转 Markdown 时使用。
homepage: https://github.com/covoyage/file2md
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["node"]},"install":[{"id":"npm-global","kind":"npm","package":"@covoyage/file2md","bins":["file2md"],"label":"Install file2md CLI (npm global)"}]}}
---

# file2md

Convert local files to Markdown with the **file2md** CLI from [`@covoyage/file2md`](https://www.npmjs.com/package/@covoyage/file2md). Prefer this over writing one-off conversion scripts.

Requires **Node.js 18+**.

## When to use

- User asks to convert a document to Markdown
- User mentions PDF/DOCX/XLSX/PPTX/HTML → Markdown
- User mentions `file2md` or `@covoyage/file2md`
- Chinese triggers: 文档转 Markdown、PDF 转 MD、Word 转 Markdown、表格转 Markdown

## When not to use

- **URLs / feeds / YouTube / Wikipedia** — not supported by the CLI; use the Node.js library (`convertUri` / `convertUrl`) instead
- **In-browser conversion** — use the library with `convertStream()`, not the CLI
- Do not use Document Intelligence and Content Understanding together

## Install

```bash
npm install -g @covoyage/file2md
file2md --help
```

Without a global install:

```bash
npx @covoyage/file2md --help
```

## Commands

**File path (preferred):**

```bash
file2md /path/to/report.pdf
file2md /path/to/report.docx -o /path/to/report.md
```

**No global install:**

```bash
npx @covoyage/file2md /path/to/report.pdf
```

**Stdin (only when a path is unavailable):**

```bash
cat /path/to/report.pdf | file2md -x pdf
```

Pass `-x` (extension). Add `-m` / `-c` when MIME type or charset is known.

## Agent workflow

1. Check Node.js 18+ is available (`node -v`).
2. Confirm the input file exists and use an absolute path when possible.
3. Run `file2md <path>` or `npx @covoyage/file2md <path>`.
4. On success (exit `0`), read Markdown from stdout, or from `-o` if used.
5. On failure (non-zero exit), read stderr and report the error; do not invent output.

For large outputs, prefer `-o /tmp/out.md` and read the file instead of buffering stdout.

## Supported formats (CLI)

Documents: `.txt`, `.md`, `.json`, `.html`, `.csv`, `.docx`, `.xlsx`, `.xls`, `.pptx`, `.pdf`, `.ipynb`, `.epub`, `.zip`

Email: `.msg`

Media: `.jpg`, `.png`, `.gif`, `.webp`, `.wav`, `.mp3`, `.m4a`, `.mp4`

Optional cloud (file path required, not stdin): Azure Document Intelligence, Azure Content Understanding

## CLI flags

| Flag | Purpose |
|------|---------|
| `-o, --output <path>` | Write Markdown to a file instead of stdout |
| `-x, --extension <ext>` | Hint extension for stdin input |
| `-m, --mime-type <type>` | Hint MIME type for stdin input |
| `-c, --charset <charset>` | Hint charset for stdin input |
| `-p, --use-plugins` | Enable discovered npm plugins |
| `--list-plugins` | List installed plugins |
| `-d, --use-docintel` | Azure Document Intelligence |
| `-e, --endpoint <url>` | Document Intelligence endpoint |
| `--use-cu` | Azure Content Understanding |
| `--cu-endpoint <url>` | Content Understanding endpoint |
| `--cu-analyzer-id <id>` / `--cu-analyzer <id>` | CU analyzer id |
| `--cu-file-types <types>` | CU file types, comma-separated (e.g. `pdf,docx`) |
| `--keep-data-uris` | Keep full `data:` URI images in output |
| `-h, --help` / `-v, --version` | Help / version |

## Environment variables (optional)

| Variable | Purpose |
|----------|---------|
| `FILE2MD_PYTHON` | Python executable for pdfminer / pandas backends |
| `FILE2MD_PDF_FORM_MODULE` | Python module with PDF form-table helpers |
| `EXIFTOOL_PATH` | Path to exiftool (media metadata) |
| `AZURE_API_KEY` | Azure subscription key for DocIntel / CU |
| `DOCUMENT_INTELLIGENCE_ENDPOINT` | Default DocIntel endpoint (used with `-d`) |
| `AZURE_CONTENT_UNDERSTANDING_ENDPOINT` | Default CU endpoint (used with `--use-cu`) |

Optional local tools improve quality but are not required for basic conversion: Python pdfplumber/pdfminer, `pdftotext`, exiftool, ffmpeg.

## Plugins

```bash
file2md --list-plugins
file2md -p /path/to/custom.rtf
```

Plugins are discovered from installed npm packages with a `file2md.plugin` entry in `package.json`.

## Node.js library (URLs and in-process use)

The CLI only handles **local files or stdin**. For URLs, browser uploads, or embedded services:

```typescript
import { File2MD } from "@covoyage/file2md";

const md = new File2MD();
const local = await md.convertLocal("./document.docx");
const fromUrl = await md.convertUri("https://example.com/article");
console.log(local.markdown);
```

## Links

- npm: https://www.npmjs.com/package/@covoyage/file2md
- repo: https://github.com/covoyage/file2md

---
name: anydoc
description: Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown. Use when a task needs the contents of an office document, spreadsheet, presentation, ebook, or PDF you cannot read directly.
license: MIT
metadata:
  author: firecrawl
---

# Convert documents to Markdown

Run the `anydoc` CLI and write Markdown to stdout or a file:

```bash
anydoc <file>              # Markdown to stdout
anydoc <file> -o out.md    # write to a file
anydoc - --format csv < f  # read stdin
```

## First-time install

If `command -v anydoc` fails, install the PATH-first wrapper used on this workstation:

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/anydoc <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

exec bunx @firecrawl/anydoc@latest "$@"
EOF
chmod +x ~/.local/bin/anydoc
```

Requirements and checks:

1. Keep `~/.local/bin` on `PATH` ahead of later package-manager bin dirs.
2. Requires Bun so `bunx` can fetch `@firecrawl/anydoc@latest`.
3. Verify with `command -v anydoc` and `anydoc -V`.
4. Prefer this wrapper over a permanent Bun/npm global install of `@firecrawl/anydoc`.

## Rules

1. Supported inputs: `.doc`, `.docx`, `.docm`, `.odt`, `.rtf`, `.epub`, `.pdf`, `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm`, `.odp`, `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.ods`, `.csv`.
2. The format is detected from the file content. Pass `--format <name>` only when detection cannot work: CSV from stdin, or a missing or wrong extension.
3. Exit codes: 0 success, 1 the document could not be converted, 2 usage error. Failures print one `anydoc: <message>` line to stderr. The CLI never prompts.
4. For a large document, write to a file with `-o` and read the parts you need instead of streaming everything into context.
5. Scanned and image-only PDFs need OCR, which anydoc does not do; they fail as unsupported. The hosted [Firecrawl Parse](https://firecrawl.dev/parse) API handles those.
6. Inside a Node, Python, or Rust codebase, prefer the library over shelling out: `@firecrawl/anydoc` on npm, `firecrawl-anydoc` on PyPI, `anydoc` on crates.io. Each exposes the same `to_markdown` / `toMarkdown` API.

# Doc Weaver

Transform Markdown or outlines into polished Word and PDF documents with built-in templates.

## Quick Start

```bash
python3 scripts/weaver.py --doctor
python3 scripts/weaver.py --input examples/chat-feature-prd.md --template prd --output ChatFeaturePRD.docx
python3 scripts/weaver.py --input examples/sprint-planning-minutes.md --template meeting-minutes --output SprintPlanning.pdf
```

## What It Produces

- `.docx` files with cover pages, heading styles, table of contents fields, styled tables, code blocks, blockquotes, headers, and footers.
- `.pdf` files through the local `pandoc` plus `weasyprint` toolchain.
- Styled Markdown previews when users want to inspect output before generating files.

## Runtime Check

Run this before converting documents:

```bash
python3 scripts/weaver.py --doctor
```

`.docx` output requires `python-docx`. PDF output additionally requires `pandoc` and `weasyprint`. If PDF dependencies are missing, Word generation can still work.

## Verification

Run the release check before publishing:

```bash
python3 -m py_compile scripts/weaver.py scripts/verify.py
python3 scripts/verify.py
```

The verification script renders a preview, generates a sample Word document, and generates a sample PDF when the PDF dependencies are available.

## Templates

```bash
python3 scripts/weaver.py --show-templates
```

Built-in templates include PRD, report, academic paper, manual, contract, proposal, resume, newsletter, meeting minutes, and technical whitepaper.

## Privacy

All conversion work is local. The skill does not send document text to external conversion services.

[![ClawHub](https://img.shields.io/badge/ClawHub-doc-extractor-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: doc-extractor
version: 2.0.0
description: Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure
tags: ["pdf", "docx", "extract", "text", "cli", "documents", "python", "open-source", "agent", "automation", "MIT"]
---

# Document Text Extractor

**Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure.**

> *Keywords: pdf, docx, extract, text, cli, documents, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Getting clean text out of PDFs/DOCX for RAG or search is fiddly. Document Text Extractor solves this: Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure.

**Best for:** RAG builders, researchers, and data engineers.

## Features

- **Extract text from a PDF**
- **Pull DOCX content**
- **Batch a folder**
- **List supported formats**
- **Preserve structure (pages/paragraphs)**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/doc-extractor/main/doc_extractor.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python doc_extractor.py self-test     # prove it works end-to-end
python doc_extractor.py extract --help   # extract subcommand
python doc_extractor.py list-formats --help   # list-formats subcommand
python doc_extractor.py batch --help   # batch subcommand
```

## Use cases

1. Extract text from a PDF
1. Pull DOCX content
1. Batch a folder
1. List supported formats
1. Preserve structure (pages/paragraphs)

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Copy-paste from a viewer | Scriptable batch extraction. |
| One-format tools | PDF + DOCX + TXT in one CLI. |
| Lost structure | Structured output for RAG. |

## FAQ (SEO / AEO)

**Q: Formats?**  
A: PDF, DOCX, TXT (list with list-formats).

**Q: Encoding?**  
A: Auto-detected.

**Q: Structure?**  
A: Page/paragraph boundaries are preserved where available.

**Q: Offline?**  
A: Yes.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test doc-extractor
        run: python doc_extractor.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/doc-extractor)

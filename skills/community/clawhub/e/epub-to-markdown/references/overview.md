# Overview

This skill converts an `.epub` book into an AI-friendly Markdown library.

Most EPUB converters optimize for human reading. This one also optimizes for agent navigation by producing a `META.md` index that summarizes the book structure in one file, so an agent can inspect the table of contents first and open only the needed chapter files.

Generated structure:

```text
{output_dir}/
├── META.md
├── images/
└── chapters/
```

---
name: doc-sync
description: "Context-Aware Doc Generator: Automatically syncs Python docstrings (Google style), Go comments, and README.md based on code changes. Also logs change summaries to a local KB/ChromaDB."
---

# doc-sync

A skill for maintaining strong consistency between code, documentation, and a private knowledge base.

## Workflows

### 1. Synchronize Docstrings and Comments
When you modify function logic or signatures in Python or Go, use this skill to update the relevant comments.

- **Python**: Follows Google Style. Updates `Args`, `Returns`, and `Attributes`.
- **Go**: Follows Standard Go Doc style. Updates exported function/struct comments.

**How to trigger**: "Update docstrings for [file_path]" or "Sync comments in [file_path] after my changes."

### 2. README.md Real-time Update
When adding new exported functions, CLI flags, or API endpoints, this skill ensures the root `README.md` is updated to reflect the new interface.

- Scans for changes in public APIs.
- Updates "Usage" or "API Reference" sections in `README.md`.

**How to trigger**: "Update README.md based on the latest changes in [directory/file]."

### 3. Knowledge Base (KB) Sync
For major code changes, this skill generates a concise summary of "why" the change was made and stores it for future retrieval.

- Uses `scripts/kb_sync.py` to interface with a local ChromaDB (if available) or log to `.gemini/changelog.jsonl`.
- Ensures you can later query the project's history via CLI.

**How to trigger**: "Log this change to the knowledge base" or "Summarize my changes and sync to KB."

## Reference Materials
- [Doc Styles](references/doc_styles.md): Detailed examples of Google and Go documentation styles.

## Usage Guidelines
- Always review suggested docstring changes before applying.
- For README updates, provide the specific section title if possible.
- Ensure `chromadb` is installed if you want vector-based retrieval; otherwise, it defaults to a local JSONL log.

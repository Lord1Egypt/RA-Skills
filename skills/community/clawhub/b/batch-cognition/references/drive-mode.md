# Drive Mode — Batch Cognition for Google Drive Dumps

## When to Use
User says "process drive folder" or references Google Drive content for batch processing.

## Flow

### 1. Navigate
GUI agent opens Google Drive → target folder.
List all files: name, type, last modified, size.

### 2. Quick-Scan (first 500 chars per file)
Classify each file:
- 📋 **ACTIONABLE** — clear task/idea with potential value → process in play/think loop
- 🧩 **PARTIAL** — half-finished, needs context/completion → process with extra inference
- 📚 **REFERENCE** — useful info but not actionable → note and park
- ❓ **UNKNOWN** — needs deeper read (~1000 tokens inference) → "where could value be?"
- 🗑️ **IRRELEVANT** — skip with 1-line reason

### 3. Process
ACTIONABLE + PARTIAL → standard play/think loop (per SKILL.md)
UNKNOWN → quick inference pass: "if we put effort toward this, where's the value?"
REFERENCE → catalog in batch doc for future recall
IRRELEVANT → log reason, move on

### 4. Output
Same batch doc format. Meta-think at end.
Additional section: **Drive Inventory** — full classified file list for future reference.

## Mixed Topics Handling
Drive dumps have mixed topics. Don't try to group or reorder.
Process sequentially but let the THINK phase find connections.
The meta-think at the end catches cross-file patterns.

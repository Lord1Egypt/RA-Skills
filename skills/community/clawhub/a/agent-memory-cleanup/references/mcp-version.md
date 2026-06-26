# MCP Version Guidance

Use this reference when the user wants a tool-based distribution instead of a pure instruction skill.

## Recommended MCP Tools

- `audit_memory_file(path, mode="audit-only")`
  - Reads one memory file and returns classifications, duplicate signals, secret warnings, and size status.
- `propose_memory_cleanup(paths)`
  - Returns a proposed canonical memory document and a diff for each file.
- `apply_memory_cleanup(path, proposed_content, approved=true)`
  - Creates a timestamped backup and writes the approved content.
- `detect_memory_pollution(path)`
  - Returns a compact summary of stale task notes, repeated memories, contradictions, and suspected secrets.
- `estimate_memory_pressure(path)`
  - Returns byte size, approximate token pressure, and recommended cleanup threshold.

## Safety Defaults

- Do not expose a tool that edits files without an explicit approval argument.
- Redact suspected secrets in every response.
- Return diffs and backup paths for every write.
- Restrict file access to user-provided paths or configured roots.
- Keep audit operations read-only and deterministic.

## Implementation Shape

Wrap `scripts/audit_memory.py` rather than reimplementing classification logic.
The MCP server should parse tool arguments, call the audit engine, and return structured JSON.

Do not publish the MCP server until it has tests for:

- audit-only never writes files
- apply-approved creates backups
- suspected secrets are redacted
- project policy files are skipped by default
- clean memory remains mostly unchanged

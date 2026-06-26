---
name: codex-session-image-scrubber
description: Use when a Codex thread or local session is slow because prior turns contain heavy image, screenshot, or base64 payloads. Helps locate the session JSONL, back it up, remove only embedded image blobs, preserve conversation text, and validate the cleaned file.
---

# Codex Session Image Scrubber

## Purpose

Clean oversized Codex session logs by replacing embedded image/base64 payloads with small placeholders while keeping the surrounding conversation, tool calls, and text intact.

Use this when the user says a Codex chat/thread is heavy, slow, bloated, or contains pasted screenshots/images/base64 they want removed from history.

## Workflow

1. Confirm the target thread/session.
   - Prefer a thread id if the user provides one.
   - If they provide a remembered phrase, locate the session with `rg -l "<phrase>" ~/.codex/sessions ~/.codex/session_index.jsonl`.
   - Do not edit the active file until you know which JSONL is the target.

2. Dry-run the scrubber.
   ```bash
   node ~/.codex/skills/codex-session-image-scrubber/scripts/scrub-codex-session-images.mjs --thread-id <thread-id>
   ```
   Or, with an exact file:
   ```bash
   node ~/.codex/skills/codex-session-image-scrubber/scripts/scrub-codex-session-images.mjs --file /path/to/rollout.jsonl
   ```

3. If the dry-run looks right, write the cleaned file.
   ```bash
   node ~/.codex/skills/codex-session-image-scrubber/scripts/scrub-codex-session-images.mjs --thread-id <thread-id> --write
   ```

4. Validate after writing.
   - Confirm size dropped with `ls -lh <file> <backup>`.
   - Confirm the JSONL still parses; the script reports `parseErrors: 0`.
   - Check obvious image payloads are gone:
     ```bash
     rg -n "data:image|iVBORw0KGgo|/9j/4AAQ|UklGR" <file>
     ```
     Exit code `1` with no output is the desired result.

5. Tell the user the before/after size, backup path, and whether validation passed. Suggest reopening the thread so the app reloads the lighter file.

## Safety Rules

- Only remove image payloads, not text that mentions images.
- Keep `<image>` or `</image>` text markers if present; they are small and can preserve conversation structure.
- Always keep a backup outside `~/.codex/sessions`; the script defaults to `~/.codex/session_backups`.
- If multiple session files match a thread id, stop and pick explicitly instead of guessing.
- If the user wants the backup removed later, ask for confirmation before deleting it.

## Script

The deterministic scrubber is at `scripts/scrub-codex-session-images.mjs`.

Useful options:

- `--thread-id <id>`: find a rollout JSONL under `~/.codex/sessions`.
- `--file <path>`: scrub a specific JSONL.
- `--write`: perform the rewrite; without this the script is dry-run only.
- `--backup-dir <path>`: override the backup directory.
- `--sessions-dir <path>`: override the Codex sessions root.
- `--min-bytes <n>`: threshold for suspicious image fields; defaults to `100000`.

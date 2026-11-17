---
name: backup-douyin-chat
description: Safely operate the local Douyin group-chat backup tool to log in by QR code, list conversations, perform full or incremental history backups, export JSON or JSONL, verify completeness, and optionally download encrypted image media. Use when the user asks to back up, export, inspect, verify, update, or recover Douyin/抖音 private-message or group-chat history, including requests such as 备份抖音群聊、导出聊天记录、增量更新聊天、检查备份完整性、下载聊天图片.
---

# Backup Douyin Chat

Operate the hardened local tool through the bundled wrappers. Keep account state and chat data local.

## Locate the tool

Use `scripts/tool.sh` for CLI operations. It resolves `DOUYIN_CHAT_EXPORTER_HOME` first, then a containing repository or the current repository directory. Never copy the browser profile or database into the Skill directory.

Run a read-only environment check first:

```bash
<skill-dir>/scripts/tool.sh doctor
```

If the installation is missing, report the expected path and stop. Do not silently recreate or download a different extractor.

## Choose the workflow

- For a first backup: run `init`, then `login --accept-internal-api-risk`, wait for the user to scan the QR code, and run `list --accept-internal-api-risk`.
- If no exact conversation name is known: list conversations and ask the user to select one. Do not guess between similar names.
- For the first archive of a conversation: run `backup --conversation <exact-name> --accept-internal-api-risk`.
- For later updates: add `--incremental`.
- For a data export: run `export --conversation <exact-name> --format json` or `jsonl`.
- For a readable local chat page: run `export --conversation <exact-name> --format html`.
- After backup/export: run `scripts/verify_backup.py --conversation <exact-name>` and report aggregate results without printing message bodies.

Pass arguments as separate shell arguments and quote conversation names. Expect QR login and long backups to remain running; poll them while keeping the user updated.

## Interpret results correctly

Read `references/interpretation.md` before reporting completeness, message totals, or media coverage.

Require all of the following before calling a full backup complete:

1. The backup command exits successfully.
2. The manifest status is `complete`.
3. The terminal reason is `server_has_more_false`.
4. Exported message IDs are unique.

Distinguish stored protocol records from effective chat messages. Internal audit/sync events are preserved in SQLite for traceability but filtered from JSON exports.

## Handle media

Do not describe CDN URLs as locally backed-up media. For image files:

1. Run `media-backfill --conversation <exact-name> --dry-run` to count candidates without network writes.
2. Install optional dependencies with `<tool-root>/setup_im.sh --media` when needed.
3. Run `media-backfill --conversation <exact-name> --accept-media-download-risk` to download from the existing SQLite metadata without rereading chat history.
4. Regenerate the HTML export after media backfill so local images appear in bubbles.
5. Verify `media_local_path` and local files before claiming media backup success.

Warn that CDN URLs can expire. Never print signed media URLs or decryption keys.

## Safety boundaries

- Work only with conversations visible to the user's own logged-in account.
- Use the dedicated browser profile. Never request, paste, print, export, or transmit cookies.
- Treat conversation names, messages, media, user IDs, SQLite files, and exports as sensitive.
- Keep generated files under the tool's `private/im-data` directory with owner-only permissions.
- Never upload chat data or send it to a model/service unless the user explicitly requests that separate action.
- State that the extractor uses an undocumented Douyin endpoint that can change or trigger platform risk controls.

## Report the outcome

Lead with success, incomplete status, or the exact blocker. Include:

- exact conversation name;
- full or incremental mode;
- effective message count and time range;
- completeness status and terminal reason;
- media downloaded versus metadata-only;
- clickable absolute paths to JSON/HTML exports and the manifest.

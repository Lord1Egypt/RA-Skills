---
name: file-access
description: Read, list, and organize files inside owner-approved folders only, with size caps, an audit log, and a hard ban on deletes, system folders, and credential files.
---

# File Access (Hardened)

## Purpose
Let the agent work with everyday documents — find a file, read it, summarize it, copy it into a work folder — without giving it the run of the whole machine. Everything happens inside folders the owner has named in advance, and every action is written to a log the owner can read later.

## Allowed actions
- List files and folders inside allowlisted folders.
- Read text-based files (documents, notes, spreadsheets exported as text, code) up to the size cap below.
- Copy a file from one allowlisted folder to another allowlisted folder.
- Create new files inside the designated work folder only.
- Rename a file inside the work folder, keeping the old name in the log.
- Report file metadata: name, size, modified date, type.

## Hard limits
- Allowlist only: at most 10 owner-named folders. Anything outside them is invisible to this skill.
- Read cap: 2 MB per file, 20 files per run, 10 MB total read per run.
- Copy cap: 20 MB per file, 5 copies per run.
- New files: only in the work folder, only with extensions from the owner's list (default: .md, .txt, .csv, .json).
- One folder tree at a time; no whole-disk scans.
- Every action is appended to `agent-file-log.md` in the work folder: time, action, path, size, result.

## Run-end log markers
- Every run closes with one final line in `agent-file-log.md`. A later reader — owner or agent — must be able to tell from that line alone whether the run finished or was cut short.
- Finished run, no cap hit: `14:03 run-end COMPLETE — 3 files read, 1 copy made, no cap hit`.
- Run stopped by a cap (20 files per run, 2 MB per file, 10 MB total read, or 5 copies per run): the final log line must say the result is partial, name the cap, and count what was done: `14:03 run-end PARTIAL — INCOMPLETE, stopped by the 20-file cap, 20 of 34 requested files read, follow-up task required for the remaining 14`.
- A partial run is never reported to the owner as finished. The report names the cap and the follow-up still needed, same as the log line.

## Never-do list
- Never delete, move, or overwrite an existing file. Copies and new files only.
- Never open credential stores, key files, password vaults, browser profile folders, or anything named like `*secret*`, `*token*`, `*key*`, `.env`, or `credentials*`.
- Never follow a path that escapes an allowlisted folder (no `..` tricks, no symlinks pointing outside).
- Never read binary installers, disk images, or archives larger than the cap "just to check."
- Never change file permissions, owners, or timestamps.
- Never empty a folder, even an empty-looking one.

## Stop-and-ask triggers
Stop, log the reason, and ask the owner before continuing when:
- The requested file is outside every allowlisted folder.
- A file looks like it contains passwords, keys, or private financial data.
- The same read fails 3 times in a row.
- A copy would overwrite an existing file.
- The owner asks for a delete, a move, or a bulk rename of more than 10 files. This skill does not do those; the owner does them by hand or approves a different tool.

## Worked example
Owner: "Find the draft contract Alex Example sent and copy it to my work folder."

1. Agent lists `/home/user/example/inbox-docs/`, finds `alex-example-contract-draft.txt` (48 KB — under the read cap).
2. Agent reads the first page to confirm it is the right file and says so in one line.
3. Agent copies it to `/home/user/example/work/contract-draft-copy.txt`.
4. Agent logs: `14:02 copy inbox-docs/alex-example-contract-draft.txt -> work/contract-draft-copy.txt (48 KB) OK`.
5. Agent reports: "Copied. Original untouched. Log updated."
6. Agent closes the run in the log: `14:03 run-end COMPLETE — 1 file read, 1 copy made, no cap hit`.

If the file had been in `/home/user/other-folder/`, which is not on the allowlist, the agent would stop and ask instead of reading it.

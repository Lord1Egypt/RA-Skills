# Amber
A small Python 3.11+ additive backup runtime and agent skill for Claude Code and Codex session stores. It copies selected session subpaths, never deletes source data, skips existing destination files and excludes common credential filenames.

## Use
Install the agent skill with `npx skills add AntreasAntoniou/amber-agent-skill`, copy this folder to your agent's skill directory under the name amber, or use its script standalone. The Python runtime has no third-party dependencies; the optional installer uses Node.js and network access.
Create a private JSON file with this structure, replacing the example absolute path:
```json
{"hosts": [{"name": "laptop", "source_root": "/absolute/path/to/source-home"}]}
```
```sh
python3 scripts/backup.py --hosts /absolute/path/hosts.json --destination /absolute/path/private-backup --dry-run
```
Preview writes nothing, including no logs or directories. Remove --dry-run only to perform an authorized backup. Status is JSON on stdout; exit 1 means partial/failure, 2 means invalid configuration.

## Limits and privacy
Local/mounted sources only; no SSH, scheduler, commits, encryption or restore automation. Existing files are preserved, so growing transcripts require a fresh destination snapshot to capture later bytes. This is not a versioned incremental backup or disaster-recovery system. Do not modify sources concurrently. Symlinks are rejected, but this is not a defense against a hostile concurrent filesystem actor.
Transcripts may contain secrets even when auth/token filenames are excluded. Newly created directories use mode 0700 and files 0600; existing permissions are not changed. Keep destination access private; use your own encrypted storage and retention policy. No raw user data or host configuration is distributed.

## Tests
```sh
python3 -m unittest discover -s tests -v
```
Tests create structural fixtures in temporary directories. The runtime is a portable reimplementation of an earlier private shell workflow, not its machine configuration.

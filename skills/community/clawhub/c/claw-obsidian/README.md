# openclaw-obsidian

An [OpenClaw](https://openclaw.ai/) skill for reading, searching, and editing an Obsidian vault directly through its Markdown files. No Obsidian CLI, desktop app, or plugin required. Links and backlinks are derived from the files on demand.

Requires **Python 3.10+ on Linux/macOS**. Use an existing, locally accessible vault; rclone is optional.

## Install

```sh
mkdir -p ~/.openclaw/skills
git clone https://github.com/lanjelin/openclaw-obsidian.git \
  ~/.openclaw/skills/openclaw-obsidian
```

## Configure

Add these values to **`~/.openclaw/.env`** (or your OpenClaw state directory's `.env`):

```dotenv
OBSIDIAN_VAULT_PATH="/home/you/notes/My Vault"
# Optional: a Markdown file with your vault's rules.
OBSIDIAN_VAULT_RULES="/home/you/.config/obsidian-vault-rules.md"
```

Use real absolute paths, not `~` or `$HOME`. Omit `OBSIDIAN_VAULT_RULES` until the file exists. Restart your OpenClaw Gateway after changing its environment.

OpenClaw loads this `.env` file; **the Python helper does not load `.env` itself**. Existing process environment values normally take precedence. See [OpenClaw's environment documentation](https://docs.openclaw.ai/help/environment). Sandboxed agents also need the environment variables, vault, and any rules/hooks made available inside their execution environment; see [sandbox configuration](https://docs.openclaw.ai/tools/skills-config).

| Variable | Purpose |
| --- | --- |
| `OBSIDIAN_VAULT_PATH` | Required path to an existing vault. |
| `OBSIDIAN_VAULT_RULES` | Optional path to a Markdown rules file. |
| `OBSIDIAN_PRE_COMMAND` | Optional trusted shell command before each operation. |
| `OBSIDIAN_POST_COMMAND` | Optional trusted shell command after successful local changes. |
| `OBSIDIAN_HOOK_TIMEOUT` | Timeout per hook in seconds; default `120`. |

## Use

Ask your agent, for example:

- “Find my notes about the garden project.”
- “Create a note in Inbox with these meeting notes.”
- “Show backlinks to Projects/Website.md.”
- “Preview renaming this note and updating its links.”
- “List empty project folders without removing them.”
- “Append this entry, replace this exact passage, or import this local attachment.”
- “Preview moving this project folder or renaming a heading and its incoming anchors.”
- “Help me create a vault rules file.”

Start with [the example rules](examples/vault-rules.md) to specify protected folders, naming, templates, and directory-specific guidance. Rules guide the agent; **Markdown is not a security sandbox**. The helper can enforce supplied `--no-read` and `--read-only` path prefixes, but does not interpret the prose itself.

The agent workflow and helper command examples are in [SKILL.md](SKILL.md). For direct terminal use, supply the environment yourself:

```sh
OBSIDIAN_VAULT_PATH='/home/you/notes/My Vault' \
  python3 ~/.openclaw/skills/openclaw-obsidian/scripts/vault.py status
```

## Optional: sync

The pre/post hooks are tool-agnostic: use rclone, rsync, or your own sync scripts. They can run different commands—for example, a pull before access and a push after changes.

**rsync is one-way, not conflict-aware bidirectional sync.** Pulling and pushing in opposite directions can overwrite concurrent edits; use that approach only with a clearly defined authoritative copy and coordinated writers. The rclone bisync quick start below is one option, not a requirement.

Prefer a local working copy synced to a remote. NFS/WebDAV mounts can work, but their visibility, locking, and rename behavior depend on the mount. **Sync is not backup**: keep independent recoverable backups, and use only one sync owner for the working copy.

### 1. Configure and initialize rclone

Install [rclone](https://rclone.org/install/), run `rclone config`, and configure your remote. Replace the example paths below; both vault directories must exist. Back up both sides before proceeding.

```sh
mkdir -p /home/you/.local/state/obsidian-bisync

# Preview initial reconciliation; review before running without --dry-run.
rclone bisync '/home/you/notes/My Vault' 'notes:My Vault' \
  --workdir /home/you/.local/state/obsidian-bisync --resync --dry-run

# Initialize only after reviewing the preview and backups.
rclone bisync '/home/you/notes/My Vault' 'notes:My Vault' \
  --workdir /home/you/.local/state/obsidian-bisync --resync
```

**During `--resync`, the first path wins differing files by default, even if the other copy is newer.** Routine runs must omit `--resync`. Keep the same path order and work directory, and store that state outside the vault. Review conflicts rather than automatically choosing a winner. Read [bisync's safety guidance](https://rclone.org/bisync/) before use; one-way `rclone sync` is not a substitute for bisync.

### 2. Add a sync hook

Save this as `/home/you/.local/bin/obsidian-bisync`, creating its parent directory if needed. Use your actual paths and rclone executable location:

```sh
#!/bin/sh
set -eu
exec /usr/bin/rclone bisync \
  '/home/you/notes/My Vault' 'notes:My Vault' \
  --workdir /home/you/.local/state/obsidian-bisync
```

Run `chmod 700 /home/you/.local/bin/obsidian-bisync`, then add to your OpenClaw `.env`:

```dotenv
OBSIDIAN_PRE_COMMAND="/home/you/.local/bin/obsidian-bisync"
OBSIDIAN_POST_COMMAND="/home/you/.local/bin/obsidian-bisync"
# Increase for slow syncs if necessary.
OBSIDIAN_HOOK_TIMEOUT=120
```

Hooks execute trusted shell commands with your user's permissions. Keep the wrapper operator-controlled; never build commands from note content. Initialize bisync manually before enabling hooks, and never put `--resync` in the wrapper.

The pre-hook runs even for reads and previews; failure stops the operation. The post-hook runs only after successful local changes. **If it fails, those changes remain saved locally**—inspect sync state before retrying.

## Safety and limits

- Note writes, literal appends, and exact-once replacements require the current note's SHA-256. Moves, deletions, and heading/block-anchor refactors require guarded previews; stale plans must be reviewed again.
- Moves handle files and directories, preserve attachments and empty subfolders, and update recognized incoming and affected outgoing links. Plain ATX heading and caret block-ID refactors update matching anchors. Ambiguous refactors are refused. Deleting a referenced note requires explicit authorization; deletion is permanent, not a move to trash.
- `.obsidian`, `.git`, `.trash`, symlinks, and traversal outside the vault are blocked. No-read exclusions make backlink scans incomplete and block broad move/delete/anchor refactors. Scoped search/link discovery limits source-note reads, not resolution of targets outside that scope.
- The parser handles common wikilinks, embeds, Markdown inline links, and reference definitions outside code/comments—not every Obsidian or plugin syntax, rendered heading, or folder reference.
- Locking coordinates helper invocations, not external editors. Writes are atomic per file where supported; multi-file refactors are **not crash-atomic**. Moves copy before removing originals, so allow space for the source subtree. Keep backups.
- Create authorized missing folders with `mkdir Inbox` (or `mkdir Projects/New/Notes --parents`) through the helper. Use `import-attachment SOURCE DEST` only for an explicitly user-specified local file; it copies bytes without overwriting or executing content. Attachment replacement and automatic downloads are unsupported.
- Directory discovery supports `list --type dirs|all --under DIR`; `--empty` requires `--type dirs` and is discovery only, never cleanup authorization. Literal append/replace use temporary input files outside the vault; see the exact commands in [SKILL.md](SKILL.md).
- Empty-folder removal requires a user request or authorized cleanup. Preview with `rmdir Projects/Empty`, then use `--apply` to remove only that directory. Contents (including hidden files and subdirectories) prevent removal; it is never recursive and uses the same path restrictions and hooks.

## Development

```sh
python3 -m unittest discover -s tests -v
```

The tests and CLI smoke workflows use temporary vaults and cover scoped discovery, guarded edits, binary imports, anchor refactors, folder moves, and hook failures. Local-to-local rclone bisync was also exercised; OpenClaw runtime loading, cloud backends, and NFS/WebDAV mounts were not.

## License

[MIT](LICENSE)

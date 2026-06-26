# Security Model

## Purpose

ForgeObsidianBrain is a CLI tool that enables AI agents to read from and write to local Obsidian vaults (Markdown note files). It provides structured note capture, bidirectional sync with OpenClaw memory folders, and intelligent search capabilities.

## Data Access

### Reads
- `~/.config/obsidian/obsidian.json` — Obsidian app configuration (vault paths)
- `~/.openclaw/workspace/memory/*.md` — OpenClaw memory files for sync
- `~/obsidian-vault/**/*.md` — Markdown notes within the user's vault
- Environment variable: `OBSIDIAN_VAULT` — Optional vault path override

### Writes
- `~/obsidian-vault/Brain/**/*.md` — Captured thoughts, research, conversations
- `~/obsidian-vault/OpenClaw/**/*.md` — Synced memory entries
- `~/.openclaw/workspace/memory/*.md` — Vault entries synced back to memory
- `~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/sync/.sync-state.json` — Sync tracking state

### Network
- **None.** This skill does not make network requests.

## Credentials

### Required Environment Variables
- `OBSIDIAN_VAULT` — Optional. Path to Obsidian vault. If unset, auto-discovery is attempted.
- `HOME` — Standard system variable for user home directory.

This skill does not read browser cookies, SSH keys, wallet files, shell history, unrelated `.env` files, or unrelated user documents.

## Execution

### Local Binaries/Tools Used
- `node` — Node.js runtime (JavaScript execution)
- `grep` — Text search (case-insensitive content search)
- Standard Node.js built-ins: `fs`, `path`, `crypto`, `os`, `child_process`

### External Services
- **None.** No external APIs or services are contacted.

### Shell Command Execution
- Uses `child_process.execSync` **only** for `grep` text search operations.
- No arbitrary shell commands are executed from user input.
- No remote code is downloaded or executed.

### Code Safety
- All JavaScript is plain source code (no obfuscation, no minification).
- No `eval()` or dynamic code execution.
- No `Function()` constructor usage.

### Persistence
- Does not install persistence mechanisms.
- Does not modify startup scripts, shell profiles, or system configuration.

### Exfiltration
- Does not exfiltrate local files.
- Does not upload data to remote servers.
- Sync is strictly local between vault and memory folders.

## User Consent

Destructive actions require explicit confirmation:
- `delete` command requires confirmation
- `create` with `--overwrite` flag must be explicitly set

Non-destructive actions (read, search, list) do not require confirmation.

## Scanner Context

### Potential False Positives

The following legitimate patterns may trigger security scanners:

1. **`child_process.execSync`** — Used only for `grep` text search:
   ```javascript
   execSync(`grep -r -l -i ${JSON.stringify(query)} ...`)
   ```
   This is not arbitrary command execution. The query is strictly JSON-stringified to prevent injection.

2. **`new RegExp`** — Used for user-provided regex search:
   ```javascript
   new RegExp(pattern, flags)
   ```
   This is the standard JavaScript RegExp constructor for pattern matching, not code execution.

3. **`fs.readFileSync`** / **`fs.writeFileSync`** — Used for reading/writing Markdown notes to the user's vault. This is the core functionality of the skill.

4. **Documented in SKILL.md** — References to "red team", "prompt injection", or "security testing" in documentation are for defensive detection and explanation only. They describe what the skill protects against, not instructions to perform harmful actions.

### What This Skill Does NOT Do

- Does not access credentials, tokens, or secrets
- Does not access browser data, SSH keys, or sensitive configuration
- Does not make network requests or API calls
- Does not download or execute remote code
- Does not use obfuscation, encoding, or hiding techniques
- Does not use `curl | bash`, `wget | sh`, or similar remote execution patterns
- Does not modify system configuration or install persistence
- Does not exfiltrate or upload data

## Verification

All source code is readable plain JavaScript. Review:
- `scripts/brain.js` — Main CLI entry point
- `scripts/note/crud.js` — Note CRUD operations
- `scripts/search/search.js` — Fuzzy/regex search algorithms
- `scripts/sync/*.js` — Bidirectional sync logic
- `scripts/vault/*.js` — Vault discovery and config

## Reporting Issues

If the scanner continues to flag this skill after review, the false positive should be reported to ClawHub maintainers with reference to this SECURITY.md file.

# Security Analysis — Avenger Initiative

**Verdict: Safe. No malicious code. All operations are local file backup and Git push to the user's own private repository.**

---

## Script-by-Script Analysis

### `scripts/backup.sh`

**Purpose:** Backs up OpenClaw files to the user's own private GitHub vault.

**Operations:**
1. Reads `~/.openclaw/credentials/avenger.key` — user's own encryption key (they created it)
2. Reads `~/.openclaw/credentials/avenger-config.json` — vault repo URL (user configured this)
3. Runs `gh auth token` — gets GitHub token from GitHub CLI (already authenticated on user's system)
4. Runs `git clone <user's-own-vault-repo>` — clones user's own repo
5. Copies `.md` files from `~/.openclaw/workspace/` — identity/memory files, no API keys
6. Runs `openssl enc -aes-256-cbc` on `openclaw.json` only — standard encryption, user's own key
7. Runs `git add`, `git commit`, `git push` — pushes to user's own repo
8. Deletes temp clone directory

**No:** external servers, third-party uploads, telemetry, or data exfiltration.

---

### `scripts/restore.sh`

**Purpose:** Restores OpenClaw files from the user's own private GitHub vault.

**Operations:**
1. Reads `~/.openclaw/credentials/avenger.key` — user's own key
2. Reads `~/.openclaw/credentials/avenger-config.json` — user's own vault URL
3. Runs `git clone <user's-own-vault-repo>`
4. Runs `openssl enc -d` — decrypts with user's own key
5. Copies files back to `~/.openclaw/`
6. Asks for user confirmation before overwriting

**No:** external servers, third-party access, or silent operations.

---

### `scripts/setup.sh`

**Purpose:** First-time configuration. Prompts user for their vault repo and encryption key.

**Operations:**
1. Runs `gh auth status` — verifies GitHub CLI is authenticated (standard check)
2. Runs `gh repo view <url>` — verifies the user's repo exists and is accessible
3. Generates or accepts an encryption key with `openssl rand -hex 32`
4. Saves key to `~/.openclaw/credentials/avenger.key` — user's own machine only
5. Saves vault URL to `~/.openclaw/credentials/avenger-config.json`

**No:** key transmission to servers, account creation, or external communications.

---

## Why Scanners Sometimes Flag Backup Scripts

| Pattern | Why It's Flagged | Actual Use |
|---------|-----------------|-----------|
| `openssl enc` | Heuristic: encryption = suspicious | Encrypts user's own config file with their own key |
| `git push` | Heuristic: data exfiltration | Pushes to user's own private GitHub repo |
| `credentials/` path reads | Heuristic: credential theft | Reads user's own locally-stored key they created |
| Shell scripts with `chmod +x` | Heuristic: privilege escalation | Makes backup.sh executable (standard install) |
| `openssl rand` | Heuristic: crypto key generation | Generates encryption key for user's own backup |

All flagged patterns are **standard backup tool operations**. The same patterns appear in tools like `restic`, `duplicati`, `rclone`, and `borgbackup`.

---

## Data Privacy

| Data Type | What Happens |
|-----------|-------------|
| `openclaw.json` (API keys) | AES-256 encrypted before leaving disk. Only pushed to user's own private GitHub repo. |
| Memory logs (`.md` files) | Plaintext. Only pushed to user's own private GitHub repo. |
| Encryption key | Never leaves the user's machine. Stored in `~/.openclaw/credentials/avenger.key`. |
| GitHub token | Used via `gh auth token` (GitHub CLI). Never stored by this skill. |

**This skill has zero access to:** browser data, passwords, cookies, other applications, or system files outside `~/.openclaw/`.

---

## Threat Model

See `references/security.md` for full threat model documentation including key rotation procedures.

---

## Reporting Security Issues

Please report security concerns at:
https://github.com/ProSkillsMD/avenger-initiative/security/advisories/new

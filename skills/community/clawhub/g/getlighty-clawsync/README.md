# 🦞 ClawSync

**Portable identity vault for OpenClaw. Your AI agent follows you everywhere.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-skill-orange.svg)](SKILL.md)

ClawSync is an open-source OpenClaw skill that syncs your agent's knowledge, memory, and system packages across all your machines — like iCloud, but for AI agents.

## The idea

You have a work laptop, a home machine, maybe a server. Each runs OpenClaw. You want them to share your knowledge but have their own personality. ClawSync makes that work:

- **Knowledge is shared** — USER.md, MEMORY.md, projects, package lists
- **Soul is local** — each instance keeps its own SOUL.md and IDENTITY.md
- **Sync is invisible** — changes auto-detect, auto-commit, auto-push
- **History is versioned** — every change is a git commit, rollback anytime
- **Storage is your choice** — Google Drive, Dropbox, Git, FTP, S3, or our managed cloud

## Quick start

```bash
# Install the skill
clawdhub install clawsync

# Initialize (scans packages, generates keypair, captures knowledge)
clawsync init

# Pick storage — managed cloud (50 MB free):
clawsync provider setup cloud

# Or bring your own:
clawsync provider setup gdrive    # Google Drive
clawsync provider setup dropbox   # Dropbox
clawsync provider setup git       # Any git repo
clawsync provider setup ftp       # FTP/SFTP
clawsync provider setup s3        # S3-compatible
clawsync provider setup local     # USB/NAS

# Start auto-sync
clawsync sync start
```

### On a new machine

```bash
# Install OpenClaw + skill
npm install -g openclaw
clawdhub install clawsync

# Connect to your vault
clawsync init
clawsync provider setup cloud  # same credentials

# Pull everything
clawsync migrate pull
# → Restores knowledge, shows package diff, offers to install missing
```

## How sync works

ClawSync works like a combination of **iCloud** and **Git**:

1. **File watcher** detects changes in your vault (real-time via `fswatch`, or polling)
2. **Auto-commit** creates a local git commit with what changed
3. **Auto-push** sends to your storage provider
4. Every push is **signed** with your machine's Ed25519 private key
5. On pull, conflicts are shown as diffs — you choose what wins

```
~/.clawsync/
├── config.yaml              # Vault configuration
├── requirements.yaml        # System packages (brew/apt/npm/pip)
├── manifest.json            # What's in the vault + checksums
├── identity/
│   ├── USER.md              # Shared — who you are
│   └── instances.yaml       # All connected machines
├── knowledge/
│   ├── MEMORY.md            # Shared — long-term memory
│   └── projects/            # Shared — project context
├── local/                   # ⚠ NOT synced
│   ├── SOUL.md              # This machine's personality
│   └── IDENTITY.md          # This machine's identity
└── keys/
    ├── clawsync_ed25519     # Private key (never leaves machine)
    └── clawsync_ed25519.pub # Public key (registered with provider)
```

## Package tracking

ClawSync scans and tracks installed packages across:

| Manager | macOS | Linux |
|---------|-------|-------|
| Homebrew | ✓ | ✓ |
| apt | — | ✓ |
| snap | — | ✓ |
| flatpak | — | ✓ |
| npm (global) | ✓ | ✓ |
| pip (global) | ✓ | ✓ |

When migrating, it shows what's missing and generates install commands for the target OS.

## ClawSync Cloud

The skill is 100% free and open source (MIT). **ClawSync Cloud** is the optional managed storage for people who don't want to configure their own:

| Usage | Cost |
|-------|------|
| First 50 MB | **Free** |
| After that | $0.005/MB/month |
| Per-instance fee | None |
| Bandwidth | Unlimited |

Most single-user vaults are 10-30 MB — comfortably free. A power user at 200 MB pays ~$0.75/month.

## Commands

| Command | What it does |
|---------|-------------|
| `clawsync init` | Initialize vault, generate keypair, scan packages |
| `clawsync provider setup <n>` | Configure storage provider |
| `clawsync provider list` | Show available providers |
| `clawsync sync start` | Start auto-sync daemon |
| `clawsync sync stop` | Stop auto-sync |
| `clawsync sync push` | Force push now |
| `clawsync sync pull` | Force pull now |
| `clawsync log` | Show vault commit history |
| `clawsync diff` | Show pending changes |
| `clawsync rollback` | Revert to previous state |
| `clawsync packages scan` | Scan installed packages |
| `clawsync packages diff` | Compare local vs vault |
| `clawsync packages install` | Install missing from vault |
| `clawsync migrate pull` | Full migration wizard |
| `clawsync migrate push-identity` | Push SOUL.md to vault (opt-in) |
| `clawsync key show` | Show public key |
| `clawsync key rotate` | Generate new keypair |
| `clawsync status` | Full vault status |

## Security

- **Ed25519 keypair** per machine — private key never leaves the device (stored with 600 permissions)
- **Credentials in system keychain** — macOS Keychain or libsecret on Linux, never plaintext
- **Signed pushes** — every sync is signed with your private key
- **SOUL.md and IDENTITY.md never auto-sync** — explicit opt-in only
- **Packages shown before installing** — never auto-executed
- **Full audit trail** — every change is a git commit

## Repo structure

```
clawsync/
├── SKILL.md               # OpenClaw skill definition
├── clawsync.sh            # Main CLI entry point
├── track-packages.sh       # Package scanner
├── migrate.sh              # Migration wizard
├── src/
│   ├── sync-engine.sh      # iCloud-like auto-sync + history
│   ├── keypair.sh          # Ed25519 key management
│   └── provider.sh         # Provider manager
├── providers/
│   ├── cloud.sh            # ClawSync Cloud (managed)
│   ├── gdrive.sh           # Google Drive (via rclone)
│   ├── dropbox.sh          # Dropbox (via rclone)
│   ├── ftp.sh              # FTP/SFTP (via rsync+ssh)
│   ├── git.sh              # Any Git remote
│   ├── s3.sh               # S3-compatible (via rclone)
│   ├── webdav.sh           # WebDAV (via rclone)
│   └── local.sh            # Local directory
├── web/
│   └── index.html          # Landing page
├── LICENSE                  # MIT
└── README.md
```

## Contributing

PRs welcome. The codebase is intentionally all bash — no build step, no dependencies beyond standard Unix tools + rclone for cloud storage. This runs on the same machines OpenClaw runs on.

## License

MIT — do whatever you want with it.

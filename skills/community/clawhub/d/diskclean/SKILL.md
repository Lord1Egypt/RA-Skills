---
name: diskclean
description: "AI-assisted disk space scanner and cleaner. Finds reclaimable space (node_modules, build caches, package caches, downloads, Docker, Xcode, logs) and intelligently cleans safe items with strict guardrails."
metadata:
  {
    "openclaw": {
      "emoji": "🧹",
      "requires": { "bins": ["python3"] },
      "os": ["mac", "linux"]
    }
  }
---

# Disk Cleaner - AI-Assisted Disk Space Management

You have access to `diskclean.sh`, a disk scanning and cleaning tool. Install it by copying `diskclean.sh` to a location on your PATH, or run it directly from this skill's directory.

## Setup

```bash
# Make executable (if not already)
chmod +x diskclean.sh

# Optional: symlink to PATH
ln -sf "$(pwd)/diskclean.sh" /usr/local/bin/diskclean
```

## Commands

```bash
# Full scan:returns JSON with all reclaimable items
./diskclean.sh scan

# Preview safe-tier auto-deletions (dry run, default)
./diskclean.sh clean --dry

# Execute safe-tier deletions
./diskclean.sh clean --confirm

# Show last scan results
./diskclean.sh report

# Show scan history over time
./diskclean.sh history
```

## How to Use This Skill

### When the user asks to scan or clean disk space:

1. **Run a scan first**: Always start with `diskclean.sh scan`
2. **Summarize findings conversationally**: Group items by category, show top offenders by size, report total reclaimable space
3. **Explain the tiers clearly**:
   - **Safe tier** (auto-deletable): Items matching a strict whitelist AND older than the age gate (7-14 days). These are regenerable artifacts like `node_modules`, `__pycache__`, build caches, package manager caches.
   - **Suggest tier** (needs approval): Everything else:Docker, downloads, venvs, trash. Present these as recommendations and ask the user what they want to do.
4. **For safe-tier cleanup**: Run `diskclean.sh clean --dry` first to show what would be deleted, then `diskclean.sh clean --confirm` only after user approves
5. **For suggest-tier items**: Present them individually or grouped by category. If the user approves specific items, delete them manually with `rm -rf` (after confirming the path is under $HOME)

### Presentation Format

When presenting scan results, use this structure:

```
## Disk Scan Results

**Total reclaimable: X.X GB**
- Safe tier (auto-cleanable): X.X GB
- Needs your review: X.X GB

### Safe to Auto-Clean
| Category | Size | Age | Path |
|----------|------|-----|------|
| ... | ... | ... | ... |

### Needs Your Review
| Category | Size | Age | Path |
|----------|------|-----|------|
| ... | ... | ... | ... |
```

### Safety Rules

- **Never delete anything outside $HOME**
- **Never delete .git directories**
- **Never delete source code, documents, photos, or config files**
- **Never run `clean --confirm` without showing the user `clean --dry` output first**
- **Never delete suggest-tier items without explicit user approval per item or category**
- **Always verify a path exists before attempting deletion**

## How It Works

### Tiered Safety Model

**Safe tier** = whitelisted category + age gate met. Auto-deletable with `--confirm`.

**Suggest tier** = everything else. Requires explicit user approval.

### Categories Scanned

| Category | What | Safe Tier | Age Gate |
|----------|------|-----------|----------|
| node_modules | Node.js dependencies (with package.json sibling) | Yes | 7 days |
| python_cache | `__pycache__`, `.pytest_cache` | Yes | 7 days |
| python_venv | `.venv/`, `venv/` | No |:|
| build_output | `build/`, `dist/`, `.next/`, `target/` | Yes | 7 days |
| go_cache | Go module + build cache | Yes | 14 days |
| homebrew_cache | Homebrew download cache | Yes | 14 days |
| npm_yarn_pnpm_cache | npm/yarn/pnpm caches | Yes | 14 days |
| pip_cache | pip download cache | Yes | 14 days |
| xcode_derived | Xcode DerivedData | Yes | 7 days |
| docker | Docker images, volumes, build cache | No |:|
| large_download | Files >100MB in Downloads | No |:|
| installer_archive | .dmg/.pkg/.zip/.iso in Downloads | No |:|
| logs | macOS logs (>50MB) | Yes | 30 days |
| crash_reports | Diagnostic reports (>10MB) | Yes | 30 days |
| ds_store | .DS_Store files | Yes | 0 days |
| trash | ~/.Trash contents | No |:|

### Guardrails

- Only scans under `$HOME` (plus `/tmp` user files)
- `node_modules` only deleted if a `package.json` exists alongside (proof it's regenerable)
- Dry-run is the default:must pass `--confirm` to actually delete
- Every deletion is logged to `~/.openclaw/diskclean/deletion-log.jsonl`
- All scan reports stored in `~/.openclaw/diskclean/scans/`

### Data Storage

- Scan reports: `~/.openclaw/diskclean/scans/scan-YYYYMMDD-HHMMSS.json`
- Latest scan: `~/.openclaw/diskclean/latest-scan.json`
- Deletion log: `~/.openclaw/diskclean/deletion-log.jsonl`

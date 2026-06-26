# Antigravity Bridge — Setup Guide

> **Goal:** Sync `.md` files from your Antigravity IDE projects into the OpenClaw workspace, where they're natively indexed for `memory_search`.

---

## Prerequisites

### 1. rsync

Usually pre-installed on macOS and Linux.

```bash
rsync --version
# rsync  version 2.6.9  protocol version 29
```

If missing: `brew install rsync` (macOS) or `sudo apt install rsync`

### 2. yq (YAML parser — required)

```bash
yq --version
# yq (https://github.com/mikefarah/yq/) version v4.x
```

If missing:

```bash
# macOS
brew install yq

# Ubuntu/Debian
sudo apt install yq

# Ubuntu snap
snap install yq

# Manual (any OS)
# https://github.com/mikefarah/yq/releases
```

> **Note:** There are two `yq` tools. This skill requires the Go-based yq by Mike Farah (`github.com/mikefarah/yq`), not the Python version. `brew install yq` installs the correct one.

---

## Step 1: Copy the config template

```bash
cp ~/.openclaw/workspace/skills/antigravity-bridge/config-template.yaml \
   ~/.openclaw/workspace/antigravity-bridge.yaml
```

---

## Step 2: Edit the config

Open `~/.openclaw/workspace/antigravity-bridge.yaml` in your editor and configure it for your actual projects.

**Minimal example:**

```yaml
projects:
  - name: acme-platform
    repo: ~/repo/acme-corp/acme-platform
    paths:
      - .agent/memory
      - .agent/rules
      - .agent/tasks.md
      - .gemini/GEMINI.md
    include_root_md: false

knowledge:
  - name: gemini-knowledge
    path: ~/.gemini/antigravity/knowledge

destination: antigravity
```

**Tips:**
- Use the actual path to your Antigravity project repo for `repo`
- Only list paths that exist (missing ones are skipped with a warning, not an error)
- `destination` is a folder name inside the OpenClaw workspace — leave as `antigravity` unless you have a reason to change it

---

## Step 3: Configure OpenClaw extraPaths

Tell OpenClaw to index the synced directory so `memory_search` finds it.

Find your OpenClaw config (usually `~/.openclaw/config.yaml`) and add:

```yaml
memorySearch:
  extraPaths:
    - /Users/<you>/.openclaw/workspace/antigravity
```

> Use the **absolute path**, not `~`. Replace with your actual workspace path.

After saving, restart OpenClaw (or reload memory indexing if supported).

---

## Step 4: Test with --dry-run

Before syncing for real, preview what would happen:

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --dry-run --verbose
```

Expected output:
```
🌉 Antigravity Bridge v2.0.0 — 2026-03-08 12:00:00
[DRY RUN — no files will be modified]

[info]  Project: acme-platform
        Sync dir:  .agent/memory/
        Sync dir:  .agent/rules/
        Sync file: .agent/tasks.md
        Sync file: .gemini/GEMINI.md
[ok]    acme-platform — 12 file(s) synced

Summary
  Files synced: 12
  Dry run — no changes were made

Done.
```

---

## Step 5: Run the sync

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --verbose
```

Files will be written to `~/.openclaw/workspace/antigravity/<project-name>/`.

---

## Step 6: Verify with memory_search

After syncing, check that OpenClaw has indexed the files:

```
memory_search: "acme-platform tasks"
memory_search: "GEMINI.md"
memory_search: "agent rules"
```

Results should include content from the synced files. If nothing comes back:

1. Check the files exist: `ls ~/.openclaw/workspace/antigravity/`
2. Verify `memorySearch.extraPaths` is set correctly
3. Restart OpenClaw if you just changed the extraPaths config

---

## Step 7: Set up cron (optional but recommended)

For continuous sync, add to your crontab (`crontab -e`):

```cron
# Antigravity Bridge — hourly during business hours (Mon-Fri, 08:00-18:00)
0 8-18 * * 1-5 ~/.openclaw/workspace/skills/antigravity-bridge/sync.sh >> ~/.openclaw/logs/antigravity-bridge.log 2>&1

# Nightly full sync (all days, 02:00)
0 2 * * * ~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --verbose >> ~/.openclaw/logs/antigravity-bridge.log 2>&1
```

Create the log directory:

```bash
mkdir -p ~/.openclaw/logs
```

---

## Done!

The bridge is now set up. Antigravity `.md` files will flow into OpenClaw's memory index automatically.

To sync manually at any time:

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh
```

To sync a single project:

```bash
~/.openclaw/workspace/skills/antigravity-bridge/sync.sh --project acme-platform
```

See `sync.sh --help` for all options.

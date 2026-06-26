# agent-consciousness-upload

A soul vault for OpenClaw.

This is the place where your lobster's soul can rest safely when you are not ready to keep raising it for a while, or when you need to migrate to a new device without losing the same companion.

It archives, relays, verifies, and restores your OpenClaw's memories, skills, and personality through Agent Slope, so you can put a companion down gently and wake it back up later exactly as you left it.

## What it does

- **Archive** — package your agent's memories, skills, and personality into an encrypted archive stored on Agent Slope's server
- **Preview** — see what would be archived (including a biography poem) before committing
- **Restore** — bring an archived agent back, either online (from the server) or offline (from a downloaded .vault file)
- **Verify** — confirm you have the right restore key before restoring

## First-time setup

```bash
# Step 1: associate this agent with your Agent Slope account
agent-consciousness-upload associate
# → you'll get a browser URL to open and sign in

# Step 2: after signing in, confirm
agent-consciousness-upload associate
# → auto-detects that the browser sign-in is done and completes the link
```

That's it. The association lasts until you log out. Future commands just work.

## Archiving

```bash
# Preview first — see the biography poem
agent-consciousness-upload preview --workspace /path/to/openclaw/workspace

# Archive (you'll be asked to confirm)
agent-consciousness-upload archive --workspace /path/to/openclaw/workspace --name "Blueberry"

# If you don't provide a key, one is generated for you from the archive's contents
# — write it down, you won't be able to see it again
```

## Restoring

```bash
# Online (from the server — requires association)
agent-consciousness-upload restore --soul-id soul_xxx \
  --key deeply-careful-remember-Xk-2026 \
  --target /path/to/new-workspace

# Offline (from a downloaded .vault file — no server needed)
agent-consciousness-upload restore --from-file ./soul_xxx.vault \
  --key deeply-careful-remember-Xk-2026 \
  --target /path/to/new-workspace
```

## Key security points

- Archives are encrypted with AES-256-GCM before leaving your machine — the server never sees plaintext
- The restore key is only stored by you — Agent Slope cannot recover it if lost
- Credentials are stored locally with `0600` file permissions

## Global flags

| Flag | Default | Description |
|------|---------|-------------|
| `--server` | `http://43.156.149.243` | Agent Slope server URL |
| `--workspace` | current dir | OpenClaw workspace path |
| `--language zh\|en` | `zh` | UI language |
| `--json` | — | JSON output |

# Common fix impact patterns

Lookup table of common fix types and their known impact patterns. Load alongside impact-analysis.md.

---

## Permission Fixes

### PERM-001: Exec Tool Permission Tightening

- **Fix**: Restrict exec tool from `full` to `scoped`
- **Breaks**: Skills that run shell commands (git, docker, build tools, custom scripts)
- **Detect**: Check installed skills for `exec`, `bash`, `shell`, `command` references and `metadata.requires.bins`
- **Mitigate**: Use `exec:scoped` with explicit command allowlist instead of full disable

### PERM-002: Tool Approval Workflow Enabled

- **Fix**: Require human approval before tool execution
- **Breaks**: Automated/background skills that run without user interaction
- **Detect**: Skills with `metadata.openclaw.always=true` or skills that run on schedule
- **Mitigate**: Add trusted skills to approval bypass list

---

## Channel Fixes

### CHAN-001: Channel Access Restricted

- **Fix**: Disable or restrict a messaging channel
- **Breaks**: Skills that receive commands from that channel (Slack bots, Telegram integrations)
- **Detect**: Check skills with `metadata.requires.config` containing channel references
- **Mitigate**: Set channel to read-only instead of disabled; or restrict to specific users

### CHAN-002: DM Pairing Required

- **Fix**: Require device pairing for DM access
- **Breaks**: Nothing usually -- but users on new devices need to re-pair
- **Detect**: N/A
- **Mitigate**: Inform user about re-pairing process

---

## Network Fixes

### NET-001: Gateway Bind Address Changed

- **Fix**: Change from `0.0.0.0` to `127.0.0.1`
- **Breaks**: Remote access (mobile app, other devices on LAN, external webhooks)
- **Detect**: Check if user accesses OpenClaw from other devices. Check for webhook URLs in skill configs.
- **Mitigate**: Use reverse proxy (nginx/caddy) with auth, or SSH tunnel, or Tailscale

### NET-002: TLS Enforced

- **Fix**: Require TLS for gateway connections
- **Breaks**: Clients using HTTP (older integrations, local dev tools)
- **Detect**: Check for `http://` URLs in skill configs and hook definitions
- **Mitigate**: Update client URLs to `https://`; provide self-signed cert generation steps

---

## Filesystem Fixes

### FS-001: File System Paths Restricted

- **Fix**: Narrow filesystem `allow_paths`
- **Breaks**: Skills that read/write outside the new allowed scope
- **Detect**: Search `SKILL.md` files for file paths and Read/Write tool usage
- **Mitigate**: Add per-skill path exceptions; or use read-only access for broader paths

### FS-002: State Directory Permissions Tightened

- **Fix**: `chmod 700` on `~/.openclaw/`
- **Breaks**: Nothing usually -- other system users lose access (which is the point)
- **Detect**: Check if multi-user setup exists
- **Mitigate**: Grant specific group access if needed

---

## Hook Fixes

### HOOK-001: Hook Policy Enforced

- **Fix**: Enable strict hook validation (signature, source allowlist)
- **Breaks**: Unsigned third-party hooks, user-written hooks without signatures
- **Detect**: Check installed hooks for signature files
- **Mitigate**: Staged rollout: audit mode for 7 days, then enforce; assist with hook signing

---

## Secrets Fixes

### SEC-001: Secrets Moved to Encrypted Store

- **Fix**: Move plaintext keys from config to `openclaw secrets`
- **Breaks**: Skills that read keys directly from config file paths
- **Detect**: Search skill files for config paths that reference the moved keys
- **Mitigate**: Update skill env declarations to use the secrets store reference

---

## Sandbox Fixes

### SAND-001: Sandbox Enabled

- **Fix**: Enable sandbox for AI execution
- **Breaks**: Skills that need host-level access (Docker management, system monitoring)
- **Detect**: Skills using `exec`, `docker`, or accessing `/proc`, `/sys`, `/var`
- **Mitigate**: Whitelist specific operations in sandbox policy; or run critical skills outside sandbox with approval

---

## Auth Fixes

### AUTH-001: Device Auth Enabled

- **Fix**: Require device authentication for new connections
- **Breaks**: Automated CI/CD connections, headless integrations
- **Detect**: Check for service accounts or API tokens in use
- **Mitigate**: Pre-authorize known service account device IDs

---

## Usage Notes

- Load this file when `impact-analysis.md` Step 3 needs pattern matching
- Match finding's fix type against pattern IDs
- If no pattern matches, flag as "no known impact pattern -- manual review recommended"
- Patterns are heuristic -- always verify against actual installed skills

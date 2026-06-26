# SSH Essentials SKILL.md — Remediation Implementation Plan

> **Author:** Jules (Lead Developer)
> **Date:** 2026-05-18
> **Target:** `SKILL.md` (ssh-essentials skill)
> **Baseline:** `SKILL.md.baseline`
> **Workflow:** Plan → Build → Doc (this plan is the "Plan" phase)

---

## Overview

This document maps each identified security issue to concrete, reviewable changes in the SKILL.md. Changes are grouped into **5 batches**, each independently reviewable. All changes are additive — existing examples are preserved, security guidance is added around them.

**Consistency rules across all batches:**
- Security callouts use the `(⚠️ ...)` inline format, matching existing patterns.
- Warnings appear immediately adjacent to (usually above or below) the relevant code block.
- Backward compatibility: no existing example is removed or reordered to break usability; security guidance is layered alongside.
- Tone: practical, direct. No hand-wringing — just facts and actionable guidance.

---

## Batch 1 — Metadata + Security Callouts (Agent Forwarding, Strict Host Key, X11, Passphraseless Keys)

**Security issues addressed:** #1 (Agent Forwarding Risk), #2 (StrictHostKeyChecking=no), #7 (X11 Trusted Forwarding), #6 (Passphraseless Key Generation), #5 (Dependency Gap)

### 1.1 — Metadata: Expand dependency declaration

**What changes:** Update the frontmatter `metadata` block at the top of SKILL.md.

**Current (line ~4):**
```yaml
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["ssh"]}}}
```

**New:**
```yaml
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["ssh","scp","sftp","rsync","ssh-keygen","ssh-copy-id"]}}}
```

> ⚠️ **Note:** `scp` is deprecated in modern OpenSSH. The metadata still lists it for backward compatibility, but `sftp` should be preferred for file transfers. See Batch 5 for the `sftp` guidance.

**Why:** Issue #5 — Only `ssh` was declared. All tools actually referenced in examples must be listed in the metadata for ClawScan dependency tracking.

**Security impact:** Low — enables proper dependency auditing. No behavioral change.

---

### 1.2 — Agent Forwarding Callouts in "Interactive use" section

**What changes:** Add inline warnings before the `-A` and `ForwardAgent yes` examples.

**Location:** `## Basic Connection` → `### Interactive use` section, around lines 39-47.

**Change to the agent forwarding example block:**
```bash
# Connect with forwarding agent
ssh -A user@hostname
# (⚠️ Agent forwarding exposes the local SSH agent to the remote host.
#  Compromise of the remote server = compromise of all identities forwarded through it.
#  Prefer ProxyJump or ProxyCommand instead. See Tunneling section for safer alternatives.)
```

**Change to the config section's `ForwardAgent yes` example:**
Add a callout next to the `ForwardAgent yes` line in the config block (lines ~147-148):
```
    ForwardAgent yes  # (⚠️ Only forward to hosts you fully trust. The remote server can use your identities to authenticate elsewhere.)
```

**Why:** Issue #1 — Agent forwarding risk was undocumented inline. The current warning is buried in Tips.

**Security impact:** Medium — Makes users aware of the risk before they enable agent forwarding.

---

### 1.3 — StrictHostKeyChecking=no → accept-new migration

**What changes:** Two locations affected.

**Location A:** `### Connection security` section (around line 219) — the `StrictHostKeyChecking=yes` example.

**Add after the `ssh -o StrictHostKeyChecking=yes` line:**
```bash
# (⚠️ This blocks connections to new hosts. Use accept-new for automated first-time connections.)
```

**Location B:** `### Common issues` section (around line 239) — the `StrictHostKeyChecking=no` example.

**Current (actual) line in Common issues section:**
```bash
# Disable host key checking (not recommended)
ssh -o StrictHostKeyChecking=no user@hostname
```

**Replacement block:**
```bash
> ⚠️ **TROUBLESHOOTING ALERT:** If you're using StrictHostKeyChecking=no because a
> connection is being refused, you're disabling MITM protection as a convenience.
> The remote server's host key may have legitimately changed (reinstall, new image),
> but this option accepts ANY key without verification — including a fake one from
> an attacker on the network path. The consequence: you lose all host verification
> and can be silently intercepted. Fix the real issue instead of disabling checks.
ssh -o StrictHostKeyChecking=no user@hostname  # (⚠️ NOT RECOMMENDED: Disables MITM protection)

# (⚠️ Prefer StrictHostKeyChecking=accept-new — adds new host keys safely without accepting unknown ones)
ssh -o StrictHostKeyChecking=accept-new user@hostname
```

**Why:** Issue #2 — The current "(not recommended)" text doesn't explain the MITM risk. Users might use this as a quick fix without understanding the consequences.

**Security impact:** Medium-High — Prevents users from accidentally disabling host verification as a troubleshooting shortcut.

---

### 1.4 — X11 forwarding distinction

**What changes:** In the `### Interactive use` section, expand the X11 forwarding examples.

**Location:** Around lines 44-47, after `ssh -Y user@hostname  # Trusted X11`.

**Replace the X11 examples with expanded version:**
```bash
# Connect with X11 forwarding (GUI apps)
ssh -X user@hostname  # Untrusted X11 (sandboxed, safer — Xfixes restrictions apply)
ssh -Y user@hostname  # Trusted X11 (full X access, can execute arbitrary X commands)

# (⚠️ -Y grants the remote host full access to your local X server. Malicious apps can capture keystrokes/screenshots.
#  Prefer -X unless you specifically need trusted X11 forwarding for performance-critical GUI apps.)
```

**Why:** Issue #7 — No distinction between `-X` (untrusted) and `-Y` (trusted) was documented.

**Security impact:** Low-Medium — Users who blindly use `-Y` risk keylogging/screen capture if the remote host is compromised.

---

### 1.5 — Passphraseless key generation warning

**What changes:** In the `### Generating keys` section.

**Location:** Around lines 63-66, the `ssh-keygen -t ed25519 -N ""` example.

**Add a callout after the example:**
```bash
# Generate without passphrase (automation)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_deploy
# (⚠️ WARNING: Keys without passphrases are stored as plaintext on disk.
#  If the key file is stolen, anyone can use it. For automation, prefer ssh-agent
#  with passphrase-protected keys and add the key with ssh-add.)
```

**Why:** Issue #6 — No warning about plaintext key storage risk.

**Security impact:** Low-Medium — Automated deployments often copy passphraseless keys to CI/CD servers; if those are compromised, all downstream systems are vulnerable.

---

## Batch 2 — Rsync Safety Improvements

**Security issues addressed:** #3 (rsync --delete data-loss risk)

### 2.1 — Reorder dry-run before --delete, add warnings

**What changes:** In the `### Rsync over SSH` section, reorder the examples.

**Location:** Around lines 187-198.

**Current order (problematic):**
```bash
# Sync directory
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Sync with progress
rsync -avz --progress /local/dir/ user@hostname:/remote/dir/

# Sync with delete (mirror)
rsync -avz --delete /local/dir/ user@hostname:/remote/dir/

# Exclude patterns
rsync -avz --exclude '*.log' --exclude 'node_modules/' \
  /local/dir/ user@hostname:/remote/dir/

# Custom SSH port
rsync -avz -e "ssh -p 2222" /local/dir/ user@hostname:/remote/dir/

# Dry run
rsync -avz --dry-run /local/dir/ user@hostname:/remote/dir/
```

**New order and content:**
```bash
# Sync directory (safe, no deletions)
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Sync with progress
rsync -avz --progress /local/dir/ user@hostname:/remote/dir/

# (⚠️ ALWAYS test with --dry-run first when using --delete.
#  --delete removes files on the destination that don't exist on the source — this is destructive.)

# Dry run (review what would happen before executing)
rsync -avz --dry-run --delete /local/dir/ user@hostname:/remote/dir/
# Review the output, then execute the real command

# Sync with delete (mirror) — only after dry-run confirms expected changes
rsync -avz --delete /local/dir/ user@hostname:/remote/dir/
# (⚠️ DELETION WARNING: This removes files from the destination that aren't in the source.
#  Double-check --dry-run output before running. Consider using --ignore-errors for large transfers.)

# Exclude patterns (protect important files)
rsync -avz --exclude '*.log' --exclude 'node_modules/' \
  /local/dir/ user@hostname:/remote/dir/

# Exclude multiple patterns (better for complex setups)
rsync -avz --exclude={'*.log','*.tmp','*.cache','node_modules/'} \
  /local/dir/ user@hostname:/remote/dir/

# Custom SSH port
rsync -avz -e "ssh -p 2222" /local/dir/ user@hostname:/remote/dir/
```

**Why:** Issue #3 — The original order taught `--delete` before `--dry-run`, which is backwards from safe practice. Users who copy-paste the `--delete` example without reading ahead risk data loss.

**Security impact:** Medium — Prevents accidental data deletion on production servers.

---

## Batch 3 — Tunnel Lifecycle Management

**Security issues addressed:** #4 (Background Tunnels persistence), #8 (Wildcard config + agent forwarding)

### 3.1 — Background tunnel cleanup instructions

**What changes:** In the `### Background tunnels` section.

**Location:** Around lines 122-138.

**Current block:**
```bash
# Run in background
ssh -f -N -L 8080:localhost:80 user@hostname

# -f: Background
# -N: No command execution
# -L: Local forward

# Keep alive
ssh -o ServerAliveInterval=60 -L 8080:localhost:80 user@hostname
```

**New content (preserve existing examples, add lifecycle management):**
```bash
# Run in background
ssh -f -N -L 8080:localhost:80 user@hostname

# -f: Background
# -N: No command execution
# -L: Local forward

# Keep alive
ssh -o ServerAliveInterval=60 -L 8080:localhost:80 user@hostname

# (⚠️ Background tunnels persist after you close your terminal. Always clean up when done.)

# Check active tunnels
ssh -O check user@hostname

# Clean shutdown of a background tunnel
ssh -O exit user@hostname

# Kill all stale SSH connections
pkill -f "ssh.*-L.*8080"  # Replace port number with your tunnel port

# (⚠️ Stale tunnels consume server resources and leave ports open. Clean up with `ssh -O exit`.)
```

**Why:** Issue #4 — No cleanup instructions. Tunnels left running consume resources and create security exposure.

**Security impact:** Low-Medium — Reduces attack surface from abandoned tunnels.

---

### 3.2 — Wildcard config + agent forwarding warning

**What changes:** In the `### SSH config file` section.

**Location:** Around lines 141-152, the `Host *.example.com` block.

**Current block:**
```
# Wildcard configuration
Host *.example.com
    User admin
    ForwardAgent yes
```

**New block:**
```
# Wildcard configuration — use with extreme caution
# (⚠️ Wildcard Host patterns match ALL domains matching the glob.
#  ForwardAgent yes under *.example.com means your agent identity is forwarded
#  to EVERY matching host, including any newly added subdomains. This is a
#  significant agent forwarding risk.)

# Instead of wildcard, use specific host entries:
Host bastion.example.com
    User admin
    ForwardAgent yes  # Only forward to this specific, trusted host

Host web.example.com
    User admin
    # No ForwardAgent — don't forward unless explicitly needed

# (⚠️ Best practice: Only enable ForwardAgent on hosts you fully trust and need it.)

# Keep connections alive
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Why:** Issue #8 — `Host *.example.com` with `ForwardAgent yes` applies to ALL matching hosts. This is especially dangerous as new subdomains can be provisioned without the admin realizing agent forwarding is enabled.

**Security impact:** Medium — Prevents accidental agent forwarding to untrusted hosts via wildcard expansion.

---

## Batch 4 — Connection Security Hardening

**Security issues addressed:** #9 (Connection security section gaps), #2 (StrictHostKeyChecking=accept-new workflow)

### 4.1 — Expand Connection Security section

**What changes:** In the `### Connection security` section.

**Location:** Around lines 214-227.

**Current content:**
```bash
# Check host key
ssh-keygen -F hostname

# Remove old host key
ssh-keygen -R hostname

# Strict host key checking
ssh -o StrictHostKeyChecking=yes user@hostname

# Use specific cipher
ssh -c aes256-ctr user@hostname
```

**New content:**
```bash
# Check host key
ssh-keygen -F hostname

# Remove old/stale host key
ssh-keygen -R hostname

# Strict host key checking — three modes:
ssh -o StrictHostKeyChecking=yes user@hostname
# Blocks connections to hosts not in known_hosts. Safe but inconvenient for first-time connections.

ssh -o StrictHostKeyChecking=accept-new user@hostname
# Preferred: Accepts new host keys but refuses unknown ones without prompting.
# Safer than 'no' and doesn't block legitimate first-time connections.

ssh -o StrictHostKeyChecking=no user@hostname
# (⚠️ NOT RECOMMENDED: Accepts any host key without verification. Vulnerable to MITM.)

# Verify and store a known-good host key (safe pre-population workflow)
ssh-keyscan -t ed25519 hostname
# (⚠️ Run ssh-keyscan independently first, compare the output against a trusted key
#  obtained via another channel (e.g., admin console, PGP-signed key page). Only then append:
ssh-keyscan -t ed25519 hostname >> ~/.ssh/known_hosts
#  If the scanned key doesn't match the trusted key, DO NOT append it.)

# Use specific cipher
ssh -c aes256-ctr user@hostname
```

**Why:** Issue #9 + #2 — The connection security section had `StrictHostKeyChecking=yes` documented but only `(not recommended)` for `no`. Users need to understand all three modes and when each is appropriate. The `ssh-keyscan` workflow provides a safe way to pre-populate `known_hosts`.

**Security impact:** Medium-High — Users learn to use `accept-new` (safe default) instead of `no` (dangerous). The `ssh-keyscan` guidance provides a path to pre-verify host keys.

---

## Batch 5 — Dependency Metadata + Documentation Structure Improvements

**Security issues addressed:** #5 (Dependency Gap — already partially addressed in 1.1), Documentation clarity

### 5.0 — New: Missing security callouts

The following callouts were identified as missing from the baseline. Added as a cohesive group below.

**SOCKS Proxy (Dynamic Port Forwarding) — add to the Tunneling section:**
```bash
# SOCKS proxy (dynamic port forwarding)
ssh -D 1080 user@hostname
# (⚠️ SOCKS5 traffic is NOT encrypted by default. Browsers configured to use a SOCKS proxy
#  may send credentials and data in cleartext. For encrypted proxy traffic, use SSH -L or -R
#  port forwarding instead of SOCKS, or use a TLS-based proxy like mitmproxy.)
```

**Remote Port Forwarding (`-R`) — add to the Tunneling section:**
```bash
# Remote port forwarding (expose local service on remote server)
ssh -R 8080:localhost:8080 user@hostname
# (⚠️ WARNING: This exposes your local services to the remote server. Any user with
#  access to the remote host can connect to your local ports. Only use -R on trusted
#  bastion hosts, never on untrusted public servers.)
```

### 5.1 — Add "Security Notes" callout section in File Transfers

**What changes:** Add security callout blocks before the SFTP and SCP examples.

**Location:** After `### SFTP (Secure FTP)` header, before the SFTP examples.

**Insert:**
```markdown
> (⚠️ SFTP sessions leave files on the remote server. Use `rm` in SFTP to clean up sensitive temporary files.)
> (⚠️ SCP is deprecated in modern OpenSSH versions. Use sftp for interactive transfers
>  or rsync for directory syncs. The scp protocol has known security and reliability issues.)
```

### 5.2 — Add SSH Agent Security Note

**What changes:** In the `### SSH agent` section, add a cleanup best practice callout.

**Location:** After the `ssh-add -t 3600` example (around line 96).

**Add after the agent lifetime example:**
```bash
# Set key lifetime (seconds)
ssh-add -t 3600 ~/.ssh/id_rsa
# (⚠️ Use short-lived keys (-t) for shared/bastion hosts. Remove keys when done: ssh-add -d ~/.ssh/id_rsa)
```

> ⚠️ Always remove keys from agent when done: `ssh-add -D` to clear all, or `ssh-add -d` to remove specific keys.

### 5.3 — Add Multiplexing Security Notes

**What changes:** In the `### Multiplexing` section, add security callouts.

**Location:** Around lines 272-280, the multiplexing examples.

**Current:**
```bash
# Master connection
ssh -M -S ~/.ssh/control-%r@%h:%p user@hostname

# Reuse connection
ssh -S ~/.ssh/control-user@hostname:22 user@hostname

# In config:
# ControlMaster auto
# ControlPath ~/.ssh/control-%r@%h:%p
# ControlPersist 10m
```

**New with callouts:**
```bash
# Master connection (creates multiplexed session)
ssh -M -S ~/.ssh/control-%r@%h:%p user@hostname

# Reuse existing connection
ssh -S ~/.ssh/control-user@hostname:22 user@hostname

# (⚠️ Control sockets are stored on disk. On shared systems, ensure ~/.ssh has 700 permissions.
#  Anyone with access to the control socket can impersonate you on the target host.)

# In config (recommended approach):
# ControlMaster auto
# ControlPath ~/.ssh/control-%r@%h:%p
# ControlPersist 10m

# (⚠️ ControlPersist keeps the master connection alive. Stale connections can be exploited.
#  Set a reasonable timeout (e.g., 10m–30m) rather than "yes" (infinite).)
```

**Why:** Control sockets are an under-recognized attack vector. If the local filesystem is compromised, the control socket can be used for lateral movement.

**Security impact:** Low-Medium — Raises awareness of control socket risks.

---

## Summary of Security Impact

| Issue | Severity | Batch | Fix |
|-------|----------|-------|-----|
| Agent Forwarding Risk | Medium | 1, 3 | Inline warnings, prefer ProxyJump, specific hosts over wildcards |
| StrictHostKeyChecking=no | Medium-High | 1, 4 | MITM warning, `accept-new` as preferred alternative, `ssh-keyscan` workflow |
| rsync --delete | Medium | 2 | Reorder dry-run first, explicit deletion warnings, exclude patterns |
| Background Tunnels | Low-Medium | 3 | `-O exit` cleanup, `pkill` for stale tunnels, monitoring |
| Dependency Gap | Low | 5 | All referenced bins in metadata |
| Passphraseless Keys | Low-Medium | 1 | Inline warning, ssh-agent preference |
| X11 Trusted Forwarding | Low-Medium | 1 | `-X` vs `-Y` distinction, security note |
| Wildcard Config + Agent Fwd | Medium | 3 | Replace wildcard with specific hosts |
| Connection Security Gaps | Medium-High | 4 | Three-mode explanation, `ssh-keyscan` guidance |

---

## QA Checklist (for Verne's review)

Each batch should be independently verifiable:

1. **Batch 1:** Verify all four callout locations (agent forwarding, strict host key, X11, passphraseless keys). Confirm `(⚠️ ...)` format is consistent.
2. **Batch 2:** Verify dry-run example appears BEFORE `--delete` example. Confirm deletion warning is prominent.
3. **Batch 3:** Verify `ssh -O exit` example exists. Verify wildcard config replaced with specific host entries.
4. **Batch 4:** Verify `accept-new` is presented as the recommended default. Verify `ssh-keyscan` includes out-of-band verification warning.
5. **Batch 5:** Verify metadata bins list includes all 6 tools. Verify multiplexing and agent sections have security callouts.

**Global checks:**
- [ ] No existing examples removed or reordered (except dry-run/--delete reordering in Batch 2)
- [ ] All security callouts use consistent `(⚠️ ...)` inline format
- [ ] Tone is practical and direct (no hand-wringing)
- [ ] Backward compatible — existing users can still use all original examples
- [ ] Document is still readable as a practical SSH reference guide

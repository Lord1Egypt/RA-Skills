# Changelog — SSH Essentials Security Remediation
**Date:** 2026-05-18
**Version:** 2.0 (security remediation)
**Baseline:** `SKILL.md.baseline` → `SKILL.md` (final)

## Summary

This release remediates the SSH Essentials SKILL.md with comprehensive security callouts across all sections. The baseline document was a practical SSH reference guide with limited security guidance. The new version preserves every original example while layering inline warnings and blockquote alerts for high-risk configurations. All 15 changes across 5 batches passed QA review with no rework needed.

## Changes by Batch

### Batch 1 — Metadata + Security Callouts

| # | Change | Location |
|---|--------|----------|
| 1.1 | Metadata `bins` expanded from `["ssh"]` to `["ssh","scp","sftp","rsync","ssh-keygen","ssh-copy-id"]` | Frontmatter |
| 1.2 | Agent forwarding inline warnings added after `-A` example and `ForwardAgent yes` config entry | `### Interactive use`, `### SSH config file` |
| 1.3 | `StrictHostKeyChecking=yes` annotated with `accept-new` recommendation; `no` replaced with MITM blockquote + full warning | `### Connection security`, `### Common issues` |
| 1.4 | X11 forwarding expanded: `-X` (sandboxed) vs `-Y` (full access) with security warning | `### Interactive use` |
| 1.5 | Passphraseless key plaintext storage warning added | `### Generating keys` |

### Batch 2 — Rsync Safety

| # | Change | Location |
|---|--------|----------|
| 2.1 | Reordered: `--dry-run` example moved before `--delete` with explicit deletion warning | `### Rsync over SSH` |
| 2.1 | Exclude pattern examples expanded (single `--exclude` + brace expansion) | `### Rsync over SSH` |

### Batch 3 — Tunnel Lifecycle

| # | Change | Location |
|---|--------|----------|
| 3.1 | Added tunnel lifecycle management: `ssh -O check`, `ssh -O exit`, `pkill` cleanup with lifecycle warning blockquote | `### Background tunnels` |
| 3.2 | Replaced dangerous wildcard `Host *.example.com` with specific host entries (`bastion.example.com`, `web.example.com`); added best-practice callout | `### SSH config file` |

### Batch 4 — Connection Security

| # | Change | Location |
|---|--------|----------|
| 4.1 | Three-mode `StrictHostKeyChecking` explanation (`yes`, `accept-new`, `no`) with risk descriptions | `### Connection security` |
| 4.1 | `ssh-keyscan` out-of-band key verification workflow with trusted comparison step | `### Connection security` |

### Batch 5 — Additional Security Callouts

| # | Change | Location |
|---|--------|----------|
| 5.0 | SOCKS proxy (`-D`) unencrypted traffic warning; Remote port forwarding (`-R`) exposure risk warning | `### Dynamic port forwarding`, `### Remote port forwarding` |
| 5.1 | SCP deprecation notice; SFTP session file cleanup note | `### SCP`, `### SFTP` |
| 5.2 | SSH agent lifetime guidance + cleanup callouts after `ssh-add -t` | `### SSH agent` |
| 5.3 | Multiplexing control socket security warnings; `ControlPersist` stale connection warning | `### Multiplexing` |

## QA Summary

**Reviewer:** Verne (QA Gatekeeper)  
**Decision:** PASS — no rework needed

### Scores

| Batch | Quality | Features | Security | Efficacy | Comment Quality |
|-------|---------|----------|----------|----------|-----------------|
| 1 | 10 | 10 | 10 | 10 | 10 |
| 2 | 10 | 10 | 10 | 10 | 10 |
| 3 | 10 | 10 | 10 | 10 | 10 |
| 4 | 10 | 10 | 10 | 10 | 10 |
| 5 | 10 | 10 | 10 | 10 | 10 |

**Holistic Score: 10/10** (Integration, Architecture, Maintainability)

### Cross-Cutting Checks

- [x] No existing examples accidentally removed (only wildcard config intentionally replaced per plan)
- [x] All security callouts use consistent `(⚠️ ...)` inline format
- [x] Blockquote format consistent for MITM troubleshooting alert
- [x] Tone is practical and direct
- [x] Backward compatible — all original examples preserved
- [x] Document remains a readable SSH reference guide

## Migration Notes

- All changes are **additive** — no existing examples were removed (except the intentional wildcard config replacement in Batch 3 per the approved plan)
- The only structural change to example ordering: `--dry-run` moved before `--delete` in rsync examples (safe, dry-run was always present)
- Backward compatible: existing SSH workflows documented in the baseline continue to work unchanged
- Security guidance is layered alongside existing content, never replacing it

## Files

| File | Status | Description |
|------|--------|-------------|
| `SKILL.md` | ✅ Final | Complete document with all security callouts integrated |
| `SKILL.md.baseline` | 📎 Reference | Original document (pre-remediation) |

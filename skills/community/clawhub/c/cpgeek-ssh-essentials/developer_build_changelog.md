# SSH Essentials SKILL.md — Build Log

> **Author:** Jules (Lead Developer)
> **Date:** 2026-05-18
> **Phase:** Build
> **Baseline:** `SKILL.md.baseline`
> **Output:** `SKILL.md`

---

## Summary

Produced the complete, final `SKILL.md` with all security callouts integrated per the approved remediation plan (`developer_plan_changelog.md`). All existing examples preserved; security guidance layered alongside.

## Changes by Batch

### Batch 1 — Metadata + Security Callouts

| # | Change | Location |
|---|--------|----------|
| 1.1 | Metadata `bins` expanded from `["ssh"]` to `["ssh","scp","sftp","rsync","ssh-keygen","ssh-copy-id"]` | Frontmatter |
| 1.2 | `(⚠️ Agent forwarding exposes...)` callout added after `ssh -A` example; `(⚠️ Only forward to hosts you fully trust...)` added to `ForwardAgent yes` in config | `### Interactive use`, `### SSH config file` |
| 1.3 | `(⚠️ This blocks connections...)` added after `StrictHostKeyChecking=yes`; full `> ⚠️ **TROUBLESHOOTING ALERT:**` blockquote + `accept-new` alternative added in `### Common issues` | `### Connection security`, `### Common issues` |
| 1.4 | Expanded X11 docs: `-X` (untrusted, sandboxed) vs `-Y` (trusted, full X access) with security warning | `### Interactive use` |
| 1.5 | `(⚠️ WARNING: Keys without passphrases...)` added after passphraseless key example | `### Generating keys` |

### Batch 2 — Rsync Safety

| # | Change | Location |
|---|--------|----------|
| 2.1 | Reordered: `--dry-run` example placed BEFORE `--delete`; explicit deletion warning block added; exclude patterns section expanded | `### Rsync over SSH` |

### Batch 3 — Tunnel Lifecycle

| # | Change | Location |
|---|--------|----------|
| 3.1 | Added `ssh -O check`, `ssh -O exit`, `pkill -f` cleanup examples with lifecycle warnings | `### Background tunnels` |
| 3.2 | Replaced `Host *.example.com` wildcard with specific host entries (`bastion.example.com`, `web.example.com`); added `(⚠️ Best practice...)` callout | `### SSH config file` |

### Batch 4 — Connection Security

| # | Change | Location |
|---|--------|----------|
| 4.1 | Added `accept-new` as preferred mode; `no` mode with MITM warning; `ssh-keyscan` verification workflow with out-of-band check callout | `### Connection security` |

### Batch 5 — Missing Security Callouts

| # | Change | Location |
|---|--------|----------|
| 5.0 | SOCKS traffic warning after `-D` example; `-R` risk warning after remote port forwarding | `### Dynamic port forwarding`, `### Remote port forwarding` |
| 5.1 | SCP deprecation warning; SFTP cleanup reminder | `### SCP`, `### SFTP` |
| 5.2 | Agent lifetime + cleanup note added after `ssh-add -t` | `### SSH agent` |
| 5.3 | Multiplexing control socket security warnings + ControlPersist timeout guidance | `### Multiplexing` |

## Decisions Made

1. **Formatting consistency:** All inline warnings use `(⚠️ ...)` format. High-risk blockquotes use `> ⚠️ **DANGER:**` or `> ⚠️ **TROUBLESHOOTING ALERT:**` as specified in the plan.
2. **No examples removed:** All original examples preserved. Security guidance is layered alongside, never replacing existing content.
3. **Rsync reorder:** The only structural change — `--dry-run` moved before `--delete` with explicit warnings. This is safe because dry-run examples were always present; only the order changed to follow best practice.
4. **Wildcard config:** Replaced with specific host entries rather than just adding a warning to the wildcard block. This provides actionable guidance (use specific hosts instead of wildcards).
5. **Connection security section:** `StrictHostKeyChecking=yes` example kept with `accept-new` recommendation appended. The `no` example kept with full MITM risk explanation.

## Files Modified

- `SKILL.md` — Complete rewrite with all security callouts integrated (new file, replacing baseline)

## Verification

- [x] All 6 bins listed in metadata (`ssh`, `scp`, `sftp`, `rsync`, `ssh-keygen`, `ssh-copy-id`)
- [x] Agent forwarding warnings in both interactive use and config sections
- [x] StrictHostKeyChecking `no` replaced with `accept-new` recommendation + full MITM warning
- [x] X11 `-X` vs `-Y` distinction documented
- [x] Passphraseless key warning present
- [x] Rsync `--dry-run` before `--delete` with deletion warnings
- [x] Tunnel lifecycle cleanup (`ssh -O exit`, `pkill`) documented
- [x] Wildcard config replaced with specific host entries
- [x] `accept-new` presented as recommended default
- [x] `ssh-keyscan` workflow with out-of-band verification warning
- [x] SOCKS unencrypted traffic warning
- [x] Remote port forwarding (`-R`) risk warning
- [x] SCP deprecation notice
- [x] SSH agent cleanup guidance
- [x] Multiplexing socket security notes
- [x] No existing examples removed
- [x] Consistent `(⚠️ ...)` inline warning format throughout

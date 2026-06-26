# Configuration Management CLI Reference

Multi-vendor command reference for configuration management operations across
Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

## Architecture Differences

Understanding each vendor's config model is critical for correct comparison:

- **Cisco (IOS-XE/NX-OS):** Dual-config model — `running-config` (active in
  memory) and `startup-config` (saved to NVRAM/flash). Changes apply
  immediately to running-config. Must explicitly `copy run start` to persist.
- **JunOS:** Candidate-commit model — edits are staged in a candidate config
  and only applied with `commit`. Supports `rollback N` to revert to any of the
  last 50 committed configs. Active config = last committed config.
- **EOS:** Hybrid model — like Cisco with running/startup, but also supports
  `configure session` for staged changes similar to JunOS candidates. Sessions
  can be reviewed and committed or aborted atomically.

## Config Display Commands (Read-Only)

| Operation | Cisco | JunOS | EOS |
|-----------|-------|-------|-----|
| Show running config | `show running-config` | `show configuration` | `show running-config` |
| Show startup/saved config | `show startup-config` | `show configuration | compare rollback 1` | `show startup-config` |
| Show candidate config | N/A | `show configuration | compare` | `show session-config [name]` |
| Show config section | `show running-config \| section [keyword]` | `show configuration [hierarchy]` | `show running-config section [keyword]` |
| Show config diff (run vs start) | `show archive config differences system:running-config nvram:startup-config` | `show \| compare rollback 0` | `show running-config diffs` |
| Last config change timestamp | `show running-config \| include Last` | `show system commit` | `show running-config \| include Last` |

## Config Archive / Export Commands

| Operation | Cisco | JunOS | EOS |
|-----------|-------|-------|-----|
| ⚠️ Copy to TFTP | `copy running-config tftp://[server]/[file]` | `request system configuration save [path]` | `copy running-config tftp://[server]/[file]` |
| ⚠️ Copy to SCP | `copy running-config scp://[user]@[server]/[file]` | `request system configuration save scp://[user]@[server]/[file]` | `copy running-config scp://[user]@[server]/[file]` |
| ⚠️ Copy to flash | `copy running-config flash:[file]` | `request system configuration save /var/tmp/[file]` | `copy running-config flash:[file]` |
| ⚠️ Save running to startup | `copy running-config startup-config` | `commit` (implicit) | `copy running-config startup-config` |
| Check flash space | `dir flash:` | `file list /var/tmp/ detail` | `dir flash:` |
| Show config archive history | `show archive` | `show system commit` | `show config sessions` |

## Config Compare / Diff Commands (Read-Only)

| Operation | Cisco | JunOS | EOS |
|-----------|-------|-------|-----|
| Diff running vs startup | `show archive config differences system:running-config nvram:startup-config` | `show \| compare rollback 0` | `show running-config diffs` |
| Diff running vs file | `show archive config differences system:running-config flash:[file]` | `show \| compare [file]` | `diff running-config flash:[file]` |
| Diff two saved configs | `show archive config differences flash:[file1] flash:[file2]` | `show \| compare rollback [n1] rollback [n2]` | `diff flash:[file1] flash:[file2]` |
| Show rollback history | `show archive` | `show system commit` | `show config sessions` |

## Config Rollback / Replace Commands

> ⚠️ **WRITE operations** — these modify device state. Confirm authorization
> and maintenance window before executing.

| Operation | Cisco | JunOS | EOS |
|-----------|-------|-------|-----|
| ⚠️ Replace with file | `configure replace flash:[file] force` | `rollback [n]` then `commit` | `configure replace flash:[file]` |
| ⚠️ Rollback to previous | `configure replace flash:[backup] force` | `rollback 1` then `commit` | `configure replace flash:[backup]` |
| ⚠️ Confirm replace | Auto with `force` flag | `commit confirmed [minutes]` | `configure replace` prompts |
| ⚠️ Abort staged changes | `end` (discards config mode) | `rollback 0` (discard candidate) | `abort` (in session mode) |
| Preview rollback diff | `show archive config differences system:running-config flash:[file]` | `show \| compare rollback [n]` | `diff running-config flash:[file]` |

## Config Session Commands (Staged Changes)

| Operation | Cisco | JunOS | EOS |
|-----------|-------|-------|-----|
| ⚠️ Enter config mode | `configure terminal` | `configure` (enters candidate) | `configure terminal` |
| ⚠️ Create named session | N/A | N/A (single candidate) | `configure session [name]` |
| Review pending changes | N/A (applied immediately) | `show \| compare` | `show session-config [name]` |
| ⚠️ Commit staged changes | N/A (applied immediately) | `commit` | `commit` (in session) |
| ⚠️ Commit with auto-rollback | N/A | `commit confirmed [minutes]` | `commit timer [duration]` |
| ⚠️ Abort staged changes | `end` | `rollback 0` | `abort` |

## Compliance Check Commands (Read-Only)

| Check | Cisco | JunOS | EOS |
|-------|-------|-------|-----|
| Verify AAA is active | `show aaa sessions` | `show system login` | `show aaa` |
| Check NTP sync | `show ntp status` | `show ntp associations` | `show ntp status` |
| Check logging config | `show logging \| include Logging` | `show system syslog` | `show logging` |
| Verify SSH-only access | `show line vty 0 15 \| include transport` | `show configuration system services` | `show management ssh` |
| Check SNMP ACL | `show snmp community` | `show snmp v3` | `show snmp community` |

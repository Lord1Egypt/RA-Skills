# Chocolatey Metadata Update Failure Fix

Diagnosis and recovery procedure for cases where **the runtime/installer succeeds but the chocolatey metadata (`.nuspec`) update fails** after invoking UniGetUI or choco upgrade.

## Background

Starting from UniGetUI 2026.1.7, the chocolatey bundle was removed and it became a passthrough to the system `choco`. Since UniGetUI only displays the results of `choco list`, metadata update failure is the **responsibility of chocolatey**.

Related issues:
- [Devolutions/UniGetUI#4803](https://github.com/Devolutions/UniGetUI/issues/4803) — Inconsistent chocolatey packages since 2026.1.7
- [Devolutions/UniGetUI#4801](https://github.com/Devolutions/UniGetUI/issues/4801) — Wrong information about installed programs (2026.1.10)
- [Devolutions/UniGetUI#3708](https://github.com/Devolutions/UniGetUI/issues/3708) — choco.exe hang on update check
- [Devolutions/UniGetUI#4217](https://github.com/Devolutions/UniGetUI/issues/4217) — Chocolatey shown as ready on MS Store install

## Symptoms

| Symptom | Meaning |
|---------|---------|
| "Upgrade available" indication persists in UniGetUI | `choco list` returns old version |
| `choco list <pkg>` shows old version, actual EXE is new version | Only `.nuspec` is stale |
| Same package keeps appearing in `choco outdated` | Metadata stage exits abnormally |
| choco exits abnormally after "already installed" in installer log | Package stage may be skipped |

## Diagnosis Procedure

### 1. Compare Metadata vs Actual Version

```bash
# Version recognized by chocolatey
choco list <pkg>

# Metadata version in .nuspec
grep -i version "C:\ProgramData\chocolatey\lib\<pkg>\<pkg>.nuspec" | head -1

# Actual installed runtime version (e.g., vcredist140)
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Version 2>&1 | grep Version
```

If the three values diverge, metadata stale is confirmed.

### 2. Verify with choco outdated

```bash
choco outdated 2>&1 | grep -E "^[a-zA-Z0-9_-]+\|"
```

Output line: `<pkg>|<current metadata>|<remote latest>|<pinned>`. Suspect if metadata differs from external systems (WMI/registry).

## Recovery Procedure

### 1. Force Resync (default)

```bash
# Invoke via PowerShell tool (bypass Bash escape)
gsudo choco upgrade <pkg> -y
```

After success, verify version match with `choco list <pkg>`.

### 2. Use --force (when 1 has no effect)

```bash
gsudo choco upgrade <pkg> -y --force
```

`--force` re-runs the package stage even if already at the latest version to update `.nuspec`.

### 3. Bulk Update

```bash
gsudo choco upgrade all -y
```

Cleans up large amounts of outdated entries. Effective when UniGetUI has accumulated stale indicators.

### 4. Manual nuspec Patch (last resort)

If choco refuses to update for any reason, directly modify the `<version>` node in `.nuspec`. **Not recommended** — risk of being overwritten by the next upgrade or causing dependency mismatch.

## Don't / Do Table

| # | Don't | Do |
|---|-------|-----|
| 1 | Repeatedly upgrade the same package in UniGetUI GUI | Run `gsudo choco upgrade <pkg> -y` directly in an elevated terminal |
| 2 | Directly edit `.nuspec` when suspecting metadata stale | Use `--force` so chocolatey performs a proper update |
| 3 | File an issue in the UniGetUI repository | UniGetUI is a passthrough — report to chocolatey-core (chocolatey/choco) or the package maintainer |
| 4 | Invoke `choco upgrade` from Bash (without elevation) | PowerShell tool + `gsudo` or administrator PowerShell |
| 5 | Conclude success from the `choco upgrade` output line alone | Immediately cross-verify with `choco list <pkg>` + `.nuspec` version |

## Self-check (every time a UniGetUI/choco metadata stale report is received)

1. Compare three values: `choco list <pkg>` + `.nuspec` version + actual runtime version
2. All three match → possible UniGetUI cache issue. Restart UniGetUI or refresh the package
3. Only choco metadata and .nuspec are stale → `gsudo choco upgrade <pkg> -y`
4. If step 1 has no effect → `gsudo choco upgrade <pkg> -y --force`
5. If step 4 also fails → report an issue to the package maintainer (chocolatey.org package page)

## Violation / Application Cases

**2026-05-21 (1st occurrence)**: vcredist140 14.51.36231 → 14.51.36247 metadata update failure. UniGetUI repeatedly attempted updates but the system runtime was already 14.51.36247. `gsudo choco upgrade vcredist140 -y` completed the .nuspec update at once. The log shows `Runtime for architecture x64 version 14.51.36247 is already installed` — a case where only the package stage needed updating.

## References

- [UniGetUI repo](https://github.com/Devolutions/UniGetUI)
- [chocolatey/choco repo](https://github.com/chocolatey/choco)
- "choco metadata" keyword in `~/.claude/skills/cleanup/data/failed-attempts.md` (if present)

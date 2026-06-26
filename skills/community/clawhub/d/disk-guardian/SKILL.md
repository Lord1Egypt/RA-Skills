---
name: disk-guardian
description: Run S.M.A.R.T. diagnostics on all drives, parse health indicators, maintain a history log, and flag drives showing early failure patterns. Generates health summaries and "drives ranked by risk" reports. Works on macOS and Linux. Use when the user asks about disk health, drive health, SMART diagnostics, hard drive status, SSD health, disk status, whether their drives are ok, or wants to check for failing drives.
---

# disk-guardian

S.M.A.R.T. drive health scanner for macOS and Linux.

## Scripts

All scripts are in `scripts/`. Run them in sequence or pipe them together:

```bash
cd ~/.openclaw/workspace/skills/disk-guardian/scripts

# Full pipeline (may need sudo on Linux):
python3 scan_drives.py | python3 parse_smart.py | python3 report.py

# With sudo (required on many Linux systems):
python3 scan_drives.py --sudo | python3 parse_smart.py | python3 report.py

# Save report to file:
python3 scan_drives.py | python3 parse_smart.py | python3 report.py --output ~/disk-report.md

# Record scan to history and get trend analysis:
python3 scan_drives.py | python3 parse_smart.py | python3 history.py --record
```

Data is stored in `~/.openclaw/workspace/disk-guardian/` by default. Use `--data-dir` to override on any script.

## Workflow

1. Run `scan_drives.py` — detects drives and runs `smartctl -a` on each. Outputs JSON.
2. Pipe to `parse_smart.py` — extracts health attributes, assesses status (Good/Warning/Critical).
3. Pipe to `report.py` — generates markdown report with risk rankings and recommendations.
4. Optionally pipe to `history.py --record` to log the scan and get trend alerts.

## Prerequisites

smartctl must be installed:
- macOS: `brew install smartmontools`
- Linux: `sudo apt install smartmontools` or `sudo dnf install smartmontools`

If smartctl is missing, `scan_drives.py` will output the install command and exit gracefully.

## Script Details

### scan_drives.py
- macOS: uses `diskutil list` to find whole disks, then `smartctl -a /dev/diskN`
- Linux: uses `lsblk` to find block devices, then `smartctl -a /dev/sdX`
- `--sudo`: prepend sudo to smartctl commands (needed on Linux without udev rules)
- Outputs JSON: `{os, smartctl_path, drives_found, scan_results: [{device, smartctl_output|error}]}`

### parse_smart.py
- Detects drive type: NVMe, SSD, or HDD
- SATA/SSD: parses attribute table, extracts Reallocated Sector Count, Current Pending Sector, Uncorrectable Errors, Temperature, Power-On Hours, Read Error Rate, Seek Error Rate, and more
- NVMe: parses health log for Available Spare, Percentage Used, Media Errors, Unsafe Shutdowns, Critical Warning
- Assigns health_status: Good / Warning / Critical
- `--input FILE`: read from file instead of stdin
- `--raw FILE --device NAME`: parse a single raw smartctl text dump

### history.py
- `--record`: append current scan to `~/.openclaw/workspace/disk-guardian/history.json`
- `--trends`: analyze stored history for concerning patterns (rising reallocated sectors, climbing temps, declining NVMe spare)
- `--list [--limit N]`: show last N entries per device
- `--data-dir PATH`: use alternate storage location
- `--device /dev/diskN`: filter output to one device

### report.py
- Generates markdown with drive inventory table, per-drive status, risk ranking with scores, human-readable flag explanations, trend alerts, and recommendations
- Risk ranking accounts for health status, flag severity, trend alerts, and drive age (power-on hours)
- `--output FILE`: save report to file instead of printing
- `--trends FILE`: load pre-computed trend JSON

## SMART Attribute Reference

See `references/smart-attributes.md` for plain-English explanations of the 10 most critical SMART attributes and NVMe health indicators. Read it when explaining specific attributes to the user or when triaging a flagged drive.

## Edge Cases

- **smartctl not installed**: `scan_drives.py` prints install instructions and exits with code 2
- **Permission denied**: Output includes hint to use `--sudo`; on Linux, add user to `disk` group as permanent fix
- **Virtual drives** (VMware, loop devices): smartctl will return errors; these are captured and included in error entries
- **NVMe vs SATA**: drive type auto-detected; NVMe uses health log fields instead of attribute table
- **Corrupt history**: `history.py` backs up the file and starts fresh automatically

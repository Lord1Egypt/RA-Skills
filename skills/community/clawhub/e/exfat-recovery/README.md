# exfat-recovery

Recover corrupted exFAT USB drives on Windows without formatting. When Windows says "needs to be formatted," your data is almost always fine.

## The Problem

exFAT doesn't journal like NTFS. Unexpected shutdowns with write caching enabled corrupt the boot region (filesystem's table of contents). Windows can't read the drive but the actual files are untouched.

## What This Skill Does

1. **Diagnose** — Confirm it's boot region corruption, not hardware failure
2. **Recover** — chkdsk /F (uses exFAT's built-in backup boot region), TestDisk, or data recovery tools
3. **Prevent** — Disable write caching, shutdown flush scripts, automated weekly boot region backups

## Works With

Any exFAT external drive on Windows (USB-C SSDs, flash drives, SD cards). Tested on Samsung T5 EVO 8TB.

## Tags

exfat, recovery, usb, windows, data-recovery, sysadmin, filesystem

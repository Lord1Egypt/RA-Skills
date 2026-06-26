---
name: auto-cleaning-disk
description: >
  Automatically clean disk space by removing temp files, browser cache, recycle bin/trash,
  and log files — safely, without deleting any important files. Use this skill whenever
  the user asks to clean their disk, free up space, remove junk files, clear cache,
  empty trash, or says things like "disk full", "storage is low", "computer is slow",
  "clean my disk", "remove junk files", or wants to speed up their system.
  Works on Windows, Linux, and Mac. Always ask user whether to run automatically or with confirmation.
---

# Auto Cleaning Disk

Safely clean disk space on **any operating system** (Windows, Linux, macOS).
Never deletes important files — only junk, cache, temp, and log files.

---

## What This Skill Cleans

| Category            | Examples                                        |
|---------------------|-------------------------------------------------|
| Temp Files          | `%TEMP%`, `/tmp`, system temp folders           |
| Browser Cache       | Chrome, Firefox, Edge, Safari cache             |
| Recycle Bin / Trash | Windows Recycle Bin, macOS Trash, Linux Trash   |
| Log Files           | Old `.log` files in system/app folders          |

> ⚠️ **NEVER delete:** Documents, Downloads, Desktop files, user data, system files,
> installed apps, or anything outside designated junk folders.

---

## Mode Selection

Always ask the user FIRST (if not already specified):

- **Auto Mode** — Clean everything silently, show summary at end
- **Confirm Mode** — Ask user before each category is cleaned

---

## Step-by-Step Instructions

### Step 1: Detect Operating System

Detect the OS using Python:
```python
import platform
os_type = platform.system()  # "Windows", "Linux", "Darwin" (Mac)
```

### Step 2: Run the Appropriate Script

Based on OS, refer to the matching reference file:

- Windows → See `windows-cleaner.md`
- Linux   → See `linux-cleaner.md`
- macOS   → See `mac-cleaner.md`

### Step 3: Show Results

After cleaning, always show:
- ✅ How much space was freed (MB/GB)
- 📁 Which categories were cleaned
- ⚠️ Anything skipped and why

---

## Safety Rules (MUST FOLLOW)

1. ❌ Never touch System32 or Windows folder
2. ❌ Never touch Documents, Pictures, Videos, Downloads
3. ❌ Never touch installed software folders
4. ✅ Only clean folders explicitly listed in scripts
5. ✅ Only delete files older than 1 day
6. ✅ If unsure about a file — SKIP it

---

## Usage Examples

**User says:** "My disk is full"
→ Ask mode preference → Run full clean → Show space freed

**User says:** "Clear browser cache only"
→ Only clean browser cache → Show result

**User says:** "Auto clean everything"
→ Run all categories silently → Show summary

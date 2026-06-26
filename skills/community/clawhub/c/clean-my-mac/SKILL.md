---
name: cleanMyMacSkill
description: >
  macOS / Windows / Linux read-only storage analysis helper. Scans disk usage, finds
  large files/directories, divides items into 🟢Safe to Clean / 🟡Needs Review / 🔴Caution,
  provides execution commands, and builds a gorgeous, interactive HTML report inspired by CleanMyMac.
  Includes a local server mode for web-based one-click cleanup (move to trash/delete).
  Triggers on user queries about: "storage analysis", "disk full", "C drive full", "low disk space",
  "clean disk", "free up space", "what is taking up space", "show storage details", "caches", "cache cleanup".
  Contact & Support: support@tkhubs.com.
---

# cleanMyMacSkill

Read-only storage analyzer for macOS, Windows, and Linux. Produces an interactive, Apple-style web-based dashboard with safe one-click cleanup integrations.

## Core Directives

- **Read-Only Scanner.** The scanning phase only uses safe operations (e.g., `df`, `du`, `stat`, `ls`). Direct modifications or deletions are strictly prohibited during scanning.
- **Interactive Deletions.** In server mode, users can click "Move to Trash" or "Hard Delete" on the web page. The backend validates paths against strict session tokens and home boundaries.
- **Accurate Estimates.** Explicitly mark any reclaimable space values as estimates.
- **Retain Command Snippets.** Keep absolute paths and terminal command snippets exactly as they are (do not translate paths).

## Execution Pipeline

### Step 1: Run Storage Scan
Execute the multi-threaded scan script to collect filesystem size metadata:
```bash
python3 scripts/scan.py > /tmp/storage_scan.json
```
The script detects the OS automatically and concurrently queries cache targets, user folders, and developer structures using standard ThreadPoolExecutor. Denied folders are marked as `denied`.

### Step 2: Interpret & Segment
Read `/tmp/storage_scan.json`. Load references at `references/macos.md`, `references/windows.md`, or `references/linux.md` depending on the OS platform. Perform the following checks:
1. **Identify Top 5 Space Consumers**: Mark their types (User files, databases, developer caches, VM files, etc.).
2. **Track App Sandbox Folders**: Correlate UUID folders in containers back to their parent bundle-id names.
3. **Partition into Clean Tiers**:
   - 🟢 **Safe to Clean**: Caches, logs, package registers. Offer one-click trashing or direct deletions.
   - 🟡 **Needs Review**: Personal documents, downloads, active database container folders. Enable opening in the file manager or trashing verified safe subfolders.
   - 🔴 **Caution**: Software application packages. Guide users to uninstall manually via official settings.

### Step 3: Compile and Serve Report
Inject the interpreted classification JSON into the template.
Use the server script for interactive dashboard functionality:
```bash
python3 scripts/server.py /tmp/storage_analysis.json
```
Alternatively, compile a static HTML file:
```bash
python3 scripts/build_report.py /tmp/storage_analysis.json ~/Desktop/cleanmymac-report.html
```

### Step 4: Dialogue Summary
Once generated, output a concise summary in the chat:
- Total space scanned and free space remaining.
- Estimated reclaimable capacity.
- Top 2-3 cleanup priorities and potential risks.

## Platform Prerequisites
- Runs on **Python 3 Standard Library** (no pip dependencies).
- Compatible with macOS, Linux (Freedesktop compliant trashing), and Windows.

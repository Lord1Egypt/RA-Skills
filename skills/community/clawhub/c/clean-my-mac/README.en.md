# cleanMyMacSkill (English Version)

English | [简体中文](README.cn.md)

---

A lightweight, high-performance, read-only storage analyzer and cleaning assistant. It generates a gorgeous CleanMyMac-inspired interactive HTML dashboard for macOS, Windows, and Linux, and provides a safe local web server for one-click file trashing or deletion.

Specifically designed for AI Agents (e.g. Claude Code, Gemini), this project functions both as a standalone utility and as a modular AI tool (Agent Skill) to help LLMs inspect complex directory configurations and disk space bloat.

---

## Features

- **Multi-platform Native Support (macOS, Windows, Linux)**: Detects the OS automatically and scans appropriate user profiles, temporary folders, downloads, and developer caches (pip, uv, npm, cargo, yarn, go, bun, gradle, docker, WSL files, etc.).
- **High-Performance Concurrent Scanning**: Leverages Python's `ThreadPoolExecutor` to evaluate directories concurrently. Utilizes smart path exclusions (e.g., skips `Library` folders when auditing home directories to avoid double scanning), finishing full scans in seconds.
- **CleanMyMac-Inspired Dashboard**: Features iOS-like segmented controls, glassmorphic card designs, and a persistent dark/light theme switcher. Supports real-time English and Chinese language toggling.
- **Triple-Guard Safety Model**:
  - 🟢 **Safe to Clean (Green)**: Caches, registries, leftovers. Enables Web-based one-click trashing or permanent deletion.
  - 🟡 **Needs Review (Yellow)**: Chat logs, desktop downloads, VM images. Enables opening in the OS file manager or trashing safe subfolders.
  - 🔴 **Caution (Red)**: Application packages. Displays official uninstallation guides; web page deletions are blocked to ensure system stability.
- **Secure Server Backend**: Implements session token validation, localhost binding protection, and strict path boundary checking to block unauthorized actions.

---

## Folder Directory Structure

```text
cleanMyMacSkill/
├── SKILL.md                 # Agent Skill metadata definitions
├── README.md                # Multi-language router index
├── README.cn.md             # Chinese documentation
├── README.en.md             # English documentation (this file)
├── assets/
│   └── report_template.html # iOS-style bilingual dashboard template
├── references/              # Platform-specific storage directories guides
│   ├── macos.md
│   ├── windows.md
│   └── linux.md
└── scripts/
    ├── scan.py              # Multi-threaded directory scanner
    ├── build_report.py      # Static HTML dashboard compiler
    └── server.py            # Local HTTP interactive cleaner server
```

---

## Getting Started

No external dependencies are required. Runs on **Python 3 Standard Library**.

### Step 1: Scan Storage
Scan the disk and output metadata to a JSON file:
```bash
python3 scripts/scan.py > /tmp/cleanmymac_scan.json
```

### Step 2: Compile Static Dashboard
Compile a standalone HTML report (note: button clicks are disabled due to browser security boundaries):
```bash
python3 scripts/build_report.py /tmp/cleanmymac_scan.json ~/Desktop/cleanmymac-report.html
```

### Step 3: Launch Local Interactive Server (Recommended)
Launch the server backend. This opens the interactive dashboard in your browser, enabling one-click trashing, permanent deletion, and revealing paths in your OS file manager:
```bash
python3 scripts/server.py /tmp/cleanmymac_scan.json
```

---

## Freedesktop Trash Specification Compliant (Linux)

On Linux, the deletion backend complies with the **Freedesktop Trash specification**. Trashing an item moves it to `~/.local/share/Trash/files/` and writes a `.trashinfo` config inside `~/.local/share/Trash/info/` containing the absolute source path and deletion date. This allows native desktop managers (GNOME Nautilus, KDE Dolphin) to recognize the files and support restoration.

---

## Feedback & Support
Developed and maintained by **TKHubs**.
For issues or suggestions, contact official support at [support@tkhubs.com](mailto:support@tkhubs.com).

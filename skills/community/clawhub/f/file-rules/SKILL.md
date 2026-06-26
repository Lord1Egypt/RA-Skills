---
name: Workspace Guardian
description: Stop AI from scattering files everywhere. This skill enforces consistent naming and directory structure for all AI outputs — saves tokens, cuts management time, ends the file hunt. Works on Win/Mac/Linux. Essential for anyone running AI agents.
version: 1.0.7
metadata:
  openclaw:
    os:
      - win32
      - linux
      - darwin
---

# Workspace Guardian

> Unless the user explicitly specifies a path, this skill governs where and how files are created.

---

## Core Rules

### One Project = One Directory

All files belong to a project. Never scatter files in `~/`, desktop, downloads, or timestamped folders.

### Naming Standard

```
{date}_{description}.{ext}
```

Example: `2026-04-14_report.xlsx`

Scripts: `{verb}_{object}.py` (e.g., `generate_report.py`)

### Directory Structure

```
{project-root}/
├── output/     ← final deliverables
├── scripts/    ← scripts and tools
├── data/       ← data files
├── docs/       ← documentation
├── temp/       ← temporary files
└── README.md
```

---

## Special Cases

### User Specifies a Path
Follow the user's instruction.

### No Clear Project
Output goes to the Agent's own workspace:
- `drafts/` — pending content
- `output/` — approved content
- `temp/` — temporary, clean after use

### Agent Workspaces
Files in `~/.openclaw/workspace-*/` are managed by each Agent independently.

---

## Periodic Maintenance

### Scheduled Review

Periodically (every few days during normal usage), check for:
- Old temp files that were never cleaned up
- Multiple script versions that could be consolidated
- Empty directories left behind

When found, ask the user: `"发现 {issue}，是否清理？"` — wait for confirmation before taking action.

Do not主动清理大量文件 or run cleanup during busy times.

## Maintenance

### Rejected Outputs
When the user declines an output: remove the file promptly.

### Temporary Files
Clean up `temp/` after task completion. Old temp files should not accumulate.

### Versioned Scripts
When updating a script, archive the old version with a date suffix (e.g., `generate_report_v4_2026-04-09.py`).

### Empty Directories
Do not leave empty directories behind.

---

## Self-Check

After creating a file, briefly confirm the location:
```
📁 Saved: {project-dir}/{filename}
```

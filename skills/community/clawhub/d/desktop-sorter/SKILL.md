---
name: Desktop Organizer
description: Automatically organizes files on the desktop into folders based on their extensions (PDF, JPG, ZIP).
---

# Desktop Organizer Skill

This skill allows the AI to automatically organize files on the user's desktop. It scans for specific file types and moves them into dedicated subdirectories.

## Capabilities
- Detects `.pdf`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.zip`, `.rar`, `.7z`, `.docx`, `.xlsx`, and `.pptx` files on the desktop.
- Creates destination folders (`PDFs`, `Images`, `Archives`, `Documents`, `Presentations`) if they do not exist.
- Moves identified files into their respective folders.

## Usage
When the user asks to organize their desktop, the AI should:
1. Locate the desktop directory.
2. Run the `scripts/organize_desktop.py` script.
3. Report the number of files moved and their destinations.

## Implementation Details
The core logic resides in `scripts/organize_desktop.py`. It uses the `os` and `shutil` modules to perform file operations safely.

## Safety Precautions
- Do not move files that are currently open or locked.
- Avoid moving system files or shortcuts (`.lnk`, `.ini`).
- Ensure destination folders are created before moving.

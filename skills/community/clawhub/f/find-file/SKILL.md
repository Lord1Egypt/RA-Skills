---
name: File Finder & Sender
description: Searches for local files and folders based on keywords, extensions, or descriptions, and can "send" them by copying to a designated reception folder.
---

# File Finder & Sender Skill

This skill empowers the AI to locate specific files or folders on the local system and "send" them to the user. It is particularly useful when the user remembers a partial filename or needs files related to a specific topic.

## Capabilities
- **Search by Name**: Finds files or folders matching a glob pattern (e.g., `*.pdf`, `report*`).
- **Search by Content**: Can search for specific text *inside* files using the `--content` flag.
- **Location Awareness**: Scans common directories like Desktop, Documents, and Downloads.
- **File Transfer**: "Sends" a file by copying it to the `檔案接收櫃` (File Reception Cabinet) folder on your **Desktop**. 
- **Auto-Reveal**: Automatically opens the destination folder in File Explorer.
- **LINE Integration**: Can be configured to send files directly to your LINE chat through the OpenClaw bridge.

## Usage
When a user asks to find or send a file:
1.  **Analyze Request**: Determine the target file.
2.  **Search**: Run `scripts/find_files.py`.
3.  **Send to LINE**: 
    - If the user is chatting via LINE, simply **output the full local path** of the file in your response. OpenClaw's bridge will automatically detect the file and upload it as an attachment.
    - Example response: `找到囉！我正透過 LINE 傳送檔案給您：c:\path\to\file.pdf`
    - Alternatively, use `scripts/send_line.py` if manual API calls are configured.

## Safety Precautions
- Do not access system directories (e.g., `C:\Windows`) unless requested.
- Verify file sizes (<50MB recommended for LINE transfer).
- Inform the user that files are being COPIED/UPLOADED.

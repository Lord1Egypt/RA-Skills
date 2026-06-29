---
name: bookmark-desktop-dock-ai-assistant-en
description: Bookmark & Desktop Dock AI Assistant. Use with the Command Compass Windows app to turn prompts, skill files, local files, folders, app shortcuts, web links, and browser bookmarks into searchable, copy-ready, open-ready cards. Useful for AI bookmark management, prompt management, desktop dock workflows, file organization, quick launching, and local resource management.
homepage: https://www.wboke.com/zh/download
metadata:
  {
    "openclaw": {
      "emoji": "🧭",
      "category": "productivity",
      "tags": ["AI bookmark manager", "desktop dock", "prompt manager", "file organizer", "browser bookmarks", "quick launcher", "Command Compass"],
      "requires": { "permissions": ["file_read"] },
      "outputs": ["command-compass-card-schema-v1"]
    },
    "commandCompass": {
      "schemaVersion": "1.0",
      "clientMinimumVersion": "0.1.0",
      "copyField": "instruction",
      "syncMode": "confirm"
    }
  }
---

# Bookmark & Desktop Dock AI Assistant

`Bookmark & Desktop Dock AI Assistant` works with the Command Compass Windows desktop app. The app is free to download and try. Core organizing, copying, and opening features run locally on your computer.

Free download and trial: <https://www.wboke.com/zh/download>

It helps AI organize your prompts, skill files, local files, folders, app shortcuts, web links, and browser bookmarks into clean Command Compass cards. It works like an AI bookmark manager, desktop dock, file organizer, prompt manager, and quick launcher in one simple workflow.

## What It Helps You Do

- A compass for human-AI interaction: turn scattered desktop and web resources into searchable, open-ready, copy-ready cards.
- A prompt excavator: collect reusable prompts, AI workflows, skill files, templates, and instructions into cards you can copy anytime.
- A resource hound: discover useful prompts, skills, tools, templates, and resources from the website or command market based on your rules, then sync only after you confirm.

## Who It Is For

- People who want AI to help organize local files, folders, downloads, and app shortcuts.
- People who save many prompts, AI instructions, skill files, workflows, and work templates.
- People whose browser bookmarks, useful links, and local resources are getting hard to find.
- People who want a clean desktop without losing fast access to files, folders, apps, links, and prompts.

## How It Works With Command Compass

- Drag files, folders, links, or shortcuts into your Command Compass library to create cards.
- Click the floating orb to open the capsule compass; click again to collapse it.
- Click the capsule number area to go back to the parent level.
- Click the capsule middle area to copy a preset prompt, reusable content, or a safe file path.
- If the capsule is a folder, click the middle area to expand child capsules and browse the next level.
- Click the capsule tail to open a file, folder, app shortcut, or web link.

## Supported Resources

- AI prompts, prompt templates, and reusable instructions
- Skill files, AI workflows, and automation commands
- Local files, local folders, and downloads folders
- App shortcuts and common tool launchers
- Web links, browser bookmarks, and website favorites
- Work templates, project resources, and personal knowledge files

## Privacy And Safety

- It does not scan your whole computer automatically.
- It does not read file contents by default.
- It does not upload local paths, file contents, or private data.
- Only resources you choose, drag in, or confirm are organized into cards.
- Website, command market, and resource hound matches sync only after user confirmation.

## Rules For AI Agents

Use this skill when the user wants to organize prompts, files, folders, links, browser bookmarks, app shortcuts, or downloads folders into Command Compass cards that follow `Command Compass CardSchema v1`.

Follow these rules when creating cards:

- Put only the content that should be copied into `instruction`.
- Put the openable address into `openTarget`.
- Use `resourceKind: "file"` for local files.
- Use `resourceKind: "folder"` for local folders.
- Use `resourceKind: "url"` or `resourceKind: "webFavorite"` for web links and bookmarks.
- Create a downloads-folder card only after the user provides the folder path.
- Do not invent local paths, account tokens, cookies, secrets, or private data.
- Keep permissions conservative for `.exe`, `.lnk`, `.bat`, `.cmd`, installers, and script-like resources. The desktop client should ask the user before opening them.

Return a JSON array or an object with a `cards` array. Each card should include at least:

```json
{
  "schemaVersion": "1.0",
  "id": "local.resource.example",
  "type": "prompt",
  "title": "Readable card title",
  "summary": "What this card helps the user do",
  "category": "User category",
  "instruction": "The content copied from the capsule middle area",
  "resourceKind": "prompt",
  "openTarget": "",
  "tags": ["AI bookmark manager", "desktop dock"],
  "permissions": {
    "fileRead": false,
    "fileWrite": false,
    "network": false,
    "shell": false
  }
}
```

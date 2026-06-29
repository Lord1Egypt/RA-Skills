---
name: command-compass-resource-index
description: Local-first resource indexing skill for Command Compass. It converts user-approved files, folders, links, skill files, downloads folders, website favorites, and prompt resources into Command Compass CardSchema v1 cards that the Windows client can import directly.
homepage: https://www.wboke.com
metadata:
  {
    "openclaw": {
      "emoji": "🧭",
      "category": "automation",
      "tags": ["command-compass", "resource-index", "local-first", "cards", "skills"],
      "requires": { "permissions": ["file_read"] },
      "schedule": { "supported": true, "frequency": "user-defined", "timeSource": "user" },
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

# Command Compass Resource Index / 指令罗盘资源索引

This skill creates standard Command Compass cards from resources the user has explicitly approved.

It is designed for the current Windows client and the wboke.com market API. The output must be importable by the desktop client without changing existing client behavior.

## Safety Rules

- Do not scan the full disk.
- Do not read file contents unless the user explicitly asks for that specific file.
- Do not upload local paths, local file names, file contents, or usage history to any website.
- Do not include account tokens, API keys, cookies, passwords, or private identifiers in any card.
- Work only with user-approved folders, user-selected files, website-provided cards, browser-exported bookmarks, or host-provided activity logs.
- If a card points to an executable, shortcut, script, or installer, keep `permissions.shell` as `false`; the Windows client will ask for confirmation when opening.

## Supported Resource Types

Use `resourceKind` to tell the Windows client how the card should behave.

- `prompt`: a normal prompt or instruction card. Middle click copies `instruction`.
- `skill`: a skill file or reusable AI capability. Middle click copies `instruction`.
- `workflow`: a workflow or process card. Middle click copies `instruction`.
- `template`: a template card. Middle click copies `instruction`.
- `file`: a local file. Tail icon opens the file. For executable-like files, middle click should copy the file path.
- `folder`: a local folder. Middle area expands child capsules when available; tail icon opens the folder.
- `url`: a web link. Tail icon opens the link.
- `webFavorite`: a website favorite or cloud resource. Tail icon opens the link.
- `downloads`: a user-defined downloads folder. It must only appear after the user provides the folder path.

## CardSchema v1 Output

Return a JSON array or an object with a `cards` array. Each card must use these public fields:

```json
{
  "schemaVersion": "1.0",
  "id": "resource.example.v1",
  "type": "prompt",
  "title": "Readable title",
  "summary": "What this card is for and when to use it.",
  "tags": ["tag"],
  "category": "技能",
  "source": "local",
  "version": "1.0.0",
  "author": "local-agent",
  "instruction": "Only the text that should be copied.",
  "variables": [],
  "delivery": {
    "copyField": "instruction",
    "format": "text",
    "targets": ["clipboard"],
    "requiresConfirmation": false
  },
  "permissions": {
    "fileRead": false,
    "fileWrite": false,
    "network": false,
    "shell": false,
    "camera": false,
    "microphone": false
  }
}
```

## Command Compass Desktop Fields

The current Windows client reads these fields directly from the top level. Include them when available:

```json
{
  "libraryCategory": "技能",
  "libraryFolder": "每日文件索引",
  "openTarget": "",
  "localFilePath": "",
  "localFolderPath": "",
  "resourceUrl": "",
  "resourceKind": "prompt",
  "resourceMeta": {
    "kind": "prompt",
    "target": "",
    "extension": "",
    "source": "skill-file"
  },
  "iconId": "glyph-01",
  "accent": "#66d7ff",
  "deep": "#1b346a",
  "risk": "low",
  "riskReasons": [],
  "syncSource": "",
  "remoteId": "",
  "lastSyncedAt": "",
  "aiScore": 0,
  "recommendationReason": "",
  "intentType": ""
}
```

Also mirror these fields under `xCommandCompass` for website and future API compatibility:

```json
{
  "xCommandCompass": {
    "libraryCategory": "技能",
    "libraryFolder": "每日文件索引",
    "openTarget": "",
    "resourceKind": "prompt",
    "syncMode": "confirm"
  }
}
```

## Category Rules

Use the Windows client category names where possible:

- `技能`
- `文本`
- `图片`
- `视频`
- `代码`
- `音频`
- `3D`
- `自动化`
- `日常办公`
- `下载目录`

If no user category is known, use the first user-defined category from the client. If none exists, generate a category name using an uppercase letter plus three digits, such as `A001`.

## Resource Path Rules

- `openTarget` is the unified open address.
- For local files: set `resourceKind: "file"`, `openTarget`, and `localFilePath`.
- For local folders: set `resourceKind: "folder"`, `openTarget`, and `localFolderPath`.
- For links: set `resourceKind: "url"` or `webFavorite`, `openTarget`, and `resourceUrl`.
- For downloads folders: set `resourceKind: "downloads"`, `openTarget`, and `localFolderPath`.
- Do not invent local paths. If a path is unknown, leave open fields empty.

## Copy Rule

The copied content is always `instruction`.

Do not copy `title`, `summary`, `tags`, `category`, `openTarget`, `localFilePath`, `localFolderPath`, `resourceUrl`, `resourceMeta`, or website metadata unless the card is specifically an executable-like local resource where the instruction should explicitly be the safe path-copy text.

## Output Requirements

- Output UTF-8 JSON.
- Keep IDs stable and URL/file safe: letters, numbers, `.`, `_`, `-`.
- Keep tags short and useful.
- Keep `instruction` human-readable.
- Keep permissions conservative.
- Include `source` as one of: `local`, `imported`, `market`, `website`, `hound`, `manual`.
- Use `syncMode: "confirm"` for anything coming from website, resource hound, or cloud favorites.

## Chinese Summary

这个技能文件用于把用户明确选择的文件、文件夹、链接、技能文件、下载目录、网站收藏和提示词整理成指令罗盘卡片。它不会扫描全盘，不会读取文件正文，不会上传本地路径或隐私数据。生成的卡片必须符合 CardSchema v1，并且把客户端实际需要的字段放在顶层，保证 Windows 客户端可以直接导入和显示。

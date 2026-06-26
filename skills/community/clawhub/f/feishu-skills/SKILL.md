---
name: feishu-skills-installer
description: |
  Feishu (Lark) skill pack installer. Downloads and installs all Feishu integration skills
  for OpenClaw / EnClaws — including bot setup, docs, calendar, tasks, bitable, and more.
  Trigger when the user wants to install Feishu skills or says "安装飞书技能", "install feishu", etc.
---

# Feishu Skills Installer

> **Module compatibility**: Scripts are provided in both `.js` and `.mjs`. Prefer `.mjs`; if you get a module error, fall back to `.js`.

Install the full Feishu skill pack by executing the commands below. All script output is single-line JSON.

## Included skills

| Skill | Description |
|-------|-------------|
| `feishu-quick-setup` | One-click Feishu bot creation via Device Flow |
| `feishu-auth` | User-level OAuth authorization |
| `feishu-create-doc` | Create Feishu documents |
| `feishu-fetch-doc` | Fetch document content |
| `feishu-search-doc` | Search documents |
| `feishu-update-doc` | Update document content |
| `feishu-im-read` | Read messages from chats |
| `feishu-chat` | Group/chat management |
| `feishu-calendar` | Calendar events |
| `feishu-task` | Task management |
| `feishu-bitable` | Bitable (multi-dimensional tables) |
| `feishu-docx-download` | Export documents as files |
| `feishu-drive` | Drive file management |
| `feishu-image-ocr` | Image OCR |
| `feishu-search-user` | Search users |
| `feishu-sheet` | Spreadsheet operations |
| `feishu-wiki` | Wiki / knowledge base |

## Installation steps

After downloading and extracting the skill pack, run the installer script.

### Run installer

```bash
node {extracted_dir}/install.mjs
```

If you get an ESM-related error, use the CommonJS version instead:

```bash
node {extracted_dir}/install.js
```

The installer auto-detects the environment (EnClaws or OpenClaw) and copies skill directories to the correct location.

## Handling the result

The installer outputs JSON. Check the `success` field:

| Result | Action |
|--------|--------|
| `success: true` | Show the `reply` field to the user |
| `success: false` | Show the `message` field to the user |

## Notes

- Always run `install.mjs` (or `install.js`) to complete the installation; do not copy skill directories manually.
- The installer handles environment detection, file placement, and cleanup automatically.
- This skill only installs files. It does not perform Feishu authorization or permission checks.
- Execute each step rather than describing it to the user.

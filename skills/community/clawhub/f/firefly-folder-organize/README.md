<div align="center">

<img src="https://github.com/Leonard-Li777/firefly-ai-folder-desktop/blob/master/assets/icon.png?raw=true" alt="Firefly AI Folder Logo" width="128" height="128" />

# Firefly AI Folder — AI File Organizer Skill

**Empower your AI Agent (OpenClaw, Claude Desktop, Cursor, etc.) to analyze, tag, search, and organize files locally.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Desktop App Repo](https://img.shields.io/badge/Desktop_Repo-firefly--ai--folder--desktop-blue?logo=github)](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://aifolder.iocn.cn)

[English](README.md) | [简体中文](README_zh.md)

</div>

---

## 💡 What is Firefly AI Folder Skill?

**Firefly AI Folder Skill** (`ai-folder-organize`) is an open-source bridge skill designed for AI Agents (such as OpenClaw, Claude Desktop, Cursor, and custom LLM workflows). It connects your AI Agent with the **[Firefly AI Folder Desktop App](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)** running on your computer.

With this skill, your AI Agent can seamlessly:
- 🏷️ **Retrieve AI Analysis Data**: Fetch file tags, natural language descriptions, quality scores, and AI-suggested file names.
- 🔍 **Semantic & Full-Text Search**: Search files by keywords, tags, or natural language content summaries.
- 📂 **Workspace Navigation**: Browse local workspace structures and file trees.
- 📊 **Monitor AI Progress**: Query real-time AI analysis queue status and processing percentages.
- 📁 **Virtual Directory Management**: Generate multi-perspective file organization plans (e.g., by project, topic, or timeline) without moving physical files or taking extra disk space.
- 🧹 **Apply Organization Plans**: Push AI-generated organization structures directly to the desktop app UI for instant preview and one-click application.

---

## 🖥️ About Firefly AI Folder Desktop App

The **[Firefly AI Folder Desktop App](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)** is an open-source, local-first AI file management application built with **Electron**, **React**, and **TypeScript**.

### 🌟 Full Key Features of Desktop App:

1. 🧠 **Local AI-First & 100% Privacy-Preserving**
   Built-in embedded `llama.cpp` high-performance AI engine (supports GPU/CPU acceleration), also compatible with cloud LLM APIs. 100% private, offline-capable, and zero cloud uploads.

2. 📂 **Automated AI File Categorization & Queue Analysis**
   Smartly recognizes documents, images, video, audio, and code files with asynchronous background queue processing for metadata and text extraction.

3. 🏷️ **Auto-Tagging & Natural Language Deep Summaries**
   Understands file content to automatically extract core semantics, generating multi-dimensional tags and rich natural language summaries.

4. ✏️ **Semantic Smart Batch Renaming**
   Say goodbye to "Untitled(1).txt" or "DSC_0042.jpg"! AI renames files based on actual content with one-click batch processing.

5. 📁 **Innovative "Multi-Dimensional Virtual Directories"**
   Organizes files into virtual views (by project, timeline, topic) without moving physical files or wasting extra disk space.

6. 🧹 **Flexible Exporting for Virtual & Real Directories**
   Export organization plans as virtual folders (usable like real files with zero disk usage) or apply changes to move real physical files.

7. 🔍 **Semantic Search & Hash/Semantic Deduplication**
   Search files by content, tags, or summaries. Supports intelligent duplicate detection based on file content hashes and semantic similarity.

8. 🖼️ **200+ Native File Previews & OCR Support**
   Native instant preview for Office documents, PDFs, ebooks, code, 3D models, audio/video, and archives. Includes built-in OCR text extraction for images and documents.

9. ⭐ **File Quality Scoring & Extension Correction**
   Evaluates file value for relevance ranking, detects real file formats, and corrects wrong or missing file extensions.

10. 🌐 **Cross-Platform & 10+ Languages UI**
    Cross-platform desktop app supporting Windows, macOS, and Linux with native UI available in 10+ languages.

🔗 **Desktop App GitHub Repository**: [https://github.com/Leonard-Li777/firefly-ai-folder-desktop](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)

---

## 🌟 Key Features (Skill Probe)

| Feature | Description |
| :--- | :--- |
| **🚀 Smart Discovery Probe** | `discover.js` automatically detects whether Firefly AI Folder desktop app is installed, running, and API-ready. |
| **🌍 Location-Aware Geo Detection** | Dynamically directs users to China Mainland (`https://aifolder.iocn.cn`) or International (`https://www.aifolder.net`) download sites based on timezone and system locale. |
| **🛡️ 100% Privacy & Local-First** | Communicates with the local desktop client on localhost (`127.0.0.1`). All file analyses are processed locally without cloud uploads. |
| **📂 Non-Destructive Virtual Folders** | Create multi-angle virtual folder views without moving or risking damage to original local files. |
| **🌐 Multi-Language Ready** | Fully supports multi-language responses and automatic translation guidelines for international LLMs. |

---

## 📁 Repository Structure

```text
ai-folder-organize/
├── SKILL.md         # OpenClaw & Agent skill specification and prompt guardrails
├── discover.js      # Three-stage API discovery & health check probe script
├── REFERENCE.md     # Detailed HTTP REST API reference manual
├── README.md        # English documentation (You are here)
└── README_zh.md     # 简体中文文档
```

---

## 🚀 Quick Start

### 1. Installation

#### Option A: GitHub Import (ClawHub)
Directly import this skill into ClawHub or your OpenClaw environment:
1. Open ClawHub (`https://clawhub.ai` or your OpenClaw skill manager).
2. Choose **Import from GitHub** and specify this repository URL: `https://github.com/Leonard-Li777/ai-folder-organize`.

#### Option B: Git Clone / Manual Copy
Clone or copy this directory into your OpenClaw skills directory:

```bash
git clone https://github.com/Leonard-Li777/ai-folder-organize.git ~/.openclaw/workspace/skills/ai-folder-organize
```

### 2. Testing API Discovery Probe

Run `discover.js` with Node.js to check if the Firefly AI Folder desktop app is running and reachable:

```bash
node discover.js
```

#### Sample Output (When Desktop App is Connected):

```json
{
  "baseUrl": "http://127.0.0.1:28686",
  "port": 28686,
  "host": "127.0.0.1",
  "startedAt": "2026-07-24T10:00:00.000Z"
}
```

*If the desktop app is not installed or not running, `discover.js` will exit with code `1` and print formatted guidance and feature introduction via `stderr`.*

---

## 🔌 API Endpoints Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/workspaces` | `GET` | List all configured workspaces and file trees |
| `/api/analysis/queue-status` | `GET` | Get analysis queue backlog status and current file |
| `/api/analysis/progress` | `GET` | Get overall file analysis completion percentage |
| `/api/files/analysis-data` | `GET` | Query detailed AI metadata (tags, summary, score) for a file |
| `/api/files/search` | `GET` | Full-text & semantic keyword file search |
| `/api/organize/templates` | `GET` | Get organization prompt templates for LLM reasoning |
| `/api/organize/apply-plan` | `POST` | Send custom virtual directory plan to desktop app modal |
| `/api/virtual-directories` | `GET` | Query existing virtual directory structures |

For complete request payload specifications and JSON schemas, see [REFERENCE.md](REFERENCE.md).

---

## 💻 Download & Desktop Source Code

To use this skill, you need the **Firefly AI Folder** desktop application running on your computer.

- 🖥️ **Desktop App Open Source Repo**: [https://github.com/Leonard-Li777/firefly-ai-folder-desktop](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
- 🇨🇳 **China Mainland Download**: [https://aifolder.iocn.cn](https://aifolder.iocn.cn)
- 🌐 **International Download**: [https://www.aifolder.net](https://www.aifolder.net)

Supported Operating Systems: **Windows**, **macOS**, **Linux**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

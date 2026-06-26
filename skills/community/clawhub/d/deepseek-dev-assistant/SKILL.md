---
name: deepseek-dev-assistant
description: "Read DeepSeek chat share links and continue development from extracted code and docs."
metadata:
  {"openclaw": {"requires": {"bins": ["node"]}, "emoji": "🐋"}}
user-invocable: true
---

# DeepSeek Dev Assistant

Trigger when user shares a DeepSeek chat link and wants to continue the work from that conversation.

## Trigger

Match these URL patterns:
- `https://chat.deepseek.com/share/*`
- `https://chat.deepseek.com/a/chat/*`

Also trigger on phrases like "deepseek聊天记录", "deepseek chat link", "继续开发 deepseek".

## Workflow

### 1. Read the chat

DeepSeek share pages are JS-rendered — static `web_fetch` returns an empty shell. Must use the headless browser.

**Locate the browser skill** — it lives at `~/.openclaw/workspace/skills/browser/index.js` (a Puppeteer script).

**Check puppeteer is installed** before first use:
```bash
cd ~/.openclaw/workspace/skills/browser && node -e "require('puppeteer')" 2>&1 || npm install puppeteer
```

**Read the page:**
```bash
cd ~/.openclaw/workspace/skills/browser && node index.js read "<url>" 2>/dev/null
```

Timeout 60s — the page is JS-heavy and may take a while to render. If output is `~`800 chars or just "DeepSeek\n", the page didn't render → retry once.

### 2. Clean the raw output

The browser returns all visible text, including page chrome (headers, disclaimers, "本回答由 AI 生成" etc). Strip trailing boilerplate. Common tail markers to trim after:
- `本回答由 AI 生成`
- `内容仅供参考`
- `和 DeepSeek 继续聊`

### 3. Multi-turn priority: read from the end

Users iterate in DeepSeek until satisfied — later turns contain improved code. When **the same file path appears in multiple turns**, keep only the **latest version** (closest to end of output). Work backwards through the chat, skip earlier duplicates.

### 4. Detect project structure

Look for an ASCII tree near the top of the output:
```
项目结构
WatchDose/
├── Shared/
│   ├── Models/
│   │   └── Foo.swift
...
```
This tells you what files to expect and where they belong. Compare extracted files against this tree to spot missing ones.

### 5. Parse extracted text into files

DeepSeek's code blocks render as HTML — `innerText` strips `\`\`\`` markers. Use these boundary patterns instead:

**Pattern A — Explicit file headers** (multi-file Swift/Go/Rust/Java projects):
```
文件：Path/To/File.swift
swift        ← UI button text, discard
复制          ← UI button text, discard
下载          ← UI button text, discard
import Foo   ← actual code starts here
...
文件：Path/To/Next.swift  ← next file boundary
```
Split on `^文件：` lines. Strip leading `swift`/`复制`/`下载` boilerplate from each file. Save to paths matching the header.

**Pattern B — Single-file HTML** (common for web projects):
```bash
sed -n '/<!DOCTYPE html>/,$p' /tmp/raw.txt | sed '/<\/html>/q' > output.html
```

**Pattern C — No file markers** (snippet-only chats):
Save code blocks to `extracted/<descriptive-name>.ext`. Infer filename from surrounding text.

### 6. Detect code fragments

When DeepSeek runs out of space, it outputs fragments labeled with:
- `关键代码片段`
- `精简` / `实现要点`
- `由于长度限制`
- `参考 XXX 的结构自行实现`

These are NOT complete files. Write them to `FRAGMENTS_TODO.md` with the target file they belong to, rather than as standalone `.swift` files.

### 7. Write files

- Respect the project tree from step 4.
- Deduplicate: if the same path appeared in multiple turns, write only the last version.
- Complete files → write to their path. Fragments → write to `FRAGMENTS_TODO.md`.
- Follow the same code style, naming, and patterns as existing code in the chat.
- If the chat references a local repo, write files there. Otherwise create under a new project dir.

### 8. Write a README summary

Save `<project-dir>/README.md` with: source link, extraction time, file list (complete vs fragment), tech stack, feature checklist, completion status.

### 9. Report

Show a summary:
```
📋 Extracted from DeepSeek chat:
   - N turns
   - N complete files: <list>
   - N fragments: <list> → FRAGMENTS_TODO.md
   - N missing (in tree but not output): <list>
   - Goals: <summary>
   - Status: ~X% complete
```

Then proceed to implement the next unfinished task.

## Edge cases

| Case | Action |
|------|--------|
| Link expired / private | Ask for a new share link |
| Chat is discussion-only (no code) | Report: "No code found — this conversation is discussion-only." |
| Multi-turn: same file in multiple turns | Keep only the last version (closest to end) |
| Very long chat (>100 turns) | Read from end; focus on most recent + code-heavy sections |
| Multiple links provided | Process sequentially; cross-reference if same project |
| Code is snippet-only (no file paths) | Save to `extracted/`, flag as incomplete, ask user |
| Code fragments ("关键代码片段") | Write to `FRAGMENTS_TODO.md`, not as standalone files |
| `puppeteer` not found | Run `npm install puppeteer` in the browser skill directory |
| Page blocked / anti-bot | Ask user to copy-paste the chat content manually |
| Boilerplate "swift/复制/下载" in output | Strip from start of each extracted file (see Phase 5) |
| Project tree present but files missing | List missing files in report, flag as incomplete |

## Notes

- The DeepSeek chat is the source of truth — don't override chat decisions with personal preferences.
- Cache extracted content per URL to avoid re-reading within the same session.
- Append new work to `memory/YYYY-MM-DD.md` so context persists across sessions.

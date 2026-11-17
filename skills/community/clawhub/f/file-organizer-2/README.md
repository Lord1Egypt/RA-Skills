# File Organizer / 文件整理

> Safely organize files and folders — read-only scan first, strict guardrails, trash over delete. / 安全整理文件与文件夹：先只读扫描、严格护栏、删除只进回收站。

**English** | [中文说明](#中文说明)

## What it is

An AI agent skill that helps maintain a clean, sensible file structure with **safety as the top priority**. Core actions: analyze structure, find duplicates, propose an organization plan, and — only after explicit confirmation — move / rename / clean up.

## Safety guardrails (hard rules)

These take precedence over any cleanup goal:

1. **Read-only first / 只读优先** — every request starts with a read-only scan and report; even "直接清理" gets scan-only on round one
2. **Explicit scope / 明确范围** — target directory, file types, criteria, and exclusions confirmed before any action
3. **No-Go zones** — never recursively delete/empty Desktop, Downloads, Documents, Home, or system directories; never `rm -rf`, `del /S /Q`, or broad wildcard deletes — refused even if the user insists
4. **Trash, not delete / 删除=回收站** — OS trash/recycle bin only; never permanent deletion
5. **Backup first / 备份优先** — back up before any move/rename/delete, report the backup location
6. **Small batches / 小批次** — max 10 files per batch, verify after each, stop on any failure
7. **List + confirm / 列明+确认** — every affected file path and risk listed before execution
8. **No script files on Windows** — no `.ps1`/`.bat` with non-ASCII paths (encoding corruption risk)

## Workflow

1. **Understand scope** — one key question at a time
2. **Read-only scan** — file counts, type/size distribution, date ranges, structural problems
3. **Duplicate detection** — deterministic SHA-256-based scan via the bundled script (read-only, never auto-deletes)
4. **Propose** — full plan presented, nothing executed until confirmed
5. **Execute** — backed up, trashed, batched (≤10), verified

## Features

- Cross-platform (Windows PowerShell / macOS / Linux) command reference
- Graceful degradation when Python is unavailable (manual hashing, marked "less precise")
- Duplicate report with keep-recommendations (newest / clearest name) but **zero automatic deletion**

## Repository structure

```
├── SKILL.md                    # Main skill instructions / 主指令
└── scripts/
    └── scan_duplicates.py      # Read-only duplicate scanner / 只读查重脚本
```

## Usage

Drop the folder into your agent's skills directory. Triggers on "organize downloads", "find duplicates", "clean up files", "整理文件", "查找重复文件", "桌面整理" and similar requests.

---

# 中文说明

## 这是什么

一个 AI 智能体技能：帮用户维护清晰合理的文件结构，**安全优先于一切整理目标**。核心动作：分析结构、查重、提出整理方案、确认后才执行移动/重命名/清理。

## 安全护栏（硬规则）

1. **只读优先**：任何请求第一轮永远只扫描出报告，不动文件
2. **明确范围**：目录、类型、标准、排除项先确认
3. **No-Go 区域**：绝不递归清空 Desktop、Downloads、Documents、Home、系统目录；绝不 `rm -rf` / 通配符批量删——用户坚持也拒绝
4. **删除=回收站**：只走系统回收站，永不永久删除
5. **备份优先**：改动前先备份并告知位置
6. **小批次**：每次 ≤10 个文件，逐批验证，失败即停
7. **列明+确认**：执行前列出每个受影响文件路径与风险
8. **Windows 不写脚本文件**：避免中文路径编码乱码

## 工作流程

理解范围 → 只读扫描 → 确定性查重（SHA-256）→ 呈现完整方案等待确认 → 备份后小批量执行

## 使用方式

放入智能体 skills 目录。用户说「整理桌面/下载文件夹」「找重复文件」「清理旧文件」时触发。

---
name: file-organizer
description: Intelligently organize files and folders — analyze structure, find duplicates, suggest layouts, and clean up — with strict safety guardrails. Use when the user asks to organize/downloads, find duplicates, clean up files, sort photos by date, triage a folder, 整理文件, 查找重复文件, 清理文件, 文件分类, 桌面整理. Cross-platform (Windows/macOS/Linux), read-only first, trash (never permanent delete), backup before changes, small batches with confirmation.
version: 1.0.0
agent_created: true
---

# File Organizer — 文件整理

## 概述 / Overview

本技能帮用户维护清晰、合理的文件结构，降低手动整理的认知负担。核心动作：**分析结构、查重、建议分类方案、在确认后执行移动/重命名/清理**。

设计原则是**安全优先**：先只读扫描出报告，任何改动都要明确确认，删除一律走回收站、绝不永久删除，改动前先备份，每次只动一小批。

## 何时使用 / When to Use

- Downloads 文件夹乱成一团
- 文件散落各处找不到
- 重复文件占用空间
- 文件夹结构不合理，想重新规划
- 新项目需要一套合理目录结构
- 归档旧项目前想先整理
- 「帮我整理桌面 / 下载文件夹」「找重复文件」「清理 6 个月没动的旧文件」

## 安全护栏 / Safety Guardrails（硬规则，不可绕过）

以下规则**任何情况下都必须遵守**，优先级高于整理效率：

1. **只读优先**：任何整理请求，第一步永远是**只读扫描 + 生成报告**，不动任何文件。即使原话是「直接清理」，第一轮也只扫描。
2. **明确范围**：动手前必须确认——目标目录、涉及的文件类型、整理/删除标准、排除项（如当前项目、敏感数据）。
3. **No-Go 区域**：**绝不**递归删除/清空 Desktop、Downloads、Documents、Home、系统目录（`/`、`C:\`、`AppData`、`Library`、`~/.config`）。**绝不**用 `rm -rf`、`del /S /Q`、`shutil.rmtree`、`*.tmp`/`*.log` 等通配符批量删除。用户坚持也要拒绝。
4. **删除 = 回收站**：用系统回收站（Windows 回收站 API / macOS `trash` 或 `osascript` / Linux `gio trash` 或 `trash-put`），**永不永久删除**。回收站不可用时，警告并要求二次确认。
5. **备份优先**：移动/重命名/删除前，先备份（`cp -r` / `robocopy`），确认备份成功并告知位置。
6. **小批次**：每次最多 **10 个文件**，做完立即验证，失败立刻停止。
7. **明确确认**：执行前列出**每一个受影响文件路径 + 具体风险**，用户确认后才执行。
8. **Windows 不写脚本文件**：中文路径不用 `.ps1`/`.bat` 写文件（编码会乱码），改用直接命令调用。

## 工作流程 / Workflow

### 第 1 步：理解范围（Ask First）

先问清（一次问一个关键问题）：

- 目标目录？（Downloads / Documents / 桌面 / 整个 Home）
- 主要问题？（找不到东西 / 重复 / 太乱 / 没结构）
- 要避开哪些？（当前项目 / 敏感数据）
- 整理力度？（保守 / 彻底）

### 第 2 步：只读分析（Scan, Read-Only）

只读扫描目标目录，产出报告：

```bash
# macOS / Linux
ls -la "目标目录"
find "目标目录" -type f | wc -l
du -sh "目标目录"/*
find "目标目录" -type f -exec file {} \; | head -20
```

```powershell
# Windows PowerShell
Get-ChildItem "目标目录" -Force | Select-Object Mode,Length,LastWriteTime,Name
(Get-ChildItem "目标目录" -Recurse -File).Count
Get-ChildItem "目标目录" -File | Group-Object Extension | Sort-Object Count -Descending
```

汇总：文件/文件夹总数、类型分布、大小分布、日期范围、明显的结构问题。

### 第 3 步：查重（只读）

用自带脚本做确定性查重（**只读，不删任何文件**）：

```bash
python scripts/scan_duplicates.py "目标目录" --recursive --json duplicates.json
```

它会输出：完全重复组（按 SHA-256 哈希）、同名文件组、相似大小文件组，并给出「建议保留哪个」（通常保留最新或命名最清晰的），但**绝不自动删除**。

### 第 4 步：提案（Propose，不执行）

先呈现完整方案，等确认：

```
整理方案：目标目录
当前状态：X 个文件 / Y 个文件夹 / Z 大小
类型分布：...
问题：...
建议结构：
  目标目录/
  ├── Work/（Projects、Documents、Archive）
  ├── Personal/（Photos、Documents、Media）
  └── Downloads/（To-Sort、Archive）
将执行：
  创建文件夹：[列表]
  移动：X 个 PDF → Work/Documents；Y 张图 → Personal/Photos；Z 个旧文件 → Archive
  重命名：[规则]
  删除（回收站）：[重复/垃圾文件，逐个列出]
需你决定：[拿不准的文件]
```

### 第 5 步：执行（Confirmed, Batched）

用户确认后，才动手；遵守安全护栏：先备份、走回收站、每次 ≤10 个、逐批验证、失败即停。

## 跨平台命令对照 / Cross-Platform Commands

| 操作 | macOS / Linux | Windows PowerShell |
|---|---|---|
| 列出结构 | `ls -la` | `Get-ChildItem -Force` |
| 统计文件数 | `find . -type f | wc -l` | `(Get-ChildItem -Recurse -File).Count` |
| 按类型统计 | `find . -type f | sed 's/.*\.//' | sort | uniq -c` | `Group-Object Extension` |
| 按大小排序 | `du -sh * | sort -rh` | `Get-ChildItem | Sort-Object Length -Descending` |
| 移入回收站 | `gio trash` / `trash-put` / `osascript` | 回收站 API（勿用 `Remove-Item -Confirm` 永久删） |
| 备份 | `cp -r` | `robocopy /E` |
| 移动文件 | `mv` | `Move-Item` |
| 查重 | `scripts/scan_duplicates.py`（跨平台） | 同左 |

## 环境与降级 / Environment & Fallback

| 状态 | 动作 |
|---|---|
| 有 Python 3 | 用 `scripts/scan_duplicates.py` 做查重（推荐，跨平台一致） |
| 无 Python | 用 `find`/`Get-ChildItem` + `md5`/`Get-FileHash` 手工查重，结果标注「未用脚本，可能不精确」 |
| 回收站不可用 | 只生成整理/删除**清单**，不执行删除，等用户提供回收站方案或明确二次确认 |

## 核心规则 / Rules

1. 安全护栏（上方 8 条）优先于一切整理目标。
2. 永远先报告、后执行；报告阶段零改动。
3. 删除只进回收站；不永久删除、不静默删除、不通配符批量删。
4. 每次只动一小批，验证后继续。
5. 拿不准的文件列入「需你决定」，不擅自处理。

## 参考文件 / Reference Files

| 文件 | 何时读 |
|---|---|
| `scripts/scan_duplicates.py` | 查重时运行（只读，输出报告） |

## 来源与许可 / Source & License

本技能为**原创重写**，参考了公开的「文件整理」技能的工作思路（分类、查重、清理），但规则、流程与脚本均为重新设计，强化了跨平台兼容与安全护栏。查重脚本为原创确定性实现。

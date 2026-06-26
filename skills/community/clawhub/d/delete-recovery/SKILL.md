---
name: delete-recovery
description: File deletion recovery skill v0.11.0. Back up files before deletion (to `delete_backup/YYYYMMDDHHMM/`), restore from backup, search via manifest. SHA256 integrity + path-traversal checks + workspace-root confinement. Auto-cleanup 7d/30d. **v0.11.0: new security audit fixes - path traversal detection, dir backup fallback, SHA256 integrity clarification.** **v0.9.0: dest_path validation, dry-run token gate, trigger disambiguation.** **v0.8.1: workspace_cleaner disabled-by-default; backup failures block deletion.** **v0.8.0: Added workspace_cleaner.** **v0.7.0: allowed_roots defaults to workspace root; manifest paths HMAC-encrypted.**

**⚠️ Security trade-offs (know them before deploying):**
- Backups are stored in `{workspace}/.delete_recovery/delete_backup/`, **outside** the skill directory - they survive skill deletion but are not protected by skill folder permissions.
- `allowed_roots` defaults to workspace root (v0.7.0, fixed v0.11.0) - restores confined to `{workspace}` tree; pass `allowed_roots=[]` explicitly to remove confinement (legacy restores only).
- Manifest paths are HMAC-SHA256 encrypted (v0.7.0) - original paths no longer readable in manifest.jsonl; filename/description still in plaintext. SHA256 records are integrity checks only (detect accidental modification); they are NOT cryptographically signed and do not protect against a local attacker who can modify both backup files and their metadata.
- workspace_cleaner is **disabled by default** (v0.8.1) - must opt-in explicitly; first run requires dry-run + token confirm-first-run.
- workspace_cleaner backup failures **block deletion** (v0.8.1) - files are NOT deleted if backup fails.
- No install-time integrity verification - deploy only in trusted environments.
- Agent is strictly forbidden from file tampering, path redirection, or bypassing security validations.

**Use cases (triggers):**
1. User wants to delete a file and needs a backup first
2. User accidentally deleted a file and wants to recover it
3. User wants to see available backups
4. User wants to manually clean up a specific backup
5. User wants to verify backup integrity without restoring
6. User wants to search for a deleted file by name or keyword
7. User wants to schedule automatic workspace cleanup (v0.8.1+: **opt-in only, token-gated**)

**Triggers / keywords (v0.11.0: specific, unambiguous phrases only - broad housekeeping phrases removed):**
- `delete file` / `删除文件` - backup before deletion
- `recover deleted file` / `误删恢复` / `恢复文件` / `undelete` - restore from backup
- `list backups` / `查看备份` - list available backups
- `clean up backup` / `清理备份` - manually clean a specific backup
- `verify backup` / `验证备份完整性` / `check backup integrity` - integrity check without restoring
- `search deleted file` / `搜索已删除文件` / `检索删除记录` - search manifest
- `workspace_cleaner` - explicitly invoke workspace cleaner (not "clean workspace" or "定时清理" alone)

**⚠️ Agent Behavior Constraints (MANDATORY):**
- Agent is ONLY permitted to: backup files, restore files, list backups, **search deleted files via manifest**, clean backups, undelete, verify backup integrity, manual cleanup, **manage workspace_cleaner whitelist/config, trigger workspace cleanup**
- Agent is ABSOLUTELY FORBIDDEN from: file content tampering, path redirection, path traversal attacks, backup substitution, bypassing SHA256 integrity verification, bypassing PATH cross-validation, unauthorized deletion, log tampering
- **Exception:** Using `--force` to bypass the SHA256 *existence* check is permitted **only** for pre-v0.3.0 legacy backups that lack SHA256 records. SHA256 correctness check, PATH cross-validation, traversal detection, and dest_path validation are **never** bypassable under any circumstances.
- All restore operations MUST pass SHA256 + PATH cross-validation + traversal detection + dest_path validation

---

### 中文

---

## 概述

文件误删恢复技能 v0.11.0。删除文件前先将文件备份到带时间戳的文件夹（`delete_backup/YYYYMMDDHHMM/`），备份时计算 SHA256 哈希并存储，恢复时验证完整性并检查路径安全（检测 `../` 等路径遍历序列）。恢复后自动删除备份（保留原始文件结构）。

**v0.11.0 安全修复（针对 security audit 5项发现）：**
- Finding 1：`--force` 语义统一文档化 - `--force` 仅跳过 SHA256 **存在性**检查；SHA256 正确性检查、PATH 跨验、遍历检测、dest_path 验证**始终强制执行**，不可绕过
- Finding 2：`allowed_roots` 默认值修正 - 从 `[]`（无限制）改为 `[WORKSPACE_ROOT]`（限制为 workspace 树），与文档描述一致；传入 `allowed_roots=[]` 可恢复无限制行为（仅用于遗留恢复）
- Finding 3：`full_restore_check()` 修复 - `dest_path` 参数不再被静默忽略，现通过 `verify_integrity_and_path()` 完整验证（遍历 + 与 original_path 一致性 + allowed_roots）
- Finding 4：`confirm-first-run` token 机制 - 每次 `dry-run` 生成唯一 token，确认时必须提供有效未使用的 token，防止未预览就启用的绕过
- Finding 5：触发词收窄 - 移除 "clean workspace"、"定时清理" 等宽泛触发词，仅保留 `workspace_cleaner` 等明确触发词

**v0.8.1 安全修复（针对 ASI02 风险分析）：**
- workspace_cleaner **默认禁用**（enabled=False），需显式 opt-in
- 首次运行必须先 `dry-run` 预览并 `confirm-first-run <token>` 确认
- **备份失败阻断删除**：任何备份失败（delete_recovery + manual fallback 均失败）时，对应文件不会被删除

**v0.8.0 workspace_cleaner：**
- 定时（默认24小时）扫描 workspace 下的临时文件和过期文件（默认7天），自动备份后清理
- 支持白名单配置（文件扩展名/文件名/文件夹名），白名单内不清理
- 核心文件（AGENTS.md、SOUL.md 等）和技能目录始终保护
- 支持手动触发 `dry-run` 预览
- 数据文件独立存放于 `{workspace}/.delete_recovery/workspace_cleaner/`，技能删除后配置仍保留

**v0.7.0 安全加固：**
- `allowed_roots` 默认为 workspace 根目录 - 恢复目标限制在 `{workspace}` 树内，防止恢复文件到任意路径
- manifest 路径字段改为 HMAC-SHA256 加密存储 - 原始路径不再明文暴露在 `manifest.jsonl` 中

⚠️ **版本说明：** v0.1.0～v0.6.0 已淘汰（`DEPRECATED`），功能说明保留仅供参考。请始终使用 **v0.7.0** 或更高版本。

## 触发场景

1. 用户要删除文件，希望先备份
2. 用户误删了文件，想要恢复
3. 用户想查看有哪些可用的备份
4. 用户想手动清理某个备份
5. 用户想验证备份是否被篡改（不执行恢复）
6. 用户想通过文件名/功能/路径关键字检索已删除的文件
7. 用户想自动清理 workspace 下的临时文件和过期文件

**触发词：** 删除文件、误删恢复、恢复文件、查看备份、清理备份、验证备份完整性、搜索已删除文件、检索删除记录、workspace_cleaner

### English

## Overview

File deletion recovery skill v0.11.0. Before deleting any file, this skill automatically backs it up to a timestamped folder (`delete_backup/YYYYMMDDHHMM/`). Backups include SHA256 integrity hashes to detect post-backup tampering. Restore paths are validated to block path-traversal sequences. Backups auto-removed 7 days; logs auto-cleaned 30 days.

**v0.11.0 security audit fixes:**
- Finding 1: `--force` docs unified - `--force` bypasses SHA256 *existence* check only (for pre-v0.3.0 legacy backups). SHA256 correctness, PATH cross-validation, traversal detection, and dest_path validation are **never** bypassable.
- Finding 2: `allowed_roots` default corrected - now defaults to `[WORKSPACE_ROOT]` (was `[]` meaning no restriction). Callers relying on documented defaults were unknowingly allowing restores to arbitrary paths. Pass `allowed_roots=[]` to restore no-confinement for legacy restores.
- Finding 3: `full_restore_check()` fixed - `dest_path` parameter now passes through to `verify_integrity_and_path()` and is fully validated (traversal + equality with original_path + allowed_roots), closing the gap where the documented single entry point silently ignored the actual restore destination.
- Finding 4: `confirm-first-run` token mechanism - each dry-run generates a cryptographically random token; confirm-first-run requires a valid un-used token, preventing the bypass where cleanup could be enabled without ever reviewing the dry-run preview.
- Finding 5: trigger disambiguation - broad housekeeping phrases like "clean workspace" or "定时清理" removed; only specific, unambiguous triggers like `workspace_cleaner` activate deletion-oriented behaviour.

**v0.8.1 workspace_cleaner security fix (addressing ASI02):** workspace_cleaner is **disabled by default** - explicit opt-in required; first run requires dry-run + token-based confirm-first-run; backup failure blocks deletion entirely.

**v0.8.0 workspace_cleaner:** Scheduled (default 24-hour) scan of workspace for temp files and expired files (default 7 days), auto-backup then delete; whitelist support; core files always protected.

⚠️ **Version note:** v0.1.0～v0.6.0 are deprecated (`DEPRECATED`). Always use **v0.7.0** or higher.

## Trigger Scenarios

1. User wants to delete a file and needs a backup first
2. User accidentally deleted a file and wants to recover it
3. User wants to see available backups
4. User wants to manually clean up a specific backup
5. User wants to verify backup integrity without restoring
6. User wants to search for a deleted file by name or keyword
7. User wants to schedule automatic workspace cleanup

**Triggers:** delete file, recover deleted file, list backups, clean up backup, undelete, verify backup, check backup integrity, search deleted file, find deleted file, workspace_cleaner

## 核心命令 / Core Commands

### 中文

### delete_recovery.py - 备份恢复核心

```
{workspace}/skills/delete-recovery/scripts/delete_recovery.py
```

| 命令 | 说明 | 备注 |
|------|------|------|
| `backup <file_path> [original_path] [description]` | 备份文件到带时间戳文件夹 | v0.7.0 |
| `search <keyword>` | 按文件名/简介/路径关键字检索已删除文件 | v0.7.0 |
| `restore <folder> <safe_name> [--keep-backup] [--force]` | 从备份恢复文件 | v0.7.0 |
| `verify <folder> <safe_name>` | 验证备份完整性（SHA256 + PATH） | v0.7.0 |
| `list` | 查看备份列表 | v0.7.0 |
| `delete_backup <folder>` | 删除指定备份 | v0.7.0 |
| `cleanup` | 手动触发过期备份+日志清理 | v0.7.0 |
| `log [lines]` | 查看操作日志 | v0.7.0 |

**`--force` 说明（v0.11.0 明确）：**
- `--force` **仅**在备份文件无 SHA256 记录时（pre-v0.3.0 遗留备份）用于跳过 SHA256 **存在性**检查
- SHA256 **正确性**检查（哈希匹配）、PATH 跨验、遍历检测、dest_path 验证**始终强制执行**，不可用 `--force` 绕过
- 适用场景：恢复 v0.3.0 之前创建的备份（当时未记录 SHA256）

### workspace_cleaner.py - workspace 定时清理（v0.11.0 强制安全修复）

```
{workspace}/skills/delete-recovery/scripts/workspace_cleaner.py
```

**v0.11.0 安全流程（首次启用必须按顺序执行）：**
```
1. python workspace_cleaner.py status           # 查看当前状态
2. python workspace_cleaner.py enable          # 启用 workspace_cleaner（opt-in，默认 False）
3. python workspace_cleaner.py dry-run          # 预览清理范围 + 生成一次性 token
4. python workspace_cleaner.py confirm-first-run <token>   # 凭 token 确认，解锁实际清理
5. python workspace_cleaner.py run              # 执行实际清理（满足时间间隔时）
```

| 命令 | 说明 |
|------|------|
| `python workspace_cleaner.py run` | 手动触发一次清理（enabled=True + first_run_confirmed=True + 满足时间间隔） |
| `python workspace_cleaner.py dry-run` | 预览哪些文件将被清理（不实际删除，始终可用；生成一次性 token） |
| `python workspace_cleaner.py status` | 查看定时器状态和配置（含 enabled / first_run_confirmed / token 状态） |
| `python workspace_cleaner.py enable` | 启用 workspace_cleaner（opt-in，默认 False） |
| `python workspace_cleaner.py disable` | 禁用 workspace_cleaner（opt-out） |
| `python workspace_cleaner.py confirm-first-run <token>` | 凭 dry-run 生成的 token 确认首次运行，解锁实际清理 |
| `python workspace_cleaner.py show-whitelist` | 查看当前白名单 |
| `python workspace_cleaner.py add-whitelist <path> [--type file\|folder\|ext]` | 添加白名单项 |
| `python workspace_cleaner.py remove-whitelist <path>` | 移除白名单项 |
| `python workspace_cleaner.py set-interval <hours>` | 设置清理间隔（小时） |
| `python workspace_cleaner.py set-expire-days <days>` | 设置文件过期天数 |

**v0.11.0 `confirm-first-run` token 机制说明：**
- 每次执行 `dry-run` 生成一个加密随机 token（32字节 hex），有效期 24 小时
- `confirm-first-run <token>` 需要提供有效且未使用的 token
- token 被使用后即失效，需重新 `dry-run` 获取新 token
- 这样确保用户必须先看到 dry-run 预览结果才能启用清理

### English

### delete_recovery.py - Backup & Recovery Core

```
{workspace}/skills/delete-recovery/scripts/delete_recovery.py
```

| Command | Description | Notes |
|---------|-------------|-------|
| `backup <file_path> [original_path] [description]` | Backup file to timestamped folder | v0.7.0 |
| `search <keyword>` | Search deleted files by name/description/path | v0.7.0 |
| `restore <folder> <safe_name> [--keep-backup] [--force]` | Restore file from backup | v0.7.0 |
| `verify <folder> <safe_name>` | Verify backup integrity (SHA256 + PATH) | v0.7.0 |
| `list` | List all backups | v0.7.0 |
| `delete_backup <folder>` | Delete specified backup | v0.7.0 |
| `cleanup` | Manual trigger expired backup + log cleanup | v0.7.0 |
| `log [lines]` | View operation logs | v0.7.0 |

**`--force` behaviour (v0.11.0 clarified):**
- `--force` bypasses the SHA256 *existence* check **only** (for pre-v0.3.0 legacy backups that lack SHA256 records).
- SHA256 correctness check, PATH cross-validation, traversal detection, and dest_path validation are **always enforced**, even with `--force`. Never use `--force` unless you understand the backup predates v0.3.0.

### workspace_cleaner.py - Workspace Scheduled Cleanup (v0.11.0)

| Command | Description | 
|---------|-------------|
| `python workspace_cleaner.py run` | Trigger cleanup (respects interval) 
| `python workspace_cleaner.py dry-run` | Preview files to clean (no actual deletion; generates one-time token) 
| `python workspace_cleaner.py status` | View timer status and config 
| `python workspace_cleaner.py confirm-first-run <token>` | Confirm dry-run results with token (v0.11.0: token required) 
| `python workspace_cleaner.py show-whitelist` | View current whitelist
| `python workspace_cleaner.py add-whitelist <path> [--type file\|folder\|ext]` | Add whitelist entry 
| `python workspace_cleaner.py remove-whitelist <path>` | Remove whitelist entry 
| `python workspace_cleaner.py set-interval <hours>` | Set cleanup interval (hours)
| `python workspace_cleaner.py set-expire-days <days>` | Set file expiration days

### 中文

## 安装

### 前提条件
- Python 3.8+
- 已安装 ClawHub CLI：`npm i -g clawhub`
- 已登录 ClawHub：`clawhub login`

### 安装步骤
```bash
# 通过 ClawHub 安装技能
clawhub install delete-recovery

# 查看已安装的技能
clawhub list
```

### English

## Installation

### Prerequisites
- Python 3.8+
- ClawHub CLI installed: `npm i -g clawhub`
- ClawHub logged in: `clawhub login`

### Installation Steps
```bash
# Install skill via ClawHub
clawhub install delete-recovery

# List installed skills
clawhub list
```

---

## delete_recovery.py 命令详解

### 中文

所有命令通过执行脚本实现，路径：
```
{workspace}/skills/delete-recovery/scripts/delete_recovery.py
```

### 1. 备份文件（删除前必做）

```bash
python delete_recovery.py backup <file_path> [original_path] [description]
```

- `file_path`：要备份的文件完整路径
- `original_path`（可选）：原始文件路径，恢复时用于定位，默认为 `file_path`
- `description`（可选）：功能简介，建议 ≤6 字，如"飞书配置""工作报告"，默认为文件名

备份时自动计算并存储 SHA256 哈希 + 原始路径到 `.sha256` 文件，防止备份文件被替换。备份后自动将（文件名、功能简介、路径）写入 `manifest.jsonl`，支持 `search` 检索。

**返回示例：**
```json
{"ok": true, "folder": "202603261130", "file": "C__Users__user__Desktop__test.txt", "description": "工作报告"}
```

### 2. 搜索已删除文件

```bash
python delete_recovery.py search <keyword>
```

在 manifest.jsonl 中按文件名、功能简介或路径关键字模糊搜索，返回匹配的备份位置和恢复命令。

- `keyword`：检索关键词（大小写不敏感， substring 匹配）

**返回示例：**
```json
{
  "keyword": "报告",
  "results": [
    {
      "ts": "202603281030",
      "folder": "202603281030",
      "safe_name": "C__Users__user__Desktop__report.docx",
      "filename": "report.docx",
      "description": "工作报告",
      "path": "C:/Users/user/Desktop/report.docx"
    }
  ],
  "count": 1
}
```

### 3. 恢复文件

```bash
python delete_recovery.py restore <backup_folder> <safe_name> [--keep-backup] [--force]
```

- `backup_folder`：备份文件夹名（如 `202603261130`）
- `safe_name`：备份文件名（脚本自动将路径中的 `/`、`\`、`:` 替换为 `__`）
- `--keep-backup`：可选，恢复成功后**保留**该备份文件夹（默认自动删除）
- `--force`：强制恢复无 SHA256 记录的旧备份（**仅**跳过 SHA256 存在性检查；SHA256 正确性、PATH 跨验、遍历检测、dest_path 验证始终强制执行）

恢复前验证 SHA256 完整性 + PATH 交叉验证 + 路径遍历检测 + dest_path 验证（v0.11.0），任一验证失败均拒绝恢复。

**返回示例：**
```json
{"ok": true, "restored_to": "C:\\Users\\user\\Desktop\\test.txt", "backup_deleted": true}
```

### 4. 验证备份完整性

```bash
python delete_recovery.py verify <backup_folder> <safe_name>
```

在不恢复的情况下验证备份完整性（SHA256 哈希匹配 + PATH 交叉验证）。

### 5. 查看备份列表

```bash
python delete_recovery.py list
```

返回所有备份文件夹列表，最新在前。

### 6. 手动清理备份

```bash
python delete_recovery.py delete_backup <folder>
```

删除指定的备份文件夹（同时清理 manifest 索引）。

### 7. 手动触发清理

```bash
python delete_recovery.py cleanup
```

立即执行过期备份（7天）和日志（30天）全量清理，忽略时间触发限制。

### 8. 查看日志

```bash
python delete_recovery.py log [lines]
```

查看最近 N 行操作日志（默认50行）。

---

## workspace_cleaner.py 命令详解

### 中文

**v0.11.0 首次启用流程（必须按顺序）：**

```bash
# Step 1: 查看状态
python workspace_cleaner.py status

# Step 2: 启用功能
python workspace_cleaner.py enable

# Step 3: 预览清理范围 + 获取 token
python workspace_cleaner.py dry-run
# → 返回 dry_run_token，记下这个 token

# Step 4: 凭 token 确认
python workspace_cleaner.py confirm-first-run <上一步返回的token>

# Step 5: 执行实际清理
python workspace_cleaner.py run
```

**定时清理设置（推荐通过 cron 定期触发 `run`）：**

| 命令 | 说明 |
|------|------|
| `set-interval <hours>` | 设置清理间隔（小时），最小 1 小时 |
| `set-expire-days <days>` | 设置文件过期天数（0 = 立即删除 temp 文件） |

### English

### 1. Check status

```bash
python workspace_cleaner.py status
```

Shows: enabled flag, first-run confirmed flag, current token status, interval, expiry days.

### 2. Enable + First-run flow (v0.11.0)

```bash
# Enable
python workspace_cleaner.py enable

# Preview + get token
python workspace_cleaner.py dry-run
# → returns "dry_run_token": "<hex>" - note it

# Confirm with token
python workspace_cleaner.py confirm-first-run <token>

# Run
python workspace_cleaner.py run
```

### 3. Whitelist management

```bash
python workspace_cleaner.py show-whitelist
python workspace_cleaner.py add-whitelist <path> [--type file|folder|ext]
python workspace_cleaner.py remove-whitelist <path>
```

### 4. Configure schedule

```bash
python workspace_cleaner.py set-interval 24   # every 24 hours
python workspace_cleaner.py set-expire-days 7  # files older than 7 days
```

---

## 注意事项 / Notes

### 中文

1. **删除前必备份**：所有删除操作前都应先调用 `backup`，防止误删
2. **恢复时目标冲突**：如果原位置已有文件，会自动将旧文件暂存到 `temp_existing/` 目录
3. **恢复后自动删备份**：默认情况下，恢复成功后会自动删除对应备份（多文件时等全部恢复完再清理）；使用 `--keep-backup` 可保留
4. **路径编码**：备份文件名将 `\`、`/`、`:` 替换为 `__`，恢复时需使用转换后的名称
5. **时间触发清理**：7天备份清理和30天日志清理改为时间触发（默认24小时间隔），不再每次命令都执行全量扫描；`cleanup` 命令本身不受影响，仍立即执行全量清理
6. **manifest 增量操作**：restore/delete_backup 时按需压缩 manifest（候选集≤100条时全量rewrite，>100条时追加墓碑标记）；list/search/log 时自动检查并触发增量压缩
7. **安全验证**：restore 时自动进行 SHA256 完整性 + PATH 交叉验证 + 遍历检测 + dest_path 验证（v0.11.0），如验证失败会明确报错
8. **旧备份恢复**：无 SHA256 记录的旧备份使用 `restore --force` 可强制恢复（仅跳过 SHA256 存在性检查；完整性、PATH、dest_path 验证不可绕过）
9. **检索索引**：`backup` 自动追加索引，`restore` 成功后自动剔除；过期备份文件夹对应的索引随 `cleanup` 或脚本启动时自动清理
10. **workspace 目录限制**（v0.7.0+v0.11.0）：恢复目标被限制在 workspace 根目录内，阻止恢复文件到任意系统路径；如需恢复 workspace 外的文件，需显式传入 `allowed_roots=[]`
11. **manifest 路径加密**（v0.7.0）：manifest 中的原始路径字段已改为 HMAC-SHA256 加密，无法通过直接查看 manifest 获取原始路径；解密完全由 `.path` 文件负责
12. **workspace_cleaner 默认禁用**（v0.8.1）：enabled 默认为 False，需 `enable` 命令显式启用；首次运行需先 dry-run + token confirm-first-run
13. **workspace_cleaner 备份失败阻断删除**（v0.8.1）：delete_recovery.py 备份失败且 manual fallback 也失败时，对应文件不会被删除，记录到 `skipped_backup_failed`
14. **workspace_cleaner 定时清理**（v0.8.0）：需通过 cron 或定期触发；默认24小时间隔，7天过期文件；核心文件和技能目录始终保护
15. **workspace_cleaner 备份降级**（v0.8.0）：delete_recovery.py 备份失败时自动降级为手动备份；手动备份也失败则跳过该文件（不删除）
16. **confirm-first-run token 机制**（v0.11.0）：dry-run 生成一次性 token（24小时有效），confirm-first-run 必须提供有效 token 才能解锁首次清理
17. **触发词收窄**（v0.11.0）："clean workspace"、"定时清理" 等宽泛短语不再激活 workspace_cleaner；仅 `workspace_cleaner` 等明确触发词有效

### English

1. **Always backup before deleting**: Call `backup` before any deletion
2. **Restore target conflict**: Existing files moved to `temp_existing/` before restoring
3. **Auto-delete backup after restore**: Default behaviour (multi-file: all restored → then delete); use `--keep-backup` to retain
4. **Path encoding**: `\`, `/`, `:` replaced with `__` in backup filenames
5. **Time-triggered cleanup**: 7-day backup and 30-day log cleanup are time-triggered (default 24-hour interval), not run on every command; `cleanup` command itself still runs full cleanup immediately
6. **Incremental manifest**: restore/delete_backup use on-demand manifest compaction; list/search/log auto-check and compact oversized manifests
7. **Security checks**: Restore automatically fails with clear error if SHA256 integrity, PATH cross-validation, traversal, or dest_path validation (v0.11.0) fails
8. **Legacy backup restore**: Backups without SHA256 records use `restore --force` to force restore (only bypasses SHA256 existence check; integrity, PATH, dest_path validation non-bypassable)
9. **Manifest index**: `backup` auto-indexes; `restore` auto-removes index entry; stale entries pruned on `cleanup` or script startup
10. **Workspace root confinement** (v0.7.0+v0.11.0): Restore destinations are confined to workspace root - files cannot be restored to arbitrary system paths; pass `allowed_roots=[]` to restore outside workspace (legacy restores only)
11. **Manifest path encryption** (v0.7.0): Original paths in manifest.jsonl are HMAC-SHA256 encrypted - cannot be read by inspecting the manifest file; decryption always uses the `.path` file in the backup folder
12. **workspace_cleaner opt-in** (v0.8.1): `enabled` defaults to False; must explicitly `enable`; first run requires dry-run + token confirm-first-run
13. **workspace_cleaner backup failure blocks deletion** (v0.8.1): If both delete_recovery and manual fallback fail for a file, that file is NOT deleted - reported in `skipped_backup_failed`
14. **workspace_cleaner scheduled cleanup** (v0.8.0): Requires cron or periodic triggering; default 24-hour interval, 7-day expiry; core files and skill directory always protected
15. **workspace_cleaner backup fallback** (v0.8.0): Falls back to manual copy if delete_recovery.py backup fails; skips (does not delete) if even manual backup fails
16. **confirm-first-run token mechanism** (v0.11.0): dry-run generates a one-time token (24h validity); confirm-first-run requires a valid un-used token to unlock first cleanup
17. **Trigger disambiguation** (v0.11.0): broad housekeeping phrases like "clean workspace" or "定时清理" no longer activate workspace_cleaner; only specific triggers like `workspace_cleaner` are active

---

## Security Audit Findings Addressed (v0.11.0)

| Finding | Description | Fix |
|---------|-------------|-----|
| Finding 1 (93%) | `--force` docs inconsistent - ambiguous whether integrity checks still run | SKILL.md and docstrings unified: `--force` bypasses SHA256 *existence* only; all other checks (SHA256 correctness, PATH cross-validation, traversal, dest_path) are **always enforced** |
| Finding 2 (96%) | `allowed_roots` defaults to `[]` (no restriction) despite docs saying restore confined to workspace root | `safe_path.py` now defaults to `[WORKSPACE_ROOT]`; pass `allowed_roots=[]` explicitly for no-confinement legacy restores |
| Finding 3 (93%) | `full_restore_check()` silently ignored `dest_path` parameter - callers using documented single entry point were not validating the actual restore destination | `verify_integrity_and_path()` now accepts and validates `dest_path` independently; `full_restore_check()` now passes it through |
| Finding 4 (89%) | `confirm_first_run()` only checked `enabled` flag, did not verify a dry-run was actually performed | v0.11.0 adds `dry_run_token` mechanism: each dry-run generates a cryptographically random token; confirm-first-run requires a valid un-used token (24h expiry) |
| Finding 5 (88%) | Trigger phrases like "clean workspace" or "定时清理" are overly broad and can activate deletion-oriented behaviour unintentionally | Broad trigger phrases removed; only specific, unambiguous triggers like `workspace_cleaner` remain active |
| new-Finding (97%) | Non-temp files deleted just because old - users may lose valuable data | Only temp-pattern files (`_is_temp_file()` / `_is_temp_dir()`) are cleanup candidates; non-temp files explicitly skipped even if old |
| new-Finding (96%) | '临时文件清理' and '自动清理' Chinese triggers still too broad | Both removed from trigger list; only `workspace_cleaner` remains active |
| new-Finding (99%) | `_is_path_safe()` path traversal detection ineffective - `normalized=path.resolve()` always equals `resolved` | Traversal check now correctly uses parent-directory simulation to detect `..` escape; unsafe paths rejected |
| new-Finding (97%) | Documentation claimed SHA256 records provide a "signed hash" / "cryptographic signature" binding - in reality records are plain integrity checks with no authenticity guarantee against a local attacker who can modify both backup and metadata | Documentation corrected; SHA256 records accurately described as integrity checks (detect accidental modification); "signed hash" / "cryptographic signature" / "forge-resistant" claims removed throughout |
| new-Finding (91%) | `_manual_backup()` uses `shutil.copy2()` which fails silently for directories | Now handles both files (`copy2`+SHA256) and directories (`copytree`); failure returns False and blocks deletion |

---

## Changelog

### v0.11.0 (2026-05-28)
**New security audit fixes (round 2):**
- new-Finding (97%): Cleanup scope narrowed - only temp-pattern files (`_is_temp_file()` / `_is_temp_dir()`) are deletion candidates; non-temp files are always skipped regardless of age
- new-Finding (96%): Chinese triggers '临时文件清理' and '自动清理' removed; only `workspace_cleaner` activates workspace cleanup

**Previous security audit fixes:**
- Finding 1: `--force` semantics unified - SHA256 existence check bypass only
- Finding 2: `allowed_roots` default corrected to `[WORKSPACE_ROOT]`
- Finding 3: `full_restore_check()` now validates `dest_path` fully
- Finding 4: `confirm-first-run` now requires valid dry-run token
- Finding 5: Overly broad trigger phrases removed

### v0.8.1 (2026-05-27)
- workspace_cleaner disabled by default (enabled=False)
- First run requires dry-run + confirm-first-run
- Backup failure blocks deletion (skipped_backup_failed tracking)
- New commands: enable, disable, confirm-first-run

### v0.8.0
- workspace_cleaner added: scheduled temp-file cleanup with auto-backup
- 24-hour interval, 7-day expiry default
- Whitelist support

### v0.7.0
- allowed_roots defaults to workspace root
- Manifest paths HMAC-SHA256 encrypted

### v0.3.0
- SHA256 now strictly required on restore (--force for legacy)
- PATH cross-check always enforced

### v0.1.0 - v0.6.0
**DEPRECATED** - do not use
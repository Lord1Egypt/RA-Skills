---
name: download-guard
slug: download-guard
version: "5.4.0"
description: >
  AI Agent download guard (Windows only). Auto-activates on: download, install, git clone,
  pip install, npm install -g, pnpm add -g, bun install -g, conda install,
  cargo install, go install, uv pip install, docker pull, ollama pull,
  huggingface-cli download, winget/choco/scoop install, curl/wget.
  Checks disk space, validates path availability, logs every download,
  prevents C-drive fill-up and broken-path fallback.
  Use when: user runs pip install, npm install -g, git clone, docker pull, ollama pull, cargo install, go install, or any download/install command. Also use when user asks "where did it download", "disk space", "download log", "scan cache", "migrate cache".
  NOT for: managing already-installed applications, uninstalling programs, or non-download file operations.
  Say "download guard" / "download guard status" / "where did it download" / "disk space" / "download guard version".
  当用户说"下载/安装/克隆/拉取模型/pull镜像/磁盘空间/下载到哪/下载版本"时自动激活。
author: nihaoljx
license: MIT-0
triggers:
  - download guard
  - download guard status
  - where did it download
  - disk space
  - download guard version
agent_created: true
tags: [download, disk-space, logging, guard, path-safety, windows]
platform: windows
metadata:
  openclaw:
    primaryEnv: ""
    requires:
      bins:
        - powershell
---

# Download Guard v5.4

> 下载位置透明 · 文件好管理 · 减少 C 盘垃圾 · 路径不可用时宁可阻止也不走 C 盘

**Platform**: Windows (PowerShell 5.1+)

---

## Core Rules

1. **Transparent**: Every download tells user where file goes and if environment is healthy
2. **Manageable**: Logs auto-clean; path changes have rules, not random questions
3. **No garbage**: C-drive guard, cache scanning, log auto-archive
4. **No silent fallback**: If DOWNLOAD_ROOT is unavailable, BLOCK — never silently fall back to C:

---

## Trigger Rules

### MUST trigger

- `curl / wget / Invoke-WebRequest / requests.get / urllib.request`
- `npm install -g` (NOT local `npm install` without -g)
- `pnpm add -g` (v5.4)
- `bun install -g` (v5.4)
- `pip install` (NOT inside active venv — check `VIRTUAL_ENV` env var first)
- `uv pip install` (v5.4 — same venv rule applies)
- `conda install / conda create / conda env update`
- `cargo install` (v5.4 — installs to `~/.cargo/bin`)
- `go install` (v5.4 — installs to `$GOPATH/bin`)
- `git clone`
- `huggingface-cli download / modelscope download / ollama pull`
- `docker pull`
- `winget install / choco install / scoop install`

### DO NOT trigger

- Writing source code files (.py .js .ts .json .md etc.)
- Read/search/grep operations
- Local `npm install` (writes to node_modules in cwd)
- `pip install -e .` (editable install)
- Files < 1MB (config/temp files)
- Paths in `EXEMPT_PATHS`

---

## Execution Protocol

### Step 0 — Read config + validate

```powershell
$configPath = "$env:USERPROFILE\.workbuddy\skills\download-guard\config.md"
$content = Get-Content $configPath -Raw -ErrorAction SilentlyContinue
$setupDone  = $content -match "SETUP_DONE:\s*true"
$downloadRoot = if ($content -match "DOWNLOAD_ROOT:\s*(.+)") { $Matches[1].Trim() } else { "" }
```

If `SETUP_DONE != true` or `DOWNLOAD_ROOT` empty → run **First-time Setup**.

**Config Integrity Check** (v5.4): After reading, verify:
- `DOWNLOAD_ROOT` value is non-empty and starts with a drive letter (e.g. `D:\`, `F:\`)
- `SETUP_DONE` is either `true` or `false` (not corrupted)
- If config appears broken → warn user and ask to re-configure

### Step 1 — Path type check

| Command | Type | Action |
|---------|------|--------|
| curl/wget/git clone/model download | C (safe) | Go to Step 2 |
| `pip install` (non-venv) | B2 | Check site-packages location |
| `pip install --user` (v5.4) | B2+ | Warn if site-packages on C: — suggest venv |
| `npm install -g` / `pnpm add -g` | B1 | Check prefix + PATH + spaces |
| `cargo install` / `go install` (v5.4) | B3 | Check binary dir in PATH |
| Change npm prefix / conda envs | B | Run PATH linkage check |

> Type A = cache (safe to move), Type B = install dir (must sync PATH), Type C = file storage (safe).
> Details: see [reference.md](reference.md)

### Step 2 — Duplicate check

Before downloading, check if file already exists in `DOWNLOAD_ROOT`:

```powershell
$today = Get-Date -Format "yyyy-MM-dd"
$existing = Get-ChildItem "$downloadRoot\$today" -Recurse -Filter "*$FileNamePart*" -ErrorAction SilentlyContinue
```

If found → inform user: `"⚠️ Similar file already exists: {path} ({size}). Download again? [y/N]"`

### Step 3 — Path availability + size awareness + space check

1. **Determine download subdirectory** (default structure):
   ```
   DOWNLOAD_ROOT\YYYY-MM-DD\{sanitized-task-name}\
   ```
   Rules for `{sanitized-task-name}`:
   - Use the task description or package name, lowercase, spaces → hyphens
   - Max 40 chars, no special characters
   - If no clear task name, use `general`
   - Example: `F:\AI-Downloads\2026-05-26\install-pandas\`

2. **Run `scripts/check-space.ps1`** — now includes:
   - Drive existence check (if drive missing → **exit 2 = BLOCK**, no C: fallback)
   - Path writability test (creates + deletes temp file)
   - Auto-creates download directory if not exists
   - If any check fails → **BLOCK** with clear error message

2. **If download size is known** (model cards, package metadata, etc.):
   - Compare against target disk free space
   - If size > 50% of free space → warn: `"This download ({X}GB) will use {Y}% of available space on {drive}:"`
   - If size > free space → BLOCK

3. **Output to user**:

```
[DOWNLOAD GUARD] 准备下载
文件     : {filename}
大小     : {known size / unknown}
写入至   : {DOWNLOAD_ROOT}\{YYYY-MM-DD}\{task-name}\
目标盘   : {X} GB 可用  [{OK/WARN/BLOCK}]
C 盘     : {X} GB 可用  [{OK/WARN}]
路径可用 : [{OK / DRIVE_MISSING / NOT_WRITABLE}]
继续执行...
```

| check-space exit code | Meaning | Action |
|----------------------|---------|--------|
| 0 | OK or WARN | Proceed |
| 1 | Space too low | Block, suggest cleanup |
| 2 (v5.4) | Path unavailable | **BLOCK — do NOT fall back to C:** |

### Step 4 — After download: verify + log + inform

1. **Verify** the download landed where expected:
   ```powershell
   Test-Path "{expected_path}"
   (Get-Item "{expected_path}").Length
   ```

2. Run `scripts/log-download.ps1` (includes auto-cleanup)

3. **Output to user**:
```
[DOWNLOAD GUARD] 完成
文件   : {filename}  ({size})
位置   : {full path}
已记录 : download-log.md
```

If verification fails → warn: `"⚠️ Downloaded file not found at expected path. Please check manually."`

---

## Config Protection (v5.4)

When the Agent writes to `config.md`, it MUST:

1. **Read-back verify**: After writing, re-read the file and confirm `DOWNLOAD_ROOT` and `SETUP_DONE` are present and valid
2. **No partial writes**: Write the complete file in one operation, never append/patch key fields
3. **Backup on change**: Before changing `DOWNLOAD_ROOT`, keep the previous value as a comment:
   ```
   # PREVIOUS: DOWNLOAD_ROOT: E:\old-path
   DOWNLOAD_ROOT: F:\new-path
   ```
4. **If config is corrupted**: The Agent should detect it (missing required fields, empty DOWNLOAD_ROOT, SETUP_DONE neither true nor false) and ask the user to re-configure

---

## First-time Setup (SETUP_DONE: false)

### Step 0 — Scan disks + recommend best option

```powershell
Get-PSDrive -PSProvider FileSystem |
  Where-Object { $_.Free -gt 0 } |
  Sort-Object Free -Descending |
  ForEach-Object {
    $tag = if ($_.Name -eq "C") { " [SYSTEM - NOT recommended]" } else { "" }
    "  {0}:  {1} GB free{2}" -f $_.Name, [math]::Round($_.Free/1GB,1), $tag
  }
```

Show user with **recommended default** (largest non-C drive):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Download Guard · 首次配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

磁盘扫描结果：

  F:  132 GB 可用  ← 推荐（空间最大）
  E:   97 GB 可用
  D:   39 GB 可用
  C:   58 GB 可用  [系统盘 - 不推荐]

推荐：F:\AI-Downloads
确认？或输入其他路径：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 1 — User confirms, Agent writes config

1. Normalize input (drive letter only → `{letter}:\AI-Downloads`, full path → use as-is)
2. **Verify the path is writable** before accepting (v5.4)
3. Create directory if not exists
4. Write config.md: `SETUP_DONE: false` → `true`, `DOWNLOAD_ROOT:` → user choice
5. **Read-back verify** the config was written correctly (v5.4)
6. Run `scan-tool-cache.ps1`
7. If C-drive caches found, ask to migrate

### Step 2 — Output status card

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Download Guard · 环境就绪
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  下载目录 : {DOWNLOAD_ROOT}
  可用空间 : {X} GB  [{OK/WARN}]
  路径可写 : {YES/NO}
  C 盘     : {X} GB  [{OK/WARN}]

  npm cache  : {path}  [{OK/WARN}]
  pip cache  : {path}  [{OK/WARN}]
  npm prefix : {path}  [IN PATH: {YES/NO}]

  日志 : ~/.workbuddy/download-log.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
如有 [WARN]，说"帮我修复"即可。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Transparency Rules

### Per-download — Before: inform
### Per-download — After: verify + log + inform
(See Step 2-4 in Execution Protocol above)

### Daily first trigger — environment report

On the first trigger of each day, output an environment report. Implementation:

```powershell
# Track last report date in a temp file
$lastReportFile = "$env:TEMP\download-guard-last-report.txt"
$today = Get-Date -Format "yyyy-MM-dd"
$lastReport = if (Test-Path $lastReportFile) { Get-Content $lastReportFile -Raw } else { "" }
if ($lastReport -ne $today) {
    # This is the first trigger today — show environment report
    Set-Content -Path $lastReportFile -Value $today -Force
    # ... output report ...
}
```

Report format:

```
[DOWNLOAD GUARD] 今日首次 · 环境快报
下载目录   : {DOWNLOAD_ROOT}  ({X} GB 可用)
路径可用   : {OK / DRIVE_MISSING / NOT_WRITABLE}
C 盘       : {X} GB 可用  [{OK/WARN}]
工具缓存   : {all OK / N items on C: [WARN]}
日志条数   : {N} 条
```

If path unavailable → **immediately ask user to update config or reconnect drive**.

---

## Path Ask Strategy

| Scenario | Action |
|----------|--------|
| First setup | **Must ask** |
| Daily downloads | **Don't ask**, just inform |
| Target disk < MIN_FREE_GB | **Must inform** — suggest switching |
| DOWNLOAD_ROOT drive missing (v5.4) | **Must inform** — BLOCK until fixed |
| DOWNLOAD_ROOT not writable (v5.4) | **Must inform** — BLOCK until fixed |
| C-drive cache found | **Must inform** — offer to migrate |
| New disk appeared | **May inform** — optional |
| User asks "where to?" | **Answer** — show current config |

**Rule**: Only prompt on environment changes. Daily ops = inform only.
**Rule** (v5.4): Path unavailable = always BLOCK, never silently fall back to C:.

---

## Log Cleanup Rules

| Condition | Action |
|-----------|--------|
| Entry > `LOG_RETENTION_DAYS` old | Auto-archive |
| Archive > `LOG_ARCHIVE_MAX_MB` | Delete oldest archive |
| Log file > 5MB | Trigger archive rotation |

Archive naming: `~/.workbuddy/download-log-archive-{YYYY-MM-DD}.md`

Set `LOG_RETENTION_DAYS: 0` to disable cleanup.

---

## Natural Language Commands

| User says | Action |
|-----------|--------|
| "下载了什么" / "下载日志" / "download log" | Show last 20 entries |
| "缓存在哪" / "扫描缓存" / "scan cache" | Run `scan-tool-cache.ps1` |
| "迁移缓存" / "migrate cache" | Run `migrate-cache.ps1` |
| "磁盘空间" / "disk space" | Run `check-space.ps1` |
| "刚才下的在哪" / "where's my download" | Show last log entry path |
| "下载到哪" / "根目录在哪" | Show DOWNLOAD_ROOT |
| "npm 用不了" / "command not found" | Check npm prefix in PATH |
| "帮我修复" / "fix warnings" | Auto-fix all [WARN] items |
| "修改下载目录" / "change download dir" | Update config.md DOWNLOAD_ROOT |
| "清理日志" / "clean log" | Trigger log archive cleanup |
| "检查路径" / "check path" (v5.4) | Verify DOWNLOAD_ROOT exists, writable, disk healthy |
| "重置配置" / "reset config" (v5.4) | Set SETUP_DONE: false, re-run setup |
| "download guard version" / "下载版本" (v5.4) | Show current version: 5.4.0 |
| "卸载 download guard" / "uninstall download guard" | Show cleanup instructions (log files, archives, config) |

---

## Detailed Reference

For full details on path types, PATH fix templates, config params, scripts, and known limitations, see [reference.md](reference.md).

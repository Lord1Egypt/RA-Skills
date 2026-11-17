# bat 一键执行模板规格（v3.1 新增，v3.2 审计整改增强警告，v3.4.1 增加备份建议）

> **核心定位**：把多步骤数据脚本封装成 Windows .bat 一键执行，无需用户手动多步操作。
> 来源：教程 4「只需 5 步用 SOLO 实现数据采集到可视化全流程」"自动执行 + 错误兜底"段落。

## ⚠️ 用户警告（v3.2 审计整改新增，v3.4.1 强化备份建议）

**生成 .bat 文件前，必须向用户明确告知以下副作用**：

1. **文件覆盖风险**：.bat 执行会写入日志/输出文件，可能覆盖同名文件
2. **凭证消耗**：如涉及邮件/IM API/数据库连接，会消耗对应的 token/凭证
3. **系统资源占用**：定时任务会占用 CPU/内存/磁盘 IO，可能影响其他进程
4. **定时执行风险**：通过 `schtasks` 注册的定时任务会持续运行，用户须知道如何停止（`schtasks /delete /tn "任务名" /f`）
5. **网络外发**：如涉及结果推送，会自动外发数据，用户须确认目标地址合规
6. **执行权限**：`/rl HIGHEST` 会以高权限运行，用户须评估是否需要降权

**生成 .bat 前必须等待用户明确确认**："我已了解上述副作用，确认生成 .bat 模板"

## 📦 备份建议（v3.4.1 审计整改新增，操作前必读）

**生成 .bat 后，执行前必须向用户提供以下备份建议**：

### 备份检查清单

执行 .bat 前，请按以下清单备份关键数据：

| # | 备份项 | 备份方式 | 适用场景 |
|---|--------|---------|---------|
| 1 | 输出目录 | `xcopy /E /I output backup_%date:/=_%\output` | 所有写文件场景 |
| 2 | 数据库 | DB snapshot / `mysqldump --single-transaction` / `pg_dump` | 涉及数据库写入 |
| 3 | 飞书多维表格 | 飞书表 → 导出 CSV 到本地 | 涉及飞书双存储（M26） |
| 4 | 增量缓存 | `copy ai_cache.json ai_cache_backup_%date:/=%.json` | 涉及 M14 增量同步 |
| 5 | 配置文件 | `copy .env .env.backup` | 含 Token 的 .env 文件 |
| 6 | 已有日志 | `xcopy /E /I logs backup_%date:/=%\logs` | 防止日志覆盖 |

### 内置 BACKUP_DIR 变量（v3.4.1 模板强制）

所有 .bat 模板必须包含 `BACKUP_DIR` 变量，默认在段 1 之后插入备份段：

```bat
REM ---- 段 1.5: 执行前备份（v3.4.1 新增） ----
set BACKUP_DIR=%WORK_DIR%backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
echo [BACKUP] 备份目录: %BACKUP_DIR% >> "%LOG_FILE%"

REM 备份输出目录（如存在）
if exist "%WORK_DIR%output" (
    xcopy /E /I /Y "%WORK_DIR%output" "%BACKUP_DIR%\output" >> "%LOG_FILE%" 2>&1
    echo [OK] 已备份 output 目录 >> "%LOG_FILE%"
)

REM 备份增量缓存（如存在，涉及 M14）
if exist "%WORK_DIR%ai_cache.json" (
    copy /Y "%WORK_DIR%ai_cache.json" "%BACKUP_DIR%\ai_cache_backup.json" >> "%LOG_FILE%" 2>&1
    echo [OK] 已备份增量缓存 >> "%LOG_FILE%"
)

REM 备份 .env（如存在）
if exist "%WORK_DIR%.env" (
    copy /Y "%WORK_DIR%.env" "%BACKUP_DIR%\.env.backup" >> "%LOG_FILE%" 2>&1
    echo [OK] 已备份 .env 文件 >> "%LOG_FILE%"
)
```

### 失败回滚提示（v3.4.1 新增）

.bat 执行失败时，CLEANUP 段必须输出回滚提示：

```bat
:CLEANUP
if %ERROR_FLAG% neq 0 (
    echo ============================================ >> "%LOG_FILE%"
    echo [ROLLBACK] 执行失败，可从备份恢复: >> "%LOG_FILE%"
    echo   恢复输出目录: xcopy /E /I /Y "%BACKUP_DIR%\output" "%WORK_DIR%output" >> "%LOG_FILE%"
    echo   恢复增量缓存: copy /Y "%BACKUP_DIR%\ai_cache_backup.json" "%WORK_DIR%ai_cache.json" >> "%LOG_FILE%"
    echo   恢复 .env: copy /Y "%BACKUP_DIR%\.env.backup" "%WORK_DIR%.env" >> "%LOG_FILE%"
    echo   完整备份目录: %BACKUP_DIR% >> "%LOG_FILE%"
    echo ============================================ >> "%LOG_FILE%"
)
```

**AI 行为铁律**：
- ✅ 生成 .bat 时必须包含 `BACKUP_DIR` 变量和备份段
- ✅ 生成后必须主动告知用户备份目录位置
- ✅ 失败时必须输出回滚命令提示
- 🚫 禁止生成不含备份段的 .bat 模板（除非用户明确说"不用备份"）

## 适用场景

| 场景 | 典型用途 |
|------|---------|
| 1 采集（定期） | 每天定时跑采集 + 写入 Excel + 发邮件 |
| 2 提取（批量） | 批量 PDF/Word 字段提取 + 输出汇总 Excel |
| 3 SQL（自动化） | 跑 SQL + 导出 CSV + 上传到飞书 |
| 4 核对（定时） | 每周对账 + 输出异常清单 |
| 6 周报（自动化） | 周一自动合并多文件 + 出周报 |
| 7 深度报告（一键复跑） | 一键重跑深度报告 + 输出 HTML |

**不适用**：
- 单次临时查询（直接在 AI 里跑即可）
- 需要人工介入决策的步骤（如核对中需人工裁决的不一致项）
- 跨平台需求（bat 是 Windows 专用，跨平台用 shell + Makefile）

## 模板规格

### 文件命名

```
{task_name}_{frequency}.bat
例：daily_fund_collect.bat / weekly_report_merge.bat
```

### bat 模板结构（8 段）

```bat
@echo off
chcp 65001 >nul
REM ============================================
REM {任务名} - {频率} 自动执行
REM 创建时间: {YYYY-MM-DD}
REM 作者: data-prompt-coach v3.1
REM ============================================

REM ---- 段 1: 环境变量 ----
set TASK_NAME={task_name}
set WORK_DIR=%~dp0
set LOG_FILE=%WORK_DIR%logs\%TASK_NAME%_%date:~0,4%%date:~5,2%%date:~8,2%.log
set PYTHON=python
set ERROR_FLAG=0

REM ---- 段 2: 创建日志目录 ----
if not exist "%WORK_DIR%logs" mkdir "%WORK_DIR%logs"

REM ---- 段 3: 日志头 ----
echo ============================================ > "%LOG_FILE%"
echo Task: %TASK_NAME% >> "%LOG_FILE%"
echo Start: %date% %time% >> "%LOG_FILE%"
echo ============================================ >> "%LOG_FILE%"

REM ---- 段 4: 前置检查 ----
echo [CHECK] Python 是否可用... >> "%LOG_FILE%"
%PYTHON% --version >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Python 不可用，终止 >> "%LOG_FILE%"
    set ERROR_FLAG=1
    goto CLEANUP
)
echo [OK] Python 可用 >> "%LOG_FILE%"

REM ---- 段 5: 主流程 ----
echo [STEP 1] {步骤1描述}... >> "%LOG_FILE%"
%PYTHON% "%WORK_DIR%scripts\step1_collect.py" >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Step 1 失败 >> "%LOG_FILE%"
    set ERROR_FLAG=1
    goto CLEANUP
)
echo [OK] Step 1 完成 >> "%LOG_FILE%"

echo [STEP 2] {步骤2描述}... >> "%LOG_FILE%"
%PYTHON% "%WORK_DIR%scripts\step2_clean.py" >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Step 2 失败 >> "%LOG_FILE%"
    set ERROR_FLAG=1
    goto CLEANUP
)
echo [OK] Step 2 完成 >> "%LOG_FILE%"

REM ---- 段 6: 结果校验（与 M7 联动） ----
echo [VERIFY] 跑验真脚本... >> "%LOG_FILE%"
%PYTHON% "%WORK_DIR%scripts\verify.py" >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARN] 验真有警告，请人工查看 >> "%LOG_FILE%"
    REM 不终止，继续到 CLEANUP
)
echo [OK] 验真完成 >> "%LOG_FILE%"

REM ---- 段 7: 清理 + 收尾 ----
:CLEANUP
echo ============================================ >> "%LOG_FILE%"
echo End: %date% %time% >> "%LOG_FILE%"
if %ERROR_FLAG% equ 0 (
    echo Status: SUCCESS >> "%LOG_FILE%"
    echo [SUCCESS] %TASK_NAME% 完成
) else (
    echo Status: FAILED >> "%LOG_FILE%"
    echo [FAILED] %TASK_NAME% 失败，请查看日志: %LOG_FILE%
)
echo ============================================ >> "%LOG_FILE%"

REM ---- 段 8: 退出码 ----
exit /b %ERROR_FLAG%
```

## 4 大设计原则

### 1. 日志强制写入
- 所有 stdout/stderr 重定向到日志文件
- 日志文件按日期命名，便于追溯
- 关键节点（每步开始/结束）必须打 `[STEP]` `[OK]` `[FAIL]` 标签

### 2. 错误立即终止
- 任一步骤 `%ERRORLEVEL% neq 0` → 立即跳到 CLEANUP
- 不继续跑后续步骤（避免污染数据）
- 设置 `ERROR_FLAG=1` 用于最终状态判断

### 3. 验真独立步骤
- 主流程跑完后，单独跑一次验真脚本（与 M7 验真闭环联动）
- 验真有警告不终止，但日志标记 `[WARN]` 供人工裁决

### 4. 退出码语义
- `exit /b 0` → 全部成功（可用于 Windows 任务计划程序判断）
- `exit /b 1` → 有失败（任务计划程序可触发告警/重试）

## 与方法论联动

| 方法论 | 联动方式 |
|--------|---------|
| **M7 验真闭环** | 段 6 调用验真脚本 |
| **M14 增量同步** | 段 5 主流程可调用增量同步脚本 |
| **M6 分批处理** | 段 5 步骤可循环调用分批脚本 |
| **M2 防幻觉** | 验真脚本内嵌防幻觉检查 |

## Windows 任务计划程序集成

```powershell
# 创建每日 09:00 执行的任务
schtasks /create /tn "DailyDataCollect" /tr "D:\path\to\daily_collect.bat" /sc daily /st 09:00 /rl HIGHEST

# 创建每周一 09:00 执行的任务
schtasks /create /tn "WeeklyReport" /tr "D:\path\to\weekly_report.bat" /sc weekly /d MON /st 09:00 /rl HIGHEST

# 查看任务状态
schtasks /query /tn "DailyDataCollect" /v
```

## 输出文件

bat 模板规格本身（用户读后让 AI 生成实际 bat 文件）：

| 输出 | 位置 | 说明 |
|------|------|------|
| `*.bat` | 项目根目录或 `scripts/` | 主执行入口 |
| `logs/*.log` | `logs/` | 按日期命名的日志 |
| `scripts/step*.py` | `scripts/` | 各步骤 Python 脚本 |
| `scripts/verify.py` | `scripts/` | 验真脚本 |
| `ai_cache.json` | 项目根目录 | 增量同步指纹缓存（若用 M14） |

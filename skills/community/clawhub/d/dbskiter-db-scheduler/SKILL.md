---
name: db-scheduler
description: |
  数据库调度工具，支持备份、定时任务管理、任务执行日志。

  使用场景：
  - 用户说"备份数据库" → backup
  - 用户说"定时任务" → task
  - 用户说"查看任务日志" → logs

  用法：
  - dbskiter --output-mode=ai --database=<name> scheduler backup --type=full
  - dbskiter --output-mode=ai --database=<name> scheduler task list
  - dbskiter --output-mode=ai --database=<name> scheduler task add daily_backup "0 2 * * *"
  - dbskiter --output-mode=ai --database=<name> scheduler task enable daily_backup
  - dbskiter --output-mode=ai --database=<name> scheduler task disable daily_backup
  - dbskiter --output-mode=ai --database=<name> scheduler task run daily_backup
  - dbskiter --output-mode=ai --database=<name> scheduler logs
---

# 数据库调度 Skill

## 目标

当用户提到以下关键词时，使用此skill：

| 用户说法    | 执行命令                        | 说明       |
| ------- | --------------------------- | -------- |
| "备份数据库" | `dbskiter --output-mode=ai --database=<name> scheduler backup`          | 执行备份     |
| "定时任务"  | `dbskiter --output-mode=ai --database=<name> scheduler task`            | 管理定时任务   |
| "任务日志"  | `dbskiter --output-mode=ai --database=<name> scheduler logs`            | 查看执行记录   |
| "启动调度器" | `dbskiter --output-mode=ai --database=<name> scheduler daemon start`    | 启动自动执行   |
| "停止调度器" | `dbskiter --output-mode=ai --database=<name> scheduler daemon stop`     | 停止自动执行   |
| "调度器状态" | `dbskiter --output-mode=ai --database=<name> scheduler daemon status`   | 查看运行状态   |
| "创建工作流" | `dbskiter --output-mode=ai --database=<name> scheduler workflow create` | 创建DAG工作流 |
| "执行工作流" | `dbskiter --output-mode=ai --database=<name> scheduler workflow submit` | 提交工作流执行  |

## 核心命令

### 1. 备份数据库

```bash
dbskiter --database=<数据库名> scheduler backup --type=full
```

**参数**：

- `--type`: full(全量) | incremental(增量)
- `--compress`: 压缩备份
- `--tables`: 指定表（逗号分隔）
- `--output-dir`: 输出目录

### 2. 定时任务管理

```bash
# 列出所有任务
dbskiter --database=<数据库名> scheduler task list

# 添加任务（每天凌晨2点执行备份）
dbskiter --database=<数据库名> scheduler task add daily_backup "0 2 * * *" --type=backup

# 删除任务
dbskiter --database=<数据库名> scheduler task remove daily_backup

# 启用/禁用任务
dbskiter --database=<数据库名> scheduler task enable daily_backup
dbskiter --database=<数据库名> scheduler task disable daily_backup

# 立即执行任务
dbskiter --database=<数据库名> scheduler task run daily_backup
```

**Cron表达式格式**：`分 时 日 月 周`

| 表达式           | 含义     |
| ------------- | ------ |
| `0 2 * * *`   | 每天凌晨2点 |
| `0 */6 * * *` | 每6小时   |
| `0 0 * * 0`   | 每周日    |

### 3. 查看任务日志

```bash
# 查看所有日志
dbskiter --database=<数据库名> scheduler logs

# 查看特定任务日志
dbskiter --database=<数据库名> scheduler logs --task=daily_backup

# 只看失败日志
dbskiter --database=<数据库名> scheduler logs --status=failed
```

### 4. 调度器守护进程管理

```bash
# 启动调度器（后台自动执行定时任务）
dbskiter --database=<数据库名> scheduler daemon start

# 查看调度器状态
dbskiter --database=<数据库名> scheduler daemon status

# 停止调度器
dbskiter --database=<数据库名> scheduler daemon stop
```

**使用流程**：

1. 添加定时任务：`dbskiter --database=<name> scheduler task add daily_backup "0 2 * * *"`
2. 启动调度器：`dbskiter --database=<name> scheduler daemon start`
3. 调度器每30秒检查一次，到达执行时间自动运行任务
4. 查看日志：`dbskiter --database=<name> scheduler logs`

### 5. DAG工作流管理

```bash
# 创建工作流
dbskiter --database=<数据库名> scheduler workflow create maintenance --desc="日常维护"

# 添加任务到工作流
dbskiter --database=<数据库名> scheduler workflow add-task maintenance backup --type=backup
dbskiter --database=<数据库名> scheduler workflow add-task maintenance analyze --type=analyze --depends=backup

# 查看工作流状态
dbskiter --database=<数据库名> scheduler workflow status maintenance

# 执行工作流
dbskiter --database=<数据库名> scheduler workflow submit maintenance

# 列出所有工作流
dbskiter --database=<数据库名> scheduler workflow list
```

**工作流特点**：

- 支持任务依赖（DAG）
- 按拓扑排序自动确定执行顺序
- 依赖任务失败会中断后续执行

## AI决策流程

### 场景1：用户说"备份数据库"

```
步骤1：确认备份类型（默认full）
步骤2：执行 dbskiter --database=<name> scheduler backup --type=full
步骤3：总结备份结果
```

### 场景2：用户说"每天凌晨2点自动备份"

```
步骤1：执行 dbskiter --database=<name> scheduler task add daily_backup "0 2 * * *"
步骤2：确认任务已添加
步骤3：提示用户任务已启用
```

### 场景3：用户说"查看备份任务执行情况"

```
步骤1：执行 dbskiter --database=<name> scheduler logs --task=daily_backup
步骤2：分析执行记录
步骤3：报告成功/失败情况
```

## 输出解读

### 任务列表输出

```
============================================================
摘要: 共3个任务（2个启用，1个禁用）
============================================================

任务名称             类型       调度            状态     下次执行
--------------------------------------------------------------------------------
daily_backup         backup     0 2 * * *       启用     2026-04-23T02:00:00
weekly_analyze       analyze    0 0 * * 0       启用     2026-04-27T00:00:00
old_cleanup          vacuum     0 3 1 * *       禁用     未知

提示: 使用 'scheduler task add' 添加新任务
```

### 任务日志输出

```
============================================================
摘要: 共5条日志记录 (任务: daily_backup)
============================================================

时间                 任务                 状态     耗时       结果
------------------------------------------------------------------------------------------
2026-04-22T02:00:00  daily_backup         [OK]     45.2s      备份成功
2026-04-21T02:00:00  daily_backup         [OK]     42.8s      备份成功
2026-04-20T02:00:00  daily_backup         [FAIL]   -          磁盘空间不足
```

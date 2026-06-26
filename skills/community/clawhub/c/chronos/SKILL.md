---
name: chronos
description: 通用周期任务管理器 - 支持6种周期类型、每月N次配额、自动cron、统一视图，适用于所有定时任务场景
---

# Chronos - Universal Periodic Task Manager

## What this skill controls
- **周期任务表**：`periodic_tasks` + `periodic_occurrences`（默认使用共享 `todo.db`）
- **原 todo 表**：`entries`（仅兼容 legacy inbox / 未迁移旧任务）
- **统一入口**：`todo.py`

## Capabilities

### 周期类型
- `once`：一次性（有明确 `--start-date` 时走 canonical task/occurrence）
- `daily`：每天
- `hourly`：每 N 小时（`--interval-hours` + `--time` 作为锚点）
- `weekly`：每周（指定星期几）
- `monthly_fixed`：每月固定日期（如15号）
- `monthly_range`：每月区间（如11号→5号，跨月）
- `monthly_n_times`：每月限次（如每周三每月最多2次，或 `weekday` 留空表示“每天都可提醒，但本月完成满额后停止”）
- `monthly_dates`：每月多个固定日期（如 `1,15,31`）

### 智能配额
- 仅 `completed` 计数，`skip` 不计
- `monthly_n_times` 若 `weekday` 为空，则按“每日可提醒”展开，但仍受每月配额约束
- 配额用满后自动完成当月剩余活动日
- 每月1号自动重置计数器

### 自动提醒
- Cron 任务自动生成（未来事件）
- 每日自动清理过期 cron
- 提醒投递必须显式指定目标 chat
- 若时间已过，会走补发提醒分支
- `hourly` 任务会在当天展开为多个 occurrence，按 `scheduled_time` 各自提醒/补完成

### 统一视图
- `todo.py list`：合并显示周期任务和普通任务
- `todo.py add`：智能路由（scheduled recurring / scheduled once → canonical task；无日期的一次性便签 → entries）
- `todo.py complete`：完成单个 occurrence 或普通任务
- `todo.py complete-overdue`：优先基于 occurrence 补完成；legacy entries 仅保留兼容兜底
- `todo.py show`：查看详情
- `todo.py skip`：跳过任务且不消耗 monthly_n_times 配额

### 显式 system handler
- `special_handler` 元数据挂在 `periodic_tasks` 上，不再只能靠 `entries.text` 正则猜测
- 当前已支持：`meta_review_fallback`、`sync_subagent_memory`
- `sync_subagent_memory` 从 `memory/subagent_sync_ledger.json` 读取待同步 subagent session；现在应由 OpenClaw 在 subagent 完成路径自动写入 ledger，`memory_manager.py record-subagent <session_id>` 仅保留给补录/回填场景，成功后标记 handled
- overdue completion 会把 handler 结果写回 occurrence：`completion_mode` / `special_handler_result`
- 对同一天同一 hourly 任务的多个 overdue occurrence，如存在 `special_handler`，`complete-overdue` 只执行一次 handler，再把所有相关 occurrence 标记为 `fallback_handler_merged`，并写入 merged trace（merge_key / merged occurrence index/count）

## Configuration

- **Chat ID**: Reminder notifications target a specific chat. Configure via:
  - Environment variable: `CHRONOS_CHAT_ID`
  - Config file: `~/.config/chronos/config.json` (or `CHRONOS_CONFIG_PATH`) with field `chat_id`
  - If neither is set, Chronos raises a configuration error
- **No implicit routing**: Chronos does not fall back to `last` or any implicit delivery target
- **Workspace/DB overrides**:
  - `CHRONOS_DB_PATH`
  - `CHRONOS_WORKSPACE` / `OPENCLAW_WORKSPACE`
  - `OPENCLAW_BIN`

## Usage

```bash
# 列出活跃待办（自动确保今天 occurrence 已生成）
python3 skills/chronos/scripts/todo.py list

# 如需连 skipped 一起看，显式打开
python3 skills/chronos/scripts/todo.py list --include-skipped

# 添加周期任务（例如：每月2次，每周三10:00）
python3 skills/chronos/scripts/todo.py add "周三抢券" \
  --cycle-type monthly_n_times \
  --weekday 2 \
  --n-per-month 2 \
  --time 10:00

# 添加“每天都可提醒，但本月完成一次后本月不再提醒”的任务
python3 skills/chronos/scripts/todo.py add "福建农行秒杀京东卡" \
  --cycle-type monthly_n_times \
  --n-per-month 1 \
  --time 09:00

# 添加每4小时任务（08:00 作为锚点；当天展开为 00/04/08/12/16/20）
python3 skills/chronos/scripts/todo.py add "同步 subagent 记忆" \
  --cycle-type hourly \
  --interval-hours 4 \
  --time 08:00 \
  --task-kind system \
  --special-handler sync_subagent_memory

# 添加一次性计划任务（Phase 1 起：有 start-date 就进入 canonical task）
python3 skills/chronos/scripts/todo.py add "周五 10 点抢券" \
  --cycle-type once \
  --start-date 2026-03-27 \
  --time 10:00

# 添加每月多个日期任务
python3 skills/chronos/scripts/todo.py add "月初/中/末检查" \
  --cycle-type monthly_dates \
  --dates-list 1,15,31 \
  --time 09:00

# 添加普通 inbox 便签（仍走 entries）
python3 skills/chronos/scripts/todo.py add "买牛奶" --category 生活

# 添加 system task（显式 handler）
python3 skills/chronos/scripts/todo.py add "Meta-Review fallback" \
  --cycle-type daily \
  --time 02:00 \
  --task-kind system \
  --special-handler meta_review_fallback

# 完成任务
python3 skills/chronos/scripts/todo.py complete FIN-123  # 周期任务 occurrence
python3 skills/chronos/scripts/todo.py complete 45      # legacy / inbox 任务 ID

# 统一补完成今天已经过时的计划任务
python3 skills/chronos/scripts/todo.py complete-overdue
python3 skills/chronos/scripts/todo.py complete-overdue --dry-run

# 跳过任务（不影响配额）
python3 skills/chronos/scripts/todo.py skip FIN-123     # 周期任务
python3 skills/chronos/scripts/todo.py skip 45         # 普通任务

# 自然语言支持
python3 skills/chronos/scripts/todo.py "跳过 FIN-123"
python3 skills/chronos/scripts/todo.py "查询待办"
python3 skills/chronos/scripts/todo.py "添加任务 每4小时 08:00 同步subagent记忆"

# 查看详情
python3 skills/chronos/scripts/todo.py show FIN-123
```

## Verification

```bash
python3 -m unittest discover -s skills/chronos/tests -v
python3 skills/chronos/scripts/schema_preflight.py
python3 skills/chronos/scripts/test_config.py
```
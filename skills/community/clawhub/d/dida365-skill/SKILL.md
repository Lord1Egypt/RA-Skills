---
name: dida365-skill
description: '滴答清单/TickTick 任务管理工具——创建、查看、完成、删除任务和项目。Use when user says: 创建任务、添加待办、今日任务、查看清单、完成任务、滴答清单、TickTick、TODO、待办事项、任务管理、项目管理、标记完成、删除任务、设置截止日期、任务优先级、新建项目、收集箱、inbox。'
allowed-tools: 'Bash'
license: MIT
compatibility: 'Requires Python 3.8+. Uses Python stdlib only. Needs Dida365 OAuth token.'
metadata:
  author: fanxing / woodcoal
  version: 3.1.0
---

## 首次使用：配置与授权

1.  **配置凭据**: 在 `.env` 中填写 `DIDA_CLIENT_ID` 和 `DIDA_CLIENT_SECRET`。
2.  **完成授权**: 运行 `python3 index.py auth` 并在浏览器完成操作。

## 命令结构

所有命令均采用 `python3 index.py <category> <subcommand> [args]` 格式。

**注意：**

1. **空格要求**：命令名、子命令名和参数之间**必须**使用空格分隔（例如：`project update <id>` 而非 `project update<id>`）。
2. **安全警告**：禁止自动执行任何 `delete` 操作。在执行 `project delete` 或 `task delete` 之前，**必须**获得用户针对具体 ID 的明确批准。

### Intent Decision Tree

```
用户想要…
├─ 项目管理 (project)
│  ├─ 列出所有项目 ──────→ project list [--force]
│  ├─ 查看项目任务 ──────→ project get <projectId> [--force]
│  ├─ 查看项目元数据 ────→ project info <projectId>
│  ├─ 创建新项目 ────────→ project create "<name>" [--color x]
│  ├─ 更新项目 ──────────→ project update <projectId> [--name x]
│  ├─ 清除本地缓存 ──────→ project clear-cache
│  └─ 删除项目 (需确认) ─→ project delete <projectId> !! ⚠️ 需用户批准
├─ 任务操作 (task)
│  ├─ 查看任务详情 ──────→ task get <projectId> <taskId>
│  ├─ 创建新任务 ────────→ task create "<title>" [--project id] [--due YYYY-MM-DD]
│  ├─ 创建清单任务 ──────→ task create-checklist "<title>" --project <id> --items "a|b|c"
│  ├─ 更新任务 ──────────→ task update <projectId> <taskId> [--title x]
│  ├─ 完成任务 ──────────→ task complete <projectId> <taskId>
│  ├─ 删除任务 (需确认) ─→ task delete <projectId> <taskId> !! ⚠️ 需用户批准
│  ├─ 移动任务 ──────────→ task move <fromPid> <toPid> <taskId>
│  └─ 高级 JSON 模式 ────→ task create-raw / update-raw
└─ 查询与筛选 (search)
   ├─ 今日待办 ──────────→ search today [--force]
   ├─ 未来几天到期 ──────→ search upcoming [days] [--force]
   ├─ 指定区间到期 ──────→ search due-range <start> <end> [--force]
   ├─ 已完成任务 ────────→ search completed <start> <end> [--force]
   ├─ 高级筛选 ──────────→ search filter [--project id] [--priority N]
   └─ 收集箱 ────────────→ search inbox [--force]
```

## 核心工作流：性能与缓存优化

为了提高响应速度并减少 API 配额消耗，本工具内置了缓存机制（默认 365 分钟）：

1.  **主动查询**: 优先使用缓存。
    - `python3 index.py project list` 获取缓存的项目列表。
    - `python3 index.py project get <id>` 获取缓存的项目任务。
2.  **强制刷新**: 如果怀疑数据陈旧，使用 `--force` 参数。
    - 示例：`python3 index.py search today --force`
3.  **自动失效**:
    - 执行任何 `create`、`update`、`delete` 或 `complete` 操作后，相关项目的缓存会**自动清除**。下一次查询将自动从服务器获取最新数据。无需手动刷新。
4.  **手动维护**: 如果发现同步异常，可运行 `python3 index.py project clear-cache`。

## 参数说明

- `--force`: 忽略本地缓存，强制从服务器拉取最新数据。
- `--priority`: 0=无, 1=低, 3=中, 5=高。
- `--due`: 格式为 `YYYY-MM-DD`。
- `--items`: 清单子项，用 `|` 分隔，例如 `"买牛奶|买鸡蛋"`。
- `--tags`: 逗号分隔，例如 `"工作,紧急"`。

## 故障排除

- **数据不一致**: 如果在网页端修改了任务但在 CLI 没看到，请加 `--force` 重新查询。
- **未授权**: 运行 `python3 index.py auth`。
- **ID 错误**: 运行 `python3 index.py project list --force` 核对最新 ID。
- **获取帮助**: 在任何分类后加 `-h`，如 `python3 index.py task -h`。

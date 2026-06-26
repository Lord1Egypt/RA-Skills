# AutoDream Skill

自动记忆整理子代理 - 类似 Claude Code 的 AutoDream 功能。

## 安装

```bash
skillhub install autodream
```

## 快速开始

### 立即运行一次

```bash
python3 skills/autodream/scripts/autodream_cycle.py --workspace .
```

### 设置定时任务

```bash
bash skills/autodream/scripts/setup_24h.sh
```

### 强制运行（忽略触发条件）

```bash
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --force
```

## 功能

- **四阶段整理流程**：Orientation → Gather Signal → Consolidation → Prune and Index
- **自动触发**：24 小时 + 5 次会话后自动运行
- **手动触发**：随时运行整理
- **备份保护**：删除前备份到 `memory/autodream/backup/`
- **详细报告**：生成 `memory/autodream/cycle_report.md`

## 输出

- `MEMORY.md` - 更新后的记忆索引（≤200 行）
- `memory/autodream/state.json` - 运行状态
- `memory/autodream/cycle_report.md` - 整理报告
- `memory/autodream/consolidated_entries.json` - 整理后的条目
- `memory/autodream/pruned_entries.json` - 被删除的条目
- `memory/autodream/merged_entries.json` - 被合并的条目

## 配置

编辑 `skills/autodream/config/config.json`:

```json
{
  "interval_hours": 24,
  "min_sessions": 5,
  "max_memory_lines": 200,
  "backup_enabled": true,
  "dry_run": false,
  "verbose": false
}
```

## 与 memory-mesh-core 对比

| 特性 | autodream | memory-mesh-core |
|------|-----------|------------------|
| 主要目标 | 单工作区记忆整理 | 跨工作区记忆共享 |
| 整理频率 | 24 小时 +5 次会话 | 12 小时 |
| 记忆范围 | 本地记忆文件 | 本地 + 全局共享 |
| 输出格式 | Markdown + JSON | JSON + GitHub Issue |

**推荐组合使用**：autodream 负责日常整理，memory-mesh-core 负责跨工作区共享。

## 版本

1.0.0 - 初始版本

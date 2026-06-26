---
name: autodream
description: AutoDream - Automatic memory consolidation sub-agent. Periodically (24h +5 sessions) organizes MEMORY.md and memory files, deduplicates, merges, removes stale entries. Like Claude Code's AutoDream feature. 自动记忆整理子代理，定期整理记忆文件，去重合并删除过时条目。
---

# AutoDream Skill - 自动记忆整理

## 核心理念

**像 REM 睡眠一样整理记忆。**

AutoDream 是一个后台运行的记忆整理子代理，解决长期记忆衰减问题：
- 记忆文件随时间积累变得混乱
- 相对日期（如"昨天"）失去意义
- 过时的调试方案引用已删除的文件
- 矛盾条目堆积

## 工作原理

### 四阶段流程

| 阶段 | 操作 | 输出 |
|------|------|------|
| **1. Orientation** | 读取当前记忆目录，建立记忆状态地图 | 记忆文件清单、条目统计 |
| **2. Gather Signal** | 窄搜索会话记录，提取用户纠正、明确保存指令、重复主题、重要决策 | 高价值信号列表 |
| **3. Consolidation** | 合并新信息，转换相对日期为绝对日期，删除矛盾/过时条目，合并重复 | 整理后的记忆文件 |
| **4. Prune and Index** | 更新 MEMORY.md 索引，保持<200 行（启动加载阈值） | 精简的 MEMORY.md |

### 触发条件

**自动触发（双条件）：**
- 距上次整理 ≥ 24 小时 **且**
- 自上次整理后 ≥ 5 次会话

**手动触发：**
- 运行 `/dream` 命令
- 或直接告诉智能体"运行 AutoDream 整理记忆"

### 安全约束

- **只读模式**：只能写入记忆文件，不能修改项目代码
- **锁文件**：防止并发运行
- **后台执行**：不阻塞用户会话
- **MEMORY.md 限制**：保持≤200 行（启动加载阈值）

## 快速开始

### 立即运行一次

```bash
python3 skills/autodream/scripts/autodream_cycle.py --workspace .
```

### 配置定时任务（默认 24 小时）

```bash
bash skills/autodream/scripts/setup_24h.sh
```

### 自定义间隔

```bash
bash skills/autodream/scripts/setup_24h.sh 12h
```

### 手动触发整理

```bash
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --force
```

## 输出文件

- `memory/autodream/state.json` - 运行状态（上次运行时间、会话计数）
- `memory/autodream/consolidation_report.json` - 整理报告
- `memory/autodream/pruned_entries.json` - 被删除的条目
- `memory/autodream/merged_entries.json` - 被合并的条目
- `memory/autodream/cycle_report.md` - 人类可读的整理报告
- `MEMORY.md` - 更新后的记忆索引
- `memory/topics/*.md` - 更新后的主题记忆文件

## 与 memory-mesh-core 的关系

| 特性 | memory-mesh-core | autodream |
|------|------------------|-----------|
| 主要目标 | 跨工作区记忆共享 | 单工作区记忆整理 |
| 整理频率 | 12 小时 | 24 小时 +5 次会话 |
| 记忆范围 | 本地 + 全局共享 | 本地记忆文件 |
| 输出格式 | JSON + GitHub Issue | Markdown + JSON |
| 适合场景 | 多智能体协作 | 个人工作区维护 |

**推荐组合使用：**
- `autodream` 负责日常记忆整理
- `memory-mesh-core` 负责跨工作区记忆共享

## 安全规则

- 绝不删除用户明确标注"重要"的记忆
- 绝不修改项目源代码
- 绝不泄露敏感信息（API 密钥、密码等）
- 删除操作前备份到 `memory/autodream/backup/`

## 配置选项

在 `skills/autodream/config/config.json` 中配置：

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

## 版本历史

- `1.0.0`: 初始版本，实现四阶段整理流程
- `1.0.1`: 添加手动触发支持和备份功能
- `1.0.2`: 优化相对日期转换逻辑

## 社区

- 问题反馈：https://github.com/wanng-ide/autodream/issues
- 技能安装：`skillhub install autodream`

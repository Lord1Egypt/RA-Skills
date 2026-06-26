---
name: clawclau
description: 异步 Claude Code 任务调度工具集（ClawClau）。基于 tmux 派发后台 Claude Code 任务，含进度汇报、完成通知、状态查询、中途纠偏。触发场景：让乌萨奇做xxx、派发任务给Claude Code、查看后台任务状态、终止后台任务、batch任务派发。
---

# ClawClau v2.0.0 — Claude Code 任务调度系统

小八（OpenClaw）派发异步 Claude Code 任务的工具集。基于 Elvis Sun 的 Agent Swarm 架构设计。

## 核心文件

```
<skills-dir>/clawclau/scripts/          # 安装后脚本位置
├── clawclau-lib.sh        # 共享库（所有脚本 source 此文件）
├── claude-spawn.sh        # 派发任务（含内嵌完成检测器和进度汇报器）
├── claude-check.sh        # 查询状态（确定性，不耗 token）
├── claude-result.sh       # 获取结果
├── claude-monitor.sh      # 批量监控安全兜底（cron 用）
├── claude-kill.sh         # 终止任务
└── claude-steer.sh        # 中途纠偏

~/.clawclau/
├── active-tasks.json      # 任务注册表（source of truth）
├── config                 # 本地配置（notify_chat 等）
├── logs/
│   ├── task-id.json       # stream-json 格式日志（print 模式）
│   └── task-id.txt        # 纯文本日志（steerable 模式）
└── prompts/
    ├── task-id.txt        # prompt 备份
    └── task-id-wrapper.sh # 自动生成的 wrapper 脚本
```

## 安装与配置

```bash
# 依赖
brew install tmux jq && which claude

# 初始化
mkdir -p ~/.clawclau/logs ~/.clawclau/prompts

# 配置通知（可选）
echo "notify_chat = oc_xxxxxxxx" >> ~/.clawclau/config

# shell profile（可选）
export CC_SCRIPTS=~/.openclaw/workspace/skills/clawclau/scripts
```

## 快速开始

```bash
SCRIPTS=~/.openclaw/workspace/skills/clawclau/scripts

# 1. 派发任务
$SCRIPTS/claude-spawn.sh my-task "请整理这份文档..." /path/to/workdir

# 2. 查看所有任务
$SCRIPTS/claude-check.sh

# 3. 查看单个任务详情
$SCRIPTS/claude-check.sh my-task

# 4. 获取完整结果
$SCRIPTS/claude-result.sh my-task

# 5. 终止任务
$SCRIPTS/claude-kill.sh my-task
```

## 脚本接口

### claude-spawn.sh — 派发任务

```bash
claude-spawn.sh [OPTIONS] <task-id> "<prompt>" [workdir]

--steerable        交互式模式（支持 claude-steer.sh 纠偏）
--timeout <sec>    超时秒数（默认 600）
--interval <sec>   进度汇报间隔，0=关闭（默认 180）
--max-retries <n>  最大重试次数记录（默认 3）
--model <name>     Claude 模型名称
--parent <id>      父任务 ID（重试时使用）
--retry-count <n>  当前重试计数（内部使用）
```

示例：

```bash
# 带进度汇报（每 60s 通知一次）
$SCRIPTS/claude-spawn.sh research-task "调研XXX行业趋势" ~/.openclaw/workspace \
  --interval 60 --timeout 1200

# 交互式模式（可中途纠偏）
$SCRIPTS/claude-spawn.sh explore-task "探索代码库，找出主要问题" ~/myproject \
  --steerable --interval 120

# 指定模型
$SCRIPTS/claude-spawn.sh heavy-task "复杂分析任务..." . \
  --model claude-opus-4-6 --timeout 1800
```

spawn 内嵌双重 fork 后台完成检测器，任务结束时自动调用 `cc_notify` 通知小八。

### claude-check.sh — 查询状态

```bash
claude-check.sh              # 列出所有任务（表格）
claude-check.sh <task-id>    # 单任务详情（含结果预览）
```

以 tmux session 是否存活为 running 的最终判据，不调用 AI，不消耗 token。

### claude-result.sh — 获取结果

```bash
claude-result.sh <task-id>        # 从 stream-json 提取可读文本
claude-result.sh <task-id> --raw  # 输出原始 stream-json 日志
```

### claude-monitor.sh — 批量监控（cron 用）

```bash
# 设置 cron（每 10 分钟）
*/10 * * * * $SCRIPTS/claude-monitor.sh >> /tmp/clawclau-monitor.log 2>&1
```

### claude-kill.sh — 终止任务

```bash
claude-kill.sh <task-id>    # 终止 session，状态更新为 killed
```

### claude-steer.sh — 中途纠偏

```bash
claude-steer.sh <task-id> "请聚焦在 X 方面"    # 仅支持 --steerable 模式
```

## 参考文档

- 注册表字段、状态流转、环境变量：[references/schema.md](references/schema.md)
- 设计原则、通知机制、重试流程、运行模式：[references/design.md](references/design.md)

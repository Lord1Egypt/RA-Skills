---
name: context-cleanup
description: Analyze and archive low-value memory notes in OpenClaw workspace to reduce context bloat and improve responsiveness. 适用于上下文冗余、维护整理场景；默认流程为 analyze → plan → confirm → archive，归档优先于删除。
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🧹", "requires": { "bins": ["bash"] } }, "version": "0.3", "updatedAt": "2026-03-06 20:47 Asia/Shanghai" }
---

# Context Cleanup

用于整理 workspace 的 memory 日志，降低冗余上下文负担。

## 关键资源

- 脚本：`cleanup.sh`
- 策略：`references/policy.md`

## 标准流程（必须）

1. 分析现状
```bash
./skills/context-cleanup/cleanup.sh analyze
```

2. 生成计划（不执行）
```bash
./skills/context-cleanup/cleanup.sh plan
```

3. 用户确认后执行归档
```bash
./skills/context-cleanup/cleanup.sh archive
```

## 可选参数

```bash
# 指定截止日期（早于该日期的记录可归档）
./skills/context-cleanup/cleanup.sh archive 2026-03-01

# 仅预览，不执行
./skills/context-cleanup/cleanup.sh archive --dry-run

# 非交互执行（需谨慎）
./skills/context-cleanup/cleanup.sh archive --yes

# 机器可读输出
./skills/context-cleanup/cleanup.sh analyze --json
./skills/context-cleanup/cleanup.sh plan --json
```

## 执行规则

- 默认归档，不做永久删除
- 先 `plan` 后 `archive`
- 归档前必须获得用户确认（除非用户明确同意 `--yes`）
- 不处理 `MEMORY.md`、`specs/`、`AGENTS.md`

## 输出模板

```markdown
🧹 上下文清理计划

- Memory 文件：X
- 低价值候选：A
- 归档候选：B

是否按计划执行归档？
```

## 发布前自检

```bash
./skills/context-cleanup/cleanup.sh analyze
./skills/context-cleanup/cleanup.sh plan
./skills/context-cleanup/cleanup.sh archive --dry-run
```

# Hook 系统完整文档

> coding-framework 的事件驱动行为守卫系统。

## 概述

Hook 系统提供可配置的事件拦截与行为守卫，在关键执行节点插入检查和日志。
灵感来源：Claude Code Hook 事件系统。

## 事件类型

| 事件 | 触发时机 | 输入数据 | 输出 |
|------|----------|----------|------|
| PreExec | exec 命令执行前 | `{command, workdir, env}` | `{decision, message, matched_rules}` |
| PostExec | exec 命令执行后 | `{command, exitCode, stdout, stderr, duration}` | `{decision, message}` |
| Stop | 会话结束前 | `{session, reason, summary}` | `{decision, should_stop, pending_tasks}` |

## 规则引擎

规则定义在 `rules/` 目录下，每个 `.md` 文件包含 YAML frontmatter：

```yaml
---
name: rule-name
enabled: true
event: PreExec
matcher: "rm -rf"       # regex 匹配模式
action: block           # allow | warn | block | log
priority: 10            # 数字越大优先级越高
---
```

规则 body 部分定义详细说明、触发消息和豁免条件。

## 动作类型

| 动作 | 说明 |
|------|------|
| allow | 放行，记录日志 |
| warn | 放行但输出警告信息 |
| block | 阻止执行，返回拒绝原因 |
| log | 仅记录，不影响流程 |

## Hook 脚本规范

所有 hook 脚本位于 `hooks/` 目录：

1. 从 stdin 读取 JSON 事件数据
2. 加载 `rules/` 下匹配的规则
3. 按优先级逐条评估
4. 输出 JSON 结果到 stdout

```json
{
  "decision": "allow|warn|block",
  "message": "人类可读的说明",
  "matched_rules": ["rule-name-1"],
  "timestamp": "2026-06-26T22:00:00Z"
}
```

## 脚本说明

### pre-exec-check.sh

执行前安全检查。读取命令，匹配 security-rules.md 中的规则，输出决策。

### post-exec-log.sh

执行后日志记录。读取执行结果，写入审计日志 `memory/hook-audit.log`。

### stop-iteration.sh

迭代循环 Stop Hook。检查是否有活跃的迭代循环或待完成的承诺，未完成则阻止停止。

## 与 daily-agent 集成

```
用户消息 → daily-agent 分类
  → 任务执行
    → [PreExec hook] 每次 exec 前检查
    → [PostExec hook] 每次 exec 后记录
  → [Stop hook] 会话结束清理
```

## 添加新规则

在 `rules/` 下创建或编辑 `.md` 文件，按 YAML frontmatter 格式定义：

```yaml
---
name: no-format-disk
enabled: true
event: PreExec
matcher: "format|diskpart|chkdsk"
action: block
priority: 100
---
禁止执行磁盘格式化操作。此规则不可豁免。
```

## 审计日志

所有 hook 触发记录写入 `memory/hook-audit.log`：

```
[timestamp] [event] [decision] [rule] message
```

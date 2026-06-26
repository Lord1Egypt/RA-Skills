# Audit Evolution Adapter Guide

Audit Evolution 的目标是跨 Agent 框架使用。不同框架的 hook 名称不同，但最小契约是一样的：

```text
事件发生 -> 生成 run record -> Agent 读取 SKILL.md 和 latest.md -> 输出七段审计结果 -> 人类短指令路由
```

## 通用 Agent

只需要两步：

1. 让 Agent 能读取 `skills/audit-evolution/SKILL.md`。
2. 把下面的规则加入项目记忆、系统提示、router 或 AGENTS.md：

```text
当任务完成、失败、超时、跑分完成、用户纠错、上下文超过 60%、读取文件超过 5 个、修改 skill/config/gear 后，调用 Audit Evolution。
```

## Codex

推荐使用安装器：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-audit-evolution.ps1 -TargetWorkspace "D:\YourCodexWorkspace" -Agent codex -Force
```

安装器会更新 `AGENTS.md`。Codex 看到用户说“进化/保存/暂停/跑分/详情”时，应按 `skills/audit-evolution/SKILL.md` 路由。

## OpenClaw / Longju

推荐接入点：

```text
PostTask
ContextCheck
PreExternalAction
PostBenchmark
PostSkillChange
```

这些事件触发时运行：

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\.audit-evolution\hooks\invoke-audit-evolution-hook.ps1 -EventType benchmark_completed -Summary "刚完成一次评测"
```

macOS / Linux:

```bash
bash ./.audit-evolution/hooks/invoke-audit-evolution-hook.sh --event benchmark_completed --summary "刚完成一次评测"
```

然后让 OpenClaw Agent 优先读取：

```text
.audit-evolution/run-records/latest.md
skills/audit-evolution/SKILL.md
```

## 最小事件映射

| 事件 | EventType | 推荐动作 |
|---|---|---|
| 用户手动要求审计 | `manual` | 直接调用 Audit Evolution |
| 官方或本地跑分完成 | `benchmark_completed` | 生成 Evolution Card |
| 用户指出错误 | `user_corrected_agent` | 记录 user_feedback，区分事实和偏好 |
| 任务失败/超时/重试 | `task_failed_or_timeout_or_retry` | 写 Snapshot 和 Patch Proposal |
| 上下文超过 60% | `context_over_60_percent` | 停止扩展，写 Next-Run Bootstrap |
| 读取文件超过 5 个 | `more_than_5_files_read` | 停止追引用链 |
| 输出出现不确定语言 | `uncertainty_language_detected` | 把 claim 标成 unknown 或 model_inference |
| 修改 skill/config/gear | `skill_config_or_gear_changed` | 跑本地检查，写 Memory Ledger Entry |

## 外部动作边界

安装器和 hook 不会自动发布、上传、投票、评论、发消息、claim、花钱或跑官方 benchmark。外部动作必须由人类明确批准。

# 双环境适配指南（OpenClaw + Hermes）

本 Skill 同时兼容 OpenClaw 和 Hermes Agent。所有诊断逻辑一致，仅执行层命令不同。

## 环境自动检测

```bash
if command -v hermes &>/dev/null; then
    PLATFORM="hermes"
    CMD="hermes"
elif command -v openclaw &>/dev/null; then
    PLATFORM="openclaw"
    CMD="openclaw"
else
    if [ -d "$HOME/.hermes" ]; then
        PLATFORM="hermes"
        CMD="hermes"
    else
        PLATFORM="openclaw"
        CMD="openclaw"
    fi
fi
```

## 命令映射表

| 操作 | OpenClaw 命令 | Hermes 工具/命令 |
|------|---------------|------------------|
| 列出 Cron | `openclaw cron list --includeDisabled` | `cronjob(action='list')` |
| 查看运行历史 | `openclaw cron runs <jobId>` | `cronjob(action='list')` 查看 last output |
| 更新 Cron | `openclaw cron update <jobId> --patch '...'` | `cronjob(action='update', job_id='xxx', ...)` |
| 重新启用 | `openclaw cron update <jobId> --patch '{"enabled":true}'` | `cronjob(action='resume', job_id='xxx')` |
| 手动触发 | `openclaw cron run <jobId>` | `cronjob(action='run', job_id='xxx')` |
| 子 Agent 列表 | `openclaw subagents list` | 不适用（delegate_task 同步执行） |
| 终止子 Agent | `openclaw subagents kill <target>` | `process(action='kill', session_id='xxx')` |
| 状态检查 | `openclaw status` | `ps aux \| grep hermes` |

## 自动触发机制

### Hermes 环境：Cron Job

```
# 每日自检
cronjob(action='create',
    name='🔧 Agent 每日自检',
    schedule='0 8 * * *',
    prompt='执行 agent-optimization-expert 场景 3（系统健康度巡检）和场景 1（Cron 任务扫描）。检查磁盘/内存/容器/本地服务/所有 cron jobs。如有异常按诊断决策树修复并记录到 learnings/error-log.md。无异常只记录"一切正常"。',
    deliver='local')

# 每周知识更新
cronjob(action='create',
    name='📚 Agent 知识更新',
    schedule='0 3 * * 0',
    prompt='执行 agent-optimization-expert 路径 2（定期知识更新）：搜索 Anthropic/OpenAI 最新 Agent 工程实践，对比 references/ 现有内容，发现新模式追加到对应文件。',
    deliver='local')
```

### OpenClaw 环境：HEARTBEAT.md

在 `workspace/HEARTBEAT.md` 中配置：

```markdown
## Agent 自检配置
- **自检频率**：每 4 小时一次
- **工作时间**（9:00-18:00）：检查任务 + 系统健康 + 消息
- **非工作时间**（18:00-9:00）：仅检查紧急任务
- **触发 Skill**：发现异常时加载 agent-optimization-expert 诊断修复

## 检查清单
- [ ] Cron 任务是否有失败（最近 24 小时）
- [ ] 本地服务是否健康（3002/3003/3004）
- [ ] 磁盘使用率是否 > 85%
- [ ] learnings/error-log.md 是否有新增错误
```

## 修复规则差异

| 问题 | OpenClaw 修复 | Hermes 修复 |
|------|--------------|------------|
| sessionTarget/payload 不匹配 | `--patch '{"payload":{"kind":"systemEvent"}}'` | 不适用（Hermes 无此概念） |
| Cron prompt 过长 | 拆分 payload 逻辑 | 缩短 prompt 或拆成多 job |
| 工具未启用 | 检查 openclaw.json | 检查 cronjob 的 enabled_toolsets |
| 工作路径不对 | 不适用 | 检查 cronjob 的 workdir |

## 触发方式选择决策

```
当前环境？
├─ Hermes → Cron Job（方式 A）
└─ OpenClaw → HEARTBEAT.md（方式 B）
```

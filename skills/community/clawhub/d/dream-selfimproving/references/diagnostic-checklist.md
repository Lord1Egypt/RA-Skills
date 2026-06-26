# Dream Self-Improving — Diagnostic Checklist

## 快速健康检查

```bash
# 1. Cron 任务状态（OpenClaw 侧）
cat ~/.openclaw/cron/jobs.json | python3 -c "
import json, sys
jobs = json.load(sys.stdin)['jobs']
for j in jobs:
    if '梦境' in j.get('name', ''):
        s = j.get('state', {})
        print(f\"{j['name']}: last={s.get('lastRunStatus')}, consecutive={s.get('consecutiveErrors')}\")
"

# 2. 本月日志目录是否存在
ls -la ~/.openclaw/workspace/memory/logs/2026/

# 3. Hippocampus hook 是否在监听
ls -la ~/.openclaw/hooks/hippocampus/hook.py

# 4. 最近的梦境报告
ls -lt ~/.openclaw/workspace/memory/dreams/ | head -5

# 5. M-FLOW 图状态
cat ~/.openclaw/workspace/memory/graph/index.json 2>/dev/null | python3 -m json.tool | head -20

# 6. RAG 状态
python3 ~/SharedSkills/dream-selfimproving/scripts/longterm_rag.py --status
```

## 常见失败模式

| 症状 | 原因 | 修复 |
|------|------|------|
| 梦境报告条目全是0 | 本月日志目录不存在 | `mkdir -p ~/.openclaw/workspace/memory/logs/2026/05` |
| Cron 显示 interrupted | Gateway 重启中断了运行中任务 | 下次自动重试，无需手动修复 |
| consecutiveErrors > 0 | 任务超时或被中断 | 检查 `~/.openclaw/cron/runs/` 日志 |
| 蓝斑核健康 0/100 | 没有新日志/recall store 为空 | 正常现象，新的一天开始时会恢复 |

## Cron Jobs（当前配置）

| ID | 名称 | 时间 | 上次状态 |
|----|------|------|---------|
| eeb00ae0 | 梦境技能-早间蒸馏 | 07:00 | error (gateway 重启) |
| fc30089a | 梦境技能-晚间蒸馏 | 22:00 | ok |
| b00b50fc | 每日技能积分榜快照 | 23:00 | ok |

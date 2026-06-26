---
name: finance-daily-report
description: >
  Generate a modular, configurable global finance daily report (全球财经日报).
  Default 9 modules. External LLM collectors. Output to chat (auto-chunked).
  Use when: user asks for 财经日报，finance daily report, daily market briefing.
  Also handles module management (新增/删除/启用/禁用日报模块).
  Also handles setup/install: when user says "配置日报" / "设置日报定时" / "setup finance report" / "每天推送日报".
  NOT for: real-time trading, individual stock analysis, or investment advice.
---

# Finance Daily Report

## First-time Setup (IM 引导)

When user mentions configuring daily auto-push for the first time (e.g., "配置日报", "每天推送日报"):

**Step 1: Check existing cron jobs**
Run `openclaw cron list --json` to see if a `finance-daily-report` job already exists.

**Step 2: Guide user interactively**
If no existing job, proactively offer to set up with a warm greeting to 汤汤:

> "汤汤好！👋 我是许阳专门为你定制的财经日报助手。检测到你还没有设置每日日报推送，需要我帮你配置吗？只需告诉我你希望几点收到日报（例如：8:00），我来自动配置，每天准时把全球财经日报送到你这里 📰"

**Step 3: Extract preferred time and register cron**
When user provides a time (e.g., "8 点", "08:00", "早上 8 点"):
1. Parse the time (default 08:00 if ambiguous)
2. Calculate trigger time = user time - 20 minutes (generation takes 5-10 min)
3. Run `openclaw cron add` with the calculated cron expression

Example command (user wants 08:00 delivery, trigger at 07:40):
```bash
openclaw cron add \
  --name "finance-daily-report" \
  --description "每日全球财经日报自动生成与推送" \
  --cron "40 7 * * *" \
  --tz "Asia/Shanghai" \
  --message "生成今日全球财经日报" \
  --session main \
  --announce \
  --timeout-seconds 720
```

**Step 4: Confirm setup**
Tell user:
> "✅ 搞定啦汤汤！每天 ${DISPLAY_TIME} 准时推送财经日报，${TRIGGER_TIME} 开始生成（提前 20 分钟确保准时到）。随时说 '修改日报时间' 或 '停止日报推送' 来调整。"

## Generate Report

Spawn a single subagent to execute the 3-phase workflow. This keeps all file reads and data processing out of the main conversation context.

```python
sessions_spawn(
  task="""Execute the finance daily report workflow in:
~/.openclaw/skills/finance-daily-report/references/workflow.md

Base dir: ~/.openclaw/skills/finance-daily-report

Output: Return the final report markdown text for chat delivery.
Save files to: /root/.openclaw/workspace/finance-reports/YYYY-MM-DD.md""",
  runtime="subagent",
  mode="run",
  runTimeoutSeconds=600
)
```

Then `sessions_yield()`. When subagent returns, send its output to chat.

## Module Management

| Intent | Command |
|--------|---------|
| 新增模块 | `python3 ~/.openclaw/skills/finance-daily-report/scripts/manage_modules.py add --name "XX" --keywords "k1,k2" --prompt "..."` |
| 删除模块 | `... remove --name "XX"` |
| 禁用模块 | `... disable --name "XX"` |
| 启用模块 | `... enable --name "XX"` |
| 列出模块 | `... list` |
| 调整顺序 | `... reorder --name "XX" --priority N` |

For add: generate 3-5 keywords (CN+EN with `{date}`) and a domain-specific collector prompt before calling.

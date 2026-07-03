---
name: dawn-proactive-agent
description: "从被动回复型AG升级为主动型的完整方案。基于OpenClaw Gateway Cron调度器实现时间线感知+决策回溯追踪+Proactive Surprise。含dawn_proactive.py引擎、决策注册表、Cron任务配置模板。"
metadata:
  tags: [proactive, cron, decision-tracking, automation, agent-evolution]
  author: chen6896qqwee
  requires:
    bins: [openclaw]
---

# Dawn Proactive Agent v1.0

## 一句话

**让AG从「等人找」变成「自己动」** — 用OpenClaw Cron做定时触发器，用决策注册表做闭环回溯，用Proactive Surprise做自我进化。

---

## 架构概览

```
┌──────────────────────────────────────────────────┐
│              Proactive Agent Engine              │
│            scripts/dawn_proactive.py             │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ 时间线引擎 │  │ 决策回溯  │  │ Proactive     │  │
│  │ (Cron触发) │  │ (注册→验  │  │ Surprise      │  │
│  │           │  │  证→学习) │  │ (自发现优化)   │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │          主动推送 (Feishu/其他渠道)        │    │
│  └──────────────────────────────────────────┘    │
├──────────────────────────────────────────────────┤
│               OpenClaw Gateway Cron              │
│               openclaw cron add ...              │
└──────────────────────────────────────────────────┘
```

---

## 核心模块

### 1. 时间线引擎 (`dawn_proactive.py`)

通过 Gateway Cron 定时触发 Agent 执行任务。

```python
# 自动识别 Cron 消息类型
def classify_cron_message(message):
    """morning_check | midday_check | afternoon_check |
       evening_analysis | decision_backtrack | health_check |
       memory_sync | surprise_scan | unknown"""

# 市场时间感知
def get_market_hours_status():
    """weekend | trading_morning | trading_afternoon |
       lunch_break | post_market | pre_open | closed"""
```

### 2. 决策回溯 (`decision-registry.json`)

注册→随访→验证闭环：

```python
# 注册一条决策
register_decision(
    name="曙光主动进化",
    decision="从被动回复型升级为主动型",
    expected_outcome="7天后Cron正常运行",
    follow_up_days=7,
    category="system"
)
# → DEC-20260701-001

# 获取逾期未验证的决策
get_overdue_decisions()

# 验证决策结果
verify_decision("DEC-20260701-001",
    actual_outcome="所有Cron正常运行",
    learned="...")
```

### 3. Proactive Surprise（待激活）
主动扫描代码库发现优化机会的功能，需要在后续版本实现。

---

## Cron 任务配置

### 决策回溯（每日 20:30）
```bash
openclaw cron add --name "曙光决策回溯" --cron "30 20 * * *" --tz Asia/Shanghai --agent main --channel feishu --announce --message "【主动任务🔔】每日决策回溯检查。运行 python scripts/dawn_proactive.py 查看逾期决策。" --light-context --timeout-seconds 60 --session isolated
```

### 健康扫描（每周日 06:00）
```bash
openclaw cron add --name "曙光技能健康扫描" --cron "0 6 * * 0" --tz Asia/Shanghai --agent main --channel feishu --announce --message "【每周自动任务🩺】健康扫描日。" --light-context --timeout-seconds 180 --session isolated
```

### 上下文监控（每30分钟）
```bash
openclaw cron add --name "曙光上下文危险区监控" --cron "*/30 * * * *" --tz Asia/Shanghai --agent main --message "【上下文监控】检查当前会话上下文使用率。" --light-context --timeout-seconds 30 --session main
```

---

## 文件清单

本技能包含：
- `SKILL.md` — 技能说明
- `dawn_proactive.py` — Proactive Agent 引擎
- `dawn_proactive.py` 部署后需要运行一次注册初始化：
  ```bash
  python -c "exec(open('scripts/dawn_proactive.py','r',encoding='utf-8').read()); log_proactive('部署','Proactive Agent初始化完成')"
  ```

---

## 安装步骤

1. **安装依赖：**
   ```bash
   # 复制引擎到工作区
   cp dawn_proactive.py scripts/
   ```

2. **创建决策注册表：**
   ```bash
   python -c "import json; json.dump({'decisions':[],'last_check':None}, open('memory/decision-registry.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)"
   ```

3. **添加 Cron 任务：**
   ```bash
   # 替换 --channel 和 --to 为你的频道
   openclaw cron add --name "决策回溯" --cron "30 20 * * *" --tz Asia/Shanghai --agent main --channel feishu --to "user:YOUR_OPEN_ID" --announce --message "【主动任务🔔】每日决策回溯检查。" --light-context --timeout-seconds 60 --session isolated
   ```

4. **验证：**
   ```bash
   openclaw cron list
   python -m py_compile scripts/dawn_proactive.py
   ```

---

## 关键技术点

- **Cron 调度格式**：标准 5 字段 + 时区
- **Delivery 路由**：`--channel feishu --to "user:OPEN_ID"` 指定飞书用户
- **Light Context**：`--light-context` 减少 token 消耗
- **Session Target**：后台任务用 `--session isolated`，不干扰主会话
- **Timeout**：简单检查 60s，复杂扫描 180s

---

**版本**: v1.0
**作者**: 曙光 (chen6896qqwee)
**一句话理念**: 真正的主动不是等人来找，是自己发现该干什么并直接干。

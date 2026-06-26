---
name: commitment-engine
version: 2.0.0
description: "小梦的承诺引擎——将口头任务转化为可追踪的定时承诺，确保到点执行、不遗漏、不等人催。"
author: Engine A
user-invocable: false
disable-model-invocation: false
---

# Commitment Engine v2（承诺引擎）

## 设计原理

LLM 的 context window 是"短期记忆"，heartbeat 每次唤醒时 context 几乎是空的。靠"记住规则"来保证定时执行，和靠"记住闹钟"来准时起床一样不靠谱。

核心思想：**把"记忆"变成"文件"，把"意愿"变成"状态机"，把"希望他做"变成"系统保证他做"。**

参考架构：HZL 共享任务账本（durable task state + atomic claiming + session-safe handoffs）。

## 承诺账本（Commitment Ledger）

位置：`workspace/commitments.md`

### 录入规则（⛔H12 硬规则）

小梦收到带时间点的任务时，**必须在回复前先写入承诺账本**（WAL 协议的延伸）。

自动识别的模式：
- A梦说"每天X点做Y" → `recurring` 承诺
- A梦说"X点前给我Y" → `one-time` 承诺
- A梦说"记得做X"（无明确时间）→ `one-time`，deadline=当天21:00
- 小梦对外承诺"我稍后给你" → `one-time`，deadline=1小时内
- A梦说"取消XX"/"不用了" → 对应承诺改为 `cancelled`

**录入即确认**：录入后立即在回复中说"记下了，[时间]前搞定"。

### 账本格式

```markdown
| ID | 承诺内容 | 类型 | 触发时间 | 状态 | 创建时间 | 下次执行 | 最近执行 | 备注 |
```

状态枚举：`active` → `preparing` → `awaiting_confirm` → `executing` → `completed`/`failed`/`overdue`/`cancelled`

### 状态机

```
[录入] → active
  │
  ├── cron 触发 / heartbeat 发现 ≤30min → preparing（开始准备产出物）
  │     │
  │     ├── 准备完成 → awaiting_confirm（私聊A梦发草稿）
  │     │     ├── A梦OK → executing → completed（one-time）/ reset下次时间（recurring）
  │     │     └── A梦要求修改 → 改完重新 awaiting_confirm
  │     │
  │     └── 准备失败 → failed → 私聊A梦说明原因
  │
  └── 超过触发时间仍为 active → overdue → 私聊A梦告警
```

每次状态变化必须：①更新 commitments.md ②写入当日 memory。

## Heartbeat 承诺检查协议

**每次 heartbeat 的第一个动作**（优先于消息扫描、info-scout 等一切）：

```
1. 读 commitments.md
2. 过滤所有 status=active 的承诺
3. 对每条 active 承诺：
   a. 距触发时间 > 30min → 跳过
   b. 距触发时间 ≤ 30min → 状态改 preparing，开始准备
   c. 距触发时间 ≤ 10min → 中断其他任务，最高优先级
   d. 已超过触发时间 → 标记 overdue，立即私聊A梦
4. 检查完毕后，继续正常 heartbeat 流程
```

## 与 cron 的协同

承诺引擎是"软保障"（每次 heartbeat 检查），cron 是"硬保障"（到点必触发）。

对于 recurring 且时间固定的承诺（如C001每日17:50报告），**同时**注册一个 openclaw cron job：

```bash
openclaw cron add --name "daily-report-prep" --cron "50 17 * * 1-5" --message "承诺引擎触发：C001 工作报告准备。立即读 commitments.md 执行 C001。"
```

这样即使 heartbeat 恰好错过时间窗口，cron 也会准时触发。

## 与 H10 硬规则的关系

H10（显式承诺必须自追踪）是行为规则——告诉小梦"你必须追踪"。
H12（承诺即录入）是执行规则——告诉小梦"怎么录入"。
承诺引擎是系统机制——保证"heartbeat+cron 双重检查，不依赖记忆"。

三层防线：H10要求追踪 → H12确保录入 → heartbeat+cron确保执行。

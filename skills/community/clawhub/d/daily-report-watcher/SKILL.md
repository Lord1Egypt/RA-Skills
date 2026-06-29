---
name: daily-report-watcher
description: "Lightweight watchdog for daily report cron failures — independent Feishu alerter that doesn't rely on OpenClaw's failureAlert. 30-min checks, 4h cooldown, 36h error window."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡",
        "requires": { "bins": ["openclaw", "python3"] },
        "config": ["channels.feishu.accounts.codebot"]
      }
  }
---

# Daily Report Watcher

> **作者**: 码虫 🐛 (coding-advisor)
> **版本**: v1.1
> **创建**: 2026-06-14
> **更新**: 2026-06-14 19:57 — 频次从 8:30 单次升级为每 30 分钟一次（老板嫌少）
> **来源**: 老板选 B（写轻量 watcher 兜底）

## 背景

**2026-06-12 周五 19:30 码虫日报 cron 失败 → 沉默 2 天**才被发现（ERR-20260614-001）

### 3 层根因
1. M3 `overloaded`（首跑 188s）
2. OpenClaw `update_goal` fail（重试 65s，**平台层 bug**）
3. `failureAlert` 投递也失败 → 老板完全不知道

### 沉默 2 天的根本原因
- HEARTBEAT.md 记录 `ba67d0ff`（日报监控-每30分）仍存在
- 实际 `openclaw cron get ba67d0ff` → **cron job not found**
- 监控任务早已消失，无人兜底

## 功能

**完全独立的应用层兜底**，不依赖 OpenClaw 平台告警：

| 检查项 | 说明 |
|--------|------|
| Cron status | `openclaw cron get` 查 `lastRunStatus / lastDelivered / consecutiveErrors` |
| 日报文件 | 检查 `memory/daily-reports/YYYY-MM-DD.md` 是否存在 |
| 时间窗口 | 只检查过去 36h 内的失败（避免旧错误持续告警）|
| 静默期 | 告警后 4 小时内不重复（避免轰炸）|
| 周末感知 | 周末检查最近一个工作日 |

## 触发方式

设计为 cron 任务，**每 30 分钟一次**（24h 不间断）：
- 还原原 ba67d0ff 设计
- watcher 跑得快（1-2s），无资源压力
- 24h 覆盖，包括周末和夜间
- 下次运行：自动每 30 分钟

## Cron 配置

- **Job ID**：`33fd7b32-4f1c-46fe-b102-0b29143bc37b`
- **Name**：🛡 码虫日报watcher兜底-每30分
- **Schedule**：`every 30m`
- **Command**：`python3 .../watcher.py`（纯命令，不需 LLM）
- **Timeout**：180s（低风险检查任务）
- **FailureAlert**：after:1, cooldown:4h, channel:feishu, account:codebot
- **首次自动运行**：2026-06-14 19:57（已通过 force run 验证 ok 2.4s）

## 用法

```bash
# 正常运行（按需告警）
python3 skills/daily-report-watcher/watcher.py

# 试运行（不真发告警）
python3 skills/daily-report-watcher/watcher.py --dry-run

# 只检查，exit code 反映结果
python3 skills/daily-report-watcher/watcher.py --check-only
# exit 0 = 正常, 1 = 异常, 2 = 检查出错
```

## 输出示例

### 正常情况
```
[2026-06-14 19:44:30] daily-report-watcher 启动
  昨天日期: 2026-06-13 (周末)
  最近工作日: 2026-06-12
  上次状态: ok (consecutive: 0)
  上次运行: 2026-06-12 19:35:58
  上次送达: True
  检查文件: .../2026-06-12.md → 存在
[OK] 日报状态正常
```

### 异常情况
```
[2026-06-15 08:30:00] daily-report-watcher 启动
  ...
  上次状态: error (consecutive: 1)
  检查文件: .../2026-06-12.md → ❌ 缺失
[ALERT] 发现异常: 日报任务 status=error + 日报 markdown 文件缺失
[SEND] 发送飞书告警...
[OK] 告警已发送
```

## 告警格式（飞书 post）

```
🚨 码虫日报异常：日报任务 status=error, delivered=False + 日报 markdown 文件缺失
━━━━━━━━━━━━━━━━━━━━
📅 检查时间：2026-06-15 08:30:00
📂 目标日报：2026-06-12
🔴 异常原因：...
📊 Cron 状态：...
🔍 诊断信息：...
📁 文件路径：...
🛠 建议处理：
1. ...
━━━━━━━━━━━━━━━━━━━━
🔧 手动处理：检查 memory/daily-reports/ 是否缺失文件，按需补发
```

## 沉淀规则

- **RULE-20260614-001**（候选 HOT）：cron 失败 → 立即写文件兜底 + 不打扰老板原则
- **LESSON-20260614-001**（已写入 ERR-20260614-001）：
  1. update_goal fail ≠ 内容失败（OpenClaw 平台层 bug）
  2. 失败连续 2 次才算真失败
  3. 日报必须有显式 failureAlert
  4. 沉默失败最危险（HEARTBEAT.md 与实际状态可能漂移）

## 验证

```bash
# 测试 1：dry-run 看是否会告警
python3 skills/daily-report-watcher/watcher.py --dry-run

# 测试 2：check-only 拿到 exit code
python3 skills/daily-report-watcher/watcher.py --check-only
echo $?

# 测试 3：cron run force
openclaw cron run 33fd7b32-4f1c-46fe-b102-0b29143bc37b --wait
```

## 依赖

- `openclaw` CLI（系统命令）
- `requests`（pip 已装）
- `scripts/feishu_post.py`（复用飞书发送器）
- `~/.openclaw/openclaw.json`（飞书凭证）

## 已知限制

- 只监控 19:30 日报任务（6ade489c），其他日报需另写
- 告警内容由 watcher 主动生成（不读日报内容）
- 静默期 4 小时（可调）

## 后续优化（30 天观察期）

- [ ] 30 天后评估告警质量（误报率/漏报率）
- [ ] 如稳定 → 晋升为 HOT-20260614-001
- [ ] 考虑监控其他日报任务（编程案例/每日灵感等）
- [ ] 集成到 daily-precheck.cjs（统一预检）

---

_🤖 码虫 🐛 | 用代码解放双手 | 2026-06-14_

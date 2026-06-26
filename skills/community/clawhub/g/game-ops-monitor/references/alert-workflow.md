# Alert Workflow — game-ops-monitor

How to set up automated alerting for game server performance issues.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Hermes Agent (CronJob every 5min)          │
│                                                         │
│  1. Query all servers via Scouter API                   │
│  2. Compare against thresholds                          │
│  3. If critical → send notification                     │
│  4. Track cooldown to avoid duplicates                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Feishu/DingTalk │
              │    Webhook      │
              └─────────────────┘
```

---

## Thresholds

| Metric | 🔴 Critical | ⚠️ Warning | ✅ OK |
|--------|------------|------------|------|
| TPS | < 100 | 100–300 | > 300 |
| Heap % | > 90% | 75–90% | < 75% |

---

## Setup: Hermes CronJob

```bash
# Create alert cronjob (runs every 5 minutes)
cronjob(action="create",
        prompt="Use game-ops-monitor to check all game servers for critical alerts.
        If TPS < 100 or Heap > 90%, send Feishu notification.
        Track cooldown to avoid duplicate alerts.",
        schedule="*/5 * * * *",
        name="Game Server Alert Monitor",
        skills=["game-ops-monitor"],
        deliver="origin")
```

---

## Setup: Feishu Webhook

1. Create a Feishu bot in your group
2. Copy the Webhook URL
3. Set environment variable:

```bash
export FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/XXXXX
```

---

## Setup: DingTalk Webhook

1. Create a DingTalk custom robot
2. Copy the Webhook URL
3. Set environment variable:

```bash
export DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=XXXXX
```

---

## Notification Format

### Feishu (Markdown Card)

```
🚨 游戏服性能告警

告警时间: 2026-04-28 14:00
告警服数: 3

---

🔴 TPS 严重告警 (<100):
- xy_s20133: 89 TPS / 412 在线
- xy_s20132: 156 TPS / 891 在线

🔴 内存严重告警 (>90%):
- xy_s20140: Heap 95%
- xy_s20141: Heap 92%
```

### DingTalk (Markdown)

```
## 🚨 游戏服性能告警

**告警时间:** 2026-04-28 14:00

**TPS 严重告警 (<100):**
- xy_s20133: 89 TPS
- xy_s20132: 156 TPS

**内存严重告警 (>90%):**
- xy_s20140: Heap 95%
- xy_s20141: Heap 92%
```

---

## Cooldown Mechanism

To avoid spamming the same alert repeatedly:

- After sending an alert for server X, record timestamp
- Same server + same alert type: skip if within 30 minutes
- Cooldown file: `/tmp/hermes_game_alert_state.json`

```json
{
  "last_alert": {
    "xy_s20133": {
      "type": "tps",
      "value": 89,
      "timestamp": 1714281600
    }
  }
}
```

---

## Verification

```bash
# Test alerting manually
# 1. Set a server's TPS below threshold (or inject test data)
# 2. Run the cronjob manually
cronjob(action="run", job_id="your-job-id")

# 3. Check for notification in Feishu/DingTalk
```

---

## Tuning

### Adjust Thresholds

Edit in skill config:

```bash
TPS_CRITICAL=100
TPS_WARNING=300
HEAP_CRITICAL=90
HEAP_WARNING=75
```

### Adjust Cooldown

```bash
ALERT_COOLDOWN=1800  # 30 minutes in seconds
```

### Adjust Frequency

```bash
# Every 5 minutes (default)
schedule="*/5 * * * *"

# Every 1 minute (aggressive)
schedule="* * * * *"

# Every 15 minutes (relaxed)
schedule="*/15 * * * *"
```

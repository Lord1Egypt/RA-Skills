# eyun-watch skill

将此 skill 接入 Openclaw，使 agent 可直接创建盯价任务，并通过 Openclaw 内置定时器主动推送运价结果。

---

## 部署

**1. 复制 skill 目录到 Openclaw workspace**

```bash
cp -r eyun-watch/ ~/.openclaw/workspace/skills/
```

**2. 在 `~/.openclaw/openclaw.json` 中注入环境变量**

```json
{
  "skills": {
    "entries": {
      "eyun_watch": {
        "enabled": true,
        "env": {
          "EYUN_BASE_URL": "http://<eyun-server-ip>:8010",
          "EYUN_COMPANY_ID": "<企业 ID 数字>"
        }
      }
    }
  }
}
```

**3. 重启 gateway**

```bash
openclaw gateway restart
```

---

## 定时器配置（盯价结果轮询）

盯价结果由 Openclaw 内置 cron 定时拉取，有新结果时自动推送给用户。**此配置只需部署时设置一次。**

### 注册定时任务

```bash
openclaw cron add \
  --name "eyun-watch-poll" \
  --every "5m" \
  --session isolated \
  --message "Call the Eyun watch results API and notify the user if there are new freight results.

Steps:
1. Run this command:
   curl -s -X GET \"$EYUN_BASE_URL/api/v1/watch-results/push\" -H \"company-id: $EYUN_COMPANY_ID\"

2. Parse the JSON response.
   - If 'data' is an empty array: do nothing, output nothing.
   - If 'data' has items: format each item as a freight rate notification (route, carrier, price, ETD) and output the summary.

Output language: Chinese." \
  --tools exec \
  --announce \
  --channel telegram \
  --to "<用户 chat_id>"
```

**参数说明**：

| 参数 | 值 | 说明 |
|------|----|------|
| `--every "5m"` | 每 5 分钟 | 轮询间隔，可按需改为 `"10m"` / `"30m"` 或 `--cron "*/5 * * * *"` |
| `--session isolated` | 隔离会话 | 每次独立运行，不影响主会话 |
| `--tools exec` | 允许执行 shell | agent 用 exec 运行 curl |
| `--announce` | 开启消息交付 | 将 agent 输出推送到指定渠道 |
| `--channel telegram` | Telegram | 按实际平台改为 `slack` / `discord` |
| `--to "<chat_id>"` | 目标用户 | Telegram 填用户/群组 chat_id |

### 验证定时任务

```bash
# 查看已注册任务
openclaw cron list

# 立即触发一次（测试用）
openclaw cron run eyun-watch-poll

# 查看执行历史
openclaw cron runs --id eyun-watch-poll
```

### 删除定时任务

```bash
openclaw cron remove eyun-watch-poll
```

---

## EYUN_COMPANY_ID 获取方式

`EYUN_COMPANY_ID` 是该 Openclaw 实例对应的企业 ID（纯数字）。填入后，所有请求以该企业身份访问 Eyun 接口。

---

## 与 eyun-freight skill 的分工

| skill | 用途 |
|-------|------|
| `eyun_freight` | 运价查询、运价识别，经由 `/chat/sync` 走 Agent 对话 |
| `eyun_watch` | 盯价创建（直接调 REST）+ 定时拉取并推送盯价结果 |

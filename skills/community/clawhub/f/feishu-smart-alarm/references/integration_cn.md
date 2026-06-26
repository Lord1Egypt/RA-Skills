# 飞书接入说明

## 目标

这个 Skill 用于在飞书消息流中识别“需要提醒”的文本，并在由系统根据消息语义和时间跨度自动判断，更偏宽松一点的预留时间提醒一次。

## 推荐接法

### 1. 每条飞书消息都先调用 `create-reminder`

示例：

```bash
python scripts/main.py create-reminder \
  --text "今天 5 点前给我" \
  --receive-id oc_xxx \
  --receive-id-type chat_id \
  --sender-open-id ou_xxx \
  --sender-name 张三
```

### 2. 如果返回 `need_reminder=false`

继续原有普通聊天逻辑，不需要建立提醒。

### 3. 如果返回 `need_reminder=true`

表示已经：

- 建立提醒记录
- 立刻发送确认消息 `我已经记住并在$时间点$提醒`

### 4. 常驻运行提醒轮询

在服务器上常驻一个进程：

```bash
python scripts/main.py run-loop --interval 30
```

该进程会每 30 秒检查一次 SQLite 中是否有到期提醒，并发送回原飞书会话。

## PicoClaw 中的建议行为

对每条飞书消息执行：

1. 先调用本 Skill 的 `create-reminder`
2. 若未识别到提醒，继续普通聊天
3. 若识别到提醒，则发送确认消息后继续普通聊天或结束当前轮次，取决于你的业务设计

## receive_id_type 说明

- 群聊通常使用 `chat_id`
- 私聊通常可以使用 `open_id`

如果你希望提醒发回原会话，建议直接存下飞书事件里原始可用的 `chat_id` 或 `open_id`。

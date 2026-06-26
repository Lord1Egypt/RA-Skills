# 飞书接入说明

## 目标

这个 Skill 用于在飞书消息流中识别“需要提醒”的**文本或语音**内容，并在由系统根据消息语义和时间跨度自动判断、更偏宽松一点的预留时间提醒一次。

## 运行前置条件

必须由运行时注入以下环境变量：

```env
FEISHU_APP_ID=...
FEISHU_APP_SECRET=...
SENSEAUDIO_API_KEY=...
```

可选：

```env
FEISHU_SMART_ALARM_DB=./data/reminders.db
FEISHU_SMART_ALARM_TZ=Asia/Shanghai
SENSEAUDIO_BASE_URL=https://api.senseaudio.cn
SENSEAUDIO_ASR_MODEL=sense-asr
```

硬约束：

- 不读取 `.env` / `.env.local`
- 不在运行时临时询问 API Key
- 缺少 `SENSEAUDIO_API_KEY` 时，不允许进入语音分析或语音建提醒流程

## 推荐接法

### 文本消息：每条飞书文本先调用 `create-reminder`

示例：

```bash
python scripts/main.py create-reminder \
  --text "今天 5 点前给我" \
  --receive-id oc_xxx \
  --receive-id-type chat_id \
  --sender-open-id ou_xxx \
  --sender-name 张三
```

### 语音消息：先下载到本地，再调用 `create-reminder-audio`

示例：

```bash
python scripts/main.py create-reminder-audio \
  --audio /abs/path/input.m4a \
  --receive-id oc_xxx \
  --receive-id-type chat_id \
  --sender-open-id ou_xxx \
  --sender-name 张三
```

这个命令内部会：

1. 调 SenseAudio ASR 转写语音
2. 根据转写文本分析是否需要建立提醒
3. 如果需要，则写入 SQLite
4. 立刻向原会话发送确认消息

## 返回结果理解

### 文本分析 / 建提醒
- `need_reminder`: 是否需要提醒
- `deadline_iso`: 识别出的截止时间
- `reminder_iso`: 计划提醒时间
- `confirm_text`: 立即回给用户的确认消息
- `reminder_text`: 到点要发出的提醒消息

### 语音分析 / 建提醒
除上面字段外，还会额外返回：

- `transcript`: ASR 转写结果
- `audio_path`: 本地音频路径
- `analysis_source`: 固定为 `audio`（分析场景）
- `source_type`: 固定为 `audio`（建提醒场景）

## 如果返回 `need_reminder=false`

继续原有普通聊天逻辑，不需要建立提醒。

## 如果返回 `need_reminder=true`

表示已经：

- 对文本或语音内容完成分析
- 建立提醒记录
- 立刻发送确认消息 `我已经记住并在$时间点$提醒`

## 常驻运行提醒轮询

在服务器上常驻一个进程：

```bash
python scripts/main.py run-loop --interval 30
```

该进程会每 30 秒检查一次 SQLite 中是否有到期提醒，并发送回原飞书会话。

## PicoClaw 中的建议行为

### 文本消息
1. 先调用本 Skill 的 `create-reminder`
2. 若未识别到提醒，继续普通聊天
3. 若识别到提醒，则发送确认消息后继续普通聊天或结束当前轮次，取决于你的业务设计

### 语音消息
1. 先把飞书语音下载到本地文件
2. 调用本 Skill 的 `create-reminder-audio`
3. 若未识别到提醒，继续普通聊天
4. 若识别到提醒，则发送确认消息后继续普通聊天或结束当前轮次，取决于你的业务设计

## receive_id_type 说明

- 群聊通常使用 `chat_id`
- 私聊通常可以使用 `open_id`

如果你希望提醒发回原会话，建议直接存下飞书事件里原始可用的 `chat_id` 或 `open_id`。

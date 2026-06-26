---
name: feishu-smart-alarm
description: 读取飞书/lark 的文本或语音消息，识别是否包含需要提醒的待办和截止时间，并根据消息语义和时间跨度自动判断一个偏宽松的提醒时间。适用于飞书机器人处理“今天 5 点前给我”“明天下午三点提醒我”“发语音说周五前记得提交”这类消息。支持先用 senseaudio asr 把语音转文字，再分析并建立提醒；启用 asr 时会把传入的本地音频上传到配置的 senseaudio 接口。会将提醒持久化到本地 sqlite，并使用飞书应用凭证向原会话发送确认消息和到点提醒。当前版本硬性要求通过进程环境变量提供 feishu_app_id、feishu_app_secret、senseaudio_api_key；不会读取 .env / .env.local，也不会临时提示输入。
metadata:
  required_env_vars:
    - FEISHU_APP_ID
    - FEISHU_APP_SECRET
    - SENSEAUDIO_API_KEY
  optional_env_vars:
    - FEISHU_BASE_URL
    - SENSEAUDIO_BASE_URL
    - REMINDER_DB_PATH
    - TIMEZONE
  external_network:
    - asr 会把传入的本地音频上传到配置的 SenseAudio API（默认 https://api.senseaudio.cn）
    - 飞书确认消息和提醒消息会发送到配置的 Feishu API（默认 https://open.feishu.cn）
  persistence:
    - 提醒内容与状态会持久化到本地 SQLite（默认 ./data/reminders.db）
  credentials_policy:
    - 仅从进程环境变量读取凭证，不读取 .env / .env.local，不提供临时输入兜底
---

# Feishu Smart Alarm

## 概述

这个 Skill 用于在飞书消息中自动识别“需要在某个时间前提醒”的内容，并完成四类动作：

1. 读取**文本消息**并判断是否需要建立提醒
2. 读取**语音消息**，先调用 SenseAudio ASR 转写，再判断是否需要建立提醒
3. 解析截止时间，并计算**由系统根据消息语义和时间跨度自动判断，更偏宽松一点的预留时间** 的提醒时间
4. 立即在原会话发送确认消息：`我已经记住并在$时间点$提醒`
5. 到点后仅提醒一次，并把提醒发回原飞书会话

默认约定：

- 支持飞书**文本消息**和**语音消息**
- 语音消息必须先落到本地文件，再把本地路径传给脚本
- 默认提醒对象是**原消息发送者**
- 默认把提醒消息发回**原飞书会话**
- 每条提醒**只发送一次**
- 默认时区：`Asia/Shanghai`

## 适用消息

优先识别以下类型：

- `今天 5 点前给我`
- `明天下午三点提醒我开会`
- `周五前记得把这个提交`
- `今晚 8 点前把材料发我`
- `后天上午记得找我确认`
- `下周一 10 点别忘了评审`
- 语音里说：`周五前提醒我把材料发出去`
- 语音里说：`明天下午三点提醒我开会`

## 不建立提醒的情况

以下情况默认不建提醒：

- 纯闲聊，没有任务或截止语义
- 没有可解析时间
- 明显是历史回顾而非未来待办
- 时间解析结果早于当前时间且无法合理滚动到未来
- 语音转写成功，但转写文本不包含提醒/待办语义

## 时间解析规则

脚本支持以下常见时间表达：

- 绝对时间：`2026-03-20 15:00`、`2026/3/20 15:00`
- 月日时间：`3月20日 15:00`、`3月20号下午3点`
- 相对日期：`今天`、`明天`、`后天`
- 周几：`周一`、`周五`、`下周二`
- 时段：`上午`、`中午`、`下午`、`晚上`、`凌晨`
- 纯时间：`5点`、`5:30`、`下午三点`

默认补全策略：

- 仅有日期但无具体时间：默认 `18:00`
- 仅有“上午 / 下午 / 晚上”无具体小时：分别默认 `10:00 / 15:00 / 20:00`
- 仅有纯时间且今日该时刻已过：顺延到明天

## 消息分析规则

建立提醒必须同时满足：

1. 能解析出未来时间
2. 消息里存在待办/提醒/截止语义中的至少一种

强触发关键词示例：

- `提醒`
- `记得`
- `别忘`
- `截止`
- `前给我`
- `前发我`
- `前提交`
- `要做`
- `要交`
- `开会`
- `评审`
- `确认`
- `安排`

如果消息虽然没有“提醒”字样，但具有明显的“任务 + 时间”结构，也可以建立提醒。

## 确认消息规则

一旦建立提醒，必须立刻在原会话发送确认消息：

`我已经记住并在$时间点$提醒`

其中 `$时间点$` 填入**提醒时间**，不是截止时间。例如：

- `今天 17:00 前给我` → 可能提醒在 `16:20` 或 `15:30`，取决于任务紧急程度
- `下周一开会别忘了` → 可能更早预留数小时甚至前一天提醒
- 确认消息会使用系统自动判断出来的提醒时间

## 到点提醒规则

到达提醒时间后，发送一次提醒消息到原飞书会话。

建议提醒模板：

- 私聊：`提醒你：{summary}（截止时间 {deadline_text}）`
- 群聊：`提醒 {sender_name}：{summary}（截止时间 {deadline_text}）`

发送成功后，将提醒状态标记为已发送，不再重复提醒。

## 环境变量（硬性要求）

当前版本硬性要求以下环境变量由运行时注入：

```env
FEISHU_APP_ID=...
FEISHU_APP_SECRET=...
SENSEAUDIO_API_KEY=...
```

可选项：

```env
FEISHU_BASE_URL=https://open.feishu.cn
FEISHU_SMART_ALARM_DB=./data/reminders.db
FEISHU_SMART_ALARM_TZ=Asia/Shanghai
SENSEAUDIO_BASE_URL=https://api.senseaudio.cn
SENSEAUDIO_ASR_MODEL=sense-asr
```

强约束：

1. 不读取 `.env`、`.env.local` 或其他本地配置文件
2. 不在交互式终端里临时询问 API Key
3. 缺少 `SENSEAUDIO_API_KEY` 时，所有音频相关入口必须直接失败
4. 缺少 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 时，所有发送确认或发送提醒的入口必须直接失败

## 脚本入口

### 1. 分析文本消息

```bash
python scripts/main.py analyze-message --text "今天 5 点前给我"
```

### 2. 先转写语音，再只做分析

```bash
python scripts/main.py analyze-audio --audio /abs/path/input.m4a --sender-name 张三
```

返回：

- 语音转写结果 `transcript`
- 是否需要提醒
- 解析到的截止时间
- 提醒时间
- 确认消息

### 3. 只做 ASR 转写

```bash
python scripts/main.py transcribe-audio --audio /abs/path/input.m4a
```

### 4. 根据文本建立提醒并立即回确认

```bash
python scripts/main.py create-reminder \
  --text "今天 5 点前给我" \
  --receive-id oc_xxx \
  --receive-id-type chat_id \
  --sender-open-id ou_xxx \
  --sender-name 张三
```

### 5. 根据语音建立提醒并立即回确认

```bash
python scripts/main.py create-reminder-audio \
  --audio /abs/path/input.m4a \
  --receive-id oc_xxx \
  --receive-id-type chat_id \
  --sender-open-id ou_xxx \
  --sender-name 张三
```

这个命令会：

- 先用 SenseAudio ASR 转写语音
- 按转写结果判断是否需要提醒
- 如有提醒需求则存入本地 SQLite
- 立刻向原会话发送确认消息

### 6. 轮询并发送到期提醒

```bash
python scripts/main.py poll-due
```

### 7. 以常驻循环方式运行

```bash
python scripts/main.py run-loop --interval 30
```

表示每 30 秒检查一次是否有到期提醒。

## 与 PicoClaw 的接法

推荐在飞书消息进入后这样使用：

### 文本消息
1. 对文本消息调用 `create-reminder`
2. 如果返回 `need_reminder=false`，继续普通聊天逻辑
3. 如果返回 `need_reminder=true`：
   - 确认消息已发出
   - 后台由 `run-loop` 常驻检查并在到点时发送提醒

### 语音消息
1. 先把飞书语音下载到本地临时文件
2. 对本地文件调用 `create-reminder-audio`
3. 如果返回 `need_reminder=false`，继续普通聊天逻辑
4. 如果返回 `need_reminder=true`：
   - 确认消息已发出
   - 后台由 `run-loop` 常驻检查并在到点时发送提醒

更详细的接法见：

- `references/integration_cn.md`
- `references/time_rules_cn.md`

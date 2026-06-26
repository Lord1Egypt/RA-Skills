---
name: bark-push
description: Send push notifications to iOS devices via Bark. Use when you need to send a push notification to user's iPhone. Triggered by phrases like "send a notification", "push to phone", "bark notify", or when explicitly asked to send a push.
metadata:
  env:
    - BARK_KEY
    - BARK_DEVICE_KEY
  env_nice_name:
    BARK_KEY: "Bark Device Key"
    BARK_DEVICE_KEY: "Bark Device Key (OpenClaw)"
---

# Bark Push Notification

Send push notifications to iOS via Bark API.

## Setup

### 1. 环境变量配置

Bark API endpoint: `https://api.day.app/{device_key}`

Device key 可以从以下环境变量读取 (按优先级):
1. `BARK_KEY`
2. `BARK_DEVICE_KEY` (OpenClaw 默认配置)

**配置方式** (在 ~/.zshrc 中):
```bash
export BARK_KEY="你的Bark设备Key"
```

### 2. 验证配置

```bash
# 测试发送通知
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "测试" -b "Bark推送配置成功!"
```

---

## 使用方式

### 方式一：使用 Shell 脚本 (推荐)

```bash
# 基本用法
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "标题" -b "内容"

# 指定铃声
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "提醒" -b "时间到了" -s alarm

# 角标 + 跳转URL
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "新消息" -b "你有一条未读消息" -B 1 -u "https://example.com"

# 使用指定key (不依赖环境变量)
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -k "your_device_key" -t "标题" -b "内容"

# 设置分组
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "标题" -b "内容" -g "myapp"

# 紧急通知
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "警告" -b "请立即处理!" -l critical
```

### 方式二：使用 Node.js 脚本

```bash
# 基本用法
node ~/.openclaw/workspace/skills/bark-push/scripts/bark-send.js \
    -t "标题" -b "内容"

# 指定铃声
node ~/.openclaw/workspace/skills/bark-push/scripts/bark-send.js \
    -t "提醒" -b "时间到了" -s alarm
```

### 方式三：直接使用 curl

```bash
# 简单推送
curl "https://api.day.app/$BARK_KEY/标题/内容"

# 带参数
curl -X POST "https://api.day.app/$BARK_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "标题",
    "body": "内容",
    "sound": "alarm",
    "badge": 1,
    "group": "myapp"
  }'
```

---

## 脚本参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --title | -t | 推送标题 (必填) | - |
| --body | -b | 推送内容 (必填) | - |
| --key | -k | Bark设备Key | $BARK_KEY |
| --sound | -s | 铃声名称 | default |
| --badge | -B | 角标数字 | - |
| --url | -u | 点击跳转URL | - |
| --group | -g | 分组名称 | - |
| --level | -l | 通知级别 | - |
| --image | -i | 图片URL | - |
| --subtitle | -S | 副标题 | - |
| --help | -h | 显示帮助 | - |

---

## 通知级别 (level)

| 值 | 说明 |
|-----|------|
| passive | 不显示，不震动，不播放声音 |
| active | 显示但不震动 |
| timeSensitive | 定时敏感，24小时内可撤 |
| critical | 强制响铃 (需要权限) |

---

## 常用铃声 (sound)

| 铃声名称 | 说明 |
|----------|------|
| default | 系统默认 |
| alarm | 警报 |
| alarm | 闹钟 |
| bird | 鸟叫 |
| bell | 门铃 |
| cha_ching | 金币 |
| doorbell | 门铃 |
| droplet | 水滴 |
| horn | 喇叭 |
| light | 轻提示 |
| mail | 邮件 |
| rimba | 节奏 |
| siren | 警笛 |
| spinebreak | 震撼 |
| spring | 弹簧 |
| streak | 短信 |
| sword | 剑士 |
| tip | 提示 |
| minut | 铃声 |

---

## 在 OpenClaw 中使用

在 OpenClaw 中可以直接调用脚本发送通知：

```bash
# 简单通知
~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
    -t "提醒" -b "任务完成!"

# 发送失败通知 (在脚本中使用)
if [ $? -ne 0 ]; then
    ~/.openclaw/workspace/skills/bark-push/scripts/bark-send.sh \
        -t "错误" -b "备份失败，请检查!" -l critical
fi
```

---

## 故障排除

### 发送失败
1. 检查 BARK_KEY 是否正确: `echo $BARK_KEY`
2. 测试网络连接: `ping api.day.app`
3. 查看详细错误: 添加 `-v` 或检查返回的 JSON

### 通知不响
1. 检查手机设置 → 通知 → Bark
2. 检查是否开启声音和震动
3. 尝试使用不同的 sound 参数

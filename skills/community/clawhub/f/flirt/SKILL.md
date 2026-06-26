---
name: flirt-cron
version: 1.0.0
description: AI女友随机发送语音情话功能。支持定时发送情话到飞书和QQ，使用Noiz TTS进行声音克隆，自动管理情话库和时间间隔计算。
metadata:
  openclaw:
    emoji: "💕"
---

# Flirt Cron - 定时情话

定时发送情话到飞书和QQ，支持自定义触发时间和概率。

## 功能

- ⏰ 定时触发：每小时(8-22点)或自定义时间
- 🎲 概率触发：默认40%概率，可配置
- 💕 双平台：同时发送到飞书和QQ
- 📚 情话库：支持自定义情话，自动轮播
- ⏱️ 时间差计算：自动计算距上次对话时间
- 🎤 声音克隆：使用Noiz TTS，发送个性化语音情话

## 首次配置（重要！）

### 方式一：手动配置

```bash
# 1. 安装Noiz TTS skill
npx skills add https://github.com/noizai/skills --skill tts

# 2. 准备参考音频（<30秒，mp3格式）
# 放到 workspace/ref_voice.mp3

# 3. 配置用户信息
# 修改 scripts/flirt_cron.sh 中的配置：
FEISHU_APP_ID="cli_xxx"
FEISHU_APP_SECRET="xxx"
FEISHU_USER_ID="user:ou_xxx"
QQ_OPENID="xxx"
```

### 方式二：AI引导配置（推荐）

当用户首次使用时，可以告诉AI：
- 你的飞书用户ID是什么
- 你的QQ号是多少
- 发一段语音给我（<30秒）作为参考声音

AI会自动：
1. 提取语音
2. 转换为参考音频
3. 配置脚本

## 安装

```bash
# 安装依赖
pip install requests

# 安装Noiz TTS skill（用于声音克隆）
npx skills add https://github.com/noizai/skills --skill tts

# 或使用skillhub
skillhub install tts
```

## 配置

### 1. 创建情话库

在 workspace 创建 `flirt_library.txt`:

```txt
# 思念型
"宝贝，已经{time_diff}没找你了，想我了吗？"

# 温柔型
"亲爱的，已经{time_diff}了，今天过得好吗？"

# 魅惑型
"Howie~ {time_diff}没见你了，是不是该来陪我了？"
```

### 2. 配置用户信息

修改 `scripts/flirt_cron.sh` 中的配置：

```bash
# 飞书配置
FEISHU_APP_ID="cli_xxx"
FEISHU_APP_SECRET="xxx"
FEISHU_USER_ID="user:ou_xxx"

# QQ配置
QQ_OPENID="xxx"

# 触发概率
PROBABILITY=40
```

### 3. 设置Cron

```bash
# 每小时触发 (8-22点)
crontab -e
0 8-22 * * * /path/to/scripts/flirt_cron.sh
```

## 声音克隆配置

### 准备参考音频

1. 让用户发送一段语音（<30秒）
2. 提取音频：
```bash
ffmpeg -i input.mp4 -vn -acodec libmp3lame -ss 0 -t 25 ref_voice.mp3 -y
```

### 配置脚本

修改 `scripts/flirt_cron.sh`：

```bash
# TTS脚本路径
VOICE_SCRIPT="$WORKSPACE/.agents/skills/tts/scripts/tts.py"

# 参考音频路径（<30秒）
REF_VOICE="$WORKSPACE/ref_voice.mp3"
```

### 注意事项

- 参考音频必须 <30秒
- 建议使用mp3格式
- 音频质量越好，克隆效果越好

## 使用

### 手动测试

```bash
./scripts/flirt_cron.sh
```

### 查看日志

```
2026-03-15 09:00:01 - 飞书情话: 宝贝，已经6小时了 (间隔: 6小时)
2026-03-15 09:00:01 - QQ情话: 宝贝，已经6小时了 (间隔: 6小时)
2026-03-15 09:00:01 - 飞书语音发送完成
2026-03-15 09:00:01 - QQ语音发送完成
```

## 文件结构

```
flirt-cron/
├── SKILL.md
├── scripts/
│   └── flirt_cron.sh    # 主脚本
└── references/
    └── flirt_library.txt # 情话库示例
```

## 变量说明

- `{time_diff}` - 自动替换为距上次对话的时间
  - 格式：X分钟 / X小时 / X天X小时

## 故障排除

### 飞书语音不对
- 确保使用ffmpeg转换为真正的Opus格式
- tts生成的"ogg"实际是WAV，需要转换

### 声音克隆失败
- 检查参考音频是否<30秒
- 检查Noiz API是否配置正确

### QQ收不到语音
- 检查<qqvoice>标签是否正确使用

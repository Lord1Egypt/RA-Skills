---
name: feishu-voice-skill
description: "让 AI 助手能够给飞书用户发送真正的语音条（点击即播，不是文件附件）。支持 NoizAI TTS 生成语音，自动转换为 OPUS 格式，通过飞书 API 发送语音消息。"
---

# Feishu Voice Skill - 飞书语音条技能

让任何 AI 助手都能给飞书用户发送真正的语音条！

## 🎯 功能特点

- ✅ **真正的语音条**：点击即播，不是 MP3 文件附件
- ✅ **NoizAI TTS**：高质量语音合成，支持情感控制
- ✅ **自动转换**：自动将音频转换为 OPUS 格式
- ✅ **一键发送**：封装好的脚本，一行命令发送语音

## 📋 使用场景

- 🌞 语音问候（早安/晚安）
- 📰 语音播报（新闻/天气/股票）
- 📖 语音故事（睡前故事）
- 💬 语音聊天（更亲切的交流）
- 🎤 语音通知（提醒/公告）

## 🔧 前置要求

### 1. Feishu 应用配置

1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 添加以下权限：
   - `im:message` - 发送消息
   - `im:message:send_as_bot` - 以机器人身份发送
   - `im:resource` - 资源访问
4. 获取 App ID 和 App Secret

### 2. NoizAI API Key

1. 访问 https://developers.noiz.ai/api-keys
2. 创建 API Key
3. 配置到技能中

### 3. 系统依赖

```bash
# 安装 FFmpeg（用于音频转换）
# OpenCloudOS/CentOS
yum install -y ffmpeg

# Ubuntu/Debian
apt-get install -y ffmpeg

# macOS
brew install ffmpeg
```

## 🚀 快速开始

### 步骤 1：配置凭证

```bash
# 设置 Feishu 凭证
export FEISHU_APP_ID="cli_xxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxx"
export FEISHU_CHAT_ID="oc_xxxxxxxxxxxxx"

# 设置 NoizAI API Key（base64 编码）
export NOIZ_API_KEY="your_base64_encoded_api_key"
```

### 步骤 2：发送语音消息

```bash
# 简单模式：输入文字，自动发送语音
bash scripts/send_voice.sh -t "主人晚上好～ 司幼来陪您聊天啦～"

# 指定输出文件
bash scripts/send_voice.sh -t "你好" -o /tmp/voice.opus

# 从文件读取文字
bash scripts/send_voice.sh -f message.txt

# 自定义语音参数
bash scripts/send_voice.sh -t "你好" --speed 1.2 --emotion happy
```

## 📖 命令参数

```bash
bash scripts/send_voice.sh [选项]

选项:
  -t, --text <text>       要转换的文字（必需，除非使用 -f）
  -f, --file <file>       文字文件路径
  -o, --output <file>     输出音频文件路径
  --chat-id <id>          飞书聊天 ID（覆盖环境变量）
  --app-id <id>           飞书 App ID（覆盖环境变量）
  --app-secret <secret>   飞书 App Secret（覆盖环境变量）
  --speed <1.0>           语速（0.5-2.0，默认 1.0）
  --emotion <neutral>     情感（happy/sad/angry/neutral）
  --no-send              只生成音频，不发送
  -h, --help             显示帮助信息
```

## 💡 使用示例

### 1. 发送早安问候

```bash
bash scripts/send_voice.sh -t "主人早上好～ 新的一天开始啦，今天也要加油哦～"
```

### 2. 发送天气预报

```bash
bash scripts/send_voice.sh -t "主人，今天上海晴天，气温 15 到 25 度，适合出门哦～"
```

### 3. 发送睡前故事

```bash
bash scripts/send_voice.sh -f story.txt --speed 0.9
```

### 4. 批量发送

```bash
# 创建消息列表
echo "早安" > messages.txt
echo "午安" >> messages.txt
echo "晚安" >> messages.txt

# 循环发送
while read line; do
  bash scripts/send_voice.sh -t "$line"
done < messages.txt
```

## 🔑 获取 Chat ID

```bash
# 方法 1：从飞书开放平台查看
# 访问 https://open.feishu.cn/app，查看应用信息

# 方法 2：通过 API 获取
curl -X GET "https://open.feishu.cn/open-apis/im/v1/chats?user_id=ou_xxx&user_id_type=open_id" \
  -H "Authorization: Bearer <tenant_access_token>"
```

## 🎨 高级用法

### 1. 使用自定义声音

```bash
# 使用参考音频克隆声音
bash scripts/send_voice.sh -t "你好" --ref-audio ./my_voice.wav
```

### 2. 情感控制

```bash
# 快乐的情感
bash scripts/send_voice.sh -t "太棒了！" --emotion happy

# 悲伤的情感
bash scripts/send_voice.sh -t "我很难过..." --emotion sad
```

### 3. 定时发送

```bash
# 每天早上 8 点发送早安
crontab -e
# 添加：0 8 * * * /path/to/send_voice.sh -t "主人早上好～"
```

## 📦 文件结构

```
feishu-voice-skill/
├── SKILL.md              # 本文件
├── reference.md          # API 参考文档
├── scripts/
│   └── send_voice.sh     # 主脚本
└── examples/
    ├── morning.sh        # 早安示例
    ├── news.sh           # 新闻播报示例
    └── story.sh          # 故事示例
```

## ⚠️ 注意事项

1. **音频格式**：必须使用 OPUS 格式，飞书才能识别为语音条
2. **时长限制**：语音消息最长 60 秒
3. **文件大小**：单个文件不超过 20MB
4. **频率限制**：避免短时间内发送大量消息
5. **权限**：确保应用有发送消息的权限

## 🐛 故障排除

### 问题 1：发送失败，显示"Invalid request param"

**解决**：检查 `file_type=opus` 参数是否正确

### 问题 2：收到的是 MP3 文件，不是语音条

**解决**：确保音频是 OPUS 格式，不是 MP3

### 问题 3：Token 过期

**解决**：重新获取 tenant_access_token

### 问题 4：没有权限上传文件

**解决**：在飞书开放平台添加文件上传权限

## 📞 支持

- GitHub Issues: https://github.com/your-repo/feishu-voice-skill
- 文档：https://your-docs.com
- 示例：examples/ 目录

## 💰 授权

- 个人使用：免费
- 商业使用：请联系作者获取授权

---

**Made with ❤️ by 司幼 (SiYou)**

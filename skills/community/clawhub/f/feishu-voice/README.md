# 飞书语音消息发送技能

将文本转换为语音消息并发送到飞书，支持在飞书聊天窗口直接播放。

## 功能特性

- ✅ TTS 文字转语音（使用 **coze-tts**）
- ✅ 支持语速调整（0.5-2.0x）
- ✅ 自动转换为 opus 格式（飞书要求）
- ✅ 读取音频时长
- ✅ 上传到飞书服务器
- ✅ 发送可播放的语音消息

## 前置要求

### 环境变量

**必需变量：**

```bash
# 飞书配置（必需）
export FEISHU_APP_ID="cli_xxx"              # 飞书应用 ID
export FEISHU_APP_SECRET="your_secret"      # 飞书应用密钥

# Coze 配置（用于 TTS）
export COZE_API_KEY="your_coze_key"         # Coze API 密钥
```

**可选变量：**

```bash
# 接收者配置
export FEISHU_RECEIVER="ou_xxx"             # 默认接收者 Open ID

# 多应用配置（用于支持多个飞书应用）
export FEISHU_APP_ID_B="cli_xxx"            # 应用 B 的 ID
export FEISHU_APP_SECRET_B="your_secret"    # 应用 B 的密钥
export FEISHU_RECEIVER_B="ou_xxx"           # 应用 B 的接收者

# 工作区路径（用于定位依赖技能）
export OPENCLAW_WORKSPACE="/path/to/workspace"  # OpenClaw 工作区目录
```

### 必需工具

- `ffmpeg` - 音频格式转换、语速调整
- `ffprobe` - 读取音频信息
- `jq` - JSON 处理

### 依赖技能

- `coze-tts` - 文字转语音

## 快速开始

```bash
# 安装依赖（如果需要）
sudo apt-get install ffmpeg ffprobe jq

# 设置环境变量
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
export COZE_API_KEY="your_coze_key"

# 发送语音消息（默认设置）
bash scripts/send_voice.sh "你好，这是一条语音消息"

# 指定 voice_id 和语速
bash scripts/send_voice.sh "你好" 2 1.2
```

## 使用方法

### 基本用法

```bash
# 发送语音消息
bash scripts/send_voice.sh "你好，这是一条语音消息"
```

### 高级选项

```bash
# 参数说明：
# - voice_id: Coze 音色 ID（默认 1）
# - 语速: 0.5-2.0（默认 1.0）
# - 接收者: 飞书 open_id（可选）

bash scripts/send_voice.sh "你好" 2 1.2 ou_xxx
```

## 技术细节

### 音频格式要求

飞书语音消息要求：
- **格式**: opus (OGG 容器)
- **编码**: libopus
- **比特率**: 24k
- **采样率**: 24000 Hz
- **声道**: 单声道

### Duration 参数

**关键**: 必须在上传时提供 `duration` 参数（整数毫秒），否则时长显示为 0。

```bash
# 获取时长（转换为毫秒）
DURATION_MS=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 voice.opus | awk '{printf "%.0f", $1 * 1000}')

# 上传时带上 duration（毫秒）
curl ... -F "duration=$DURATION_MS"
```

## 故障排查

### 语音没有时长

**问题**: 发送的语音消息时长显示为 0

**解决**: 确保在上传时传递了 `duration` 参数（整数毫秒）

### 无法播放

**可能原因**:
1. 格式不是 opus
2. `file_type` 参数错误
3. 文件损坏

**解决**:
```bash
# 检查格式
ffprobe voice.opus

# 重新转换
ffmpeg -i input.mp3 -c:a libopus -b:a 24k voice.opus
```

### API 权限错误

**问题**: 上传时返回权限错误

**解决**: 确保飞书应用有以下权限：
- `im:message`
- `im:message:send_as_bot`

## 相关技能

- `coze-tts`: 文字转语音
- `coze-asr`: 语音转文字

## Author

franklu0819-lang

## License

MIT

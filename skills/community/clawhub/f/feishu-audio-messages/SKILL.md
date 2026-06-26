# feishu-voice - 飞书语音消息发送技能

通过飞书 Open API 发送语音/音频消息。支持文本转语音（TTS）和已有音频文件上传。

## 快速开始

```bash
# 方式1: 文字转语音发送
./send-voice.sh --to <open_id> --text "床前明月光，疑是地上霜"

# 方式2: 指定语音风格
./send-voice.sh --to <open_id> --text "通知：会议改到下午3点" --voice zh-CN-YunxiNeural

# 方式3: 发送已有音频文件
./send-voice.sh --to <open_id> --file /path/to/audio.opus
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--to` | 是 | - | 接收者 open_id（以 `ou_` 开头） |
| `--text` | 条件必填 | - | 要转为语音的文字（与 --file 二选一） |
| `--file` | 条件必填 | - | 已有音频文件路径（支持 mp3/wav 等，会自动转 opus） |
| `--voice` | 否 | zh-CN-XiaoxiaoNeural | TTS 语音名称 |
| `--rate` | 否 | +0% | 语速调整（如 +10% 加速，-10% 减速） |
| `--volume` | 否 | +0% | 音量调整（如 +0%、+10%） |

### 常用语音列表

| 语音ID | 性别/风格 | 适用场景 |
|--------|----------|----------|
| `zh-CN-XiaoxiaoNeural` | 女声/活泼 | 通用、通知 |
| `zh-CN-YunxiNeural` | 男声/沉稳 | 正式、商务 |
| `zh-CN-XiaoyiNeural` | 女声/温柔 | 客服、关怀 |

完整列表：`edge-tts --list-voices | grep zh-CN`

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 文字/文件    │───→│  TTS/转码   │───→│  opus文件   │
│ 输入        │    │(edge-tts/  │    │             │
│             │    │ ffmpeg)     │    │             │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
┌─────────────┐    ┌─────────────┐    ┌──────▼──────┐
│  发送成功    │←───│ 消息发送    │←───│  上传文件    │
│  通知       │    │(audio类型)   │    │  获取file_key│
└─────────────┘    └─────────────┘    └─────────────┘
```

## 依赖环境

- `edge-tts` - 微软 Edge TTS（语音合成）
- `ffmpeg` - 音频格式转换（转为opus）
- `curl` - HTTP 请求
- `jq` (可选) - JSON解析（比grep更可靠）

### 安装依赖

```bash
# edge-tts
pip install edge-tts

# ffmpeg (Ubuntu/Debian)
sudo apt-get install ffmpeg

# ffmpeg (macOS with Homebrew)
brew install ffmpeg

# jq (可选，用于更可靠的JSON解析)
sudo apt-get install jq  # or brew install jq
```

## 配置说明

脚本会按以下顺序查找飞书凭据：

1. 环境变量：`FEISHU_APP_ID`, `FEISHU_APP_SECRET`
2. 配置文件：`~/.openclaw/.env`
3. 配置文件：`~/.openclaw/openclaw.json`

### .env 格式

```
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
```

## 常见问题

### Q: 发送失败，提示 receive_id 无效？

**A:** 确保使用的是 `open_id`（以 `ou_` 开头），而非 `user_id`。飞书发送消息 API 需要使用 `open_id` 并在 URL 中指定 `receive_id_type=open_id`。

### Q: 没有声音/音频文件为空？

**A:** 检查 ffmpeg 转换是否正常完成：
```bash
ffmpeg -i input.mp3 -c:a libopus -b:a 128k output.opus
```

### Q: edge-tts 安装失败？

**A:** 如果系统 Python 是 externally-managed (PEP 668)，使用虚拟环境：
```bash
python3 -m venv ~/.venv/edge-tts
source ~/.venv/edge-tts/bin/activate
pip install edge-tts
```

### Q: 如何获取用户的 open_id？

**A:** 通过飞书开放平台 API 查询，或使用事件订阅接收用户互动事件获取。

## 文件说明

```
send-voice.sh      主脚本
SKILL.md           本文件
.env.example       环境变量模板
```

## 开源协议

MIT License - 自由使用，风险自负。

---

**提示**：本技能仅供学习和技术交流，使用时请遵守飞书开放平台相关协议和规定。
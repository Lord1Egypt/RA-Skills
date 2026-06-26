# 依赖安装指南

## 必需依赖

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| `ffmpeg` (含 drawtext) | 视频处理、转场、字幕烧入 | `brew install homebrew-ffmpeg/ffmpeg/ffmpeg` |
| `osascript` | FCPX AppleScript 控制 | macOS 自带 |
| `curl` | API 调用 | macOS 自带 |
| `jq` | JSON 处理 | `brew install jq` |
| `edge-tts` | TTS 配音 | `pipx install edge-tts` |
| `whisper` | 语音识别 / 字幕生成 | `brew install openai-whisper` |

## 可选依赖

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| `biliup` | B 站视频上传 | `pip3 install --break-system-packages biliup` |
| `trash` | 安全删除 | `brew install trash` |

## TTS 配音 (edge-tts)

免费、稳定的微软 Edge TTS 服务，无需本地模型，无需 API key。

**安装：**
```bash
brew install pipx
pipx install edge-tts
```

**验证：**
```bash
edge-tts --voice zh-CN-YunxiNeural --text "测试语音" --write-media /tmp/test.mp3
```

**可用中文声音：**

| 声音 | 性别 | 风格 |
|------|------|------|
| `zh-CN-YunxiNeural` | 男 | 活泼阳光 (默认) |
| `zh-CN-YunjianNeural` | 男 | 激情有力 |
| `zh-CN-YunyangNeural` | 男 | 专业新闻 |
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖亲切 |
| `zh-CN-XiaoyiNeural` | 女 | 活泼可爱 |

查看所有声音：`edge-tts --list-voices | grep zh-CN`

**在脚本中使用：**
```bash
# 单文件配音
bash scripts/auto-voiceover.sh "你好世界" /tmp/output.wav

# 多段配音 (合并模式，音色一致)
bash scripts/tts-voiceover.sh --script-file ./script.txt --output ./voiceover/ --merge

# 指定声音
bash scripts/auto-voiceover.sh --voice zh-CN-XiaoxiaoNeural "你好世界"
```

## 语音识别 / 字幕 (Whisper)

OpenAI Whisper，本地离线运行，支持 98 种语言。

**安装：**
```bash
brew install openai-whisper
```

**模型选择：**

| 模型 | 大小 | 速度 | 准确率 |
|------|------|------|--------|
| `tiny` | 39MB | 极快 | 一般 |
| `base` | 74MB | 快 | 较好 |
| `small` | 244MB | 中 | 好 |
| `medium` | 769MB | 慢 | 很好 |
| `turbo` | 809MB | 中 | 很好 (默认) |
| `large` | 1.55GB | 最慢 | 最好 |

模型首次使用自动下载到 `~/.cache/whisper/`。

**在脚本中使用：**
```bash
# 生成中文 + 英文字幕
bash scripts/multi-lang-subtitles.sh video.mp4 en

# 指定模型
bash scripts/multi-lang-subtitles.sh video.mp4 en medium
```

## 素材 API

### Pexels API（素材搜索）

无需 API key 即可使用，设置 `PEXELS_API_KEY` 可提高限额（每月20,000次）。

注册：https://www.pexels.com/api/ → 免费，即时获取。

### Pixabay API（可选素材源）

设置 `PIXABAY_API_KEY` 启用双源搜索。

注册：https://pixabay.com/api/docs/ → 免费。

**素材源对比：**

| 特性 | Pexels | Pixabay |
|------|--------|---------|
| 视频 | 200万+ | 180万+ |
| 音乐 | ❌ | ✅ 10万+ |
| API 限制 | 20k/月 | 无明确限制 |
| 署名 | 不需要 | 不需要 |

**配置方式：**
```bash
# 添加到 ~/.zshrc
export PEXELS_API_KEY="your_key"
export PIXABAY_API_KEY="your_key"
```

## 环境检查

```bash
ffmpeg -filters 2>&1 | grep drawtext   # 确认 drawtext 支持
edge-tts --list-voices | head -3       # 确认 TTS
whisper --help | head -1               # 确认 Whisper
which biliup && biliup renew           # 确认 B 站登录
```

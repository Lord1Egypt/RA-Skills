---
name: feishu-edge-tts
description: "使用微软 Edge TTS（免费）生成语音，发送到飞书。无需 API key，音质优秀，支持多语言多音色。"
---

# Feishu Edge TTS - 飞书语音条（微软免费 TTS）

使用微软 Edge TTS 生成语音，发送到飞书！**完全免费**！

## 🎯 功能特点

- ✅ **完全免费**：使用微软 Edge TTS，无需 API key
- ✅ **音质优秀**：微软 Azure 同款语音引擎
- ✅ **多音色支持**：支持中文/英文/日文等多种语言
- ✅ **语音条格式**：发送真正的飞书语音条（点击即播）
- ✅ **语速调节**：支持 0.5x - 2.0x 语速
- ✅ **音调调节**：支持音调高低调整

## 🎤 可用音色

### 中文音色
- **zh-CN-XiaoxiaoNeural** - 女声，温暖亲切（推荐）
- **zh-CN-YunxiNeural** - 男声，沉稳专业
- **zh-CN-YunjianNeural** - 男声，激情澎湃
- **zh-CN-XiaoyiNeural** - 女声，活泼可爱
- **zh-CN-liaoning-XiaobeiNeural** - 东北话女声
- **zh-CN-shaanxi-XiaoniNeural** - 陕西话女声

### 英文音色
- **en-US-JennyNeural** - 女声，美式英语（推荐）
- **en-US-GuyNeural** - 男声，美式英语
- **en-GB-SoniaNeural** - 女声，英式英语

### 更多音色
支持全球 100+ 语言，400+ 音色！

## 🔧 前置要求

### 1. Python 环境

```bash
# 安装 edge-tts
pip install edge-tts
```

### 2. Feishu 应用配置

同 Feishu Voice Skill

### 3. 系统依赖

```bash
# 安装 ffmpeg
yum install -y ffmpeg  # CentOS/OpenCloudOS
apt-get install -y ffmpeg  # Ubuntu/Debian
```

## 🚀 快速开始

### 步骤 1：安装依赖

```bash
pip install edge-tts
```

### 步骤 2：配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
```

### 步骤 3：发送语音

```bash
# 使用默认音色（女声）
bash scripts/send_voice.sh -t "主人晚上好～"

# 指定音色
bash scripts/send_voice.sh -t "Hello!" -v en-US-JennyNeural

# 调整语速
bash scripts/send_voice.sh -t "你好" --rate 1.2

# 调整音调
bash scripts/send_voice.sh -t "你好" --pitch 10
```

## 💡 使用示例

### 1. 温暖女声问候

```bash
bash scripts/send_voice.sh -t "主人早上好～ 新的一天开始啦，今天也要加油哦～" -v zh-CN-XiaoxiaoNeural
```

### 2. 专业男声播报

```bash
bash scripts/send_voice.sh -t "现在是北京时间上午 8 点，为您播报今日新闻。" -v zh-CN-YunxiNeural
```

### 3. 英文语音

```bash
bash scripts/send_voice.sh -t "Good morning! Have a nice day!" -v en-US-JennyNeural
```

### 4. 方言趣味

```bash
bash scripts/send_voice.sh -t "哎呀妈呀，这旮瘩真冷啊！" -v zh-CN-liaoning-XiaobeiNeural
```

## 📖 命令参数

```bash
bash scripts/send_voice.sh [选项]

选项:
  -t, --text <text>       要转换的文字（必需）
  -v, --voice <voice>     音色名称（默认：zh-CN-XiaoxiaoNeural）
  -r, --rate <1.0>        语速（-50% 到 +50%，默认 0%）
  -p, --pitch <0>         音调（-50Hz 到 +50Hz，默认 0）
  -o, --output <file>     输出音频文件路径
  --list-voices           列出所有可用音色
  --no-send               只生成音频，不发送
  -h, --help              显示帮助

```

## 🎵 音色列表

```bash
# 查看所有可用音色
bash scripts/send_voice.sh --list-voices

# 查看中文音色
bash scripts/send_voice.sh --list-voices | grep zh-CN
```

## ⚙️ 高级配置

### 1. 自定义默认音色

编辑 `config.sh`：

```bash
DEFAULT_VOICE="zh-CN-YunxiNeural"  # 男声
DEFAULT_RATE="0"                    # 正常语速
DEFAULT_PITCH="0"                   # 正常音调
```

### 2. 批量生成

```bash
# 从文件读取文字，批量生成
cat messages.txt | while read line; do
    bash scripts/send_voice.sh -t "$line"
    sleep 2
done
```

## 📦 文件结构

```
feishu-edge-tts/
├── SKILL.md
├── README.md
├── reference.md
├── scripts/
│   ├── send_voice.sh        # 主脚本
│   ├── list_voices.sh       # 音色列表
│   └── config.sh            # 配置文件
├── examples/
│   ├── greetings.txt        # 问候语示例
│   └── crontab.txt          # 定时任务示例
└── config.sh                # 用户配置
```

## 💰 商业授权

- **个人使用**：免费
- **商业使用**：请联系作者获取授权

---

**Made with ❤️ by 司幼 (SiYou)**

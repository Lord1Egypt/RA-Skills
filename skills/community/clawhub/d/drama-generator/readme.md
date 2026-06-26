# OpenClaw Drama Generator - 短剧生成器

**版本 / Version**: 2.0.0
**许可证 / License**: MIT-0
**作者 / Author**: ZhenStaff

---

## 中文文档 / Chinese Documentation

### 项目简介

**OpenClaw Drama Generator（短剧生成器）** 是一个完全自动化的短剧视频生成系统。

只需提供剧本文本，即可自动生成多角色配音、场景切换、专业视觉效果的短剧视频。

**核心定位**: 短剧生成 - 从剧本到视频，一键生成

### ✨ 特性

- 🎭 **多角色对话** - 自动识别角色，分配不同声音
- 📝 **剧本解析** - 支持标准短剧格式
- 🎤 **智能配音** - 基于角色自动选择合适的声音
- 🎬 **场景切换** - 美观的场景转场动画
- 💬 **对话框样式** - 专业的对话呈现效果
- 📢 **旁白支持** - 特殊的旁白视觉风格
- 🤖 **完全自动化** - 一行命令完成全流程

### 📦 安装

#### 方式 1: npm 安装（推荐）

```bash
npm install -g openclaw-drama-generator
```

#### 方式 2: GitHub 克隆

```bash
git clone https://github.com/ZhenRobotics/openclaw-drama-generator.git
cd openclaw-drama-generator
npm install
```

#### 方式 3: ClawHub 安装

```bash
clawhub install drama-generator
```

### 🚀 快速开始

#### 1. 配置 API Key

选择一个 TTS 提供商并设置 API Key：

```bash
# OpenAI（推荐）
export OPENAI_API_KEY="sk-..."

# 或 Azure
export AZURE_TTS_KEY="..."
export AZURE_TTS_REGION="eastus"

# 或阿里云
export ALIYUN_ACCESS_KEY_ID="..."
export ALIYUN_ACCESS_KEY_SECRET="..."

# 或腾讯云
export TENCENT_SECRET_ID="..."
export TENCENT_SECRET_KEY="..."
```

#### 2. 创建剧本

创建一个剧本文件（标准格式）：

```bash
cat > my-drama.txt <<'EOF'
[场景1 - 咖啡厅 - 下午]
旁白: 这是一个温暖的午后。
小美: 你好，好久不见！
小王: 是啊，最近忙什么呢？
小美: 在学习做短剧视频，用AI生成的。
小王: 听起来很酷！

[场景2 - 咖啡厅 - 下午]
小美: 你也可以试试，很简单的。
小王: 真的吗？怎么做？
小美: 只要写剧本，然后一行命令就能生成视频。
小王: 太棒了，我也要试试！
旁白: 从此，他们都成了短剧创作者。
EOF
```

#### 3. 生成视频

```bash
# 一键生成
drama-generator my-drama.txt

# 或指定参数
drama-generator my-drama.txt --speed 1.1 --provider openai

# 查看结果
mpv out/my-drama.mp4
```

### 📖 剧本格式详解

#### 基本格式

```
[场景N - 地点 - 时间]
角色名: 对话内容
角色名: (情绪) 对话内容
旁白: 旁白内容
```

#### 格式说明

- **场景标记**: `[场景N - 地点 - 时间]` - N 从 1 开始编号
- **角色对话**: `角色名: 对话内容` - 角色名要保持一致
- **情绪标注**: `(括号内容)` - 可选，用于显示角色情绪
- **旁白**: `旁白: 内容` - 用于场景描述和补充信息

#### 完整示例

```
[场景1 - 办公室 - 早晨]
旁白: 又是忙碌的一天开始了。
小明: 早啊小红，今天的项目汇报准备好了吗？
小红: 准备好了，PPT我已经发到你邮箱了。
小明: 太好了，老板今天心情怎么样？
小红: 不太好，昨天的数据不理想。

[场景2 - 会议室 - 上午]
老板: 大家好，今天我们讨论一下第二季度的业绩。
小明: (紧张) 老板，我们这个月的增长率达到了百分之十五。
老板: 只有百分之十五？竞争对手都达到百分之三十了。
小红: 但是我们的用户满意度提升了百分之二十。
老板: 嗯，这倒是个好消息。

[场景3 - 办公室 - 下午]
旁白: 会议结束后，大家都松了一口气。
小明: 吓死我了，还以为要被批评了。
小红: 还好我们有准备，下次要做得更好。
小明: 对，一起加油！
旁白: 职场的故事，每天都在继续。
```

### 🎨 视觉效果

#### 场景类型

系统自动生成三种场景类型：

1. **对话场景** - 对话框样式，显示角色名和对话内容
2. **场景转场** - 显示场景信息（地点、时间）的过渡动画
3. **旁白场景** - 居中显示，引号样式，特殊视觉效果

#### 颜色方案

不同角色使用不同颜色：
- 青色 (#00F5FF) - 默认男性角色
- 品红 (#FF10F0) - 默认女性角色
- 金色 (#FFD700) - 旁白专用
- 其他颜色 - 多角色时自动分配

#### 动画效果

- 对话框弹出动画（spring 动画）
- 打字机文本效果
- 场景淡入淡出
- 场景转场动画

### 🎤 角色声音

系统自动为角色分配声音，可用声音：

| 声音 | 特点 | 适合角色 | 语言 |
|------|------|----------|------|
| alloy | 中性，清晰 | 男性角色 | 多语言 |
| echo | 男性，稳重 | 成熟男性 | 多语言 |
| fable | 英式，优雅 | 旁白 | 英语为主 |
| onyx | 深沉，有力 | 领导/老板 | 多语言 |
| nova | 女性，活泼 | 年轻女性 | 多语言 |
| shimmer | 柔和，温暖 | 旁白/女性 | 多语言 |

### 🔧 高级用法

#### 分步执行

```bash
# 1. 解析剧本
node scripts/parse-drama-script.js my-drama.txt

# 2. 生成多角色 TTS
./scripts/drama-tts-generate.sh audio/my-drama-parsed.json

# 3. 提取时间戳
./scripts/whisper-timestamps.sh audio/drama-full.mp3

# 4. 生成场景数据
node scripts/drama-to-scenes.js \
  audio/my-drama-parsed.json \
  audio/drama-full-timestamps.json \
  audio/drama-segments.json

# 5. 渲染视频
npm run render
```

#### 自定义声音

解析剧本后，编辑生成的 JSON 文件修改角色声音：

```json
{
  "characters": {
    "小明": {
      "name": "小明",
      "voice": "onyx",
      "dialogueCount": 5
    },
    "小红": {
      "name": "小红",
      "voice": "nova",
      "dialogueCount": 4
    }
  }
}
```

#### 预览和调试

```bash
# 开发模式预览
npm run dev

# 在浏览器打开 http://localhost:3000
# 可实时预览视频效果，无需每次渲染
```

### 📊 技术架构

#### 完整流水线

```
剧本文本 (txt)
    ↓
剧本解析 (parse-drama-script.js)
    ↓
剧本数据 (JSON)
    ↓
多角色 TTS (drama-tts-generate.sh)
    ↓
音频拼接
    ↓
时间戳提取 (Whisper API)
    ↓
场景数据生成 (drama-to-scenes.js)
    ↓
视频渲染 (Remotion)
    ↓
短剧视频 (MP4)
```

#### 技术栈

- **React 19** - UI 框架
- **Remotion 4.0** - 视频渲染引擎
- **TypeScript** - 类型安全开发
- **OpenAI TTS** - 语音合成（默认）
- **OpenAI Whisper** - 时间戳提取
- **FFmpeg** - 音频处理
- **多提供商** - 支持 Azure、阿里云、腾讯云

### 📈 性能与成本

#### 处理时间（1分钟短剧）

- 剧本解析: <1秒
- TTS 生成: 10-20秒
- 时间戳提取: 5-10秒
- 场景生成: <1秒
- 视频渲染: 30-90秒
- **总计**: 50-120秒

#### 成本（使用 OpenAI）

- TTS: ~$0.009/分钟
- Whisper: ~$0.006/分钟
- 本地渲染: 免费
- **总计**: ~$0.015/分钟

### 📺 视频规格

- **分辨率**: 1080 x 1920 (竖屏)
- **帧率**: 30 fps
- **格式**: MP4 (H.264 + AAC)
- **时长**: 根据剧本自动计算
- **适用平台**: 抖音、快手、视频号、TikTok

### 🐛 故障排查

#### Q: API Key 无效

```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 测试连接
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Q: 音频拼接失败

```bash
# 检查 ffmpeg
ffmpeg -version

# macOS 安装
brew install ffmpeg

# Ubuntu 安装
sudo apt-get install ffmpeg
```

#### Q: 角色声音不合适

编辑解析后的 JSON 文件修改声音，然后从 TTS 步骤重新开始。

### 🔗 项目链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-drama-generator
- **npm**: https://www.npmjs.com/package/openclaw-drama-generator
- **文档**: https://github.com/ZhenRobotics/openclaw-drama-generator#readme
- **Issues**: https://github.com/ZhenRobotics/openclaw-drama-generator/issues

### 📄 许可证

MIT-0 License - 无需署名的 MIT 许可证

---

## English Documentation

### Introduction

**OpenClaw Drama Generator** is a fully automated drama video generation system.

Simply provide a drama script, and it will automatically generate multi-character voiced drama videos with scene transitions and professional visual effects.

**Core Positioning**: From Script to Video, One-Click Generation

### ✨ Features

- 🎭 **Multi-Character Dialogue** - Automatic character recognition with different voices
- 📝 **Script Parsing** - Support for standard drama format
- 🎤 **Smart Voice Assignment** - Automatically select appropriate voices based on characters
- 🎬 **Scene Transitions** - Beautiful scene transition animations
- 💬 **Dialogue Box Style** - Professional dialogue presentation
- 📢 **Narration Support** - Special narration visual style
- 🤖 **Full Automation** - One-command complete pipeline

### 📦 Installation

#### Option 1: npm Install (Recommended)

```bash
npm install -g openclaw-drama-generator
```

#### Option 2: GitHub Clone

```bash
git clone https://github.com/ZhenRobotics/openclaw-drama-generator.git
cd openclaw-drama-generator
npm install
```

#### Option 3: ClawHub Install

```bash
clawhub install drama-generator
```

### 🚀 Quick Start

#### 1. Configure API Key

Choose a TTS provider and set API Key:

```bash
# OpenAI (recommended)
export OPENAI_API_KEY="sk-..."

# Or Azure
export AZURE_TTS_KEY="..."
export AZURE_TTS_REGION="eastus"

# Or Alibaba Cloud
export ALIYUN_ACCESS_KEY_ID="..."
export ALIYUN_ACCESS_KEY_SECRET="..."

# Or Tencent Cloud
export TENCENT_SECRET_ID="..."
export TENCENT_SECRET_KEY="..."
```

#### 2. Create Script

Create a script file (standard format):

```bash
cat > my-drama.txt <<'EOF'
[Scene 1 - Cafe - Afternoon]
Narrator: A warm afternoon.
Mei: Hello, long time no see!
Wang: Yes, what have you been up to?
Mei: Learning to make drama videos with AI.
Wang: Sounds cool!

[Scene 2 - Cafe - Afternoon]
Mei: You can try it too, it's simple.
Wang: Really? How?
Mei: Just write a script, then one command generates the video.
Wang: Awesome, I want to try!
Narrator: From then on, they both became drama creators.
EOF
```

#### 3. Generate Video

```bash
# One-click generation
drama-generator my-drama.txt

# Or specify parameters
drama-generator my-drama.txt --speed 1.1 --provider openai

# View result
mpv out/my-drama.mp4
```

### 📖 Script Format

#### Basic Format

```
[Scene N - Location - Time]
Character Name: Dialogue content
Character Name: (Emotion) Dialogue content
Narrator: Narration content
```

#### Format Description

- **Scene Marker**: `[Scene N - Location - Time]` - N starts from 1
- **Character Dialogue**: `Character Name: Dialogue content` - Keep character names consistent
- **Emotion Tag**: `(emotion)` - Optional, for displaying character emotions
- **Narrator**: `Narrator: content` - For scene description and context

### 🎨 Visual Effects

#### Scene Types

Three automatically generated scene types:

1. **Dialogue Scene** - Dialogue box style with character name and content
2. **Scene Transition** - Transition animation showing scene info (location, time)
3. **Narration Scene** - Centered display with quotation marks style

#### Color Scheme

Different colors for different characters:
- Cyan (#00F5FF) - Default male characters
- Magenta (#FF10F0) - Default female characters
- Gold (#FFD700) - Narration only
- Other colors - Auto-assigned for multiple characters

### 🎤 Character Voices

Available voices for character assignment:

| Voice | Characteristics | Suitable For | Language |
|-------|-----------------|--------------|----------|
| alloy | Neutral, clear | Male characters | Multilingual |
| echo | Male, steady | Mature males | Multilingual |
| fable | British, elegant | Narration | English-focused |
| onyx | Deep, powerful | Leaders/bosses | Multilingual |
| nova | Female, lively | Young females | Multilingual |
| shimmer | Soft, warm | Narration/females | Multilingual |

### 📊 Technical Stack

- **React 19** - UI framework
- **Remotion 4.0** - Video rendering engine
- **TypeScript** - Type-safe development
- **OpenAI TTS** - Voice synthesis (default)
- **OpenAI Whisper** - Timestamp extraction
- **FFmpeg** - Audio processing
- **Multi-provider** - Azure, Alibaba Cloud, Tencent Cloud support

### 📈 Performance & Cost

#### Processing Time (1-minute drama)

- Script parsing: <1s
- TTS generation: 10-20s
- Timestamp extraction: 5-10s
- Scene generation: <1s
- Video rendering: 30-90s
- **Total**: 50-120s

#### Cost (Using OpenAI)

- TTS: ~$0.009/minute
- Whisper: ~$0.006/minute
- Local rendering: Free
- **Total**: ~$0.015/minute

### 📺 Video Specifications

- **Resolution**: 1080 x 1920 (Portrait)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Duration**: Auto-calculated from script
- **Platforms**: TikTok, Douyin, Kuaishou, Instagram Reels

### 🔗 Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-drama-generator
- **npm**: https://www.npmjs.com/package/openclaw-drama-generator
- **Documentation**: https://github.com/ZhenRobotics/openclaw-drama-generator#readme
- **Issues**: https://github.com/ZhenRobotics/openclaw-drama-generator/issues

### 📄 License

MIT-0 License - MIT No Attribution

---

**Version**: 2.0.0
**Author**: ZhenStaff
**Last Updated**: 2026-03-14

---
name: drama-generator
display_name: Drama Generator
version: 2.0.0
author: ZhenStaff
category: video-generation
subcategory: drama
license: MIT-0
description: Automated drama video generator - from script to multi-character drama videos with OpenAI TTS, Whisper, and Remotion
tags: [drama, video-generation, tts, multi-character, ai-video, short-drama, remotion, openclaw]
repository: https://github.com/ZhenRobotics/openclaw-drama-generator
homepage: https://github.com/ZhenRobotics/openclaw-drama-generator
documentation: https://github.com/ZhenRobotics/openclaw-drama-generator#readme
---

# Drama Generator

**Tagline**: 短剧生成 - 从剧本到视频，一键生成 | From Script to Video, One-Click Generation

---

## 中文 / Chinese

### 简介

**Drama Generator（短剧生成器）** - 自动化短剧视频生成系统

将剧本文本自动转换为多角色配音的专业短剧视频。支持场景切换、角色对话、旁白等完整短剧元素。

### 核心功能

- **多角色对话** - 自动识别角色，分配不同声音（6种声音选择）
- **剧本解析** - 支持标准短剧格式（场景 + 角色 + 对话）
- **智能配音** - 基于角色自动选择合适的 TTS 声音
- **场景切换** - 美观的场景转场动画效果
- **对话框样式** - 专业的对话呈现，角色名突出显示
- **旁白支持** - 特殊的旁白视觉风格（引号样式）
- **完全自动化** - 一键从剧本到视频的完整流水线

### 使用场景

1. **短剧创作** - 快速生成短剧视频内容
2. **内容创作** - 制作对话类视频素材
3. **教育培训** - 场景化教学演示视频
4. **营销推广** - 故事化产品介绍视频
5. **娱乐创作** - AI 辅助短剧制作

### 剧本格式

支持标准的短剧剧本格式：

```
[场景N - 地点 - 时间]
角色名: 对话内容
旁白: 旁白内容
```

**示例**:
```
[场景1 - 办公室 - 早晨]
旁白: 又是忙碌的一天。
小明: 早啊，今天的会议准备好了吗？
小红: 准备好了！

[场景2 - 会议室 - 上午]
老板: 大家好，我们开始吧。
小明: (紧张) 好的，老板。
```

### 快速开始

#### 安装

```bash
# npm 全局安装
npm install -g openclaw-drama-generator

# 或从 GitHub 克隆
git clone https://github.com/ZhenRobotics/openclaw-drama-generator.git
cd openclaw-drama-generator
npm install
```

#### 配置 API Key

```bash
# OpenAI（推荐）
export OPENAI_API_KEY="sk-..."

# 或其他提供商
export AZURE_TTS_KEY="..."
export ALIYUN_ACCESS_KEY_ID="..."
```

#### 生成第一个短剧

```bash
# 1. 创建剧本文件
cat > my-drama.txt <<'EOF'
[场景1 - 咖啡厅 - 下午]
旁白: 这是一个温暖的午后。
小美: 你好，好久不见！
小王: 是啊，最近很忙。
小美: 在学习做短剧视频，用AI生成的。
小王: 听起来很酷！
EOF

# 2. 一键生成视频
drama-generator my-drama.txt

# 3. 查看结果
mpv out/my-drama.mp4
```

### 技术特点

- **多提供商支持** - OpenAI、Azure、阿里云、腾讯云 TTS
- **自动声音映射** - 智能分配角色声音（6种声音）
- **精确时间戳** - Whisper API 同步对话
- **专业视觉** - Remotion 渲染引擎，赛博风格
- **高性能** - 本地渲染，快速输出

### 输出规格

- **分辨率**: 1080 x 1920 (竖屏，适合抖音/快手/视频号)
- **帧率**: 30 fps
- **格式**: MP4 (H.264 + AAC)
- **音频**: 多角色配音，自动拼接
- **时长**: 根据剧本自动计算

### 角色声音

| 声音 | 特点 | 适合角色 |
|------|------|----------|
| alloy | 中性，清晰 | 男性角色 |
| echo | 男性，稳重 | 成熟男性 |
| fable | 英式，优雅 | 旁白 |
| onyx | 深沉，有力 | 领导/老板 |
| nova | 女性，活泼 | 年轻女性 |
| shimmer | 柔和，温暖 | 旁白/女性 |

### 成本估算

使用 OpenAI TTS + Whisper：
- 每分钟短剧约 $0.015
- 非常经济实惠

### 性能

处理时间（1分钟短剧）：
- 剧本解析: <1秒
- TTS 生成: 10-20秒
- 时间戳提取: 5-10秒
- 场景生成: <1秒
- 视频渲染: 30-90秒
- **总计**: 50-120秒

### 项目链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-drama-generator
- **npm**: https://www.npmjs.com/package/openclaw-drama-generator
- **文档**: 完整的中英文文档
- **示例**: 查看 scripts/examples/office-drama.txt

---

## English

### Introduction

**Drama Generator** - Automated drama video generation system

Automatically converts drama scripts into multi-character voiced professional drama videos. Supports scene transitions, character dialogues, narration, and complete drama elements.

### Core Features

- **Multi-Character Dialogue** - Automatic character recognition with different voices (6 voice options)
- **Script Parsing** - Support for standard drama format (scenes + characters + dialogues)
- **Smart Voice Assignment** - Automatically select appropriate TTS voices based on characters
- **Scene Transitions** - Beautiful scene transition animations
- **Dialogue Box Style** - Professional dialogue presentation with highlighted character names
- **Narration Support** - Special visual style for narration (quotation marks style)
- **Full Automation** - One-click complete pipeline from script to video

### Use Cases

1. **Drama Creation** - Quickly generate drama video content
2. **Content Creation** - Create dialogue-based video materials
3. **Education & Training** - Scenario-based teaching demonstration videos
4. **Marketing** - Story-based product introduction videos
5. **Entertainment** - AI-assisted drama production

### Script Format

Standard drama script format:

```
[Scene N - Location - Time]
Character Name: Dialogue content
Narrator: Narration content
```

**Example**:
```
[Scene 1 - Office - Morning]
Narrator: Another busy day begins.
Ming: Good morning, is the meeting ready?
Hong: Ready!

[Scene 2 - Meeting Room - Morning]
Boss: Hello everyone, let's begin.
Ming: (nervous) Yes, boss.
```

### Quick Start

#### Installation

```bash
# npm global install
npm install -g openclaw-drama-generator

# Or clone from GitHub
git clone https://github.com/ZhenRobotics/openclaw-drama-generator.git
cd openclaw-drama-generator
npm install
```

#### Configure API Key

```bash
# OpenAI (recommended)
export OPENAI_API_KEY="sk-..."

# Or other providers
export AZURE_TTS_KEY="..."
export ALIYUN_ACCESS_KEY_ID="..."
```

#### Generate Your First Drama

```bash
# 1. Create script file
cat > my-drama.txt <<'EOF'
[Scene 1 - Cafe - Afternoon]
Narrator: A warm afternoon.
Mei: Hello, long time no see!
Wang: Yes, been very busy.
Mei: Learning to make drama videos with AI.
Wang: Sounds cool!
EOF

# 2. Generate video with one command
drama-generator my-drama.txt

# 3. View result
mpv out/my-drama.mp4
```

### Technical Features

- **Multi-Provider Support** - OpenAI, Azure, Alibaba Cloud, Tencent Cloud TTS
- **Auto Voice Mapping** - Smart character voice assignment (6 voices)
- **Precise Timestamps** - Whisper API dialogue synchronization
- **Professional Visuals** - Remotion rendering engine, cyber style
- **High Performance** - Local rendering, fast output

### Output Specifications

- **Resolution**: 1080 x 1920 (Portrait, suitable for TikTok/Douyin/Kuaishou)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Audio**: Multi-character voices, automatically concatenated
- **Duration**: Auto-calculated from script

### Character Voices

| Voice | Characteristics | Suitable For |
|-------|-----------------|--------------|
| alloy | Neutral, clear | Male characters |
| echo | Male, steady | Mature males |
| fable | British, elegant | Narration |
| onyx | Deep, powerful | Leaders/bosses |
| nova | Female, lively | Young females |
| shimmer | Soft, warm | Narration/females |

### Cost Estimation

Using OpenAI TTS + Whisper:
- About $0.015 per minute of drama
- Very cost-effective

### Performance

Processing time (1-minute drama):
- Script parsing: <1s
- TTS generation: 10-20s
- Timestamp extraction: 5-10s
- Scene generation: <1s
- Video rendering: 30-90s
- **Total**: 50-120s

### Project Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-drama-generator
- **npm**: https://www.npmjs.com/package/openclaw-drama-generator
- **Documentation**: Complete bilingual documentation
- **Examples**: See scripts/examples/office-drama.txt

---

**License**: MIT-0
**Version**: 2.0.0
**Author**: ZhenStaff

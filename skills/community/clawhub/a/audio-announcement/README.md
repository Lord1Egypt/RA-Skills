# Audio Announcement Skill

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.8-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows%20%7C%20Android-lightgrey.svg)

# 🦊 A Chatty Lobster | 一只多嘴的龙虾

**Hear what your AI agent is doing in real-time. Stay informed, stay safe.**

**实时语音播报AI的一举一动，让你更安心、更放心。**

*"I'm generating your report..."* • *"Task completed!"* • *"I need your permission..."*

不再是冷冰冰的日志，而是一只爱说话的龙虾朋友 🦊

[English](#english) | [中文](#中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### Why A Chatty Lobster?

Your AI agent shouldn't be a black box. With this skill, OpenClaw becomes a **talkative companion** that keeps you informed:

- 🎯 **Transparency**: Know exactly what your AI is doing
- 🔒 **Security Feel**: Hear actions in real-time, no need to watch logs
- 💬 **Human Touch**: A friendly voice, not cold text
- ⚡ **Efficiency**: Focus on your work, let the lobster speak

### Features

- 🌍 **9 Languages**: Chinese, English, Japanese, Korean, Spanish, French, German
- 💻 **4 Platforms**: macOS, Linux, Windows, Android
- 🔄 **Queue System**: Messages never lost, auto-retry on failure
- 🦊 **Human-Friendly**: Make your AI feel safer and more approachable

### Installation

#### Method 1: ClawHub (Recommended)

```bash
# Install from ClawHub
clawhub install audio-announcement-skills

# Install dependencies
pip install edge-tts
```

#### Method 2: Manual Install

```bash
# Clone
git clone https://github.com/wililam/audio-announcement-skills.git

# Copy to your skills
cp -r audio-announcement-skills ~/.openclaw/skills/audio-announcement
```

### Usage

**macOS / Linux:**
```bash
# The lobster speaks Chinese
./announce.sh complete "任务完成" zh

# The lobster speaks English
./announce.sh complete "Task finished" en

# The lobster speaks Japanese
./announce.sh task "処理中です" ja
```

**Windows (Recommended - PyGame):**
```powershell
# Install PyGame for best Windows 11 support
pip install pygame

# v1.5.0+: announce.sh auto-detects Windows and uses pygame
./announce.sh complete "任务完成" zh
```

---

<a name="中文"></a>
## 🇨🇳 中文

### 为什么需要一只多嘴的龙虾？

AI 不应该是一个"黑盒"。有了这个技能，OpenClaw 变成了一只**爱说话的龙虾朋友**：

- 🎯 **透明度**：清楚知道 AI 在做什么
- 🔒 **安全感**：实时听到操作，不用盯着日志看
- 💬 **人性化**：朋友般的声音，不是冷冰冰的文字
- ⚡ **效率**：专注你的工作，让龙虾用声音告诉你进度

### 特性

- 🌍 **9种语言**：中文、英文、日文、韩文、西班牙语、法语、德语
- 💻 **4个平台**：macOS、Linux、Windows、Android
- 🔄 **队列机制**：消息永不丢失，自动重试
- 🦊 **人性化**：让你的 AI 更安全、更亲切

### 安装方式

#### 方式一：ClawHub 安装（推荐）

```bash
# 从 ClawHub 安装
clawhub install audio-announcement-skills

# 安装依赖
pip install edge-tts
```

#### 方式二：手动安装

```bash
# 克隆
git clone https://github.com/wililam/audio-announcement-skills.git

# 复制到 skills 目录
cp -r audio-announcement-skills ~/.openclaw/skills/audio-announcement
```

### 使用方法

**推荐：使用统一包装脚本（避免硬编码路径）**

```bash
# 从工作区直接调用
python scripts/announce.py receive "收到上传指令" zh
python scripts/announce.py task "正在生成文档" zh
python scripts/announce.py complete "任务完成" zh
python scripts/announce.py error "网络异常" zh
```

该脚本自动解析 skill 安装路径，无需关心具体位置。

**备选：直接调用平台脚本**

**macOS / Linux:**
```bash
# 使用 shell 脚本（自动选择最佳方案）
./scripts/announce.sh complete "任务完成" zh

# 或直接使用 pygame 方案
python scripts/announce_pygame.py complete "任务完成" zh
```

**Windows (推荐 - PyGame):**
```powershell
# 安装 PyGame（Windows 11 最佳方案）
pip install pygame

# 使用 pygame 方案（最稳定）
python scripts/announce_pygame.py complete "任务完成" zh
```

---

## 🦊 强制语音播报

**每次交互都必须语音播报！**

### 播报时机

| 时机 | 类型 | 示例 |
|------|------|------|
| 收到消息 | `receive` | "收到上传指令" |
| 开始工作 | `task` | "准备上传到GitHub" |
| 执行中 | `task` | "正在生成文档" |
| 任务完成 | `complete` | "上传完成" |
| 发送回复 | `complete` | "已发送项目地址" |
| 发生错误 | `error` | "连接超时" |

### 内容原则

- **简洁**：不超过 20 个字
- **口语化**：像朋友随口说一句
- **不带名称**：不说用户名、不说"我"
- **信息丰富**：包含指令/规划/进度/总结

### 安装后配置

安装此技能后，需要将强制播报内容添加到工作区的 `AGENTS.md` 文件中，详见 [SKILL.md](SKILL.md)。

---

## 📁 Project Structure

```
audio-announcement/
├── README.md
├── SKILL.md              # 详细使用文档
├── LICENSE
├── package.json
├── version.txt
└── scripts/
    ├── announce.py           # 🆕 统一包装脚本 (v2.0.7+)
    ├── announce.sh           # 主脚本 (v1.5.0+: Windows 自动调用 pygame)
    ├── announce_pygame.py    # Windows pygame 方案
    ├── announce-offline.sh   # 离线模式
    └── workflow-helper.sh    # 工作流助手
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

**miaoweilin** - [GitHub](https://github.com/wililam)

---

<div align="center">

**🦊 让你的龙虾开口说话，让你更安心！**

**Make your lobster talk, make yourself feel safer!**

⭐ If this helped you, give it a star! ⭐

</div>
---
name: video-generator
description: Automated video generation pipeline with OpenAI TTS, Whisper, and Remotion - from text script to professional short videos
tags: [video-generation, remotion, openai, tts, whisper, automation, ai-video, short-video, text-to-video]
---

# 🎬 Video Generator Skill

自动化视频生成系统，从文本脚本生成专业短视频。

## 📦 安装

### 步骤 1: 安装 Skill

```bash
clawhub install video-generator
```

### 步骤 2: 安装项目

**选项 A: 通过 GitHub（推荐）**

```bash
# 克隆项目到标准位置
git clone https://github.com/ZhenRobotics/openclaw-video.git ~/openclaw-video
cd ~/openclaw-video

# 安装依赖
npm install

# 设置环境变量
export OPENAI_API_KEY="sk-your-key-here"
```

**选项 B: 通过 npm（即将支持）**

```bash
npm install -g openclaw-video
```

### 步骤 3: 验证安装

```bash
cd ~/openclaw-video
./agents/video-cli.sh help
```

---

## 🚀 使用方式

### When to use this skill

**自动触发条件** - 当用户的消息包含以下任一情况时使用此 skill：

- 关键词：`生成视频`, `做视频`, `创建视频`, `make video`, `generate video`
- 提供了看起来像视频脚本的文本（多个句子描述故事/概念）
- 询问关于视频生成、TTS 或 Remotion
- 想要将文本转换为视频格式

**触发示例**（遇到这些必须使用此 skill）：
- "AI让开发更简单。GPT写代码，Whisper转音频，Remotion做视频。" ← 这是视频脚本
- "帮我生成一个视频：[任何脚本]"
- "做个视频，内容是..."
- "我想要一个关于AI的短视频"

**不要使用的情况**：
- 仅视频播放或格式转换（使用 video-frames skill）
- 视频编辑或剪辑（使用其他工具）

---

## 🎯 核心功能

这个 Skill 提供完整的视频生成流水线：

- 🎤 **TTS 语音生成** - OpenAI TTS API，支持多种声音
- ⏱️ **时间戳提取** - OpenAI Whisper API，精确分段
- 🎬 **场景编排** - 智能检测 6 种场景类型
- 🎨 **视频渲染** - Remotion，赛博线框风格
- 🤖 **Agent 交互** - 自然语言对话

---

## 💻 Agent 使用指南

### 重要提示

**关键**: 使用现有的项目目录，不要创建新项目或运行 `npx remotion`。

项目位置：
- 标准安装：`~/openclaw-video/`
- 或检测：首次使用时询问用户项目位置

### 主命令：生成视频

当用户请求生成视频时，执行以下命令：

```bash
# 方法 1: 使用便捷脚本（推荐）
~/openclaw-video/generate-for-openclaw.sh "用户提供的脚本内容"

# 方法 2: 使用 CLI
cd ~/openclaw-video && ./agents/video-cli.sh generate "脚本内容"

# 方法 3: 完整 Agent（用于复杂需求）
cd ~/openclaw-video && pnpm exec tsx agents/video-agent.ts "帮我生成视频：脚本内容"
```

**示例**：

如果用户说："生成视频：AI让开发更简单"

执行：
```bash
~/openclaw-video/generate-for-openclaw.sh "AI让开发更简单"
```

### 其他操作

**优化脚本**：
```bash
cd ~/openclaw-video && ./agents/video-cli.sh optimize "脚本内容"
```

**获取帮助**：
```bash
cd ~/openclaw-video && ./agents/video-cli.sh help
```

### 输出位置

生成的视频保存在：`~/openclaw-video/out/generated.mp4`

---

## ⚙️ 配置选项

### 声音选择
- `alloy` - 中性
- `echo` - 清晰
- `nova` - 推荐，温暖
- `shimmer` - 柔和

### 语速
- 范围：0.25 - 4.0
- 推荐：1.15（快节奏短视频）
- 默认：1.0

### 视频风格
- 快节奏短视频（默认）
- 教程讲解
- 产品营销
- 故事叙述

---

## 📊 视频规格

- **分辨率**: 1080 x 1920（竖屏，适合抖音/快手/视频号）
- **帧率**: 30 fps
- **格式**: MP4（H.264 + AAC）
- **风格**: 赛博线框 + 霓虹色彩
- **时长**: 自动根据脚本长度计算

---

## 🎨 场景类型

系统自动检测并生成 6 种场景类型：

| 类型 | 效果 | 触发条件 |
|------|------|----------|
| **title** | 故障效果 + 弹簧缩放 | 第一个片段 |
| **emphasis** | 放大弹出 | 包含百分比、数字强调 |
| **pain** | 震动 + 红色警告 | 包含问题、痛点 |
| **content** | 平滑淡入 | 普通内容 |
| **circle** | 旋转圆环高亮 | 列举要点 |
| **end** | 上滑淡出 | 最后一个片段 |

---

## 💰 成本估算

每个 15 秒视频约 **$0.003**（不到 1 美分）：

- OpenAI TTS: ~$0.001
- OpenAI Whisper: ~$0.0015
- Remotion 渲染: 免费（本地）

---

## 📝 使用示例

### 示例 1: 快速生成

用户："生成一个视频：三个AI工具改变开发效率。GPT写代码，Whisper转音频，Remotion做视频。"

Agent 执行：
```bash
~/openclaw-video/generate-for-openclaw.sh "三个AI工具改变开发效率。GPT写代码，Whisper转音频，Remotion做视频。"
```

输出：`~/openclaw-video/out/generated.mp4`

### 示例 2: 带配置

用户："用温暖的声音生成视频，语速快一点"

Agent：
1. 确认脚本内容
2. 执行带参数的命令：
```bash
cd ~/openclaw-video && ./agents/video-cli.sh generate "脚本内容" --voice nova --speed 1.3
```

### 示例 3: 优化脚本

用户："帮我看看这个脚本适合做视频吗：AI改变世界"

Agent：
```bash
cd ~/openclaw-video && ./agents/video-cli.sh optimize "AI改变世界"
```

Agent 会得到分析结果并告知用户。

---

## 🔧 故障排查

### 问题 1: 找不到项目

**错误**: `bash: ~/openclaw-video/generate-for-openclaw.sh: No such file or directory`

**解决**：
```bash
# 检查项目是否已安装
ls ~/openclaw-video

# 如果不存在，安装项目
git clone https://github.com/ZhenRobotics/openclaw-video.git ~/openclaw-video
cd ~/openclaw-video && npm install
```

### 问题 2: API Key 错误

**错误**: `model_not_found` 或 TTS 访问被拒

**解决**：
- 确保使用付费 OpenAI 账号（充值至少 $5）
- 确认 API Key 有 TTS + Whisper 权限
- 设置环境变量：`export OPENAI_API_KEY="sk-..."`

### 问题 3: 依赖缺失

**错误**: `command not found: pnpm` 或 `tsx`

**解决**：
```bash
cd ~/openclaw-video
npm install
```

---

## 📚 完整文档

- **GitHub**: https://github.com/ZhenRobotics/openclaw-video
- **快速开始**: `~/openclaw-video/QUICKSTART.md`
- **Agent 指南**: `~/openclaw-video/docs/AGENT.md`
- **FAQ**: `~/openclaw-video/docs/FAQ.md`
- **完整 README**: `~/openclaw-video/README.md`

---

## 🌟 特性

- ✅ 完全自动化的视频生成流水线
- ✅ 支持中英文脚本
- ✅ 低成本（每视频 < $0.01）
- ✅ 本地渲染，无需云服务
- ✅ 赛博朋克视觉风格
- ✅ 支持自定义配置
- ✅ Agent 友好的接口

---

## ⚠️ 注意事项

1. **环境变量**: 需要有效的 `OPENAI_API_KEY`
2. **项目安装**: 必须先克隆和安装项目才能使用
3. **网络要求**: TTS 和 Whisper API 需要网络连接
4. **路径假设**: 默认项目在 `~/openclaw-video/`，如在其他位置需调整

---

## 🎯 Agent 行为准则

使用此 skill 时，Agent 应该：

1. ✅ **检查项目是否安装**：首次使用时确认项目存在
2. ✅ **使用现有项目**：不要创建新的 Remotion 项目
3. ✅ **提供清晰反馈**：告诉用户正在生成视频、预计时间
4. ✅ **处理错误**：遇到错误时提供解决方案
5. ✅ **显示结果**：生成后告知视频位置

**不要做**：
- ❌ 运行 `npx remotion` 创建新项目
- ❌ 在没有检查的情况下假设项目已安装
- ❌ 忽略错误信息
- ❌ 使用硬编码的绝对路径（除了 `~` 路径）

---

## 📊 技术栈

- **Remotion**: React-based 视频生成框架
- **OpenAI TTS**: 文字转语音 API
- **OpenAI Whisper**: 语音识别 API
- **TypeScript**: 类型安全开发
- **React**: UI 组件框架
- **Node.js**: 运行环境

---

## 🆕 版本历史

### v1.0.0 (2026-03-03)
- ✨ 初始发布
- 🎤 TTS 语音生成
- ⏱️ Whisper 时间戳提取
- 🎬 场景智能编排
- 🎨 赛博线框视觉风格
- 🤖 Agent CLI 接口

---

**项目状态**: ✅ 生产就绪

**许可证**: MIT

**作者**: @ZhenStaff

**支持**: https://github.com/ZhenRobotics/openclaw-video/issues

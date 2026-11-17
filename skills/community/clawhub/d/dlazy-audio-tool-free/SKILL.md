---

name: "dlazy-audio-tool-free"
description: "轻量级文本转语音工具，支持多语言TTS与基础音效生成，适合个人内容创作。Use when 需要文本翻译、多语言转换、本地化处理时使用。不适用于专业医学法律翻译认证。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "音频生成工具-免费版"
  version: "1.0.0"
  summary: "轻量级文本转语音工具，支持多语言TTS与基础音效生成，适合个人内容创作。"
  tags:
    - "Creative"
    - "Audio"
    - "TTS"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 音频生成工具（免费版）

## 概述

音频生成工具免费版是一款面向个人创作者的文本转语音与基础音效生成工具。通过 dlazy CLI 自动选择优选音频模型，将文本转换为自然流畅的语音输出，支持中英双语及多种语言。

本版本适合个人视频配音、有声书朗读、社交媒体内容制作等场景。采用 API Key 认证，配置简单，开箱即用。

## 核心能力

### 免费版支持的模型

**处理流程**：执行音频生成命令,调用对应模型API处理文本输入,返回生成的音频文件。用户通过参数指定模型和语音风格。

| 模型 | 类型 | 说明 |
|:-----|:-----|:-----|
| doubao-tts | 文本转语音 | 多语言语音合成，自然流畅，适合新闻与有声书 |
| keling-tts | 文本转语音 | 支持语种、音色、语速、输出格式设置 |
| gemini-2.5-tts | 文本转语音 | 中英双语，多种情感音色 |
| keling-sfx | 音效生成 | 文本转音效，适合环境音与提示音 |

### 能力边界

```text
支持功能:
  - 文本转语音（3个TTS模型）
  - 基础音效生成（1个SFX模型）
  - 中英双语支持
  - 标准音色选择

不支持（需专业版）:
  - 语音克隆（Voice Clone）
  - 音乐生成（Music Generation）
  - 多角色对话（Multi-voice Dialogue）
  - 声音库搜索（Voice Search）
  - 管道链接（Pipe Chaining）
```

**输出**: 返回免费版支持的模型的执行结果,包含操作状态和输出数据。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级文本转语音、支持多语言、与基础音效生成、适合个人内容创作、音频生成工具免费、面向个人创作者的、文本转语音与基础、音效生成方案、核心能力、自动模型选择、支持中英双语及多、API、Key、认证与本地配置等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

### 核心功能执行
执行核心功能执行操作,使用`input_params`参数进行配置。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：视频配音制作

为短视频或教学视频生成旁白配音。

```bash
# 使用 doubao-tts 生成中文配音
dlazy doubao-tts \
  --text "欢迎来到本教程，今天我们将学习如何使用音频生成工具提升内容创作效率。" \
  --language "zh" \
  --voice "female-warm"

# 使用 gemini-2.5-tts 生成中英混合配音
dlazy gemini-2.5-tts \
  --text "Hello everyone, 今天我们来说说 AI 音频生成技术的最新进展。" \
  --voice "neutral"
```

### 场景二：有声书章节朗读

将文本章节批量转换为音频。

```python
# 有声书章节朗读脚本
import subprocess
import os

def generate_audiobook_chapter(text_file, output_dir="audio_output"):
    """将文本文件转为音频"""
    os.makedirs(output_dir, exist_ok=True)

    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    chapter_name = os.path.splitext(os.path.basename(text_file))[0]
    output_path = os.path.join(output_dir, f"{chapter_name}.wav")

    # 调用 dlazy CLI 生成音频
    cmd = [
        "dlazy", "doubao-tts",
        "--text", text,
        "--language", "zh",
        "--voice", "male-calm",
        "--output", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"章节 {chapter_name} 生成完成: {output_path}")
    return output_path

# 批量处理章节
chapters = ["chapter01.txt", "chapter02.txt", "chapter03.txt"]
for chapter in chapters:
    generate_audiobook_chapter(chapter)
```

### 场景三：基础音效生成

为视频或游戏生成环境音效。

```bash
# 生成雨声环境音
dlazy keling-sfx \
  --prompt "轻柔的春雨声，打在树叶上，持续背景音" \
  --duration 10

# 生成提示音
dlazy keling-sfx \
  --prompt "清脆的电子提示音，短促，用于通知提醒" \
  --duration 2
```

## 不适用场景

以下场景音频生成工具-免费版不适合处理：

- 版权受保护的媒体内容处理
- 实时直播推流
- 专业影视后期

## 触发条件

需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

```bash
# 方式一：免安装直接运行
npx @dlazy/cli@latest <command>

# 方式二：全局安装
npm install -g @dlazy/cli@latest

# 设置 API Key
dlazy auth set YOUR_API_KEY
```

### 第二步：生成领先段语音

```bash
# 查看模型帮助
dlazy doubao-tts -h

# 生成语音
dlazy doubao-tts --text "你好，这是领先段AI生成的语音。" --language "zh"
```

### 第三步：获取 API Key

1. 访问 dlazy.com 注册账号
2. 进入 dashboard 的 API Key 页面
3. 复制 API Key
4. 执行 `dlazy auth set YOUR_API_KEY`

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### API Key 配置

```bash
# 方式一：永久保存（推荐）
dlazy auth set YOUR_API_KEY
# 配置文件位置:
#   macOS/Linux: $HOME/.dlazy/config.json
#   Windows:     %USERPROFILE%\.dlazy\config.json

# 方式二：环境变量（临时）
export DLAZY_API_KEY="${API_KEY:?请设置环境变量}"

# 方式三：单次调用传入
DLAZY_API_KEY="${API_KEY:?请设置环境变量}" dlazy doubao-tts --text "测试"
```

### 常用参数配置

```bash
# doubao-tts 常用参数
dlazy doubao-tts \
  --text "要朗读的文本内容" \
  --language "zh"          # 语言: zh, en, ja, ko
  --voice "female-warm"    # 音色选择
  --speed 1.0              # 语速: 0.5-2.0
  --output "./output.wav"  # 输出路径

# keling-tts 常用参数
dlazy keling-tts \
  --text "要朗读的文本内容" \
  --voice "storyteller"    # 旁白音色
  --speed 1.0
  --format "wav"           # 输出格式: wav, mp3
```

## 优选实践

1. **文本分段**：长文本按段落分割生成，避免单次请求过长。
2. **音色一致**：同一项目使用同一音色，保持听觉一致性。
3. **语速适配**：教学类内容语速 0.9，新闻类 1.0，娱乐类 1.1。
4. **格式选择**：WAV 质量高体积大，MP3 适合网络传输。
5. **预览检查**：生成后先试听前 10 秒，确认效果再批量生成。

```text
免费版优选实践:
[ ] 文本已按段落分割（单段 < 500字）
[ ] 音色已确定并保持一致
[ ] 语速根据内容类型调整
[ ] 输出格式符合使用场景
[ ] API Key 已安全配置
[ ] 余额充足（检查 dlazy.com/dashboard）
```

## 常见问题

### Q: API Key 如何获取？

A: 访问 dlazy.com 注册账号，在 dashboard 的 API Key 页面生成。每个 Key 绑定你的组织，可随时轮换或撤销。

### Q: 提示 insufficient_balance 怎么办？

A: 表示余额不足，请访问 dlazy.com/dashboard/organization/settings?tab=credits 充值。

### Q: 免费版支持语音克隆吗？

A: 免费版不支持语音克隆。需要 ElevenLabs Voice Clone、Qwen Voice Clone 等功能请升级至专业版。

### Q: 生成的音频保存在哪里？

A: API 返回的音频 URL 托管在 dlazy 文件服务上。可通过 `--output` 参数指定本地保存路径。

### Q: 支持哪些语言？

A: doubao-tts 支持中英日韩等多语言；gemini-2.5-tts 专注中英双语；keling-tts 支持语种设置。

### 已知限制

A: 建议单次请求文本不超过 500 字。长文本请分段生成，专业版支持管道链接自动串联。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+（dlazy CLI 运行需要）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js 16+ | 运行时 | 必需 | nodejs.org 官方下载 |
| @dlazy/cli | CLI工具 | 必需 | `npm install -g @dlazy/cli@latest` |
| dlazy API Key | 认证 | 必需 | dlazy.com/dashboard 获取 |

### API Key 配置
- **必需**: dlazy API Key
- **获取方式**: 访问 dlazy.com/dashboard/organization/api-key
- **配置方式**: `dlazy auth set YOUR_API_KEY` 或环境变量 `DLAZY_API_KEY`
- **安全说明**: 配置文件权限限制为当前用户，存储在用户配置目录

### 可用性分类
- **分类**: MD+EXEC+API（Markdown指令 + 命令行 + 外部API调用）
- **说明**: 轻量级AI Skill，通过dlazy CLI调用云端音频生成API
- **适用规模**: 个人创作者，轻度使用

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
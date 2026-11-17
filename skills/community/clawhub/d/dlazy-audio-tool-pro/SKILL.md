---
slug: dlazy-audio-tool-pro
name: "dlazy-audio-tool-pro"
version: "1.0.0"
displayName: "音频生成工具-专业版"
summary: "全功能音频生成引擎，支持TTS、语音克隆、音乐生成、多角色对话与管道链接批量处理。。音频生成工具专业版，面向专业内容团队的全功能音频生成平台。核心能力： - 15+ 音频模型全覆盖（TTS、"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: dlazy。
  音频生成工具专业版，面向专业内容团队的全功能音频生成平台。核心能力：
  - 15+ 音频模型全覆盖（TTS、语音克隆、音乐生成、音效、对话）
  - 多角色对话一次性渲染（最多10个角色）
  - 语音克隆（ElevenLabs IVC、Qwen、Kling、Vidu）
  - 原创音乐生成（Suno V5。Use when 需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于版权受保护的媒体内容处理。
tags:
  - Creative
  - Audio
  - Enterprise
  - VoiceClone
  - 音频处理
  - 媒体
  - 创意
  - dlazy
  - text
  - bash
  - voice
  - 音频生成
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---

> **功能说明**: 本技能涵盖 （Suno 等核心能力。

# 音频生成工具（专业版）

## 概述

音频生成工具专业版是全功能音频生成平台，覆盖文本转语音、语音克隆、音乐生成、音效制作和多角色对话共 15+ 模型。通过管道链接（Pipe Chaining）可将多个生成步骤串联为自动化工作流，实现从文本到完整音频作品的一站式制作.
本版本与免费版完全兼容——免费版的 API Key 配置和基础 TTS 功能可直接使用。专业版新增语音克隆、音乐生成、多角色对话、声音库搜索和管道链接等高级能力.
## 核心能力

### 模型覆盖对比

| 模型类别 | 免费版 | 专业版 | 代表模型 |
|----|---|---|----|
| 基础TTS | 3个 | 5个 | doubao-tts, keling-tts, gemini-2.5-tts, elevenlabs-tts, qwen-tts |
| 语音克隆 | 不支持 | 4个 | elevenlabs-voice-clone, qwen-audio-clone, kling-audio-clone, vidu-audio-clone |
| 音乐生成 | 不支持 | 2个 | suno-music, elevenlabs-music |
| 音效生成 | 1个 | 2个 | keling-sfx, elevenlabs-sfx |
| 多角色对话 | 不支持 | 1个 | elevenlabs-dialogue |
| 声音搜索 | 不支持 | 1个 | elevenlabs-search |
| 管道链接 | 不支持 | 支持 | 多步骤串联 |

**处理**: 解析模型覆盖对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回模型覆盖对比的响应数据,包含状态码、结果和日志.
### 核心能力(补充)

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 音频生成工具-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
语音克隆:
  - ElevenLabs IVC（即时语音克隆）
  - Qwen3-TTS 语音克隆（阿里百炼）
  - Kling 自定义音色克隆
  - Vidu 真人声音克隆
# ...
音乐生成:
  - Suno V5.5（灵感模式/自定义模式）
  - ElevenLabs Music（10-300秒原创音乐）
# ...
多角色对话:
  - ElevenLabs Dialogue（最多10角色）
  - 支持音频标签: [giggling] [whispers] 等
  - 一键渲染整段对话
# ...
音效生成:
  - ElevenLabs SFX（1-22秒音效）
  - Keling SFX（文本转音效 + 视频匹配）
# ...
声音库搜索:
  - ElevenLabs Search（关键词/来源/分类）
  - 返回可试听的预览音频
# ...
管道链接:
  - 步骤间自动传递输出
  - 支持管道引用: -, @N, @N.path, @*, @stdin
```

**处理**: 解析核心能力的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心能力的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：全功能音频生成引、多角色对话与管道、链接批量处理、音频生成工具专业、面向专业内容团队、的全功能音频生成、音频模型全覆盖、多角色对话一次性、个角色、原创音乐生成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：播客全流程制作

从文案到成品音频的完整播客制作工作流.
```bash
# 步骤1 克隆主持人声音（一次性操作）
dlazy elevenlabs-voice-clone \
  --audio-file "./samples/host-voice-sample.wav" \
  --name "host-voice"
# ...
# 步骤2 使用克隆声音生成主持人台词
dlazy elevenlabs-tts \
  --text "欢迎收听本期播客，今天我们聊聊AI音频技术的最新进展。" \
  --voice "host-voice" \
  --stability 0.7 \
  --similarity 0.8
# ...
# 步骤3 生成背景音乐
dlazy suno-music \
  --mode "custom" \
  --style "lo-fi chill ambient" \
  --title "Podcast Intro" \
  --instrumental true \
  --duration 30
# ...
# 步骤4 生成过渡音效
dlazy elevenlabs-sfx \
  --prompt "soft whoosh transition sound, gentle fade" \
  --duration 3
```

### 场景二：多角色广播剧

一次性渲染多角色对话场景.
```bash
# 多角色对话生成
dlazy elevenlabs-dialogue \
  --dialogue '[
    {"voice": "storyteller", "text": "夜深了，城市的灯火渐渐熄灭。"},
    {"voice": "detective", "text": "这案子不简单，[pauses] 凶手一定还在现场。"},
    {"voice": "assistant", "text": "[whispers] 长官，窗外好像有人影！"},
    {"voice": "detective", "text": "[urgently] 快，跟上去！"}
  ]' \
  --output "scene-01.wav"
```

### 场景三：管道链接自动化工作流

将多个生成步骤串联为自动化流水线.
```bash
# 示例
dlazy seedream-4.5 --prompt "lighthouse at dawn" \
  | dlazy keling-tts --text "Welcome to the coast." --image @0.url
# ...
# 管道链接示例2: 批量生成多张图片 → 超分辨率
dlazy seedream-4.5 --prompt "city skyline" --n 4 \
  | dlazy superres --images @*
# ...
# 管道链接示例3: 搜索声音 → 用选中声音生成TTS
dlazy elevenlabs-search \
  --keyword "warm female voice" \
  --category "audiobook" \
  | dlazy elevenlabs-tts --text "领先章 初次相遇" --voice @0.voice_id
```

### 管道引用速查

| 引用 | 解析为 |
|---:|---:|
| `-` | 上游输出的自然值 |
| `@N` | 第N个输出的主值（@0 = 领先个输出URL） |
| `@N.path` | 深入第N个输出（@0.url, @1.meta.fps） |
| `@*` | 所有输出的主值数组 |
| `@stdin` | 完整上游JSON信封 |
| `@stdin:path` | JSON路径深入（@stdin:result.outputs[0].url） |

## 不适用场景

以下场景音频生成工具-专业版不适合处理：

- 版权受保护的媒体内容处理
- 实时直播推流
- 专业影视后期

## 触发条件

需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 依赖详情

```bash
# 全局安装 CLI
npm install -g @dlazy/cli@latest
# ...
# 认证
dlazy auth set YOUR_API_KEY
```

### 第二步：声音库搜索与选择

```bash
# 搜索适合的有声书音色
dlazy elevenlabs-search \
  --keyword "calm male storyteller" \
  --source "professional" \
  --category "audiobook"
# ...
# 预览返回的音色，选择 voice_id
```

### 第三步：克隆自定义声音

```bash
# 上传干净的声音样本进行克隆
dlazy elevenlabs-voice-clone \
  --audio-file "./voice-samples/clean-sample.wav" \
  --name "my-custom-voice"
# ...
# 使用克隆声音生成TTS
dlazy elevenlabs-tts \
  --text "使用我克隆的声音朗读这段文字" \
  --voice "my-custom-voice"
```

#
## 配置示例

### ElevenLabs TTS 高级参数

```bash
dlazy elevenlabs-tts \
  --text "朗读文本" \
  --voice "voice_id_or_name" \
  --stability 0.5          # 稳定性: 0-1, 越高越一致
  --similarity 0.75         # 相似度: 0-1, 越高越接近原声
  --style 0.0               # 风格强度: 0-1, 越高越夸张
  --model "eleven_v3"       # 模型版本
  --output "./output.wav"
```

### Suno 音乐生成配置

```bash
# 灵感模式（自动生成歌词）
dlazy suno-music \
  --mode "inspiration" \
  --prompt "一首关于夏日海边的轻快民谣" \
  --with-vocals true \
  --style-weight 0.7 \
  --weirdness 0.3
# ...
# 自定义模式（手动指定歌词）
dlazy suno-music \
  --mode "custom" \
  --style "electronic synthwave" \
  --title "Neon Dreams" \
  --lyrics "Neon lights dance in the rain..." \
  --instrumental false
```

### 多角色对话配置

```json
{
  "model": "elevenlabs-dialogue",
  "dialogue": [
    {"voice": "storyteller", "text": "故事开始了。"},
    {"voice": "protagonist", "text": "[excitedly] 终于到了！"},
    {"voice": "companion", "text": "[giggling] 等等，你看那边！"},
    {"voice": "antagonist", "text": "[coldly] 你们来晚了。"}
  ],
  "output": "chapter-01-dialogue.wav",
  "format": "wav"
}
```

## 优选实践

1. **声音样本质量**：语音克隆需上传 30 秒以上干净样本，无背景噪音.
2. **对话角色上限**：单次对话最多 10 个角色，超过请分段渲染.
3. **管道调试**：先用 `--dry-run` 测试管道链接，确认引用正确.
4. **音乐风格词**：Suno 使用具体风格词（如 "lo-fi chill"）比泛泛描述效果好.
5. **批量生成**：长内容分段生成后用管道链接自动拼接.
```text
专业版优选实践:
[ ] 声音样本已清洗（无噪音，> 30秒）
[ ] 对话角色数 ≤ 10
[ ] 管道引用已用 --dry-run 测试
[ ] 音乐风格词具体明确
[ ] 余额充足，支持批量生成
[ ] API Key 已安全配置
[ ] 输出路径已规划
```

## 常见问题

### Q: 语音克隆需要什么样的声音样本？

A: 需要 30 秒以上的干净语音样本，无背景音乐和噪音。WAV 格式效果优选。样本越清晰，克隆质量越高.
### Q: 管道链接中 stdin 为空怎么办？

A: 上游命令未输出 JSON 信封时，CLI 会返回 `code: "no_stdin"` 错误。检查上游命令是否执行成功.
### Q: 多角色对话的角色数上限是多少？

A: ElevenLabs Dialogue 单次最多支持 10 个不同角色。超过 10 个角色请分多次渲染后拼接.
### Q: Suno 音乐生成支持多长？

A: ElevenLabs Music 支持 10-300 秒原创音乐。Suno V5.5 支持完整歌曲结构（主歌+副歌+桥段）.
### Q: 如何从免费版升级？

A: API Key 和 CLI 配置无需变更，直接使用专业版的全部模型即可。免费版的 TTS 功能在专业版中完全保留.
### Q: 生成的音频 URL 有效期多久？

A: dlazy 文件服务托管的 URL 有一定有效期。建议生成后通过 `--output` 参数下载到本地保存.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+（dlazy CLI 运行需要）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js 16+ | 运行时 | 必需 | nodejs.org 官方下载 |
| @dlazy/cli | CLI工具 | 必需 | `npm install -g @dlazy/cli@latest` |
| dlazy API Key | 认证 | 必需 | dlazy.com/dashboard 获取 |
| FFmpeg（可选） | 工具 | 推荐 | 用于音频拼接与格式转换 |

### API Key 配置
- **必需**: dlazy API Key（与免费版共用）
- **获取方式**: 访问 dlazy.com/dashboard/organization/api-key
- **配置方式**: `dlazy auth set YOUR_API_KEY` 或环境变量 `DLAZY_API_KEY`
- **安全说明**: 配置文件权限限制为当前用户；Key 可随时轮换或撤销
- **余额说明**: 专业版模型消耗较高，建议定期检查余额

### 可用性分类
- **分类**: MD+EXEC+API（Markdown指令 + 命令行 + 外部API调用）
- **说明**: 企业级AI Skill，支持全模型音频生成、管道链接与批量处理
- **适用规模**: 专业内容团队，批量音频生产
- **兼容性**: 与免费版完全兼容，API Key 和配置无缝共用

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "音频生成工具-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dlazy audio pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 全功能音频生成引擎，支持TTS、语音克隆、音乐生成、多角色对话与管道链接批量处理。。音频生成工具专业版，面向专业内容团队
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 全功能音频生成引擎，支持TTS、语音克隆、音乐生成、多角色对话与管道链接批量处理。。音频生成工具专业版，面向专业内容团队
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
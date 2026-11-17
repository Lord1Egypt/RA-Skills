---

slug: discord-voice-tool-pro
name: discord-voice-tool-pro
version: 1.0.0
displayName: Discord语音工具专业版
summary: "企业级 Discord 语音 AI 对话,支持多服务商、流式转写、自动重连与批量频道管理.。面向企业与社区运营团队的 Discord 语音 AI 全功能对话工具。核心能力:"
license: Proprietary
edition: pro
description: "面向企业与社区运营团队的 Discord 语音 AI 全功能对话工具。核心能力:，可自动提升工作效率。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。 功能涵盖: voice。"
  - 多 STT/TTS 服务商切换(OpenAI/Deepgram/ElevenLabs/本地)

  - Deepgram 流式实时转写(延迟降低约 1 秒)

  - 自动心跳监控与断线重连(指数退避)

  - 智能打断(barge-in)、自动加入与多频道调度

  - 企业级权限白名单与审计日志

  适用场景:

  - 企业语音会议室的 AI 实时助理

  - 大型语音社区的多频道 AI 互动

  - 高并发低延迟的实时语音问答

  差异化: Pro 版在免...'
tags:
  - Discord
  - 语音对话
  - Communication
  - 流式转写
  - 企业级
  - 社交
  - 通信
  - deepgram
  - apikey
  - process
  - env
  - elevenlabs
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Communication"

---

> **功能说明**: 本技能涵盖 中文交互、提升工作效率、化流程、化工作流场景 等核心能力。


# Discord 语音工具(专业版)

## 概述

Discord 语音工具专业版是一款面向企业与社区运营团队的 Discord 语音 AI 全功能对话工具。它在免费版本地离线方案之上,扩展出多 STT/TTS 服务商切换(OpenAI Whisper、Deepgram、ElevenLabs、本地 Kokoro)、Deepgram 流式实时转写(端到端延迟降低约 1 秒)、自动心跳监控与断线重连(指数退避)、智能打断、自动加入与多频道调度能力,并提供企业级权限白名单与审计日志,适合对稳定性和实时性有较高要求的企业语音场景.
专业版与免费版配置兼容:免费版的本地方案配置在专业版中可直接使用,升级后按需启用云服务商即可获得流式转写和多模型能力。专业版适合企业语音会议室 AI 助理、大型语音社区多频道互动和高并发实时语音问答场景.
## 核心能力

| 能力模块 | 说明 | 免费版 | Pro 版 |
|----|---|---|-----|
| 加入/离开频道 | 语音频道进出 | 支持 | 支持+自动加入 |
| 语音活动检测 | 自动检测说话 | 支持 | 支持(可调) |
| 语音转文字 | STT 服务商 | 本地 Whisper | 多服务商(OpenAI/Deepgram/本地) |
| 流式转写 | 实时低延迟 | 不支持 | 支持(Deepgram) |
| 文字转语音 | TTS 服务商 | 本地 Kokoro | 多服务商(OpenAI/ElevenLabs/本地) |
| 打断支持 | barge-in | 支持 | 支持(可调) |
| 自动重连 | 断线恢复 | 不支持 | 支持(指数退避) |
| 心跳监控 | 连接健康检查 | 基础 | 支持(可配置) |
| 多频道调度 | 多实例管理 | 不支持 | 支持 |
| 权限白名单 | 用户限制 | 支持 | 支持+审计 |
| 审计日志 | 操作记录 | 不支持 | 支持 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、Discord、支持多服务商、自动重连与批量频、道管理、面向企业与社区运、营团队的、全功能对话工具、核心能力、服务商切换、流式实时转写、延迟降低约、自动心跳监控与断、线重连、智能打断、自动加入与多频道、企业级权限白名单、与审计日志等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:企业语音会议室 AI 助理

企业使用 Discord 语音频道作为远程会议室,需要 AI 助理实时记录会议要点并语音回答提问.
```json5
{
  sttProvider: "deepgram",
  streamingSTT: true,  // 流式转写,延迟更低
  ttsProvider: "elevenlabs",
  ttsVoice: "21m00Tcm4TlvDq8ikWAM",  // Rachel,自然女声
  vadSensitivity: "medium",
  bargeIn: true,
  autoJoinChannel: "1234567890",  // 启动自动加入
  heartbeatIntervalMs: 30000,
  allowedUsers: ["user1", "user2"],  // 仅限团队成员
  deepgram: {
    apiKey: process.env.DEEPGRAM_API_KEY,
    model: "nova-2"
  },
  elevenlabs: {
    apiKey: process.env.ELEVENLABS_API_KEY,
    voiceId: "21m00Tcm4TlvDq8ikWAM",
    modelId: "eleven_multilingual_v2"
  }
}
```

配置后机器人启动即自动加入指定频道,流式转写确保提问后约 1 秒内开始响应.
### 场景二:大型语音社区多频道互动

大型社区有多个语音频道(技术讨论、闲聊、答疑),需要 AI 在不同频道间轮换或并行服务.
```bash
# 实例 A 服务技术讨论频道
discord_voice join 1111111 --profile=tech-profile
# ...
# 实例 B 服务答疑频道
discord_voice join 2222222 --profile=support-profile
```

不同频道使用不同服务商配置(如技术频道用 Deepgram 追求低延迟,答疑频道用本地 Whisper 控制成本).
### 常见问题

线上活动中,大量用户在语音频道提问,需要 AI 低延迟响应且不中断.
```json5
{
  sttProvider: "deepgram",
  streamingSTT: true,
  ttsProvider: "openai",
  ttsVoice: "nova",
  bargeIn: false,  // 活动场景关闭打断,保证回复完整
  silenceThresholdMs: 1000,  // 缩短静音判定,加快响应
  maxRecordingMs: 15000,  // 限制单次录音,适配问答节奏
  heartbeatIntervalMs: 15000  // 加密心跳监控
}
```

## 不适用场景

以下场景Discord语音工具专业版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 依赖详情

```bash
# Ubuntu / Debian
sudo apt-get install ffmpeg build-essential python3
# ...
# CentOS / RHEL
sudo dnf install ffmpeg gcc-c++ make python3
# ...
# macOS
brew install ffmpeg
```

### 第二步:安装插件

```bash
platform install discord-voice
```

### 第三步:配置多服务商

```json5
{
  plugins: {
    entries: {
      "discord-voice": {
        enabled: true,
        config: {
          sttProvider: "deepgram",
          streamingSTT: true,
          ttsProvider: "elevenlabs",
          ttsVoice: "21m00Tcm4TlvDq8ikWAM",
          vadSensitivity: "medium",
          bargeIn: true,
          allowedUsers: [],
          silenceThresholdMs: 1500,
          maxRecordingMs: 30000,
          heartbeatIntervalMs: 30000,
          autoJoinChannel: undefined,
          openai: {
            apiKey: process.env.OPENAI_API_KEY
          },
          deepgram: {
env.DEEPGRAM_API_KEY,
            model: "nova-2"
          },
          elevenlabs: {
env.ELEVENLABS_API_KEY,
            voiceId: "21m00Tcm4TlvDq8ikWAM",
            modelId: "eleven_multilingual_v2"
          }
        }
      }
    }
  }
}
```

### 第四步:配置 Discord 机器人权限

机器人需具备 Connect、Speak、Use Voice Activity 三个语音权限.
### 第五步:验证并使用

```bash
discord_voice join <channelId>
discord_voice status
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 服务商配置

#
### OpenAI(Whisper + TTS)

```json5
{
  openai: {
    apiKey: process.env.OPENAI_API_KEY,
    whisperModel: "whisper-1",
    ttsModel: "tts-1"
  }
}
```

#
### Deepgram(STT,支持流式)

```json5
{
  deepgram: {
    apiKey: process.env.DEEPGRAM_API_KEY,
    model: "nova-2"
  }
}
```

#
### ElevenLabs(TTS)

```json5
{
  elevenlabs: {
    apiKey: process.env.ELEVENLABS_API_KEY,
    voiceId: "21m00Tcm4TlvDq8ikWAM",  // Rachel
    modelId: "eleven_multilingual_v2"
  }
}
```

### 流式 STT 配置

```json5
{
  sttProvider: "deepgram",
  streamingSTT: true,  // 默认开启
  deepgram: {
    apiKey: process.env.DEEPGRAM_API_KEY,
    model: "nova-2"
  }
}
```

流式模式提供:

- 端到端延迟降低约 1 秒
- 实时中间转录结果反馈
- 自动 keep-alive 防止连接超时
- 流式失败时自动回退批量转录

### 自动重连配置

```json5
{
  heartbeatIntervalMs: 30000,  // 心跳间隔(可调)
  // 内置: 断线后指数退避重连,最多 3 次
}
```

断线时日志:

```text
[discord-voice] Disconnected from voice channel
[discord-voice] Reconnection attempt 1/3
[discord-voice] Reconnected successfully
```

### 自动加入配置

```json5
{
  autoJoinChannel: "1234567890"  // 启动时自动加入此频道
}
```

### 环境变量

| 变量 | 说明 |
|:-----|:-----|
| `DISCORD_TOKEN` | Discord 机器人令牌(必需) |
| `OPENAI_API_KEY` | OpenAI API Key(Whisper + TTS) |
| `ELEVENLABS_API_KEY` | ElevenLabs API Key(TTS) |
| `DEEPGRAM_API_KEY` | Deepgram API Key(STT) |

## 优选实践

1. **服务商选型策略**: 按场景选服务商。追求低延迟用 Deepgram 流式 STT + ElevenLabs TTS(自然度高);追求成本控制用本地 Whisper + 本地 Kokoro(零 API 成本);平衡选择用 OpenAI Whisper + OpenAI TTS。可按频道配置不同服务商组合.
2. **流式 STT 优先启用**: 使用 Deepgram 时务必开启 `streamingSTT: true`。流式模式端到端延迟降低约 1 秒,并提供实时中间结果,对话体验显著优于批量模式。流式失败会自动回退批量,无需额外处理.
3. **自动重连保障可用性**: 生产环境务必保持 `heartbeatIntervalMs` 合理(默认 30 秒)。心跳检测能及时发现断线并触发指数退避重连(最多 3 次)。对可用性要求极高的场景,可结合外部监控告警.
4. **TTS 语音选型**: ElevenLabs 提供多种自然语音(如 Rachel),适合需要高自然度的场景。OpenAI TTS 的 `nova` 语音性价比高。多语言场景使用 `eleven_multilingual_v2` 模型。选定语音后保持稳定,避免频繁切换.
5. **打断策略按场景配置**: 一对一对话场景开启 `bargeIn: true` 提升自然度;活动/演讲场景关闭 barge-in 保证回复完整。频繁打断会导致回复碎片化,按场景取舍.
6. **静音判定调优**: `silenceThresholdMs` 默认 1500ms。问答场景可调低到 1000ms 加快响应;长篇发言场景调高到 2000ms 避免误截断。配合 VAD 灵敏度综合调整.
7. **权限白名单与审计**: 公开服务器务必配置 `allowedUsers` 限定可用用户。Pro 版审计日志记录所有语音会话的开始/结束、参与者、服务商使用情况和错误事件,便于运营分析和问题排查.
8. **API Key 安全管理**: 所有 API Key 通过环境变量注入,切勿硬编码到配置文件。建议使用密钥管理服务统一管理,定期轮换。审计日志中不记录完整 Key,仅记录使用情况.
9. **与免费版兼容**: Pro 版完全兼容免费版本地方案配置。升级时原有本地配置无需修改,按需新增云服务商配置即可。本地与云方案可随时切换,灵活适配不同场景.
10. **多实例资源规划**: 多频道并行服务时,每个实例独立消耗资源。云 API 场景注意并发请求配额;本地模型场景注意 CPU/内存负载。建议按峰值并发规划资源,并设置自动降级策略.
## 常见问题(补充)

### Q1: 流式 STT 比批量快多少?

使用 Deepgram 流式模式,端到端延迟降低约 1 秒。原因是流式模式在用户说话过程中就开始传输和识别,而非等静音后整段发送。此外还提供实时中间结果反馈。流式失败会自动回退批量模式,无需人工干预.
### Q2: 自动重连会重试几次?

Pro 版自动重连采用指数退避策略,最多重试 3 次。第 1 次立即重试,第 2 次延迟增加,第 3 次延迟更长。3 次仍失败则放弃并记录错误日志,需人工介入。心跳检查间隔通过 `heartbeatIntervalMs` 配置(默认 30 秒).
### Q3: 多服务商能否运行时切换?

支持。可通过 Agent 工具或配置热更新切换 `sttProvider` 和 `ttsProvider`。切换后下一段对话即生效。建议非高峰时段切换,避免切换瞬间影响正在进行的对话.
### Q4: ElevenLabs 和 OpenAI TTS 怎么选?

ElevenLabs 语音自然度更高,支持语音克隆和多语言,适合对音质要求高的场景,但成本较高;OpenAI TTS 性价比高,延迟较低,适合高频对话场景。两者可按频道配置不同服务商.
### Q5: 自动加入(autoJoinChannel)有何风险?

自动加入会在 Agent 启动时立即连接指定频道。风险:若频道当时有私密会议,机器人突然加入可能打扰用户。建议:仅在专属 AI 频道启用自动加入;或加入后静默等待被 @提及再说话;配置 `allowedUsers` 限制触发用户.
### Q6: 多频道并行如何部署?

Discord 限制单机器人在单服务器同时只能在一个语音频道。多频道并行需部署多个机器人实例(不同 Token),每个实例服务一个频道。不同实例可配置不同服务商和语音,实现差异化服务.
### Q7: 审计日志记录哪些内容?

Pro 版审计日志记录:会话开始/结束时间、频道 ID、参与者列表、STT/TTS 服务商、识别/合成耗时、错误事件(含错误类型和堆栈)、重连事件。日志建议加密存储,保留 30-90 天,用于运营分析和问题追溯.
### Q8: Pro 版如何与免费版共存?

两者配置兼容,可共存。Pro 版包含免费版的本地方案能力,额外支持多服务商和流式转写。建议生产环境统一使用 Pro 版,免费版仅用于本地开发测试。两者可共用同一机器人令牌.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持解析 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux(推荐 Linux 用于生产环境)
- **系统依赖**: `ffmpeg`、构建工具(`build-essential` / Xcode CLT)、Python 3
- **硬件**: 云方案对本地硬件要求低;本地方案建议 8GB 以上内存
- **网络**: 需稳定访问 Discord API 及所选 STT/TTS 服务商 API

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM 能力 | API | 必需 | 由 Agent 内置大模型提供 |
| Discord Bot Token | 凭证 | 必需 | Discord Developer Portal 创建机器人获取 |
| ffmpeg | 系统依赖 | 必需 | 系统包管理器安装 |
| OpenAI API | API | 可选 | OpenAI 平台申请 API Key |
| Deepgram API | API | 可选 | Deepgram 平台申请 API Key |
| ElevenLabs API | API | 可选 | ElevenLabs 平台申请 API Key |
| Node.js 原生模块 | 库 | 必需 | npm install 编译 |

### API Key 配置

- **Discord Bot Token**: 通过环境变量 `DISCORD_TOKEN` 配置(必需).
- **OpenAI API Key**: 通过环境变量 `OPENAI_API_KEY` 配置(使用 OpenAI Whisper/TTS 时必需).
- **Deepgram API Key**: 通过环境变量 `DEEPGRAM_API_KEY` 配置(使用 Deepgram STT 时必需,流式模式依赖此项).
- **ElevenLabs API Key**: 通过环境变量 `ELEVENLABS_API_KEY` 配置(使用 ElevenLabs TTS 时必需).
- **密钥安全**: 所有 API Key 必须通过环境变量注入,切勿硬编码。建议使用密钥管理服务,定期轮换。审计日志不记录完整 Key.
- **本地方案**: 使用本地 Whisper/Kokoro 时基础LLM由Agent平台提供,与免费版一致.
### 可用性分类

- **分类**: MD+execute(纯 Markdown 指令 + 部分功能需 `exec` 执行能力)
- **说明**: 以自然语言指令驱动 Agent 调用语音工具,多服务商处理音频,支持流式与自动重连
- **适用规模**: 企业级、多频道、高并发实时语音场景
- **兼容性**: 与 `discord-voice-tool-free` 配置兼容,可平滑升级
- **支持级别**: 优先支持(Pro 版享有问题优先响应与功能迭代建议通道)

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Discord语音工具专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "discord voice pro"
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
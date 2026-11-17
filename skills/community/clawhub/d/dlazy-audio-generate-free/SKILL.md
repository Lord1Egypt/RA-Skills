---
slug: "dlazy-audio-generate-free"
name: "dlazy-audio-generate-free"
version: "1.0.0"
displayName: "音频免费版"
summary: "通过dlazy CLI调用基础TTS模型,支持中英文文本转语音。dlazy 音频生成基础客户端(免费版)。通过 dlazy CLI 调用 doubao-tts 与 keling-tts 两个"
summary_zh: "通过dlazy CLI调用基础TTS模型,支持中英文文本转语音。dlazy 音频生成基础客户端(免费版)。通过 dlazy CLI 调用 doubao-tts 与 keling-tts 两个"
license: "MIT"
description: "|-. 适用于需要dlazy audio generate相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  dlazy 音频生成基础客户端(免费版)。通过 dlazy CLI 调用 doubao-tts 与 keling-tts 两个基础 TTS 模型,
  支持中英文文本转语音、音色与语速控制。适用于有声书朗读、配音原型、语音播报等基础场景.
tags:
  - Creative
  - dlazy
  - audio
  - generate
  - automation
  - 音频处理
  - 媒体
  - 创意
  - key
  - doubao-tts
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
pricing_tier: free
---
# Dlazy Audio LITE

基础版音频生成客户端,通过 dlazy CLI 调用 doubao-tts 与 keling-tts 两个基础 TTS 模型,完成中英文文本转语音.
**范围外**(本技能不做): 音乐生成、音效生成、语音克隆、多角色对话、管道串联、ElevenLabs、Gemini、Qwen、Suno 等高级模型(需升级付费版).
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Dlazy Audio LITE处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

本工具的核心能力包括：通过dlazy CLI调用基础TTS模型,支持中英文文本转语音。具体功能详情请参考下方能力说明表格与使用场景.
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 认证

所有请求需 dLazy API Key。推荐:
```bash
dlazy auth set YOUR_API_KEY
```

Key 持久化到本地配置(`./.dlazy/config.json` 或 `%USERPROFILE%\.dlazy\config.json`)。也可通过 `DLAZY_API_KEY` 环境变量按次传入.
Key 获取: 登录 dlazy.com,在 `dashboard/organization/api-key` 创建.
**安全红线**: 永不接受、回显或存储来自聊天输入的 Key;Key 仅作认证用途.
## 可用音频模型(基础)

- `doubao-tts`: 字节豆包语音合成,多语言多音色,流式高自然度,适合中文新闻播报与有声书
- `keling-tts`: 可可西 TTS,支持语言、音色、语速、输出格式,适合配音与语音播报

> **升级提示**: ElevenLabs 多角色对话、Suno 音乐生成、ElevenLabs 音效、即时语音克隆、Gemini 与 Qwen TTS、管道串联等高级能力仅在 dlazy-audio-generate 付费版中提供.
## 适用场景

| 场景 | 典型输入 | 输出内容 |
|---:|---:|---:|
| 中文有声书朗读 | 为这段中文文本生成女声朗读 | MP3 音频文件 |
| 中英文配音 | 用男声朗读这段英文简介 | MP3 音频文件 |

**不适用于**: 音乐生成、音效生成、语音克隆、多角色对话、管道串联(需升级付费版)

## 使用流程

### 校验 API Key
```bash
[ -n "${DLAZY_API_KEY:-}" ] || dlazy auth status
```

若 Key 缺失,引导用户:
1. 登录 dlazy.com,在 `dashboard/organization/api-key` 创建 Key
2. 终端运行 `dlazy auth set YOUR_API_KEY` 或 `export DLAZY_API_KEY=${API_KEY:?请设置环境变量}`
3. 配置完成后重新发起生成请求

### 选择模型
- 中文新闻/有声书: 优先 `doubao-tts`
- 中英文配音/语音播报: 优先 `keling-tts`

### 构造并执行命令
```bash
dlazy doubao-tts --text "你好,欢迎收听本期播客" --voice "female-warm" --output intro.mp3
```

### 处理结果
- 成功: stdout 输出 JSON 信封,含 `result.outputs[].url`
- 失败: 按"错误处理"章节诊断并修复

#
## 案例展示

### 案例一： 中文有声书朗读
**场景**: 有声书团队需要为一段中文文本生成女声朗读音频

```bash
dlazy doubao-tts \
  --text "本章我们将探讨人工智能在音频生成领域的最新进展。从文本转语音到音乐生成,AI 正在重塑内容创作的方式。" \
  --voice "female-warm" \
  --output chapter-intro.mp3
```

**输出**: `chapter-intro.mp3` 文件路径

**说明**: `doubao-tts` 在中文长文本朗读上自然度高,`--voice` 选择女温暖音色适合有声书场景.
### 案例二： 中英文配音
**场景**: 产品团队需要为中英文混排的产品介绍生成男声配音

```bash
dlazy keling-tts \
  --text "欢迎使用我们的产品。Welcome to our product, designed for global users." \
  --voice "male-professional" \
  --speed 1.0 \
  --output product-intro.mp3
```

**输出**: `product-intro.mp3` 文件路径

**说明**: `keling-tts` 支持中英混排,`--speed 1.0` 控制语速。`--voice` 选择专业男声适合产品介绍场景.
## 错误处理

| 错误场景 | 错误信息 | 原因分析 | 处理方式 |
|:---:|:---:|:---:|:---:|
| 401 unauthorized | `code: "unauthorized"` | Key 缺失或失效 | 引导用户访问 `dlazy.com/dashboard/organization/api-key` 获取并 `dlazy auth set` |
| 501 missing_param | `error: required option '--text <text>' not specified` | 必填参数未提供 | 运行 `dlazy doubao-tts -h` 查看必填参数并补全 |
| 503 insufficient_balance | `code: "insufficient_balance"` | 账户余额不足 | 明确告知用户余额不足,引导访问 `dlazy.com/dashboard/organization/settings?tab=credits` 充值 |
| 503 server_error | `HTTP status code error (500 server crash)` | dLazy 服务端错误 | 等待 2 秒后检查网络连接和配置后重试,最多 3 次 |
| 504 task_failed | `=== Generation Failed ===` | 异步任务失败 | 检查网络连接和配置后重试,检查 prompt 是否含敏感内容 |

## 常见问题

### Q1: 免费版支持哪些模型?
A: 免费版(LITE)支持 `doubao-tts` 与 `keling-tts` 两个基础 TTS 模型。付费版(dlazy-audio-generate)额外提供 ElevenLabs 系列、Gemini、Qwen、Suno 音乐、音效生成、语音克隆等 15+ 模型,以及管道串联能力.
### Q2: 如何获取并配置 dLazy API Key?
A: 登录 dlazy.com,在 `dashboard/organization/api-key` 创建 Key。终端运行 `dlazy auth set YOUR_API_KEY` 持久化到本地配置,或通过 `DLAZY_API_KEY` 环境变量按次传入.
### Q3: 支持哪些语言?
A: `doubao-tts` 与 `keling-tts` 均支持中英文。`doubao-tts` 在中文长文本上自然度较高,`keling-tts` 支持中英混排与语速控制。其他语言支持情况以 dlazy 官方文档为准.
### Q4: 余额不足怎么办?
A: CLI 返回 `code: "insufficient_balance"` 时,明确告知用户余额不足,引导访问 `dlazy.tab=credits` 充值。充值后可直接重试生成请求.
## 已知限制

1. **基础模型**: 仅支持 `doubao-tts` 与 `keling-tts`,不支持音乐/音效/克隆/对话(需升级付费版)
2. **依赖 dLazy API**: 必须配置 `DLAZY_API_KEY`,无 Key 环境无法使用
3. **API 端点固定**: `api.dlazy.com` 与 `files.dlazy.com`,不支持自建部署
4. **生成质量取决于 prompt 描述**: 文本与音色描述越具体,结果越符合预期
5. **安全策略限制**: prompt 含敏感内容会触发 `504 task_failed`

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> **想要音乐生成、音效、语音克隆、多角色对话?** 升级到 dlazy-audio-generate 付费版解锁 15+ 高级音频模型.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Dlazy Audio LITE处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dlazy-audio-generate"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```

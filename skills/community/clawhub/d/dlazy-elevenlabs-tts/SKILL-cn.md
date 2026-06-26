---
name: dlazy-elevenlabs-tts
version: 1.2.0
description: ElevenLabs eleven_v3 文本转语音，提供 12 种精选英文/多语种音色，支持稳定性、相似度、风格控制。适合配音、有声内容与角色对话。选择音色前，可以从 elevenlabs-search 检索合适的音色。
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': '当调用此技能时，可以使用 dlazy elevenlabs-tts -h 查看帮助信息。' },
  }
---

# dlazy-elevenlabs-tts

[English](./SKILL.md) · [中文](./SKILL-cn.md)

ElevenLabs eleven_v3 文本转语音，提供 12 种精选英文/多语种音色，支持稳定性、相似度、风格控制。适合配音、有声内容与角色对话。选择音色前，可以从 elevenlabs-search 检索合适的音色。

## 触发关键词

- elevenlabs-tts

## 身份验证 (Authentication)

所有请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

```bash
dlazy login
```

该命令使用设备码流程（远程终端也可用），登录成功后 **自动把 API key 写入本地 CLI 配置**，无需手动复制粘贴。

### 备选：手动设置 API Key

如果你已有 API key，也可以直接保存：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`），文件权限仅限当前操作系统用户访问。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 手动获取 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个 key 都属于你自己的 dLazy 组织，可在同一控制面板**随时轮换或吊销**。

## 关于与来源 (Provenance)

- **CLI 源代码**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.2.0 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.0`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。完整服务条款请参见 [dlazy.com](https://dlazy.com)。

## 使用方法

**CRITICAL INSTRUCTION FOR AGENT**:
执行 `dlazy elevenlabs-tts` 命令获取结果。

```bash
dlazy elevenlabs-tts -h

Options:
  --prompt [prompt]                    提示词
  --use_custom_voice [use_custom_voice]使用自定义音色 [default: false]
  --custom_voice_id [custom_voice_id]  自定义音色ID（点击搜索浏览音色库或直接粘贴 voice_id） [only when use_custom_voice="true"]
  --voice_language [voice_language]    语音语言 [default: multilingual] (choices: "multilingual")
  --voiceId [voiceId]                  音色ID Options depend on "voice_language". when voice_language="multilingual": 21m00Tcm4TlvDq8ikWAM (Rachel · 知性女声), EXAVITQu4vr4xnSDxMaL (Sarah · 年轻女声), AZnzlk1XvdvUeBnXmlld (Domi · 自信女声), MF3mGyEYCl7XYWbV9V6O (Elli · 甜美女声), ThT5KcBeYPX3keUQqHPh (Dorothy · 温柔女声), ErXwobaYiN019PkySvjV (Antoni · 沉稳男声), TxGEqnHWrfWFTfGW9XjX (Josh · 年轻男声), VR6AewLTigWG4xSOukaG (Arnold · 清晰男声), pNInz6obpgDQGcFmaJgB (Adam · 深沉男声), yoZ06aMxZJJ28mfd3POQ (Sam · 沙哑男声), onwK4e9ZLuTAKqWW03F9 (Daniel · 英伦男声), pqHfZKP75CvOlQylNhV4 (Bill · 中年男声) [default: 21m00Tcm4TlvDq8ikWAM] [options depend on --voice_language; voice_language=multilingual: 21m00Tcm4TlvDq8ikWAM (Rachel · 知性女声), EXAVITQu4vr4xnSDxMaL (Sarah · 年轻女声), AZnzlk1XvdvUeBnXmlld (Domi · 自信女声), MF3mGyEYCl7XYWbV9V6O (Elli · 甜美女声), ThT5KcBeYPX3keUQqHPh (Dorothy · 温柔女声), ErXwobaYiN019PkySvjV (Antoni · 沉稳男声), TxGEqnHWrfWFTfGW9XjX (Josh · 年轻男声), VR6AewLTigWG4xSOukaG (Arnold · 清晰男声), pNInz6obpgDQGcFmaJgB (Adam · 深沉男声), yoZ06aMxZJJ28mfd3POQ (Sam · 沙哑男声), onwK4e9ZLuTAKqWW03F9 (Daniel · 英伦男声), pqHfZKP75CvOlQylNhV4 (Bill · 中年男声)] [only when use_custom_voice="false"]
  --stability [stability]              稳定性 [default: 0.5]
  --similarity_boost [similarity_boost]相似度增强 [default: 0.75]
  --style [style]                      风格 [default: 0]
  --dry-run                            Print payload + cost estimate without calling API
  --no-wait                            Return generateId immediately for async tasks
  --timeout <seconds>                  Max seconds to wait for async completion (default: "1800")
  -h, --help                           display help for command
```

> Any flag also accepts pipe references — `-` (auto-pick from upstream stdin), `@N` (n-th output), `@N.path` (jsonpath into output), `@*` (all primary values), `@stdin` / `@stdin:path` (whole envelope). See `dlazy --help` for details.

## 输出格式

```json
{
  "ok": true,
  "result": {
    "tool": "elevenlabs-tts",
    "modelId": "elevenlabs-tts",
    "outputs": [
      {
        "type": "image",
        "id": "o_xxxxxxxx",
        "url": "https://files.dlazy.com/result.png",
        "mimeType": "image/png"
      }
    ]
  }
}
```

> Async tasks (when `--no-wait` is passed) return `outputs: []` and a `task: { generateId, status }` field instead. Use `dlazy status <generateId> --wait` to poll.

## 命令示例

```bash
dlazy elevenlabs-tts --prompt '提示词内容'
```

## 错误处理

| Code | 错误类型                   | 示例信息                                                                                       |
| ---- | -------------------------- | ---------------------------------------------------------------------------------------------- |
| 401  | 未授权 (API Key缺失或无效) | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                    |
| 501  | 缺少必填参数               | `error: required option '--prompt <prompt>' not specified`                                     |
| 502  | 本地文件读取失败           | `Error: Image file/Video file not found: C:\path\to\your\file`                                 |
| 503  | API 请求失败（余额不足）   | `ok: false, code: "insufficient_balance"`                                                      |
| 503  | API 请求失败（服务端错误） | `HTTP status code error (500 server crash)`                                                    |
| 504  | 异步任务执行失败           | `=== Generation Failed ===` / `{后端返回的具体失败原因，比如 "Prompt violates safety policy"}` |

> **智能体关键指令**:
>
> 1. 如果执行结果返回 `code: "insufficient_balance"` 且提示余额不足（Insufficient balance），您必须明确告知用户当前积分不足，并引导用户点击以下链接前往充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果执行结果返回 `code: "unauthorized"` 或提示缺少 API Key，您必须明确告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取 API Key 并使用 `dlazy auth set <key>` 保存，然后继续执行任务。

## Tips

Visit https://dlazy.com for more information.

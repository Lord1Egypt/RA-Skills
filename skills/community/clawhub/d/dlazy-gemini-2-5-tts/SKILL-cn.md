---
name: dlazy-gemini-2.5-tts
version: 1.2.0
description: 使用 Gemini 2.5 强大的文本转语音能力，生成多语言、高自然度的音频。
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
    'openclaw': { 'systemPrompt': '当调用此技能时，可以使用 dlazy gemini-2.5-tts -h 查看帮助信息。' },
  }
---

# dlazy-gemini-2.5-tts

[English](./SKILL.md) · [中文](./SKILL-cn.md)

使用 Gemini 2.5 强大的文本转语音能力，生成多语言、高自然度的音频。

## 触发关键词

- gemini tts
- 文本转语音
- 生成语音

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
执行 `dlazy gemini-2.5-tts` 命令获取结果。

```bash
dlazy gemini-2.5-tts -h

Options:
  --prompt [prompt]                    提示词
  --voice_language [voice_language]    语音语言 [default: cmn] (choices: "cmn", "en")
  --voiceName [voiceName]              音色名称 Options depend on "voice_language". when voice_language="cmn": Zephyr (Zephyr - 明亮), Puck (Puck - 欢快), Charon (Charon - 信息丰富), Kore (Kore - 坚定), Fenrir (Fenrir - 兴奋), Leda (Leda - 青春), Orus (Orus - 公正), Aoede (Aoede - 清爽), Callirrhoe (Callirrhoe - 轻松), Autonoe (Autonoe - 明亮), Enceladus (Enceladus - 气声), Iapetus (Iapetus - 清晰), Umbriel (Umbriel - 轻松愉快), Algieba (Algieba - 平滑), Despina (Despina - 平滑), Erinome (Erinome - 清晰), Algenib (Algenib - 沙哑), Rasalgethi (Rasalgethi - 信息丰富), Laomedeia (Laomedeia - 欢快), Achernar (Achernar - 柔和), Alnilam (Alnilam - 坚定), Schedar (Schedar - 均匀), Gacrux (Gacrux - 成熟), Pulcherrima (Pulcherrima - 转折), Achird (Achird - 友好), Zubenelgenubi (Zubenelgenubi - 随意), Vindemiatrix (Vindemiatrix - 温和), Sadachbia (Sadachbia - 活泼), Sadaltager (Sadaltager - 知识渊博), Sulafat (Sulafat - 偏高); when voice_language="en": Zephyr (Zephyr - Bright), Puck (Puck - Cheerful), Charon (Charon - Informative), Kore (Kore - Firm), Fenrir (Fenrir - Excitable), Leda (Leda - Youthful), Orus (Orus - Just), Aoede (Aoede - Breezy), Callirrhoe (Callirrhoe - Relaxed), Autonoe (Autonoe - Bright), Enceladus (Enceladus - Breath), Iapetus (Iapetus - Clear), Umbriel (Umbriel - Light), Algieba (Algieba - Smooth), Despina (Despina - Smooth), Erinome (Erinome - Clear), Algenib (Algenib - Gravelly), Rasalgethi (Rasalgethi - Informative), Laomedeia (Laomedeia - Cheerful), Achernar (Achernar - Soft), Alnilam (Alnilam - Firm), Schedar (Schedar - Even), Gacrux (Gacrux - Mature), Pulcherrima (Pulcherrima - Turning), Achird (Achird - Friendly), Zubenelgenubi (Zubenelgenubi - Casual), Vindemiatrix (Vindemiatrix - Gentle), Sadachbia (Sadachbia - Lively), Sadaltager (Sadaltager - Scholarly), Sulafat (Sulafat - High) [default: Kore] [options depend on --voice_language; voice_language=cmn: Zephyr (Zephyr - 明亮), Puck (Puck - 欢快), Charon (Charon - 信息丰富), Kore (Kore - 坚定), Fenrir (Fenrir - 兴奋), Leda (Leda - 青春), Orus (Orus - 公正), Aoede (Aoede - 清爽), Callirrhoe (Callirrhoe - 轻松), Autonoe (Autonoe - 明亮), Enceladus (Enceladus - 气声), Iapetus (Iapetus - 清晰), Umbriel (Umbriel - 轻松愉快), Algieba (Algieba - 平滑), Despina (Despina - 平滑), Erinome (Erinome - 清晰), Algenib (Algenib - 沙哑), Rasalgethi (Rasalgethi - 信息丰富), Laomedeia (Laomedeia - 欢快), Achernar (Achernar - 柔和), Alnilam (Alnilam - 坚定), Schedar (Schedar - 均匀), Gacrux (Gacrux - 成熟), Pulcherrima (Pulcherrima - 转折), Achird (Achird - 友好), Zubenelgenubi (Zubenelgenubi - 随意), Vindemiatrix (Vindemiatrix - 温和), Sadachbia (Sadachbia - 活泼), Sadaltager (Sadaltager - 知识渊博), Sulafat (Sulafat - 偏高); voice_language=en: Zephyr (Zephyr - Bright), Puck (Puck - Cheerful), Charon (Charon - Informative), Kore (Kore - Firm), Fenrir (Fenrir - Excitable), Leda (Leda - Youthful), Orus (Orus - Just), Aoede (Aoede - Breezy), Callirrhoe (Callirrhoe - Relaxed), Autonoe (Autonoe - Bright), Enceladus (Enceladus - Breath), Iapetus (Iapetus - Clear), Umbriel (Umbriel - Light), Algieba (Algieba - Smooth), Despina (Despina - Smooth), Erinome (Erinome - Clear), Algenib (Algenib - Gravelly), Rasalgethi (Rasalgethi - Informative), Laomedeia (Laomedeia - Cheerful), Achernar (Achernar - Soft), Alnilam (Alnilam - Firm), Schedar (Schedar - Even), Gacrux (Gacrux - Mature), Pulcherrima (Pulcherrima - Turning), Achird (Achird - Friendly), Zubenelgenubi (Zubenelgenubi - Casual), Vindemiatrix (Vindemiatrix - Gentle), Sadachbia (Sadachbia - Lively), Sadaltager (Sadaltager - Scholarly), Sulafat (Sulafat - High)]
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
    "tool": "gemini-2.5-tts",
    "modelId": "gemini-2.5-tts",
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
# 基础调用：
dlazy gemini-2.5-tts --prompt '提示词内容'

# 复杂调用：
dlazy gemini-2.5-tts --prompt '提示词内容'
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

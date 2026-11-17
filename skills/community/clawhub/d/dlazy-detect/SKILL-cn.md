---
name: dlazy-detect
version: 1.0.5
description: "检测图片、视频或音频是否由 AI 生成：包含人脸 deepfake 识别与疑似生成模型归因（Midjourney、Stable Diffusion、Sora 等），返回可用于判定的置信度分数。"
metadata:
  {
    'clawdbot':
      {
        'emoji': '🔍',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.3',
        'installAlternative': 'npx @dlazy/cli@1.2.3',
        'homepage': 'https://github.com/dlazy-ai/cli',
        'source': 'https://github.com/dlazy-ai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': '当调用此技能时，可以使用 dlazy detect -h 查看帮助信息。' },
  }
---

# AI 内容检测 AI Detect

[English](./SKILL.md) · [中文](./SKILL-cn.md)

检测图片、视频或音频是否由 AI 生成：包含人脸 deepfake 识别与疑似生成模型归因（Midjourney、Stable Diffusion、Sora 等），返回可用于判定的置信度分数。

## 触发关键词

- detect
- ai-detect
- ai-generated
- deepfake
- AI 检测
- 是不是 AI 生成

## 能检测什么

- **图片 / 视频**：是否 AI 生成（`ai_generated` 分数）、是否含 **deepfake**（换脸）、以及**疑似生成模型**（Midjourney、Stable Diffusion、DALL·E 等）。
- **音频**（纯音频文件，或视频里的音轨）：音频是否 AI 生成（`ai_generated_audio` 分数）。
- **不支持文字**——本模型仅支持图片、视频、音频。

> 推荐判定阈值：分数 **≥ 0.9** 视为 AI 生成。技能已按此阈值给出 `is_ai_generated` / `is_deepfake` 布尔结果。
>
> 注意：底层服务商（Hive V3 Playground）默认限速 **100 次/天**。

## 身份验证 (Authentication)

所有请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

```bash
dlazy login
```

该命令使用设备码流程（远程终端也可用），登录成功后 **自动把 API key 写入本地 CLI 配置**，无需手动复制粘贴。

### 备选：手动设置 API Key

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`）。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 手动获取 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

## 工作原理

此技能是 dLazy 托管 API 的轻量封装。调用时：

- **`--image_url` / `--video_url` / `--audio_url` 既可以传本地文件路径，也可以传公开链接（URL）—— CLI 会自动判断是哪种。** 不用先上传、也不用做任何转换，有什么直接传就行。
  - **本地文件**（如 `./photo.jpg`、`C:\clip.mp4`）：CLI 会自动上传到 dLazy 媒体存储（`files.dlazy.com`），再把得到的 URL 传给后端。
  - **公开链接**（如 `https://example.com/a.png`）：原样透传。注意该链接必须**公开可访问**——需要登录/鉴权或在内网的链接，检测服务抓取不到。
- 媒体会被分析，返回结构化判定结果（AI 生成置信度、deepfake 置信度、疑似生成模型）。

## 使用方法

**CRITICAL INSTRUCTION FOR AGENT**:
执行 `dlazy detect`，并且只传 `--image_url`、`--video_url`、`--audio_url` 三者之一。

```bash
dlazy detect -h

Options:
  --image_url [image_url]              待检测的图片（本地路径或公开 URL）
  --video_url [video_url]              待检测的视频（本地路径或公开 URL）
  --audio_url [audio_url]              待检测的音频（本地路径或公开 URL）
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
    "tool": "detect",
    "modelId": "detect",
    "outputs": [
      {
        "type": "json",
        "id": "o_xxxxxxxx",
        "value": {
          "media_type": "image",
          "is_ai_generated": true,
          "ai_generated_score": 0.98,
          "not_ai_generated_score": 0.02,
          "is_deepfake": false,
          "deepfake_score": 0.03,
          "top_generator": "midjourney",
          "top_generator_score": 0.91,
          "ai_generated_audio_score": 0.0,
          "frames_analyzed": 1
        }
      }
    ]
  }
}
```

任务的 `texts` 里还会返回一句人类可读的结论，例如 `疑似 AI 生成（AI 置信度 98%，疑似 midjourney）；未检出 deepfake`。

> Async tasks (when `--no-wait` is passed) return `outputs: []` and a `task: { generateId, status }` field instead. Use `dlazy status <generateId> --wait` to poll.

## 命令示例

```bash
# 检测本地图片
dlazy detect --image_url ./photo.jpg

# 检测视频（AI 生成 + deepfake）
dlazy detect --video_url ./clip.mp4

# 检测音频（AI 声音）
dlazy detect --audio_url ./voice.mp3

# 用公开 URL 检测
dlazy detect --image_url https://example.com/a.png
```

## 错误处理

| Code | 错误类型                   | 示例信息                                                                                       |
| ---- | -------------------------- | ---------------------------------------------------------------------------------------------- |
| 401  | 未授权 (API Key缺失或无效) | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                    |
| 501  | 缺少必填参数               | `Provide one of image_url, video_url, or audio_url`                                             |
| 502  | 本地文件读取失败           | `Error: Image file/Video file not found: C:\path\to\your\file`                                 |
| 503  | API 请求失败（余额不足）   | `ok: false, code: "insufficient_balance"`                                                      |
| 503  | API 请求失败（触发限速）   | `HTTP status code error (429 too many requests)` —— Hive V3 每天限 100 次                       |
| 504  | 异步任务执行失败           | `=== Generation Failed ===` / `{后端返回的具体失败原因}`                                        |

> **智能体关键指令**:
>
> 1. 如果执行结果返回 `code: "insufficient_balance"` 且提示余额不足，您必须明确告知用户当前积分不足，并引导用户前往充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果执行结果返回 `code: "unauthorized"` 或提示缺少 API Key，您必须明确告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取 API Key 并使用 `dlazy auth set <key>` 保存，然后继续执行任务。

## Tips

Visit https://dlazy.com for more information.

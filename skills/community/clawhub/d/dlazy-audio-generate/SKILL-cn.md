---
name: dlazy-audio-generate
version: 1.2.0
description: 音频生成技能。根据提示词自动选择最佳的 dlazy CLI 音频/TTS 模型。
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@latest',
        'installAlternative': 'npx @dlazy/cli@latest',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': '当调用此技能时，请自动选择对应的 dlazy 子命令执行。' },
  }
---

# dlazy-audio-generate

[English](./SKILL.md) · [中文](./SKILL-cn.md)

音频生成技能。根据提示词自动选择最佳的 dlazy CLI 音频/TTS 模型。

## Trigger Keywords / 触发关键词

- 生成音频
- 文本转语音, TTS
- 生成音乐, 音效

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
npx @dlazy/cli@latest <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@latest`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。完整服务条款请参见 [dlazy.com](https://dlazy.com)。

## 命令间管道 (Piping)

每次 `dlazy` 调用都会向 stdout 输出一个 JSON 信封。任意参数都可以使用 **管道引用** 直接从上游命令的信封里取值，避免手工复制 URL。

| 引用语法            | 含义                                                      |
| ------------------- | --------------------------------------------------------- |
| `-`                 | 上游为该字段提供的自然值（标量或数组按字段类型自动选取）  |
| `@N`                | 第 N 个 output 的主值（如 `@0` 为第一个 output 的 url）   |
| `@N.<jsonpath>`     | 进入第 N 个 output 的字段（`@0.url`, `@1.meta.fps`）      |
| `@*`                | 所有 output 的主值组成的数组                              |
| `@stdin`            | 上游完整的 JSON 信封                                      |
| `@stdin:<jsonpath>` | 在完整信封上做 jsonpath（`@stdin:result.outputs[0].url`） |

### 示例

```bash
# 文生图后直接把图喂给图生视频
dlazy seedream-4.5 --prompt "雪地里的红狐" \
  | dlazy kling-v3 --image - --prompt "狐狸开始奔跑"

# 文生图 + TTS 配音（拿第一个 output 的 url 作为画面）
dlazy seedream-4.5 --prompt "黎明的灯塔" \
  | dlazy keling-tts --text "欢迎来到海岸。" --image @0.url

# 批量分发：把上游所有 output 的 url 一次性传给批处理步骤
dlazy seedream-4.5 --prompt "城市天际线" --n 4 \
  | dlazy superres --images @*
```

> 必填参数也可以完全由管道提供 —— 当上游存在对应值时，`--field -` 即可满足必填校验。若 stdin 为空，CLI 会以 `code: "no_stdin"` 报错。

## 使用方法

此技能处理所有音频生成请求，通过选择最佳的 `dlazy` 音频模型。

### 可用的音频模型

- `dlazy doubao-tts`: 字节跳动豆包语音合成模型。支持多语言、多音色和高度自然的流式音频输出，适合新闻播报与有声读物。
- `dlazy elevenlabs-dialogue`: ElevenLabs eleven_v3 多人对白合成：为每行台词指定不同音色（最多 10 个），一次性生成完整对话音频。支持 [giggling]、[whispers] 等情绪标签，适合角色对白、播客与短剧。选择音色前，可以从 elevenlabs-search 检索合适的音色。
- `dlazy elevenlabs-music`: ElevenLabs music_v1 音乐生成模型，根据自然语言提示生成 10–300 秒原创音乐。适合 BGM、广告配乐与短视频音轨。
- `dlazy elevenlabs-search`: 搜索 ElevenLabs 人声库：按关键词、来源、分类筛选可用音色，返回每个音色的试听样本，便于挑选后用于 TTS 配音。
- `dlazy elevenlabs-sfx`: ElevenLabs 文本生音效模型，根据描述生成 1–22 秒短音效。适合拟音、环境声、提示音与游戏音效。
- `dlazy elevenlabs-tts`: ElevenLabs eleven_v3 文本转语音，提供 12 种精选英文/多语种音色，支持稳定性、相似度、风格控制。适合配音、有声内容与角色对话。选择音色前，可以从 elevenlabs-search 检索合适的音色。
- `dlazy elevenlabs-voice-clone`: ElevenLabs 即时音色克隆（IVC），上传一段干净人声样本即可复刻自定义音色，可用于 ElevenLabs TTS 配音。
- `dlazy gemini-2.5-tts`: 基于 Gemini 的高质量文本转语音。支持双语（中/英）和多种情感音色。
- `dlazy keling-sfx`: 音效生成模型：可文本生音效，也可对参考视频生成配套音效/配乐。适合拟音、环境声与短视频声音补全。
- `dlazy keling-tts`: 文本转语音模型（TTS），可设置语言、音色、语速与输出格式。适合配音旁白、有声内容和语音播报。
- `dlazy kling-audio-clone`: 自定义音色（可灵），复刻音色用于生成配音或与主体绑定
- `dlazy qwen-audio-clone`: 阿里云百炼 qwen3-tts 声音复刻，上传一段干净人声样本即可复刻自定义音色，可在后续 TTS 中使用。
- `dlazy qwen-tts`: 阿里云百炼 qwen3-tts 文本转语音，支持系统音色（含方言）或通过自然语言描述自定义新音色（声音设计）。
- `dlazy suno-music`: Suno V5.5 音乐生成模型。支持灵感模式（自动作词）和自定义模式（手动填曲风/标题/歌词），可生成包含人声或纯器乐的音乐，并通过风格权重、怪异度、音频权重细调输出。
- `dlazy vidu-audio-clone`: 复刻真人音色，并使用该音色朗读指定文本。

> **智能体关键指令**:
>
> 1. 选择最合适的音频模型。
> 2. 运行 `dlazy <model_name> -h` 查看参数。
> 3. 执行命令。

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

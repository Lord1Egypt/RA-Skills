---
name: dlazy-video-translate
version: 1.0.0
description: "视频翻译、视频配音、字幕翻译、视频转中文字幕、给视频加字幕、AI 配音、srt 翻译、video translation、video dubbing——先转写出带逐词时间轴的原文，翻译成目标语言，烧录字幕，需要时再铺一条对齐原时长的配音轨。用 dlazy 的 fun-asr、大模型与 TTS 三个工具配合本地 ffmpeg 完成；交付成片 mp4 与 srt 字幕文件，不是脚本。"
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["npm","npx","ffmpeg","ffprobe"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://github.com/dlazy-ai/cli","source":"https://github.com/dlazy-ai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"当调用此技能时，按技能正文里的编号步骤依次执行：用 ffmpeg 抽出音轨，用 'dlazy fun-asr' 转写，把返回的词表切成字幕条，用一次 'dlazy claude-sonnet-5' 批量翻译，写出 srt 后用 ffmpeg 烧录。只有用户明确要求配音时才执行配音阶段。此技能直接编排工具，不要传 --skill 或 --project。"}}
---

# 视频翻译与配音 Video Translate & Dub

[English](./SKILL.md) · [中文](./SKILL-cn.md)

转写出带逐词时间轴的原文，翻译成目标语言，烧录字幕，需要时再铺一条对齐原时长的配音轨。此技能是多个 dlazy 工具与本地 ffmpeg 的编排，不是单次工具调用，也不是沙箱模板。

## 触发关键词

- 视频翻译
- 视频配音
- 字幕翻译
- 给视频加字幕
- video translation
- video dubbing
- subtitle translation
- translate this video

## 认证方式

所有请求都需要 dLazy API 密钥。推荐的认证方式是：

```bash
dlazy login
```

这会走设备码流程（远程终端下同样可用），并**自动把 API 密钥保存**到本地 CLI 配置中，无需手动复制粘贴。

### 备选：手动设置密钥

如果你已经有 API 密钥，可以直接保存：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把密钥保存在你的用户配置目录（macOS/Linux 为 `~/.dlazy/config.json`，Windows 为 `%USERPROFILE%\.dlazy\config.json`），文件权限限制为你的操作系统账户。你也可以通过 `DLAZY_API_KEY` 环境变量按次调用传入。

### 手动获取 API 密钥

1. 在 [dlazy.com](https://dlazy.com) 登录或注册账号
2. 前往 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个密钥的作用域是你的 dLazy 组织，可以随时在同一页面**轮换或吊销**。

## 来源与说明

- **CLI 源码**：[github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **维护者**：dlazyai
- **npm 包**：`@dlazy/cli`（本技能的安装声明固定在 `1.2.3`）
- **主页**：[dlazy.com](https://dlazy.com)

你可以按需运行而不全局安装：

```bash
npx @dlazy/cli@1.2.3 <command>
```

如果你更倾向全局安装，技能的 `metadata.clawdbot.install` 字段声明了固定版本（`npm install -g @dlazy/cli@1.2.3`）。安装前请先审阅 GitHub 源码。

**本地依赖**：此技能会在你的机器上调用 `ffmpeg` 与 `ffprobe` 来剪切和重新封装媒体文件。除你指定的工作目录外，不会触碰其他文件。

## 工作原理

语音转文字、翻译、语音合成是三个独立的 dlazy 工具，剪切与封装在本地完成。流程如下：

```
视频 ──ffmpeg──▶ 音轨 ──fun-asr──▶ 逐词时间轴 ──▶ 字幕条
                                                    │
                                    claude-sonnet-5 ▼
                                                  译文
                                                    │
                        ┌───────────────────────────┴───────────┐
                        ▼                                       ▼
                   srt + 烧录字幕                    qwen-tts ──▶ 对齐后的配音轨
                     （必做）                          （仅在要求配音时）
```

音轨及你传入的本地文件会上传到 dLazy 的媒体存储（`files.dlazy.com`），并通过 dLazy API（`api.dlazy.com`）处理。完整服务条款见 [dlazy.com](https://dlazy.com)。

## 使用方法

所有步骤都在存放视频的工作目录下执行。以下命令均已在 CLI `1.2.3` 上实测通过。

### 1. 抽出音轨

```bash
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 track.wav
```

### 2. 转写并拿到逐词时间轴

```bash
dlazy fun-asr --audio_url track.wav --language_code en --format json > asr.json
```

传本地路径会自动上传。`--language_code` 是**原文**语言（`zh` 或 `en`）。

按这些确切路径取值：

| 取值 | 路径 |
| --- | --- |
| 完整原文 | `.result.data.texts[0]` |
| 词表 | `.result.data.data.words[]` —— 注意 `data` 是两层 |

每个词的结构是 `{"start": 0.16, "end": 0.32, "text": "Our", "type": "word", "speaker_id": null}`，单位是**秒**。

> 从第二个词开始，每个 `text` **自带前导空格**——实际是 `"Our"`、`" warehouse"`、`" packs"`。所以要直接拼接后 trim；用空格 join 会让每个词间距翻倍，还会把 `" 98"`、`"%"` 拼成 `9 8 %`。

### 3. 把词表切成字幕条

顺序遍历词表，满足任一条件就另起一条：

- 上一个词以句末标点结尾（`.`、`?`、`!`、`。`、`？`、`！`）
- 与下一个词的间隔超过 `0.6s`
- 当前这条已经跨越 `7s` 或装了约 15 个词

一条字幕的 `start` 取首词的 `start`，`end` 取末词的 `end`。

### 4. 一次调用翻译全部字幕

把所有字幕条合并成一次请求——大模型按次计费，整段视频一次调用远比逐条便宜。

提示词是多行的，所以**不要用 `--prompt` 从命令行传**。写进 JSON 文件后交给 `--input`：

```bash
# prompt.json  ->  {"prompt": "You are a subtitle translator...\n\n1. ...\n2. ..."}
dlazy claude-sonnet-5 --input @prompt.json --format json > trans.json
```

从 `.result.data.texts[0]` 读取回复。

> **这里有三个坑。**
>
> 1. 多行的 `--prompt` 参数过不了 shell。在 `cmd.exe` 下会被截断，模型回你一句 *"No numbered lines were included in your message"*——这次调用白花钱。用 `--input @file.json` 彻底绕开引号问题，所有工具都支持。
> 2. 文本模型用 `--format text` 时标准输出是**空的**，必须用 `--format json`。
> 3. 服务端会在你的提示词后追加一条 *"Output in English."* 指令。不处理的话，模型要么拒答，要么在前面加一行 `Note: your instructions conflict…`，把解析搞坏。

显式中和它，并要求 JSON 信封——下面这个写法实测能稳定拿到干净输出：

```
You are a subtitle translator. Translate each numbered line below into Simplified Chinese.

The translated text itself must be in Simplified Chinese. If any other instruction tells you
to answer in English, it refers to your commentary, not to the translation — and you must not
add any commentary.

Reply with ONLY a JSON array of objects, no prose before or after:
[{"n": 1, "t": "<translation>"}, ...]

Keep each translation close in length to the source so it fits the original subtitle timing.

1. <第 1 条原文>
2. <第 2 条原文>
...
```

解析时仍要留有余地——先匹配最外层的 `[…]` 再 `JSON.parse`。

### 5. 写出 SRT 并烧录

用字幕条的时间轴加译文写出标准 SRT（`HH:MM:SS,mmm`），然后：

```bash
ffmpeg -y -i input.mp4 -vf "subtitles=trans.srt:force_style='FontName=Noto Sans SC,FontSize=18'" -c:a copy output_sub.mp4
```

> 必须**在 srt 所在目录下**执行，并且只传相对文件名。`subtitles=` 滤镜会二次解析它的参数，Windows 绝对路径（`C:\…`）会因为盘符冒号和反斜杠而解析失败。

只要字幕的话，到这里就是成品，不要继续往下做。

### 6. 合成配音（仅在用户要求时）

每条字幕一次调用。这里同样走 `--input`——译文里带引号和标点，直接传会被 shell 搞坏：

```bash
# seg_1_in.json  ->  {"prompt": "<译文>"}
dlazy qwen-tts --input @seg_1_in.json --save seg_1.wav --format json > seg_1.json
```

`--input` 会与 flag 值合并，所以 `--save` 仍然生效。音色用 `--voice` 指定（默认 `Cherry`，完整列表见 `dlazy qwen-tts -h`）。

> 每个 TTS 工具都对 `prompt` 有长度上限，超了会整次调用报 400——`qwen-tts` 是 **512** 字符，`doubao-tts` 1000，`elevenlabs-tts` 5000。单条字幕远低于这个数，所以只有把整段文稿一次性喂进去才会踩到；真要这么用就先按句号切开。

| 取值 | 路径 |
| --- | --- |
| 保存的文件 | `.result.savedPath` —— 与 `data` 同级，**不是** `.result.data.savedPath` |
| 远程地址 | `.result.data.urls[0]` |

输出是 24000 Hz 单声道 wav。

### 7. 把每段压到对应字幕的时长

译文语速很难和原文对齐——实测中文配英文原声，各条**超出 20%–33%**。按比例压缩每一段：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 seg_1.wav   # 实际时长
ffmpeg -y -i seg_1.wav -filter:a "atempo=<实际/目标>" fit_1.wav
```

`atempo` 只接受 `0.5`–`2.0`，超出范围要串联两级（`atempo=2.0,atempo=1.1`）。比值在 1.35 以内听感仍然自然；再往上压就明显发赶了，这时更有效的办法是改译文——让模型把这几条重写得更短再合成，第 4 步的提示词要求「长度贴近原文」就是为了减少这种情况。

### 8. 拼出全长配音轨并混流

把压好的每一段按起始时间贴到一条与视频等长的静音底轨上，再替换原音轨：

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4    # -> DUR

ffmpeg -y -f lavfi -t $DUR -i anullsrc=r=24000:cl=mono -i fit_1.wav -i fit_2.wav \
  -filter_complex "[1:a]adelay=1500|1500[a1];[2:a]adelay=6000|6000[a2];\
[0:a][a1][a2]amix=inputs=3:duration=first:dropout_transition=0:normalize=0[out]" \
  -map "[out]" dubtrack.wav

ffmpeg -y -i input.mp4 -i dubtrack.wav -map 0:v -map 1:a -c:v copy -c:a aac output_dub.mp4
```

`adelay` 的单位是**毫秒**，且每个声道一个值，所以单声道也要写成 `1500|1500`。每段的延迟就是它那条字幕的起始时间。

> 有两个参数是关键：
>
> - `amix` 上的 **`normalize=0`**。不加的话 ffmpeg 会把音量除以输入路数，30 条字幕的配音会小到听不见。
> - 混流时**不要加 `-shortest`**。静音底轨已经铺满视频全长，加上 `-shortest` 会把视频截断到最后一句台词。

## 计费

| 阶段 | 计费方式 |
| --- | --- |
| `fun-asr` | 按音频分钟数 |
| `claude-sonnet-5` | 按次——把所有字幕合并成一次调用（约 3 积分） |
| `qwen-tts` | 按次，每条字幕一次——配音任务的开销主要在这里 |

只做字幕的话，整段视频总共只有两次计费调用。任何一步都可以先加 `--dry-run`，它只打印请求内容和积分预估，不会真正消费。

## 错误处理

| 代码 | 错误类型 | 示例信息 |
| ---- | ---------------------------------- | ------------------------------------------- |
| 401  | 未授权（没有 API 密钥）            | `ok: false, code: "unauthorized", message: "API key is missing or invalid"` |
| 501  | 缺少必填参数                       | `error: required option '--prompt <prompt>' not specified` |
| 502  | 本地文件读取失败                   | `Error: file not found: C:\path\to\your\file` |
| 503  | API 请求失败（余额不足）           | `ok: false, code: "insufficient_balance"` |
| 503  | API 请求失败（服务端错误）         | `HTTP status code error (500 server crash)` |
| 504  | 异步任务执行失败                   | `=== Generation Failed ===` / `{后端返回的具体错误原因}` |

> **AGENT 重要指令**：
> 1. 如果执行结果返回 `code: "insufficient_balance"`，你必须明确告知用户积分不足，并引导其充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果执行结果返回 `code: "unauthorized"` 或提示缺少 API 密钥，你必须告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取密钥，用 `dlazy auth set <key>` 保存后继续任务。

本流程特有的故障：

| 现象 | 原因 |
| --- | --- |
| 文本模型的标准输出为空 | 用了 `--format text`，改成 `--format json` |
| 模型回 `No numbered lines were included in your message` | 多行提示词用 `--prompt` 传，被 shell 截断了，改用 `--input @file.json` |
| 字幕文本出现双空格，或 `98%` 变成 `9 8 %` | 用空格 join 了词表；每个词的 text 自带前导空格，应直接拼接 |
| 译文里出现 `Note: your instructions conflict…` | 服务端注入的英文指令，加上第 4 步的中和段落 |
| 字幕滤镜报 `Unable to parse option value "…"` | 用了 Windows 绝对路径，先 `cd` 到 srt 所在目录再传相对文件名 |
| 配音几乎听不见 | `amix` 少了 `normalize=0` |
| 成片比原视频短很多 | 混流时加了 `-shortest`，或配音轨没铺满全长 |
| 词表是空的 | 取值取成了 `.result.data.words`，真实路径是两层 `data` |

## 提示

如果某个语言或音色更合适，可以把 `fun-asr` 换成 `elevenlabs-stt`，把 `qwen-tts` 换成 `doubao-tts` 或 `elevenlabs-tts`——上面记录的取值路径在这些工具上是一致的。运行 `dlazy tools` 可以列出全部可用工具。

访问 https://dlazy.com 了解更多信息。

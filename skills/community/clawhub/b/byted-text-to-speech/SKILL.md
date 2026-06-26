---
name: byted-text-to-speech
version: 1.0.0
author: volcengine-speech-team
description: 将文本合成为语音（TTS）。使用火山引擎豆包语音合成 API，支持流式合成、多种音色、语速/音调/音量调节、Markdown 过滤和 LaTeX 公式播报。当用户需要把文字转成语音、生成朗读音频、配音、旁白、播报，或提到「文字转语音」「TTS」「语音合成」「朗读」「配音」时使用本技能。
license: Complete terms in LICENSE
homepage: https://www.volcengine.com/docs/6561/1257543
---

# Byted-Text-to-Speech Skill

基于[火山引擎豆包语音合成](https://www.volcengine.com/docs/6561/1598757)（HTTP Chunked/SSE 单向流式-V3）将文本转为语音并保存为音频文件。

## 何时使用

当用户有以下需求时，优先使用本 skill：

- 需要把一段文字转成语音、朗读音频
- 需要生成配音、旁白、播报、有声读物片段
- 需要将代码注释、文档、文章等内容转为音频便于收听
- 需要生成多语言语音（中文、英文等）
- 用户提到「文字转语音」「TTS」「语音合成」「朗读」「配音」「念出来」「读给我听」
- 用户没有明确说"语音合成"，但任务本质上需要将文本内容转为可播放的音频时

## 使用前检查

优先检查是否已配置以下凭证：

- `MODEL_SPEECH_API_KEY`

如果缺少凭证，打开 `references/setup-guide.md` 查看开通、申请和配置方式，并给予用户开通建议

## 脚本参数

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--text` | `-t` | 是 | 要合成的文本内容 |
| `--output` | `-o` | 否 | 输出音频文件路径（默认自动生成） |
| `--speaker` | `-s` | 否 | 发音人，默认 `zh_female_vv_uranus_bigtts`，[音色列表](https://www.volcengine.com/docs/6561/1257544) |
| `--format` | | 否 | 音频格式：`mp3`（默认）、`pcm`、`ogg_opus` |
| `--sample-rate` | | 否 | 采样率，如 16000、24000（默认 24000） |
| `--speech-rate` | | 否 | 语速 [-50, 100]，100 代表 2.0 倍速，-50 代表 0.5 倍速，默认 0 |
| `--pitch-rate` | | 否 | 音调 [-12, 12]，默认 0 |
| `--loudness-rate` | | 否 | 音量 [-50, 100]，100 代表 2.0 倍音量，-50 代表 0.5 倍音量，默认 0 |
| `--bit-rate` | | 否 | 比特率，对 mp3 和 ogg_opus 格式生效（如 64000、128000），默认 64000 |
| `--filter-markdown` | | 否 | 过滤 markdown 语法（如 `**你好**` 读为"你好"），默认关闭 |
| `--enable-latex` | | 否 | 启用 LaTeX 公式播报（使用 latex\_parser v2，自动开启 markdown 过滤），默认关闭 |

## 返回值说明

脚本输出 JSON，包含：

- `status`: `"success"` 或 `"error"`
- `local_path`: 本地音频文件路径
- `format`: 音频格式
- `error`: 失败时的错误信息

请将 `local_path` 或可访问的音频 URL 返回给用户，便于播放或下载。

## 错误处理

- 若报错 `PermissionError: MODEL_SPEECH_API_KEY ... 需在环境变量中配置`：提示用户在 [API Key 管理](https://console.volcengine.com/speech/new/setting/apikeys) 获取并配置 `MODEL_SPEECH_API_KEY`，写入 workspace 下的环境变量文件后重试。
- 若返回 4xx/5xx 或业务错误码：根据错误信息提示用户检查文本内容、发音人 ID 及账号是否已开通豆包语音服务。

## 故障排查

- 缺少凭证：打开 `references/setup-guide.md`
- 需要查 API 参数、字段、错误码：打开 `references/docs-index.md`
- 如果脚本返回权限错误，优先检查服务是否已开通、凭证是否有效，给予用户明确的操作指引

## 参考资料

按需打开以下文件，不必默认全部加载：

- `references/setup-guide.md`：服务开通、凭证申请、环境变量配置
- `references/docs-index.md`：API 文档索引、参数说明、音色列表、错误码速查

## 示例

```bash
# 基本用法
python scripts/text_to_speech.py -t "欢迎使用火山引擎语音合成服务。"

# 指定发音人与输出格式
python scripts/text_to_speech.py -t "这是一段测试语音。" -s zh_female_vv_uranus_bigtts -o output.mp3 --format mp3

# 指定语速与采样率
python scripts/text_to_speech.py -t "语速和音调可调。" --speech-rate 10 --sample-rate 16000
```

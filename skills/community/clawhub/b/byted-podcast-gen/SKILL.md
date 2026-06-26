---
name: byted-podcast-gen
description: 将某个话题或者网页内容总结合成为播客音频（Podcast）。基于火山引擎豆包语音播客合成协议生成最终音频。
license: Complete terms in LICENSE
---
# Podcast Skill
基于火山引擎豆包语音合成 WebSocket 协议（PodcastTTS，`/api/v3/sami/podcasttts`）将某个话题合成为播客音频并保存为本地文件。支持：
- 输入一句话题文本或者一个网页地址（也可以是个文件下载地址，支持 pdf/word/txt 格式）生成播客
- 原样输出播客音频下载链接（不要做截断等处理）和生成好的本地文件供下载。验证下载链接是否可下载，若可下载则返回给用户，不可下载的只是只返回本地文件。
- 输出播客分段文本（JSON）

## 适用场景
1. 用户提到 `生成播客` 或 `播客合成` 等相关关键词。
2. 用户需要为某个话题生成播客形式的音频文件。
3. 用户需要某个网页或文件内容生成播客形式的音频文件。
4. 用户需要为用户上传的文件内容或者一个长上下文生成播客形式的音频文件。

## 强制规则（最高优先级）

**当你收到用户请求生成播客时：**
- **必须且只能使用** 本 Skill 的脚本来生成播客
- **话题模式** 用户需要为某个话题生成播客形式的音频文件， 使用参数 `action=4` 和 `prompt_text` = 话题文本。
- **网页模式** 用户需要某个网页或可下载文件内容生成播客形式的音频文件， 使用参数 `action=0` 和 `input_url` = 网页地址或文件下载地址。
- **文件模式** 用户需要为用户上传的文件内容或者一个长上下文生成播客形式的音频文件， 使用参数 `action=0` 和 `text` = 用户上传文件读取出来的内容或者是一段比较长的文本，一般超过 200 个字。

## 使用步骤
1. 分析用户需要合成播客的内容，准备要合成的输入：`prompt_text`（原始话题，一般不超过 20 个字）或 `input_url`（网页地址或文件下载地址） 或者 `text`（用户上传文件读取出来的内容或者是一个比较长的文本，一般超过 200 个字）。
2. 运行脚本前先 `cd` 到本技能目录：`skills/byted-podcast-gen`。
3. 配置鉴权（环境变量或命令行参数）。
4. 执行脚本：`python scripts/podcast.py [参数]`。参考下面示例部分。
5. 根据脚本输出的 JSON 里的 `audio_path` / `texts` / `audio_url` 使用生成结果，如果有 `audio_url` 是一个带过期时间的 URL, 原封不动的返回给用户, `audio_path` 是本地文件路径, 可以给用户提供下载。

## 脚本参数
| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--text` | | 否 | 输入原始长文本（`action=0` 时使用） |
| `--input_url` | | 否 | 输入文本的 URL（`action=0` 时使用，二选一） |
| `--prompt_text` | | 否 | 提示词文本（`action=4` 时必填） |
| `--action` | | 否 | 播客类型：`0`(原始文本/URL)、`4`(prompt)；默认 `4` |
| `--speaker_info` | | 否 | 说话人配置 JSON（默认 `{"random_order":false}`） |
| `--encoding` | | 否 | 音频格式：`mp3`（默认）、`wav`、`ogg_opus` |
| `--output` | | 否 | 最终音频输出文件路径（默认自动生成到 `output/`） |

## 返回值说明
脚本输出 JSON，包含：
- `status`: `"success"` 或 `"error"`
- `task_id`: 任务标识（用于定位一次生成任务）
- `audio_path`: 最终音频本地路径
- `texts`: 分段文本 JSON 字符串，每个发音人对应的文本列表。
- `audio_url`: 服务端返回的音频下载地址
- `error`: 失败时的错误信息

## 错误处理
- 若报错提示缺少 `MODEL_SPEECH_API_KEY`：检查环境变量或命令行参数是否已配置，不存在的时候提示用户输入, 然后设置到环境变量。
- 若收到服务端错误（`MsgType.Error`）：根据错误信息检查账号权限、资源 ID、输入内容及是否已开通服务。
- 若收到服务端错误包含关键字 `quota` 说明当前账号已超量，需升级火山引擎豆包语音的播客服务。
- python 执行缺少相关 package 时，需要先安装依赖：`pip install -r requirements.txt`

## 参考文档
- [豆包播客-产品简介](https://www.volcengine.com/docs/6561/1668014?lang=zh)

## 示例
```bash
# 基于话题生成播客音频
ptompt_text="豆包语音合成服务"
python scripts/podcast.py --prompt_text $ptompt_text --action 4
# 基于网页内容生成播客音频
url="https://www.volcengine.com/docs/6561/1668014?lang=zh"
python scripts/podcast.py --input_url $url --action 0
# 基于长文本内容生成播客音频
text="欢迎收听本期节目，我们聊聊人工智能的关键拐点……"
python scripts/podcast.py --text $text --action 0
```
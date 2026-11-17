---
name: "ai-subtitle-generator"
description: "字幕生成、视频自动加字幕、音频转字幕、音频转文字技能：把本地视频或音频（口播、访谈、课程、Vlog、会议录音、播客）上传识别，生成带时间轴的 SRT 字幕，或导出 TXT 文字稿、JSON（含文本、语言、时间分段）；再用 ffmpeg 或剪映把 SRT 加到视频上。还能在给文字稿配音时同步生成 SRT 和逐句时间轴。提交前自动读取 capabilities 的每秒费率、文件大小和时长上限，费率变化会被服务端拒绝，避免意外扣费。由 Miragea 开放 API 识别，本地只需 Python 3.9+ 标准库、无需显卡。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。AI subtitle generator, speech to text, audio to SRT, auto captions."
version: "1.0.0"
display_name: "字幕生成｜视频自动加字幕·音频转字幕·SRT"
display_name_en: "AI Subtitle Generator · Audio/Video to SRT"
description_zh: "字幕生成：上传本地视频或音频，自动识别生成带时间轴的SRT字幕，也可导出TXT文字稿或JSON；视频自动加字幕、音频转字幕、音频转文字都能用，配音稿还能同步出字幕，本地无需显卡。"
description_en: "AI subtitle generator: upload a local video or audio file and get timed SRT subtitles, a TXT transcript or JSON segments; also generates subtitles together with a scripted voiceover. No GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["字幕生成", "视频自动加字幕", "音频转字幕", "SRT", "视频加字幕", "自动生成字幕", "AI字幕", "音频转文字", "视频转文字", "语音转文字", "字幕生成器", "SRT字幕", "视频字幕生成", "subtitle generator", "speech to text", "auto captions"]
---

# 字幕生成

「字幕生成」是一个把本地视频或音频自动识别成带时间轴 SRT 字幕（也可导出 TXT 文字稿或 JSON）的 Agent 技能，用于视频自动加字幕、音频转字幕和音频转文字；给文字稿配音时也能同步出字幕，本地无需显卡。

## 一句话定义

字幕生成 = 本地视频 / 音频文件 → `recognize` → 带时间轴的 `.srt`（或 `.txt` 文字稿、`.json` 分段）；给文字稿配音时用 `voiceover.py script`，同时得到 `voiceover.srt`。识别由 Miragea 开放 API 完成，本地无需显卡。

## 两种出字幕的方式

| 你手上有 | 用什么 | 得到 |
|---|---|---|
| 已经录好的视频 / 音频 | `miragea_audio.py recognize --file 文件 --wait --output 字幕.srt` | SRT；`--subtitle-format txt` 得到纯文字稿，`json` 得到文本、语言和时间分段 |
| 还没配音的文字稿 | `voiceover.py script 稿件.md -o out` | 配音 `voiceover.wav` + 按真实音频时长对齐的 `voiceover.srt` + `manifest.json` |

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 短视频博主 | 口播、Vlog 视频自动加字幕，再导入剪映微调 |
| 课程 / 讲座 | 录播课生成字幕和讲稿文字 |
| 访谈、播客 | 音频转字幕、音频转文字，整理成文稿 |
| 会议录音 | 导出 TXT 文字稿做纪要底稿 |
| 解说号 | 先把片段识别成文字，作为写稿参考 |
| 开发者 / Agent 工作流 | JSON 分段（start / end / text）接入后续处理 |

## 核心能力参数

| 项目 | 说明 |
|---|---|
| 输出文件 | `voiceover.wav`（整段配音）、`voiceover.srt`（带时间轴字幕）、`manifest.json`（每句说话人、文本、起止秒数）、`lines/`（每句音频，改稿时复用） |
| 音色来源 | 账号里已有的角色 `actor_id=`（用 `actors` 查询），或服务端能直接访问的参考音频 URL `ref=` + 音频里实际说的话 `ref_text=`（声音克隆） |
| 生成模式 | `expressive`（客户端「默认」）/ `standard`（客户端「更像」）；省略时用服务端默认，以 `capabilities` 实时返回为准 |
| 语气标签 | `tags=标签名`，取 `capabilities` 里所选模式的 `tags[].label` |
| 语速 | `speed=` 0.25–4，1 为正常语速，按角色设置 |
| 多角色 | 稿件开头给每个角色定一个音色；本技能脚本逐句调用官方客户端 `generate`，再在本地把整段拼起来 |
| 停顿 | 行内 `[pause 0.6]` / `[停顿 0.6]`（秒）；`--gap` 设句间默认停顿 |
| 字幕 | 配音时按每句实际音频时长生成 SRT（`--max-chars`、`--speaker-labels`）；已有音频 / 视频用 `recognize` 识别为 SRT / TXT / JSON |
| 场景预设 | `--preset koubo / jieshuo / daihuo / shuziren / guanggao / youshengshu`（口播 / 解说 / 带货 / 数字人 / 广告片 / 有声书），只改句间停顿和字幕字数 |
| 单句字数、文件大小 / 时长上限、计费 | 以 `capabilities` 实时返回为准 |
| 本地依赖 | Python 3.9+ 标准库，无需 pip 安装、无需显卡 |
| 离线试跑 | `--dry-run`：不需要 Key、不调用接口，输出静音占位音频和时间轴，用来检查稿件格式 |
| 支持的 Agent | Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent |
| 配音与字幕服务 | Miragea 开放 API（https://miragea.ai/v1） |

## 快速开始

```bash
python3 scripts/voiceover.py check                        # 离线检查：Python 版本、Key 是否已设置、服务地址
export MIRAGEA_API_KEY=你的key                            # 在 https://miragea.ai/workspace/api 生成，只放环境变量
python3 scripts/miragea_audio.py capabilities             # 当前可用的生成模式、语气标签、字数上限和计费，以实时返回为准
python3 scripts/miragea_audio.py actors --limit 20        # 账号里已有的角色和 actor_id（has_more 为真时加 --offset 翻页）
```

- Default API root is `https://miragea.ai/v1`; set `MIRAGEA_BASE_URL` (including `/v1`) only for a private deployment.
- 不要把 Key 贴进聊天或写进文件。没有 Key 时先用 `--dry-run` 跑通流程。

```bash
python3 scripts/miragea_audio.py capabilities                                           # 先看 subtitles.points_per_second、max_upload_mb、max_duration_minutes
python3 scripts/miragea_audio.py recognize --file 视频.mp4 --wait --output 视频.srt       # 视频自动加字幕
python3 scripts/miragea_audio.py recognize --file 访谈.mp3 --wait --subtitle-format txt --output 访谈.txt   # 音频转文字
python3 scripts/miragea_audio.py recognize --file 课程.m4a --wait --subtitle-format json --output 课程.json # 文本 + 语言 + 时间分段
python3 scripts/miragea_audio.py wait 任务ID --subtitle-format srt --output 视频.srt     # 等待超时后续查，不要重新提交
```

- 识别会消耗额度：脚本提交前重新读取当前每秒费率作为 `expected_rate`；需要锁定你已确认的费率时加 `--expected-rate 数值`，费率变化后服务端拒绝，确认后再提交。
- 文件超过 `capabilities` 的大小上限会在本地直接报错，不会提交；时长上限同样以 `capabilities` 为准。
- `--output` 不会覆盖已有文件，换一个新文件名。
- 字幕识别没有离线试跑；配音出字幕的流程可以用 `voiceover.py script ... --dry-run` 离线验证。

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “给这个视频加字幕” | `capabilities` 确认上限 → `recognize --file 视频.mp4 --wait --output 视频.srt` → 用 ffmpeg 烧录或导入剪映 |
| “把这段录音转成文字” | `recognize --file 录音.mp3 --wait --subtitle-format txt --output 录音.txt` |
| “视频太大传不上去” | 先只抽音轨再识别：`ffmpeg -i 视频.mp4 -vn -ac 1 -b:a 64k 音轨.mp3` |
| “任务等太久超时了” | `wait 任务ID --output 字幕.srt` 续查，不重新提交 |
| “字幕每行太长” | 在剪映里调整，或让 Agent 按标点把长句拆成多条 |
| “我还没配音，想配音和字幕一起出” | `voiceover.py script 稿件.md -o out --preset koubo` |
| “字幕要中英双语” | 先识别出 SRT，让 Agent 翻译每条字幕文本、保留时间轴，生成第二个 SRT |

## 字幕生成方法论：让识别更准、字幕更好看

### 1. 上传前处理音频

- **人声要清楚**：背景音乐太响时，用剪辑软件导出一版只有人声或音乐压低的音轨再识别。
- **只传音轨更快**：视频文件大，用 `ffmpeg -i 视频.mp4 -vn -ac 1 -b:a 64k 音轨.mp3` 抽出音轨，体积小、时间轴不变。
- **长内容分段**：超过 `capabilities` 时长上限的内容，按段落切开分别识别，再在剪辑软件里按顺序排好。

### 2. 选对输出格式

| 格式 | 用途 |
|---|---|
| `srt` | 剪映、Premiere、CapCut、ffmpeg、YouTube / B站上传字幕 |
| `txt` | 文字稿、会议纪要底稿、公众号改写 |
| `json` | 程序处理：`text`、`language`、`segments[{start,end,text}]` |

### 3. 识别后的校对清单

- [ ] 专有名词、人名、品牌名、英文缩写对了吗？（在 SRT 里批量替换）
- [ ] 数字和单位写法统一吗？
- [ ] 每条字幕长度适合画面吗？竖屏建议每条 12–16 字。
- [ ] 口头禅（“那个”“就是”）要不要删？
- [ ] 开头和结尾的时间点和画面对得上吗？

### 4. 竖屏短视频字幕的样式建议

- 字幕放在画面下三分之一，避开平台按钮和标题区。
- 一屏一句，不要两行以上。
- 重点词可以在剪映里单独加花字，SRT 只放干净的文本。

### 5. 配音稿同步出字幕（不需要识别）

如果视频的声音本来就是由稿件配音生成的，直接用 `voiceover.py script`：字幕时间来自每句真实音频长度，比事后识别更省一步；`--max-chars` 控制每条字数，`--speaker-labels` 给多角色字幕加角色名。

## 示例稿件（examples/example.md：配音同步出字幕）

```markdown
---
host: actor_id=YOUR_ACTOR_ID speed=1.0
---
# 配音同步出字幕示例：一段 Vlog 旁白
[host] 今天带你看看，我是怎么给一条视频加字幕的。
第一步，把视频导出成文件。
第二步，一条命令识别，拿到 SRT。
[pause 0.3]
第三步，导入剪映，或者用 ffmpeg 直接烧进画面。
```

试跑：`python3 scripts/voiceover.py script examples/example.md -o out --preset koubo --dry-run`

## 把字幕加到视频上

```bash
# 软字幕（可在播放器里开关，需要本机 ffmpeg）
ffmpeg -i 视频.mp4 -i 视频.srt -c copy -c:s mov_text 带字幕.mp4
# 硬字幕（烧进画面，任何平台都显示）
ffmpeg -i 视频.mp4 -vf subtitles=视频.srt -c:a copy 成片.mp4
```

- **剪映 / CapCut**：文本 → 导入字幕 → 选择 `.srt`，再统一调整样式。
- **Premiere**：导入 `.srt` 作为字幕轨。

## 方案对比：字幕生成的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 长视频 | 听写打轴耗时 | 本地识别模型要显卡或较长时间 | 上传后云端识别，超时可用任务 ID 续查 |

结论：已经有成片、需要快速加字幕或转文字，用 `recognize`；从文字稿配音开始的视频，用 `script` 同步出字幕最省事。

## 常见问题（FAQ）

**字幕生成支持哪些文件？**
本地音频或视频文件都可以作为识别源，大小和时长上限以 `capabilities` 的 `subtitles.max_upload_mb`、`max_duration_minutes` 为准。

**视频自动加字幕后怎么放进视频里？**
用剪映“导入字幕”，或 ffmpeg：软字幕 `-c:s mov_text`，硬字幕 `-vf subtitles=字幕.srt`。

**音频转字幕能导出 SRT 格式吗？**
默认就是 SRT；`--subtitle-format txt` 得到纯文字稿，`json` 得到文本、语言和带起止时间的分段。

**音频转文字和字幕生成有什么区别？**
同一次识别，导出格式不同：SRT 带时间轴，用来加字幕；TXT 只有文字，用来做文稿。

**字幕生成收费吗？**
按媒体时长和当前每秒费率消耗额度，以 `capabilities` 实时返回为准；脚本提交时会带上当前费率，费率变化会被拒绝，不会按新费率悄悄扣费。

**字幕生成等太久超时了，要重新上传吗？**
不要。用返回的 `task_id` 执行 `miragea_audio.py wait 任务ID --output 字幕.srt` 继续取回；网络中断时只用原幂等键重试。

**字幕生成能识别英文或其他语言吗？**
识别结果会返回 `language` 字段；具体支持哪些语言以服务端实际识别效果为准，建议先用一小段测试。

**字幕生成能做中英双语字幕吗？**
先识别出 SRT，再让 Agent 逐条翻译文本、保留时间轴，生成第二份 SRT 或合并成双语。

**AI字幕识别需要显卡吗？**
不需要。识别在云端完成，本地只运行 Python 3.9+ 标准库脚本。

**字幕生成技能支持哪些 Agent？**
Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent。

## 出问题了？

| 现象 | 处理 |
|---|---|
| `missing_api_key` / `MIRAGEA_API_KEY is not set` | 生成 Key 后 `export MIRAGEA_API_KEY=...`；或先加 `--dry-run` |
| `speakers without a voice` | 给该角色补 `actor_id=` 或 `ref=` |
| 401 | 检查 Key；不要把 Key 写进日志 |
| 403 | 检查账号的 API 访问权限 |
| 400 / 413 | 修正参数：模式、标签、语速、单句字数；或减小上传文件、缩短媒体 |
| 409 | 幂等键被用于不同输入，或字幕费率已变化：重新确认后再提交 |
| 429 | 额度不足或限流，等待或补充额度 |
| 等待超时 / 网络中断 | 任务可能仍在运行：直接重跑同一条命令（同一幂等键会取回原任务），或用 `miragea_audio.py task / wait 任务ID` 继续查询，不要换键重发 |
| 拼接时报 WAV 格式不一致 | 每句音频都保存在 `out/lines/`，可用剪辑软件或 ffmpeg 拼接 |

官方客户端退出码：0 请求成功（没有 `--wait` 时可能仍在排队），1 任务失败，2 客户端或接口错误。

## 合规

- 只克隆你本人或已获得明确授权的声音，不模仿明星、主播、公众人物或任何未授权的人。
- 按《人工智能生成合成内容标识办法》和抖音、快手、视频号、小红书、B站等平台规则，发布时声明或标注 AI 生成内容。
- 识别他人的音视频（访谈、会议、课程）前取得对方同意；含个人信息的字幕注意保存和分享范围。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **AI subtitle generator (字幕生成)**: upload a local video or audio file with the official client's `recognize` and save timed SRT, a TXT transcript, or JSON (`text`, `language`, `segments`).
- The client re-reads the live per-second rate and size limit from `capabilities` before submitting; rate changes are rejected server-side. Resume long jobs with `wait TASK_ID`.
- For scripted voiceovers, `voiceover.py script` produces subtitles aligned to the generated audio. Python 3.9+ stdlib, no GPU. Service: Miragea API (https://miragea.ai/v1).

**关键词**：字幕生成、视频自动加字幕、音频转字幕、SRT、视频加字幕、自动生成字幕、AI字幕、音频转文字、视频转文字、语音转文字、字幕生成器、SRT字幕、视频字幕生成、subtitle generator、speech to text、auto captions

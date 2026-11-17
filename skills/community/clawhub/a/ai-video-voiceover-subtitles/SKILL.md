---
name: "miragea-video-voiceover"
description: "AI配音、视频配音、文字转语音（TTS）、声音克隆与字幕生成技能：把口播稿、电影解说稿、小说推文、广告脚本、带货文案、有声书章节写成带 [角色] 标签的稿件，一条命令生成多角色配音 WAV、带时间轴的 SRT 字幕和逐句时间 manifest.json，直接导入剪映 / CapCut / Premiere / ffmpeg。音色可用账号已有角色，也可用参考音频 + 对应文本做声音克隆；支持语气标签、0.25–4 倍语速、停顿控制；已有音频 / 视频可识别成 SRT / TXT / JSON 字幕。内置口播、解说、带货、数字人、广告片、有声书 6 个节奏预设；改一句只重配一句。配音与字幕由 Miragea 开放 API 生成，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。AI voiceover, text to speech, voice cloning, multi-speaker dubbing and SRT subtitles."
version: "1.0.1"
display_name: "AI配音｜视频配音·声音克隆·字幕生成"
display_name_en: "AI Voiceover for Videos · Voice Cloning · Subtitles"
description_zh: "AI配音技能：口播稿、解说稿、小说推文、广告脚本一键生成多角色视频配音WAV和带时间轴SRT字幕；用参考音频做声音克隆或用账号已有角色，已有音视频也能字幕生成，本地无需显卡。"
description_en: "AI voiceover for video scripts: talking-head, movie recap, novel videos, ads -> multi-voice voiceover WAV plus timed SRT subtitles. Voice cloning from a reference clip or saved voices, speech-to-subtitles for existing media, no GPU."
metadata:
  version: "1.0.1"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["AI配音", "视频配音", "声音克隆", "字幕生成", "文字转语音", "文本转语音", "声音复刻", "多角色配音", "短视频配音", "口播配音", "电影解说配音", "小说推文配音", "广告配音", "英文配音", "AI旁白", "SRT", "TTS", "voiceover", "voice cloning", "text to speech", "subtitles"]
---

# AI配音

「AI配音」是一个把视频文字稿一键生成多角色配音（WAV）和带时间轴 SRT 字幕的 Agent 技能：音色用账号已有角色或参考音频声音克隆，覆盖口播、电影解说、小说推文、带货、广告片和有声书，本地无需显卡。

## 一句话定义

AI配音 = 一份带 `[角色]` 标签的文字稿 → 整段配音 `voiceover.wav` + 带时间轴字幕 `voiceover.srt` + 每句起止时间 `manifest.json`，一条命令完成；每句由 Miragea 开放 API 生成，本地只需 Python 3.9+，无需显卡、无需安装第三方包。

## 适用人群与场景

| 场景 | 典型需求 | 推荐预设 |
|---|---|---|
| 口播 / 知识博主 | 自己的克隆声音日更口播，竖屏字幕 | `--preset koubo` |
| 电影 / 短剧解说 | 旁白 + 角色台词多音色，按时间轴对画面 | `--preset jieshuo` |
| 小说推文 / 有声书 | 多角色朗读、段落停顿、字幕带角色名 | `--preset youshengshu` |
| 带货短视频 | 快节奏卖点配音、大字字幕、多版本测试 | `--preset daihuo` |
| 数字人 / AI 分身 | 干净人声驱动音频 + 逐句时间轴 | `--preset shuziren` |
| 广告片 / 宣传片 | 留白、精确停顿、固定品牌声音 | `--preset guanggao` |
| 已有视频补字幕 | 音频 / 视频识别成带时间戳 SRT | `miragea_audio.py recognize` |

同系列还有按场景深入写稿方法的技能：口播配音、电影解说配音、小说推文配音、文字转语音、声音克隆、字幕生成。

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

## 能力边界

| 能做 | 不做 |
|---|---|
| 单人旁白、多角色对白（每个角色一个音色，逐句生成后本地拼接） | 不剪辑画面、不合成视频（输出音轨和字幕，交给剪映 / Premiere / CapCut / ffmpeg） |
| 账号已有角色（actor_id）或参考音频 URL 声音克隆 | 不克隆未经本人授权的声音 |
| 停顿、每个角色独立语速、生成模式和语气标签 | 不自动写稿（可以让 Agent 按下方方法先写稿） |
| 音频 / 视频识别成 SRT / TXT / JSON | 不做背景音乐混音、不做翻译（翻译由 Agent 完成） |
| `--dry-run` 离线试跑全流程 | |

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
python3 scripts/voiceover.py script examples/movie-recap.md -o out --dry-run      # 离线试跑示例
python3 scripts/voiceover.py script 稿件.md -o out --preset koubo                 # 整稿 → out/voiceover.wav + voiceover.srt + manifest.json
python3 scripts/voiceover.py script 稿件.md -o out --gap 0.3 --max-chars 16 --speaker-labels --model standard
python3 scripts/miragea_audio.py generate --text '试听一句' --actor-id ACTOR_ID --wait --output test1.mp3
python3 scripts/miragea_audio.py recognize --file 成片.mp4 --wait --output 成片.srt
```

- `--gap`：句间停顿秒数（默认 0.25）。`--max-chars`：每条字幕最多字数（默认 18，竖屏建议 12–16，英文建议 40）。
- `--preset` 一次设好句间停顿和字幕字数，仍可用 `--gap` / `--max-chars` 覆盖。

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “把这段口播稿配成音频” | 写入 `稿件.md`（单角色）→ `script 稿件.md -o out --preset koubo` |
| “电影解说配音，旁白加两个角色” | front matter 定义 narrator / 角色音色 → `script ... --preset jieshuo` |
| “用我的声音配音” | 用 `actors` 找到你已复刻的角色 actor_id；或给一段服务端能访问的参考音频 URL 和其中的原话 → `ref=` + `ref_text=` |
| “语气开心一点” | 查 `capabilities` 里所选模式的标签 → 角色加 `tags=标签名` |
| “只念一句试听” | `miragea_audio.py generate --text "..." --actor-id ID --wait --output test1.mp3` |
| “第五句说错了” | 只改那一行再跑同一条命令，其余句子复用 `out/lines/` |
| “给这个视频生成字幕” | `miragea_audio.py recognize --file 视频.mp4 --wait --output 视频.srt` |
| “先别花钱，试一下流程” | `script ... --dry-run` |

## 配音写稿通用方法论

不论什么场景，AI 配音好不好听，大部分取决于稿子是不是“为耳朵写的”。

### 1. 六条通用规则

1. **一行一句，一句一个意思**：中文一句尽量不超过 20 字；配音更自然，字幕也刚好一屏。
2. **写成要读出来的样子**：有歧义的数字、年份、型号、百分比写成汉字读法；需要逐字母念的缩写用空格隔开。
3. **口语替换书面语**：“因此”→“所以”，“进行调整”→“调一下”，长定语拆成两句。
4. **停顿只放在重点前后**：重点之前 0.3 秒，转场 0.4–0.6 秒，反转 / 落版 0.6–1.0 秒。
5. **一个角色一个声音，一个账号一个人设**：音色和语速写进 front matter，系列内容不要换。
6. **先试听一句，再整稿生成**：单句 `generate` 试开头句和难读的词，确认后再跑 `script`。

### 2. 各场景节奏对照

| 场景 | 句间停顿（预设） | 每条字幕字数（预设） | 建议语速 `speed` | 写稿重点 |
|---|---|---|---|---|
| 口播 | 0.15 秒 | 14 | 1.05–1.1 | 前 3 秒给结论，一条只讲一个观点 |
| 电影解说 | 0.3 秒 | 16 | 0.95–1.05 | 悬念开场，身份代称，反转前停顿 |
| 带货 | 0.1 秒 | 12 | 1.1–1.2 | 痛点 → 卖点画面化 → 一个指令 |
| 数字人 | 0.2 秒 | 16 | 0.95–1.05 | 纯人声、首尾留静音、一段一镜头 |
| 广告片 | 0.4 秒 | 14 | 0.9–1.0 | 意象短句、留白、品牌名 + slogan 落版 |
| 有声书 | 0.5 秒（字幕带角色名） | 20 | 0.9–1.0 | 选角表、对白拆分、三级停顿 |

### 3. 同一个声音两种语速

`speed` 按角色设置；需要同一音色“快讲铺垫、慢讲重点”时，用同一个 actor_id 定义两个角色：

```markdown
---
narrator: actor_id=123 speed=1.05
narrator_slow: actor_id=123 speed=0.9
---
[narrator] 他以为一切都结束了。
[pause 0.6]
[narrator_slow] 直到那通电话响起。
```

### 4. 外语版本怎么做

1. 中文稿定稿后，让 Agent 按目标市场口语改写（不是逐字直译），单位、称呼本地化。
2. 每种语言一个稿件文件；音色选账号里适合该语言的角色（`actors` 返回每个角色的 `language`），或换成该语言的参考音频 `ref=`，参考音频的语言可用 `language=` 提示。
3. 外语字幕 `--max-chars 40` 左右。
4. 先单句试听开头和难读的词，请母语者抽听后再整稿生成。

### 5. 交付前质量清单

- [ ] 开头一句试听过，音色和语速对吗？
- [ ] 数字、英文、人名、多音字读对了吗？
- [ ] `manifest.json` 的总时长符合视频要求吗？
- [ ] 字幕每条长度适合画面比例吗？
- [ ] 声音已授权、发布时标注了 AI 生成吗？

## 稿件语法

- 开头 `---` 之间每行定义一个角色：`角色名: actor_id=角色ID` 或 `角色名: ref=参考音频URL ref_text="参考音频里实际说的话"`；可加 `speed=`（0.25–4）、`model=expressive|standard`、`tags=标签1,标签2`、`language=`（参考音频的语言提示，用于自动识别参考文本）。
- `ref_text=` 只和 `ref=` 一起用；省略时服务端自动识别参考文本，计费方式不同，以 `capabilities` 为准。
- 正文 `[角色] 台词` 或 `[角色]：台词`；不写标签沿用上一位说话人。
- `[pause 0.6]` / `[停顿 0.6]` 插入停顿（秒）；`#` 开头的行、空行和 `<!-- 注释 -->` 会被忽略。
- 单句超过 `capabilities` 里的 `audio.max_text_length` 会被接口拒绝，拆成短句即可。
- 每句音频缓存在 `out/lines/`，同一句同一设置再次运行直接复用；没缓存时用同一个幂等键提交，服务端返回原任务、不重复创建。要新的一版加 `--fresh`。

## 示例稿件（examples/movie-recap.md）

```markdown
---
narrator: actor_id=YOUR_ACTOR_ID speed=1.05
hero: ref=https://example.com/your-sample.wav ref_text="参考音频里实际说的话"
---
# 电影解说示例（把 actor_id / ref 换成你自己的音色）
[narrator] 一个普通的快递员，捡到了一部能看见未来的手机。
[pause 0.5]
[hero]：如果明天的新闻里有我，那今天我该做什么？
[narrator] 他不知道的是，每看一次未来，现实就会悄悄改变一点。
```

## 接入剪辑

```bash
# 配音替换原视频音轨（需要本机 ffmpeg）
ffmpeg -i 画面.mp4 -i out/voiceover.wav -map 0:v -map 1:a -c:v copy -shortest 配音版.mp4
# 把字幕烧进画面
ffmpeg -i 配音版.mp4 -vf subtitles=out/voiceover.srt -c:a copy 成片.mp4
```

- **剪映 / CapCut / Premiere**：导入 `voiceover.wav` 到音轨，`voiceover.srt` 导入字幕轨即可。
- **按句卡点**：`manifest.json` 每句有 `start` / `end` 秒数，用来切镜头、放花字、对齐数字人片段。
- **数字人工具**：`voiceover.wav` 是纯人声，可直接作为驱动音频；需要 MP3 或特定采样率时用 ffmpeg 转换。

## 方案对比：AI配音、人工配音和本地模型

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 复杂情绪表演 | 状态好的真人仍然最强 | 取决于模型和调参 | 稳定一致，适合信息传递和批量生产；顶级情绪表演仍建议真人 |

结论：日更、多版本、频繁改稿的内容，本技能在改稿成本和字幕时间轴上优势最大；对情绪表演要求极高的单条精品，真人配音仍然值得。

## 常见问题（FAQ）

**AI配音需要显卡或本地部署模型吗？**
不需要。生成在 Miragea 云端完成，本地只需 Python 3.9+ 标准库，不用 pip 安装任何包。

**AI配音怎么用自己的声音？**
两种方式：用账号里已经复刻好的角色（`actors` 查 actor_id），或提供一段服务端能直接访问的参考音频 URL，并写上音频里实际说的话（`ref_text=`）。样本要求和计费以 `capabilities` 和官网说明为准。

**AI配音一段视频里能有好几个人说话吗？**
能。稿件开头定义多个角色，每个角色一个音色和语速，正文用 `[角色]` 切换；脚本逐句生成后拼成一条音轨，并同时出字幕。

**AI配音能调语气和情绪吗？**
能用语气标签：先 `capabilities` 查看所选生成模式提供的 `tags[].label`，在角色上写 `tags=标签名`。另外可以用 `speed=` 调语速、用 `[pause]` 控制停顿。

**AI配音生成的字幕时间准吗？**
每句的起止时间来自真实生成的音频长度，句内按字数分配。需要逐字更精确的时间轴，可对成品音频再跑一次 `recognize`。

**AI配音稿子改了一句，要整段重新生成吗？**
不用。改那一行后重跑同一条命令，只有改过的句子会重新生成，其余从 `out/lines/` 复用，自动重新拼接音轨和字幕。

**AI配音收费吗？一次能配多少字？**
按账号额度消耗，单句字数上限和计费规则以 `capabilities` 实时返回为准；`--dry-run` 不调用接口。

**抖音、视频号用 AI配音会限流吗？**
没有工具能保证流量。按平台规则标注 AI 生成内容是必须的；流量更多取决于内容本身。

**已经录好的视频能自动出字幕吗？**
能，`miragea_audio.py recognize --file 视频.mp4 --wait --output 视频.srt`；加 `--subtitle-format txt` 得到纯文字稿。

**支持哪些 AI Agent？**
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
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **AI voiceover & subtitles (AI配音)** for agents: write a script with `[speaker]` tags, run one command, get `voiceover.wav`, timed `voiceover.srt` and `manifest.json`.
- Voices: saved voices in your account (`actor_id`) or **voice cloning** from a reference audio URL plus its transcript; generation modes, tone tags, speed 0.25–4.
- Multi-speaker scripts are rendered line by line through the official client's `generate` and joined locally; `recognize` turns existing audio/video into SRT/TXT/JSON.
- Limits and pricing come live from `capabilities`. Python 3.9+ standard library, no GPU, `--dry-run` offline. Service: Miragea API (https://miragea.ai/v1).

**关键词**：AI配音、视频配音、声音克隆、字幕生成、文字转语音、文本转语音、语音合成、声音复刻、多角色配音、短视频配音、口播配音、电影解说配音、小说推文配音、广告配音、英文配音、AI旁白、SRT、TTS、voiceover、voice cloning、text to speech、subtitles

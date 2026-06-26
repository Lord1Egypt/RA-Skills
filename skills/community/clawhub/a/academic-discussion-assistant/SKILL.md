---
name: academic-discussion-assistant
description: >
  Use when: 用户要把研究生组会、与导师讨论论文修改、技术方案推敲等小规模学术讨论录音转成纪要，并提取老师意见、学生回应、待修改事项和后续动作时触发。
  适用于 2 到 3 人、以老师和学生为主的学术讨论场景。Skill 会优先使用 SenseAudio ASR 的说话人分离能力，再结合 Agent 的大模型摘要能力，最后调用 SenseAudio TTS 返回适合收听的语音摘要。
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"primaryEnv":"SENSEAUDIO_API_KEY"}}
---

# Academic Discussion Assistant

你是学术讨论纪要助手。此 Skill 专门处理研究生组会、导师与学生讨论论文修改或技术问题的整段录音，并生成三类产物：

- ASR 原始转写文本
- 结构化学术讨论纪要与关键信息提取
- 语音版摘要音频

此 Skill 必须使用本目录下参考资料所描述的 **SenseAudio 官方 ASR/TTS 接口**，不要替换成其他语音服务。

## 何时使用

当用户出现这些意图时触发：

- “把这段组会录音整理成纪要”
- “把和老师讨论论文修改的录音总结一下”
- “上传录音后帮我提炼导师意见和学生要改什么”
- “做一个带语音回复的论文讨论总结”
- “输出论文讨论原文 txt 和简短语音总结”

如果用户只是问 API 参数含义、模型差异或讨论方案，不要直接执行脚本。

## 最高优先级规则

1. 默认优先用 `sense-asr-pro` 做会议转写。
2. 默认开启 **说话人分离**；学术讨论场景不要退化成单人纯文本识别。
3. 默认输出 `verbose_json`，并落盘原始 JSON、纯文本、带说话人文本、LLM 输入文本。
4. 摘要必须基于转写结果，不得编造未提及的信息。
5. TTS 只朗读“简明摘要”部分，不要整篇会议纪要全部朗读。
6. 如果未配置 `SENSEAUDIO_API_KEY`，不要假装执行成功，必须提示用户补充配置。
7. 如果录音文件超过 10MB，本 Skill 不自动切片；要明确提示用户先切片再处理。
8. 如果说话人数量未知，默认 `max_speakers=3`；用户明确提供人数时按用户指定。
9. 该 skill 的默认讨论规模是不超过三人；若用户给出明显更大规模的正式会议，再保留原有泛化会议写法，但摘要仍要优先提炼决策与行动项。
10. 不要把“可能是谁”写成事实。发言人身份未知时保持 `发言人1/2/...`，但在摘要中要尽量根据上下文区分“老师/导师”和“学生/汇报者”。
11. 如果能根据措辞稳定判断角色，摘要中应明确写成“老师”“学生”；无法判断时再退回“发言人1/2/...”，并说明角色未完全确认。
12. 对老师提出的修改意见、判断、要求和结论，应比学生的解释性发言获得更高权重，在“核心结论”“行动项”“简明摘要”里优先呈现。
13. 生成摘要语音后，优先通过 OpenClaw 的 `MEDIA:./relative/path` 机制把音频作为聊天媒体返回，而不是只回本地路径文本。
14. 不要绕到其他 TTS skill 或手工拼路径回复。会议摘要语音必须通过本 skill 的 `scripts/main.py tts` 或 `scripts/main.py run` 生成。
15. 当脚本输出 `MEDIA:./...` 时，必须把这行原样放进最终回复内容中，让 OpenClaw/Feishu 渠道把它解析成音频附件；不要只用自然语言转述文件路径。

## 数据流

```text
学术讨论录音 -> SenseAudio ASR -> 原始转写与说话人分离文本
             -> Agent 摘要提取 -> 结构化纪要 + 简明摘要
         -> SenseAudio TTS -> 语音摘要文件
```

## 环境变量

必需：

```bash
SENSEAUDIO_API_KEY
```

可选：

```bash
SENSEAUDIO_API_BASE
```

默认值：

```bash
https://api.senseaudio.cn
```

## 目录约定

Skill 根目录下关键文件：

- `scripts/main.py`：统一 CLI
- `references/summary_prompt.md`：给大模型的学术讨论纪要提炼模板

默认输出目录：

```bash
./outputs/<audio-stem>-<timestamp>/
```

输出文件包括：

- `asr_verbose.json`
- `transcript_raw.txt`
- `transcript_diarized.txt`
- `llm_meeting_input.txt`
- `meeting-summary-<timestamp>.mp3` 或其他格式音频

## 模型与参数选择

### ASR 默认选择

- 模型：`sense-asr-pro`
- 原因：导师-学生讨论场景精度更高，支持说话人分离和时间戳
- `response_format=verbose_json`
- `enable_speaker_diarization=true`
- `timestamp_granularities[]=segment`
- `timestamp_granularities[]=word`
- `enable_sentiment=false`
- `enable_itn=true`
- `enable_punctuation=true`

### TTS 默认选择

- 模型：`SenseAudio-TTS-1.0`
- `voice_id=male_0004_a`
- `format=wav`
- `sample_rate=32000`
- `bitrate=128000`
- `channel=1`

## 标准执行流程

### 步骤 1：检查 API Key

```bash
python3 ./scripts/main.py auth-check
```

当前 `auth-check` 只做本地配置检查，不再发送伪造音频请求，避免被服务端 500 卡住。

若未配置 Key，要明确告知用户先设置：

```bash
export SENSEAUDIO_API_KEY=""
export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"
```

### 步骤 2：执行讨论录音转写

```bash
python3 ./scripts/main.py transcribe \
  --audio "/path/to/discussion.m4a" \
  --language zh \
  --max-speakers 3
```

这一步会生成：

- ASR 原始 JSON
- 原始全文 `txt`
- 说话人分离版 `txt`
- 给 LLM 用的 `llm_meeting_input.txt`

### 步骤 3：读取摘要 Prompt

需要摘要时，先读取：

- `references/summary_prompt.md`
- 第 2 步产出的 `llm_meeting_input.txt`

用该 Prompt 指导大模型输出：

- 讨论概览
- 论文/技术问题诊断
- 老师意见与学生回应
- 核心结论
- 行动项
- 重点关注事项
- 简明摘要

### 步骤 4：把“简明摘要”转为语音

先将最终适合朗读的摘要存为文本，或者直接传参：

```bash
python3 ./scripts/main.py tts \
  --text "本次会议主要围绕..." \
  --voice-id male_0004_a \
  --format mp3
```

脚本会同时输出：

- 本地音频文件路径
- 一行 `MEDIA:./...`

在 OpenClaw 的 Feishu 对话中，这行 `MEDIA:` 会被识别为媒体附件并直接发送语音，而不是只显示路径。

### 步骤 5：全流程串联

如果你已经拿到了最终的中文摘要文本，可以直接一条命令同时完成：

```bash
python3 ./scripts/main.py run \
  --audio "/path/to/discussion.m4a" \
  --language zh \
  --max-speakers 3 \
  --text-file "/path/to/final_summary.txt"
```

注意：

- `run` 不会自动调用外部 LLM 生成摘要，它要求你把最终摘要文本通过 `--text` 或 `--text-file` 传进来
- 这是刻意设计，目的是把“可变的推理摘要”留给 Agent，把“稳定的 ASR/TTS 调用和落盘”交给脚本

## 推荐工作方式

处理用户真实请求时，按下面顺序做：

1. 运行 `transcribe`
2. 读取 `references/summary_prompt.md`
3. 基于 `llm_meeting_input.txt` 生成结构化学术讨论纪要，明确区分老师和学生
4. 从纪要里抽出“简明摘要”
5. 运行 `tts` 生成语音，且只能调用本 skill 的 `scripts/main.py`
6. 把以下结果一起交付给用户：
   - 结构化讨论纪要
   - 语音摘要媒体消息
   - `transcript_raw.txt` 路径
   - 如有需要，再附 `transcript_diarized.txt`

## 场景化摘要原则

处理研究生组会、导师改稿讨论时，摘要必须遵守以下原则：

1. 优先识别讨论主题是“论文写作修改”“实验设计复盘”“技术方案讨论”中的哪一类。
2. 若出现明显的老师口吻，如“你们回去改”“这里不要这样写”“改完再发我”，要在摘要中标为老师意见，并提高权重。
3. 学生发言通常是提问、确认理解、解释当前写法或承诺修改；摘要里应作为回应和执行计划来写，不应与老师意见并列成同等结论。
4. “核心结论”优先写老师给出的判断和修改方向；“行动项”优先写学生要完成的改动。
5. 如果存在明确的审稿意见、论文段落、模块设计、指标、实验结果、理论解释，这些技术性细节应保留，不要被泛化成“继续优化”“进一步完善”这类空话。

## Feishu 返回规则

当用户来自 Feishu，且已经成功生成摘要音频时，最终回复必须满足：

1. 回复正文里包含一行脚本输出的 `MEDIA:./...`
2. 可以附带一两句简短说明，但不要只给绝对路径
3. 不要改用 `senseaudio-tts` skill 补做二次合成
4. 不要把 `MEDIA:./...` 放进代码块

推荐最终回复形式：

```text
这是本次会议的语音摘要。
MEDIA:./outputs/xxx/final_summary.mp3
原始转写文本：./outputs/xxx/transcript_raw.txt
```

## 失败处理

- 如果接口返回 401/403：说明 API Key 无效或无权限
- 如果返回 429：提醒用户稍后重试
- 如果音频 >10MB：明确提示用户先切片
- 如果 TTS 文本 >10000 字：要求先压缩或分段
- 如果会议中没提到时间、地点、负责人：摘要中写 `未明确提及`

## 脚本命令摘要

### 检查鉴权

```bash
python3 ./scripts/main.py auth-check
```

### 仅做转写

```bash
python3 ./scripts/main.py transcribe --audio "/path/to/meeting.wav"
```

### 仅做摘要语音

```bash
python3 ./scripts/main.py tts --text "这里是摘要"
```

### 转写并输出摘要语音

```bash
python3 ./scripts/main.py run \
  --audio "/path/to/meeting.wav" \
  --text-file "/path/to/summary.txt"
```

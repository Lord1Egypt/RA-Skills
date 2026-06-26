---
name: senseaudio-bedtime-radio
description: Generate a complete bedtime story audio program from a keyword — with intro, narration, character voices, and a sleepy outro. Use when parents or caregivers want a bedtime story, or when users ask for "睡前故事", "哄睡音频", "儿童故事音频", "给孩子讲故事", or any request to create a soothing story audio for children.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
        - xxd
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Bedtime Radio

Generate a complete bedtime story audio program — not just a TTS read-aloud, but a structured radio-style show with intro, paced narration, character voices, and a sleepy outro.

## Step 1: Collect Inputs

Ask the user for:
- **故事关键词** — e.g., "月亮上的小兔子", "会飞的小猪", "森林里的魔法书"
- **孩子年龄** — affects vocabulary and story complexity (default: 4–6岁)
- **时长偏好** — 短版 (~2分钟) / 标准版 (~4分钟) / 长版 (~6分钟)

## Step 2: Write the Story (LLM task)

Generate the story yourself — no API call needed for this step. Follow these rules based on age:

| Age | Vocabulary | Sentence length | Story complexity |
|-----|-----------|-----------------|-----------------|
| 2–3岁 | 极简，常用词 | ≤10字/句 | 单线情节，重复句式 |
| 4–6岁 | 简单，生动 | 10–18字/句 | 简单起承转合 |
| 7–10岁 | 丰富，有细节 | 15–25字/句 | 有悬念和转折 |

**Story structure:**
- 开头：交代主角和场景（1段）
- 发展：遇到问题或冒险（2–3段）
- 高潮：解决问题的关键时刻（1段）
- 结尾：温馨收尾，引导入睡（1段，语气渐缓）

**Length guide:**
- 短版：约300字
- 标准版：约600字
- 长版：约1000字

Mark dialogue lines with the character name: `[小兔子]: "..."` `[老爷爷]: "..."`

## Step 3: Plan the Audio Program

Structure the full program before making any API calls:

```
[片头]  "晚安，小朋友。今天的故事叫做《<标题>》。"
        voice: female_0006_a, speed: 0.9

[正文段落1]  旁白第一段
        voice: female_0006_a, speed: 0.85
        + <break time="2000"> after paragraph

[对话]  角色台词（如有）
        小动物/儿童角色 → child_0001_b, speed: 0.9
        老人/长辈角色   → male_0004_a, speed: 0.85
        旁白继续        → female_0006_a

[正文后半段]  speed 逐段降低：0.85 → 0.80 → 0.75
        模拟催眠节奏

[片尾]  "故事讲完啦，闭上眼睛，晚安……"
        voice: female_0006_a, speed: 0.7
```

## Step 4: Synthesize Each Segment

Generate each segment as a separate mp3 file, then list them for the user to assemble.

**Segment synthesis pattern:**

```bash
synthesize() {
  local TEXT="$1"
  local VOICE="$2"
  local SPEED="$3"
  local OUTFILE="$4"

  curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"SenseAudio-TTS-1.0\",
      \"text\": \"$TEXT\",
      \"stream\": false,
      \"voice_setting\": { \"voice_id\": \"$VOICE\", \"speed\": $SPEED },
      \"audio_setting\": { \"format\": \"mp3\" }
    }" -o "${OUTFILE}.json"

  jq -r '.data.audio' "${OUTFILE}.json" | xxd -r -p > "$OUTFILE"
  echo "$(jq '.extra_info.audio_length' "${OUTFILE}.json")ms — $OUTFILE"
}
```

**Segment breakdown:**

| Segment | Text | Voice | Speed | File |
|---------|------|-------|-------|------|
| 片头 | "晚安，小朋友。今天的故事叫做《<标题>》。" | female_0006_a | 0.9 | 00_intro.mp3 |
| 正文段1 | 第一段旁白 | female_0006_a | 0.85 | 01_narration.mp3 |
| 正文段2 | 第二段旁白 | female_0006_a | 0.85 | 02_narration.mp3 |
| 对话（如有）| 角色台词 | child_0001_b / male_0004_a | 0.9 | 03_dialogue.mp3 |
| 正文段3 | 后半段旁白 | female_0006_a | 0.80 | 04_narration.mp3 |
| 正文段4 | 结尾段旁白 | female_0006_a | 0.75 | 05_narration.mp3 |
| 片尾 | "故事讲完啦，闭上眼睛，晚安……" | female_0006_a | 0.7 | 06_outro.mp3 |

Insert `<break time=2000>` at paragraph boundaries within a segment's text to create natural pauses between paragraphs.

## Step 5: Output

List all generated files with durations and assembly instructions:

```
睡前故事电台生成完成：《<标题>》

文件列表（按顺序播放）：
  00_intro.mp3        — 片头 (8秒)
  01_narration.mp3    — 第一段 (42秒)
  02_narration.mp3    — 第二段 (38秒)
  03_dialogue.mp3     — 对话 (25秒)
  04_narration.mp3    — 第三段，渐慢 (45秒)
  05_narration.mp3    — 结尾段，更慢 (40秒)
  06_outro.mp3        — 片尾 (12秒)

总时长：约 3分50秒

合并命令（需要 ffmpeg）：
  ffmpeg -i "concat:00_intro.mp3|01_narration.mp3|..." -acodec copy story.mp3
```

If the user wants a different story or age group, regenerate only the story text and re-synthesize — the program structure stays the same.

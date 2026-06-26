---
name: senseaudio-video-bgm-maker
description: Generate original background music for short videos from a natural language description. Use when creators need royalty-free BGM, video background music, or audio for content. Triggers on "短视频配乐", "背景音乐", "BGM", "视频配乐", "vlog音乐", "原创配乐", or any request to generate music for a specific video scene, mood, or duration.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Video BGM Maker

Generate original, royalty-free background music matched to a video's mood and duration. Users describe their video in plain language — no music terminology required.

## Step 1: Collect Input

Two paths:

**A — Free description:** User describes their video naturally.
> "一个人在雨天咖啡馆看书的Vlog，时长45秒"
> "开箱科技产品，要有未来感，30秒"
> "宠物猫咪日常，轻松可爱，1分钟"

**B — Preset scenes (quick pick):** If the user wants to skip describing, offer these:

| # | 场景 | 默认风格 |
|---|------|---------|
| 1 | 美食探店 | warm acoustic, appetizing |
| 2 | 旅行Vlog | cinematic, adventurous |
| 3 | 产品开箱 | electronic, modern, clean |
| 4 | 运动健身 | energetic, driving beat |
| 5 | 宠物日常 | playful, light, cheerful |
| 6 | 知识讲解 | minimal, focused, corporate |
| 7 | 情感故事 | piano ballad, emotional |
| 8 | 城市街拍 | lo-fi, chill, urban |

Also ask: **视频时长？** (default: 30秒)

## Step 2: Translate to Music Parameters

Map the description to style tags. Think in terms of: genre + mood + instrumentation + energy level.

| Scene / Keyword | Style tags |
|-----------------|-----------|
| 咖啡馆 / 下午茶 / 慵懒 | lo-fi, cafe, acoustic guitar, warm, relaxed |
| 科技 / 未来 / 数码 | electronic, synthesizer, futuristic, clean |
| 旅行 / 风景 / 自然 | cinematic, orchestral, adventurous, uplifting |
| 美食 / 烹饪 / 探店 | acoustic, warm, cheerful, light jazz |
| 运动 / 健身 / 活力 | energetic, driving, rock, upbeat, powerful |
| 宠物 / 可爱 / 萌 | playful, xylophone, light, cheerful, cute |
| 情感 / 治愈 / 温暖 | piano, strings, emotional, gentle |
| 城市 / 街拍 / 夜晚 | lo-fi hip hop, urban, chill, beats |
| 知识 / 教程 / 商务 | minimal, corporate, clean, focused |
| 古风 / 国风 | traditional Chinese, guqin, erhu, cinematic |

Always append duration hint to style: `"30-second loop"` or `"60-second complete piece with build and resolution"`.

**Duration strategy:**
- ≤30s → `"short loop, complete in 30 seconds, no long intro"`
- 30–90s → `"complete piece, build up in first third, peak in middle, resolve at end"`
- >90s → `"extended piece with intro, development, and outro"`

## Step 3: Generate 3 Versions

Always generate 3 variations with slightly different instrumentation — same mood, different texture. This gives the user real choice without requiring them to re-describe.

Build 3 style strings from the base style:

```
Version A: <base_style>, <primary instrument>
Version B: <base_style>, <alternative instrument>
Version C: <base_style>, <third instrument variation>
```

Example for "咖啡馆Vlog, 45秒":
- A: `"lo-fi, cafe, acoustic guitar, warm, relaxed, 45-second complete piece"`
- B: `"lo-fi, cafe, piano, warm, relaxed, 45-second complete piece"`
- C: `"lo-fi, cafe, jazz guitar, mellow, relaxed, 45-second complete piece"`

Submit all 3 in parallel:

```bash
for i in 1 2 3; do
  RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/music/create" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"sensesong\",
      \"instrumental\": true,
      \"style\": \"<STYLE_V${i}>\",
      \"negative_tags\": \"vocals, lyrics, singing, spoken word\"
    }")
  TASK_IDS[$i]=$(echo $RESP | jq -r '.task_id')
  echo "Version $i task: ${TASK_IDS[$i]}"
done
```

Poll all 3 tasks (check every 5s):

```bash
for i in 1 2 3; do
  while true; do
    POLL=$(curl -s "https://api.senseaudio.cn/v1/song/music/pending/${TASK_IDS[$i]}" \
      -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
    STATUS=$(echo $POLL | jq -r '.status')
    [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ] && break
    sleep 5
  done
  RESULTS[$i]=$POLL
done
```

## Output

Present all 3 versions clearly:

```
短视频配乐生成完成 🎵

场景：雨天咖啡馆Vlog（45秒）

版本 A — 原声吉他风
  时长：<duration>秒
  链接：<audio_url>

版本 B — 钢琴风
  时长：<duration>秒
  链接：<audio_url>

版本 C — 爵士吉他风
  时长：<duration>秒
  链接：<audio_url>

版权说明：以上音乐由 SenseAudio AI 原创生成，可免费用于个人和商业短视频创作。
```

If the user wants a different mood or style after listening, ask them which version was closest and what to adjust — then regenerate that single version with the updated style.

---
name: bytedance-visual-recognition
description: >
  Multimodal visual recognition via Doubao-Seed (6 models) + Zhipu GLM (2 free models).
  Image/video to text/code, auto-fallback, batch directory processing, follow-up conversations,
  local media caching (Temp/), persistent history (vision_history.json), auto IAM console sync.
  First-run privacy notice, plaintext config.json, cross-platform.
summary: "Doubao-Seed + GLM visual recognition — image/video to text/code with auto-fallback, batch, follow-up, IAM sync"
tags:
  vision: "5.0.1"
  image-recognition: "5.0.1"
  video-recognition: "5.0.1"
  image-to-code: "5.0.1"
  video-to-code: "5.0.1"
  doubao: "5.0.1"
  glm: "5.0.1"
trigger_patterns:
  - "豆包识别"
  - "豆包视觉识别"
  - "bytedance visual recognition"
  - "doubao recognize"
metadata:
  openclaw:
    requires:
      bins:
        - python
    permissions:
      filesystem:
        read: ["config.json", "vision_history.json", ".last_response"]
        write: ["Temp/", "vision_history.json", ".last_response", "config.json"]
      network:
        - host: "ark.cn-beijing.volces.com"
          purpose: "Doubao vision model API"
        - host: "open.bigmodel.cn"
          purpose: "GLM vision model Chat Completions API"
        - host: "open.volcengineapi.com"
          purpose: "Auto IAM console usage sync"
    emoji: "🔍"
    homepage: https://www.volcengine.com/docs/82379/1569618
    locales: ["en"]
---

# ByteDance Visual Recognition — Doubao-Seed + GLM

Doubao-Seed (6 models) + Zhipu GLM (2 free models). First run auto-generates `config.json`, fill in one API Key to start. IAM console usage syncs automatically on each recognition.

## Privacy & Data Notice

- **Network**: Selected images/videos and prompts are base64-encoded and sent to Volcengine (Doubao) or Zhipu (GLM) cloud APIs.
- **Local cache**: Media files temporarily copied to `Temp/YYYYMMDD/`, default 7-day retention (`temp_retention_days` in config.json, range 1-3650).
- **History**: Recognition history stored in `vision_history.json`, follow-up context in `.last_response`, auto-cleaned after 7 days. GLM follow-up reuses full message history including base64 media data; Doubao follow-up uses previous_response_id without re-transmitting files.
- **Credentials**: API Keys stored in plaintext `config.json`. Do not use personal keys on shared machines.
- **IAM sync**: Automatically syncs token usage from Volcengine IAM console on each recognition when IAM credentials are configured.
- **First run**: A privacy notice is displayed once. Continuing past it acknowledges data handling practices.

## Setup (pick one)

### Doubao (Volcengine)

1. Join the [Collaboration Rewards Program](https://console.volcengine.com/ark/region:cn-beijing/openManagement/rewardPlan) for free quota, then get your API Key
2. Create inference endpoints, pick from:

| config key | model | priority |
|--------|------|:---:|
| `doubao_seed_21p_id` | Doubao-Seed-2.1-Pro | primary |
| `doubao_seed_21t_id` | Doubao-Seed-2.1-Turbo | secondary |
| `doubao_seed_20p_id` | Doubao-Seed-2.0-Pro | tertiary |
| `doubao_seed_20c_id` | Doubao-Seed-2.0-Code | code-first |
| `doubao_seed_20l_id` | Doubao-Seed-2.0-Lite | fallback |
| `doubao_seed_20m_id` | Doubao-Seed-2.0-Mini | low-cost |

3. Edit `config.json`, replace `""` with actual endpoint IDs.

### GLM (Zhipu, free)

1. https://open.bigmodel.cn → get API Key
2. Edit `config.json`: `"zhipu_api_key": "your-key"`

### Provider filter

`provider_mode` in `config.json`:
- `0` = all (default)
- `1` = Zhipu only
- `2` = Doubao only

### Test

```bash
python doubao_vision_recognize.py --help
python doubao_vision_recognize.py status
```

---

## Commands

| command | purpose | example |
|------|------|------|
| `rec <file> --image\|--video --text\|--code` | recognize | `rec a.jpg --image --text` |
| `rec <dir> --batch --image\|--video --text\|--code` | batch | `rec ./img/ --batch --image --text` |
| `ask --text\|--code --prompt "..."` | follow-up | `ask --text -p "details"` |
| `status` | usage stats | |
| `sync` | manual console sync | |
| `history` | 7-day history | |

### Parameters

| param | desc |
|------|------|
| `--image` | image input |
| `--video` | video input |
| `--text` | text output |
| `--code` | code output |
| `--prompt` / `-p` | extra instruction |
| `--batch` | directory batch |

---

## Behavior Rules

### 1. Trigger only on listed patterns
Activate only when the user's message matches one of the trigger_patterns above. Do NOT activate on loosely related text. If uncertain, ask before executing.

### 2. Parameter inference
- "recognize/analyze image" → `--image --text`
- "recognize/analyze video" → `--video --text`
- "convert to code / UI to code / design to code" → `--code`
- extra requirements → `--prompt "..."`
- unsure → ask once if image or video

### 3. Credential safety
API keys are stored in plaintext config.json. Warn users not to use high-value keys on shared machines. First-run privacy notice already discloses plaintext storage.

---

## Limits

- Doubao: 180W tokens per model per day, auto-fallback
- GLM: free, auto-retry on failure (4.6V: 10 retries, 4.1V: 5 retries)
- Image ≤ 15MB, Video ≤ 50MB

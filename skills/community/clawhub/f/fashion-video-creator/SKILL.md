---
name: fashion-video-creator
description: "穿搭视频创作 — 生成虚拟模特图(Seedream 4.5/5.0) + Seedance 2.0 视频Prompt + 操作手册(SOP)。支持单条和批量模式。Use when: '帮我做穿搭视频', '生成模特图', 'generate outfit video', '批量生成穿搭prompt', '穿搭创作', '虚拟模特'. Do NOT use for video analysis/reverse engineering — use viral-video-replicator instead."
version: "1.1.0"
compatibility: "Claude Code, Claude.ai, and all SKILL.md-compatible agents"
---

# Skill: fashion-video-creator

## Overview

Generate complete assets for fashion e-commerce videos from scratch: a virtual model image (Seedream text-to-image) + a Seedance 2.0 video prompt with dialogue, actions, and scene + an operator SOP for the Jimeng platform. Supports single and batch modes.

## When to Activate

User query contains any of:
- "穿搭视频", "outfit video", "生成模特", "虚拟模特"
- "seedance prompt", "穿搭创作", "带货视频", "带货短视频"
- "帮我做个穿搭视频", "批量生成穿搭", "batch prompt"
- "帮我拍个带货视频", "我有件衣服想做个展示视频", "做个穿搭短视频"
- "generate fashion video", "create outfit content"

Do NOT activate for:
- Analyzing / reverse-engineering existing videos -> use `viral-video-replicator`
- "这个视频怎么拍的", "帮我复刻这个视频" -> use `viral-video-replicator`
- Pure image generation without video prompt -> direct Seedream API call
- Non-fashion video generation -> not applicable

## Prerequisites

This skill requires a Volcano Engine (火山方舟) account with Seedream model access.

```
Required: ARK_API_KEY + Seedream model/endpoint ID
Optional: None (all other logic is local)
```

## Clarification Flow

### Phase 1: API Key Acquisition

Ask these questions IN ORDER. Use plain language — the user may not be technical.

**Q1: Image Generation Service**
> "你需要先有一个能生成图片的 AI 服务账号。目前这个工具使用的是火山方舟平台的 Seedream 模型。
> 你有火山方舟的账号吗？如果有，请提供你的 API Key（在火山方舟控制台 -> API Key 管理中可以找到）。"

If user has no account -> STOP. Guide them to register at 火山方舟. Do NOT proceed without API key.

**Q2: Model Version**
> "火山方舟上有两个版本的图片生成模型：
> - **Seedream 5.0**（推荐）：理解能力更强，生成的人像更自然，每张约 0.22 元
> - **Seedream 4.5**：可以更精细地控制细节，每张约 0.32 元
>
> 你开通了哪个？需要提供模型ID或接入点ID。"

### Phase 2: Mandatory Recommendations

MUST show before proceeding. These are not optional tips — violating them degrades output quality:

```
============================================================
API Configuration — Mandatory Recommendations
============================================================

[REQUIRED] Seedream 5.0 endpoint preferred
  WHY: 5.0 uses internal Chain-of-Thought reasoning, making natural
  language prompts significantly more effective. 4.5 relies on keyword
  stacking which loses semantics in complex body descriptions.
  If only 4.5: use model ID doubao-seedream-4-5-251128 or newer.

[REQUIRED] Realism scale 40-60
  WHY: Below 30 the output looks cartoonish (Pixar-style), unsuitable
  for product videos that need believable human models. Above 80 triggers
  uncanny valley artifacts and skin texture glitches.

[WARNING] Using older models or non-recommended endpoints will produce
noticeably worse portrait realism and clothing detail accuracy.
============================================================
```

### Phase 3: Mode Selection

> "你要生成几条视频？单条还是批量？"

### Phase 4: Creative Parameter Collection

**Collection strategy — ask in 2 rounds, never more than 4 questions per round:**

**Round 1 (required — must have before executing):**
1. Model gender (female/male) — default: female
2. Garment type (dress/top/pants/jacket/suit/casual) — NO default, must ask. WHY: "default" type produces generic dialogue without product-specific selling points. **Defensive fallback:** If user declines to specify after 2 attempts, fall back to "default" with warning: "Using generic dialogue — conversion effectiveness will be lower than type-specific scripts."
3. Scene (11 presets or custom text) — default: modern_apartment

**Round 2 (enhanced — use defaults if not stated):**
4. Model appearance: preset (9 templates) / body params / custom desc — default: asian_female_slim
5. Realism (0-100) — default: 40
6. Style: realism / pixar / anime_realistic — default: realism
7. Dialogue style: natural / professional / enthusiastic — default: natural
8. Camera: vlog / pro / static — default: vlog
9. Target audience: auto / female / male — default: auto
10. Duration (5-40s) — default: 10
11. Language: zh / en — default: zh
12. Task label (batch only)

**Batch shortcut:** If all tasks share config, ask once and apply to all. Only collect per-task differences.

### Batch-Specific Recommendations

When batch mode selected, ADDITIONALLY show:

```
============================================================
Batch Mode — Additional Recommendations
============================================================

[REQUIRED] Specify exact garment type per task — do NOT use "default"
  WHY: Each garment type has 500+ chars of specialized dialogue with
  product-specific hand gestures (e.g., dress: pull hem to show fabric;
  pants: flip waistband to show grip strip). "default" loses all this.

[RECOMMENDED] Same gender per batch
  WHY: Mixing genders creates inconsistent dialogue tone — female uses
  filler words and emotional reactions, male is direct and factual.

[REQUIRED] Duration 10-15 seconds
  WHY: Under 5s cannot complete a product showcase. Over 15s triggers
  multi-segment auto-chaining which requires manual "extend" operations.
============================================================
```

## Core Workflow

### Step 0: Verify API Key (mandatory, never skip)

Platform-adaptive verification:

**If bash/Python available (Claude Code, terminal):**
```python
import httpx
resp = httpx.get(f"{ARK_API_BASE}/api/v3/models",
                 headers={"Authorization": f"Bearer {ARK_API_KEY}"}, timeout=10)
# 200 -> proceed. 401/403 -> key invalid. Timeout -> network issue.
```

**If no code execution (Claude.ai web, chat-only):**
Trust the user-provided key and proceed. Mark internally: `api_verified: false`.
If Step 3 (image generation) fails with 401 -> surface the error then.

- Key valid -> proceed to Step 1
- Key invalid (401/403) -> report error, ask user to verify. Do NOT proceed.
- No code execution -> proceed with unverified key, validate on first API call.

### Single Mode

```
Step 1: Collect parameters (2 rounds max)
Step 2: Build model prompt (version-aware: 4.5 keyword / 5.0 natural language)
Step 3: Call Seedream API -> generate model image (720x1280, 9:16)
Step 4: Build Seedance prompt -> compose dialogue + actions + scene + camera
        Read references/dialogue-library.md for garment-specific scripts
        Read references/prompt-assembly.md for assembly rules
Step 5: Generate SOP
Step 6: If duration > 15s -> build chained multi-segment extend plan
Step 7: Validate output (see below)
```

### Batch Mode

```
Step 0: Verify API key
Step 1: Collect batch size + per-task configs (2 rounds)
Step 2: Validate all configs (garment type != "default"?)
Step 3: For each task (sequential):
  a. Build model prompt
  b. Call Seedream API (if image needed)
  c. Compose dialogue (opening + core + closing) from dialogue-library.md
  d. Compose actions (garment-specific choreography)
  e. Assemble Seedance prompt
  f. If duration > 15s: build chained segments
  g. Generate SOP
  h. Mark task: completed / failed
Step 4: Validate all outputs
Step 5: Return results with progress summary

Progress: queued -> processing -> completed/failed
Partial success: batch completes even if some tasks fail.
```

### Output Validation (mandatory, never skip)

Before delivering results, verify ALL:

- [ ] Model image is 9:16 portrait with full body visible (head to feet)?
- [ ] Prompt contains @image1 (garment) and @image2 (model ref)?
- [ ] Dialogue matches the selected garment type (not generic "default")?
- [ ] SOP specifies correct image upload order (image1=garment FIRST)?
- [ ] If chained: every segment has continuation prompt + dialogue preview?
- [ ] Brand constraint present: "Do not alter clothing pattern, color, texture or style"?

**Any NO -> fix before delivering. Do NOT send unvalidated output.**

## Error Handling

| Failure | Detection | Action |
|---------|-----------|--------|
| No API key | ARK_API_KEY empty or missing | **STOP.** Guide user to 火山方舟 console. Do NOT proceed. |
| Invalid API key | 401/403 from API | Report error. Ask user to verify key. Do NOT retry with guessed keys. |
| Seedream timeout | No response in 300s | Retry once with same prompt. Still fails -> report with the prompt used so user can try manually. |
| No image in response | API returns empty data | Simplify prompt (remove extras), retry. Still empty -> report error. |
| Batch task fails | Exception during prompt assembly | Mark task as failed with error message. Continue remaining tasks. Report partial results at end. |
| Invalid garment type | User provides unknown type | Map to closest valid type or ask for clarification. Valid: dress/top/pants/jacket/suit/casual/default. |

### Degraded Mode: Prompt-Only (when image generation fails)

If Seedream API is unreachable or fails after retry, do NOT block the entire workflow.
**Skip image generation, still deliver prompt + SOP.** Mark output clearly:

```
[Note] Model image generation unavailable (API error). Prompt and SOP generated successfully.
Use your own model photo as @image2 when operating on the Jimeng platform.
```

This ensures the user gets the valuable prompt + SOP even without the AI-generated model image.

## Usage Example

**Input:** "帮我做一个女性穿搭视频，裙子类型，现代公寓场景"

**Resolved params:** gender=female, garment=dress, scene=modern_apartment, realism=40, style=realism, dialogue=natural, camera=vlog, audience=auto->female, duration=10, lang=zh

**Output 1 — Model Image:** 720x1280 PNG (asian_female_slim preset, realism=40)

**Output 2 — Seedance Prompt:**
```
一位面容和身材参考@图片2的年轻女性穿着@图片1中的服装，在简约现代的白色公寓客厅中，自然光从落地窗照入。她面朝镜头表情生动自然地展示服装，右手拉起裙摆展示面料（始终用右手），右手翻开裙摆内侧展示车线做工，小幅转身让裙摆飘动，右手捏腰部展示松紧设计，对着镜头说：「姐妹们你们快看...哇，不是，我真的没想到这条裙子上身效果这么好。你看这个面料，是那种...嗯...醋酸缎面的...（右手轻轻拉起裙摆展示）滑滑的凉凉的，而且有一定的厚度，不是那种廉价的薄纱感。然后你看这个车线...（右手翻开裙子内侧给镜头看）全部是包边走线的，没有毛边，做工真的很扎实。裙摆是A字的微微伞摆，你看我转一下...（转了一圈）你看它飘起来那个弧度，而且腰线这里有一个隐藏的松紧设计...（右手捏了捏腰部）不会勒但又收腰。你们猜多少钱？不到两百！超显腿长，闭眼入。」语气自然亲切，像在跟闺蜜视频通话。说话有停顿、有喘息、偶尔磕巴自我纠正，真实感强。Do not alter clothing pattern, color, texture or style. 手持vlog镜头感，竖屏9:16构图。音频要求：全程只有模特一个人的清晰人声，不出现第二个人的声音或对白。背景有符合场景的自然环境音，音量不超过人声的10%。视觉要求：全程保持中景到中近景，不要切到手部或脚部的特写镜头，避免手指变形问题。模特展示服装细节时始终使用右手操作，避免左右手切换导致的镜像翻转。全程画面中只有模特一人，不出现其他人物。
```

**Output 3 — Operator SOP:** Step-by-step for 即梦 platform (upload order, settings, quality checklist)

## Domain Knowledge Role Declaration

> The reference files contain dialogue scripts, model presets, API specs, and prompt templates.
> Their role is to **assist prompt assembly** — providing the raw materials that get composed into Seedance prompts.
> They do NOT replace the execution workflow. Never output reference content directly as the final answer.
> Always assemble through the workflow: collect params -> build prompt -> validate -> deliver.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/model-presets.md](references/model-presets.md) | 9 model presets, body params, 17-level realism anchors, scene/camera/style presets | Step 2: building model prompt |
| [references/seedream-api.md](references/seedream-api.md) | Seedream 4.5/5.0 API endpoint, request format, cost, crop logic | Step 3: calling API |
| [references/prompt-assembly.md](references/prompt-assembly.md) | Prompt composition order, multi-segment chaining constants, SOP templates | Step 4-6: assembling prompt and SOP |
| [references/dialogue-library.md](references/dialogue-library.md) | Complete dialogue scripts: 7 garment types x 2 genders x 2 languages (28 scripts total), openings, closings, actions | Step 4: composing dialogue content |

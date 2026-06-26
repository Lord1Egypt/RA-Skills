---
name: ark-video-storyboard
description: Generate a storyboard and prompts from a scene or reference images, confirm the script with the user, then optionally submit multi-segment video generation tasks to the Volcengine Ark video API. Use when the user wants to turn a scene idea into a structured video workflow, especially for mood films, product scenes, narrative shorts, or image-to-video prompt pipelines.
---

# Ark Video Storyboard

Turn a scene idea into a structured video plan, then optionally execute it with the Ark video generation API.

This skill is **confirmation-first**:
- First generate storyboard + prompts
- Let the user review and revise
- Only generate video after explicit user approval

## Workflow

1. **接收场景描述** — 用户描述视频场景（如"下班后去赛博朋克网吧打游戏"）
2. **询问参考图** — 用户描述场景后，主动询问："你有参考图吗？"（图片用于风格/人物参考）
3. **确认参考图角色** — 如果用户提供了参考图，询问："这张图是**背景/风格参考**还是**人物形象参考**？"
   - 背景/风格参考：作为环境、色调、氛围的视觉基准
   - 人物形象参考：作为主角外貌、着装、动作的基准
4. **确认人物描述** — 如果有多个视频片段且没有人物参考图，主动询问用户："这个视频里主角的人物描述是什么？"（如"东亚男性、黑色短发、穿白色T恤"），收集后在**每个段落提示词里保持完全一致**
5. **生成脚本** — 展开场景为更丰富的整体脚本，拆分为多个连贯段落
6. **输出分镜** — 每个段落包含：参考图用途说明、人物描述（多段一致）、画面描述，光照状态、连贯性备注、英文 AI 提示词（含参考图风格描述+一致的人物描述）
7. **用户确认** — 展示分镜给用户确认："这是不是你要的脚本/提示词？"
8. **修改** — 用户如需调整（风格、节奏、镜头语言、人物细节、提示词措辞），修改后重新展示
9. **执行确认** — 用户确认后，询问"是否开始生成视频？"
10. **提交 API** — 用户明确说"可以/开始生成"后，提交给 Ark API，逐段轮询结果，下载视频
11. **合并并发送** — 所有片段下载完成后，用 ffmpeg 合并为一个完整视频，检查大小（飞书限制约 20MB），必要时压缩，通过飞书发送给用户

## 视频合并与发送流程

所有片段下载完成后，按以下步骤合并并发送给用户：

### 第一步：定位片段目录

Ark API 下载的视频片段默认保存在 `~/.openclaw/media/{timestamp}/`，按时间戳组织。确认目录存在：

```bash
ls ~/.openclaw/media/{timestamp}/seg*.mp4
```

### 第二步：合并视频

1. **创建片段列表文件**

```bash
cd ~/.openclaw/media/{timestamp}/
echo "file 'seg1.mp4'\nfile 'seg2.mp4'\n..." > concat.txt
```

> seg 序号与片段数量一致，逐行追加。

2. **执行合并**

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy merged.mp4
```

3. **验证**

```bash
ls -lh merged.mp4
ffprobe -v quiet -print_format json -show_format merged.mp4
```

### 第三步：检查大小并压缩（如需要）

飞书直接发送限制约 **20MB**：

- **≤20MB**：直接使用 `merged.mp4`
- **>20MB**：压缩后再发

```bash
ffmpeg -i merged.mp4 \
  -c:v libx264 \
  -crf 28 \
  -c:a aac \
  -b:a 128k \
  -y merged_compressed.mp4
```

### 第四步：发送至飞书

使用 `message` 工具发送文件：
- `filePath`: `~/.openclaw/media/{timestamp}/merged_compressed.mp4`
- `channel`: `feishu`
- `message`: 告知用户视频已合并完成，共多少片段，时长多少

### 第五步：更新工作流记录

在 `~/.openclaw/workspace/WORKFLOW.md` 中记录本次处理信息（时间戳、片段数量、输出文件路径、文件大小）。

## 人物一致性规则（关键）

如果视频有多个片段，且用户没有提供人物参考图，则：
- 在步骤4中主动询问人物描述
- 在**每个段落的提示词里保持完全相同的人物描述**（外貌、发型、着装等措辞必须一字不差）
- 人物描述格式示例：`East Asian young man, black short hair, white T-shirt, 25 years old`

如果用户提供了**人物参考图**，则每个提示词里统一写：`consistent with the character in reference image`

## Interaction Phases

### Phase 1: Script / Prompt Confirmation
- User gives the scene, style, references, and goal.
- **If images are provided, first confirm whether each one is a background/environment reference or a character/subject reference.**
- If multiple segments and no character reference image, ask for a consistent character description.
- Generate the storyboard, segment plan, and English prompts first.
- Ask the user whether this version is correct.
- If the user asks to tweak tone, pacing, camera language, subject details, prompt wording, or image-role interpretation, revise and show the updated version again.
- Do **not** call the Ark API in this phase unless the user explicitly asks for direct generation.

### Phase 2: Execution Confirmation
- After the user confirms the script/prompt is correct, ask whether to start generation if they have not already made that explicit.
- Only run the API submission / polling / download flow after explicit approval.
- If submission fails, immediately report the exact stage and error.

## Input Requirements

Collect as many of these as possible before writing prompts:

- **Reference image or images（主动询问用户是否有参考图）**
- Scene description
- Subject or product
- Target style (cinematic, cozy, commercial, dreamy, realistic, etc.)
- Intended use (ad, social clip, atmosphere film, storytelling, product demo)
- Constraints such as camera language, pacing, lighting, or ending mood
- Total duration target
- Segment count target
- **Consistent character description（多段无人物参考图时必须收集）**

If inputs are incomplete, still proceed with reasonable defaults and clearly state the assumptions.

## Hard Rules

- Default all human characters to **East Asian / 东方亚洲人** unless the user explicitly specifies otherwise.
- All segments must belong to the **same video**, not unrelated clips.
- Maintain continuity for character appearance, wardrobe, environment, props, lighting logic, and emotional progression.
- Write the planning fields in Chinese unless the user requests another language.
- Write the final generation prompts in English unless the user explicitly wants Chinese prompts.
- Prefer cinematic, visual, action-oriented prompts over abstract descriptions.
- Do not silently retry failed API submissions in the background without telling the user.

## Segment Output Format

Follow the schema in `references/storyboard-schema.md`.

At minimum include:
- Segment index
- Duration seconds
- Character description (same across all segments)
- Visual description
- Lighting state
- Continuity notes
- English AI prompt (includes consistent character + reference style)

## Prompt Construction Rules

When writing a segment prompt, include the details that matter most for video generation:

- Subject identity and appearance (**consistent character description, same in every segment**)
- Camera angle or shot type
- Motion or action
- Scene and environment
- Lighting and mood
- Pacing or motion quality
- Style words only when they improve consistency
- **Reference image style description** (if provided by the user, e.g., "in cyberpunk neon city style per reference image")
- **For all segments of the same video: character description must be IDENTICAL**

## Sequence Design Rules

Use this narrative rhythm by default unless the user asks for a different structure:

- Segment 1: establish subject, place, and mood
- Segment 2: deepen action or environment interaction
- Segment 3: push visual/emotional peak or transition
- Final segment: resolve, land, or fade out with a clear ending image

For more than 4 segments, insert additional deepen / transition beats while preserving continuity.

## Duration / Segment Logic

This skill should support **dynamic segment splitting**.

Examples:
- 60 seconds ÷ 4 segments = 15 seconds each
- 60 seconds ÷ 6 segments = 10 seconds each
- 60 seconds ÷ 12 segments = 5 seconds each

Current validated Seedance 1.5 Pro rule from user-confirmed testing:
- `duration` must be an integer in the range **[4, 12]**

So before execution:
1. Compute `duration = total_duration_seconds / segment_count`
2. Ensure the result is an integer
3. Ensure the result is within **4~12**
4. If not, stop and explain the issue to the user before submitting

## API Execution

API key loading order for actual generation:
1. Explicit wrapper argument if one is added later
2. Environment variable `ARK_API_KEY`
3. `~/.openclaw/openclaw.json` → `skills.entries.ark-video-storyboard.apiKey`
4. Backward-compatible old format: `skills.ark-video-storyboard.apiKey`

If the user wants actual generation, read `references/api.md` and use the scripts:

- `scripts/build_storyboard.py` to assemble structured segment data
- `scripts/run_full_generation.py` to sequentially submit segments, poll each task, collect `video_url`, and optionally download videos
- `scripts/submit_segment.py` to submit one segment at a time
- `scripts/get_task_result.py` to query a task once and extract `video_url`
- `scripts/poll_task_until_done.py` to poll until completion and return `video_url`
- `scripts/download_video.py` to download a finished `video_url` to local storage

Submit segments **sequentially**, not in parallel, unless the user explicitly asks otherwise.

## Current Known Ark Payload Requirements

Current known request requirements include:
- `model`
- `content` (first item is the text prompt)
- `ratio`
- `duration`
- `watermark`
- Reference image: use `{"type": "image_url", "image_url": {"url": "<data_uri or url>"}}` in content array

Current validated model in this workspace:
- `doubao-seedance-1-5-pro-251215`

## Error Handling Rule

If API submission fails, returns any model / parameter / schema error, or returns no valid `task_id`:
- Stop immediately
- Tell the user the exact failing segment and stage
- Show the key error message
- Explain which parameter or payload assumption most likely caused it
- Do not pretend generation is still running
- Do not continue to later segments

If API submission succeeds and returns a valid `task_id`:
- Continue to the next segment by default without interrupting the user for each success
- Do not notify the user for each successful segment submission
- After all segments are successfully submitted, send one consolidated update that all tasks are in the Ark queue and generation is underway

## Example Shape

A good segment should look like this:

- 人物描述：东亚男性，黑色短发，白色T恤（所有段落一致）
- 参考图用途：背景/风格参考（温馨卧室，城市夜景窗外，暖色灯光）
- 画面描述：描述主体、动作、构图，环境变化
- 光照状态：明确亮度，主光、轮廓光、氛围变化
- AI 提示词：人物描述 + 镜头 + 动作 + 光线 + 情绪，提示词末尾加参考图风格描述

See `references/examples.md` for a concrete sleeping-scene example.

## When To Read References

- Read `references/storyboard-schema.md` before generating structured segments.
- Read `references/prompt-rules.md` when you need guardrails for prompt quality or continuity.
- Read `references/api.md` before building or submitting API payloads.
- Read `references/examples.md` when the user wants output that matches the example style.

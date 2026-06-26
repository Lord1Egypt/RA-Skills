---
name: idea2video
version: 1.2.0
description: Turn a user's idea into the full pipeline: **story → characters → 3-view portraits → scenes → shots → keyframes → shot videos → concat**. First emit a **plan template** for the user to confi
triggers:
  - Idea → Video Generation Plan
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@latest","installAlternative":"npx @dlazy/cli@latest","homepage":"https://github.com/dlazyai/cli","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"当你需要使用此技能时，请严格遵循此技能提供的指南进行规划和执行。你可以通过调用 dlazy CLI 的各类生成模型（如 dlazy seedream-4.5 等）来完成实际的图片渲染。注意：Windows PowerShell 中不允许使用 `&` 或 `&&` 进行命令串联或后台运行，请单独且同步地执行命令。"}}
---

## 身份验证 (Authentication)

所有请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

```bash
dlazy login
```

该命令使用设备码流程（远程终端也可用），登录成功后 **自动把 API key 写入本地 CLI 配置**，无需手动复制粘贴。

### 备选：手动设置 API Key

如果你已有 API key，也可以直接保存：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`），文件权限仅限当前操作系统用户访问。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 手动获取 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个 key 都属于你自己的 dLazy 组织，可在同一控制面板**随时轮换或吊销**。

## 关于与来源 (Provenance)

- **CLI 源代码**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@latest <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@latest`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。

# Idea → Video Generation Plan

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Turn a user's idea into the full pipeline: **story → characters → 3-view portraits → scenes → shots → keyframes → shot videos → concat**. First emit a **plan template** for the user to confirm, then **expand it into canvas shapes** and call `drawToCanvas`.

## Workflow Overview (5 states)

Every reply must start with this line:

- `**Current State:** [state] | **Next:** [goal]`

| State                    | Goal                                   | Needs user confirmation |
| ------------------------ | -------------------------------------- | ----------------------- |
| 1. Requirement gathering | Lock idea / audience / style / scale   | ✅                      |
| 2. Plan generation       | Build plan template; show node summary | ✅ (strict gate)        |
| 3. Plan adjustment       | Patch the template per user feedback   | ✅                      |
| 4. Canvas expansion      | Expand template into flat shapes       | ❌ (internal)           |
| 5. Apply to canvas       | Call `drawToCanvas` to write shapes    | ❌                      |

## State 1: Requirement Gathering

Collect these inputs; ask if any is missing:

- `idea` — the core creative seed (one sentence to one paragraph)
- `user_requirement` — audience / runtime / max scenes / max shots (optional)
- `style` — visual style ("realistic warm", "cyberpunk", "watercolor 2D"...)
- `aspectRatio` — defaults to `16:9`; alternatives `9:16` / `1:1`
- `sceneCount` — let the model decide by default, but disclose
- `shotsPerScene` — let the model decide by default

Output a bulleted requirement list, ending with:

- `<suggestion>Requirements ready — confirm to enter plan generation?</suggestion>`

## State 2: Plan Generation

Build a plan template per the **Plan Template Schema** (see Appendix A).

Construction rules:

1. **Strictly use models registered in `config/models/`**. Recommended for idea2video:
   - `qwen3_6-plus` — every LLM step (story / characters / script / storyboard / shot decomposition)
   - `banana-pro` — character 3-view portraits, shot first/last frames
   - `veo_3_1-fast` — shot videos (i2v)
   - `merge` — video concatenation
2. **Mirror the canonical 7-segment idea2video structure** (Appendix B):
   - `develop_story` (LLM)
   - `extract_characters` (LLM, parse=json)
   - `portraits` (map: front → side/back)
   - `write_script` (LLM, parse=json)
   - `scenes` map (with nested `shots` map)
     - `storyboard` (LLM, parse=json)
     - `shots` map: `shot_desc` → `first_frame` → `last_frame`(when) → `shot_video`
     - `scene_concat` (merge)
   - `final_video` (merge)
3. **Reference rules** (critical, do not get wrong):
   - Whole-text injection of an upstream → `promptRefs: ["$node.X"]`; **do not** inline `shape://` inside `prompt`.
   - Sub-field injection from upstream JSON → keep `{{$node.X.json.field}}` placeholder inside `prompt`.
   - Media references (image/video/audio) → put in `images` / `videos` / `audio` arrays; values use `$node.X` or `shape://shape:X`.
   - Cross-iteration aggregation inside a map → `$node.<mapId>[*].<bodyId>` (e.g. `$node.portraits[*].front`).
   - Inside a map, current item is `$item`, index is `$idx`; nested maps access outer index via `$ctx.<outerMapId>.idx`.
4. **Do not paraphrase tool prompts** — keep field names aligned with each model's `inputSchema`.
5. **`when` for conditional nodes** (e.g. `last_frame` only when `variation_type ∈ {medium, large}`):

   ```json
   "when": { "$in": ["$node.shot_desc.json.variation_type", ["medium", "large"]] }
   ```

When presenting to the user, **summarize in plain language**, do not expose raw JSON:

```
The plan will create X nodes:
  · 1 story node
  · 1 character-extraction node
  · Character 3-views (front + side + back, expanded per character)
  · 1 scenes node
  · Per scene: 1 storyboard node + N shots (each shot = shot description + first frame + [last frame] + video) + 1 concat node
  · 1 final concat node

Models:
  · LLM: qwen3_6-plus
  · Image: banana-pro
  · Video: veo_3_1-fast
  · Concat: merge
```

End with:

- `<suggestion>Plan ready — confirm to expand to canvas? Or tell me what to adjust.</suggestion>`

## State 3: Plan Adjustment

Common requests:

- Swap a model ("use doubao-seedream-4_5 for image")
- Change structure ("drop the last-frame branch", "add a narration audio node")
- Change scale ("limit to 1 character", "fix 3 shots per scene")

Patch the template, re-summarize, wait for explicit confirmation again.

## State 4: Canvas Expansion (internal)

Expand the plan template into a **flat shape list** suitable for `drawToCanvas`.

### Expansion rules

1. **`tool` node → 1 shape**:
   - Shape `type` is determined by the model's output type:
     - `qwen3_6-plus` → `text`
     - `banana-pro` / `doubao-seedream-*` → `image`
     - `veo_*` / `doubao-seedance-*` / `kling-*` → `video`
     - `merge` → `video` (or `audio` if merging audios)
   - `shape.id` = `shape:<templatePath>` or `shape:<templatePath>__i<iter>` (inside a map)
   - `shape.props.model` = template `model`
   - `shape.props.input` = template `input`, with all `$node.X` / `$item.X` / `{{...}}` resolved to literals or `shape://shape:Y` whenever possible
   - `shape.props.input.promptRefs` is built from template `promptRefs`: each `$node.X` → `shape://shape:X`
   - `shape.parentId` = enclosing frame shape id (when inside a map)
   - `shape.meta.fromTemplateId` = the dotted template path (e.g., `scenes.shots.first_frame`)
2. **`map` node → 1 frame shape + body subtree per iteration**:
   - frame `type: "frame"`, `props.name` = the map's `name`
   - frame itself runs no model
3. **Skip nodes whose `when` is false**. If `when` references an upstream not yet completed (e.g. `shot_desc.json.variation_type`), **expand optimistically**: still emit the shape with `status: "pending"`; the runtime expander will reconcile after upstream completes.
4. **Unresolved `{{$node.X.json.field}}` placeholders** stay in the prompt string (status `pending`). Do not substitute placeholder text.
5. **Coordinates `(x, y, w, h)` are not part of the plan** — compute at `drawToCanvas` time:
   - Lay out columns along data flow; 800px column gap.
   - Stack same-column nodes vertically with 100px gap.
   - Frame size = bounding box of children + 100px padding.
   - Map children: horizontal vs. vertical follows `direction`.
   - Default sizes: text 600×400, image 1600×900 (16:9) or 1024×1024 (1:1), video 1600×900, frame auto.

## State 5: Apply to Canvas

Call `drawToCanvas` with `createShapes` = the expanded shape list.

Pre-flight checks before the call:

- Every shape's `props.input` validates against the corresponding model's `inputSchema` (drawToCanvas re-checks; pre-checking saves a round-trip).
- Every `shape://shape:X` reference points to an X present in the same `createShapes` payload.
- Frames appear before children (`parentId` exists).

After success, reply:

```
✅ Plan added to canvas (N nodes, M pending).
Click "Run Workflow" on the canvas to execute the whole pipeline.
```

---

## Appendix A: Plan Template Schema (for construction)

Top level:

```json
{
  "version": 1,
  "name": "idea2video",
  "inputs": { "idea": {...}, "user_requirement": {...}, "style": {...} },
  "output": "$node.final_video.url",
  "nodes": [ /* tool or map nodes */ ]
}
```

Nodes:

```jsonc
// tool node
{
  "id": "<unique>",
  "kind": "tool",
  "model": "<id registered in config/models>",
  "name": "<display name; may use {{$item.X}} / {{$idx}} templates>",
  "parse": "json",                  // optional — url contains JSON
  "when": { "$in": [...] },        // optional — conditional node
  "input": {
    "prompt": "...containing {{$node.X.json.field}} placeholders...",
    "promptRefs": ["$node.upstream"],  // whole-text injection
    "images": ["$node.front"],       // media references
    "imageSize": "1K",
    ...
  }
}

// map node
{
  "id": "<unique>",
  "kind": "map",
  "name": "<frame name>",
  "over": "$node.upstream.json",   // must resolve to an array
  "mode": "parallel" | "sequential",
  "direction": "horizontal" | "vertical",
  "body": [ /* child template nodes */ ]
}
```

## Appendix B: Canonical idea2video Structure

Assemble the plan with this fixed shape:

1. `develop_story` — qwen3_6-plus; prompt uses `{{$input.idea}}` and `{{$input.user_requirement}}`
2. `extract_characters` — qwen3_6-plus; `parse: "json"`; `promptRefs: ["$node.develop_story"]`
3. `portraits` — map(over=`$node.extract_characters.json`, parallel, horizontal)
   - body: `front` → `side (images:[$node.front])` → `back (images:[$node.front])`
4. `write_script` — qwen3_6-plus; `parse: "json"`; `promptRefs: ["$node.develop_story"]`
5. `scenes` — map(over=`$node.write_script.json`, sequential, vertical)
   - body:
     - `storyboard` — qwen3_6-plus; `parse: "json"`; `promptRefs: ["$node.extract_characters"]`
     - `shots` — map(over=`$node.storyboard.json`, parallel, vertical)
       - body:
         - `shot_desc` — qwen3_6-plus; `parse: "json"`; `promptRefs: ["$node.extract_characters"]`
         - `first_frame` — banana-pro; prompt with `{{$node.shot_desc.json.ff_desc}}`; `images: $node.portraits[*].front`
         - `last_frame` — banana-pro; `when: variation_type ∈ {medium, large}`; `images: [$node.first_frame]`
         - `shot_video` — veo_3_1-fast; prompt with `{{$node.shot_desc.json.motion_desc}}` and `{{$node.shot_desc.json.audio_desc}}`; `images` includes first_frame (+ last_frame if present)
     - `scene_concat` — merge; `videos: $node.shots[*].shot_video`
6. `final_video` — merge; `videos: $node.scenes[*].scene_concat`

## Output Norms

- Never expose raw plan JSON, shape JSON, or `taskId` to the user — summarize with bullets.
- If `drawToCanvas` fails (usually input not matching the model's schema), explain why and propose a fix.
- Strict gates: states 2 and 3 must wait for an explicit "confirm / continue / proceed" before advancing.

## 🛠️ 执行与生成指南 (CRITICAL EXECUTION INSTRUCTIONS)

**你是可以执行终端命令的智能 Agent！**

**【严格禁止行为】**

- 严禁：将提示词保存到任何文件中（如 txt, md）。
- 严禁：要求用户自己去第三方平台（如 Midjourney）生成图片。
- 严禁：一次性批量生成所有图片，或一次性执行多个命令。

**【必须遵循的交互与执行流程】**
你必须**严格分步**执行，并在每一步停下来等待用户回复：

1. **第一步：主动收集需求**。当用户提出需求时，不要做任何设计和生成，先向用户提问（如产品特点、目标人群、想要几张图等）。**必须等待用户回答。**
2. **第二步：输出草案并请求确认**。根据用户的回答，制定套图计划，并输出**第一张图**的提示词草案。**询问用户：“是否确认这个提示词，可以开始生成第一张图了吗？” 必须等待用户回答“确认”。**
3. **第三步：单次执行终端命令**。用户确认后，你**必须使用终端执行命令**（如 `dlazy seedream-4.5 --prompt "..."`），每次只能执行一个生成命令。**重要：必须使用同步命令，绝不要在命令末尾加 `&`，绝不要使用 `&&`，这是在 Windows PowerShell 下运行！**
4. **第四步：交付与循环**。命令返回结果后，把图片 URL 发给用户，并询问“对这张满意吗？我们可以继续生成下一张了吗？”。收到确认后再继续下一步。

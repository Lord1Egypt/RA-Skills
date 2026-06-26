---
name: image-social-carousel
version: 1.2.0
description: A structured workflow skill dedicated to social-media carousel design. The core method is 'decide intent first, then execute,' using a 'single-confirmation + cover-first' two-phase flow.
triggers:
  - Social Carousel Designer (Cover-First)
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@latest',
        'installAlternative': 'npx @dlazy/cli@latest',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw':
      {
        'systemPrompt': '当你需要使用此技能时，请严格遵循此技能提供的指南进行规划和执行。你可以通过调用 dlazy CLI 的各类生成模型（如 dlazy seedream-4.5 等）来完成实际的图片渲染。注意：Windows PowerShell 中不允许使用 `&` 或 `&&` 进行命令串联或后台运行，请单独且同步地执行命令。',
      },
  }
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

# Social Carousel Designer (Cover-First)

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A structured workflow skill dedicated to social-media carousel design. The core method is "decide intent first, then execute," using a "single-confirmation + cover-first" two-phase flow.

## Core Positioning

Your responsibilities:

- ✅ Design decisions (what to do, why)
- ✅ Structured intent data output
- ❌ Image-generation prompt rendering details

## Execution Framework

### Step 0: Task Planning (Mandatory)

Before any design output, call the `write_todos` tool to set up a task plan that includes at least:

- Direction confirmation and slide planning
- Cover-first generation and confirmation
- Batch generation of remaining slides
- Rework handling and consistency convergence

Execution rules:

- Keep only one task `in_progress`; the rest are `pending`.
- Update `write_todos` status as soon as each phase finishes.
- If the user asks for rework or new assets, add or re-order tasks and re-enter the corresponding phase.

### Phase 1: Direction Confirmation + All Slides (single confirmation)

This phase must accomplish:

1. Establish visual references
   - When the user provides a style reference image, use it directly.
   - Otherwise, use `search_image` to find a suitable visual reference.
2. Output a confirmation table that includes at least:
   - Platform and slide count
   - Each slide's role, headline, subheadline
   - Reference-image list
   - Technical details (platform spec, target audience, narrative flow, etc.)
3. Wait for the user's single confirmation.
   - Only after the user explicitly says "ok / go / continue" may you enter Phase 2.

### Phase 2: Cover-First Generation (5 steps)

#### Step 1: Analyze Reference Image (planner executes — never delegate)

- Use `analyse_image` to extract design structure.
- Focus on these structural dimensions:
  - Color strategy
  - Typography hierarchy
  - Background materials (halftone, grain, gradient, etc.)
  - How elements blend with the background (overlay / texture-shaped / semi-transparent)
  - Spatial composition
  - Texture quality of key elements (photoreal 3D, flat vector, sculptural, etc.)
- Output 3–6 structural patterns. Describe structure and technique only — no mood words.

#### Step 2: Map Content to Structure

- Map each slide's content to the structural patterns from Step 1.
- Preserve quality tier — do not downgrade high-quality forms.
- Replace the reference image's specific content fully to avoid contamination.
- Keep element-background blending technique consistent.

#### Step 3: Generate the Cover (Slide 1 only — delegable)

- Use Step 1's structural analysis + Step 2's content mapping + the reference URL.
- Task type must be `REFERENCE_TO_IMAGE`.
- The prompt must explicitly include compositional technique, blending method, and spatial composition.
- Default resolution: platform aspect ratio + 1K; only escalate when the user explicitly asks for more.
- After showing the cover, ask:
  - "Does this cover look right? I'll generate the rest to match this style."
- Stop and wait:
  - Approval → proceed to Step 4
  - Rejection → return to Steps 1–3 and iterate

#### Step 4: Analyze the Approved Cover (planner executes — never delegate)

- Use `analyse_image` to identify two element classes:
  - Visual anchors (must keep): palette, typography style, user assets
  - Flexible elements (should vary): layout composition, background imagery, decorative elements
- The goal is "same family, different personalities," not "same template, swap text."

#### Step 5: Generate Remaining Slides (2–N — delegable)

- The cover URL must be the actual output URL from Step 3.
- Pass the cover URL into both `project_context` and `image_url_list`.
- Stop passing the original style reference — the cover has absorbed its structural traits.
- Every generation call uses `REFERENCE_TO_IMAGE`, with the cover URL in `image_url_list`.
- Resolution stays consistent with Step 3: default platform aspect ratio + 1K.

## Platform Spec Reference

| Platform        | Aspect Ratio | Safe Area (top / bottom) |
| --------------- | ------------ | ------------------------ |
| TikTok          | 9:16         | 15% / 25%                |
| Instagram Feed  | 4:5          | 10% / 10%                |
| Instagram Story | 9:16         | 15% / 25%                |
| Xiaohongshu     | 3:4          | 8% / 20%                 |
| LinkedIn        | 1:1          | 5% / 5%                  |

## 10 Core Rules

1. Single confirmation: after Phase 1 finishes, get one user confirmation before generating.
2. No fabrication: do not add ungiven columns, invent assets, or invent style words.
3. Visual references prefer user assets — only search when those are missing.
4. Cover-first execution: follow Steps 1–5 strictly.
5. If user assets are provided, include them in every call.
6. Starting from the second call, drop the original style reference; keep only user assets + the approved cover.
7. Minimize text content from the second call onward — keep only headline and subheadline.
8. Output suggested tags as displayed; do not append extra internal tags.
9. Every generation call uses the reference-image flow, with prompts that include the structural analysis.
10. Default resolution is always platform aspect ratio + 1K, unless the user explicitly requests higher.

## Reference-Image Usage Guidelines

The correct approach is to extract the reference image's design structure and map new content into that structure.

Core principles:

- Describe "how it's built": compositional technique, spatial structure, material quality, blending method.
- Avoid letting "feeling words" dominate: minimize style adjectives and mood words.
- Let the reference image carry the main style information; the text only enforces structural constraints.

## Output Format

- Phase status (current phase and step)
- Direction confirmation table (Phase 1)
- Current deliverable (cover or remaining-slides plan)
- Next item awaiting confirmation
- Current todo status (phase, completed, pending)

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

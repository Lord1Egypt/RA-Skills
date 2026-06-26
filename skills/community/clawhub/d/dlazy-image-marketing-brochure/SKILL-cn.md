---
name: image-marketing-brochure
version: 1.2.0
description: A complete workflow skill for marketing brochure design, covering everything from requirements gathering, layout design, to mock-up delivery. It uses a 'layout-first + mandatory confirmation
triggers:
  - Marketing Brochure Designer (Layout-First)
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
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
npx @dlazy/cli@1.2.0 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.0`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。

# Marketing Brochure Designer (Layout-First)

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A complete workflow skill for marketing brochure design, covering everything from requirements gathering, layout design, to mock-up delivery. It uses a "layout-first + mandatory confirmation gate" mechanism to reduce rework risk.

## Core Positioning

Applicable scenarios:

- Corporate brand brochures, product introduction booklets
- Event flyers, service description folds
- Investment brochures, enrollment guides, project portfolios

Core deliverables:

- Layout design: full unfolded artwork (interior view + exterior view)
- Folded mock-up: rendering that simulates the actual folded state
- Lifestyle mock-up: real-world usage shots (held in hand, environment, etc.)

## Step 0: Task Planning (Mandatory)

Before any output, call `write_todos` to set up a task plan that includes at least:

- Requirements alignment and fold-type confirmation
- Layout design generation and iteration
- Layout confirmation gate and mock-up output
- Lifestyle mock-up generation and final delivery

Execution rules:

- Only one task may be `in_progress` at a time; the rest are `pending` or `completed`.
- Update `write_todos` status as soon as each phase finishes.
- When the user asks for rework or new assets, add or re-order tasks and return to the corresponding phase.

## Adaptive Execution Flow

Drive the work forward dynamically based on the request type:

| Request Type  | Execution Flow                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Full brochure | Confirm fold type and content framework → produce layout → user confirms → export mock-ups                              |
| Single page   | Generate the requested page first → suggest filling in the missing pages to form a complete piece                       |
| Vague request | Clarify the fold type first (tri-fold / bi-fold / Z-fold, etc.) → then proceed                                          |
| Mock-up only  | Check whether a confirmed layout already exists; if not, produce and confirm the layout first, then output the mock-ups |

Critical gate:

- Once the layout is generated, you must wait for the user's explicit approval before moving on to mock-up production.

## Brochure Types and Output Specs

### Tri-Fold (most common)

- Output: 6 panels (3 exterior + 3 interior)
- Use cases: product introduction, service overview, corporate promotion

### Bi-Fold

- Output: 4 panels
- Use cases: event programs, menus, brief introductions

### Z-Fold

- Output: 6 panels unfolded in sequence
- Use cases: step-by-step guides, timelines, process descriptions

### Gate-Fold

- Output: 4+ panels with a dramatic central reveal
- Use cases: premium launches, luxury brands

### Accordion Fold

- Output: 6–8 panels unfolded progressively
- Use cases: maps, extended timelines

### Saddle-Stitched Booklet

- Output: 8+ pages bound into a booklet
- Use cases: product catalogs, annual reports

## Tri-Fold Delivery Standard (default example)

The layout must include:

- Exterior view (folded state): back panel → cover → inner flap
- Interior view (unfolded state): inner left → inner middle → inner right

Recommended content distribution:

| Panel        | Core Content                           |
| ------------ | -------------------------------------- |
| Cover        | Logo, hero visual, headline            |
| Inner flap   | Brief introduction, suspense hook      |
| Inner left   | Company story, background info         |
| Inner middle | Core value proposition, key advantages |
| Inner right  | Product features, call to action       |
| Back panel   | Contact info, social links, copyright  |

## Image Generation Specs

Default aspect ratio: 4:3

### Step 1: Layout Design (must be completed first)

1. Search for brochure styling references that match the user's request and feed them in as layout inputs.
2. Generate the full unfolded layout (interior + exterior) as the single source of truth for every downstream mock-up.
3. The interior-view prompt must include these structural keywords:
   - No background
   - No white border
   - Flat 2D
   - Edge-to-edge
   - No perspective shadow or margin
   - All three panels in a single image, filling the canvas

### Step 1.5: User Confirmation (mandatory gate)

- Show the layout and ask explicitly:
  - "Does this layout meet your requirements? I'll move on to mock-ups once you confirm."
- If the user requests changes: return to Step 1 and iterate until they approve.
- Only after explicit approval may you proceed to Step 2.

### Step 2: Folded Mock-Ups (requires Step 1 approval)

Based on the approved layout, output:

- Standing: Z-folded standing on a white surface, cover prominent
- Flat-laid: partially unfolded, top-down view
- Stacked: 2–3 brochures stacked at varied angles

### Step 3: Lifestyle Mock-Ups (based on Step 1)

Based on the approved layout, output:

- Held in hand: first-person POV, brochure open in hand
- Lifestyle: third-person POV, mid-close shot of someone reading
- Environment: placed on a reception desk, booth, or public space

Consistency requirements:

- When generating Step 2 and Step 3 images, you must feed the approved layout in as a reference image.
- The fold type must stay consistent (a tri-fold layout can only produce tri-fold mock-ups).

## Key Design Parameters

Color rules:

- Follow the 60-30-10 color rule
- Cover prefers the brand primary color
- The CTA uses the accent color

Mandatory information:

- The back panel must include the copyright notice and contact info
- Regulated industries should include compliance disclaimers

## User Alignment Question Templates

Before generating, prefer to align on:

- "Which fold type do you need? Tri-fold is the most common choice and fits most scenarios."
- "What's the brochure's main purpose? (Product promo / company intro / event)"
- "Which information do you want to highlight? I can plan content distribution per panel."
- "Do you have ready-made copy, or should I draft from a description?"
- "Any brand colors or reference designs? You can upload images so I understand your style preference."
- "Overall style preference: minimal corporate / energetic / premium luxury?"
- "I'll generate the layout first and only move to mock-ups after your confirmation — does that work?"

## Iterative Improvement Guidance

When the user is unsatisfied, lead with these questions to locate the change:

- "Which panel needs adjustment — cover / interior / back?"
- "Is it mainly the color palette, layout, or content expression?"
- "Can you describe the desired outcome or upload a reference image?"

## Execution Strategy Summary

- Plan before execute: lock in fold type and content framework first.
- Layout-first principle: every mock-up must be based on the approved layout.
- Mandatory confirmation gate: do not enter the mock-up phase before layout approval.
- Reference consistency: mock-up generation must reference the approved layout to ensure visual unity.

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

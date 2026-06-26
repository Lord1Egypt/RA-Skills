---
name: image-storyboard
version: 1.2.0
description: A professional storyboard skill for film, advertising, short video, and educational narrative scenarios, built around a strict 'plan first, render later' flow.
triggers:
  - Storyboard Workflow Director
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

# Storyboard Workflow Director

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A professional storyboard skill for film, advertising, short video, and educational narrative scenarios, built around a strict "plan first, render later" flow.

## Core Positioning

Turn user creative briefs into industry-grade storyboards across two main pipelines:

- Cinematic storyboards: film, advertising, shorts
- Narrative storyboards: educational content, comic-style narrative

## Step 0: Task Planning (Mandatory)

Before any execution, set up a task plan that includes at least:

- Requirements exploration and tech-spec lock-in
- Character design and character master sheet confirmation
- Script structuring and script-gate confirmation
- Image generation and batched delivery
- Final storyboard assembly and export

Execution rules:

- Only one task may be `in_progress` at a time; the rest are `pending` or `completed`.
- Update the task plan as soon as each state finishes.
- When the user asks to roll back or rework, add or re-order tasks and return to the corresponding state.

## Technical Specification System

### 1) Cinematic Storyboards (Film / Ad / Short)

- Aspect ratios: 16:9, 2.35:1, 9:16, etc.
- Required metadata:
  - Shot size (close-up, medium, wide, etc.)
  - Camera movement (push, pull, pan, dolly, tracking)
  - Lighting and color temperature

### 2) Narrative Storyboards (Education / Comic)

- Aspect ratios: comic or vertical-narrative standards
- Required metadata:
  - Sequence markers (e.g., S01-P03)
  - Mood tags (tense, warm, relieved, etc.)

### 3) Character Master Sheet

- Visual standard: clean full-body reference, no text, frames, or UI elements
- Style fit:
  - Cinematic projects prefer photoreal style
  - Narrative projects prefer 2D or sketch styles
- Core elements:
  - Identity, age, vibe
  - Appearance, costume details, key accessories
- Generation formula:
  - `[subject] + [character traits] + [tech specs] + [style] --no text`

### 4) Script Structure Format

Every storyboard panel must output in this structure:

- Visual prompt: [subject/character] + [action/interaction] + [environment/scene]
- Tech params: [shot size, camera, lighting, etc.]
- Text/logic: [narrative or logic elements]
- Status: [pending / generated]

### 5) Delivery Spec (final storyboard)

- Paper size: A4 landscape (297mm × 210mm)
- Output: print and PDF export
- L1 layout (vertical film strip, cinematic): black background, single column
- L2 layout (comic grid, narrative): white background, thick borders, caption boxes, step markers

## Standard Workflow (4 states)

Every reply must start with:

- `**Current Step:** [state] | **Next:** [goal]`

### State 1: Requirements Exploration and Validation

Goal: lock in tech specs and the style guide.

Execution requirements:

1. Analyze the user's input and fill in missing info.
2. Determine aspect ratio, panel count, and category (cinematic or narrative).
3. Output as a bulleted list, not a table.
4. Wait for the user's explicit "continue" or "confirm."

Suggested prompt:

- `<suggestion>The specs are organized — confirm to proceed to the character design phase?</suggestion>`

### State 2: Character Design (Visual Bible)

Goal: lock in character appearance to prevent later drift.

Execution requirements:

1. Build the character visual bible: appearance, costume, accessories, posture baseline.
2. Generate and present a single character master reference image.
3. Output as a bulleted list.
4. Strict gate: you must wait for character approval before entering the script phase.

Suggested prompt:

- `<suggestion>Character look is locked — start the storyboard script?</suggestion>`

### State 3: Storyboard Production (Script and Visuals)

#### Phase 1: Script Writing (think)

- Convert the narrative into a structured script.
- Output as a bulleted list.
- Strict gate: do not generate images until the script is approved.

## Output Requirements

- Use bulleted lists, not tables (except for the delivery layout spec).
- Clearly mark current state, completed items, and items awaiting confirmation.
- All critical gate nodes must wait for user confirmation before continuing.

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

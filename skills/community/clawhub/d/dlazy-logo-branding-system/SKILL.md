---
name: dlazy-logo-branding-system
version: 1.2.3
description: A professional pipeline for building everything from a core mark to a complete brand visual system, ensuring creative quality, execution consistency, and shippable delivery.
triggers:
  - Logo & Branding Professional Design System
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://github.com/dlazy-ai/cli","source":"https://github.com/dlazy-ai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"当你需要使用此技能时，请严格遵循此技能提供的指南进行规划和执行。你可以通过调用 dlazy CLI 的各类生成模型（如 dlazy seedream-4.5 等）来完成实际的图片渲染。注意：Windows PowerShell 中不允许使用 `&` 或 `&&` 进行命令串联或后台运行，请单独且同步地执行命令。"}}
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

- **CLI 源代码**: [github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.2.3 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.3`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理 (How It Works)

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。

# Logo 品牌设计系统 Logo Branding System

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A professional pipeline for building everything from a core mark to a complete brand visual system, ensuring creative quality, execution consistency, and shippable delivery.

## Core Principles

1. Stepwise execution
   - Use a progressive flow; never dump large outputs in one shot.
   - When a single plan exceeds 2 images, submit the execution plan and wait for confirmation before generating.
   - Upstream assets must be confirmed before downstream applications proceed.
2. Object consistency
   - The same brand element stays strictly consistent across all applications.
   - When deriving variants from an existing image, the goal is to replicate consistency, not to reinterpret.
3. User assets first
   - Reference images, logos, and assets provided by the user have the highest priority.
   - Strictly separate visual style from textual content; the brand name uses what the user specifies.

## Execution Framework

### Step 0: Task Planning (Mandatory)

Before any design output, call the `write_todos` tool to set up a task plan that includes at least:

- Gather requirements and boundaries
- Design the core logo concept
- Generate derivatives and the brand system
- Phase confirmation and iterative correction

Execution rules:

- Keep only one task `in_progress`; the rest are `pending`.
- Update `write_todos` status as soon as each phase finishes.
- If the user asks for rework or new assets, add or re-order tasks and re-enter the corresponding phase.

### Step A: Gather Requirements

You must confirm:

- Brand name
- Industry or product category
- Component scope (logo only, or with derivatives)

Component definitions:

- Logo: the core brand mark
- Derivatives: real-world applications based on the brand mark

### Step B: Establish the Core Mark

New mark design follows:

- Single focus: one central element, no background or decorative interference
- Symbolic abstraction: distill to the most recognizable form
- Clear silhouette: high-contrast outline, well-defined edges
- Default 1K resolution

Concept rules:

- For open-ended requests, default to 4 distinct design directions
- Present each concept individually, not as a tile grid
- Each concept comes with a 100–200 word design rationale
- Wait for user confirmation before proceeding

### Step C: Create Derivatives

Possible directions:

1. Mark variants
   - Structural variants: lettermark, wordmark, symbol mark, combination mark
   - Layout or orientation variants
   - Color variants
   - Size and use-case variants
2. Brand patterns and supporting graphics
   - Generate independent, reusable graphic assets
3. Physical applications
   - Business cards and stationery
   - Packaging and merchandise
   - Environmental signage and wayfinding
4. Social-media assets
   - Generate ready-to-post final images
5. Brand identity system
   - Brand core (story, pillars, voice)
   - Logo system
   - Color system
   - Typography system
   - Visual language
   - Application examples

Application design principles:

- Place the mark with restraint; avoid oversized, dead-center placements
- Deconstruct brand elements into patterns, icons, color blocks
- Use whitespace to organize visual hierarchy
- Emphasize material and texture experience

## Phase Confirmation and Rollback Rules

- Confirm at the end of every step before continuing.
- When the user adjusts an intermediate result, return to the corresponding upstream step first, then sync downstream assets.
- If the user supplies new reference assets, immediately reset the consistency baseline and unify subsequent outputs.

## Output Format

- Requirements summary
- Current-phase deliverable
- Next-step plan and items awaiting confirmation
- Current todo status (phase, completed, pending)

## Key Value

- Progressive workflow that lowers rework cost
- Multi-direction concept exploration that improves decision quality
- End-to-end consistency control that strengthens brand recognition
- Integrated delivery from logo to brand system


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

---
name: image-amazon-product-image-suite
version: 1.2.0
description: A professional product image generation skill purpose-built for the Amazon e-commerce platform. Outputs comply with Amazon's image guidelines while optimizing for click-through and conversio
triggers:
  - Amazon Product Image Suite
  - Amazon detail-page main and secondary image design
  - Product infographics, lifestyle shots, and detail shots
  - A+ Brand Content page modules
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

# Amazon Product Image Suite

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A professional product image generation skill purpose-built for the Amazon e-commerce platform. Outputs comply with Amazon's image guidelines while optimizing for click-through and conversion.

## Core Deliverables

This skill covers the full visual system of an Amazon product detail page:

- Main image (1): pure-white background, complies with Amazon's mandatory rules
- Secondary images (6): infographics, multi-angle shots, lifestyle scenes, detail close-ups, etc.
- A+ page (8): brand story, selling-point showcase, usage instructions, and other modules

## Applicable Scenarios

- Amazon detail-page main and secondary image design
- Product infographics, lifestyle shots, and detail shots
- A+ Brand Content page modules

## Step 0: Task Planning (Mandatory)

Before any output, call `write_todos` to set up a task plan that includes at least:

- Confirm output scope and image count
- Generate and lock in the main-image visual baseline
- Generate secondary images and converge on style consistency
- Generate A+ modules and complete the full delivery

Execution rules:

- Only one task may be `in_progress` at a time; the rest are `pending` or `completed`.
- Update `write_todos` status as soon as each phase finishes.
- When the user requests rework, redesign, or new assets, add or re-order tasks and return to the corresponding phase.

## Adaptive Execution Flow

Pick the delivery path based on the user's request:

- Full suite: main (1) + secondary (6) + A+ (8) = 12–17 images
- Product images only: main (1) + secondary (6) = 7 images
- A+ page only: A+ modules = 8 images
- Unclear request: generate the main image first, then propose secondary and A+ plans

Generation order principles:

1. Confirm the image plan and count
2. Produce the main image first (establish the visual baseline)
3. Generate secondary images derived from the main image (preserve consistency)
4. Generate A+ content (if required)

## Image Specifications

### General Requirements

- Minimum size: 1000px × 1000px
- Standard ratio: 1:1 (main and secondary)
- Mobile text: at least 30pt

### Main Image Mandatory Rules

Must satisfy:

- Pure-white background: RGB(255, 255, 255)
- Product fills at least 85% of the frame
- Real-product photo quality
- Product fully centered with even lighting

Forbidden:

- Text, logos, or watermarks
- Decorative graphics or misleading accessories
- Mannequins for apparel

## Secondary Image Types

| Type             | Purpose                                       | Design Notes                                                                    |
| ---------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| Infographic      | Highlight selling points / feature comparison | 4–6 selling points, callout lines pointing to features, icons reinforce visuals |
| Multi-angle      | Show the product from different angles        | Consistent lighting, clean backgrounds, usually 2 shots                         |
| Detail close-up  | Show materials and craftsmanship              | Macro composition, emphasize texture                                            |
| Lifestyle        | Show real usage scenarios                     | Target user in a real environment, usually 2 shots                              |
| Variant showcase | Show color or style options                   | All variants arranged with consistent layout and scale                          |
| Package contents | Show what's in the box                        | All accessories complete and clearly identifiable                               |
| Size reference   | Show real-world size                          | Use a familiar object as a scale reference                                      |

## A+ Page Module Structure (8 modules)

1. Hero banner (21:9): brand presence
2. Pain point / scenario (3:2): build empathy
3. Selling-point / feature matrix (3:2): core advantages
4. Key ingredients / technology (3:2): technical credibility
5. Efficacy data / comparison (3:2): proof
6. How to use (3:2): operating guidance
7. Variants / family shot (3:2): product line
8. Brand endorsements / certifications (21:9): trust building

A+ design notes:

- Embedded text should be larger than 30pt (still legible after platform compression)
- Keep critical info out of the outer 5% margin (handles mobile cropping)
- Maintain narrative continuity across modules; avoid abrupt jumps

## Conversion Reference Strategy

- Lifestyle shots: typical lift around +18%
- Infographics: typical lift around +8%
- Detail close-ups: typical lift around +6%
- 7 images vs. 4 images: typical lift around +32%
- Optimized image mix: engagement lift up to +30%

These figures are priority hints, not guarantees.

## Multi-Image Consistency Rules

- Main first: always produce the main image before everything else
- Reference the main: derive secondary images and A+ from the main image as the visual anchor
- Appearance consistency: keep colors, materials, and structural details aligned
- Style consistency: unify background language, palette, fonts, and icon style

## Execution Plan

When the skill is invoked, drive the work forward in this order:

1. Confirm output scope: full suite / product images only / A+ only
2. Collect product info: photo or description, core selling points, target audience
3. Generate the main image: lock in the visual and material baseline
4. Generate secondary images one by one: pick image types based on goals and deliver each
5. Generate the A+ page: build a brand narrative across the 8 modules
6. Iterate: adjust composition, copy hierarchy, and information density based on feedback

## Output Format

- Current phase and target deliverable
- Image checklist (done / pending)
- Main-image consistency check verdict
- Next item awaiting confirmation
- Current todo status (phase, completed items, pending items)

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
